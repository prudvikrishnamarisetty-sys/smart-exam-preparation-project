import { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import MarkdownRenderer from '../components/MarkdownRenderer';

// ── Inline resource card (no download buttons) ───────────────────────────────
function ResourceCard({ resource }) {
  const [expanded, setExpanded] = useState(false);
  const icons = { PDF: '📄', Image: '🖼️', Video: '🎬', Document: '📝' };

  return (
    <div style={{
      background: 'rgba(56,189,248,0.05)', border: '1px solid var(--border)',
      borderRadius: '0.75rem', padding: '1rem', transition: 'border-color 0.2s',
    }}
      onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--accent)'}
      onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
        <span style={{ fontSize: '1.8rem', flexShrink: 0 }}>{icons[resource.file_type] || '📎'}</span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-main)' }}>{resource.title}</div>
          {resource.exam_name && (
            <span style={{
              display: 'inline-block', fontSize: '0.72rem', background: 'rgba(56,189,248,0.12)',
              color: 'var(--accent)', padding: '0.15rem 0.45rem', borderRadius: '0.3rem', margin: '0.25rem 0',
            }}>{resource.exam_name}</span>
          )}
          {resource.subject && <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>📚 {resource.subject}</div>}

          {/* Description shown inline as text */}
          {resource.description && (
            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginTop: '0.4rem' }}>
              {expanded ? resource.description : resource.description.slice(0, 150)}
              {resource.description.length > 150 && (
                <button onClick={() => setExpanded(!expanded)} style={{
                  background: 'none', border: 'none', color: 'var(--accent)',
                  cursor: 'pointer', fontSize: '0.78rem', padding: '0 0.3rem',
                }}>
                  {expanded ? ' Show less' : '… Read more'}
                </button>
              )}
            </div>
          )}

          {/* Tags */}
          {resource.tags && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '0.5rem' }}>
              {resource.tags.split(',').map((t, i) => t.trim() && (
                <span key={i} style={{
                  fontSize: '0.68rem', background: 'rgba(124,58,237,0.1)',
                  color: '#a78bfa', padding: '0.12rem 0.35rem', borderRadius: '0.3rem',
                }}>{t.trim()}</span>
              ))}
            </div>
          )}

          {/* Uploaded material note and download button */}
          <div style={{
            marginTop: '0.6rem', fontSize: '0.74rem', color: 'var(--text-muted)',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <span>📌</span>
              <span>Admin-uploaded {resource.file_type} material</span>
            </div>
            {resource.has_file && (
              <a
                href={api.downloadResource(resource.id)}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ textDecoration: 'none', padding: '0.2rem 0.5rem', fontSize: '0.75rem', borderRadius: '0.3rem' }}
              >
                👁️ View
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Popular topics per exam ───────────────────────────────────────────────────
const POPULAR_TOPICS = {
  GATE_CSE:              ['Data Structures', 'Algorithms', 'DBMS', 'Operating Systems', 'Computer Networks', 'Theory of Computation'],
  SSC_JE_IT:             ['Digital Logic', 'Computer Organisation', 'Programming in C', 'Data Structures', 'Networking Basics'],
  JAVA_OCJP:             ['OOP Concepts', 'Collections', 'Exception Handling', 'Generics', 'Threads', 'Lambda Expressions'],
  DSA_PRACTICE:          ['Arrays', 'Linked List', 'Trees', 'Graphs', 'Dynamic Programming', 'Sorting'],
  AWS_SAA_C03:           ['EC2', 'S3', 'IAM', 'VPC', 'RDS', 'Lambda'],
  PYTHON_PCEP:           ['Data Types', 'Control Flow', 'Functions', 'Lists & Dicts', 'File I/O', 'OOP'],
  IBPS_PO_PRELIMS:       ['Number Series', 'Data Interpretation', 'Syllogisms', 'Coding-Decoding', 'Reading Comprehension'],
  SBI_PO_PRELIMS:        ['Approximation', 'Seating Arrangement', 'Para Jumbles', 'Quadratic Equations'],
  RBI_GRADE_B:           ['Monetary Policy', 'Banking Regulation', 'Financial Inclusion', 'Economic Survey'],
  RRB_NTPC_CBT1:         ['Number System', 'Ratio & Proportion', 'General Science', 'History of Railways', 'Current Affairs'],
  RRB_ALP_STAGE1:        ['Basic Mathematics', 'General Science', 'Reasoning Puzzles', 'Physics', 'Chemistry'],
  RRB_ALP_STAGE2_PARTA:  ['Engineering Drawing', 'Basic Science', 'Physics', 'Engineering Mechanics'],
  RRB_JE_IT:             ['Data Structures', 'Computer Networks', 'Database Systems', 'Operating Systems'],
  RRB_JE_CIVIL:          ['Strength of Materials', 'Fluid Mechanics', 'Structural Analysis', 'Concrete Technology'],
  RRB_JE_MECH:           ['Thermodynamics', 'Fluid Mechanics', 'Manufacturing Processes', 'Machine Design'],
  RRB_JE_EEE:            ['Electric Circuits', 'Machines', 'Power Systems', 'Control Systems'],
  RRB_JE_ECE:            ['Electronic Circuits', 'Digital Electronics', 'Signals & Systems', 'Communication Systems'],
  RRB_CONSTABLE_RPF:     ['Indian Constitution', 'Railway Acts', 'Current Affairs', 'Simple Arithmetic'],
  NDA_MATHS:             ['Matrices', 'Differential Calculus', 'Probability', 'Vector Algebra', 'Integration'],
  NDA_GAT:               ['British History', 'Indian Geography', 'Physics Laws', 'Chemistry Equations', 'English Grammar'],
  AFCAT:                 ['Indian Air Force History', 'Current Affairs', 'Physics', 'English Vocabulary'],
  UPSC_PRELIMS_GS1:      ['Indian Constitution', 'Modern History', 'Physical Geography', 'Economic Survey', 'Environment & Ecology'],
  CTET_PAPER1:           ['Child Development', 'Inclusive Education', 'Pedagogy', 'EVS Concepts'],
  SSC_CGL_TIER1:         ['Algebra', 'Percentage', 'Profit & Loss', 'Time & Work', 'General Awareness'],
  SSC_CPO_TIER1:         ['Quantitative Aptitude', 'Reasoning Puzzles', 'English Comprehension', 'Current Affairs'],
  APPSC_GROUP1_PRELIMS:  ['Andhra Pradesh Economy', 'AP History', 'Indian Polity', 'Current Affairs AP'],
  GCP_ACE:               ['Compute Engine', 'Cloud Storage', 'VPC Networking', 'IAM', 'Kubernetes Engine'],
  K8S_CKA:               ['Pods & Deployments', 'Services & Networking', 'Storage', 'RBAC', 'Cluster Maintenance'],
  CPP_PRACTICE:          ['Pointers', 'OOP in C++', 'STL', 'Templates', 'Memory Management'],
  JS_PRACTICE:           ['Closures', 'Promises & Async', 'DOM Manipulation', 'ES6+ Features', 'Event Loop'],
  SQL_PRACTICE:          ['Joins', 'Subqueries', 'Aggregations', 'Indexes', 'Transactions'],
  SYSTEM_DESIGN:         ['Load Balancing', 'Database Sharding', 'Caching', 'Microservices', 'CAP Theorem'],
};

const CATEGORY_LABELS = {
  GOVT_IT: '🏛️ Govt IT Jobs', GOVT_NON_IT: '📝 Govt Non-IT', BANKING: '🏦 Banking',
  RAILWAY: '🚂 Railway', DEFENCE: '⚔️ Defence', UPSC: '🏛️ UPSC',
  TEACHING: '📚 Teaching', STATE_PSC: '🏢 State PSC',
  BTECH_LANG: '💻 B.Tech Languages', CORE_CS: '🖥️ Core CS',
  CLOUD_DEVOPS: '☁️ Cloud/DevOps', COMPANY: '🏢 Company Tests',
};

export default function Resources() {
  const [configs, setConfigs]               = useState([]);
  const [selectedExam, setSelectedExam]     = useState('');
  const [subjects, setSubjects]             = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [topic, setTopic]                   = useState('');
  const [activeTab, setActiveTab]           = useState('notes'); // 'notes' | 'papers' | 'uploaded'
  const [loading, setLoading]               = useState(false);
  const [content, setContent]               = useState(null);
  const [contentTitle, setContentTitle]     = useState('');
  const [error, setError]                   = useState('');
  const [paperMode, setPaperMode]           = useState('exam_and_subject');

  // Uploaded resources — NOT auto-loaded; only populated after search
  const [uploadedResources, setUploadedResources] = useState([]);
  const [resLoading, setResLoading]         = useState(false);
  const [hasSearched, setHasSearched]       = useState(false);

  const contentRef = useRef(null);

  useEffect(() => {
    api.getExamConfigs().then(setConfigs).catch(console.error);
    // ✅ No auto-load of uploaded resources on mount
  }, []);

  useEffect(() => {
    if (!selectedExam) return;
    api.getExamSubjects(selectedExam)
      .then(s => { setSubjects(s); setSelectedSubject(s[0] || ''); })
      .catch(() => setSubjects([]));
  }, [selectedExam]);

  const grouped = useMemo(() => configs.reduce((acc, c) => {
    (acc[c.category] = acc[c.category] || []).push(c);
    return acc;
  }, {}), [configs]);

  const popularTopics  = POPULAR_TOPICS[selectedExam] || [];
  const examLabel      = configs.find(c => c.exam_key === selectedExam)?.display_name || selectedExam;

  // ── Master search: AI notes + uploaded resources ─────────────────────────
  const handleSearch = async () => {
    if (!selectedExam) { setError('Please select an exam first.'); return; }
    const topicFinal = topic.trim() || 'General Overview';
    setError(''); setContent(null); setHasSearched(true);

    if (activeTab === 'notes') {
      setLoading(true);
      try {
        const res = await api.fetchResource({
          exam_type: selectedExam,
          subject: selectedSubject,
          topic: topicFinal,
        });
        setContent(res.content);
        setContentTitle(`Study Notes — ${topicFinal}`);
        setTimeout(() => contentRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
      } catch (err) { setError(err.message || 'Failed to fetch notes'); }
      finally { setLoading(false); }

    } else if (activeTab === 'papers') {
      setLoading(true);
      try {
        const res = await api.fetchPastPapers({
          exam_type: selectedExam,
          subject: paperMode === 'exam_and_subject' ? selectedSubject || 'General' : 'All Subjects',
          mode: paperMode,
        });
        setContent(res.content);
        setContentTitle('📚 Past 10 Years Question Papers');
        setTimeout(() => contentRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
      } catch (err) { setError(err.message || 'Failed to fetch past papers'); }
      finally { setLoading(false); }

    } else {
      // Uploaded resources tab
      setResLoading(true);
      try {
        const results = await api.listPublicResources({
          exam_type: selectedExam || undefined,
          search: topicFinal !== 'General Overview' ? topicFinal : undefined,
        });
        setUploadedResources(results);
      } catch { setUploadedResources([]); }
      finally { setResLoading(false); }
    }
  };

  const handlePrint = () => window.print();

  return (
    <div className="page fade-in">
      <div className="page-header">
        <h1>🔍 Search Resources</h1>
        <p>Search by Exam + Topic to get AI study notes, past papers, or uploaded materials</p>
      </div>

      {/* ── Search Panel ────────────────────────────────────────────────── */}
      <div className="card" style={{ marginBottom: '2rem' }}>

        {/* Exam + Subject row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>Exam *</label>
            <select value={selectedExam} onChange={e => { setSelectedExam(e.target.value); setContent(null); setHasSearched(false); }}>
              <option value="">— Select Exam —</option>
              {Object.entries(grouped).map(([cat, exs]) => (
                <optgroup key={cat} label={CATEGORY_LABELS[cat] || cat}>
                  {exs.map(e => <option key={e.exam_key} value={e.exam_key}>{e.display_name}</option>)}
                </optgroup>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>Subject / Section</label>
            <select value={selectedSubject} onChange={e => setSelectedSubject(e.target.value)}>
              {subjects.length > 0
                ? subjects.map((s, i) => <option key={i} value={s}>{s}</option>)
                : <option value="">All Subjects</option>}
            </select>
          </div>
        </div>

        {/* Topic input */}
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.4rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Topic <span style={{ fontWeight: 400 }}>(optional)</span>
          </label>
          <input
            value={topic}
            onChange={e => setTopic(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            placeholder="e.g. Binary Search, Normalization, Monetary Policy…"
            style={{ marginBottom: 0 }}
          />
        </div>

        {/* Popular topic chips */}
        {popularTopics.length > 0 && (
          <div style={{ marginBottom: '1rem' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginRight: '0.6rem' }}>Popular:</span>
            {popularTopics.map((t, i) => (
              <button key={i} className="starter-chip" onClick={() => setTopic(t)}>{t}</button>
            ))}
          </div>
        )}

        {/* Resource type tabs */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', background: 'rgba(0,0,0,0.2)', padding: '0.3rem', borderRadius: '0.5rem', width: 'fit-content' }}>
          {[
            { key: 'notes',    label: '📖 Study Notes'     },
            { key: 'papers',   label: '📚 Past Papers'     },
            { key: 'uploaded', label: '📁 Uploaded Files'  },
          ].map(tab => (
            <button
              key={tab.key}
              className={`btn btn-sm ${activeTab === tab.key ? 'btn-primary' : 'btn-secondary'}`}
              style={{ borderRadius: '0.35rem' }}
              onClick={() => { setActiveTab(tab.key); setContent(null); setHasSearched(false); }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Past papers mode (only when papers tab active) */}
        {activeTab === 'papers' && (
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
            {[
              { key: 'exam_and_subject', label: 'By Exam + Subject' },
              { key: 'exam_only',        label: 'By Exam Only'      },
            ].map(m => (
              <button
                key={m.key}
                className={`btn btn-sm ${paperMode === m.key ? 'btn-primary' : 'btn-secondary'}`}
                style={{ borderRadius: '0.35rem' }}
                onClick={() => setPaperMode(m.key)}
              >
                {m.label}
              </button>
            ))}
          </div>
        )}

        {/* Search button */}
        <button
          className="btn btn-primary"
          onClick={handleSearch}
          disabled={loading || resLoading || !selectedExam}
          style={{ minWidth: 160 }}
        >
          {loading || resLoading ? '⏳ Searching…' : '🔍 Search Resources'}
        </button>

        {!selectedExam && (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.5rem' }}>
            ☝️ Select an exam above to enable search.
          </p>
        )}
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* ── Uploaded resources results ───────────────────────────────────── */}
      {activeTab === 'uploaded' && hasSearched && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>
            📁 Uploaded Materials
            {uploadedResources.length > 0 && (
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginLeft: '0.6rem', fontWeight: 400 }}>
                — {uploadedResources.length} result{uploadedResources.length !== 1 ? 's' : ''}
              </span>
            )}
          </h3>
          {resLoading ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}><div className="spinner" style={{ margin: '0 auto' }}></div></div>
          ) : uploadedResources.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>📂</div>
              <p>No uploaded materials found for this search.</p>
              <p style={{ fontSize: '0.83rem', marginTop: '0.5rem' }}>Try switching to <strong>Study Notes</strong> for AI-generated content.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
              {uploadedResources.map(r => <ResourceCard key={r.id} resource={r} />)}
            </div>
          )}
        </div>
      )}

      {/* ── Prompt when not searched yet ───────────────────────────────── */}
      {!hasSearched && !loading && (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '3.5rem', marginBottom: '1rem' }}>🔍</div>
          <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
            {selectedExam ? `Ready to search for ${examLabel}` : 'Select an exam and topic above'}
          </h3>
          <p style={{ fontSize: '0.9rem' }}>
            {selectedExam
              ? 'Click "Search Resources" to get AI-generated notes, past papers, or uploaded materials.'
              : 'Choose an exam, optionally enter a topic, then click Search Resources.'}
          </p>
        </div>
      )}

      {/* ── AI content loading ─────────────────────────────────────────── */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <div className="spinner" style={{ margin: '0 auto 1rem', width: 56, height: 56 }}></div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>
            AI is generating <strong>{contentTitle || 'content'}</strong>…
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
            This may take 20–40 seconds for comprehensive content.
          </p>
        </div>
      )}

      {/* ── AI-generated content rendered as inline Markdown ──────────── */}
      {content && !loading && (
        <div className="card fade-in pdf-content" ref={contentRef}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border)',
            flexWrap: 'wrap', gap: '0.75rem',
          }} className="no-print">
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <span style={{
                background: 'rgba(56,189,248,0.1)', color: 'var(--accent)',
                padding: '0.3rem 0.7rem', borderRadius: '0.4rem', fontSize: '0.8rem', fontWeight: 600,
              }}>{examLabel}</span>
              <span style={{
                background: 'rgba(16,185,129,0.1)', color: 'var(--success)',
                padding: '0.3rem 0.7rem', borderRadius: '0.4rem', fontSize: '0.8rem', fontWeight: 600,
              }}>✨ AI Generated</span>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button className="btn btn-secondary btn-sm" onClick={handleSearch}>↻ Regenerate</button>
              <button className="btn btn-primary btn-sm" onClick={handlePrint}>🖨️ Save as PDF</button>
            </div>
          </div>
          <div style={{ lineHeight: 1.8 }}><MarkdownRenderer content={content} /></div>
        </div>
      )}
    </div>
  );
}
