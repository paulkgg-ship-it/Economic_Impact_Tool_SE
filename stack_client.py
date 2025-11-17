import requests
import os
from typing import Dict, Any
import json

class StackAIClient:
    def __init__(self):
        self.api_key = os.getenv('STACK_AI_API_KEY')
        flow_id_input = os.getenv('STACK_AI_FLOW_ID')
        self.base_url = "https://api.stack-ai.com/inference/v0/run"
        
        if not self.api_key or not flow_id_input:
            raise ValueError("Stack.ai credentials not found in environment variables")
        
        # Parse flow_id - it might be "org_id/flow_id" or just "flow_id"
        if '/' in flow_id_input:
            # Format: org_id/flow_id
            parts = flow_id_input.split('/', 1)
            self.org_id = parts[0]
            self.flow_id = parts[1]
        else:
            # Just flow_id - check for separate org_id env var
            self.org_id = os.getenv('STACK_AI_ORG_ID')
            self.flow_id = flow_id_input
            
            if not self.org_id:
                raise ValueError("STACK_AI_ORG_ID not found. Please provide either 'org_id/flow_id' in STACK_AI_FLOW_ID or set STACK_AI_ORG_ID separately.")
    
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
            # Make the API call with org_id and flow_id
            response = requests.post(
                f"{self.base_url}/{self.org_id}/{self.flow_id}",
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
