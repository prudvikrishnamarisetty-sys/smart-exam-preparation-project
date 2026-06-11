import { useState, useEffect, useRef } from 'react';
import { api } from '../api/client';

const FILE_TYPE_ICON = { PDF: '📄', Image: '🖼️', Video: '🎬', Document: '📝' };

export default function AdminDashboard() {
  const [tab, setTab] = useState('users'); // 'users' | 'resources' | 'requests'

  // ─── Users state ───────────────────────────────────────────────────────────
  const [users, setUsers] = useState([]);
  const [usersLoading, setUsersLoading] = useState(true);
  const [userSearch, setUserSearch] = useState('');

  // ─── Resources state ───────────────────────────────────────────────────────
  const [resources, setResources] = useState([]);
  const [resLoading, setResLoading] = useState(false);
  const [examTypes, setExamTypes] = useState([]);
  const [uploadForm, setUploadForm] = useState({
    title: '', exam_type: '', exam_name: '', subject: '', description: '', tags: '',
  });
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [resSearch, setResSearch] = useState('');
  const fileInputRef = useRef(null);

  // ─── Requests state ────────────────────────────────────────────────────────
  const [requests, setRequests] = useState([]);
  const [reqLoading, setReqLoading] = useState(false);

  const [actionMsg, setActionMsg] = useState('');
  const [error, setError] = useState('');

  const showMsg = (msg) => { setActionMsg(msg); setTimeout(() => setActionMsg(''), 4000); };

  // ─── Load users ────────────────────────────────────────────────────────────
  const loadUsers = () => {
    setUsersLoading(true);
    setError('');
    api.adminGetUsers()
      .then(setUsers)
      .catch(err => setError(err.message))
      .finally(() => setUsersLoading(false));
  };

  // ─── Load resources & exam types ───────────────────────────────────────────
  const loadResources = () => {
    setResLoading(true);
    setError('');
    api.adminListResources()
      .then(setResources)
      .catch(err => setError(err.message))
      .finally(() => setResLoading(false));
  };

  useEffect(() => {
    loadUsers();
    api.adminGetResourceExamTypes().then(setExamTypes).catch(() => {});
  }, []);

  const loadRequests = () => {
    setReqLoading(true);
    api.adminGetRequests().then(setRequests).catch(console.error).finally(() => setReqLoading(false));
  };

  useEffect(() => {
    if (tab === 'resources') loadResources();
    if (tab === 'requests') loadRequests();
  }, [tab]);

  // ─── User actions ──────────────────────────────────────────────────────────
  const handleDeleteUser = async (u) => {
    if (!window.confirm(`Delete user "${u.username}"? This cannot be undone.`)) return;
    try {
      await api.adminDeleteUser(u.id);
      showMsg(`✅ User ${u.username} deleted`);
      loadUsers();
    } catch (err) { showMsg(`❌ ${err.message}`); }
  };

  const handleToggleAdmin = async (u) => {
    try {
      const res = await api.adminToggleAdmin(u.id);
      showMsg(`✅ ${u.username} is now ${res.is_admin ? 'an Admin' : 'a regular user'}`);
      loadUsers();
    } catch (err) { showMsg(`❌ ${err.message}`); }
  };

  const handleToggleActive = async (u) => {
    try {
      const res = await api.adminToggleActive(u.id);
      showMsg(`✅ ${u.username} is now ${res.is_active ? 'active' : 'deactivated'}`);
      loadUsers();
    } catch (err) { showMsg(`❌ ${err.message}`); }
  };

  // ─── Resource actions ──────────────────────────────────────────────────────
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadFile) { showMsg('❌ Please select a file'); return; }
    if (!uploadForm.title.trim()) { showMsg('❌ Title is required'); return; }
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append('file', uploadFile);
      Object.entries(uploadForm).forEach(([k, v]) => fd.append(k, v));
      const res = await api.adminUploadResource(fd);
      showMsg(`✅ "${res.title}" uploaded successfully`);
      setUploadForm({ title: '', exam_type: '', exam_name: '', subject: '', description: '', tags: '' });
      setUploadFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      loadResources();
    } catch (err) {
      showMsg(`❌ Upload failed: ${err.message}`);
    } finally { setUploading(false); }
  };

  const handleDeleteResource = async (r) => {
    if (!window.confirm(`Delete "${r.title}"?`)) return;
    try {
      await api.adminDeleteResource(r.id);
      showMsg(`✅ "${r.title}" deleted`);
      loadResources();
    } catch (err) { showMsg(`❌ ${err.message}`); }
  };

  const handleFulfillRequest = async (reqId) => {
    if (!window.confirm("Mark this request as fulfilled?")) return;
    try {
      await api.adminFulfillRequest(reqId);
      showMsg(`✅ Request marked as fulfilled`);
      loadRequests();
    } catch (err) { showMsg(`❌ ${err.message}`); }
  };

  const filteredUsers = users.filter(u =>
    u.username.toLowerCase().includes(userSearch.toLowerCase()) ||
    u.email.toLowerCase().includes(userSearch.toLowerCase()) ||
    (u.full_name || '').toLowerCase().includes(userSearch.toLowerCase())
  );

  const filteredResources = resources.filter(r =>
    !resSearch ||
    r.title.toLowerCase().includes(resSearch.toLowerCase()) ||
    (r.exam_name || '').toLowerCase().includes(resSearch.toLowerCase()) ||
    (r.exam_type || '').toLowerCase().includes(resSearch.toLowerCase()) ||
    (r.subject || '').toLowerCase().includes(resSearch.toLowerCase())
  );

  const stats = {
    total: users.length,
    admins: users.filter(u => u.is_admin).length,
    active: users.filter(u => u.is_active).length,
    totalExams: users.reduce((sum, u) => sum + (u.total_exams || 0), 0),
  };

  const selectedExamType = examTypes.find(e => e.exam_key === uploadForm.exam_type);

  return (
    <div className="page fade-in">
      <div className="page-header">
        <h1>🛡️ Admin Dashboard</h1>
        <p>Manage users, resources, and platform activity</p>
      </div>

      {/* Stats */}
      <div className="card-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', marginBottom: '2rem' }}>
        {[
          { label: 'Total Users', value: stats.total, icon: '👥' },
          { label: 'Admins', value: stats.admins, icon: '🛡️' },
          { label: 'Active Users', value: stats.active, icon: '✅' },
          { label: 'Total Exams Taken', value: stats.totalExams, icon: '📝' },
          { label: 'Resources Uploaded', value: resources.length, icon: '📁' },
          { label: 'Pending Requests', value: requests.filter(r => r.status === 'pending').length || 0, icon: '📬' },
        ].map((s, i) => (
          <div key={i} className="stat-card">
            <span style={{ fontSize: '2rem' }}>{s.icon}</span>
            <span className="stat-label">{s.label}</span>
            <span className="stat-value" style={{ fontSize: '2rem' }}>{s.value}</span>
          </div>
        ))}
      </div>

      {actionMsg && <div className={`alert ${actionMsg.startsWith('✅') ? 'alert-success' : 'alert-error'}`}>{actionMsg}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      {/* Tab Switcher */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        {[
          { key: 'users', label: '👥 Users' },
          { key: 'resources', label: '📁 Resources' },
          { key: 'requests', label: '📬 Material Requests' },
        ].map(t => (
          <button
            key={t.key}
            className={`btn ${tab === t.key ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ── USERS TAB ── */}
      {tab === 'users' && (
        <>
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <input value={userSearch} onChange={e => setUserSearch(e.target.value)}
              placeholder="🔍 Search by username, email, or name..." style={{ marginBottom: 0 }} />
          </div>
          {usersLoading ? <div className="loader"><div className="spinner"></div></div> : (
            <div className="card">
              <div style={{ overflowX: 'auto' }}>
                <table>
                  <thead><tr>
                    <th>ID</th><th>Name</th><th>Username</th><th>Email</th>
                    <th>College</th><th>Exams</th><th>Joined</th><th>Status</th><th>Actions</th>
                  </tr></thead>
                  <tbody>
                    {filteredUsers.map(u => (
                      <tr key={u.id} style={{ opacity: u.is_active ? 1 : 0.5 }}>
                        <td style={{ color: 'var(--text-muted)', fontFamily: 'monospace' }}>{u.id}</td>
                        <td>
                          <div style={{ fontWeight: 600 }}>{u.full_name || '—'}</div>
                          {u.is_admin && <span className="badge badge-warning" style={{ fontSize: '0.7rem' }}>Admin</span>}
                        </td>
                        <td style={{ color: 'var(--accent)', fontFamily: 'monospace' }}>@{u.username}</td>
                        <td style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{u.email}</td>
                        <td style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{u.college || '—'}</td>
                        <td style={{ textAlign: 'center', fontWeight: 700, color: 'var(--success)' }}>{u.total_exams}</td>
                        <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                          {u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}
                        </td>
                        <td>
                          <span className={`badge ${u.is_active ? 'badge-success' : 'badge-danger'}`}>
                            {u.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                            <button className="btn btn-secondary btn-sm" onClick={() => handleToggleAdmin(u)}>
                              {u.is_admin ? '⬇️ Demote' : '⬆️ Promote'}
                            </button>
                            <button className="btn btn-secondary btn-sm" onClick={() => handleToggleActive(u)}>
                              {u.is_active ? '🚫 Deactivate' : '✅ Activate'}
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteUser(u)}>🗑️ Delete</button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {filteredUsers.length === 0 && (
                  <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>
                    No users found matching "{userSearch}"
                  </p>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* ── RESOURCES TAB ── */}
      {tab === 'resources' && (
        <>
          {/* Upload Form */}
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ marginBottom: '1.5rem' }}>📤 Upload New Resource</h3>
            <form onSubmit={handleUpload}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    Title *
                  </label>
                  <input
                    value={uploadForm.title}
                    onChange={e => setUploadForm(f => ({ ...f, title: e.target.value }))}
                    placeholder="e.g. SSC CGL Maths PYQ 2024"
                    style={{ marginBottom: 0 }}
                    required
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    Exam Type
                  </label>
                  <select
                    value={uploadForm.exam_type}
                    onChange={e => {
                      const et = examTypes.find(x => x.exam_key === e.target.value);
                      setUploadForm(f => ({
                        ...f,
                        exam_type: e.target.value,
                        exam_name: et ? et.display_name : '',
                      }));
                    }}
                    style={{ marginBottom: 0 }}
                  >
                    <option value="">-- Select Exam --</option>
                    {['GOVT_IT','GOVT_NON_IT','BANKING','RAILWAY','DEFENCE','UPSC','TEACHING','STATE_PSC','BTECH_LANG','CORE_CS','CLOUD_DEVOPS','COMPANY'].map(cat => {
                      const group = examTypes.filter(e => e.category === cat);
                      if (!group.length) return null;
                      return (
                        <optgroup key={cat} label={cat.replace(/_/g, ' ')}>
                          {group.map(e => (
                            <option key={e.exam_key} value={e.exam_key}>
                              {e.icon} {e.display_name}
                            </option>
                          ))}
                        </optgroup>
                      );
                    })}
                  </select>
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    Subject / Section
                  </label>
                  <input
                    value={uploadForm.subject}
                    onChange={e => setUploadForm(f => ({ ...f, subject: e.target.value }))}
                    placeholder="e.g. Quantitative Aptitude"
                    style={{ marginBottom: 0 }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    Tags (comma separated)
                  </label>
                  <input
                    value={uploadForm.tags}
                    onChange={e => setUploadForm(f => ({ ...f, tags: e.target.value }))}
                    placeholder="e.g. PYQ, 2024, Maths, SSC"
                    style={{ marginBottom: 0 }}
                  />
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  Description
                </label>
                <textarea
                  value={uploadForm.description}
                  onChange={e => setUploadForm(f => ({ ...f, description: e.target.value }))}
                  placeholder="Brief description of the resource..."
                  style={{ width: '100%', minHeight: 70, background: 'var(--card-bg)', border: '1px solid var(--border)', borderRadius: '0.5rem', padding: '0.75rem', color: 'var(--text-main)', fontSize: '0.9rem', resize: 'vertical' }}
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  File * (PDF, Image, Word Doc — max 50 MB)
                </label>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png,.gif,.webp,.mp4,.doc,.docx"
                  onChange={e => setUploadFile(e.target.files[0] || null)}
                  style={{ marginBottom: 0 }}
                  required
                />
                {uploadFile && (
                  <p style={{ fontSize: '0.8rem', color: 'var(--success)', marginTop: '0.3rem' }}>
                    ✅ {uploadFile.name} ({(uploadFile.size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                )}
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={uploading}
                style={{ minWidth: 160 }}
              >
                {uploading ? '⏳ Uploading…' : '📤 Upload Resource'}
              </button>
            </form>
          </div>

          {/* Resources List */}
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0 }}>📁 Uploaded Resources ({resources.length})</h3>
              <input
                value={resSearch}
                onChange={e => setResSearch(e.target.value)}
                placeholder="🔍 Search resources..."
                style={{ marginBottom: 0, maxWidth: 260 }}
              />
            </div>

            {resLoading ? (
              <div style={{ textAlign: 'center', padding: '2rem' }}><div className="spinner" style={{ margin: '0 auto' }}></div></div>
            ) : filteredResources.length === 0 ? (
              <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>
                {resources.length === 0 ? 'No resources uploaded yet. Use the form above to add the first one!' : `No resources matching "${resSearch}"`}
              </p>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table>
                  <thead><tr>
                    <th>Type</th><th>Title</th><th>Exam</th><th>Subject</th><th>Tags</th><th>Uploaded</th><th>Actions</th>
                  </tr></thead>
                  <tbody>
                    {filteredResources.map(r => (
                      <tr key={r.id}>
                        <td style={{ textAlign: 'center', fontSize: '1.3rem' }} title={r.file_type}>
                          {FILE_TYPE_ICON[r.file_type] || '📎'}
                        </td>
                        <td>
                          <div style={{ fontWeight: 600, color: 'var(--text-main)' }}>{r.title}</div>
                          {r.description && <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>{r.description.slice(0, 60)}{r.description.length > 60 ? '…' : ''}</div>}
                        </td>
                        <td>
                          <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{r.exam_name || r.exam_type || '—'}</div>
                          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.exam_type}</div>
                        </td>
                        <td style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{r.subject || '—'}</td>
                        <td style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{r.tags || '—'}</td>
                        <td style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                          {r.created_at ? new Date(r.created_at).toLocaleDateString() : '—'}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.4rem' }}>
                            {r.has_file && (
                              <a
                                href={api.downloadResource(r.id)}
                                target="_blank"
                                rel="noreferrer"
                                className="btn btn-secondary btn-sm"
                                style={{ textDecoration: 'none' }}
                              >
                                👁️ View
                              </a>
                            )}
                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteResource(r)}>
                              🗑️ Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}
      {/* ── REQUESTS TAB ── */}
      {tab === 'requests' && (
        <div className="card">
          <h3 style={{ marginBottom: '1.5rem' }}>📬 User Material Requests</h3>
          {reqLoading ? (
            <div className="loader"><div className="spinner"></div></div>
          ) : requests.length === 0 ? (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>No material requests found.</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead><tr>
                  <th>User</th><th>Exam</th><th>Subject/Topic</th><th>Message</th><th>Date</th><th>Status</th><th>Action</th>
                </tr></thead>
                <tbody>
                  {requests.map(r => (
                    <tr key={r.id}>
                      <td><div style={{ fontWeight: 600 }}>{r.user_name}</div></td>
                      <td><div style={{ fontWeight: 600, color: 'var(--accent)' }}>{r.exam_type}</div></td>
                      <td>
                        <div style={{ fontSize: '0.85rem' }}>{r.subject || '—'}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.topic}</div>
                      </td>
                      <td style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{r.message || '—'}</td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {r.created_at ? new Date(r.created_at).toLocaleDateString() : '—'}
                      </td>
                      <td>
                        <span className={`badge ${r.status === 'fulfilled' ? 'badge-success' : 'badge-warning'}`}>
                          {r.status}
                        </span>
                      </td>
                      <td>
                        {r.status === 'pending' && (
                          <button className="btn btn-primary btn-sm" onClick={() => handleFulfillRequest(r.id)}>
                            ✅ Mark Fulfilled
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
