import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

// Rotating messages during AI question generation
const LOADING_MESSAGES = [
  'Searching online for latest questions…',
  'Matching official exam pattern…',
  'Generating exam questions with AI…',
  'Verifying question quality…',
  'Preparing your exam…',
  'Almost ready…',
];
const SLOW_MESSAGE = '⏳ Taking a bit longer than usual — activating fallback mode…';

export default function ExamInstructions() {
  const { examKey } = useParams();
  const navigate    = useNavigate();

  const [config,   setConfig]   = useState(null);
  const [starting, setStarting] = useState(false);
  const [error,    setError]    = useState('');
  const [agreed,   setAgreed]   = useState(false);

  // Skeleton loader state
  const [msgIndex,  setMsgIndex]  = useState(0);
  const [elapsed,   setElapsed]   = useState(0);
  const timerRef  = useRef(null);
  const msgRef    = useRef(null);

  useEffect(() => {
    api.getExamConfigs().then(configs => {
      const c = configs.find(x => x.exam_key === examKey);
      setConfig(c);
    });
  }, [examKey]);

  // Cleanup timers on unmount
  useEffect(() => () => {
    clearInterval(timerRef.current);
    clearInterval(msgRef.current);
  }, []);

  const startTimers = () => {
    timerRef.current = setInterval(() => setElapsed(s => s + 1), 1000);
    msgRef.current   = setInterval(() => setMsgIndex(i => (i + 1) % LOADING_MESSAGES.length), 3500);
  };
  const stopTimers = () => {
    clearInterval(timerRef.current);
    clearInterval(msgRef.current);
    setElapsed(0);
    setMsgIndex(0);
  };

  const handleStart = async () => {
    setStarting(true);
    setError('');
    startTimers();
    try {
      const exam = await api.startExam({ exam_config_key: examKey });
      stopTimers();
      navigate(`/exam/${exam.id}`);
    } catch (err) {
      stopTimers();
      setError(err.message || 'Failed to start exam. Please try again.');
      setStarting(false);
    }
  };

  if (!config) return <div className="loader"><div className="spinner"></div></div>;

  const sections = JSON.parse(config.sections_json || '[]');

  // ── Skeleton loading overlay ────────────────────────────────────────────────
  if (starting) {
    const isSlow = elapsed > 8;
    return (
      <div style={{
        position: 'fixed', inset: 0, background: 'rgba(10,10,30,0.96)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        zIndex: 9999, gap: '2rem', padding: '2rem',
      }}>
        {/* Spinner + elapsed */}
        <div style={{ textAlign: 'center' }}>
          <div className="spinner" style={{ width: 64, height: 64, margin: '0 auto 1rem' }}></div>
          <p style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.4rem' }}>
            {isSlow ? SLOW_MESSAGE : LOADING_MESSAGES[msgIndex]}
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Preparing exam: <strong style={{ color: 'var(--accent)' }}>{config.display_name}</strong>
            &nbsp;•&nbsp; {elapsed}s
          </p>
        </div>

        {/* Skeleton question cards */}
        <div style={{ width: '100%', maxWidth: 700, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {[1, 2, 3].map(n => (
            <div key={n} style={{
              background: 'rgba(255,255,255,0.04)', border: '1px solid var(--border)',
              borderRadius: '0.75rem', padding: '1.25rem',
              animation: `pulse ${1 + n * 0.3}s ease-in-out infinite`,
            }}>
              <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'var(--border)', flexShrink: 0 }} />
                <div style={{ flex: 1 }}>
                  <div style={{ height: 14, background: 'var(--border)', borderRadius: 4, marginBottom: 10, width: `${70 + n * 8}%` }} />
                  <div style={{ height: 12, background: 'var(--border)', borderRadius: 4, width: '50%' }} />
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginTop: '1rem' }}>
                    {[1, 2, 3, 4].map(o => (
                      <div key={o} style={{ height: 36, background: 'var(--border)', borderRadius: '0.4rem' }} />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', maxWidth: 420, textAlign: 'center' }}>
          {isSlow
            ? 'AI is generating fallback questions to ensure you get a complete exam. Hang tight!'
            : 'AI is generating fresh questions tailored to the latest official pattern. This ensures maximum variety.'}
        </p>
      </div>
    );
  }

  // ── Normal instructions page ────────────────────────────────────────────────
  return (
    <div className="page fade-in" style={{ maxWidth: 820 }}>
      <div className="instructions-header">
        <span className="instructions-icon">{config.icon}</span>
        <div>
          <h1>{config.display_name}</h1>
          <p>Read all instructions carefully before proceeding to the exam.</p>
        </div>
      </div>

      {/* Pattern Summary */}
      <div className="instructions-pattern">
        <div className="ip-stat"><span className="ip-val">{config.total_questions}</span><span className="ip-label">Total Questions</span></div>
        <div className="ip-stat"><span className="ip-val">{config.total_marks}</span><span className="ip-label">Total Marks</span></div>
        <div className="ip-stat"><span className="ip-val">{config.duration_minutes} min</span><span className="ip-label">Duration</span></div>
        <div className="ip-stat">
          <span className="ip-val" style={{ color: 'var(--danger)' }}>
            {config.negative_marking > 0 ? `-${config.negative_marking}` : 'No'}
          </span>
          <span className="ip-label">Negative Marking</span>
        </div>
        <div className="ip-stat">
          <span className="ip-val" style={{ color: 'var(--accent)' }}>{config.marks_per_question}</span>
          <span className="ip-label">Marks/Question</span>
        </div>
      </div>

      {/* Section Breakup */}
      {sections.length > 0 && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>📊 Section-wise Breakup</h3>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Section</th><th>Questions</th><th>Marks/Q</th><th>Neg/Wrong</th><th>Max Marks</th></tr></thead>
              <tbody>
                {sections.map((s, i) => (
                  <tr key={i}>
                    <td><strong>{s.name}</strong></td>
                    <td>{s.questions}</td>
                    <td style={{ color: 'var(--success)' }}>+{s.marks_per_q}</td>
                    <td style={{ color: s.negative > 0 ? 'var(--danger)' : 'var(--text-muted)' }}>
                      {s.negative > 0 ? `-${s.negative}` : 'None'}
                    </td>
                    <td>{s.questions * s.marks_per_q}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* General Instructions */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>📋 General Instructions</h3>
        <ul className="instructions-list">
          <li>The exam will auto-submit when the timer reaches <strong>0:00</strong>.</li>
          <li>You can navigate to any question using the <strong>Question Palette</strong> on the right.</li>
          <li>Click <strong>"Save &amp; Next"</strong> to save your answer and move to the next question.</li>
          <li>Click <strong>"Clear Response"</strong> to remove your selected option.</li>
          <li>Click <strong>"Mark for Review &amp; Next"</strong> to flag a question and revisit later.</li>
          <li>You can change your answer any number of times before submitting.</li>
          <li>Questions are generated fresh by AI for every attempt — no two attempts are identical.</li>
          {config.negative_marking > 0 && (
            <li style={{ color: 'var(--warning)' }}>
              ⚠️ <strong>Negative Marking:</strong> {config.negative_marking} mark(s) will be deducted for each wrong answer. Do NOT guess randomly.
            </li>
          )}
        </ul>
      </div>

      {/* Palette Legend */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>🎨 Question Palette Legend</h3>
        <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
          <div className="palette-legend-item"><span className="palette-btn not-visited">1</span> Not Visited</div>
          <div className="palette-legend-item"><span className="palette-btn not-answered">2</span> Not Answered</div>
          <div className="palette-legend-item"><span className="palette-btn answered">3</span> Answered</div>
          <div className="palette-legend-item"><span className="palette-btn marked-review">4</span> Marked for Review</div>
          <div className="palette-legend-item"><span className="palette-btn answered-marked">5</span> Answered &amp; Marked</div>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* ── MANDATORY CHECKBOX ─────────────────────────────────────────── */}
      <label style={{
        display: 'flex', alignItems: 'center', gap: '0.75rem',
        marginBottom: '1.5rem', cursor: 'pointer',
        background: agreed ? 'rgba(34,197,94,0.08)' : 'rgba(255,255,255,0.03)',
        border: `1px solid ${agreed ? 'rgba(34,197,94,0.3)' : 'var(--border)'}`,
        borderRadius: '0.6rem', padding: '0.85rem 1rem',
        transition: 'all 0.2s',
      }}>
        <input
          type="checkbox"
          checked={agreed}
          onChange={e => setAgreed(e.target.checked)}
          style={{ width: 20, height: 20, cursor: 'pointer', accentColor: 'var(--success)', flexShrink: 0 }}
        />
        <span style={{ fontWeight: 500 }}>
          I have read and understood all the instructions above and agree to the exam rules.
        </span>
      </label>

      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          className="btn btn-primary btn-lg"
          onClick={handleStart}
          disabled={!agreed || starting}
          style={{ opacity: agreed ? 1 : 0.5, cursor: agreed ? 'pointer' : 'not-allowed' }}
        >
          {starting ? '⏳ Starting…' : '🚀 Proceed to Exam'}
        </button>
        <button className="btn btn-secondary btn-lg" onClick={() => navigate('/exams')}>
          ← Back to Exams
        </button>
      </div>

      {!agreed && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.6rem' }}>
          ☝️ Please tick the checkbox above to enable the start button.
        </p>
      )}
    </div>
  );
}
