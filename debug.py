from quora import Quora, Activity

quora = Quora()
stats = quora.get_user_stats('Christopher-J-Su')
# activity = quora.get_activity('Christopher-J-Su')
# print activity.answers
# print activity.question_follows
# print activity.user_follows
# print activity.upvotes
# print activity.questions
print stats
# print quora.get_activity_keys()
