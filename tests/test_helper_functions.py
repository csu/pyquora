import nose
from quora import try_cast_int

def test_try_cast_int():
	assert try_cast_int('200 Upvotes') == 200
	assert try_cast_int('2k Upvotes') == 2000
	assert try_cast_int('2 K Upvotes') == 2000
	assert try_cast_int('2.3k Upvotes') == 2300
	assert try_cast_int('2.3 K Upvotes') == 2300
