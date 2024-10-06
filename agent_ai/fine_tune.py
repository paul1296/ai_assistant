import docx
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key=os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

doc_file_path = "database/fine_tune.docx"

# Function to read the DOC file
def read_doc_file(doc_file_path):
    doc = docx.Document(doc_file_path)
    doc_content = []
    for paragraph in doc.paragraphs:
        doc_content.append(paragraph.text)
    return "\n".join(doc_content)

# Read the content of both files
doc_file_content = read_doc_file(doc_file_path)

def create_finetune_dataset(doc_content):
    dataset = []
    lines = doc_content.splitlines()

    question = ""
    response = []

    for line in lines:
        line = line.strip()  # Remove extra spaces

        if line.endswith("?"):  # This identifies a question
            if question and response:  # If we already have a pair, add it to the dataset
                dataset.append({
                    "prompt": f"User Query: {question}",
                    "completion": " ".join(response).strip()
                })
            # Reset for new question and response
            question = line
            response = []
        elif line:  # If it's a part of the response
            response.append(line)

    # Add the last question-response pair
    if question and response:
        dataset.append({
            "prompt": f"User Query: {question}",
            "completion": " ".join(response).strip()
        })

    return dataset


# Create dataset
finetune_dataset = create_finetune_dataset(doc_file_content)

# Save as JSONL for fine-tuning
with open('finetune_data.jsonl', 'w') as jsonl_file:
    for entry in finetune_dataset:
        jsonl_file.write(json.dumps(entry) + '\n')

# Upload the dataset
response = client.files.create(file=open('finetune_data.jsonl', 'rb'),
purpose='fine-tune')

file_id = response.id

fine_tune_response = openai.FineTune.create(
  training_file=fileid,  # Replace this with the file ID you got from the previous step
  model="davinci",  # You can replace this with other models like 'curie', 'babbage', etc.
)

fine_tune_id = fine_tune_response.id  # Get the fine-tuning job ID

# Function to check the fine-tuning status with exponential backoff
def check_fine_tune_status(fine_tune_id=fine_tune_id, max_retries=5):
    retries = 0
    wait_time = 1  # Initial wait time in seconds

    while retries < max_retries:
        try:
            status = client.fine_tunes.retrieve(fine_tune_id)
            print("Fine-tuning status:", status.status)

            if status.status in ['succeeded', 'failed']:
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

