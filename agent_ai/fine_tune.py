import docx
import json
import os
import openai
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()
"""
# Set API key for OpenAI client
api_key = os.getenv("API_KEY")
openai.api_key = api_key

# Upload the dataset file
response = openai.File.create(file=open('agent_ai/fine_tune_data.jsonl', 'rb'), purpose='fine-tune')
file_id = response.id

# Start fine-tuning the model using the new fine-tuning method

fine_tune_response = openai.FineTuningJob.create(
    training_file=file_id,  # The file ID from the upload step containing training data
    model="gpt-3.5-turbo"     # Updated model for fine-tuning (e.g., GPT-4 Turbo)
)

fine_tune_id = fine_tune_response['id']  # Get the fine-tuning job ID


# Function to check the fine-tuning status with exponential backoff
def check_fine_tune_status(fine_tune_id=fine_tune_id, max_retries=12):
    retries = 0
    wait_time = 1  # Initial wait time in seconds

    while retries < max_retries:
        try:
            status = openai.FineTuningJob.retrieve(fine_tune_id)

            if status['status'] in ['succeeded', 'failed']:
                return True  # Exit the loop if the job is complete or failed

            # Wait for a bit before the next check
            time.sleep(wait_time)
            retries += 1
            wait_time *= 2  # Double the wait time for the next attempt

        except Exception as e:
            print(f"Error retrieving status: {e}")
            time.sleep(wait_time)  # Wait before retrying
            retries += 1
            wait_time *= 2  # Double the wait time for the next attempt

    print("Max retries exceeded. Unable to retrieve the status.")
    return False


doc_file_path = "agent_ai/database/fine_tune.docx"

# Function to read the DOCX file
def read_doc_file(doc_file_path):
    doc = docx.Document(doc_file_path)
    doc_content = []
    for paragraph in doc.paragraphs:
        doc_content.append(paragraph.text)
    return "\n".join(doc_content)

# Read the content of the DOCX file
doc_file_content = read_doc_file(doc_file_path)

def create_finetune_dataset(doc_content):
    dataset = []
    lines = doc_content.splitlines()

    question = ""
    response = []

    for line in lines:
        line = line.strip()

        if line.endswith("?"):  # This identifies a question
            if question and response:
                dataset.append({
                    "messages": [
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": " ".join(response).strip()}
                    ]
                })
            question = line
            response = []
        elif line:  # If it's a part of the response
            response.append(line)

    # Add the last question-response pair
    if question and response:
        dataset.append({
            "messages": [
                {"role": "user", "content": question},
                {"role": "assistant", "content": " ".join(response).strip()}
            ]
        })

    return dataset


# Create dataset
finetune_dataset = create_finetune_dataset(doc_file_content)

# Save as JSONL for fine-tuning
with open('finetune_data.jsonl', 'w') as jsonl_file:
    for entry in finetune_dataset:
        jsonl_file.write(json.dumps(entry) + '\n')


"""