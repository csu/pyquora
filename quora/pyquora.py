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
def try_cast(s):
    try:
        return int(s)
    except ValueError:
        return s

def get_name(source):
    return str(source.find('span', attrs={'class' : 'user'}).string)

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

def want_answers(description):
    if description is not None:
        return re.match('^[0-9]* +Answers$|^1+ +Answer$', description.string)
    else:
        return False
    
def is_author(link, baseurl):
    if link.string is not None and baseurl.string is not None:
        link_username = str(re.search('[a-zA-Z]*\-+[a-zA-Z]*-?[0-9]*$', link.string).group(0))
        extracted_username = str(re.search('(com*\/)[a-zA-Z]*\-+[a-zA-Z]*-?[0-9]*(\/rss)$', baseurl.string).group(0))
        if link_username is not None and extracted_username is not None:
            return extracted_username == link_username
    else:
        return False
        
def is_review(link):
    if link.string is not None:
        match = re.match('^(https?:\/\/w{0,3}.?quora.com\/)(Reviews-of)([a-zA-Z0-9-\-])*', link.string)
        if match is not None:
            return match.group(2) == "Reviews-of"
        else:
            return False
    else:
        return False

def check_activity_type(entry):
    description = BeautifulSoup(entry['description'])
    tag  = description.find('span', id = re.compile('^[a-z]*_+[a-z]*_+[0-9]*$'))
    link     = BeautifulSoup(entry['link'])
    base_url = str(entry['summary_detail']['base'])

    if description is None:
        return ACTIVITY_ITEM_TYPES.USER_FOLLOW
    elif want_answers(tag):
        return ACTIVITY_ITEM_TYPES.WANT_ANSWER
    elif is_review(link):
        return ACTIVITY_ITEM_TYPES.REVIEW_REQUEST
    elif is_author(link, base_url):
        return ACTIVITY_ITEM_TYPES.ANSWER
    else:
        return ACTIVITY_ITEM_TYPES.UPVOTE

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
        name = get_name(soup)
        err = None

        for item in soup.findAll('span', attrs={'class' : 'profile_count'}):
            m = re.findall('\d', str(item))
            element = ''.join(m)
            data_stats.append(element)

        user_dict = {'answers'   : try_cast(data_stats[1]),
                     'blogs'     : err,
                     'edits'     : try_cast(data_stats[5]),
                     'followers' : try_cast(data_stats[3]),
                     'following' : try_cast(data_stats[4]),
                     'name'      : name,
                     'posts'     : try_cast(data_stats[2]),
                     'questions' : try_cast(data_stats[0]),
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

class Activity:
    def __init__(self, upvotes=[], user_follows=[], want_answers=[], answers=[], review_requests=[]):
        self.upvotes = upvotes
        self.user_follows = user_follows
        self.question_follows = question_follows
        self.answers = answers
        self.review_requests = review_requests
