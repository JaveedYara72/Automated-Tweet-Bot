import os
import anthropic
from telegram_handler import send_error_notification

# List of Claude models to try in order (newest to oldest)
CLAUDE_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620", 
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]

def get_claude_response(prompt_text: str, api_key: str = None, temperature: float = 0.7, telegram_bot_token: str = None, telegram_chat_id: str = None) -> str:
    """
    Sends a prompt to the Claude API and returns the response.

    Args:
        prompt_text (str): The prompt to send to Claude.
        api_key (str, optional): Your Anthropic API key. If not provided,
                                 it will try to use the ANTHROPIC_API_KEY
                                 environment variable. Defaults to None.
        temperature (float): The temperature for the generation (0.0 to 1.0).

    Returns:
        str: Claude's response text, or an empty string if an error occurs.
    """
    try:
        # Use the provided API key if it exists, otherwise try the environment variable
        if api_key:
            client = anthropic.Anthropic(api_key=api_key)
        else:
            client = anthropic.Anthropic() # Looks for ANTHROPIC_API_KEY
    except Exception as e:
        print(f"Error initializing Anthropic client: {e}")
        print("Please provide an api_key or set the ANTHROPIC_API_KEY environment variable.")
        return ""

    # Try each model in order until one works
    last_error = None
    
    for model in CLAUDE_MODELS:
        try:
            print(f"Trying Claude model: {model}...")
            
            # Make the API call
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ]
            )

            # Extract and return the response text
            response_text = message.content[0].text
            print(f"Successfully used model: {model}")
            return response_text

        except anthropic.APIError as e:
            last_error = e
            error_str = str(e)
            
            # If model not found (404), try next model
            if "not_found_error" in error_str or "404" in error_str:
                print(f"Model {model} not found, trying next model...")
                continue
            
            # For other API errors, send notification and break
            elif "rate_limit" in error_str.lower():
                error_msg = f"Claude API Rate Limit Exceeded\nModel: {model}\nError: {e}"
                if telegram_bot_token and telegram_chat_id:
                    send_error_notification(telegram_bot_token, telegram_chat_id, error_msg, "Rate Limit")
                print(f"Rate limit error: {e}")
                break
            elif "insufficient_quota" in error_str.lower() or "quota" in error_str.lower():
                error_msg = f"Claude API Quota Exceeded\nModel: {model}\nError: {e}"
                if telegram_bot_token and telegram_chat_id:
                    send_error_notification(telegram_bot_token, telegram_chat_id, error_msg, "Quota Exceeded")
                print(f"Quota exceeded: {e}")
                break
            else:
                error_msg = f"Claude API Error\nModel: {model}\nError: {e}"
                if telegram_bot_token and telegram_chat_id:
                    send_error_notification(telegram_bot_token, telegram_chat_id, error_msg, "API Error")
                print(f"API error: {e}")
                break
                
        except Exception as e:
            last_error = e
            error_msg = f"Unexpected Claude Error\nModel: {model}\nError: {e}"
            if telegram_bot_token and telegram_chat_id:
                send_error_notification(telegram_bot_token, telegram_chat_id, error_msg, "Unexpected Error")
            print(f"Unexpected error with model {model}: {e}")
            continue
    
    # If all models failed, send final error notification
    if telegram_bot_token and telegram_chat_id:
        send_error_notification(telegram_bot_token, telegram_chat_id, 
                              f"All Claude models failed. Last error: {last_error}", 
                              "Critical Error")
    
    print(f"All Claude models failed. Last error: {last_error}")
    return ""

