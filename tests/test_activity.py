from quora import User

class TestActivity:
    test_activities = []
    test_activities.append(User('Christopher-J-Su').activity)
    test_activities.append(User('Aaron-Ounn').activity)

    def test_activity_answers(self):
        for activity in self.test_activities:
            assert activity.answers

    def test_activity_want_answers(self):
        for activity in self.test_activities:
            assert activity.want_answers

    def test_activity_user_follows(self):
        for activity in self.test_activities:
            assert activity.user_follows

    def test_activity_upvotes(self):
        for activity in self.test_activities:
            assert activity.user_follows

    # TODO: add tests to ensure that all fields in all types of activity are valid