import { useState, useCallback, useMemo } from "react";
import { Sidebar } from "./Sidebar";
import { DashboardView } from "../dashboard/DashboardView";
import { ProjectsView } from "../business/ProjectsView";
import { ClientsView } from "../business/ClientsView";
import { ContractsView } from "../business/ContractsView";
import { InvoicingView } from "../invoicing/InvoicingView";
import { ContactsView } from "../contacts/ContactsView";
import { SettingsView } from "../settings/SettingsView";
import { PlaceholderView } from "../shared/PlaceholderView";
import { NavigationContext, type NavigationFilter } from "../shared/NavigationContext";
import { rpc } from "../../api/rpc";
import { Database } from "lucide-react";

export function Shell() {
  const [selected, setSelected] = useState("dashboard");
  const [collapsed, setCollapsed] = useState(false);
  const [installingDemo, setInstallingDemo] = useState(false);
  const [navFilter, setNavFilter] = useState<NavigationFilter>({});

  const navigate = useCallback((view: string, filter?: NavigationFilter) => {
    setNavFilter(filter || {});
    setSelected(view);
  }, []);

  function handleSidebarSelect(id: string) {
    setNavFilter({});
    setSelected(id);
  }

  const navContext = useMemo(() => ({ navigate, filter: navFilter }), [navigate, navFilter]);

  async function installDemo() {
    setInstallingDemo(true);
    await rpc("demo.install", { n_projects: 4 });
    setInstallingDemo(false);
    setSelected("dashboard");
    window.location.reload();
  }

  return (
    <NavigationContext.Provider value={navContext}>
      <div className="flex h-screen w-screen bg-bg-content text-primary">
        <Sidebar selected={selected} onSelect={handleSidebarSelect}
          collapsed={collapsed} onToggleCollapse={() => setCollapsed((c) => !c)} />
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="drag-region h-13 shrink-0 flex items-end justify-end px-4 pb-2">
            <button onClick={installDemo} disabled={installingDemo}
              className="no-drag flex items-center gap-1.5 text-xs text-muted hover:text-secondary transition-colors disabled:opacity-40"
              title="Install demo data">
              <Database size={13} />
              {installingDemo ? "Installing…" : "Demo Data"}
            </button>
          </div>
          <div className="flex-1 overflow-y-auto">
            <DetailView id={selected} />
          </div>
        </main>
      </div>
    </NavigationContext.Provider>
  );
}

function DetailView({ id }: { id: string }) {
  switch (id) {
    case "dashboard": return <DashboardView />;
    case "clients": return <ClientsView />;
    case "contracts": return <ContractsView />;
    case "projects": return <ProjectsView />;
    case "contacts": return <ContactsView />;
    case "invoicing": return <InvoicingView />;
    case "settings": return <SettingsView />;
    default: return <PlaceholderView title={id.charAt(0).toUpperCase() + id.slice(1)} />;
  }
}
