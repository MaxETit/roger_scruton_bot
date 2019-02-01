import praw
import config
import time
import os

def bot_login():
    print('Logging in...')
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "roger test bot v0.1")
    print('Logged in.')
    return r

def run_bot(r, comments_replied_to):
    print('Fetching 25 comments...')

    for comment in r.subreddit('ukpolitics').comments(limit=25):
        if 'Roger Scruton' in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print('String containing \'Roger Scruton\' found in comment ' + comment.id)
            comment.reply('Roger Scruton says: \'The real reason people are conservatives is that they are attached to the things they love, and want to preserve them from abuse and decay.\' [#triggerwarning](https://freebeacon.com/wp-content/uploads/2014/12/Roger-Scruton.jpg)')
            print('Replied to comment ' + comment.id)

            comments_replied_to.append(comment.id)

            with open ('comments_replied_to.txt', 'a') as f:
                f.write(comment.id + '\n')

    print('Sleeping for sixty seconds')
    #Sleep for sixty seconds....
    time.sleep(60)

def get_saved_comments():
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
    else:
        with open('comments_replied_to.txt', 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()

while True: 
    run_bot(r, comments_replied_to)