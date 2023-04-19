from unittest import TestCase, main
from whiteboard import candies
class MatchTestCase(TestCase):
    def test_example_one(self):
        self.assertEqual(candies([5,8,6,4]), 9)
    def test_example_two(self):
        self.assertEqual(candies([1,2,4,6]), 11)
    def test_multi(self):
        self.assertEqual(candies([10,20,30,11]),49 )
    def test_all_but_one(self):
        self.assertEqual(candies([0,0,0,0,1]),4)
if __name__ == '__main__':
    main()








