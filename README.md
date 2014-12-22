# pyquora
[![Build Status](https://travis-ci.org/csu/pyquora.svg?branch=master)](https://travis-ci.org/csu/pyquora)  [![Latest Version](https://pypip.in/version/quora/badge.svg)](https://pypi.python.org/pypi/quora/)

A Python module to fetch and parse data from Quora.

### Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Contribute](#contribute)

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

# do stuff with the parsed activity data
activity.upvotes
activity.user_follows
activity.want_answers
activity.answers
activity.review_requests

# get user statistics
stats = quora.get_user_stats('Christopher-J-Su')

# take a gander
print stats
```

## Features
### Currently implemented
* User statistics
* User activity

### Todo
* Questions and answers
* Detailed user information (followers, following, etc.; not just statistics)

## Projects using `pyquora`
* [`quora-api`](https://github.com/csu/quora-api) – A REST API for Quora.
* [`quora-backup`](https://github.com/csu/quora-backup) – A Python package and CLI for backing up Quora data.

## Contribute
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/csu/pyquora?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Check out the issues on GitHub and/or make a pull request to contribute!