import requests
from bs4 import BeautifulSoup
import feedparser
import re
import random
import string

### Configuration ###
POSSIBLE_FEED_KEYS = ['link', 'id', 'published', 'title', 'summary']

### Enumerated Types ###
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

ACTIVITY_ITEM_TYPES = enum(UPVOTE=1, USER_FOLLOW=2, WANT_ANSWER=3, ANSWER=4, REVIEW_REQUEST=5)
LOG_ENTRY_TYPES     = enum(ANSWER_ADDED=1, ANSWER_DELETED=2, COMMENT=2, EDIT=3, TOPIC=4)

####################################################################
# Helpers
####################################################################
def try_cast_int(s):
    try:
        temp = re.findall('\d', str(s))
        temp = ''.join(temp)
        return int(temp)
    except ValueError:
        return s

def get_name(source):
    return str(source.find('span', attrs={'class' : 'user'}).string)

def extract_name(log_entry):
    print log_entry
    name = re.match('Answer added by ([a-zA-Z-\ ]*)\. ?$', log_entry)
    if name is not None:
        return name.group(1)
    else:
        return None

def extract_username(username):
    if 'https://www.quora.com/' not in username['href']:
        return username['href'][1:]
    else:
        username = re.search("[a-zA-Z-\-]*\-+[a-zA-Z]*-?[0-9]*$", username['href'])
        if username is not None:
            return username.group(0)
        else:
            return None

def get_count(element):
    count = element.find('span', class_='profile-tab-count').string.replace(',', '')
    return try_cast_int(count)

def get_count_for_user_href(soup, user, suffix):
    element = soup.find('a', class_='link_label', href='/' + user + '/' + suffix)
    return get_count(element)

def build_feed_item(item):
    result = {}
    keys = POSSIBLE_FEED_KEYS
    for key in keys:
        if key in item.keys():
            result[key] = item[key]
    return result

def is_want_answer(description):
    tag  = description.find('span', id = re.compile('^[a-z]*_+[a-z]*_+[0-9]*$'))
    if tag is not None:
        return True
    else:
        return False

def is_author(link, baseurl):
    author = re.search('[a-zA-Z-\-]*\-+[a-zA-Z]*-?[0-9]*$', link)
    user   = re.search('com*\/([a-zA-Z]*\-+[a-zA-Z]*-?[a-z-A-Z-0-9]*)\/rss$', baseurl)
    if user is not None and author is not None:
        author = author.group(0)
        user   = user.group(1)
        return author == user
    else:
        return False

def is_review(link):
    if link is not None:
        match = re.search('^https?:\/\/www\.?quora.com\/Reviews-of[a-zA-Z0-9-\-]*$', link)
        if match is not None:
            return True
        else:
            return False
    else:
        return False

def check_activity_type(entry):
    description = BeautifulSoup(entry['description'])
    link        = entry['link']
    base_url    = entry['summary_detail']['base']

    if entry['description'] == '':
        return ACTIVITY_ITEM_TYPES.USER_FOLLOW
    elif is_review(link) is True:
        return ACTIVITY_ITEM_TYPES.REVIEW_REQUEST
    elif is_want_answer(description) is True:
        return ACTIVITY_ITEM_TYPES.WANT_ANSWER
    elif is_author(link, base_url) is True:
        return ACTIVITY_ITEM_TYPES.ANSWER
    else:
        return ACTIVITY_ITEM_TYPES.UPVOTE

def is_answer_added_log(entry):
    return re.match("Answer added", entry) is not None

def is_answer_deleted_log(entry):
    return re.match("Answer deleted", entry) is not None

def is_comment_log(entry):
    return re.match("Comment:", entry) is not None

def is_edit_log(entry):
    return False

def is_topic_log(entry):
    return re.match("Topic", entry) is not None or re.match("Context", entry) is not None

def check_log_type(log_entry):
    print "a"
    if is_answer_added_log(log_entry) is True:
        return LOG_ENTRY_TYPES.ANSWER_ADDED
    elif is_answer_deleted_log(log_entry) is True:
        return LOG_ENTRY_TYPES.ANSWER_DELETED
    elif is_comment_log(log_entry) is True:
        return LOG_ENTRY_TYPES.COMMENT
    elif is_edit_log(log_entry) is True:
        return LOG_ENTRY_TYPES.EDIT
    elif is_topic_log(log_entry) is True:
        return LOG_ENTRY_TYPES.TOPIC
    else:
        return None

####################################################################
# API
####################################################################

