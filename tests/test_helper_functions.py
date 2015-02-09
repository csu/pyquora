import quora

def test_try_cast_int():
	assert quora.try_cast_int('200 Upvotes') == 200
	assert quora.try_cast_int('2k Upvotes') == 2000
	assert quora.try_cast_int('2 K Upvotes') == 2000
	assert quora.try_cast_int('2.3k Upvotes') == 2300
	assert quora.try_cast_int('2.3 K Upvotes') == 2300
	assert quora.try_cast_int('<span class="count">3</span>') == 3

test_try_cast_int()