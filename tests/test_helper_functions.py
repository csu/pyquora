import quora

class TestHelperFunctions:
    def test_try_cast_int(self):
        input_strings = ['200 Upvotes',
                        '2k Upvotes',
                        '2 K Upvotes',
                        '2.3k Upvotes',
                        '2.3 K Upvotes',
                        '<span class="count">3</span>'
                        ]
        expected = [200, 2000, 2000, 2300, 2300, 3]

        for i in range(0, len(input_strings)):
            assert quora.try_cast_int(input_strings[i]) == expected[i]