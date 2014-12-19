# quora

A Python module to fetch and parse data from Quora.

### Projects built using pyquora
* [`quora-api`](https://github.com/csu/quora-api) – A REST API for Quora.
* [`quora-backup`](https://github.com/csu/quora-backup) – A Python package and CLI for backing up Quora data.

## Installation
You will need [Python 2](https://www.python.org/download/). [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

Install using pip:

    pip install quora

## Usage

```python
from quora import Quora, Activity

quora = new Quora()

# get user activity
activity = get_activity('Christopher-J-Su')

# do stuff with the parsed data
activity.upvotes = upvotes
activity.user_follows
activity.want_answers
activity.answers

# get user statistics
stats = quora.get_user_stats('Christopher-J-Su')

# take a gander
print stats
```

## Features
### Currently implemented
* User statistics
* User activity
    * Broken down into answers, questions, votes, user follows, and question follows

### Todo
* Questions and answers
* Detailed user information (followers, following, etc.; not just statistics)
* Unit tests

## Related Projects
* [quora-api](https://github.com/csu/quora-api)
* [quora-backup](https://github.com/csu/quora-backup)