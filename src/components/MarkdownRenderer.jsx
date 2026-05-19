import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    fontFamily: 'Inter, sans-serif',
    primaryColor: '#e0e7ff',
    primaryTextColor: '#1e1b4b',
    primaryBorderColor: '#6366f1',
    lineColor: '#6366f1',
    secondaryColor: '#f3e8ff',
    tertiaryColor: '#f1f5f9'
  }
});

function Mermaid({ chart }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && chart) {
      mermaid.render(`mermaid-${Math.random().toString(36).substr(2, 9)}`, chart)
        .then(({ svg }) => {
          containerRef.current.innerHTML = svg;
        })
        .catch(error => {
          console.error("Mermaid parsing error:", error);
          containerRef.current.innerHTML = `<pre style="color:red;font-size:0.8rem">Mermaid syntax error</pre>`;
        });
    }
  }, [chart]);

  return <div ref={containerRef} className="mermaid-wrapper" style={{ margin: '1rem 0', display: 'flex', justifyContent: 'center' }} />;
}

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          const codeString = String(children).replace(/\n$/, '');
          
          if (!inline && match && match[1] === 'mermaid') {
            return <Mermaid chart={codeString} />;
          }
          
          return !inline ? (
            <pre className="custom-code-block" style={{ background: '#1e1b4b', padding: '1rem', borderRadius: '0.5rem', overflowX: 'auto', color: '#e0e7ff', margin: '1rem 0' }}>
              <code className={className} {...props}>
                {children}
              </code>
            </pre>
          ) : (
            <code className="custom-inline-code" style={{ background: 'rgba(99, 102, 241, 0.1)', color: '#4f46e5', padding: '0.1rem 0.3rem', borderRadius: '0.2rem', fontFamily: 'monospace' }} {...props}>
              {children}
            </code>
          );
        },
        h1: ({node, ...props}) => <h1 style={{ color: 'var(--accent)', margin: '1.5rem 0 0.5rem', fontSize: '1.5rem' }} {...props} />,
        h2: ({node, ...props}) => <h2 style={{ color: 'var(--accent)', margin: '1.2rem 0 0.5rem', fontSize: '1.3rem' }} {...props} />,
        h3: ({node, ...props}) => <h3 style={{ color: 'var(--text-main)', margin: '1rem 0 0.5rem', fontSize: '1.1rem' }} {...props} />,
        p: ({node, ...props}) => <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', lineHeight: 1.6 }} {...props} />,
        ul: ({node, ...props}) => <ul style={{ margin: '0.5rem 0 1rem 1.5rem', color: 'var(--text-secondary)' }} {...props} />,
        ol: ({node, ...props}) => <ol style={{ margin: '0.5rem 0 1rem 1.5rem', color: 'var(--text-secondary)' }} {...props} />,
        li: ({node, ...props}) => <li style={{ marginBottom: '0.3rem' }} {...props} />,
        a: ({node, ...props}) => <a style={{ color: 'var(--accent)', textDecoration: 'underline' }} {...props} />,
        table: ({node, ...props}) => (
          <div style={{ overflowX: 'auto', margin: '1rem 0' }}>
            <table className="md-table" style={{ width: '100%', borderCollapse: 'collapse' }} {...props} />
          </div>
        ),
        th: ({node, ...props}) => <th style={{ border: '1px solid var(--border)', padding: '0.5rem', background: 'var(--card-bg-alt)' }} {...props} />,
        td: ({node, ...props}) => <td style={{ border: '1px solid var(--border)', padding: '0.5rem' }} {...props} />,
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
