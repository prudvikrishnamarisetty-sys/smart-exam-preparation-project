import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';

export default function Login({ onLogin }) {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await api.login(form);
      onLogin(data);
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper fade-in">
      {/* LEFT PANE: Branding / Graphic */}
      <div className="login-graphic">
        <div className="glass-panel">
          <h1>Smart Examination Platform</h1>
          <p>
            Welcome to the next generation of competitive exam preparation. 
            AI-driven insights, real-time analytics, and thousands of curated questions.
          </p>
          <div className="graphic-features">
            <div className="graphic-feature">🧠 Adaptive AI Engine</div>
            <div className="graphic-feature">📊 Live Performance Metrics</div>
            <div className="graphic-feature">📚 Instant Study Resources</div>
          </div>
        </div>
      </div>

      {/* RIGHT PANE: Auth Form */}
      <div className="login-form-container">
        <div className="login-form-box">
          <div className="login-header">
            <h2>Welcome Back</h2>
            <p>Sign in to continue your preparation journey</p>
          </div>

          {error && <div className="alert alert-error">{error}</div>}
          
          <form onSubmit={handleSubmit} className="premium-form">
            <div className="form-group floating-group">
              <input 
                type="text" 
                id="username"
                className="floating-input"
                value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })} 
                placeholder=" "
                required 
              />
              <label htmlFor="username" className="floating-label">Username</label>
            </div>
            
            <div className="form-group floating-group">
              <input 
                type="password" 
                id="password"
                className="floating-input"
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })} 
                placeholder=" "
                required 
              />
              <label htmlFor="password" className="floating-label">Password</label>
            </div>
            
            <button className="btn-gradient" disabled={loading}>
              {loading ? <span className="spinner-small"></span> : 'Sign In'}
            </button>
          </form>
          
          <p className="auth-toggle">
            Don't have an account? <Link to="/register"><span>Sign up now</span></Link>
          </p>
        </div>
      </div>
    </div>
  );
}
