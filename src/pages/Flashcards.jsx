import { useState, useEffect } from 'react';
import { api } from '../api/client';

export default function Flashcards() {
  const [examTypes, setExamTypes] = useState([]);
  const [selectedExam, setSelectedExam] = useState('');
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => { api.getExamTypes().then(setExamTypes).catch(console.error); }, []);

  const loadCards = async (et) => {
    setSelectedExam(et);
    setLoading(true);
    setCurrentIdx(0);
    setFlipped(false);
    try {
      const qs = await api.getQuestions({ exam_type: et, limit: 50 });
      setQuestions(qs.sort(() => Math.random() - 0.5));
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const next = () => { setFlipped(false); setCurrentIdx(i => Math.min(i + 1, questions.length - 1)); };
  const prev = () => { setFlipped(false); setCurrentIdx(i => Math.max(i - 1, 0)); };
  const q = questions[currentIdx];

  return (
    <div className="page fade-in">
      <div className="page-header">
        <h1>Flashcards</h1>
        <p>Tap a card to reveal the answer. Study smarter, not harder!</p>
      </div>

      <div className="filter-bar">
        <select className="form-select" value={selectedExam} onChange={e => loadCards(e.target.value)}>
          <option value="">Select Exam Type</option>
          {examTypes.map(et => <option key={et} value={et}>{et.replace(/_/g, ' ')}</option>)}
        </select>
        {questions.length > 0 && (
          <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Card {currentIdx + 1} of {questions.length}
          </span>
        )}
      </div>

      {loading && <div className="loader"><div className="spinner"></div></div>}

      {!loading && questions.length > 0 && q && (
        <>
          <div className={`flashcard ${flipped ? 'flipped' : ''}`} onClick={() => setFlipped(!flipped)} style={{ maxWidth: '600px', margin: '0 auto 1.5rem' }}>
            <div className="flashcard-inner">
              <div className="flashcard-front">
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>{q.subject} · {q.topic} · {q.difficulty}</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 500 }}>{q.text}</div>
                  <div style={{ marginTop: '1.5rem', fontSize: '0.8rem', color: 'var(--accent)' }}>Tap to reveal answer</div>
                </div>
              </div>
              <div className="flashcard-back">
                <div>
                  <div style={{ fontSize: '0.85rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Answer</div>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '0.75rem' }}>
                    {q[`option_${q.correct_option?.toLowerCase()}`] || q.correct_option}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Option {q.correct_option}</div>
                </div>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            <button className="btn btn-secondary" onClick={prev} disabled={currentIdx === 0}>← Previous</button>
            <button className="btn btn-primary" onClick={next} disabled={currentIdx === questions.length - 1}>Next →</button>
          </div>

          <div style={{ marginTop: '2rem' }}>
            <h3 style={{ fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>All Options</h3>
            <div className="options-list" style={{ maxWidth: '600px', margin: '0 auto' }}>
              {['A', 'B', 'C', 'D'].map(opt => (
                <div key={opt} className={`option-btn ${flipped && opt === q.correct_option ? 'correct' : ''}`} style={{ cursor: 'default' }}>
                  <span className="option-label">{opt}</span>
                  <span>{q[`option_${opt.toLowerCase()}`]}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {!loading && selectedExam && questions.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p>No flashcards available for this exam type.</p>
        </div>
      )}

      {!selectedExam && (
        <div className="card-grid">
          {examTypes.map(et => (
            <div key={et} className="exam-type-card" onClick={() => loadCards(et)}>
              <div className="exam-icon">📇</div>
              <h3>{et.replace(/_/g, ' ')}</h3>
              <p>Study with flashcards</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
