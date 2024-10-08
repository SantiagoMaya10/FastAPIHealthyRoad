# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install system dependencies required by some libraries (e.g. OpenCV)
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*  # Clean up the APT cache to reduce image size

# Install the necessary packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port on which your app will run
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]