from quora import Quora, Activity
from nose import with_setup

expected_user_stat_keys = ['answers',
                            'edits',
                            'followers',
                            'following',
                            'questions',
                            'name',
                            'username'
                            ]

class TestUserStatistics:
    q = Quora()
    test_stats = []

    stats1 = q.get_user_stats('Christopher-J-Su')
    test_stats.append(stats1)

    # stats2 = q.get_user_stats('Aaron-Ounn')
    # test_stats.append(stats2)

    # stats3 = q.get_user_stats('Elynn-Lee')
    # test_stats.append(stats3)

    # stats4 = q.get_user_stats('Jennifer-Apacible-1')
    # test_stats.append(stats4)

    # todo: add tests for nonexistant users and other edge cases

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_exists(self):
        for stat in self.test_stats:
            for key in expected_user_stat_keys:
                assert stat[key]

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
