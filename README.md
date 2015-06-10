# pyquora
#### Note: this library is currently broken due to changes on Quora's end. Issues and pull requests are welcome.

[![Build Status](https://travis-ci.org/csu/pyquora.svg?branch=master)](https://travis-ci.org/csu/pyquora)

A Python module to fetch and parse data from Quora.

### Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Contribute](#contribute)
* [Projects using `pyquora`](#projects-using-pyquora)

## Installation
You will need [Python 2](https://www.python.org/download/). [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

Install using pip:

    pip install quora

## Usage

### User statistics

```python
from quora import User

user = User('Christopher-J-Su')

# Get user activity
activity = user.activity

# Do stuff with the parsed activity data
print activity

# Get user statistics
stats = user.stats

# Take a gander
print stats
```

### Questions
```python
from quora import Quora

# Get question statistics
question = Quora.get_question_stats('what-is-python')

# question is:
# {
#     'want_answers': 3,
#     'question_text': u'What is python?', 
#     'topics': [u'Science, Engineering, and Technology', u'Technology', u'Electronics', u'Computers'], 
#     'question_details': None, 'answer_count': 1, 
#     'answer_wiki': '<div class="hidden" id="answer_wiki"><div id="ld_mqcfmt_15628"><div id="__w2_po3p1uM_wiki"></div></div></div>',
# }
```

### Answer statistics
```python
from quora import Quora

# The function can be called in any of the following ways.
answer = Quora.get_one_answer('http://qr.ae/6hARL')
answer = Quora.get_one_answer('6hARL')
answer = Quora.get_one_answer(question, author) # question and answer are variables

# answer is:
# {
#     'want_answers': 8, 
#     'views': 197, 
#     'author': u'Mayur-P-R-Rohith', 
#     'question_link': u'https://www.quora.com/Does-Quora-similar-question-search-when-posing-a-new-question-work-better-than-the-search-box-ove', 
#     'comment_count': 1, 
#     'answer': '...', 
#     'upvote_count': 5
# }

# Get the latest answers from a question
latest_answers = Quora.get_latest_answers('what-is-python')
```

## Features
### Currently implemented
* User statistics
* User activity
* Question statistics
* Answer statistics

### Todo
* Detailed user information (followers, following, etc.; not just statistics)

## Contribute
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/csu/pyquora?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)   [![HuBoard](http://img.shields.io/badge/Hu-Board-7965cc.svg)](https://huboard.com/csu/pyquora/)

Check out the issues on GitHub and/or make a pull request to contribute!

## Projects using `pyquora`
* [`quora-api`](https://github.com/csu/quora-api) – A REST API for Quora.
* [`quora-backup`](https://github.com/csu/quora-backup) – A Python package and CLI for backing up Quora data.
