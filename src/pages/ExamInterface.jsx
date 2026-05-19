import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import MarkdownRenderer from '../components/MarkdownRenderer';

const STATUS = { NOT_VISITED: 'not_visited', VISITED: 'visited', ANSWERED: 'answered', MARKED: 'marked_review', ANSWERED_MARKED: 'answered_marked' };



export default function ExamInterface() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const [exam, setExam] = useState(null);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState({});
  const [statuses, setStatuses] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Ask AI state
  const [aiPanel, setAiPanel] = useState(null);    // null | { loading, data }
  const [questionHovered, setQuestionHovered] = useState(false);
  const aiPanelRef = useRef(null);

  useEffect(() => {
    api.getExam(parseInt(examId)).then(e => {
      setExam(e);
      setTimeLeft(e.duration_minutes * 60);
      const init = {};
      e.exam_questions.forEach(eq => { init[eq.question_id] = STATUS.NOT_VISITED; });
      setStatuses(init);
    }).catch(() => navigate('/exams')).finally(() => setLoading(false));
  }, [examId]);

  const buildAnswerList = useCallback(() => {
    if (!exam) return [];
    return exam.exam_questions.map(eq => ({
      question_id: eq.question_id,
      selected_option: answers[eq.question_id] || null,
      marked_for_review: statuses[eq.question_id] === STATUS.MARKED || statuses[eq.question_id] === STATUS.ANSWERED_MARKED,
      visit_status: statuses[eq.question_id] || STATUS.NOT_VISITED,
    }));
  }, [exam, answers, statuses]);

  const handleSubmit = useCallback(async (auto = false) => {
    if (submitting) return;
    if (!auto && !window.confirm('Submit exam? You cannot change answers after submission.')) return;
    setSubmitting(true);
    try {
      const elapsed = exam.duration_minutes * 60 - timeLeft;
      await api.submitExam({ exam_id: exam.id, answers: buildAnswerList(), time_taken_seconds: elapsed });
      navigate(`/results/${exam.id}`);
    } catch (err) {
      alert(err.message || 'Submission failed');
      setSubmitting(false);
    }
  }, [exam, timeLeft, submitting, buildAnswerList]);

  useEffect(() => {
    if (!exam || timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) { clearInterval(timer); handleSubmit(true); return 0; }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [exam, handleSubmit]);

  const handleAskAI = async (q) => {
    setAiPanel({ loading: true, data: null });
    setTimeout(() => aiPanelRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    try {
      const result = await api.askAI({
        question_text: q.text,
        option_a: q.option_a,
        option_b: q.option_b,
        option_c: q.option_c,
        option_d: q.option_d,
        exam_context: exam?.exam_type?.replace(/_/g, ' ') || '',
      });
      setAiPanel({ loading: false, data: result });
    } catch (err) {
      setAiPanel({
        loading: false,
        data: {
          likely_answer: '?',
          confidence: 'low',
          explanation: '⚠️ AI is currently busy. Please try again in a moment.',
          follow_up: [],
        }
      });
    }
    setTimeout(() => aiPanelRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 200);
  };

  if (loading) return <div className="loader"><div className="spinner"></div></div>;
  if (!exam) return <div className="page"><p>Exam not found</p></div>;

  const questions = [...exam.exam_questions].sort((a, b) => a.order_num - b.order_num);
  const current = questions[currentQ];
  const q = current?.question;
  const qId = q?.id;
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const timerCls = timeLeft < 60 ? 'timer danger' : timeLeft < 300 ? 'timer warning' : 'timer';

  const markVisited = (qid) => {
    setStatuses(prev => {
      if (prev[qid] === STATUS.NOT_VISITED) return { ...prev, [qid]: STATUS.VISITED };
      return prev;
    });
  };

  const goTo = (idx) => {
    if (qId) markVisited(qId);
    setCurrentQ(idx);
    setAiPanel(null);
    const nextQid = questions[idx]?.question_id;
    if (nextQid) markVisited(nextQid);
  };

  const selectOption = (opt) => { setAnswers(prev => ({ ...prev, [qId]: opt })); };

  const saveAndNext = () => {
    if (answers[qId]) {
      const s = statuses[qId];
      setStatuses(prev => ({
        ...prev,
        [qId]: s === STATUS.MARKED || s === STATUS.ANSWERED_MARKED ? STATUS.ANSWERED_MARKED : STATUS.ANSWERED,
      }));
    } else {
      setStatuses(prev => ({ ...prev, [qId]: STATUS.VISITED }));
    }
    if (currentQ < questions.length - 1) goTo(currentQ + 1);
  };

  const clearResponse = () => {
    setAnswers(prev => { const n = { ...prev }; delete n[qId]; return n; });
    setStatuses(prev => ({ ...prev, [qId]: STATUS.VISITED }));
  };

  const markForReview = () => {
    const s = answers[qId] ? STATUS.ANSWERED_MARKED : STATUS.MARKED;
    setStatuses(prev => ({ ...prev, [qId]: s }));
    if (currentQ < questions.length - 1) goTo(currentQ + 1);
  };

  const getPaletteCls = (eq) => {
    const s = statuses[eq.question_id] || STATUS.NOT_VISITED;
    const map = {
      [STATUS.NOT_VISITED]: 'not-visited',
      [STATUS.VISITED]: 'not-answered',
      [STATUS.ANSWERED]: 'answered',
      [STATUS.MARKED]: 'marked-review',
      [STATUS.ANSWERED_MARKED]: 'answered-marked',
    };
    return `palette-btn ${map[s] || ''} ${questions[currentQ]?.question_id === eq.question_id ? 'current' : ''}`;
  };

  const counts = {
    answered: Object.values(statuses).filter(s => s === STATUS.ANSWERED).length,
    notAnswered: Object.values(statuses).filter(s => s === STATUS.VISITED).length,
    marked: Object.values(statuses).filter(s => s === STATUS.MARKED).length,
    answeredMarked: Object.values(statuses).filter(s => s === STATUS.ANSWERED_MARKED).length,
    notVisited: Object.values(statuses).filter(s => s === STATUS.NOT_VISITED).length,
  };

  const confidenceColor = {
    high: 'var(--success)',
    medium: '#f59e0b',
    low: 'var(--danger)',
  };

  return (
    <div className="exam-wrapper fade-in">
      {/* Sticky Header */}
      <div className="exam-header">
        <div>
          <strong>{exam.exam_type?.replace(/_/g, ' ')}</strong>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginLeft: '0.75rem' }}>
            Q {currentQ + 1} / {questions.length}
          </span>
        </div>
        <div className={timerCls}>{String(mins).padStart(2, '0')}:{String(secs).padStart(2, '0')}</div>
        <button className="btn btn-danger btn-sm" onClick={() => handleSubmit(false)} disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Exam'}
        </button>
      </div>

      <div className="exam-body">
        {/* Question Panel */}
        <div className="exam-main">
          <div className="question-card">
            <div className="question-meta">
              <span>Question {currentQ + 1}</span>
              <span className="marks-badge">+{q?.marks_per_question ?? exam.marks_per_q} &nbsp;|&nbsp; <span style={{ color: 'var(--danger)' }}>-{q?.negative_marks ?? exam.negative_marks_per_q}</span></span>
              <span className="subject-badge">{q?.section || q?.subject}</span>
            </div>

            {/* Question text with Ask AI hover */}
            <div
              style={{ position: 'relative' }}
              onMouseEnter={() => setQuestionHovered(true)}
              onMouseLeave={() => setQuestionHovered(false)}
            >
              <div className="question-text">{q?.text}</div>

              {/* Floating Ask AI button */}
              {questionHovered && q && (
                <button
                  onClick={() => handleAskAI(q)}
                  disabled={aiPanel?.loading}
                  style={{
                    position: 'absolute',
                    top: '50%',
                    right: '0.5rem',
                    transform: 'translateY(-50%)',
                    background: 'linear-gradient(135deg, #7c3aed, #4f46e5)',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '2rem',
                    padding: '0.35rem 0.85rem',
                    fontSize: '0.78rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    boxShadow: '0 4px 12px rgba(124,58,237,0.4)',
                    transition: 'all 0.2s',
                    zIndex: 10,
                    whiteSpace: 'nowrap',
                  }}
                >
                  🤖 Ask AI
                </button>
              )}
            </div>

            <div className="options-list">
              {['A', 'B', 'C', 'D'].map(opt => {
                const optText = q?.[`option_${opt.toLowerCase()}`];
                const isSelected = answers[qId] === opt;
                return (
                  <button key={opt} className={`option-btn ${isSelected ? 'selected' : ''}`} onClick={() => selectOption(opt)}>
                    <span className="option-label">{opt}</span>
                    <span>{optText}</span>
                  </button>
                );
              })}
            </div>

            {/* AI Answer Panel */}
            {aiPanel && (
              <div
                ref={aiPanelRef}
                style={{
                  marginTop: '1.25rem',
                  background: 'linear-gradient(135deg, rgba(124,58,237,0.08), rgba(79,70,229,0.08))',
                  border: '1px solid rgba(124,58,237,0.3)',
                  borderRadius: '0.75rem',
                  padding: '1.25rem',
                  animation: 'fadeIn 0.3s ease',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span style={{ fontWeight: 700, color: 'var(--accent)', fontSize: '0.95rem' }}>
                    🤖 AI Assistant
                  </span>
                  <button
                    onClick={() => setAiPanel(null)}
                    style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1.1rem', lineHeight: 1 }}
                  >✕</button>
                </div>

                {aiPanel.loading ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-secondary)' }}>
                    <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div>
                    <span style={{ fontSize: '0.9rem' }}>AI is analyzing this question…</span>
                  </div>
                ) : (
                  <>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                      <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Likely Answer:</span>
                      <span style={{
                        background: 'rgba(124,58,237,0.15)',
                        color: '#a78bfa',
                        fontWeight: 800,
                        fontSize: '1rem',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '0.4rem',
                      }}>
                        {aiPanel.data?.likely_answer || '?'}
                      </span>
                      <span style={{
                        fontSize: '0.75rem',
                        color: confidenceColor[aiPanel.data?.confidence] || 'var(--text-muted)',
                        fontWeight: 600,
                      }}>
                        ({aiPanel.data?.confidence} confidence)
                      </span>
                    </div>
                    <div style={{ maxHeight: 340, overflowY: 'auto', paddingRight: '0.25rem' }}>
                      <MarkdownRenderer content={aiPanel.data?.explanation} />
                    </div>
                    <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.75rem', borderTop: '1px solid var(--border)', paddingTop: '0.5rem' }}>
                      ⚠️ AI suggestions are indicative only. Trust your preparation for the final answer.
                    </p>
                  </>
                )}
              </div>
            )}

            {/* Action Buttons */}
            <div className="exam-actions" style={{ marginTop: '1rem' }}>
              <button className="btn btn-primary" onClick={saveAndNext}>Save &amp; Next</button>
              <button className="btn btn-secondary" onClick={clearResponse} disabled={!answers[qId]}>Clear Response</button>
              <button className="btn btn-review" onClick={markForReview}>Mark for Review &amp; Next</button>
            </div>
            {/* Nav */}
            <div className="question-nav">
              <button className="btn btn-secondary btn-sm" onClick={() => goTo(currentQ - 1)} disabled={currentQ === 0}>← Prev</button>
              <button className="btn btn-secondary btn-sm" onClick={() => goTo(currentQ + 1)} disabled={currentQ === questions.length - 1}>Next →</button>
            </div>
          </div>
        </div>

        {/* Palette Sidebar */}
        <div className="exam-sidebar">
          <div className="sidebar-card">
            <h4>Question Palette</h4>
            <div className="palette-legend-sm">
              <span className="pl-item"><span className="palette-btn not-visited sm">0</span> Not Visited ({counts.notVisited})</span>
              <span className="pl-item"><span className="palette-btn not-answered sm">0</span> Not Answered ({counts.notAnswered})</span>
              <span className="pl-item"><span className="palette-btn answered sm">0</span> Answered ({counts.answered})</span>
              <span className="pl-item"><span className="palette-btn marked-review sm">0</span> Marked ({counts.marked})</span>
              <span className="pl-item"><span className="palette-btn answered-marked sm">0</span> Ans+Marked ({counts.answeredMarked})</span>
            </div>
            <div className="palette">
              {questions.map((eq, i) => (
                <button key={i} className={getPaletteCls(eq)} onClick={() => goTo(i)}>{i + 1}</button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
