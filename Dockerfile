# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

# Copy the application code to the container
COPY agent_ai ./agent_ai

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["poetry", "run", "uvicorn", "agent_ai.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
