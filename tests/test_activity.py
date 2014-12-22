from quora import Quora, Activity
from nose import with_setup

class TestActivity:
    q = Quora()
    activity1 = q.get_activity('Christopher-J-Su')
    activity2 = q.get_activity('Aaron-Ounn')

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_activity_answers(self):
        assert self.activity1.answers
        assert self.activity2.answers

    def test_activity_want_answers(self):
        assert self.activity1.want_answers
        assert self.activity2.want_answers

    def test_activity_user_follows(self):
        assert self.activity1.user_follows
        assert self.activity2.user_follows

    def test_activity_upvotes(self):
        assert self.activity1.upvotes
        assert self.activity2.upvotes