# Gemini Agent AI Project

## Overview
The Gemini Agent project is designed to create an AI agent using the Litellm library and Google Studio AI Gemini. This project provides a structured approach to developing an intelligent agent capable of engaging in conversations and processing messages effectively.

## Project Structure
```
gemini-agent
├── src
│   ├── agent.py          # Main class for the AI agent
│   ├── config.py         # Configuration settings and loading
│   ├── utils             # Utility functions for parsing and prompts
│   │   ├── __init__.py
│   │   ├── parsing.py    # Functions for parsing messages
│   │   └── prompts.py     # Predefined prompts for the agent
│   ├── models            # Message model definitions
│   │   ├── __init__.py
│   │   └── message.py    # Message class definition
│   └── __init__.py
├── examples              # Example scripts demonstrating usage
│   ├── basic_chat.py     # Basic chat interaction example
│   └── advanced_agent.py  # Advanced features example
├── tests                 # Unit tests for the project
│   ├── __init__.py
│   ├── test_agent.py     # Tests for the Agent class
│   └── test_utils.py     # Tests for utility functions
├── .env.example          # Template for environment variables
├── requirements.txt      # Project dependencies
├── pyproject.toml        # Project configuration and metadata
└── README.md             # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd gemini-agent
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install UV if you don't have it yet:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. Install the required dependencies using UV:
   ```
   uv pip install -e .
   ```
   
   Or from requirements.txt:
   ```
   uv pip sync requirements.txt
   ```

## Usage
- To start a basic chat interaction, run:
  ```
  uv run -m src.examples.basic_chat 
  ```

- For advanced features, run:
  ```
  uv run -m src.examples.advanced_agent 
  ```

## Configuration
- Copy the `.env.example` file to `.env` and fill in the necessary environment variables, including API keys and model parameters.

## Testing
- To run the tests, use:
  ```
  python -m unittest discover -s tests
  ```
  
- Or with UV:
  ```
  uv pip install pytest
  uv run pytest
  ```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.