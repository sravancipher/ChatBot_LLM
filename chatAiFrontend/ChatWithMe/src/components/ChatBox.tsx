// src/components/ChatBox.tsx
import React from 'react';
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import oneDark from "react-syntax-highlighter/dist/esm/styles/prism/one-dark";

interface Message {
  text: string;
  sender: 'user' | 'bot';
  file?: File | undefined| string; 
}

interface ChatBoxProps {
  messages: Message[];                  
  loading: boolean; 
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages, loading }) => {
  const renderFileAttachment = (file: File | string | undefined) => {
    if (typeof file === 'string') {
      return <span>{file}</span>;
    }
    if (file && file.type.startsWith('image')) {
      return <img src={URL.createObjectURL(file)} alt="attachment" className="attachment-image" />;
    }
    return <span>{file.name}</span>;
  };

  return (
    <div className="chat-box">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.sender}`}>
          <ReactMarkdown components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              return !inline && match ? (
                <SyntaxHighlighter
                  style={oneDark}
                  language={match[1]}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}>
            {message.text}
          </ReactMarkdown>
          {message.file && <div className="file-attachment">{renderFileAttachment(message.file)}</div>}
        </div>
      ))}
      {loading && (
        <div className="loading-container">
          <div className="typing">ParaBot Typing...</div>
        </div>
      )}
    </div>
  );
  
};

export default ChatBox;
