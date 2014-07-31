# quora

A Python module to fetch and parse data from Quora.

### Note: pyquora is currently broken because of the recent Quora UI change! Fix coming soon. - July 31, 2014

## Installation
You will need [Python 2](https://www.python.org/download/). [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

Install using pip:

    pip install quora

## Usage

    from quora import Quora, Activity

    quora = new Quora()
    activity = get_activity('Christopher-J-Su')

    # do stuff with the parsed data
    activity.answers
    activity.questions
    activity.upvotes
    activity.question_follows

## Features
### Currently implemented
* User statistics
* User activity
    * Broken down into answers, questions, votes, user follows, and question follows

### Todo
* Questions and answers
* Detailed user information (followers, following, etc.; not just statistics)
* Unit tests