class Quora:
    @staticmethod
    def get_user_stats(user):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + user).text)
        data_stats = []
        name = get_name(soup)
        err = None

        for item in soup.find_all('span', attrs={'class' : 'profile_count'}):
            data_stats.append(item)
        data_stats = map(try_cast_int, data_stats)

        user_dict = {'answers'   : data_stats[1],
                     'blogs'     : err,
                     'edits'     : data_stats[5],
                     'followers' : data_stats[3],
                     'following' : data_stats[4],
                     'name'      : name,
                     'posts'     : data_stats[2],
                     'questions' : data_stats[0],
                     'topics'    : err,
                     'username'  : user }
        return user_dict

    @staticmethod
    def get_user_activity(user):
        f = feedparser.parse('http://www.quora.com/' + user + '/rss')
        result = {
            'username': user,
            'last_updated': f.feed.updated
        }
        for entry in f.entries:
            if 'activity' not in result.keys():
                result['activity'] = []
            result['activity'].append(build_feed_item(entry))
        return result

    @staticmethod
    def get_activity(user):
        f = feedparser.parse('http://www.quora.com/' + user + '/rss')
        activity = Activity()
        for entry in f.entries:
            activity_type = check_activity_type(entry)
            if activity_type is not None:
                if activity_type == ACTIVITY_ITEM_TYPES.UPVOTE:
                    activity.upvotes.append(build_feed_item(entry))
                elif activity_type == ACTIVITY_ITEM_TYPES.USER_FOLLOW:
                    activity.user_follows.append(build_feed_item(entry))
                elif activity_type == ACTIVITY_ITEM_TYPES.WANT_ANSWER:
                    activity.want_answers.append(build_feed_item(entry))
                elif activity_type == ACTIVITY_ITEM_TYPES.ANSWER:
                    activity.answers.append(build_feed_item(entry))
                elif activity_type == ACTIVITY_ITEM_TYPES.REVIEW_REQUEST:
                    activity.review_requests.append(build_feed_item(entry))
        return activity

    @staticmethod
    def get_activity_keys():
        return POSSIBLE_FEED_KEYS

    @staticmethod
    def get_question_stats(question):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + question).text)
        raw_topics = soup.find_all('span', attrs={'itemprop' : 'title'})
        topics = []

        for topic in raw_topics:
            topics.append(topic.string)

        want_answers = soup.find('span', attrs={'class' : 'count'}).string
        answer_count = soup.find('div', attrs={'class' : 'answer_count'}).next.split()[0]
        question_text = list(soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1').children)[-1]

        question_dict = {'want_answers' : try_cast_int(want_answers),
                         'answer_count' : try_cast_int(answer_count),
                         'question_text' : question_text,
                         'topics' : topics }
        return question_dict

    @staticmethod
    def get_one_answer(question, author=None):
        """(str, str) -> dict

        >>> q.get_one_answer('What-are-some-mistakes-you-noticed-on-Friends', 'Mayur-P-R-Rohith')
        >>> q.get_one_answer('znntQ')
        >>> q.get_one_answer('http://qr.ae/znntQ')
        {'want_answers': 78, 'views': 47, 'question': 'http://qr.ae/znntQ',
        'comment_count': 0, 'author': u'Mayur', 'answer': '...', 'upvote_count': 3}

        >>> print q.get_one_answer('znntQ1')
        {}
        """
        try:
            if author is None:
                # For short URL's
                if re.match('http:', question):
                    # question like http://qr.ae/znrZ3
                    soup = BeautifulSoup(requests.get(question).text)
                else:
                    # question like znrZ3
                    soup = BeautifulSoup(requests.get('http://qr.ae/' + question).text)
                author = soup.find('span', attrs = {'class' : 'user'}).text
            else:
                soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/answer/' + author).text)

            answer = soup.find('div', id = re.compile('_answer_content$')).find('div', id = re.compile('_container'))
            question_link = soup.find('link', attrs = {'href' : re.compile('^https://www.quora.com/')}).get('href')
            views = soup.find('span', attrs = {'class' : 'stats_row'}).next.next.next.next
            want_answers = soup.find('span', attrs = {'class' : 'count'}).string

            upvote_count = soup.find('a', attrs = {'class' : 'vote_item_link'}).find('span', attrs = {'class' : 'count'})
            if upvote_count is None:
                upvote_count = 0

            try:
                comment_count = soup.find_all('a', id = re.compile('_view_comment_link'))[-1].find('span').string
                # '+' is dropped from the number of comments.
                # Only the comments directly on the answer are considered. Comments on comments are ignored.
            except:
                comment_count = 0

            answer_stats = map(try_cast_int, [views, want_answers, upvote_count, comment_count])

            answer_dict = {'views' : answer_stats[0],
                           'want_answers' : answer_stats[1],
                           'upvote_count' : answer_stats[2],
                           'comment_count' : answer_stats[3],
                           'answer' : str(answer),
                           'question' : question,
                           'question_link' : question_link,
                           'author' : author
            }
            return answer_dict
        except:
            return dict()

    @staticmethod
    def get_latest_answers(question):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/log').text)
        answered_by = []
        clean_logs   = []
        raw_logs = soup.findAll('div', attrs={'class' : 'feed_item_activity'})

        for entry in raw_logs:
            username = entry.find('a', attrs={'class' : 'user'})
            if username is not None:
                username = extract_username(username)
                if username not in answered_by:
                    answered_by.append(username)

        return [Quora.get_one_answer(question, author) for author in answered_by]

    @staticmethod
    def get_random_answers(count):
        answers = []
        while len(answers) < count:
            question = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(5))
            answer = Quora.get_one_answer(question)
            if answer:
                answers.append(answer)
        return answers


class Activity:
    def __init__(self, args=None):
        self.upvotes = []
        self.user_follows = []
        self.want_answers = []
        self.answers = []
        self.review_requests = []
