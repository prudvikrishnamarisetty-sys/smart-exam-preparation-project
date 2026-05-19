import { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../api/client';
import MarkdownRenderer from '../components/MarkdownRenderer';

export default function Results() {
  const { examId }  = useParams();
  const navigate    = useNavigate();

  const [review,       setReview]       = useState(null);
  const [loading,      setLoading]      = useState(true);
  const [selectedQ,    setSelectedQ]    = useState(null);
  const [aiExpl,       setAiExpl]       = useState(null);
  const [loadingExpl,  setLoadingExpl]  = useState(false);

  useEffect(() => {
    api.reviewExam(parseInt(examId))
      .then(setReview)
      .catch(() => navigate('/'))
      .finally(() => setLoading(false));
  }, [examId]);

  const loadExplanation = async (q) => {
    if (selectedQ?.question_id === q.question_id) { setSelectedQ(null); setAiExpl(null); return; }
    setSelectedQ(q); setAiExpl(null); setLoadingExpl(true);
    try {
      const expl = await api.explainQuestion({ question_id: q.question_id, user_answer: q.selected_option });
      setAiExpl(expl);
    } catch { setAiExpl(null); }
    finally { setLoadingExpl(false); }
  };

  // ── Computed analytics ──────────────────────────────────────────────────────
  const analytics = useMemo(() => {
    if (!review) return null;
    const attempted  = (review.correct || 0) + (review.wrong || 0);
    const accuracy   = attempted > 0 ? ((review.correct / attempted) * 100).toFixed(1) : '—';
    // Estimate avg time based on duration stored in exam (seconds per question)
    const totalSecs  = (review.duration_minutes || 60) * 60;
    const timePerQ   = review.total_questions > 0
      ? Math.round(totalSecs / review.total_questions)
      : null;

    // Weak sections: sections where wrong > correct
    const sectionMap = {};
    (review.questions || []).forEach(q => {
      const sec = q.section || q.subject || 'General';
      if (!sectionMap[sec]) sectionMap[sec] = { correct: 0, wrong: 0, skipped: 0 };
      if (q.is_correct) sectionMap[sec].correct++;
      else if (q.selected_option) sectionMap[sec].wrong++;
      else sectionMap[sec].skipped++;
    });

    const weakSections = Object.entries(sectionMap)
      .map(([name, s]) => {
        const att = s.correct + s.wrong;
        const acc = att > 0 ? Math.round((s.correct / att) * 100) : 0;
        return { name, ...s, accuracy: acc };
      })
      .filter(s => s.accuracy < 60 && (s.correct + s.wrong) > 0)
      .sort((a, b) => a.accuracy - b.accuracy)
      .slice(0, 4);

    return { attempted, accuracy, timePerQ, weakSections, sectionMap };
  }, [review]);

  if (loading) return <div className="loader"><div className="spinner"></div></div>;
  if (!review)  return <div className="page"><p>Results not found</p></div>;

  const sectionScores = review.section_scores || {};
  const pct           = review.percentage || 0;
  const scoreColor    = pct >= 60 ? 'var(--success)' : pct >= 40 ? 'var(--warning)' : 'var(--danger)';

  // Section accuracy badge helper
  const accBadge = (acc) => {
    if (acc >= 70) return { cls: 'badge-success', label: `${acc}% ✓` };
    if (acc >= 40) return { cls: 'badge-warning', label: `${acc}%` };
    return { cls: 'badge-danger', label: `${acc}% ↓` };
  };

  return (
    <div className="page fade-in">

      {/* ── Score Hero ──────────────────────────────────────────────────────── */}
      <div className="result-hero">
        <div className="result-score" style={{ color: scoreColor }}>{pct.toFixed(1)}%</div>
        <p style={{ color: 'var(--text-secondary)', margin: '0.5rem 0' }}>
          {review.exam_type?.replace(/_/g, ' ')}
        </p>
        <div className="result-stats">
          <div className="result-stat">
            <div className="value" style={{ color: 'var(--success)' }}>{review.score?.toFixed(2)}</div>
            <div className="label">Final Score</div>
          </div>
          <div className="result-stat">
            <div className="value">{review.raw_score?.toFixed(2)}</div>
            <div className="label">Raw Score</div>
          </div>
          <div className="result-stat">
            <div className="value" style={{ color: 'var(--danger)' }}>-{review.negative_deducted?.toFixed(2)}</div>
            <div className="label">Neg. Deducted</div>
          </div>
          <div className="result-stat">
            <div className="value" style={{ color: 'var(--success)' }}>{review.correct}</div>
            <div className="label">Correct</div>
          </div>
          <div className="result-stat">
            <div className="value" style={{ color: 'var(--danger)' }}>{review.wrong}</div>
            <div className="label">Wrong</div>
          </div>
          <div className="result-stat">
            <div className="value" style={{ color: 'var(--text-muted)' }}>{review.unattempted}</div>
            <div className="label">Skipped</div>
          </div>
          {/* ── New: Accuracy & Time ── */}
          {analytics && (
            <>
              <div className="result-stat">
                <div className="value" style={{ color: 'var(--accent)' }}>{analytics.accuracy}%</div>
                <div className="label">Accuracy</div>
              </div>
              <div className="result-stat">
                <div className="value">{analytics.attempted}</div>
                <div className="label">Attempted</div>
              </div>
              {analytics.timePerQ && (
                <div className="result-stat">
                  <div className="value">~{analytics.timePerQ}s</div>
                  <div className="label">Avg/Question</div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* ── Section-wise Scores ─────────────────────────────────────────────── */}
      {Object.keys(sectionScores).length > 0 && analytics && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>📊 Section-wise Scores</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Section</th><th>Score</th><th>Accuracy</th><th>Correct</th><th>Wrong</th></tr>
              </thead>
              <tbody>
                {Object.entries(sectionScores).map(([sec, sc]) => {
                  const s   = analytics.sectionMap[sec] || {};
                  const att = (s.correct || 0) + (s.wrong || 0);
                  const acc = att > 0 ? Math.round((s.correct / att) * 100) : 0;
                  const { cls, label } = accBadge(acc);
                  return (
                    <tr key={sec}>
                      <td>{sec}</td>
                      <td>
                        <span style={{ color: sc >= 0 ? 'var(--success)' : 'var(--danger)', fontWeight: 700 }}>
                          {sc >= 0 ? '+' : ''}{sc}
                        </span>
                      </td>
                      <td><span className={`badge ${cls}`}>{att > 0 ? label : '—'}</span></td>
                      <td style={{ color: 'var(--success)' }}>{s.correct || 0}</td>
                      <td style={{ color: 'var(--danger)' }}>{s.wrong || 0}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Weak Topics ─────────────────────────────────────────────────────── */}
      {analytics?.weakSections?.length > 0 && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>⚠️ Weak Areas — Focus Here</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem' }}>
            Sections where your accuracy was below 60%. Prioritize these in your next revision.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '0.75rem' }}>
            {analytics.weakSections.map((s, i) => (
              <div key={i} style={{
                background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.25)',
                borderRadius: '0.65rem', padding: '0.85rem 1rem',
              }}>
                <div style={{ fontWeight: 700, marginBottom: '0.3rem', fontSize: '0.9rem' }}>{s.name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.6rem' }}>
                  Accuracy: <strong style={{ color: 'var(--danger)' }}>{s.accuracy}%</strong>
                  &nbsp;· {s.wrong} wrong, {s.correct} correct
                </div>
                <Link
                  to={`/resources?exam=${review.exam_type}&topic=${encodeURIComponent(s.name)}`}
                  className="btn btn-sm btn-secondary"
                  style={{ fontSize: '0.78rem', display: 'inline-block' }}
                >
                  📖 Study This
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Question-by-Question Review ─────────────────────────────────────── */}
      <div className="card">
        <h3 style={{ marginBottom: '1rem' }}>🔍 Question-by-Question Review</h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
          Click any question to see the AI step-by-step solution + 2 similar practice questions.
        </p>

        {review.questions?.map((q, i) => (
          <div key={i}>
            <div
              className={`review-item ${q.is_correct ? 'correct' : q.selected_option ? 'wrong' : 'skipped'}`}
              onClick={() => loadExplanation(q)}
              style={{ cursor: 'pointer' }}
            >
              <div className="review-num">
                {q.is_correct ? '✅' : q.selected_option ? '❌' : '⬜'} Q{q.order}
              </div>
              <div className="review-text">{q.question}</div>
              <div className="review-answers">
                <span className="ra-label">Your:</span>
                <span style={{ color: q.is_correct ? 'var(--success)' : 'var(--danger)' }}>
                  {q.selected_option || '—'}
                </span>
                <span className="ra-label">Correct:</span>
                <span style={{ color: 'var(--success)' }}>{q.correct_option}</span>
                <span className="badge badge-info">{q.section || q.subject}</span>
              </div>
            </div>

            {/* ── AI Explanation panel ── */}
            {selectedQ?.question_id === q.question_id && (
              <div className="ai-expl-panel fade-in">
                {loadingExpl ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1.5rem' }}>
                    <div className="spinner" style={{ width: 28, height: 28, flexShrink: 0 }}></div>
                    <span style={{ color: 'var(--text-muted)' }}>🤖 AI is solving step by step…</span>
                  </div>
                ) : aiExpl ? (
                  <>
                    <div className="ai-step"><span className="step-label">Step 1 — Problem</span><div className="step-body markdown"><MarkdownRenderer content={aiExpl.step1_restatement} /></div></div>
                    <div className="ai-step"><span className="step-label">Step 2 — Concepts</span><div className="step-body markdown"><MarkdownRenderer content={aiExpl.step2_concepts} /></div></div>
                    <div className="ai-step"><span className="step-label">Step 3 — Working</span><div className="step-body markdown"><MarkdownRenderer content={aiExpl.step3_working} /></div></div>
                    <div className="ai-step"><span className="step-label">Step 4 — Answer</span><div className="step-body markdown"><MarkdownRenderer content={aiExpl.step4_answer} /></div></div>
                    {aiExpl.step5_similar?.length > 0 && (
                      <div className="ai-step">
                        <span className="step-label">Step 5 — Similar Practice Questions</span>
                        {aiExpl.step5_similar.map((sq, j) => (
                          <div key={j} className="similar-q-card">
                            <p><strong>Q{j + 1}:</strong> {sq.text}</p>
                            {['A', 'B', 'C', 'D'].map(opt => (
                              <p key={opt} style={{ color: sq.correct_option === opt ? 'var(--success)' : 'var(--text-secondary)', fontSize: '0.85rem' }}>
                                {sq.correct_option === opt ? '✅' : '○'} {opt}: {sq[`option_${opt.toLowerCase()}`]}
                              </p>
                            ))}
                            {sq.explanation && <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.5rem' }}>💡 {sq.explanation}</p>}
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <p style={{ color: 'var(--text-muted)', padding: '1rem' }}>Could not load explanation. Please try again.</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
        <Link to="/exams" className="btn btn-primary btn-lg">🔄 Take Another Exam</Link>
        <Link to="/"     className="btn btn-secondary btn-lg">Dashboard</Link>
      </div>
    </div>
  );
}
