# How are we scraping the tweets??
# Go to this video, signup using the link in the description, you will get 100000 credits.
# Each call takes 300 credits. 
# https://www.youtube.com/watch?v=lEo7IAgj0UY&t=353s
# The API Key used here, will be found in the personal dashboard there.
# For more info, click on this link -> https://docs.twitterapi.io/introduction

# Q1. How to get the community id?
# 1. Get the community id for the community you want to scrape.
# 2. Go to the community tab on twitter and click on the community you want to scrape.
# 3. Copy the community id from the URL.

import requests
import pandas as pd
import os
import time

# Import all our helper functions
from tuple_maker import format_tweets_for_prompt
from llm_caller import get_claude_response
from telegram_handler import request_telegram_approval, send_error_notification
from tweepy_post_function import post_tweet

# --- Configuration ---
MAX_TWEETS = 50
OUTPUT_FILENAME = ""
COMMUNITY_ID = ""

# --- Load All Required API Keys from Environment Variables ---
# This section checks for all necessary keys at the start of the script.
# If any are missing, the script will exit immediately.

# Your API key from twitterapi.io
# It's best practice to load this from an environment variable for security.
TWITTER_SCRAPE_API_KEY = os.environ.get("TWITTERAPI_IO_KEY","")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY","")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN","8")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID","")
TWEEPY_API_KEY = os.environ.get("TWEEPY_API_KEY","")
TWEEPY_API_SECRET = os.environ.get("TWEEPY_API_SECRET","")
TWEEPY_ACCESS_TOKEN = os.environ.get("TWEEPY_ACCESS_TOKEN","")
TWEEPY_ACCESS_SECRET = os.environ.get("TWEEPY_ACCESS_SECRET","")

# Check if all keys are present
if not all([TWITTER_SCRAPE_API_KEY, CLAUDE_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TWEEPY_API_KEY, TWEEPY_API_SECRET, TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_SECRET]):
    raise ValueError("One or more required environment variables are not set. Please check your GitHub Secrets.")

# Whatsapp Texts
whatsapp_t1 = """T"""

whatsapp_t2 = """"""

whatsapp_t3 = """S"""

# Twitter tweets
twitter_t1 = """"""

twitter_t2 = """"""

twitter_t3 = """"""

# Prompt Text
PROMPT_TEXT = """
    You are an expert social media strategist and ghostwriter specializing in engaging technical communities on Twitter/X. Your goal is to write a viral tweet for me.
    1. My Writing Style (Persona to Adopt): First, understand my voice. I am knowledgeable but also witty and a bit sarcastic. Here are two paragraphs that show exactly how I talk:

    Here are my whatsapp texts: This is how i passionately or sometimes sarcastically talk to my friends.

    {whatsapp_t1}
    {whatsapp_t2}
    {whatsapp_t3}

    Here are my twitter tweets: This is how my persona is on twitter

    {twitter_t1}
    {twitter_t2}
    {twitter_t3}

    2. Current Community Conversation (Context): Next, analyze these recent, popular tweets from the Rust programming community to understand the current topics and mood. This is what people are talking about right now:

    {formatted_tweets_string}

    3. Your Mission (The Task): Based on the context of the community conversation and my personal writing style, generate a single, original tweet that is likely to get high interaction (likes, replies, retweets).

    4. Rules:
    a. Match My Voice: The tweet's tone must perfectly match my writing style.
    b. Be Relevant: The topic must relate to the ongoing community conversation.
    c. Be Engaging: The tweet should be interesting, ask a question, or state a sharp, insightful opinion.
    d. Output Only the Tweet: Your entire response must be ONLY the text of the tweet and nothing else. Do not add explanations, quotation marks, or any other text.
    e. The tweet should not look like its been written by a bot without em dashes, and other twitter specific things. And should be a bit more engaging.
"""


# API endpoint and parameters
url = "https://api.twitterapi.io/twitter/community/tweets"
headers = {"X-API-Key": TWITTER_SCRAPE_API_KEY}
querystring = {"community_id":f"{COMMUNITY_ID}"}


