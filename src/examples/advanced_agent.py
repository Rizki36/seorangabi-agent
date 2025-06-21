from src.agent import Agent
from src.config import load_config
from src.utils.prompts import PROMPTS

def main():
    # Load configuration settings
    config = load_config()

    # Initialize the AI agent
    agent = Agent(config)

    # Example of using a custom prompt
    custom_prompt = PROMPTS['custom_prompt']
    print("Using custom prompt:", custom_prompt)

    # Start a conversation thread
    conversation_id = agent.start_chat(custom_prompt)

    # Simulate sending and receiving messages
    user_message = "Hello, how can you assist me today?"
    response = agent.process_message(conversation_id, user_message)
    print("Agent response:", response)

    # Handle multiple conversation threads
    another_conversation_id = agent.start_chat(PROMPTS['another_prompt'])
    another_user_message = "Tell me about the weather."
    another_response = agent.process_message(another_conversation_id, another_user_message)
    print("Agent response to another conversation:", another_response)

if __name__ == "__main__":
    main()