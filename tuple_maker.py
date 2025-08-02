import pandas as pd

def format_tweets_for_prompt(csv_filename="community_rust_tweets.csv"):
    """
    Reads a CSV of scraped tweets and formats them into a multi-line string
    of (username, text, like_count) tuples, sorted by likes, for use in an
    LLM prompt.

    Args:
        csv_filename (str): The name of the CSV file to read.

    Returns:
        str: A multi-line string of (username, tweet_text, like_count) tuples,
             or an empty string if the file cannot be read or is empty.
    """
    try:
        df = pd.read_csv(csv_filename)
        
        # Ensure 'like_count' is a numeric type for correct sorting
        df['like_count'] = pd.to_numeric(df['like_count'])
        
        # Sort by 'like_count' in descending order and take the top 10
        df_sorted = df.sort_values(by="like_count", ascending=False).head(50)
        
        # Clean up the text by replacing newlines with spaces
        cleaned_texts = [str(text).replace('\n', ' ') for text in df_sorted['text']]
        
        # Create a list of tuples with username, text, and like_count
        tweet_tuples = list(zip(df_sorted['username'], cleaned_texts, df_sorted['like_count']))
        
        # Format each tuple into the desired string format: (username, text, likes)
        formatted_lines = []
        for username, text, likes in tweet_tuples:
            # Using repr() for the text to correctly handle quotes and special characters
            formatted_lines.append(f"({username}, {repr(text)}, {likes})")
            
        # Join the lines with a comma and a newline for the final output
        stringified_data = ",\n".join(formatted_lines)
        
        return stringified_data

    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
