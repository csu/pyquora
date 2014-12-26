import requests
from bs4 import BeautifulSoup
import feedparser
import re

### Configuration ###
POSSIBLE_FEED_KEYS = ['link', 'id', 'published', 'title', 'summary']

### Enumerated Types ###
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

ACTIVITY_ITEM_TYPES = enum(UPVOTE=1, USER_FOLLOW=2, WANT_ANSWER=3, ANSWER=4, REVIEW_REQUEST=5)

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

def get_count(element):
    return try_cast_int(element.find('span', class_='profile-tab-count').string.replace(',', ''))

def get_count_for_user_href(soup, user, suffix):
    return get_count(soup.find('a', class_='link_label', href='/' + user + '/' + suffix))

def build_feed_item(item):
    dict = {}
    keys = POSSIBLE_FEED_KEYS
    for key in keys:
        if key in item.keys():
            dict[key] = item[key]
    return dict

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

def format_name(name):
    try:
        return '-'.join(name.split())
    except:
        return ''

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

        for item in soup.findAll('span', attrs={'class' : 'profile_count'}):
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
        dict = {
            'username': user,
            'last_updated': f.feed.updated
        }
        for entry in f.entries:
            if 'activity' not in dict.keys():
                dict['activity'] = []
            dict['activity'].append(build_feed_item(entry))
        return dict

    @staticmethod
    def get_activity(user):
        f = feedparser.parse('http://www.quora.com/' + user + '/rss')
        activity = Activity()
        for entry in f.entries:
            type = check_activity_type(entry)
            if type is not None:
                if type == ACTIVITY_ITEM_TYPES.UPVOTE:
                    activity.upvotes.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.USER_FOLLOW:
                    activity.user_follows.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.WANT_ANSWER:
                    activity.want_answers.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.ANSWER:
                    activity.answers.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.REVIEW_REQUEST:
                    activity.review_requests.append(build_feed_item(entry))
        return activity

    @staticmethod
    def get_activity_keys():
        return POSSIBLE_FEED_KEYS

    @staticmethod
    def get_question_stats(question):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + question).text)
        raw_topics = soup.findAll('span', attrs={'itemprop' : 'title'})
        topics = []

        for topic in raw_topics:
            topics.append(i.topic)

        want_answers = soup.find('span', attrs={'class' : 'count'}).string
        answer_count = soup.find('div', attrs={'class' : 'answer_count'}).string
        question_stats = map(try_cast_int, [want_answers, answer_count])

        question_dict = {'want_answers' : try_cast(want_answers),
                         'answer_count' : try_cast(answer_count),
                         'topics' : topics }
        return question_dict

    @staticmethod
    def get_one_answer(question, user=None):
        """(str, str) -> dict

        >>> q.get_one_answer('What-are-some-mistakes-you-noticed-on-Friends', 'Mayur-P-R-Rohith')
        >>> q.get_one_answer('znntQ')
        >>> q.get_one_answer('http://qr.ae/znntQ')
        {'want_answers': 78, 'views': 47, 'question': 'http://qr.ae/znntQ',
        'comment_count': 0, 'user': u'Mayur', 'answer': '...', 'upvote_count': 3}

        >>> print q.get_one_answer('znntQ1')
        {}
        """
        try:
            if user is None:
                # For short URL's
                if re.match('http', question):
                    # question like http://qr.ae/znrZ3
                    soup = BeautifulSoup(requests.get(question).text)
                else:
                    # question like znrZ3
                    soup = BeautifulSoup(requests.get('http://qr.ae/' + question).text)
                user = soup.find('span', attrs = {'class' : 'user'}).text
            else:
                soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/answer/' + user).text)

            answer = soup.find('div', id = re.compile('_answer_content$')).find('div', id = re.compile('_container'))
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
                           'user' : user
            }
            return answer_dict
        except:
            return dict()

    @staticmethod
    def get_latest_answers(question):
        """(str) -> list

        >>> q.get_latest_answers('What-are-some-cool-Python-tricks')
        list of dicts that contain the answers and other details

        >>> q.get_latest_answers('non-existant-question')
        []
        """
        # Known bug: Some list elements might be empty dicts i.e. {}.
        # This happens when the answer's author has a number at the end of
        # of their username. Ex: Foo-Bar-23
        try:
            soup = BeautifulSoup(requests.get('https://www.quora.com/' + question + '/log').text)
            answered_by = []

            temp = soup.find('div', attrs = {'class' : 'QuestionLog FilteredLog PagedList Log'})
            temp = temp.find_all('div', attrs = {'class' : 'feed_item_activity'})

            for i in temp:
                if 'Answer added by' in i.next:
                    answered_by.append(i.find('a', attrs = {'class' : 'user'}).string)
            answered_by = map(format_name, answered_by)
            return [Quora.get_one_answer(question, i) for i in answered_by]
        except:
            return list()

class Activity:
    def __init__(self, args=None):
        self.upvotes = []
        self.user_follows = []
        self.want_answers = []
        self.answers = []
        self.review_requests = []
