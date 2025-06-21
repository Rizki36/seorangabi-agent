def load_config():
    import os
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from a .env file if it exists

    config = {
        "LLM_API_KEY": os.getenv("LLM_API_KEY"),
        "MODEL_NAME": os.getenv("MODEL_NAME", "default_model"),
        "TIMEOUT": int(os.getenv("TIMEOUT", 30)),
        "CHAT_API_KEY": os.getenv("CHAT_API_KEY"),
    }

    return config