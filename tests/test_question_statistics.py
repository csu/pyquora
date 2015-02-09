#coding=utf-8

from bs4 import BeautifulSoup
from nose import with_setup
from quora import Quora

EXPECTED_STATS_1 = {
    'want_answers': 1, 
    'question_text': u'Is there a proof of the Four Color Theorem that does not involve substantial computation?', 
    'topics': [u'Science, Engineering, and Technology', u'Science', u'Formal Sciences', u'Mathematics'], 
    'question_details': '<div class="question_details_text inline_editor_content">This is the full question: """The Four Colour Theorem is famous for being the first long-standing mathematical problem to be resolved using a computer program. The theorem was first conjectured in 1852 by Francis Guthrie, and after over a century of work by many famous mathematicians [36,28] (including De Morgan, Peirce, Hamilton, Cayley, Birkhoff, and Lebesgue), and many incorrect “proofs”, it was finally proved by Appel and Haken in 1976 [3]. This proof broke new ground because it involved using computer programs to carry out a gigantic case analysis, which could not, in any real sense, be performed by hand: it covered, quite literally, a billion cases."""... Can we thus say that the correctness of the proof depends on the correctness of the computer program which check all the billion cases… and that the correctness of the program guarantees the correct results for the billion+1th case…? This by itself constitutes a new proof technique(?), in which one can trust a computer program (or algorithm) and assume it correct as an axiom (the same way one assumes the truth of the 5-th postulate of Euclid)… This was my main issue the first time I came across this theorem and it still is… Any thoughts…? [This is my source: <span class="qlink_container"><a class="external_link" href="http://research.microsoft.com/en-us/um/people/gonthier/4colproof.pdf]" target="_blank">http://research.microsoft<wbr></wbr>.com/en...</a></span></div>', 
    'answer_count': 4, 
    'answer_wiki': '<div class="hidden" id="answer_wiki"><div id="ld_jqjkjx_2082"><div id="__w2_bZWlZkI_wiki"></div></div></div>'
    }

EXPECTED_STATS_2 = {
    'want_answers': 10, 
    'question_text': u'If space is 3 dimensional, can time also be 3 dimensional?', 
    'topics': [u'Science, Engineering, and Technology', u'Science', u'Physical Sciences', u'Physics', u'Theoretical Physics'], 
    'question_details': '<div class="question_details_text inline_editor_content"></div>', 
    'answer_count': 9, 
    'answer_wiki': '<div class="hidden" id="answer_wiki"><div id="ld_ibyjgu_158782"><div id="__w2_unO1fVs_wiki"></div></div></div>'
    }

class TestQuestionStatistics:
    q = Quora()
    stats1 = q.get_question_stats('If-space-is-3-dimensional-can-time-also-be-3-dimensional')
    stats2 = q.get_question_stats('I-need-a-summer-internship-but-I-dont-want-to-apply-because-theres-a-90-chance-Ill-get-rejected-What-should-I-do')
    stats3 = q.get_question_stats('What-are-the-best-intern-blog-posts-and-guides')
    stats4 = q.get_question_stats('What-data-structures-and-algorithms-should-one-implement-in-order-to-prepare-for-technical-interviews')
    test_stats = [stats1, stats2, stats3, stats4]

    # todo: add tests for nonexistant users and other edge cases

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_exists(self):
        for stat in self.test_stats:
            assert stat['answer_count']
            assert stat['topics']
            assert stat['want_answers']

    def test_type(self):
        for stat in self.test_stats:
            assert isinstance(stat['answer_count'], (int, long))
            assert isinstance(stat['want_answers'], (int, long))

class TestQuestionScraper:
    
    def test_correct(self):
        q = Quora()
        stats1 = q.scrape_question_stats(BeautifulSoup(open('tests/input_files/question_1')))
        stats2 = q.scrape_question_stats(BeautifulSoup(open('tests/input_files/question_2')))
        assert stats1 == EXPECTED_STATS_1
        assert stats2 == EXPECTED_STATS_2
        