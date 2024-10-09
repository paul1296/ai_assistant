from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response, JSONResponse
from agent_ai.gpt import generate_response
# from agent_ai.fine_tune import check_fine_tune_status
from twilio.twiml.messaging_response import MessagingResponse
from agent_ai.schemas import schemas
from sqlalchemy.orm import Session
from agent_ai.models.database import get_db
# Initialize FastAPI app
app = FastAPI()

# Generate Response to twilio request
@app.post("/whatsapp_response")
async def whatsapp_response(request: Request, db: Session = Depends(get_db)):
    print(request)
    form_data = await request.form()
    sender = form_data.get('From')
    print(sender)
    message = form_data.get('Body')
    incoming_msg = message.strip() if message else ''
    print(incoming_msg)
    # Generate prompt response
    content = generate_response(incoming_msg, sender, db)
    print(content)

    # Return the response as XML
    return Response(content=str(content), media_type="application/xml")

"""

@app.get("/fine_tune")
async def setup_fine_tune() -> str:
    if check_fine_tune_status():
        return "Fine tune setup"
    return "Max retries exceeded. Unable to retrieve the status."
"""

# For local testing without Twilio (optional endpoint)
@app.post("/test")
async def test_message(message: schemas.Message, db: Session = Depends(get_db)):
    content = generate_response(message.Body, message.Sender, db)
    print(content)
    # Return the response as XML
    return Response(content=str(content), media_type="application/xml")