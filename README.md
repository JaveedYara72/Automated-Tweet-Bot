# Automated Tweet Bot 🤖

An AI-powered Twitter bot that generates contextual tweets in your personal voice, with human approval via Telegram.

## 🧠 The Philosophy Behind This Bot

**Why Another Twitter Bot?**
Most Twitter bots either spam generic content or sound robotic. This bot is different:

1. **Context-Aware**: Instead of posting random thoughts, it reads what the community is currently discussing
2. **Your Voice**: Uses your actual writing samples to mimic YOUR personality, not generic AI-speak
3. **Human-in-the-Loop**: You approve every tweet via Telegram before it goes live
4. **Future-Proof**: Automatically handles API changes and model updates
5. **Error-Resilient**: Comprehensive error handling with real-time Telegram notifications

**The Process:**

```
Community Tweets → AI Analysis → Your Voice → Human Approval → Auto-Post
```

## ⚡ Quick Start (5 Minutes)

**For Complete Beginners:**

1. **Fork this repo** (click the Fork button above)
2. **Get your API keys** (follow the detailed guide below)
3. **Add them as GitHub Secrets**
4. **Customize your writing style** in `main.py`
5. **Enable GitHub Actions** - it runs automatically 3x/day

**For Developers:**

```bash
git clone https://github.com/JaveedYara72/Automated-Tweet-Bot.git
cd "To your folder"
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py  # Test locally first
```

## 🚨 Important Notes Before You Start

- **Twitter Permissions**: Your Twitter app MUST have "Read and Write" permissions
- **API Costs**: Claude API costs ~$0.01-0.05 per tweet (very cheap)
- **Rate Limits**: Built-in handling for all API rate limits
- **Security**: Never commit API keys to GitHub - always use Secrets

---

This project is a fully automated Python bot that scrapes popular tweets from a specific Twitter (X) community, uses an AI model (Claude) to generate a new, relevant tweet in your personal style, asks for your approval via Telegram, and then posts the tweet to your account.

The entire process is designed to run automatically on a schedule using GitHub Actions.

✨ Features
Context-Aware: Scrapes the latest popular tweets from a target community to understand current conversations.

Personalized Voice: Uses your own writing samples to generate tweets that sound just like you.

AI-Powered: Leverages the Claude language model for creative and relevant tweet generation.

Human-in-the-Loop: Sends every generated tweet to your Telegram for approval before posting.

Fully Automated: Runs on a schedule (e.g., three times a day) using a free GitHub Actions workflow.

Secure: Keeps all your API keys and secret tokens safe using GitHub Secrets.

📋 Prerequisites
Before you begin, ensure you have the following installed on your local machine:

Python 3.9+

Git

🚀 Setup and Deployment Guide
Follow these steps to get your automated tweet bot up and running.

Step 1: Clone the Repository and Install Dependencies
First, get the code onto your local machine and install the necessary Python libraries.

# Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

# Install the required libraries

pip install -r requirements.txt

Step 2: Obtain All Required API Keys
This is the most critical step. You will need to gather keys and tokens from four different services.

1. twitterapi.io Key (For Scraping Tweets)
   Link: https://twitterapi.io/

Steps:

Sign up for an account.

Navigate to your dashboard and copy your API Key.

You will later store this as a GitHub Secret named TWITTERAPI_IO_KEY.

2. Official Twitter API v2 Keys (For Posting Tweets)
   Link: https://developer.twitter.com/en/portal/dashboard

Steps:

Apply for a Developer Account and create a new Project and App.

Set App Permissions (CRITICAL):

In your App's settings, go to "User authentication settings" and click "Edit".

Set App permissions to "Read and Write".

Set Type of App to "Web App, Automated App or Bot".

Use http://127.0.0.1:3000 for the Callback URI and your GitHub repo URL for the Website URL.

Save the settings.

Generate Keys and Tokens:

Go to the "Keys and Tokens" tab.

Copy your API Key and API Key Secret.

Under "Access Token and Secret", click "Generate". Copy both the Access Token and Access Token Secret.

3. Anthropic API Key (For Claude)
   Link: https://console.anthropic.com/

Steps:

Sign up and navigate to the "API Keys" section.

Create a Key, give it a name, and copy it.

You will store this as CLAUDE_API_KEY.

