
import { useState } from 'react';
import ChatBox from './ChatBox';
import ChatInput from './ChatInput';

import Logo from './Logo.png'
interface Message {
  text: string;
  sender: 'user' | 'bot';
  file?: File | undefined | string; 
}

function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [file, setFile] = useState<File | null>(null); 
  const [loading, setLoading] = useState<boolean>(false); 

  const sendMessage = async (userMessage: string) => {
    const newMessage: Message = { text: userMessage, sender: 'user', file:file ?? undefined };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setLoading(true); 
  
    const formData = new FormData();
    formData.append('query', userMessage); 
  
    if (file) {
      formData.append('file', file); 
      console.log("file",file)
    }
  
    try {
      console.log('Sending request to the backend...');
      const response = await fetch('http://localhost:8000/process_input/', {
        method: 'POST',
        body: formData,
        
      });

    //   console.log("response",response)
      if (response.ok) {
        const data = await response.json();
        // console.log("response",data)
        if (Array.isArray(data.data)) {
          const botMessage: Message = { text: data.data.toString(), sender: 'bot' };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        } else if (typeof data.data === 'object') {
          const botMessage: Message = { text: data.data.content, sender: 'bot' };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        } else {
          const botMessage: Message = { text: data.data, sender: 'bot' };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        }
      } else {
        console.error('Failed to fetch response:', response.statusText);
        const errorMessage: Message = {
          text: 'There was an error processing your request.',
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    } catch (error) {
      console.error('Error occurred while fetching:', error);
      const errorMessage: Message = {
        text: 'There was an error communicating with the server.',
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  
    setFile(null); 
    setLoading(false); 
  };

  return (
    <div className="App">
      <header className="header">
      <img src={Logo} alt="Logo" style={{width:"30px",height:"30px"}}/>
        <h1 style={{color:"#0455BF"}}>ParaBot</h1>
      </header>
      <ChatBox messages={messages} loading={loading} />
      <ChatInput onSendMessage={sendMessage} setFile={setFile} />
    </div>
  );
}

export default ChatBot;
