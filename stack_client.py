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
            raise ValueError(
                "Stack.ai credentials not found in environment variables")

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
                raise ValueError(
                    "STACK_AI_ORG_ID not found. Please provide either 'org_id/flow_id' in STACK_AI_FLOW_ID or set STACK_AI_ORG_ID separately."
                )

    def run_analysis(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends form data to Stack.ai and returns the economic impact report
        """
        # Get condensed context from data processor (includes fiscal_parameters, multipliers, etc.)
        from data_processor import data_processor
        llm_context = data_processor.prepare_llm_context(form_data)

        # DEBUG: Log what we're sending
        print("=" * 60)
        print("CONTEXT BEING SENT TO STACK.AI:")
        print(json.dumps(llm_context, indent=2)[:2000])
        print("=" * 60)

        # Check if fiscal_parameters exists
        if 'fiscal_parameters' in llm_context:
            print("✓ fiscal_parameters IS included")
            print(f"  City Millage: {llm_context['fiscal_parameters'].get('city_millage')}")
            print(f"  County Millage: {llm_context['fiscal_parameters'].get('county_millage')}")
        else:
            print("✗ fiscal_parameters is MISSING!")
        print("=" * 60)

        # Prepare the payload with enriched context
        payload = {
            "in-0": json.dumps(llm_context),
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

            # Extract the output - Stack.ai returns outputs in 'outputs' dict
            outputs = result.get('outputs', {})
            output_text = outputs.get('out-0', '')

            # If output is JSON, try to parse and format it
            report_json = None
            if output_text:
                try:
                    output_data = json.loads(output_text)
                    # Store the JSON data for structured display
                    report_json = output_data
                    
                    # If it's a dict with HTML fields, combine them for text display
                    if isinstance(output_data, dict):
                        report_sections = []
                        if output_data.get('executive_summary_html'):
                            report_sections.append(
                                output_data['executive_summary_html'])
                        if output_data.get('tables_html'):
                            report_sections.append(output_data['tables_html'])
                        if output_data.get('why_this_matters_html'):
                            report_sections.append(
                                output_data['why_this_matters_html'])
                        if output_data.get('sources_html'):
                            report_sections.append(output_data['sources_html'])

                        if report_sections:
                            output_text = '\n\n'.join(report_sections)
                        else:
                            # If all sections are empty, keep the JSON string
                            output_text = json.dumps(output_data, indent=2)
                except json.JSONDecodeError:
                    # Not JSON, use as-is
                    pass

            return {
                'success': True,
                'report': output_text if output_text else
                'Report generated but no content was returned from the AI model.',
                'report_json': report_json,  # Add the structured JSON data
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
