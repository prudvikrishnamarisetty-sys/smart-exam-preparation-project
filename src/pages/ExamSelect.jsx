import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const EXPECTED_EXAM_COUNT = 77;

const CATEGORY_META = {
  PROGRAMMING:  { label: '💻 Programming',       desc: 'Python, Java, C, C++, JavaScript, SQL, React, Spring Boot' },
  APTITUDE:     { label: '🔢 Aptitude',           desc: 'Number System, Percentage, Profit & Loss, Time & Work, DI, Full Mock' },
  REASONING:    { label: '🧠 Reasoning',          desc: 'Verbal, Non-Verbal, Logical Reasoning, Puzzles, Full Mock' },
  CORE_CS:      { label: '📂 Core CS',            desc: 'DSA, DBMS, OS, Computer Networks (GATE Pattern)' },
  CLOUD_DEVOPS: { label: '☁️ Cloud & DevOps',    desc: 'AWS SAA, Azure AZ-104, GCP ACE, Docker, Kubernetes' },
  GOVT_IT:      { label: '🏛️ Govt IT Jobs',     desc: 'SSC CGL, GATE CSE, RRB JE IT, ISRO, DRDO' },
  GOVT_NON_IT:  { label: '📝 Govt Non-IT',       desc: 'SSC MTS, GD Constable, SSC CPO' },
  RAILWAY:      { label: '🚂 Railway',            desc: 'RRB NTPC, Group D, ALP, JE, RPF' },
  UPSC:         { label: '🏛️ UPSC',              desc: 'CSE Prelims, CAPF' },
  TEACHING:     { label: '📚 Teaching',           desc: 'CTET Paper 1 & 2, KVS PGT' },
  STATE_PSC:    { label: '🏢 State PSC',          desc: 'APPSC Group-1, TSPSC, MPPSC' },
  COMPANY:      { label: '🏢 Company Hiring',     desc: 'TCS NQT, Infosys SP, Wipro Elite, Cognizant' },
};

// Skeleton card shown while exam list is loading
function SkeletonCard() {
  return (
    <div style={{
      background: 'var(--card-bg)', border: '1px solid var(--border)', borderRadius: '1rem',
      padding: '1.5rem', animation: 'pulse 1.5s ease-in-out infinite',
    }}>
      <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--border)', marginBottom: '1rem' }} />
      <div style={{ height: 16, background: 'var(--border)', borderRadius: 4, marginBottom: 8, width: '70%' }} />
      <div style={{ height: 12, background: 'var(--border)', borderRadius: 4, width: '90%' }} />
    </div>
  );
}