def run_bot():
    """Main function to run the entire tweet generation and posting process."""
    
    try:
        # === Step 1: Scrape Tweets ===
        all_tweets_data = []
        next_cursor = None
        url = "https://api.twitterapi.io/twitter/community/tweets"
        headers = {"X-API-Key": TWITTER_SCRAPE_API_KEY}
        
        print(f"🚀 Starting to fetch up to {MAX_TWEETS} tweets...")
        
        scraping_attempts = 0
        max_scraping_attempts = 3
        
        while len(all_tweets_data) < MAX_TWEETS and scraping_attempts < max_scraping_attempts:
            params = {"community_id": COMMUNITY_ID}
            if next_cursor:
                params["cursor"] = next_cursor
            
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                tweets_on_page = data.get('tweets', [])
                
                if not tweets_on_page: 
                    print("No more tweets found")
                    break
                
                for tweet in tweets_on_page:
                    all_tweets_data.append({
                        "username": tweet.get("author", {}).get("userName"),
                        "created_at": tweet.get("createdAt"),
                        "text": tweet.get("text"),
                        "like_count": tweet.get("likeCount", 0),
                        "retweet_count": tweet.get("retweetCount", 0),
                        "reply_count": tweet.get("replyCount", 0),
                        "view_count": tweet.get("viewCount", 0),
                        "tweet_url": tweet.get("url")
                    })
                
                next_cursor = data.get("next_cursor")
                if not data.get("has_next"): break
                time.sleep(1)
                
            except requests.exceptions.HTTPError as e:
                scraping_attempts += 1
                if e.response.status_code == 429:  # Rate limit
                    error_msg = f"Twitter API Rate Limit Hit\nAttempt {scraping_attempts}/{max_scraping_attempts}\nWaiting 60 seconds..."
                    send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Rate Limit")
                    time.sleep(60)
                    continue
                elif e.response.status_code == 401:  # Unauthorized
                    error_msg = f"Twitter API Unauthorized - Invalid API Key\nCheck TWITTERAPI_IO_KEY\nError: {e}"
                    send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Auth Error")
                    return
                else:
                    error_msg = f"Twitter API HTTP Error\nStatus: {e.response.status_code}\nError: {e}"
                    send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "HTTP Error")
                    break
            except Exception as e:
                scraping_attempts += 1
                error_msg = f"Twitter Scraping Error\nAttempt {scraping_attempts}/{max_scraping_attempts}\nError: {e}"
                send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Scraping Error")
                if scraping_attempts >= max_scraping_attempts:
                    break
                time.sleep(10)  # Wait before retry
        
        if not all_tweets_data:
            error_msg = "No tweets scraped after all attempts. Check community ID and API key."
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Scraping Failed")
            print("No tweets scraped. Exiting.")
            return

        # === Step 1.5: Save Scraped Data ===
        try:
            df = pd.DataFrame(all_tweets_data)
            df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
            print(f"✅ Scraped {len(df)} tweets and saved to {OUTPUT_FILENAME}")
        except Exception as e:
            error_msg = f"Failed to save scraped tweets to CSV\nFile: {OUTPUT_FILENAME}\nError: {e}"
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "File Error")
            return

        # === Step 2: Format Data and Create Prompt ===
        try:
            formatted_tweets = format_tweets_for_prompt(OUTPUT_FILENAME)
            if not formatted_tweets:
                error_msg = "Failed to format tweets for prompt - empty result"
                send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Data Processing Error")
                return
                
            final_prompt = PROMPT_TEXT.format(
                whatsapp_t1=whatsapp_t1, whatsapp_t2=whatsapp_t2, whatsapp_t3=whatsapp_t3,
                twitter_t1=twitter_t1, twitter_t2=twitter_t2, twitter_t3=twitter_t3,
                formatted_tweets_string=formatted_tweets
            )
        except Exception as e:
            error_msg = f"Failed to format tweets or create prompt\nError: {e}"
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Prompt Error")
            return

        # === Step 3: Generate Tweet with Claude ===
        generated_tweet = get_claude_response(final_prompt, CLAUDE_API_KEY, 0.7, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

        if not generated_tweet:
            error_msg = "Claude failed to generate tweet after trying all models"
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "AI Generation Failed")
            print("Failed to generate tweet from Claude. Exiting.")
            try:
                os.remove(OUTPUT_FILENAME)
            except:
                pass
            return

        # === Step 4: Get Telegram Approval ===
        try:
            is_approved = request_telegram_approval(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, generated_tweet)
        except Exception as e:
            error_msg = f"Failed to get Telegram approval\nError: {e}"
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Telegram Error")
            print(f"Telegram approval failed: {e}")
            is_approved = False

        # === Step 5: Post Tweet if Approved ===
        if is_approved:
            try:
                success = post_tweet(generated_tweet, TWEEPY_API_KEY, TWEEPY_API_SECRET, TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_SECRET)
                if success:
                    send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, f"✅ Tweet posted successfully!\n\nTweet: {generated_tweet}", "Success")
                else:
                    send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, f"❌ Failed to post tweet\n\nTweet content: {generated_tweet}", "Posting Failed")
            except Exception as e:
                error_msg = f"Error during tweet posting\nTweet: {generated_tweet}\nError: {e}"
                send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Posting Error")
        else:
            print("Tweet not approved. Process finished.")

        # === Step 6: Cleanup ===
        try:
            if os.path.exists(OUTPUT_FILENAME):
                os.remove(OUTPUT_FILENAME)
                print("Temporary CSV file deleted. Bot run complete.")
        except Exception as e:
            print(f"Failed to delete CSV file: {e}")
            
    except Exception as e:
        # Critical error handler
        error_msg = f"Critical error in run_bot()\nError: {e}"
        try:
            send_error_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_msg, "Critical Error")
        except:
            print(f"Failed to send critical error notification: {error_msg}")
        print(f"Critical error: {e}")
        
        # Cleanup on critical error
        try:
            if 'OUTPUT_FILENAME' in locals() and os.path.exists(OUTPUT_FILENAME):
                os.remove(OUTPUT_FILENAME)
        except:
            pass


if __name__ == "__main__":
    run_bot()
