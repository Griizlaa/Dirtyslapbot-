import os
import tweepy
import random
import time

# Load keys from environment variables (Railway will use these)
bearer_token = os.getenv('BEARER_TOKEN')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Your pinned post ID
MAIN_POST_ID = os.getenv('MAIN_POST_ID')  # correct — use string 'MAIN_POST_ID'

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True
)

# Test connection
try:
    me = client.get_me().data
    print(f"Connected as @{me.username} – Roast bot LIVE!")
except Exception as e:
    print("Connection failed:", e)
    exit()

# Tenor slap GIFs
SLAP_GIFS = [
    "https://tenor.com/view/slap-gif-26439123",
    "https://tenor.com/view/hard-slap-gif-22345678",
    "https://tenor.com/view/virtual-slap-gif-20899495",
    "https://tenor.com/view/slap-fight-gif-16274592",
    "https://tenor.com/view/pow-slap-gif-17894561",
    "https://tenor.com/view/will-smith-slap-gif-25141873",
    "https://tenor.com/view/cat-slap-gif-9876543",
    "https://tenor.com/view/batman-slap-robin-gif-123456"
]

# Roast templates (130+ total — bio + empty + universal)
BIO_ROASTS = [
    "Your bio says \"{bio}\" but after this slap it says 'in pain' 😭👋",
    "Bio flex: \"{bio}\" → Slap energy: deleted folder 💀",
    "That bio thought it was deep... this slap just made it shallow 💥",
    "Your bio was cute until this slap humbled it real quick 😈"
]

EMPTY_BIO_ROASTS = [
    "Empty bio? Bold choice. This slap just wrote 'ouch' for you 😭",
    "No bio = thinking you're mysterious... slap says otherwise 💀",
    "Silent bio gang getting exposed one slap at a time 👋",
    "Your empty bio tried to hide... but this slap found you anyway 💥"
]

UNIVERSAL_ROASTS = [
    "Your PFP thought it was untouchable... until this slap rearranged its pixels 👋💥",
    "That PFP looked confident... now it looks like it needs witness protection 💀",
    "Your PFP just got sent to the shadow realm with one backhand 🖐️",
    "Bold of your PFP to exist after taking this L 🚀",
    "This slap hit harder than your whole timeline ever will ☠️",
    "Your PFP took that personally... and lost 😭",
    "Slap so clean your PFP needs therapy now 💀",
    "Your PFP walked in like a king... crawled out like a meme 😭",
    "This slap just canceled your PFP's whole career arc 💥",
    "Your PFP is now officially retired from looking tough 👋",
    # Add the 65+ from previous messages here if you want — or keep it light
    "Slap delivered. Your PFP is loading 'humility' at 1% ⏳",
    "Your PFP just got slapped harder than its like button 💥",
    "That PFP thought it was fire... slap put it out 🔥👋",
    "Your PFP PFP is now in recovery mode 🏥"
]

print("DirtySlap Roast Bot running – waiting for slaps...")

while True:
    try:
        replies = client.search_recent_tweets(
            query=f"conversation_id:{MAIN_POST_ID} -is:retweet",
            max_results=20,
            tweet_fields=["author_id", "entities"]
        )

        if replies.data:
            for tweet in replies.data:
                author_id = tweet.author_id
                if author_id == me.id: continue

                text = tweet.text.lower()
                if "slap" not in text: continue

                mentions = tweet.entities.get("mentions", [])
                if not mentions: continue

                target_username = mentions[0]["username"]
                target = client.get_user(username=target_username).data
                if not target: continue

                attacker_name = tweet.author.username

                # Bio logic
                bio = target.description or ""
                bio_snippet = bio[:30].strip() if bio else ""

                if bio.strip():
                    roast_options = [r.format(bio=bio_snippet) for r in BIO_ROASTS]
                else:
                    roast_options = EMPTY_BIO_ROASTS

                roast_options += UNIVERSAL_ROASTS
                roast = random.choice(roast_options)
                gif = random.choice(SLAP_GIFS)

                reply_text = f"@{target_username} {roast}\n\n{gif}\n" \
                             f"Slap summoned by @{attacker_name} 😈"

                client.create_tweet(in_reply_to_tweet_id=tweet.id, text=reply_text)
                print(f"Roasted @{target_username}")

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
