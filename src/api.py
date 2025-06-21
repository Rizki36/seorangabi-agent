from flask import Flask, request, jsonify
from src.agent import Agent
from src.config import load_config
from functools import wraps
import uuid

app = Flask(__name__)

# Store active agent sessions
sessions = {}

# Load configuration with API token
config = load_config()
CHAT_API_KEY = config.get('CHAT_API_KEY', 'your-default-secret-token')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        # If no token or invalid token
        if not token or token != CHAT_API_KEY:
            return jsonify({
                'status': 'error',
                'message': 'Invalid or missing authentication token'
            }), 401
            
        return f(*args, **kwargs)
    return decorated

@app.route('/chat/new', methods=['POST'])
@token_required
def new_chat():
    """Create a new chat session with the agent"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = Agent(config=config)
    
    return jsonify({
        'status': 'success',
        'message': 'New chat session created',
        'session_id': session_id
    })

@app.route('/chat/message', methods=['POST'])
@token_required
def process_message():
    """Process a message with the agent"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
        
    session_id = data.get('session_id')
    message = data.get('message')
    
    if not session_id or not message:
        return jsonify({
            'status': 'error',
            'message': 'Missing session_id or message'
        }), 400
        
    if session_id not in sessions:
        return jsonify({
            'status': 'error',
            'message': 'Invalid session ID'
        }), 404
    
    # Process the message with the agent
    agent = sessions[session_id]
    response = agent.process_message(message)
    
    return jsonify({
        'status': 'success',
        'message': response
    })
    
@app.route('/chat/history/<session_id>', methods=['GET'])
@token_required
def get_history(session_id):
    """Get chat history for a session"""
    if session_id not in sessions:
        return jsonify({
            'status': 'error',
            'message': 'Invalid session ID'
        }), 404
        
    agent = sessions[session_id]
    
    return jsonify({
        'status': 'success',
        'history': agent.history
    })

@app.route('/ask', methods=['POST'])
@token_required
def ask():
    """Ask a question to the agent without creating a session"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
        
    message = data.get('message')
    
    if not message:
        return jsonify({
            'status': 'error',
            'message': 'Missing message'
        }), 400
    
    # Create a temporary agent for this request
    agent = Agent(config=config)
    response = agent.process_message(message)
    
    return jsonify({
        'status': 'success',
        'message': response
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3021)