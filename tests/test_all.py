import quora

class TestActivity:

    @classmethod
    def setup_class(cls):
        self.quora = Quora()
        self.activity1 = quora.get_activity('Christopher-J-Su')
        self.activity2 = quora.get_activity('Aaron-Ounn')
        self.activity3 = quora.get_activity('Jennifer-Apacible-1')

    def test_activity_answers(self):
        assert self.activity1.answers
        assert self.activity2.answers
        assert self.activity3.answers

    def test_activity_want_answers(self):
        assert self.activity1.want_answers
        assert self.activity2.want_answers
        assert self.activity3.want_answers