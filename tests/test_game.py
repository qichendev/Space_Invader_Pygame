import unittest

class TestGame(unittest.TestCase):

    def test_score(self):
        score = 0
        score += 10
        self.assertEqual(score, 10)

    def test_lives(self):
        lives = 3
        lives -= 1
        self.assertEqual(lives, 2)

if __name__ == "__main__":
    unittest.main()