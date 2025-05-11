import praw
import os
from dotenv import load_dotenv
from strip_markdown import strip_markdown

load_dotenv()

def get_reddit_client():
    print(os.getenv("REDDIT_CLIENT_ID"))

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )
    return reddit

def get_readonly_reddit_client():

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    return reddit

def get_subreddit_content(subreddit_name, limit=10):
    reddit = get_readonly_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    posts = []
    try:
        submissions = subreddit.new(limit=limit)

        for submission in submissions:
            if not submission.is_self:
                continue
            post = {
                "title": strip_markdown(submission.title),
                "selftext": strip_markdown(submission.selftext)
            }
            posts.append(post)

    except Exception as e:
        print(f"Error fetching subreddit {subreddit_name}: {e}")
        return []

    return posts