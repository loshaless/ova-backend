# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /code

# Copy requirements.txt and install dependencies (for caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY ./src /code

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "5"]
