import { Routes, Route, Navigate } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { DashboardPage } from "@/pages/DashboardPage";
import { ScriptsPage } from "@/pages/ScriptsPage";
import { AssetsPage } from "@/pages/AssetsPage";
import { ReviewsPage } from "@/pages/ReviewsPage";
import { TasksPage } from "@/pages/TasksPage";
import { LoginPage } from "@/pages/LoginPage";

function App() {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <div className="layout-sidebar">
      <Sidebar />
      <main className="p-6 overflow-auto">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/scripts/*" element={<ScriptsPage />} />
          <Route path="/assets/*" element={<AssetsPage />} />
          <Route path="/reviews/*" element={<ReviewsPage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
