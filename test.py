#import prawless\misc\generate_username.py import it so I see it as misc.generate_username() in the code
from prawless.main import Reddit
from prawless.clients.reddit_client import RedditHTTPClient
import praw
import asyncio
from prawless.misc.random_usernames import generate_usernames

# PRAW Setup
reddit_praw = praw.Reddit(
    client_id="LoG9BNZNT1a81MsQnta6ag",
    client_secret="X_Lf4igBojOuqeLTjOSjIGfVxUC6HQ",
    username="Pure-Camp-9169",
    password="123456seven",
    user_agent="random"
)

# PRAWLESS Setup
client = RedditHTTPClient()
reddit_prawless = Reddit(client)


def compare_submission(submission_id):
    # PRAW
    submission_praw = reddit_praw.submission(id=submission_id)
    print(f"[PRAW] Submission Title: {submission_praw.title}")

    # PRAWLESS
    async def fetch_prawless_submission():
        submission = await reddit_prawless.submission(submission_id)
        print(f"[PRAWLESS] Submission Title: {submission.title}")

    asyncio.run(fetch_prawless_submission())


def compare_top_comments(submission_id):
    # PRAW
    submission_praw = reddit_praw.submission(id=submission_id)
    submission_praw.comments.replace_more(limit=0)
    for comment in submission_praw.comments.list()[:5]:
        print(f"[PRAW] Comment by {comment.author}: {comment.body[:50]}...")

    # PRAWLESS
    async def fetch_prawless_comments():
        submission = await reddit_prawless.submission(submission_id)
        for comment in submission.comments[:5]:
            print(f"[PRAWLESS] Comment by {comment.author}: {comment.body[:50]}...")

    asyncio.run(fetch_prawless_comments())


def compare_redditor_data(username):
    # PRAW
    redditor_praw = reddit_praw.redditor(username)
    print(f"[PRAW] Redditor {redditor_praw.name} - Karma: {redditor_praw.link_karma}")

    # PRAWLESS
    async def fetch_prawless_redditor():
        redditor = await reddit_prawless.redditor(username)
        print(f"[PRAWLESS] Redditor {redditor.name} - Karma: {redditor.link_karma}")

    asyncio.run(fetch_prawless_redditor())
    

def compare_redditor_submissions(username):
    # PRAW
    redditor_praw = reddit_praw.redditor(username)
    for submission in redditor_praw.submissions.new(limit=5):
        print(f"[PRAW] Submission: {submission.title}")

    # PRAWLESS
    async def fetch_prawless_submissions():
        async for submission in reddit_prawless.user_submissions(username, limit=5):
            print(f"[PRAWLESS] Submission: {submission.title}")

    asyncio.run(fetch_prawless_submissions())


def compare_subreddit_submissions(subreddit_name, limit=150):
    # PRAW
    print(f"\nFetching {limit} recent submissions from {subreddit_name} using PRAW:")
    print("-" * 50)
    praw_submissions = list(reddit_praw.subreddit(subreddit_name).new(limit=limit))
    for submission in praw_submissions:
        print(f"[PRAW] {submission.title}")

    # PRAWLESS
    print(f"\nFetching {limit} recent submissions from {subreddit_name} using PRAWLESS:")
    print("-" * 50)

    async def fetch_prawless_submissions():
        subbreddit_instance = await reddit_prawless.subreddit(subreddit_name)
        
        async for submission in subbreddit_instance.new(limit=limit):
            print(f"[PRAWLESS] {submission.title}")


    asyncio.run(fetch_prawless_submissions())


def compare_subreddit_data(subreddit_name):
    print(f"\nFetching data for {subreddit_name} using PRAW:")
    print("-" * 50)
    subreddit_praw = reddit_praw.subreddit(subreddit_name)
    print(f"[PRAW] Subreddit Name: {subreddit_praw.display_name}")
    print(f"[PRAW] Subreddit Title: {subreddit_praw.title}")
    print(f"[PRAW] Subreddit Subscribers: {subreddit_praw.subscribers}")
    print(f"[PRAW] Subreddit Created: {subreddit_praw.created_utc}")
    
    print(f"\nFetching data for {subreddit_name} using PRAWLESS:")
    async def fetch_prawless_subreddit():
        subreddit_prawless = await reddit_prawless.subreddit(subreddit_name)
        print(f"[PRAWLESS] Subreddit Name: {subreddit_prawless.display_name}")
        print(f"[PRAWLESS] Subreddit Title: {subreddit_prawless.title}")
        print(f"[PRAWLESS] Subreddit Subscribers: {subreddit_prawless.subscribers}")
        print(f"[PRAWLESS] Subreddit Created: {subreddit_prawless.created_utc}")
    
    asyncio.run(fetch_prawless_subreddit())
        
    
def get_rules(subreddit_name):
    async def fetch_prawless_subreddit():
        subreddit_prawless = await reddit_prawless.subreddit(subreddit_name)
        rules = await subreddit_prawless.rules
        for rule in rules:
            print(f"[PRAWLESS] Rule: {rule.short_name}, Description: {rule.description}, Violation Reason: {rule.violation_reason}")

    asyncio.run(fetch_prawless_subreddit())
    
    
def gen_users():
    print(asyncio.run(generate_usernames()))
            
            
    
    
if __name__ == "__main__":
    submission_id_test = "1745ihk"
    username_test = "spez"

    print("Comparing Submission Data")
    print("-" * 30)
    compare_submission(submission_id_test)

    print("\nComparing Top Comments")
    print("-" * 30)
    compare_top_comments(submission_id_test)

    print("\nComparing Redditor Data")
    print("-" * 30)
    compare_redditor_data(username_test)

    print("\nComparing Redditor Submissions")
    print("-" * 30)
    compare_redditor_submissions(username_test)

    print("\nComparing Subreddit Submissions")
    print("-" * 30)
    compare_subreddit_submissions("learnpython", limit=5)
    
    print("\nComparing Subreddit Data")
    print("-" * 30)
    compare_subreddit_data("learnpython")
    
    print("\nFetching Rules")
    print("-" * 30)
    get_rules("learnpython")
    
    print("\nGenerating Username")
    print("-" * 30)
    gen_users()
    
