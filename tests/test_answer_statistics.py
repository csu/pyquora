#coding=utf-8

from bs4 import BeautifulSoup
from nose import with_setup
from quora import Quora

EXPECTED_STATS_1 = {'want_answers': 75,
    'views': 195,
    'author': u'Mayur-P-R-Rohith',
    'question_link': u'http://www.quora.com/What-are-some-mistakes-you-noticed-on-Friends',
    'comment_count': 1,
    'answer': '<div id="__w2_ri9P9zc_container">S4E20:<br/><br/>Notice the whiteboard.<br/><div><img class="landscape qtext_image zoomable_in zoomable_in_feed" master_h="768" master_src="http://qph.is.quoracdn.net/main-qimg-5f49eaf19b138cd9df79cffe5b727869?convert_to_webp=true" master_w="1366" src="http://qph.is.quoracdn.net/main-qimg-5c869ecdfd33c35392a4de2e72f4c05f?convert_to_webp=true"/></div>10:02- "get out"<br/><br/><div><img class="landscape qtext_image zoomable_in zoomable_in_feed" master_h="768" master_src="http://qph.is.quoracdn.net/main-qimg-5bef87d5441e2b640d781fb955b9ca95?convert_to_webp=true" master_w="1366" src="http://qph.is.quoracdn.net/main-qimg-3cecd38e3f868ab419fd47978ba1ce70?convert_to_webp=true"/></div>10:21- "Poop"<br/><br/><div><img class="landscape qtext_image zoomable_in zoomable_in_feed" master_h="768" master_src="http://qph.is.quoracdn.net/main-qimg-318c3847fe38bc356cc50c744930b9cf?convert_to_webp=true" master_w="1366" src="http://qph.is.quoracdn.net/main-qimg-91cb8136c6b29b9955cbc17abd1bfdfe?convert_to_webp=true"/></div>10:36- "Poop"<br/><br/><div><img class="landscape qtext_image zoomable_in zoomable_in_feed" master_h="768" master_src="http://qph.is.quoracdn.net/main-qimg-8b382517079a9767f42559733c6e3ffe?convert_to_webp=true" master_w="1366" src="http://qph.is.quoracdn.net/main-qimg-a755dc574444bf46927bf81ccb279f6b?convert_to_webp=true"/></div>10:43- "get out"<div class="container_boundary" id="__w2_ri9P9zc_container_boundary" style="margin:0px; padding:0px; height:0px; width:0px;"></div></div>',
    'upvote_count': 3,
    }

class TestAnswerScraper:

    def test_correct(self):
        q = Quora()
        stats1 = q.scrape_one_answer(BeautifulSoup(open('tests/input_files/answer_1')))

        assert stats1 == EXPECTED_STATS_1
