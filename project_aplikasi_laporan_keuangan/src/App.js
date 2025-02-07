import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom'; // Ganti BrowserRouter dengan HashRouter
import Login from './components/LoginPage';
import Dashboard from './components/DashboardPage';
import TableManager from './components/TableManager';
import AdminDashboard from './components/AdminDashboard';
import ResetPassword from './components/ResetPassword';
import ResetPasswordForm from './components/ResetPasswordForm';
import UploadPage from './components/FinancialDocumentGenerator';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';

function App() {
  return (
    <AuthProvider>
      <HashRouter> {/* Menggunakan HashRouter */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/reset-password/:token" element={<ResetPasswordForm />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute allowedRoles={['camat', 'sekcam', 'keuangan', 'kepegawaian', 'pemerintahan', 'pembangunan', 'perekonomian', 'pelayanan', 'tantrib']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/upload/:sectionId"
            element={
              <ProtectedRoute allowedRoles={['camat', 'sekcam', 'keuangan', 'kepegawaian', 'pemerintahan', 'pembangunan', 'perekonomian', 'pelayanan', 'tantrib']}>
                <UploadPage />
              </ProtectedRoute>
            }
          />
          <Route path="/table-manager" element={<TableManager />} />
        </Routes>
      </HashRouter>
    </AuthProvider>
  );
}

export default App;