from flask import Flask, request
import logging
import sys

app = Flask(__name__)

# Disable buffering
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    received_message = data['message']
    app.logger.info(f"Received message: {received_message}")
    response_message = f"this is response: {received_message}"
    return {'response': response_message}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
