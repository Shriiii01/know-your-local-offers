import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';

// Mock the API module
jest.mock('../api', () => ({
  sendMessage: jest.fn(),
  transcribeAudio: jest.fn(),
  synthesizeSpeech: jest.fn(),
  extractTextFromImage: jest.fn(),
  sendMultimodalMessage: jest.fn(),
}));

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders chat interface', () => {
    render(<App />);
    
    // Check if main elements are rendered
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /microphone/i })).toBeInTheDocument();
  });

  test('sends text message', async () => {
    const mockSendMessage = require('../api').sendMessage;
    mockSendMessage.mockResolvedValue({ response: 'Test response' });

    render(<App />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('Test message', 'en');
    });
  });

  test('handles empty message', () => {
    render(<App />);
    
    const sendButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(sendButton);
    
    // Should not send empty message
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  });

  test('changes language', () => {
    render(<App />);
    
    const languageSelect = screen.getByRole('combobox');
    fireEvent.change(languageSelect, { target: { value: 'hi' } });
    
    expect(languageSelect).toHaveValue('hi');
  });

  test('handles file upload', async () => {
    const mockExtractText = require('../api').extractTextFromImage;
    mockExtractText.mockResolvedValue('Extracted text');
    
    render(<App />);
    
    const file = new File(['test'], 'test.png', { type: 'image/png' });
    const fileInput = screen.getByLabelText(/upload file/i);
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(screen.getByText(/test\.png/i)).toBeInTheDocument();
    });
  });

  test('handles audio recording', async () => {
    // Mock MediaRecorder
    const mockMediaRecorder = {
      start: jest.fn(),
      stop: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };
    
    global.MediaRecorder = jest.fn().mockImplementation(() => mockMediaRecorder);
    global.navigator.mediaDevices = {
      getUserMedia: jest.fn().mockResolvedValue('mock-stream'),
    };
    
    render(<App />);
    
    const recordButton = screen.getByRole('button', { name: /microphone/i });
    fireEvent.click(recordButton);
    
    await waitFor(() => {
      expect(mockMediaRecorder.start).toHaveBeenCalled();
    });
  });

  test('displays error messages', async () => {
    const mockSendMessage = require('../api').sendMessage;
    mockSendMessage.mockRejectedValue(new Error('API Error'));
    
    render(<App />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('handles keyboard shortcuts', () => {
    render(<App />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    
    // Test Enter key
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' });
    
    // Test Ctrl+Enter for new line
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter', ctrlKey: true });
  });

  test('auto-scrolls to bottom on new message', () => {
    const mockScrollIntoView = jest.fn();
    Element.prototype.scrollIntoView = mockScrollIntoView;
    
    render(<App />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);
    
    expect(mockScrollIntoView).toHaveBeenCalled();
  });
}); 