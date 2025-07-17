import os
import io
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse,PlainTextResponse
from pydantic import BaseModel 
from dotenv import load_dotenv
from typing import Optional
from twilio.twiml.messaging_response import MessagingResponse
# Import your handler classes
from chat_handler import ChatHandler
from ocr_handler import OCRHandler
from voice_handler import VoiceHandler
from supabase_client import supabase
from database_service import DatabaseService

load_dotenv()

chat_handler  = ChatHandler()
ocr_handler   = OCRHandler()
voice_handler = VoiceHandler()
db_service    = DatabaseService()

OPENAI_KEY      = os.getenv("OPENAI_API_KEY")
ELEVENLABS_KEY  = os.getenv("ELEVENLABS_API_KEY")

# Create FastAPI app
app = FastAPI(title="Health Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for text-based chat
class ChatRequest(BaseModel):
    message: str
    language: str = "en"  # Default English

class ChatResponse(BaseModel):
    response: str
    language: str

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Health Assistant API"}

# WhatsApp Webhook endpoint for Twilio
@app.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get form data from Twilio webhook
        form_data = await request.form()
        
        # Extract message details
        from_number = form_data.get('From', '')
        message_body = form_data.get('Body', '').strip()
        
        # No need for UTF-8 decoding since we're only using English
        # Just keep the message as-is
        
        print(f"WhatsApp message from {from_number}: {message_body}")
        
        # Handle greetings
        if is_greeting(message_body):
            response_text = get_welcome_message()
        else:
            # Always use English and only handle offers queries
            language = "en"
            
            # Check if this is an offers query
            if chat_handler._is_offers_query(message_body, language):
                # Generate offers response
                ai_response = await chat_handler.generate_reply(message_body, language)
            else:
                # Redirect non-offers queries to offers
                ai_response = "I can only help you find local offers and deals. Please ask me about offers in your city like 'gold offers in Kolhapur' or 'jewelry discounts in Sangli'."
            
            # Format response for WhatsApp (mobile-friendly)
            response_text = format_for_whatsapp(ai_response)
        
        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(response_text)
        
        return PlainTextResponse(content=str(twiml_response), media_type="application/xml")
        
    except Exception as e:
        print(f"WhatsApp webhook error: {e}")
        # Return error TwiML response
        error_response = MessagingResponse()
        error_response.message("Sorry, there was a technical issue. Please try again.")
        return PlainTextResponse(content=str(error_response), media_type="application/xml")

def is_greeting(message: str) -> bool:
    """Check if message is a greeting"""
    greetings = ['hi', 'hello', 'hey', 'start', 'help']
    return any(greeting in message.lower() for greeting in greetings)

def get_welcome_message() -> str:
    """Get welcome message for WhatsApp users"""
    return """Hello! Welcome to Local Offers Bot!

I help you find the best local offers and deals in your area:

Examples:
- "gold offers in Kolhapur"
- "jewelry discount in Sangli"
- "latest deals in Pune"
- "shops offering discounts"

Available cities: Kolhapur, Sangli, Pune, Mumbai
Available categories: Jewelry, Gold, Diamond

Ask me about offers in your city!"""

def format_for_whatsapp(message: str) -> str:
    """Format message for WhatsApp with proper length and mobile formatting"""
    MAX_LENGTH = 1500  # WhatsApp limit is 4096, but keeping it shorter for mobile
    
    # If message is too long, truncate it
    if len(message) > MAX_LENGTH:
        message = message[:MAX_LENGTH - 50] + "\n\nAsk for more information if needed!"
    
    # Add some mobile-friendly formatting for offers
    if "offer" in message.lower():
        # Add header for offers
        message = "BEST OFFERS:\n\n" + message
    
    return message

# Main chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await chat_handler.generate_reply(
            text=request.message,
            language=request.language
        )
        return ChatResponse(
            response=response,
            language=request.language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Multimodal endpoint (text + audio + document)
@app.post("/multimodal")
async def multimodal_endpoint(
    text: Optional[str] = Form(None),
    language: str = Form("en"),
    audio: Optional[UploadFile] = File(None),
    document: Optional[UploadFile] = File(None)
):
    try:
        combined_text = ""
        
        # Process text input
        if text:
            combined_text += f"User text: {text}\n\n"
        
        # Process audio input
        if audio:
            audio_data = await audio.read()
            transcript = await voice_handler.transcribe(audio_data)
            combined_text += f"User speech: {transcript}\n\n"
        
        # Process document input
        if document:
            doc_data = await document.read()
            extracted_text = await ocr_handler.extract_text(doc_data)
            combined_text += f"Document content: {extracted_text}\n\n"
        
        # If no inputs provided
        if not combined_text:
            raise HTTPException(status_code=400, detail="No input provided")
        
        # Add instruction for AI to analyze all inputs together
        analysis_prompt = f"""
        {combined_text}
        
        Please analyze all the provided inputs together and provide a comprehensive health-related response.
        If there's a document, relate your answer to its content.
        If there's speech and text, consider both in your response.
        """
        
        # Generate comprehensive response
        response = await chat_handler.generate_reply(
            text=analysis_prompt,
            language=language
        )
        
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2) OCR endpoint for prescriptions/reports
@app.post("/ocr")    
async def ocr_endpoint(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    # Read file bytes
    data = await file.read()
    # Extract raw text via OCR
    extracted = await ocr_handler.extract_text(data)
    # Explain it via LLM
    explanation = await chat_handler.generate_reply(
        text=f"Please analyze this medical document text and provide health insights: {extracted}",
        language=language
    )
    return {
        "extracted_text": extracted,
        "explanation": explanation
    }

# 3) Speech-to-text endpoint
@app.post("/voice/transcribe")  
async def transcribe_endpoint(file: UploadFile = File(...)):
    audio = await file.read()
    transcript = await voice_handler.transcribe(audio_bytes=audio)
    return {"transcript": transcript}

# 4) Text-to-speech endpoint
@app.post("/voice/synthesize")  
async def synthesize_endpoint(body: ChatRequest):
    audio_bytes = await voice_handler.synthesize(
        text=body.message,
        language=body.language
    )
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )

# New endpoints for database operations
@app.get("/api/offers")
async def get_offers(city: str = None, category: str = None, query: str = None, limit: int = 10):
    """Direct endpoint to search offers"""
    try:
        if query:
            offers = await db_service.search_offers(query, city, category, limit)
        elif city:
            offers = await db_service.get_offers_by_city(city, limit)
        elif category:
            offers = await db_service.get_offers_by_category(category, limit)
        else:
            # Get trending offers if no filters
            offers = await db_service.get_trending_offers(limit)
        
        return {"offers": offers, "count": len(offers), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cities")
async def get_cities():
    """Get list of available cities"""
    try:
        cities = await db_service.get_cities()
        return {"cities": cities, "count": len(cities)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    """Get list of available categories"""
    try:
        categories = await db_service.get_categories()
        return {"categories": categories, "count": len(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class OfferRequest(BaseModel):
    store_name: str
    city: str
    category: str
    offer_text: str
    price_range: Optional[str] = None
    valid_till: Optional[str] = None
    source: Optional[str] = "api"

@app.post("/api/offers")
async def add_offer(offer: OfferRequest):
    """Add a new offer to the database"""
    try:
        offer_data = offer.dict()
        success = await db_service.add_offer(offer_data)
        
        if success:
            return {"message": "Offer added successfully", "status": "success"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add offer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Allow `python app.py` to work by invoking Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)