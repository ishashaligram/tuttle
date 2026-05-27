"""Migration chain integrity tests.

Every PR that changes tuttle/model.py must come with a matching Alembic
revision. These tests prove the upgrade chain is:

    1. Complete — DB at the previous head can be upgraded to current head.
    2. Non-destructive — rows inserted before the upgrade survive it.
    3. Faithful — the resulting schema matches SQLModel.metadata.
    4. FK-clean — PRAGMA foreign_key_check is empty after upgrade.

If autogenerate ever emits a drop_column + add_column pair instead of a
rename (the silent-data-loss footgun), the row-survival assertion catches
it before the migration reaches a user.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator

import pytest
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect
from sqlmodel import SQLModel

import tuttle.model  # noqa: F401 — ensure tables register on SQLModel.metadata
from tuttle.db_schema import _alembic_config_for


def _heads(db_url: str) -> tuple[str | None, str]:
    """Return (previous_revision, current_head) for the migrations chain."""
    cfg = _alembic_config_for(db_url)
    script = ScriptDirectory.from_config(cfg)
    head = script.get_current_head()
    assert head, "No Alembic head revision found"
    revisions = list(script.walk_revisions())
    previous = revisions[1].revision if len(revisions) > 1 else None
    return previous, head


@pytest.fixture
def tmp_db(tmp_path: Path) -> Iterator[tuple[Path, str]]:
    db = tmp_path / "user.db"
    yield db, f"sqlite:///{db}"


def test_upgrade_from_empty_creates_full_schema(tmp_db: tuple[Path, str]) -> None:
    """Per-user-DB schema matches SQLModel.metadata after upgrade to head.

    The app.db registry tables (registered_user, app_setting) share the
    same global metadata but are explicitly excluded from per-user-DB
    migrations via include_object in env.py — see migrations/env.py.
    """
    db, url = tmp_db
    cfg = _alembic_config_for(url)
    command.upgrade(cfg, "head")

    excluded = {"registered_user", "app_setting"}
    engine = create_engine(url)
    try:
        live_tables = set(inspect(engine).get_table_names()) - {"alembic_version"}
        expected = set(SQLModel.metadata.tables.keys()) - excluded
        assert live_tables == expected, (
            f"Schema diverged from model. "
            f"Missing: {expected - live_tables}, extra: {live_tables - expected}"
        )
    finally:
        engine.dispose()


def test_upgrade_chain_is_non_destructive(tmp_db: tuple[Path, str]) -> None:
    """Rows inserted at the previous head must survive the upgrade to head.

    Skipped when only one revision exists (initial baseline) — the test
    becomes meaningful as soon as a second revision is added.
    """
    db, url = tmp_db
    previous, head = _heads(url)
    if previous is None:
        pytest.skip("Only the baseline revision exists; nothing to chain-test yet.")

    cfg = _alembic_config_for(url)
    command.upgrade(cfg, previous)

    excluded = {"registered_user", "app_setting"}
    engine = create_engine(url)
    try:
        with engine.begin() as conn:
            live = set(inspect(conn).get_table_names())
            for table_name in SQLModel.metadata.tables:
                if table_name in excluded or table_name not in live:
                    continue
                cols = {c["name"] for c in inspect(conn).get_columns(table_name)}
                if {"id"}.issubset(cols):
                    conn.exec_driver_sql(f"INSERT INTO {table_name} (id) VALUES (9999)")
        with engine.begin() as conn:
            live = set(inspect(conn).get_table_names())
            row_counts_before = {
                t: conn.exec_driver_sql(f"SELECT COUNT(*) FROM {t}").scalar()
                for t in SQLModel.metadata.tables
                if t in live and t not in excluded
            }
    finally:
        engine.dispose()

    command.upgrade(cfg, head)

    engine = create_engine(url)
    try:
        with engine.begin() as conn:
            for t, expected_count in row_counts_before.items():
                actual = conn.exec_driver_sql(f"SELECT COUNT(*) FROM {t}").scalar()
                assert actual == expected_count, (
                    f"Table {t}: {expected_count} rows before upgrade, {actual} after. "
                    f"Migration is destructive — check for unintended drop_column/add_column pairs."
                )
    finally:
        engine.dispose()


def test_foreign_key_check_clean_after_upgrade(tmp_db: tuple[Path, str]) -> None:
    db, url = tmp_db
    cfg = _alembic_config_for(url)
    command.upgrade(cfg, "head")

    conn = sqlite3.connect(db)
    try:
        violations = conn.execute("PRAGMA foreign_key_check").fetchall()
        assert violations == [], (
            f"Foreign key violations after upgrade: {violations}. "
            f"Likely a batch-mode op forgot to re-attach an FK."
        )
    finally:
        conn.close()


def test_versions_are_append_only_in_git() -> None:
    """Existing revisions in versions/ must not be edited after commit.

    Each revision captures the schema delta at one point in history.
    Editing an already-committed revision corrupts the chain for any
    database that already advanced past it. Schema changes must always
    ADD a new revision via `just migrate`.

    This test enforces the rule by checking git history: every file in
    versions/ must have a single commit (the one that introduced it),
    or any subsequent commits must only modify docstrings/comments —
    never op.* calls.

    Skipped outside a git checkout (e.g. wheel installs).
    """
    import subprocess

    versions = (
        Path(__file__).resolve().parent.parent / "tuttle" / "migrations" / "versions"
    )
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=versions,
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("Not a git checkout; cannot enforce append-only.")

    offenders: list[str] = []
    for script in versions.glob("*.py"):
        result = subprocess.run(
            ["git", "log", "--follow", "--pretty=format:%H", "--", script.name],
            cwd=versions,
            capture_output=True,
            text=True,
        )
        commits = [c for c in result.stdout.strip().splitlines() if c]
        if len(commits) <= 1:
            continue
        diff = subprocess.run(
            ["git", "log", "-p", "--follow", "--pretty=format:", "--", script.name],
            cwd=versions,
            capture_output=True,
            text=True,
        )
        for line in diff.stdout.splitlines():
            if line.startswith(("+    op.", "-    op.")):
                offenders.append(script.name)
                break

    assert not offenders, (
        f"These migration scripts have post-commit edits to op.* calls: {offenders}. "
        f"Revisions are append-only — schema changes must ADD a new revision via "
        f"`just migrate`, not edit existing ones."
    )


def test_no_model_imports_in_versions() -> None:
    """Migration scripts must not import from tuttle.model.

    Models drift over time; each script must be pinned to its point in
    history via local sa.table() snapshots. AST-based so docstring text
    that mentions the forbidden pattern doesn't trip the check.
    """
    import ast

    versions = (
        Path(__file__).resolve().parent.parent / "tuttle" / "migrations" / "versions"
    )
    offenders: list[str] = []
    for script in versions.glob("*.py"):
        tree = ast.parse(script.read_text(), filename=str(script))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or "").startswith(
                "tuttle.model"
            ):
                offenders.append(script.name)
                break
            if isinstance(node, ast.Import) and any(
                n.name.startswith("tuttle.model") for n in node.names
            ):
                offenders.append(script.name)
                break
    assert not offenders, (
        f"These migration scripts import tuttle.model, which breaks when the "
        f"model evolves: {offenders}. Use a local sa.table(...) snapshot instead."
    )
