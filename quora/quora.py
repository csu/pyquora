from bs4 import BeautifulSoup
import re
import requests

####################################################################
# Helpers
####################################################################
def try_cast_int(s):
  """ (str) -> int
  Look for digits in the given string and convert them to the required number.
  ('2 upvotes') -> 2
  ('2.2k upvotes') -> 2200
  """
  try:
    pattern = re.compile(r'([0-9]+(\.[0-9]+)*[ ]*[Kk])|([0-9]+)')
    raw_result = re.search(pattern, s).groups()
    if raw_result[2] != None:
      return int(raw_result[2])
    elif raw_result[1] == None:
      raw_result = re.search(r'([0-9]+)', raw_result[0])
      return int(raw_result.groups()[0]) * 1000
    else:
      raw_result = re.search(r'([0-9]+)\.([0-9]+)', raw_result[0]).groups()
      return int(raw_result[0]) * 1000 + int(raw_result[1]) * 100
  except:
    return s

def get_question_link(soup):
  """ (soup) -> str
  Returns the link at which the question can is present.
  """
  question_link = soup.find('a', attrs = {'class' : 'question_link'})
  return 'http://www.quora.com' + question_link.get('href')

def get_author(soup):
  """ (soup) -> str
  Returns the name of the author
  """
  raw_author = soup.find('div', attrs = {'class' : 'author_info'}).next.get('href')
  author = raw_author.split('/')[-1]
  return author

def extract_username(username):
  """ (soup) -> str
  Returns the username of the author
  """
  if 'https://www.quora.com/' not in username['href']:
    return username['href'][1:]
  else:
    username = re.search("[a-zA-Z-\-]*\-+[a-zA-Z]*-?[0-9]*$", username['href'])
    if username is not None:
      return username.group(0)
    else:
      return None

####################################################################
# API
####################################################################
class Quora:
  """
  The class that contains functions required to fetch details of questions and answers.
  """
  @staticmethod
  def get_one_answer(question, author=None):
    """ (str [, str]) -> dict
    Fetches one answer and it's details.
    """
    if author is None: # For short URL's
      if question.startswith('http'): # question like http://qr.ae/znrZ3
        content = requests.get(question).text
      else: # question like znrZ3
        content = requests.get('http://qr.ae/' + question).text
    else:
      content = requests.get('http://www.quora.com/' + question + '/answer/' + author + '?share=1').text

    soup = BeautifulSoup(content, "html.parser")
    return Quora.scrape_one_answer(soup)

  @staticmethod
  def scrape_one_answer(soup):
    """ (soup) -> dict
    Scrapes the soup object to get details of an answer.
    """
    try:
      answer = soup.find('div', id = re.compile('_answer_content$')).find('div', id = re.compile('_container'))
      question_link = get_question_link(soup)
      author = get_author(soup)
      views = soup.find('span', attrs = {'class' : 'stats_row'}).next.next.next.next

      try:
        upvote_count = soup.find('a', attrs = {'class' : 'vote_item_link'}).find('span', attrs = {'class' : 'count'}).string
        if upvote_count is None:
          upvote_count = 0
      except:
        upvote_count = 0

      try:
        comment_count = soup.find_all('a', id = re.compile('_view_comment_link'))[-1].find('span').string
        # '+' is dropped from the number of comments.
        # Only the comments directly on the answer are considered. Comments on comments are ignored.
      except:
        comment_count = 0

      answer_dict = {'views' : try_cast_int(views),
               'upvote_count' : try_cast_int(upvote_count),
               'comment_count' : try_cast_int(comment_count),
               'answer' : str(answer),
               'question_link' : question_link,
               'author' : author
              }
      return answer_dict
    except:
      return {}

  @staticmethod
  def get_latest_answers(question):
    """ (str) -> list
    Takes the title of one question and returns the latest answers to that question.
    """
    soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/log').text, "html.parser")
    authors =  Quora.scrape_latest_answers(soup)
    return [Quora.get_one_answer(question, author) for author in authors]

  @staticmethod
  def scrape_latest_answers(soup):
    """ (soup) -> list
    Returns a list with usernames of those who have recently answered the question.
    """
    try:
      authors = []
      clean_logs = []
      raw_logs = soup.find_all('div', attrs={'class' : 'feed_item_activity'})

      for entry in raw_logs:
        if 'Answer added by' in entry.next:
          username = entry.find('a', attrs={'class' : 'user'})
          if username is not None:
            username = extract_username(username)
            if username not in authors:
              authors.append(username)
      return authors
    except:
      return []

  @staticmethod
  def get_question_stats(question):
    """ (soup) -> dict
    Returns details about the question.
    """
    soup = BeautifulSoup(requests.get('http://www.quora.com/' + question).text, "html.parser")
    return Quora.scrape_question_stats(soup)

  @staticmethod
  def scrape_question_stats(soup):
    """ (soup) -> dict
    Scrapes the soup object to get details of a question.
    """
    try:
      raw_topics = soup.find_all('span', attrs={'itemprop' : 'title'})
      topics = []
      for topic in raw_topics:
        topics.append(topic.string)

      answer_count = soup.find('div', attrs={'class' : 'answer_count'}).next.split()[0]
      question_text = list(soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1').children)[-1]
      question_details = soup.find('div', attrs = {'class' : 'question_details_text'})
      answer_wiki = soup.find('div', attrs = {'class' : 'AnswerWikiArea'}).find('div')

      question_dict = {
               'answer_count' : try_cast_int(answer_count),
               'question_text' : question_text.string,
               'topics' : topics,
               'question_details' : str(question_details),
               'answer_wiki' : str(answer_wiki),
              }
      return question_dict
    except:
      return {}

  ### Legacy API
  @staticmethod
  def get_user_stats(u):
    """ (str) -> dict
    Depreciated. Use the User class.
    """
    from user import User
    return User.get_user_stats(u)

  @staticmethod
  def get_user_activity(u):
    """ (str) -> dict
    Depreciated. Use the User class.
    """
    from user import User
    return User.get_user_activity(u)

  @staticmethod
  def get_activity(u):
    """ (str) -> dict
    Depreciated. Use the User class.
    """
    from user import User
    return User.get_activity(u)
