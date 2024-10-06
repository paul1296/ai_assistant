from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from gpt import generate_response
from fine_tune import check_fine_tune_status

# Initialize FastAPI app
app = FastAPI()

if check_fine_tune_status():
    # Generate Response to twilio request
    @app.post("/whatsapp_response")
    async def whatsapp_response(request: Request):
        twilio_body = await request.json()
        message = body['Body']
        sender = twilio_body['From']
        incoming_msg = request.values.get('Body', '').strip()
        # Generate prompt response
        content = generate_response(incoming_message)

        return JSONResponse(content=content, media_type="application/xml")

else:
    raise Exception("Fine tune failed. The server will not start.")
