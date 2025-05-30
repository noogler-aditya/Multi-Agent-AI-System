from google.generativeai import GenerativeModel
import google.generativeai as genai

def call_llm(prompt, model="gemini-1.5-flash"):
    try:
        # Configure the API key - make sure to set this in your environment
        genai.configure(api_key='YOUR_API_KEY')
        
        # Initialize the model
        model = GenerativeModel('gemini-1.5-flash')
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Return the text response, stripped of whitespace
        return response.text.strip()
    except Exception as e:
        print("Gemini LLM call failed:", e)
        return "Other"
