from src.agent import Agent
from src.config import load_config

def main():
    # Load configuration from config.py
    config = load_config()
    
    # Initialize the AI agent with the loaded config
    agent = Agent(config=config)

    print("Welcome to the AI Chat! Type 'exit' to end the chat.")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Ending chat. Goodbye!")
            break
        
        # Process the message and get a response
        response = agent.process_message(user_input)
        
        # Display the response
        print(f"AI: {response}")

if __name__ == "__main__":
    main()