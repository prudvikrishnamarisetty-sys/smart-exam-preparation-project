import { useState, useRef, useEffect } from 'react';
import { api } from '../api/client';
import MarkdownRenderer from '../components/MarkdownRenderer';

const STARTERS = [
  'Explain binary search with dry run',
  'What is database normalization?',
  'How does TCP 3-way handshake work?',
  'Difference between stack and queue',
  'What is time complexity of merge sort?',
  'Explain OSI model layers',
  'What is deadlock in OS?',
  'Difference between SQL and NoSQL',
];

// ── 24h client-side response cache ──────────────────────────────────────────
const CACHE_TTL = 24 * 60 * 60 * 1000;
const AI_CACHE_KEY = 'smartexam_ai_cache';

function simpleHash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) { h = (Math.imul(31, h) + str.charCodeAt(i)) | 0; }
  return h.toString(36);
}

function getCachedResponse(msg) {
  try {
    const store = JSON.parse(localStorage.getItem(AI_CACHE_KEY) || '{}');
    const entry = store[simpleHash(msg.toLowerCase().trim())];
    if (entry && Date.now() - entry.ts < CACHE_TTL) return entry.data;
  } catch (_) {}
  return null;
}

function setCachedResponse(msg, data) {
  try {
    const store = JSON.parse(localStorage.getItem(AI_CACHE_KEY) || '{}');
    const now = Date.now();
    for (const k of Object.keys(store)) { if (now - store[k].ts > CACHE_TTL) delete store[k]; }
    store[simpleHash(msg.toLowerCase().trim())] = { data, ts: now };
    localStorage.setItem(AI_CACHE_KEY, JSON.stringify(store));
  } catch (_) {}
}

