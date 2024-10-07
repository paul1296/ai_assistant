from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from agent_ai.gpt import generate_response
from agent_ai.fine_tune import check_fine_tune_status
from twilio.twiml.messaging_response import MessagingResponse
from agent_ai.schemas import schemas
# Initialize FastAPI app
app = FastAPI()

# Generate Response to twilio request
@app.post("/whatsapp_response")
async def whatsapp_response(request: Request):
    twilio_body = await request.json()
    message = twilio_body['Body']
    #sender = twilio_body['From']
    incoming_msg = request.values.get('Body', '').strip()
    # Generate prompt response
    content = generate_response(incoming_message)

    return JSONResponse(content=content, media_type="application/xml")

@app.get("/fine_tune")
async def setup_fine_tune() -> str:
    if check_fine_tune_status():
        return "Fine tune setup"
    return "Max retries exceeded. Unable to retrieve the status."

# For local testing without Twilio (optional endpoint)
@app.post("/test")
async def test_message(message: schemas.Message):
    content = generate_response(message.Body)
    return JSONResponse(content=content, media_type="application/xml")


