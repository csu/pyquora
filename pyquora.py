import requests
from bs4 import BeautifulSoup
import feedparser

####################################################################
# Helpers
####################################################################
def get_count(element):
    try:
        return int(element.find('span', class_='profile-tab-count').string)
    except ValueError:
        return element.find('span', class_='profile-tab-count').string

def get_count_for_user_href(soup, user, suffix):
    return get_count(soup.find('a', class_='link_label', href='/' + user + '/' + suffix))

def parse_feed_item(item):
    dict = {}
    keys = ['link', 'guid', 'published', 'title', 'summary']
    print item.keys()
    for key in keys:
        if key in item.keys():
            dict[key] = item[key]
    return dict

####################################################################
# API
####################################################################

class Quora():
    @staticmethod
    def get_user_stats(user):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + user).text)
        user_dict = { 'username': user }
        user_dict['name'] = soup.find('h1').find('span', class_='user').string
        attributes_to_href_suffix = {
            'followers': 'followers',
            'following': 'following',
            'topics': 'topics',
            'blogs': 'blogs',
            'posts': 'all_posts',
            'questions': 'questions',
            'answers': 'answers',
            'edits': 'log'
        }
        for attribute, suffix in attributes_to_href_suffix.iteritems():
            try:
                user_dict[attribute] = get_count_for_user_href(soup, user, suffix)
            except:
                pass
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
            dict['activity'].append(parse_feed_item(entry))
        return dict