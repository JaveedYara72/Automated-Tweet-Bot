import tweepy
import os

def post_tweet(tweet_text: str, api_key: str, api_secret: str, access_token: str, access_token_secret: str) -> bool:
    """
    Posts a tweet to Twitter using the v2 API with a tweepy.Client object.

    Args:
        tweet_text: The text content of the tweet to be posted.
        api_key (str): Your Twitter App's API / Consumer Key.
        api_secret (str): Your Twitter App's API / Consumer Secret.
        access_token (str): The Access Token for your user account.
        access_token_secret (str): The Access Token Secret for your user account.

    Returns:
        True if the tweet was posted successfully, False otherwise.
    """
    try:
        # --- Initialize the client using the provided API keys and tokens ---
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        print("Posting tweet to Twitter...")
        
        # The create_tweet method belongs to the tweepy.Client object
        response = client.create_tweet(text=tweet_text)
        
        # Check the response to confirm success
        if response.data and response.data['id']:
            print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
            return True
        else:
            print("Failed to post tweet. Response did not contain expected data.")
            print(f"Full Response: {response}")
            return False

    except tweepy.errors.Forbidden as e:
        print(f"--- 403 Forbidden Error ---")
        print(f"Error: {e}")
        print("This is a permissions issue. Please double-check that your app in the Twitter Developer Portal has 'Read and Write' permissions and that you have regenerated your Access Token and Secret after changing the permission.")
        return False
    except tweepy.errors.Unauthorized as e:
        print(f"--- 401 Unauthorized Error ---")
        print(f"Error: {e}")
        print("Invalid Twitter API credentials. Check your API keys and tokens.")
        return False
    except tweepy.errors.TooManyRequests as e:
        print(f"--- 429 Rate Limit Error ---")
        print(f"Error: {e}")
        print("Twitter API rate limit exceeded. Try again later.")
        return False
    except tweepy.errors.BadRequest as e:
        print(f"--- 400 Bad Request Error ---")
        print(f"Error: {e}")
        print("Invalid tweet content or parameters.")
        return False
    except tweepy.errors.TwitterServerError as e:
        print(f"--- Twitter Server Error ---")
        print(f"Error: {e}")
        print("Twitter is experiencing server issues. Try again later.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while posting the tweet: {e}")
        return False
