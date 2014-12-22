from quora import Quora, Activity
from nose import with_setup

class TestActivity:
    q = Quora()
    activity1 = q.get_activity('Christopher-J-Su')
    activity2 = q.get_activity('Aaron-Ounn')
    test_activities = [activity1, activity2]

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_activity_answers(self):
        for activity in self.test_activities:
            assert activity.answers
            assert activity.answers

    def test_activity_want_answers(self):
        for activity in self.test_activities:
            assert activity.want_answers
            assert activity.want_answers

    def test_activity_user_follows(self):
        for activity in self.test_activities:
            assert activity.user_follows
            assert activity.user_follows

    def test_activity_upvotes(self):
        for activity in self.test_activities:
            assert activity.user_follows
            assert activity.user_follows