Setup Instructions
1. Configure OpenAI API Key

    Open the .env file in the root of your project.
    Replace the placeholder value your_api_key with your actual OpenAI API key:

    makefile

    API_KEY=your_actual_openai_api_key

2. Build and Run the Container

    Navigate to the root of your project directory.
    Run the following command to build and start the container:

    css

    docker-compose up --build

3. Access the Application

    Once the container is up and running, you can access the FastAPI application at:
        Application: http://127.0.0.1:8000
        Swagger UI (API documentation): http://127.0.0.1:8000/docs

4. Testing the Application

    There are two API endpoints available for testing:
        Twilio WhatsApp Response Endpoint: http://127.0.0.1:8000/whatsapp_response
        Swagger Test Endpoint: http://127.0.0.1:8000/test

    Tunneling for External Access:
        You can expose your local server to the internet using Serveo with the following command:

        bash

    curl -X POST https://serveo.net -d 'localhost:8000'

    or

    ruby

            ssh -R 80:localhost:8000 serveo.net

            This will redirect HTTP traffic to a public URL (e.g., https://a013a3e1dfa69bde357b38ad587fc630.serveo.net).

5. Setting up Twilio WhatsApp Webhook

    In your Twilio Console, go to the WhatsApp Sandbox Settings.
    Set the webhook URL to your Serveo endpoint:

    bash

    https://a013a3e1dfa69bde357b38ad587fc630.serveo.net/whatsapp_response

6. Testing via WhatsApp

    Open a chat with your Twilio phone number in WhatsApp.
    Join the sandbox by sending the message:

    bash

    join <sandbox_name>

    Once connected, you can start sending messages to test the integration.