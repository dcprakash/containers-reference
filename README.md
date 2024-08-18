
# Dockerized Frontend-Backend Application with OpenAI Integration

This repository contains a simple two-app setup using Docker. It consists of a frontend application built with Streamlit and a backend application built with Flask. The frontend app allows users to input a message, which is sent to the backend. The backend processes this message using the OpenAI API to generate a response, which is then displayed back to the user on the frontend.

## Project Structure
```
.
├── backend/
│   ├── app.py             # Flask application that communicates with OpenAI
│   └── Dockerfile         # Dockerfile for building the backend container
├── frontend/
│   ├── app.py             # Streamlit application that interacts with the backend
│   └── Dockerfile         # Dockerfile for building the frontend container
└── docker-compose.yml     # Docker Compose file to run both containers together
```

### Backend Application

The backend is a Flask application that listens for POST requests from the frontend. It forwards the received message to the OpenAI API and returns the generated response to the frontend. Additionally, it writes the user message and AI response to a file on the host machine using Docker volume mounting.

### Frontend Application

The frontend is a Streamlit application that provides a simple UI for users to input a message. This message is sent to the backend, and the response from the backend is displayed to the user.

## Prerequisites

- Docker installed on your local machine
- An OpenAI API key

## Setting Up and Running the Application

### Step 1: Set the OpenAI API Key

Before running the application, you need to set the `OPENAI_API_KEY` environment variable on your local machine. This key will be passed into the backend container when it runs.

#### On Linux/MacOS:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

#### On Windows (Powershell):
```bash
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

### Step 2: Modify the docker-compose.yml to Add a Volume Mount

In the `docker-compose.yml` file, add a volume to the backend service that maps a directory on the host machine to a directory inside the container.

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY
    volumes:
      - ./output:/app/output  # Mounts the ./output directory on the host to /app/output in the container
  
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

### Step 3: Modify the Backend Application to Write to a File

Update the backend application (`backend/app.py`) to write the response from OpenAI into a text file inside the mounted directory.

```python
from flask import Flask, request
import logging
import sys
import openai
import os

app = Flask(__name__)

# Disable buffering
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Set the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the output directory exists
output_dir = "/app/output"
os.makedirs(output_dir, exist_ok=True)

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    received_message = data['message']
    app.logger.info(f"Received message: {received_message}")
    
    try:
        # Send request to OpenAI using the updated API interface
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": received_message}
            ]
        )
        response_message = completion['choices'][0]['message']['content']
        app.logger.info(f"OpenAI response: {response_message}")
        
        # Write the response to a file
        with open(os.path.join(output_dir, "response.txt"), "a") as f:
            f.write(f"User message: {received_message}\n")
            f.write(f"AI response: {response_message}\n")
            f.write("-" * 50 + "\n")
        
        return {'response': response_message}, 200
    except Exception as e:
        app.logger.error(f"Error communicating with OpenAI: {e}")
        return {'error': 'Failed to get response from OpenAI'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

### Step 4: Run the Application Using Docker Compose

To start the application, navigate to the root directory of the project where the `docker-compose.yml` file is located and run:

```bash
docker-compose up --build
```

This command will:

- Build and run the backend service (Flask app) on port 8080.
- Build and run the frontend service (Streamlit app) on port 5173.

### Step 5: Access the Application

Once the containers are up and running, open your web browser and go to:

[http://localhost:5173](http://localhost:5173)

You should see the frontend application where you can enter a message and receive a response generated by OpenAI. The response will also be logged to a file named `response.txt` in the `output` directory on your host machine.

### Stopping the Application

To stop the running containers, use `Ctrl+C` in the terminal where `docker-compose up` is running. You can also stop and remove the containers with:

```bash
docker-compose down
```

### Explanation of Volume Mounting

- **Volume Mounting:** The `volumes` section in the `docker-compose.yml` file mounts the `./output` directory on your host to the `/app/output` directory inside the container. This allows the container to write files directly to your host machine.

- **Directory Creation:** The backend code ensures that the `/app/output` directory exists before trying to write files to it.

- **File Writing:** The backend writes the user message and the AI response to `response.txt`. Each interaction is appended to the file with a separator line ("-" * 50) to distinguish between different requests.

This setup ensures that all responses are logged to a file on your host machine, which can be useful for auditing, debugging, or further analysis.
