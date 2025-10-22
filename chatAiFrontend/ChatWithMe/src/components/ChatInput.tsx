import React, { useState } from 'react';
import AttachmentIcon from '@mui/icons-material/Attachment';
interface ChatInputProps {
  onSendMessage: (message: string) => void;
  setFile: (file: File | null) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, setFile }) => {
  const [input, setInput] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);

  const handleSendMessage = () => {
    if (input.trim() || fileName) {
      onSendMessage(input);
      setInput('');
      setFileName(null);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files ? e.target.files[0] : null;
    if (file) {
    
      setFile(file);
      setFileName(file.name);
    }
  };

  const handleAttachmentClick = () => {
    const fileInput = document.createElement('input');
    
    fileInput.type = 'file';
    fileInput.accept = '.txt,.pdf,.csv,.xls,.xlsx,.jpg,.png,.jpeg,.gif';
    fileInput.onchange = (e) => handleFileChange(e as any);
    fileInput.click();
  };

  return (
    <div className='bg-input'>
    <div className="chat-input">
      <button className="attachment-btn"  onClick={handleAttachmentClick}>
        <AttachmentIcon/>
      </button>
      {fileName && <span className="file-name">{fileName}</span>}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="I'm Parabot, here to help! Ask me anything"
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
    </div>
  );
};

export default ChatInput;
