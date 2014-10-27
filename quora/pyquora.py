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

ACTIVITY_ITEM_TYPES = enum(UPVOTE=1, USER_FOLLOW=2, QUESTION_FOLLOW=3, ANSWER=4, QUESTION=5, REVIEW_REQUEST=6)

####################################################################
# Helpers
####################################################################
def try_cast(s):
    try:
        return int(s)
    except ValueError:
        return s

def get_count(element):
    return try_cast(element.find('span', class_='profile-tab-count').string.replace(',', ''))

def get_count_for_user_href(soup, user, suffix):
    return get_count(soup.find('a', class_='link_label', href='/' + user + '/' + suffix))

def build_feed_item(item):
    dict = {}
    keys = POSSIBLE_FEED_KEYS
    for key in keys:
        if key in item.keys():
            dict[key] = item[key]
    return dict

def check_activity_type(description):
    soup = BeautifulSoup(description)
    tag = soup.find('div', style="color: #666666;")
    if tag is not None:
        if 'voted up this' in tag.string:
            return ACTIVITY_ITEM_TYPES.UPVOTE
        elif 'followed a question' in tag.string:
            return ACTIVITY_ITEM_TYPES.QUESTION_FOLLOW
        elif 'added this answer' in tag.string:
            return ACTIVITY_ITEM_TYPES.ANSWER
        elif 'added a question' in tag.string:
            return ACTIVITY_ITEM_TYPES.QUESTION
        elif 'requested reviews.' in tag.string:
            return ACTIVITY_ITEM_TYPES.REVIEW_REQUEST
        else:  # hopefully.
            return ACTIVITY_ITEM_TYPES.USER_FOLLOW

def is_new_ui(soup):
    return soup.find('div', attrs={'class': 'ProfileTabs'}) is not None

####################################################################
# API
####################################################################

class Quora:
    @staticmethod
    def get_user_stats(user):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + user).text)
        data_stats = []
        err = 'no data'

        for item in soup.findAll('span', attrs={'class' : 'profile_count'}):
            m = re.findall('\d', str(item))
            element = ''.join(m)
            data_stats.append(element)

        user_dict = {'answers'   : data_stats[1],
                     'blogs'     : err,
                     'edits'     : data_stats[5],
                     'followers' : data_stats[3],
                     'following' : data_stats[4],
                     'name'      : user,
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
            type = check_activity_type(entry['description'])
            if type is not None:
                if type == ACTIVITY_ITEM_TYPES.UPVOTE:
                    activity.upvotes.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.USER_FOLLOW:
                    activity.user_follows.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.QUESTION_FOLLOW:
                    activity.question_follows.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.ANSWER:
                    activity.answers.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.QUESTION:
                    activity.questions.append(build_feed_item(entry))
                elif type == ACTIVITY_ITEM_TYPES.REVIEW_REQUEST:
                    activity.review_requests.append(build_feed_item(entry))
        return activity

    @staticmethod
    def get_activity_keys():
        return POSSIBLE_FEED_KEYS

class Activity:
    def __init__(self, upvotes=[], user_follows=[], question_follows=[], answers=[], questions=[], review_requests=[]):
        self.upvotes = upvotes
        self.user_follows = user_follows
        self.question_follows = question_follows
        self.answers = answers
        self.questions = questions
        self.review_requests = review_requests
