1. Setup API_KEY in .env file
    Replace your_api_key with your actual openai api_ key

2. Build and Run the Container: After making these changes, navigate to the root of your project directory and run:
    docker-compose up --build

3. Access your FastAPI application at http://127.0.0.1:8000 and swagger at http://127.0.0.1:8000/docs


4. Testing the application
--- 2 api endpoints are hosted here
    --- http://127.0.0.1:8000/whatsapp_response (use this to test from twilio)
    --- http://127.0.0.1:8000/test (use this to test from swagger)
--- use curl -X POST https://serveo.net -d 'localhost:8000' or ssh -R 80:localhost:8000 serveo.net to tunnel into port 8000 and http traffic will be redirected to another endpoint (for eg: https://a013a3e1dfa69bde357b38ad587fc630.serveo.net)


--- In your Twilio Console, go to the WhatsApp Sandbox settings and set the webhook URL to your server’s endpoint https://a013a3e1dfa69bde357b38ad587fc630.serveo.net
/whatsapp_response 

--- Open Chat in whatsapp with your twilio phone number. Conenct your whatsapp account to twilio sandbox using "join <sandbox name>". And send messages
