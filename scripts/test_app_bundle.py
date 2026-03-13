"""Smoke-test for the packaged app bundle.

Launches the platform-specific executable produced by ``flet pack``
(via ``scripts/pack_app.py``) and verifies it survives initial startup
without crashing.

Usage:
    uv run python scripts/test_app_bundle.py          # test only
    uv run python scripts/test_app_bundle.py --build   # build then test
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import typer
from loguru import logger

APP_NAME = "Tuttle"
DIST_DIR = Path(__file__).resolve().parent.parent / "dist"
STARTUP_WAIT_SECONDS = 8


def _find_executable() -> Path:
    if sys.platform.startswith("darwin"):
        exe = DIST_DIR / f"{APP_NAME}.app" / "Contents" / "MacOS" / APP_NAME
    elif sys.platform.startswith("win"):
        exe = DIST_DIR / f"{APP_NAME}.exe"
    else:
        exe = DIST_DIR / APP_NAME
    return exe


def _build():
    logger.info("Building app bundle ...")
    result = subprocess.run(
        [sys.executable, "scripts/pack_app.py"],
        cwd=DIST_DIR.parent,
    )
    if result.returncode != 0:
        logger.error(f"Build failed with exit code {result.returncode}")
        raise typer.Exit(code=1)
    logger.info("Build succeeded")


def _launch_and_check(exe: Path) -> bool:
    """Return True if the app survives startup without crashing."""
    logger.info(f"Launching {exe}")
    env = {**os.environ, "LANG": "C"}  # simulate .app bundle locale

    proc = subprocess.Popen(
        [str(exe)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        env=env,
    )

    try:
        logger.info(f"Waiting {STARTUP_WAIT_SECONDS}s for startup ...")
        time.sleep(STARTUP_WAIT_SECONDS)
        exit_code = proc.poll()

        if exit_code is not None:
            _, stderr = proc.communicate(timeout=5)
            logger.error(
                f"App crashed during startup (exit code {exit_code})\n"
                f"stderr:\n{stderr.decode(errors='replace')}"
            )
            return False

        logger.info("App is still running after startup — smoke test passed")
        return True

    finally:
        try:
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGTERM)
            proc.wait(timeout=5)
        except (ProcessLookupError, ChildProcessError, subprocess.TimeoutExpired):
            try:
                proc.kill()
                proc.wait(timeout=3)
            except Exception:
                pass
        logger.info("App process terminated")


def main(
    build: bool = typer.Option(False, "--build", "-b", help="Build before testing"),
):
    if build:
        _build()

    exe = _find_executable()
    if not exe.exists():
        logger.error(
            f"Executable not found at {exe}\n" "Run with --build or `make pack` first."
        )
        raise typer.Exit(code=1)

    ok = _launch_and_check(exe)
    raise typer.Exit(code=0 if ok else 1)


if __name__ == "__main__":
    typer.run(main)
