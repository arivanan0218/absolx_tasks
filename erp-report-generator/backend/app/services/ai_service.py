import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google API key not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_report(self, metrics):
        """Generate a natural language report using Gemini AI"""
        
        prompt = f"""
        As a business intelligence expert, generate a clear, concise ERP report based on the following business metrics:

        {json.dumps(metrics, indent=2)}

        The report should include:
        1. A summary of overall performance
        2. Month-over-month comparison (if available)
        3. Insights about top-selling products
        4. Inventory warnings for products that are low or out of stock (if available)
        5. Regional performance highlights (if available)
        6. Category insights (if available)
        
        Important:
        - Use LKR as the currency symbol instead of $ (e.g., "LKR 5,000" not "$5,000")
        - All monetary values should be presented in Sri Lankan Rupees (LKR)

        Keep the report professional, factual, and data-driven. Use specific numbers but round percentages to one decimal place.
        Format the report with appropriate sections and summaries. Keep it concise but comprehensive.

        Important formatting guidelines:
        - Use clean section headers without any special formatting characters
        - Do not use asterisks (**) for emphasis; instead use clear, direct language
        - Separate sections with line breaks for readability
        """
        
        response = self.model.generate_content(prompt)
        return response.text