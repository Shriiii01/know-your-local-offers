/**
 * Know Your Local Offers - Frontend Application
 * Main React component for the local business offers discovery platform
 * Supports text chat, voice input, OCR, and multimodal interactions
 */
import React, { useState, useRef, useEffect } from 'react';
import { sendMessage, transcribeAudio, synthesizeSpeech, extractTextFromImage, sendMultimodalMessage } from './api';

interface Message {
  text: string;
  sender: 'user' | 'ai';
  type?: 'text' | 'document' | 'error' | 'multimodal';
  fileName?: string;
  hasAudio?: boolean;
  hasDocument?: boolean;
  id: string; // Add unique ID for each message
}

interface InputState {
  text: string;
  audioBlob: Blob | null;
  audioTranscript: string;
  document: File | null;
  isRecording: boolean;
}

interface SpeechState {
  speaking: boolean;
  currentMessageId: string | null;
  utterance: SpeechSynthesisUtterance | null;
  audioElement: HTMLAudioElement | null;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  
  // Combined input state
  const [inputState, setInputState] = useState<InputState>({
    text: '',
    audioBlob: null,
    audioTranscript: '',
    document: null,
    isRecording: false
  });

  // Speech control state
  const [speechState, setSpeechState] = useState<SpeechState>({
    speaking: false,
    currentMessageId: null,
    utterance: null,
    audioElement: null
  });
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Generate unique ID for messages
  const generateMessageId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Clean up speech when component unmounts
  useEffect(() => {
    return () => {
      stopAllSpeech();
    };
  }, []);

  const addMessage = (message: Omit<Message, 'id'>) => {
    const messageWithId = { ...message, id: generateMessageId() };
    setMessages(prev => [...prev, messageWithId]);
  };

  // CLEAN SPEECH CONTROLS
  const stopAllSpeech = () => {
    // Stop Web Speech API
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
    }
    
    // Stop server TTS audio
    if (speechState.audioElement) {
      speechState.audioElement.pause();
      speechState.audioElement.currentTime = 0;
      speechState.audioElement = null;
    }
    