4. Telegram Bot Token and Chat ID (For Notifications)
   Steps:

Get Bot Token: Open Telegram, search for BotFather, send /newbot, and follow the prompts. Copy the token he gives you.

Get Your Chat ID: Search for userinfobot, start a chat, and it will give you your Chat ID.

Step 3: Configure the Bot
Before deploying, you need to customize the bot's behavior and persona in the main.py file.

**Set Community ID:**

1. Go to Twitter/X and find the community you want to target
2. Click on the community URL - it will look like: `https://twitter.com/i/communities/1733520006279815231`
3. Copy the number at the end (e.g., `1733520006279815231`)
4. Open `main.py` and replace the `COMMUNITY_ID` variable with your number

**Customize Your Persona (CRITICAL STEP):**
This is what makes your bot sound like YOU, not a generic AI:

1. **WhatsApp Messages**: Fill in `whatsapp_t1`, `whatsapp_t2`, `whatsapp_t3` with casual messages you've sent to friends
2. **Twitter Posts**: Fill in `twitter_t1`, `twitter_t2`, `twitter_t3` with your existing tweets that represent your voice
3. **Be Authentic**: Use real messages that show your personality, humor, and writing style

Example:

```python
whatsapp_t1 = """Bro, just spent 3 hours debugging only to realize I forgot a semicolon. Why do I do this to myself? 😭"""
twitter_t1 = """Hot take: If your startup's main feature is 'AI-powered', you probably don't have a real product yet."""
```

Step 4: Set Up GitHub Secrets
Push your configured code to your GitHub repository. Then, add all your API keys as secrets.

In your GitHub repository, go to Settings > Secrets and variables > Actions.

Click New repository secret for each key. The secret names must match the ones in the table below.

Secret Name

Service

Description

TWITTERAPI_IO_KEY

twitterapi.io

For scraping community tweets.

CLAUDE_API_KEY

Anthropic (Claude)

For generating the tweet text.

TELEGRAM_BOT_TOKEN

Telegram

Your bot's token from BotFather.

TELEGRAM_CHAT_ID

Telegram

Your personal user ID.

TWEEPY_API_KEY

Twitter Developer

Your App's API Key.

TWEEPY_API_SECRET

Twitter Developer

Your App's API Key Secret.

TWEEPY_ACCESS_TOKEN

Twitter Developer

Your user account's Access Token.

TWEEPY_ACCESS_SECRET

Twitter Developer

Your user account's Access Secret.

Step 5: Test Locally (Recommended)
Before deploying to GitHub Actions, test the bot locally:

```bash
# Make sure you're in the project directory with venv activated
export TWITTERAPI_IO_KEY="your_key_here"
export CLAUDE_API_KEY="your_key_here"
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
export TWEEPY_API_KEY="your_key_here"
export TWEEPY_API_SECRET="your_secret_here"
export TWEEPY_ACCESS_TOKEN="your_token_here"
export TWEEPY_ACCESS_SECRET="your_secret_here"

python main.py
```

## 🔧 Troubleshooting Common Issues

**"403 Forbidden" Twitter Error:**

- Your Twitter app doesn't have "Read and Write" permissions
- Go to Twitter Developer Portal → Your App → Settings → User authentication settings
- Change to "Read and Write" and regenerate your Access Token & Secret

**"Model not found" Claude Error:**

- The bot automatically tries multiple Claude models
- If all fail, check your Claude API key and account credits

**No Telegram notifications:**

- Double-check your Bot Token and Chat ID
- Make sure you've started a chat with your bot first

**"No tweets scraped":**

- Check your `COMMUNITY_ID` is correct
- Verify your `TWITTERAPI_IO_KEY` has credits remaining

## 💡 Customization Tips

**Change posting frequency:**
Edit `.github/workflows/main.yml` and modify the cron schedule:

```yaml
schedule:
  - cron: "0 9,15,21 * * *" # 9 AM, 3 PM, 9 PM UTC
```

**Target different communities:**
Change the `COMMUNITY_ID` in `main.py` to scrape from different Twitter communities.

**Adjust tweet style:**
Modify the `PROMPT_TEXT` in `main.py` to change how the AI generates tweets.

**Add more error handling:**
The bot already sends Telegram notifications for all major errors, but you can customize the messages in `telegram_handler.py`.
