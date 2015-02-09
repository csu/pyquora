from bs4 import BeautifulSoup
import re
import requests

####################################################################
# Helpers
####################################################################
def try_cast_int(s):
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
	question_link = soup.find('a', attrs = {'class' : 'question_link'})
	return 'http://www.quora.com' + question_link.get('href')

def get_author(soup):
	raw_author = soup.find('div', attrs = {'class' : 'author_info'}).next.get('href')
	author = raw_author.split('/')[-1]
	return author

def extract_username(username):
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
    @staticmethod
    def get_one_answer(question, author=None):
        if author is None: # For short URL's
            if re.match('http', question): # question like http://qr.ae/znrZ3
                soup = BeautifulSoup(requests.get(question).text)
            else: # question like znrZ3
                soup = BeautifulSoup(requests.get('http://qr.ae/' + question).text)
        else:
            soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/answer/' + author).text)
        return Quora.scrape_one_answer(soup)

    @staticmethod
    def scrape_one_answer(soup):
    	answer = soup.find('div', id = re.compile('_answer_content$')).find('div', id = re.compile('_container'))
        question_link = get_question_link(soup)
        author = get_author(soup)
        views = soup.find('span', attrs = {'class' : 'stats_row'}).next.next.next.next
        want_answers = soup.find('span', attrs = {'class' : 'count'}).string

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

        answer_stats = map(try_cast_int, [views, want_answers, upvote_count, comment_count])

        answer_dict = {'views' : answer_stats[0],
                       'want_answers' : answer_stats[1],
                       'upvote_count' : answer_stats[2],
                       'comment_count' : answer_stats[3],
                       'answer' : str(answer),
                       'question_link' : question_link,
                       'author' : author
        }
        return answer_dict

    @staticmethod
    def get_latest_answers(question):
    	soup = BeautifulSoup(requests.get('http://www.quora.com/' + question + '/log').text)
    	authors =  Quora.scrape_latest_answers(soup)
    	return [Quora.get_one_answer(question, author) for author in authors]

    @staticmethod
    def scrape_latest_answers(soup):
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

    @staticmethod
    def get_question_stats(question):
        soup = BeautifulSoup(requests.get('http://www.quora.com/' + question).text)
        return Quora.scrape_question_stats(soup)

    @staticmethod
    def scrape_question_stats(soup):
        raw_topics = soup.find_all('span', attrs={'itemprop' : 'title'})
        topics = []
        for topic in raw_topics:
            topics.append(topic.string)

        want_answers = soup.find('span', attrs={'class' : 'count'}).string
        answer_count = soup.find('div', attrs={'class' : 'answer_count'}).next.split()[0]
        question_text = list(soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1').children)[-1]
        question_details = soup.find('div', attrs = {'class' : 'question_details_text'})
        answer_wiki = soup.find('div', attrs = {'class' : 'AnswerWikiArea'}).find('div')

        question_dict = {'want_answers' : try_cast_int(want_answers),
                         'answer_count' : try_cast_int(answer_count),
                         'question_text' : question_text.string,
                         'topics' : topics,
                         'question_details' : str(question_details),
                         'answer_wiki' : str(answer_wiki),
                        }
        return question_dict

    ### Legacy API
    @staticmethod
    def get_user_stats(u):
        from user import User
        user = User()
        return user.get_user_stats(u)

    @staticmethod
    def get_user_activity(u):
        from user import User
        user = User()
        return user.get_user_activity(u)

    @staticmethod
    def get_activity(u):
        from user import User
        user = User()
        return user.get_activity(u)
