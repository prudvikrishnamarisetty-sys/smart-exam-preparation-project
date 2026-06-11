const API = 'https://prudvi2004-smart-exam-backend.hf.space/api';

function getToken() { return localStorage.getItem('token'); }

async function request(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (res.status === 401) { localStorage.clear(); window.location.href = '/'; }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

async function multipartRequest(path, formData, method = 'POST') {
  const token = getToken();
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, { method, headers, body: formData });
  if (res.status === 401) { localStorage.clear(); window.location.href = '/'; }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  // Auth
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request('/auth/me'),
  updateProfile: (data) => request('/auth/profile', { method: 'PUT', body: JSON.stringify(data) }),

  // Admin — Users
  adminGetUsers: () => request('/auth/admin/users'),
  adminDeleteUser: (id) => request(`/auth/admin/users/${id}`, { method: 'DELETE' }),
  adminToggleAdmin: (id) => request(`/auth/admin/users/${id}/toggle-admin`, { method: 'PUT' }),
  adminToggleActive: (id) => request(`/auth/admin/users/${id}/toggle-active`, { method: 'PUT' }),

  // Admin — Resources
  adminGetResourceExamTypes: () => request('/admin/resources/exam-types'),
  adminUploadResource: (formData) => multipartRequest('/admin/resources/upload', formData),
  adminListResources: () => request('/admin/resources'),
  adminDeleteResource: (id) => request(`/admin/resources/${id}`, { method: 'DELETE' }),
  adminGetRequests: () => request('/admin/requests'),
  adminFulfillRequest: (id) => request(`/admin/requests/${id}/fulfill`, { method: 'POST' }),

  // Public Resources (uploaded by admin)
  listPublicResources: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v))
    ).toString();
    return request(`/admin/public/resources${qs ? '?' + qs : ''}`);
  },
  downloadResource: (id) => {
    const token = getToken();
    return `${API}/admin/public/resources/${id}/download${token ? '?token=' + token : ''}`;
  },

  // Exam Configs
  getExamConfigs: () => request('/questions/exam-configs'),
  getUnseenCount: (examKey) => request(`/questions/unseen-count?exam_key=${examKey}`),

  // Exams
  startExam: (data) => request('/exam/start', { method: 'POST', body: JSON.stringify(data) }),
  submitExam: (data) => request('/exam/submit', { method: 'POST', body: JSON.stringify(data) }),
  getExamHistory: () => request('/exam/history'),
  getExam: (id) => request(`/exam/${id}`),
  reviewExam: (id) => request(`/exam/${id}/review`),

  // Dashboard
  getDashboard: () => request('/dashboard/'),
  getSubjectAnalysis: (et) => request(`/dashboard/subject-analysis${et ? '?exam_type=' + et : ''}`),

  // Resources (AI-powered)
  fetchResource: (data) => request('/resources/fetch', { method: 'POST', body: JSON.stringify(data) }),
  fetchPastPapers: (data) => request('/resources/past-papers', { method: 'POST', body: JSON.stringify(data) }),
  getExamSubjects: (examType) => request(`/resources/exam-subjects?exam_type=${examType}`),
  requestResource: (data) => request('/resources/requests', { method: 'POST', body: JSON.stringify(data) }),

  // AI
  explainQuestion: (data) => request('/ai/explain', { method: 'POST', body: JSON.stringify(data) }),
  askAI: (data) => request('/ai/ask', { method: 'POST', body: JSON.stringify(data) }),
  aiChat: (data) => request('/ai/chat', { method: 'POST', body: JSON.stringify(data) }),
  analyzeMedia: (formData) => multipartRequest('/ai/analyze-media', formData),
  generateFromText: (data) => request('/ai/generate-from-text', { method: 'POST', body: JSON.stringify(data) }),
};