export default function ExamSelect() {
  const navigate = useNavigate();
  const [configs, setConfigs]           = useState([]);
  const [loading, setLoading]           = useState(true);
  const [activeCategory, setActiveCategory] = useState('PROGRAMMING');
  const [modalExam, setModalExam]       = useState(null);
  const [search, setSearch]             = useState('');
  const [missingWarning, setMissingWarning] = useState(false);
  const [retryCount, setRetryCount]     = useState(0);

  const loadConfigs = () => {
    setLoading(true);
    api.getExamConfigs()
      .then(data => {
        setConfigs(data);
        if (data.length < EXPECTED_EXAM_COUNT) {
          console.warn(`[ExamSelect] Only ${data.length}/${EXPECTED_EXAM_COUNT} exam configs loaded. Some cards may be missing.`);
          setMissingWarning(true);
          // Auto-retry once after 3s
          setTimeout(() => {
            api.getExamConfigs().then(d2 => {
              if (d2.length > data.length) { setConfigs(d2); setMissingWarning(d2.length < EXPECTED_EXAM_COUNT); }
              setRetryCount(r => r + 1);
            }).catch(() => {});
          }, 3000);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadConfigs(); }, []);

  // Build dynamic category list from actual loaded data
  const categories = useMemo(() => {
    const cats = [...new Set(configs.map(c => c.category))];
    // Sort by a preferred order
    const ORDER = ['PROGRAMMING','APTITUDE','REASONING','CORE_CS','CLOUD_DEVOPS','GOVT_IT','GOVT_NON_IT','RAILWAY','UPSC','TEACHING','STATE_PSC','COMPANY'];
    return cats.sort((a, b) => {
      const ia = ORDER.indexOf(a), ib = ORDER.indexOf(b);
      if (ia === -1 && ib === -1) return a.localeCompare(b);
      if (ia === -1) return 1; if (ib === -1) return -1;
      return ia - ib;
    });
  }, [configs]);

  // Filter — if search is active show across ALL categories; else filter by tab
  const filtered = useMemo(() => {
    if (search.trim()) {
      const q = search.toLowerCase();
      return configs.filter(c =>
        c.display_name.toLowerCase().includes(q) ||
        c.exam_key.toLowerCase().includes(q) ||
        (c.description || '').toLowerCase().includes(q)
      );
    }
    return configs.filter(c => c.category === activeCategory);
  }, [configs, activeCategory, search]);

  return (
    <div className="page fade-in">
      <div className="page-header">
        <h1>Select Examination</h1>
        <p>Choose from <strong>{configs.length}</strong> exams across {categories.length} categories. All follow official patterns.</p>
      </div>

      {/* ── Missing-card warning ────────────────────────────────────── */}
      {missingWarning && (
        <div style={{
          background: 'rgba(234,179,8,0.1)', border: '1px solid rgba(234,179,8,0.3)',
          borderRadius: '0.6rem', padding: '0.6rem 1.2rem', marginBottom: '1rem',
          display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.88rem',
        }}>
          <span>⚠️</span>
          <span style={{ color: '#fbbf24' }}>Some exam cards are still loading…</span>
          <button className="btn btn-sm btn-secondary" style={{ marginLeft: 'auto' }} onClick={loadConfigs}>
            🔄 Reload
          </button>
        </div>
      )}

      {/* ── Global search ───────────────────────────────────────────── */}
      <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
        <span style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}>🔍</span>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search across all exams — e.g. RRB ALP, GATE, Python, Banking…"
          style={{ paddingLeft: '2.5rem', marginBottom: 0 }}
        />
        {search && (
          <button onClick={() => setSearch('')} style={{
            position: 'absolute', right: '0.75rem', top: '50%', transform: 'translateY(-50%)',
            background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: '1.1rem',
          }}>✕</button>
        )}
      </div>

      {/* ── Category Tabs (hidden during global search) ─────────────── */}
      {!search && (
        <div className="category-tabs">
          {categories.map(cat => {
            const meta = CATEGORY_META[cat] || { label: cat.replace(/_/g, ' ') };
            const count = configs.filter(c => c.category === cat).length;
            return (
              <button
                key={cat}
                className={`cat-tab ${activeCategory === cat ? 'active' : ''}`}
                onClick={() => setActiveCategory(cat)}
                title={meta.desc}
              >
                {meta.label}
                <span style={{
                  marginLeft: '0.4rem', fontSize: '0.7rem',
                  background: activeCategory === cat ? 'rgba(255,255,255,0.2)' : 'var(--border)',
                  borderRadius: '0.8rem', padding: '0.1rem 0.45rem',
                }}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {/* ── Search result label ─────────────────────────────────────── */}
      {search && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1rem' }}>
          Showing <strong>{filtered.length}</strong> result{filtered.length !== 1 ? 's' : ''} for "{search}"
        </p>
      )}

      {/* ── Exam Grid ───────────────────────────────────────────────── */}
      <div className="card-grid" style={{ marginTop: '1.5rem' }}>
        {loading
          ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
          : filtered.length === 0
            ? (
              <p style={{ color: 'var(--text-muted)', gridColumn: '1/-1', textAlign: 'center', padding: '3rem' }}>
                {search ? `No exams match "${search}". Try a different keyword.` : 'No exams in this category yet.'}
              </p>
            )
            : filtered.map(exam => (
              <div key={exam.exam_key} className="exam-card" onClick={() => setModalExam(exam)}>
                <div className="exam-card-icon">{exam.icon}</div>
                <div className="exam-card-body">
                  <h3>{exam.display_name}</h3>
                  <p className="exam-pattern">{exam.pattern_summary}</p>
                  <p className="exam-desc">{exam.description}</p>
                </div>
                <div className="exam-card-footer">
                  <span className="exam-cat-badge">{(CATEGORY_META[exam.category]?.label || exam.category).replace(/^.+? /, '')}</span>
                  <span className="exam-start-hint">Click for details →</span>
                </div>
              </div>
            ))
        }
      </div>

      {/* ── Preview Modal — NO direct start, always route to checkbox page ── */}
      {modalExam && (
        <div className="modal-overlay" onClick={() => setModalExam(null)}>
          <div className="modal-box" onClick={e => e.stopPropagation()}>
            <div className="modal-icon">{modalExam.icon}</div>
            <h2>{modalExam.display_name}</h2>
            <p style={{ color: 'var(--text-secondary)', margin: '0.5rem 0 1.5rem' }}>{modalExam.description}</p>

            <div className="modal-pattern-grid">
              <div className="modal-stat">
                <span className="modal-stat-val">{modalExam.total_questions}</span>
                <span>Questions</span>
              </div>
              <div className="modal-stat">
                <span className="modal-stat-val">{modalExam.total_marks}</span>
                <span>Marks</span>
              </div>
              <div className="modal-stat">
                <span className="modal-stat-val">{modalExam.duration_minutes}</span>
                <span>Minutes</span>
              </div>
              <div className="modal-stat">
                <span className="modal-stat-val" style={{ color: modalExam.negative_marking > 0 ? 'var(--danger)' : 'var(--success)' }}>
                  {modalExam.negative_marking > 0 ? `-${modalExam.negative_marking}` : 'None'}
                </span>
                <span>Negative</span>
              </div>
            </div>

            {/* Marks per question highlight */}
            <div style={{
              background: 'rgba(124,92,252,0.1)', border: '1px solid rgba(124,92,252,0.25)',
              borderRadius: '0.6rem', padding: '0.75rem 1rem', margin: '1rem 0',
              display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.88rem',
            }}>
              <span style={{ fontSize: '1.2rem' }}>✅</span>
              <span style={{ color: 'var(--text-secondary)' }}>
                <strong style={{ color: 'var(--success)' }}>+{modalExam.marks_per_question}</strong> per correct &nbsp;|&nbsp;
                {modalExam.negative_marking > 0
                  ? <><strong style={{ color: 'var(--danger)' }}>-{modalExam.negative_marking}</strong> per wrong</>
                  : <strong style={{ color: 'var(--success)' }}>No negative marking</strong>
                }
              </span>
            </div>

            {/* Instruction notice */}
            <div style={{
              background: 'rgba(56,189,248,0.08)', borderRadius: '0.5rem',
              padding: '0.6rem 1rem', marginBottom: '1.25rem', fontSize: '0.83rem',
              color: 'var(--text-muted)', display: 'flex', gap: '0.5rem',
            }}>
              <span>ℹ️</span>
              <span>You must read the full instructions and tick the agreement checkbox before the exam begins.</span>
            </div>

            <div className="modal-actions">
              {/* ✅ ONLY route to instructions — checkbox is mandatory */}
              <button
                className="btn btn-primary btn-lg"
                style={{ flex: 1 }}
                onClick={() => { setModalExam(null); navigate(`/instructions/${modalExam.exam_key}`); }}
              >
                📋 Read Instructions & Start
              </button>
              <button className="btn btn-secondary" onClick={() => setModalExam(null)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
