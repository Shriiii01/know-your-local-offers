// frontend/src/api.ts

export interface ChatResponse {
  response: string;
  language: string;
}

export interface OCRResponse {
  extracted_text: string;
  explanation: string;
}

export interface MultimodalRequest {
  text?: string;
  audio?: Blob | null;
  document?: File | null;
  language: string;
}

export async function sendMessage(
  text: string,
  language: string
): Promise<string> {
  const res = await fetch("http://localhost:8000/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text, language }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Network error");
  }
  const data: ChatResponse = await res.json();
  return data.response;
}

export async function transcribeAudio(audioBlob: Blob): Promise<string> {
  const formData = new FormData();
  formData.append('file', audioBlob, 'recording.wav');

  const res = await fetch("http://localhost:8000/voice/transcribe", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Transcription failed");
  }

  const data = await res.json();
  return data.transcript;
}

export async function synthesizeSpeech(text: string, language: string): Promise<Blob> {
  const res = await fetch("http://localhost:8000/voice/synthesize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text, language }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Speech synthesis failed");
  }

  return res.blob();
}

export async function extractTextFromImage(file: File): Promise<OCRResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('language', 'en'); // You can make this dynamic if needed

  const res = await fetch("http://localhost:8000/ocr", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "OCR processing failed");
  }

  return res.json();
}

export async function sendMultimodalMessage(request: MultimodalRequest): Promise<string> {
  const formData = new FormData();
  
  // Add text
  if (request.text) {
    formData.append('text', request.text);
  }
  
  // Add audio
  if (request.audio) {
    formData.append('audio', request.audio, 'recording.wav');
  }
  
  // Add document
  if (request.document) {
    formData.append('document', request.document);
  }
  
  // Add language
  formData.append('language', request.language);

  const res = await fetch("http://localhost:8000/multimodal", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Multimodal processing failed");
  }

  const data = await res.json();
  return data.response;
}