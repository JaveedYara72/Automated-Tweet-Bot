import requests
import time

def send_error_notification(bot_token: str, chat_id: str, error_message: str, error_type: str = "Error") -> bool:
    """
    Sends an error notification to Telegram immediately.
    """
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    try:
        message_text = f"🚨 {error_type} Alert\n\n{error_message}\n\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        response = requests.post(f"{base_url}/sendMessage", json={
            "chat_id": chat_id,
            "text": message_text
        })
        
        return response.ok
    except Exception as e:
        print(f"Failed to send error notification: {e}")
        return False

def request_telegram_approval(bot_token: str, chat_id: str, tweet_text: str) -> bool:
    """
    Sends a message to Telegram with approval buttons and waits for a response.
    """
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    # Create inline keyboard
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Approve", "callback_data": "approve"},
            {"text": "❌ Deny", "callback_data": "deny"}
        ]]
    }
    
    try:
        # Send message with inline keyboard
        response = requests.post(f"{base_url}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"🤖 New tweet generated. Please approve:\n\n---\n{tweet_text}\n---",
            "reply_markup": keyboard
        })
        
        if not response.ok:
            print(f"Failed to send message: {response.text}")
            return False
            
        message_data = response.json()
        message_id = message_data["result"]["message_id"]
        print("Approval message sent. Waiting up to 5 minutes for a response...")
        
        update_id = None
        start_time = time.time()
        while time.time() - start_time < 300:  # 5 minute timeout
            # Get updates
            params = {"timeout": 10}
            if update_id:
                params["offset"] = update_id
                
            updates_response = requests.get(f"{base_url}/getUpdates", params=params)
            
            if not updates_response.ok:
                time.sleep(2)
                continue
                
            updates_data = updates_response.json()
            
            for update in updates_data.get("result", []):
                update_id = update["update_id"] + 1
                
                if "callback_query" in update:
                    callback = update["callback_query"]
                    if callback["message"]["message_id"] == message_id:
                        choice = callback["data"]
                        
                        if choice == "approve":
                            requests.post(f"{base_url}/editMessageText", json={
                                "chat_id": chat_id,
                                "message_id": message_id,
                                "text": "✅ Approved. Tweeting..."
                            })
                            return True
                        else:
                            requests.post(f"{base_url}/editMessageText", json={
                                "chat_id": chat_id,
                                "message_id": message_id,
                                "text": "❌ Denied. Tweet discarded."
                            })
                            return False
            time.sleep(2)
            
        # Timeout
        requests.post(f"{base_url}/editMessageText", json={
            "chat_id": chat_id,
            "message_id": message_id,
            "text": "⌛ Timed out. No action taken."
        })
        return False
    except Exception as e:
        print(f"An error occurred with Telegram: {e}")
        return False