import time
import praw
import prawcore
import requests
import logging
import re
import os
import datetime
import gc


import Config

reddit = praw.Reddit(client_id=Config.cid,
                     client_secret=Config.secret,
                     password=Config.password,
                     user_agent=Config.agent,
                     username=Config.user)
subreddit = reddit.subreddit(Config.subreddit)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=Config.apppath+'report.log',
                    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
os.environ['TZ'] = 'America/Los_Angeles'

f = open(Config.apppath+"submissionids.txt","a+")
f.close()
f = open(Config.apppath+"commentids.txt","a+")
f.close()


def submissionID(postid):
    f = open(Config.apppath+"submissionids.txt","a+")
    f.write(postid + "\n")
    f.close()

def commentID(postid):
    f = open(Config.apppath+"commentids.txt","a+")
    f.write(postid + "\n")
    f.close()

def getdomain( url ):
    match1 = re.search("(?:https?:\/\/)?(?:www\.)?([\w\-\.]+)", url)
    if match1:
      return match1.group(1)
    return None

def CheckWhite(text):
  if '#wiki_4._unauthorized_resellers' in text.lower():
    return None
  return True

def check_post(submission):
#    submissionID(submission.id)
    if submission.is_self:
    # check in subject
      if 'r/gamedeals' in submission.title.lower():
        data = { "text": 'https://redd.it/' + submission.id + ' `r/gamedeals` mention - title' }
        url = Config.Slack
        r = requests.post(url, json=data)
        logging.info( 'https://redd.it/' + submission.id + '`r/gamedeals` mention - title' )
      if 'r/gamedeals' in submission.selftext.lower() and CheckWhite(submission.selftext):
        data = { "text": 'https://redd.it/' + submission.id + ' `r/gamedeals` mention - body' }
        url = Config.Slack
        r = requests.post(url, json=data)
        logging.info( 'https://redd.it/' + submission.id + '`r/gamedeals` mention - body' )

    if not submission.is_self:
    # check in self post
      if 'r/gamedeals' in submission.title.lower():
        data = { "text": 'https://redd.it/' + submission.id + ' `r/gamedeals` mention - title' }
        url = Config.Slack
        r = requests.post(url, json=data)
        logging.info( 'https://redd.it/' + submission.id + '`r/gamedeals` mention - title' )




##cmt = reddit.comment('gxvgqy6')
#check_comment(cmt)
#exit()

#posts = subreddit.stream.submissions(pause_after=-1)
#cmts = subreddit.stream.comments(pause_after=-1)

while True:
  try:
    for post in subreddit.stream.submissions():
        if post is None:
            break
        check_post(post)


  except (prawcore.exceptions.RequestException, prawcore.exceptions.ResponseException):
        logging.info("Error connecting to reddit servers. Retrying in 1 minute...")
        time.sleep(60)

  except praw.exceptions.APIException:
        logging.info("Rate limited, waiting 5 seconds")
        time.sleep(5)
