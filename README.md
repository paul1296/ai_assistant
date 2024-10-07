1. Setup API_KEY in .env file
    Replace your_api_key with your actual openai api_ key

2. Build and Run the Container: After making these changes, navigate to the root of your project directory and run:
    docker-compose up --build

3. Access your FastAPI application at http://127.0.0.1:8000 and swagger at http://127.0.0.1:8000/docs


4. Testing the application
--- 2 api endpoints are hosted here
    --- http://127.0.0.1:8000/whatsapp_response (use this to test from twilio)
    --- http://127.0.0.1:8000/test (use this to test from swagger)

--- In your Twilio Console, go to the WhatsApp Sandbox settings and set the webhook URL to your server’s endpoint http://127.0.0.1:8000/whatsapp_response 