function isComplex(msg) {
  return msg.length > 80 ||
    /code|algorithm|implement|write|explain|how|why|difference|compare|debug|error|program|function/i.test(msg);
}

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      text: `## Welcome to AI Assistant! 🤖\n\nI provide **5-step structured explanations** for any CSE or exam topic. You can also **📎 upload an image** (question paper, notes, diagram) and I will analyze it!\n\n**Text Chat:** Ask me anything about DSA, DBMS, OS, Networks, Java, Python...\n**📎 Image Upload:** Upload a photo of a question, handwritten notes, or any diagram for instant AI analysis.\n\n⚡ **Tip:** Common questions are cached locally for instant responses!`,
      followUps: STARTERS.slice(0, 4),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [activeTab, setActiveTab] = useState('chat');
  const bottomRef    = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = async (msg) => {
    if (!msg.trim() || loading) return;
    const userMsg = msg.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setLoading(true);

    // ── 1. Check 24h cache first (instant response) ──
    const cached = getCachedResponse(userMsg);
    if (cached) {
      setMessages(prev => [...prev, {
        role: 'ai',
        text: `⚡ *Instant answer (cached)*\n\n${cached.response}`,
        followUps: cached.follow_up_questions,
      }]);
      setLoading(false);
      return;
    }

    // ── 2. Quick acknowledgment for complex queries ──
    let ackIndex = null;
    if (isComplex(userMsg)) {
      setMessages(prev => {
        ackIndex = prev.length;
        return [...prev, {
          role: 'ai',
          text: `🤖 **Solving this step by step…**\n\n*Step 1: Understanding your question — "${userMsg.slice(0, 60)}${userMsg.length > 60 ? '…' : ''}"*`,
          isAck: true,
        }];
      });
    }

    try {
      const res = await api.aiChat({ message: userMsg });
      setMessages(prev => {
        const next = [...prev];
        const finalMsg = { role: 'ai', text: res.response, followUps: res.follow_up_questions };
        if (ackIndex !== null && next[ackIndex]?.isAck) next[ackIndex] = finalMsg;
        else next.push(finalMsg);
        return next;
      });
      setCachedResponse(userMsg, res);
    } catch (err) {
      setMessages(prev => {
        const next = [...prev];
        const errMsg = { role: 'ai', text: `**Error:** ${err.message}`, followUps: [] };
        if (ackIndex !== null && next[ackIndex]?.isAck) next[ackIndex] = errMsg;
        else next.push(errMsg);
        return next;
      });
    } finally { setLoading(false); }
  };

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setUploadedFile(f);
    setPreviewUrl(URL.createObjectURL(f));
  };

  const analyzeMedia = async () => {
    if (!uploadedFile || loading) return;
    const question = input.trim();
    setLoading(true);
    setMessages(prev => [...prev, {
      role: 'user',
      text: question ? `📎 *[Image uploaded]*\n\n${question}` : '📎 *[Image uploaded — please analyze this]*',
      imagePreview: previewUrl,
    }]);
    setInput('');
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      if (question) formData.append('question', question);
      const res = await api.analyzeMedia(formData);
      setMessages(prev => [...prev, {
        role: 'ai', text: res.response,
        followUps: res.follow_up_questions || [],
        questionsFound: res.questions_found,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: `**Error:** ${err.message}`, followUps: [] }]);
    } finally {
      setLoading(false);
      setUploadedFile(null); setPreviewUrl(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="page fade-in" style={{ maxWidth: 1400, display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px)', padding: '1.5rem' }}>
      <div className="page-header" style={{ marginBottom: '1rem' }}>
        <h1>AI Assistant</h1>
        <p>Ask questions or upload an image for instant AI analysis</p>
      </div>

      {/* Mode Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button className={`btn ${activeTab === 'chat' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('chat')}>
          💬 Text Chat
        </button>
        <button className={`btn ${activeTab === 'upload' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('upload')}>
          📎 Upload Image
        </button>
      </div>

      {/* Quick Starters */}
      {activeTab === 'chat' && (
        <div className="quick-starters">
          {STARTERS.map((s, i) => (
            <button key={i} className="starter-chip" onClick={() => send(s)}>{s}</button>
          ))}
        </div>
      )}

      {/* Chat Window */}
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-msg ${msg.role}`}>
            <div className="chat-avatar">{msg.role === 'ai' ? '🤖' : '👤'}</div>
            <div className="chat-bubble">
              {msg.imagePreview && (
                <img src={msg.imagePreview} alt="Uploaded" style={{ maxWidth: 260, maxHeight: 180, borderRadius: '0.5rem', marginBottom: '0.75rem', display: 'block' }} />
              )}
              {msg.questionsFound > 0 && (
                <div style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)', padding: '0.3rem 0.7rem', borderRadius: '0.4rem', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.5rem', display: 'inline-block' }}>
                  ✅ {msg.questionsFound} question{msg.questionsFound !== 1 ? 's' : ''} found and solved
                </div>
              )}
              <div className="chat-text"><MarkdownRenderer content={msg.text} /></div>
              {msg.followUps?.length > 0 && (
                <div className="follow-ups">
                  {msg.followUps.map((fq, j) => (
                    <button key={j} className="follow-chip" onClick={() => send(fq)}>{fq}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-msg ai">
            <div className="chat-avatar">🤖</div>
            <div className="chat-bubble">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <div className="typing-indicator"><span></span><span></span><span></span></div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>AI is thinking…</span>
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Upload Panel */}
      {activeTab === 'upload' ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div
            style={{ border: '2px dashed var(--border)', borderRadius: '0.75rem', padding: '2rem', textAlign: 'center', background: 'rgba(79,70,229,0.05)', cursor: 'pointer', transition: '0.2s' }}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={e => e.preventDefault()}
            onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) { setUploadedFile(f); setPreviewUrl(URL.createObjectURL(f)); } }}
          >
            {previewUrl
              ? <img src={previewUrl} alt="Preview" style={{ maxHeight: 200, borderRadius: '0.5rem', marginBottom: '0.5rem' }} />
              : <>
                  <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>📸</div>
                  <p style={{ color: 'var(--text-secondary)' }}>Click or drag & drop an image here</p>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.3rem' }}>Supports JPEG, PNG, GIF, WebP • Max 10 MB</p>
                </>
            }
            <input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileChange} />
          </div>
          {uploadedFile && <p style={{ color: 'var(--success)', fontSize: '0.9rem' }}>✅ Selected: {uploadedFile.name} ({(uploadedFile.size / 1024).toFixed(1)} KB)</p>}
          <div className="chat-input-row">
            <input className="chat-input" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && analyzeMedia()} placeholder="Optional: Ask a specific question about this image..." />
            <button className="btn btn-primary" onClick={analyzeMedia} disabled={loading || !uploadedFile} style={{ borderRadius: '2rem', padding: '0 1.5rem', whiteSpace: 'nowrap' }}>
              {loading ? '⏳' : '🔍 Analyze'}
            </button>
          </div>
        </div>
      ) : (
        <div className="chat-input-row">
          <input className="chat-input" value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send(input)}
            placeholder="Ask about binary search, SQL joins, OS scheduling, GATE patterns..." />
          <button className="btn btn-primary" onClick={() => send(input)} disabled={loading || !input.trim()}>
            {loading ? '⏳' : 'Send'}
          </button>
        </div>
      )}
    </div>
  );
}
