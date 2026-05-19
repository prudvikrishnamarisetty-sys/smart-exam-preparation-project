import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

// ── Helper: fetch with auto-retry (up to `retries` times, `delay` ms apart) ──
async function fetchWithRetry(fn, retries = 3, delay = 2000) {
  let lastErr;
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      console.warn(`[Dashboard] Fetch attempt ${i + 1}/${retries} failed at ${new Date().toISOString()}:`, err.message);
      if (i < retries - 1) await new Promise(r => setTimeout(r, delay));
    }
  }
  throw lastErr;
}

const CACHE_KEY = 'smartexam_dash_cache';

export default function Dashboard() {
  const [stats, setStats]     = useState(null);
  const [user, setUser]       = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState('');
  const [fromCache, setFromCache] = useState(false);

  const loadDashboard = useCallback(() => {
    setLoading(true);
    setError('');
    setFromCache(false);

    fetchWithRetry(() => Promise.all([api.getDashboard(), api.me()]))
      .then(([s, u]) => {
        setStats(s);
        setUser(u);
        // Persist for offline fallback
        try { localStorage.setItem(CACHE_KEY, JSON.stringify({ stats: s, user: u, ts: Date.now() })); }
        catch (_) {}
      })
      .catch(err => {
        console.error('[Dashboard] All retries exhausted:', err);
        // Try localStorage fallback
        try {
          const raw = localStorage.getItem(CACHE_KEY);
          if (raw) {
            const cached = JSON.parse(raw);
            setStats(cached.stats);
            setUser(cached.user);
            setFromCache(true);
            return;
          }
        } catch (_) {}
        setError(err.message || 'Failed to load dashboard data');
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { loadDashboard(); }, [loadDashboard]);

  if (loading) return (
    <div className="loader">
      <div className="spinner"></div>
      <p style={{ color: 'var(--text-muted)', marginTop: '1rem', fontSize: '0.9rem' }}>
        Loading dashboard…
      </p>
    </div>
  );

  // Error state (no cache either)
  if (error) return (
    <div className="page fade-in" style={{ maxWidth: 600, margin: '4rem auto', textAlign: 'center' }}>
      <div className="card" style={{ padding: '3rem 2rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚠️</div>
        <h2 style={{ marginBottom: '0.75rem' }}>Dashboard Unavailable</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>{error}</p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button className="btn btn-primary" onClick={loadDashboard}>🔄 Retry</button>
          <Link to="/exams" className="btn btn-secondary">📝 Go to Exams</Link>
        </div>
      </div>
    </div>
  );

  if (!stats) return (
    <div className="page fade-in" style={{ maxWidth: 600, margin: '4rem auto', textAlign: 'center' }}>
      <div className="card" style={{ padding: '3rem 2rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎓</div>
        <h2 style={{ marginBottom: '0.75rem' }}>Welcome!</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>No exam data yet. Start your first exam to see analytics here.</p>
        <Link to="/exams" className="btn btn-primary btn-lg">Browse Exams →</Link>
      </div>
    </div>
  );

  const trendData    = (stats.performance_trend || []).slice().reverse().map((t, i) => ({
    name: `#${i + 1}`, percentage: t.percentage, score: t.score,
  }));
  const examWiseData = (stats.exam_wise_stats   || []).map(e => ({
    name: e.exam_type?.replace(/_/g, ' '), avg: e.avg_percentage, best: e.best_percentage, tests: e.exams_taken,
  }));

  return (
    <div className="page fade-in">

      {/* ── Cache banner ──────────────────────────────────────────────── */}
      {fromCache && (
        <div style={{
          background: 'rgba(234,179,8,0.12)', border: '1px solid rgba(234,179,8,0.35)',
          borderRadius: '0.6rem', padding: '0.6rem 1.2rem', marginBottom: '1.25rem',
          display: 'flex', alignItems: 'center', gap: '0.75rem',
        }}>
          <span style={{ fontSize: '1.1rem' }}>⚡</span>
          <span style={{ color: '#fbbf24', fontSize: '0.9rem' }}>
            Live data syncing… Showing last known results.
          </span>
          <button className="btn btn-sm btn-secondary" style={{ marginLeft: 'auto' }} onClick={loadDashboard}>
            🔄 Refresh
          </button>
        </div>
      )}

      {/* ── Header ───────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', marginBottom: '0.25rem' }}>
            👋 Hello, {user?.full_name || user?.username || 'Student'}!
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>
            {user?.college ? `📍 ${user.college}  •  ` : ''}{user?.email}
          </p>
        </div>
        <Link to="/profile" className="btn btn-secondary" style={{ whiteSpace: 'nowrap' }}>✏️ Edit Profile</Link>
      </div>

      {/* ── Stat Cards ───────────────────────────────────────────────── */}
      <div className="card-grid" style={{ marginBottom: '2rem' }}>
        <div className="stat-card">
          <span className="stat-label">Total Exams</span>
          <span className="stat-value">{stats.total_exams}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Avg Score</span>
          <span className="stat-value">{stats.avg_percentage}%</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Best Score</span>
          <span className="stat-value">{stats.best_score}%</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Questions Attempted</span>
          <span className="stat-value">{stats.total_questions_attempted}</span>
        </div>
      </div>

      {stats.total_exams === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <h2 style={{ marginBottom: '1rem' }}>No exams taken yet!</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            Start your preparation by taking your first exam.
          </p>
          <Link to="/exams" className="btn btn-primary btn-lg">Browse Exams</Link>
        </div>
      ) : (
        <>
          {/* ── Charts ─────────────────────────────────────────────── */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
            {trendData.length > 0 && (
              <div className="chart-container">
                <h3>📈 Performance Trend</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="name" stroke="#6868a0" fontSize={12} />
                    <YAxis stroke="#6868a0" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#1a1a3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                    <Line type="monotone" dataKey="percentage" stroke="#7c5cfc" strokeWidth={3} dot={{ fill: '#7c5cfc', r: 5 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
            {examWiseData.length > 0 && (
              <div className="chart-container">
                <h3>📊 Performance by Exam Type</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={examWiseData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="name" stroke="#6868a0" fontSize={11} angle={-20} textAnchor="end" height={60} />
                    <YAxis stroke="#6868a0" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#1a1a3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                    <Bar dataKey="avg"  fill="#7c5cfc" radius={[4,4,0,0]} name="Avg %"  />
                    <Bar dataKey="best" fill="#22c55e" radius={[4,4,0,0]} name="Best %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* ── Subject Cards ─────────────────────────────────────── */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {stats.strong_subjects?.length > 0 && (
              <div className="card">
                <h3 style={{ marginBottom: '1rem' }}>💪 Strong Subjects</h3>
                {stats.strong_subjects.map((s, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span className="badge badge-success">Strong</span>
                    <span>{s}</span>
                  </div>
                ))}
              </div>
            )}
            {stats.weak_subjects?.length > 0 && (
              <div className="card">
                <h3 style={{ marginBottom: '1rem' }}>📖 Needs Improvement</h3>
                {stats.weak_subjects.map((s, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span className="badge badge-warning">Weak</span>
                    <span>{s}</span>
                  </div>
                ))}
              </div>
            )}
            <div className="card">
              <h3 style={{ marginBottom: '1rem' }}>🕐 Recent Results</h3>
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Exam</th><th>Score</th><th>%</th></tr></thead>
                  <tbody>
                    {stats.recent_results?.map((r, i) => (
                      <tr key={i}>
                        <td><Link to={`/results/${r.exam_id}`}>Exam #{r.exam_id}</Link></td>
                        <td>{r.correct}/{r.total}</td>
                        <td>
                          <span className={`badge ${r.percentage >= 60 ? 'badge-success' : r.percentage >= 40 ? 'badge-warning' : 'badge-danger'}`}>
                            {r.percentage}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
