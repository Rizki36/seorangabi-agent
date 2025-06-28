import litellm
import re
from litellm import completion
from typing import Dict, Any
from src.utils.prompts import PROMPTS

class AgentQuery:
    def __init__(self, config: dict):
        self.config = config
        self.litellm_client = self.initialize_litellm()
        self.history = []
        self.query_safety_rules = self._initialize_safety_rules()

    def initialize_litellm(self):
        """Initialize LiteLLM with the API key from config"""
        # Set the API key from config
        litellm.api_key = self.config.get("LLM_API_KEY")
        
        # You can also set other global LiteLLM settings here
        litellm.set_verbose = True
        
        return litellm
    
    def _initialize_safety_rules(self) -> Dict:
        """Initialize safety rules for database queries"""
        return {
            "allowed_operations": ["SELECT", "FIND", "FINDMANY", "GET", "FINDUNIQUE", "FINDMANY", "COUNT", "AGGREGATE", "GROUPBY", "QUERY"],
            "forbidden_operations": ["INSERT", "CREATE", "UPDATE", "DELETE", "UPSERT", "UPDATEONE", "UPDATEMANY", "DELETEONE", "DELETEMANY", "EXECUTE", "SQL", "DROP"],
            "sensitive_fields": [],
            # "require_filters": ["User", "Team", "Project"],
            # "log_all_queries": True
        }
    
    def validate_query(self, query_text: str) -> Dict[str, Any]:
        """Validate if a query is safe according to our rules"""
        query_text = query_text.strip()
        
        # Check for forbidden operations
        for forbidden_op in self.query_safety_rules["forbidden_operations"]:
            pattern = rf'\b{forbidden_op}\b'
            if re.search(pattern, query_text, re.IGNORECASE):
                return {
                    "is_safe": False,
                    "reason": f"Forbidden operation detected: {forbidden_op}",
                    "query": query_text
                }
        
        # Check if query contains at least one allowed operation
        allowed_found = False
        for allowed_op in self.query_safety_rules["allowed_operations"]:
            pattern = rf'\b{allowed_op}\b'
            if re.search(pattern, query_text, re.IGNORECASE):
                allowed_found = True
                break
        
        if not allowed_found:
            return {
                "is_safe": False,
                "reason": "Query must use at least one allowed operation",
                "query": query_text
            }
            
        # Add more checks as needed
        
        return {
            "is_safe": True,
            "query": query_text
        }
    
    def process_database_query(self, user_query: str) -> Dict[str, Any]:
        """Process a natural language query and convert it to a safe database query"""
        # First, add this to the history
        self.history.append({"role": "user", "content": user_query})
        
        # Use LLM to generate a prisma query from natural language
        system_prompt = PROMPTS.get("system_prompt", "")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Convert this question to a safe Prisma query: {user_query}"}
        ]
        
        try:
            response = completion(
                model=self.config.get("MODEL_NAME", "gpt-3.5-turbo"),
                messages=messages,
                temperature=0.4,  # Low temperature for more deterministic outputs
                timeout=self.config.get("TIMEOUT", 30),
                # thinking={"type": "enabled", "budget_tokens": 1024},
            )
            
            generated_query = response.choices[0].message.content
            
            # Validate the generated query
            validation_result = self.validate_query(generated_query)
            
            if validation_result['is_safe']:
                self.history.append({"role": "assistant", "content": generated_query})
                return {
                    "status": "success",
                    "query": generated_query,
                    "is_safe": True
                }
            else:
                # If unsafe, return the validation error
                self.history.append({
                    "role": "assistant", 
                    "content": f"I cannot generate that query because: {validation_result['reason']}"
                })
                return {
                    "status": "error",
                    "reason": validation_result["reason"],
                    "is_safe": False
                }
                
        except Exception as e:
            error_msg = f"Error generating database query: {str(e)}"
            self.history.append({"role": "assistant", "content": error_msg})
            return {
                "status": "error",
                "reason": error_msg,
                "is_safe": False
            }

    def process_message(self, message: str) -> str:
        """Process a user message and return AI response"""
        # Add user message to history
        self.history.append({"role": "user", "content": message})
        
        # Get response from LLM
        try:
            response = completion(
                model=self.config.get("MODEL_NAME", "gemini-pro"),
                messages=self.history,
                timeout=self.config.get("TIMEOUT", 30)
            )
            
            # Extract the content from the response
            if response and response.choices and len(response.choices) > 0:
                reply = response.choices[0].message.content
                # Add response to history
                self.history.append({"role": "assistant", "content": reply})
                return reply
            return "Sorry, I couldn't generate a response."
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return f"Sorry, there was an error: {str(e)}"