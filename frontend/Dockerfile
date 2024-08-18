# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Streamlit and Requests
RUN pip install streamlit requests

# Make port 5173 available to the world outside this container
EXPOSE 5173

# Run Streamlit when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=5173", "--server.headless=true"]
