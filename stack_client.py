import requests
import os
from typing import Dict, Any
import json

class StackAIClient:
    def __init__(self):
        self.api_key = os.getenv('STACK_AI_API_KEY')
        self.flow_id = os.getenv('STACK_AI_FLOW_ID')
        self.base_url = "https://www.stack-ai.com/inference/v0/run"
        
        if not self.api_key or not self.flow_id:
            raise ValueError("Stack.ai credentials not found in environment variables")
    
    def run_analysis(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends form data to Stack.ai and returns the economic impact report
        """
        # Prepare the payload
        payload = {
            "in-0": json.dumps(form_data),  # Send all form data as JSON string
            "user_id": f"economic-impact-{form_data.get('project_name', 'unknown')}"
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API call
            response = requests.post(
                f"{self.base_url}/{self.flow_id}",
                headers=headers,
                json=payload,
                timeout=120  # 2 minute timeout for LLM processing
            )
            
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            return {
                'success': True,
                'report': result.get('out-0', ''),  # The LLM output
                'raw_response': result
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timed out. Please try again.',
                'report': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'API Error: {str(e)}',
                'report': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'report': None
            }

# Create client instance
def get_stack_client():
    """
    Returns a StackAI client instance if credentials are available,
    otherwise returns None
    """
    try:
        return StackAIClient()
    except ValueError:
        return None
