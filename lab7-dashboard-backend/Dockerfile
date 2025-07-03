# Use official Python image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

ENV IN_DOCKER=true

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]