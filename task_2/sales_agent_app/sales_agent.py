import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# AI Sales Agent function


def ai_sales_agent(user_input, chat_history):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a highly professional AI Sales Agent. Your role is to:
    - Answer product inquiries concisely.
    - Recommend suitable products from the product catalog.
    - Guide customers through the buying process.
    - Provide basic customer support for orders and returns.

    Here is the conversation history:
    {chat_history}

    Customer: {user_input}
    AI Sales Agent:
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except genai.errors.APIError as e:
        return "⚠️ Sorry, I encountered an API error. Please try again later."
    except Exception as e:
        return f"⚠️ Sorry, I encountered an error: {e}"
