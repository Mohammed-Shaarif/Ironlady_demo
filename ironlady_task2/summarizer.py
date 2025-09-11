import requests
import json

class OllamaSummarizer:
    def __init__(self, base_url="http://localhost:11434", model="codellama:latest"):
        self.base_url = base_url
        self.model = model
    
    def check_ollama_status(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=120)
            return response.status_code == 200
        except:
            return False
    
    def summarize_content(self, content, max_length=200):
        """Summarize course content using Ollama"""
        # Check if Ollama is running
        if not self.check_ollama_status():
            return "Error: Ollama server is not running. Please start Ollama with 'ollama serve' command."
        
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = f"""
            Please provide a concise summary of the following course content in {max_length} words or less:
            
            {content}
            
            Summary:
            """
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated').strip()
            else:
                return f"Error: Ollama returned status {response.status_code}. Response: {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure it's running on http://localhost:11434"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be taking too long to respond."
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {str(e)}"
        except Exception as e:
            return f"Error: Unexpected error - {str(e)}"
    
    def generate_course_outline(self, title, description):
        """Generate a course outline based on title and description"""
        # Check if Ollama is running
        if not self.check_ollama_status():
            return "Error: Ollama server is not running. Please start Ollama with 'ollama serve' command."
            
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = f"""
            Create a detailed course outline for the following course:
            
            Title: {title}
            Description: {description}
            
            Please provide:
            1. Learning objectives (3-5 points)
            2. Course modules/chapters (5-8 modules)
            3. Key topics covered
            4. Prerequisites (if any)
            
            Course Outline:
            """
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No outline generated').strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
