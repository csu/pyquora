from quora import Quora, Activity
from nose import with_setup

class TestUserStatistics:
    q = Quora()
    stats1 = q.get_user_stats('Christopher-J-Su')
    stats2 = q.get_user_stats('Aaron-Ounn')
    stats3 = q.get_user_stats('Elynn-Lee')
    stats4 = q.get_user_stats('Jennifer-Apacible-1')
    test_stats = [stats1, stats2, stats3, stats4]

    # todo: add tests for nonexistant users and other edge cases

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_exists(self):
        for stat in self.test_stats:
            assert stat['answers']
            assert stat['edits']
            assert stat['followers']
            assert stat['following']
            assert stat['questions']
            assert stat['name']
            assert stat['username']

    def test_type(self):
        for stat in self.test_stats:
            assert isinstance(stat['answers'], (int, long))
            assert isinstance(stat['edits'], (int, long))
            assert isinstance(stat['followers'], (int, long))
            assert isinstance(stat['following'], (int, long))
            assert isinstance(stat['posts'], (int, long))
            assert isinstance(stat['questions'], (int, long))
            assert isinstance(stat['name'], str)
            assert isinstance(stat['username'], str)
