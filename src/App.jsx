import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { api } from './api/client';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ExamSelect from './pages/ExamSelect';
import ExamInstructions from './pages/ExamInstructions';
import ExamInterface from './pages/ExamInterface';
import Results from './pages/Results';
import Resources from './pages/Resources';
import AIAssistant from './pages/AIAssistant';
import EditProfile from './pages/EditProfile';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

function Navbar({ user, onLogout }) {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? 'active' : '';
  // Hide navbar on admin login page and exam interface
  if (location.pathname === '/admin/login') return null;

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">🎓 SmartExam Pro</Link>
      {user && (
        <div className="navbar-links">
          {!user.is_admin && (
            <>
              <Link to="/" className={isActive('/')}>Dashboard</Link>
              <Link to="/exams" className={isActive('/exams')}>Exams</Link>
              <Link to="/resources" className={isActive('/resources')}>Resources</Link>
              <Link to="/ai-assistant" className={isActive('/ai-assistant')}>AI Assistant</Link>
            </>
          )}
          {user.is_admin && (
            <Link to="/admin" className={isActive('/admin')} style={{ color: '#f59e0b' }}>🛡️ Admin</Link>
          )}
          <Link to="/profile" className={isActive('/profile')} style={{ color: 'var(--text-muted)' }}>✏️ Profile</Link>
          <button onClick={onLogout}>Logout</button>
        </div>
      )}
    </nav>
  );
}

function ProtectedRoute({ user, children }) {
  return user ? children : <Navigate to="/login" />;
}

function AdminRoute({ user, children }) {
  if (!user) return <Navigate to="/admin/login" />;
  if (!user.is_admin) return <Navigate to="/" />;
  return children;
}

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.me().then(u => setUser(u)).catch(() => localStorage.clear()).finally(() => setLoading(false));
    } else { setLoading(false); }
  }, []);

  const handleLogin = (data) => {
    localStorage.setItem('token', data.access_token);
    setUser(data.user);
  };

  const handleLogout = () => { localStorage.clear(); setUser(null); window.location.href = '/login'; };

  if (loading) return <div className="loader"><div className="spinner"></div></div>;

  return (
    <Router>
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/login" element={user ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} />
        <Route path="/register" element={user ? <Navigate to="/" /> : <Register onLogin={handleLogin} />} />
        <Route path="/admin/login" element={<AdminLogin onAdminLogin={handleLogin} />} />

        <Route path="/" element={<ProtectedRoute user={user}>{user && user.is_admin ? <Navigate to="/admin" /> : <Dashboard />}</ProtectedRoute>} />
        <Route path="/exams" element={<ProtectedRoute user={user}><ExamSelect /></ProtectedRoute>} />
        <Route path="/instructions/:examKey" element={<ProtectedRoute user={user}><ExamInstructions /></ProtectedRoute>} />
        <Route path="/exam/:examId" element={<ProtectedRoute user={user}><ExamInterface /></ProtectedRoute>} />
        <Route path="/results/:examId" element={<ProtectedRoute user={user}><Results /></ProtectedRoute>} />
        <Route path="/resources" element={<ProtectedRoute user={user}><Resources /></ProtectedRoute>} />
        <Route path="/ai-assistant" element={<ProtectedRoute user={user}><AIAssistant /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute user={user}><EditProfile /></ProtectedRoute>} />
        <Route path="/admin" element={<AdminRoute user={user}><AdminDashboard /></AdminRoute>} />
      </Routes>
    </Router>
  );
}
