from quora import Quora, Activity
from nose import with_setup

class TestActivity:
    quoraObj = Quora()
    activity1 = quoraObj.get_activity('Christopher-J-Su')
    activity2 = quoraObj.get_activity('Aaron-Ounn')
    activity3 = quoraObj.get_activity('Jennifer-Apacible-1')

    @classmethod
    def setup_class(cls):
        print "Setup here"

    def test_activity_answers(self):
        assert self.activity1.answers
        assert self.activity2.answers
        assert self.activity3.answers

    def test_activity_want_answers(self):
        assert self.activity1.want_answers
        assert self.activity2.want_answers
        assert self.activity3.want_answers