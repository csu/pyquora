from quora import User

expected_user_stat_keys = ['answers',
                           'edits',
                           'followers',
                           'following',
                           'questions',
                           'name',
                           'username']

class TestUserStatistics:
    test_stats = []
    test_stats.append(User('Christopher-J-Su').stats)
    # TODO: add tests for nonexistent users and other edge cases

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
