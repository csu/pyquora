from bs4 import BeautifulSoup
from quora import try_cast_int
import feedparser
import re
import requests
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

def get_name(source):
    return str(source.find('span', attrs={'class' : 'user'}).string)

def extract_name(log_entry):
    print log_entry
    name = re.match('Answer added by ([a-zA-Z-\ ]*)\. ?$', log_entry)
    if name is not None:
        return name.group(1)
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
class User:
    def __init__(self, user):
        self.user = user
        self._stats = None
        self._activity = None

    @property
    def stats(self):
        if self._stats is None:
            self._stats = self.get_user_stats(self.user)
        return self._stats

    @property
    def activity(self):
        if self._activity is None:
            self._activity = self.get_user_activity(self.user)
        return self._activity

    @staticmethod
    def get_user_stats(user):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + user).text)
        data_stats = []
        name = get_name(soup)
        err = None

        for item in soup.find_all('span', attrs={'class' : 'profile_count'}):
            data_stats.append(item.string)
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

class Activity:
    def __init__(self, args=None):
        self.upvotes = []
        self.user_follows = []
        self.want_answers = []
        self.answers = []
        self.review_requests = []