    // Clear state
    setSpeechState({
      speaking: false,
      currentMessageId: null,
      utterance: null,
      audioElement: null
    });
  };

  const speakMessage = async (messageId: string, text: string) => {
    // If currently speaking, stop everything
    if (speechState.speaking) {
      stopAllSpeech();
      return;
    }

    try {
      // Always try Web Speech API first (faster, native)
      if ('speechSynthesis' in window && speechSynthesis.getVoices().length > 0) {
        startWebSpeech(messageId, text);
      } else {
        // Fallback to server TTS
        await startServerTTS(messageId, text);
      }
    } catch (error) {
      console.error('Error starting speech:', error);
      setSpeechState({
        speaking: false,
        currentMessageId: null,
        utterance: null,
        audioElement: null
      });
    }
  };

  const startWebSpeech = (messageId: string, text: string) => {
    // Ensure we're not already speaking
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Configure voice settings
    utterance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    // Set up event handlers
    utterance.onstart = () => {
      setSpeechState({
        speaking: true,
        currentMessageId: messageId,
        utterance: utterance,
        audioElement: null
      });
    };

    utterance.onend = () => {
      setSpeechState({
        speaking: false,
        currentMessageId: null,
        utterance: null,
        audioElement: null
      });
    };

    utterance.onerror = (event) => {
      console.error('Web Speech API error:', event.error);
      setSpeechState({
        speaking: false,
        currentMessageId: null,
        utterance: null,
        audioElement: null
      });
    };

    // Start speaking
    speechSynthesis.speak(utterance);
  };

  const startServerTTS = async (messageId: string, text: string) => {
    try {
      // Set speaking state immediately
      setSpeechState({
        speaking: true,
        currentMessageId: messageId,
        utterance: null,
        audioElement: null
      });

      const audioBlob = await synthesizeSpeech(text, language);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      // Update state with audio element
      setSpeechState(prev => ({
        ...prev,
        audioElement: audio
      }));

      audio.onended = () => {
        setSpeechState({
          speaking: false,
          currentMessageId: null,
          utterance: null,
          audioElement: null
        });
        URL.revokeObjectURL(audioUrl);
      };

      audio.onerror = () => {
        setSpeechState({
          speaking: false,
          currentMessageId: null,
          utterance: null,
          audioElement: null
        });
        URL.revokeObjectURL(audioUrl);
      };

      await audio.play();
    } catch (error) {
      console.error('Server TTS failed:', error);
      setSpeechState({
        speaking: false,
        currentMessageId: null,
        utterance: null,
        audioElement: null
      });
    }
  };

  // Clear all inputs
  const clearInputs = () => {
    setInputState({
      text: '',
      audioBlob: null,
      audioTranscript: '',
      document: null,
      isRecording: false
    });
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // TEXT INPUT
  const handleTextChange = (text: string) => {
    setInputState(prev => ({ ...prev, text }));
  };

  // DOCUMENT INPUT
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setInputState(prev => ({ ...prev, document: file }));
    }
  };

  const removeDocument = () => {
    setInputState(prev => ({ ...prev, document: null }));
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // AUDIO INPUT
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        
        // Transcribe the audio but don't send yet
        try {
          const transcript = await transcribeAudio(audioBlob);
          setInputState(prev => ({ 
            ...prev, 
            audioBlob, 
            audioTranscript: transcript,
            isRecording: false 
          }));
        } catch (error) {
          console.error('Error transcribing audio:', error);
          addMessage({
            text: language === 'hi'
              ? 'ऑडियो ट्रांसक्रिप्शन में त्रुटि।'
              : 'Error transcribing audio.',
            sender: 'ai',
            type: 'error'
          });
          setInputState(prev => ({ ...prev, isRecording: false }));
        }
        
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setInputState(prev => ({ ...prev, isRecording: true }));
    } catch (error) {
      console.error('Error starting recording:', error);
      addMessage({
        text: language === 'hi'
          ? 'माइक्रोफ़ोन एक्सेस अनुमति नहीं मिली।'
          : 'Microphone access denied.',
        sender: 'ai',
        type: 'error'
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && inputState.isRecording) {
      mediaRecorderRef.current.stop();
    }
  };

  const removeAudio = () => {
    setInputState(prev => ({ 
      ...prev, 
      audioBlob: null, 
      audioTranscript: '' 
    }));
  };

  // MAIN SEND FUNCTION
  const handleSend = async () => {
    const { text, audioBlob, audioTranscript, document } = inputState;
    
    // Check if we have any input
    const hasText = text.trim();
    const hasAudio = audioBlob;
    const hasDocument = document;
    
    if (!hasText && !hasAudio && !hasDocument) return;

    // Create user message description
    let userMessageText = '';
    if (hasText) userMessageText += text;
    if (hasAudio) {
      if (userMessageText) userMessageText += '\n';
      userMessageText += `🎤 "${audioTranscript}"`;
    }
    if (hasDocument) {
      if (userMessageText) userMessageText += '\n';
      userMessageText += `📄 ${document.name}`;
    }

    // Add user message
    addMessage({
      text: userMessageText,
      sender: 'user',
      type: 'multimodal',
      hasAudio: !!hasAudio,
      hasDocument: !!hasDocument,
      fileName: document?.name
    });

    clearInputs();
    setLoading(true);

    try {
      let response: string;

      // If we have multiple inputs, use multimodal endpoint
      if ((hasText && hasAudio) || (hasText && hasDocument) || (hasAudio && hasDocument) || (hasText && hasAudio && hasDocument)) {
        response = await sendMultimodalMessage({
          text: hasText ? text : hasAudio ? audioTranscript : '',
          audio: audioBlob,
          document: document,
          language
        });
      }
      // Single document
      else if (hasDocument && !hasText && !hasAudio) {
        const result = await extractTextFromImage(document);
        response = `**Extracted Text:**\n${result.extracted_text}\n\n**Analysis:**\n${result.explanation}`;
      }
      // Single text or audio
      else {
        const messageText = hasText ? text : audioTranscript;
        response = await sendMessage(messageText, language);
      }

      // Add AI response - NO AUTO-SPEAKING!
      addMessage({
        text: response,
        sender: 'ai'
      });

    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({
        text: language === 'hi'
          ? 'कुछ गलत हो गया। फिर से कोशिश करें।'
          : 'Something went wrong. Please try again.',
        sender: 'ai',
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Check if we have any input to send
  const hasAnyInput = inputState.text.trim() || inputState.audioBlob || inputState.document;

  const renderMessage = (msg: Message, idx: number) => {
    const isUser = msg.sender === 'user';
    const isError = msg.type === 'error';
    const isCurrentlySpeaking = speechState.speaking && speechState.currentMessageId === msg.id;
    
    return (
      <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className={`max-w-[80%] ${isUser ? 'flex flex-col items-end' : 'flex flex-col items-start'}`}>
          <div className={`px-4 py-3 rounded-2xl ${
            isUser 
              ? 'bg-blue-600 text-white' 
              : isError 
                ? 'bg-red-100 text-red-800 border border-red-200'
                : 'bg-gray-100 text-gray-800'
          }`}>
            <div className="whitespace-pre-wrap break-words">
              {msg.text.split('\n').map((line, i) => (
                <div key={i}>
                  {line.startsWith('**') && line.endsWith('**') ? (
                    <strong className="font-semibold">{line.slice(2, -2)}</strong>
                  ) : line}
                </div>
              ))}
            </div>
            {(msg.hasAudio || msg.hasDocument) && (
              <div className="flex gap-2 mt-2 text-xs opacity-75">
                {msg.hasAudio && <span className="bg-white/20 px-2 py-1 rounded">🎤 Audio</span>}
                {msg.hasDocument && <span className="bg-white/20 px-2 py-1 rounded">📄 Document</span>}
              </div>
            )}
          </div>
          
          {/* Speak Button for AI messages only */}
          {!isUser && !isError && (
            <button
              onClick={() => speakMessage(msg.id, msg.text)}
              disabled={speechState.speaking && !isCurrentlySpeaking}
              className={`mt-2 px-3 py-1 rounded-full text-sm font-medium transition-all ${
                isCurrentlySpeaking
                  ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse'
                  : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isCurrentlySpeaking ? '⏹️ Stop' : '🔊 Speak'}
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm shadow-sm border-b border-white/20 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                🏥
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Health Assistant
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {/* Global Speech Control */}
              {speechState.speaking && (
                <button
                  onClick={stopAllSpeech}
                  className="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 text-sm font-medium"
                >
                  🔇 Stop All Speech
                </button>
              )}
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white/80 backdrop-blur-sm"
              >
                <option value="hi">हिंदी</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 h-[70vh] flex flex-col">
          {/* Messages Area */}
          <div 
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto p-6 space-y-1"
            style={{ scrollBehavior: 'smooth' }}
          >
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-3xl mx-auto mb-4">
                    🏥
                  </div>
                  <h2 className="text-2xl font-semibold mb-2 text-gray-700">
                    {language === 'hi' ? 'नमस्ते! मैं आपका स्वास्थ्य सहायक हूं।' : 'Hello! I am your health assistant.'}
                  </h2>
                  <p className="text-lg mb-6">
                    {language === 'hi' ? 'अपनी स्वास्थ्य समस्या बताएं' : 'Tell me about your health concern'}
                  </p>
                  <div className="flex justify-center gap-3">
                    <div className="px-3 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">💬 Text</div>
                    <div className="px-3 py-2 bg-green-100 text-green-700 rounded-full text-sm">📄 Document</div>
                    <div className="px-3 py-2 bg-purple-100 text-purple-700 rounded-full text-sm">🎤 Voice</div>
                    <div className="px-3 py-2 bg-orange-100 text-orange-700 rounded-full text-sm">🔗 Combined</div>
                  </div>
                  <p className="text-sm text-gray-400 mt-4">
                    {language === 'hi' ? 'उत्तर सुनने के लिए 🔊 Speak बटन दबाएं' : 'Click 🔊 Speak to hear responses'}
                  </p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, idx) => renderMessage(msg, idx))}
                {loading && (
                  <div className="flex justify-start mb-4">
                    <div className="bg-gray-100 px-4 py-3 rounded-2xl">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200/50 p-4 bg-white/50 backdrop-blur-sm rounded-b-3xl">
            
            {/* Active Inputs Display */}
            <div className="space-y-2 mb-4">
              {/* Document Display */}
              {inputState.document && (
                <div className="p-3 bg-green-50 border border-green-200 rounded-xl flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">📄</span>
                    <span className="text-sm text-green-800 font-medium">{inputState.document.name}</span>
                    <span className="text-xs text-green-600">
                      ({(inputState.document.size / 1024).toFixed(1)} KB)
                    </span>
                  </div>
                  <button
                    onClick={removeDocument}
                    className="text-green-600 hover:text-green-800 text-sm font-medium"
                  >
                    ✕
                  </button>
                </div>
              )}

              {/* Audio Display */}
              {inputState.audioBlob && (
                <div className="p-3 bg-purple-50 border border-purple-200 rounded-xl flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-purple-600">🎤</span>
                    <span className="text-sm text-purple-800">
                      "{inputState.audioTranscript}"
                    </span>
                  </div>
                  <button
                    onClick={removeAudio}
                    className="text-purple-600 hover:text-purple-800 text-sm font-medium"
                  >
                    ✕
                  </button>
                </div>
              )}

              {/* Recording Indicator */}
              {inputState.isRecording && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-red-800 font-medium">
                      {language === 'hi' ? 'रिकॉर्डिंग...' : 'Recording...'}
                    </span>
                  </div>
                  <button
                    onClick={stopRecording}
                    className="px-3 py-1 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700"
                  >
                    {language === 'hi' ? 'रोकें' : 'Stop'}
                  </button>
                </div>
              )}
            </div>

            <div className="flex space-x-3 items-end">
              {/* Input Controls */}
              <div className="flex space-x-2">
                {/* File Upload Button */}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={loading}
                  className={`p-3 rounded-xl transition-colors ${
                    inputState.document 
                      ? 'bg-green-600 text-white' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  } disabled:opacity-50`}
                  title={language === 'hi' ? 'दस्तावेज़ अपलोड करें' : 'Upload document'}
                >
                  📎
                </button>

                {/* Voice Button */}
                <button
                  onClick={inputState.isRecording ? stopRecording : startRecording}
                  disabled={loading}
                  className={`p-3 rounded-xl transition-colors ${
                    inputState.isRecording 
                      ? 'bg-red-600 text-white animate-pulse' 
                      : inputState.audioBlob
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  } disabled:opacity-50`}
                  title={language === 'hi' ? 'बोलने के लिए क्लिक करें' : 'Click to record'}
                >
                  🎤
                </button>
              </div>

              {/* Text Input */}
              <div className="flex-1">
                <textarea
                  value={inputState.text}
                  onChange={(e) => handleTextChange(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={language === 'hi' ? 'अपना सवाल यहाँ लिखें...' : 'Type your question here...'}
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none max-h-32 bg-white/80 backdrop-blur-sm"
                  disabled={loading}
                  rows={1}
                  style={{ minHeight: '48px' }}
                />
              </div>

              {/* Send Button */}
              <button
                onClick={handleSend}
                disabled={loading || !hasAnyInput}
                className={`px-6 py-3 rounded-xl font-semibold transition-all transform ${
                  loading
                    ? 'bg-gray-400 text-white cursor-not-allowed'
                    : hasAnyInput
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 hover:scale-105 shadow-lg'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                } disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none`}
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>{language === 'hi' ? 'भेज रहे हैं...' : 'Sending...'}</span>
                  </div>
                ) : (
                  language === 'hi' ? 'भेजें' : 'Send'
                )}
              </button>
            </div>

            {/* Input Summary */}
            {hasAnyInput && (
              <div className="mt-2 text-xs text-gray-500 flex gap-4">
                {inputState.text && <span>📝 Text ready</span>}
                {inputState.audioBlob && <span>🎤 Audio ready</span>}
                {inputState.document && <span>📄 Document ready</span>}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*,.pdf"
        onChange={handleFileSelect}
        className="hidden"
      />
    </div>
  );
}

export default App;