from quora import Quora, Activity
from nose import with_setup

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