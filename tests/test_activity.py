from quora import User

class TestActivity:
    test_activities = []
    test_activities.append(User('Christopher-J-Su').activity)
    test_activities.append(User('Aaron-Ounn').activity)

    def test_activity(self):
        for activity in self.test_activities:
            assert activity['activity']

    # TODO: add tests to ensure that all fields in all types of activity are valid