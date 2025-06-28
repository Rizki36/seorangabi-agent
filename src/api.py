from flask import Flask, request, jsonify
from src.agent_query import AgentQuery
from src.config import load_config
from functools import wraps
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("query_log.log"), logging.StreamHandler()]
)
logger = logging.getLogger("database-agent")

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
    agent = AgentQuery(config=config)
    response = agent.process_message(message)
    
    return jsonify({
        'status': 'success',
        'message': response
    })

@app.route('/query', methods=['POST'])
@token_required
def query_database():
    """Convert a natural language query to a database query"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
        
    query = data.get('query')
    
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Missing query'
        }), 400
    
    # Log the incoming query request
    logger.info(f"Database query request: {query}")
    
    # Create a temporary agent for this request
    agent = AgentQuery(config=config)
    result = agent.process_database_query(query)
    
    # Log the result for security audit
    if result.get('is_safe', False):
        logger.info(f"Generated safe query: {result.get('query')}")
    else:
        logger.warning(f"Rejected unsafe query. Reason: {result.get('reason')}")
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3021)