from flask import Flask, request
import logging
import sys
from openai import OpenAI
import os

app = Flask(__name__)

# Disable buffering
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Set the OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Ensure the output directory exists
output_dir = "/app/output"
os.makedirs(output_dir, exist_ok=True)

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    received_message = data['message']
    app.logger.info(f"Received message: {received_message}")
    
    try:
        # Send request to OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": received_message
                }
            ]
        )
        response_message = completion.choices[0].message.content
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
