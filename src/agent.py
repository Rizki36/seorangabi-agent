import litellm
from litellm import completion

class Agent:
    def __init__(self, config: dict):
        self.config = config
        self.litellm_client = self.initialize_litellm()
        self.history = []

    def initialize_litellm(self):
        """Initialize LiteLLM with the API key from config"""
        # Set the API key from config
        litellm.api_key = self.config.get("LLM_API_KEY")
        
        # You can also set other global LiteLLM settings here
        # litellm.set_verbose = True
        
        return litellm

    def start_chat(self):
        """Initialize a new chat session"""
        self.history = []
        return "Chat session started. How can I help you today?"

    def process_message(self, message):
        """Process a user message and return AI response"""
        # Add user message to history
        self.history.append({"role": "user", "content": message})
        
        # Get response from LLM
        response = self.send_message(self.history)
        
        # Add response to history
        self.history.append({"role": "assistant", "content": response})
        
        return response

    def send_message(self, messages):
        """Send message to LiteLLM and get response"""
        try:
            response = completion(
                model=self.config.get("MODEL_NAME", "gpt-3.5-turbo"),
                messages=messages,
                timeout=self.config.get("TIMEOUT", 30)
            )
            
            # Extract the content from the response
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            return "Sorry, I couldn't generate a response."
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return f"Sorry, there was an error: {str(e)}"

    def receive_message(self):
        """Get the last message from chat history"""
        if self.history and len(self.history) > 0:
            last_message = self.history[-1]
            return last_message.get("content", "No messages yet.")
        return "No messages in history."