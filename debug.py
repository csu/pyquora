from pyquora import Quora, Activity

activity = Quora.get_activity('Christopher-J-Su')
print activity.answers
print activity.question_follows
print activity.user_follows
print activity.upvotes
print activity.questions