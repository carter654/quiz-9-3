from main import EngagementEngine
import unittest

class TestEngagementEngine(unittest.TestCase):

    def setUp(self):
        self.engine = EngagementEngine("test_user")
        self.verified_engine = EngagementEngine("verified_user", verified=True)

    # process_interaction tests
    def test_like(self):
        self.assertTrue(self.engine.process_interaction("like"))
        self.assertEqual(self.engine.score, 1)

    def test_comment(self):
        self.assertTrue(self.engine.process_interaction("comment"))
        self.assertEqual(self.engine.score, 5)

    def test_share(self):
        self.assertTrue(self.engine.process_interaction("share"))
        self.assertEqual(self.engine.score, 10)

    def test_invalid_type(self):
        self.assertFalse(self.engine.process_interaction("unknown"))

    def test_negative_count(self):
        with self.assertRaises(ValueError):
            self.engine.process_interaction("like", -1)

    def test_multiple_count(self):
        self.engine.process_interaction("like", 10)
        self.assertEqual(self.engine.score, 10)

    def test_verified_multiplier(self):
        self.verified_engine.process_interaction("like", 10)
        self.assertEqual(self.verified_engine.score, 15)

    def test_zero_count(self):
        self.engine.process_interaction("like", 0)
        self.assertEqual(self.engine.score, 0)

    # get_tier tests
    def test_tier_newbie(self):
        self.assertEqual(self.engine.get_tier(), "Newbie")

    def test_tier_influencer(self):
        self.engine.score = 100
        self.assertEqual(self.engine.get_tier(), "Influencer")

    def test_tier_influencer_boundary(self):
        self.engine.score = 1000
        self.assertEqual(self.engine.get_tier(), "Influencer")

    def test_tier_icon(self):
        self.engine.score = 1001
        self.assertEqual(self.engine.get_tier(), "Icon")

    # apply_penalty tests
    def test_penalty_reduces_score(self):
        self.engine.score = 100
        self.engine.apply_penalty(1)
        self.assertEqual(self.engine.score, 80)

    def test_penalty_floor_zero(self):
        self.engine.score = 10
        self.engine.apply_penalty(10)
        self.assertEqual(self.engine.score, 0)

    def test_penalty_removes_verified(self):
        self.verified_engine.apply_penalty(11)
        self.assertFalse(self.verified_engine.verified)

    def test_penalty_no_verified_removal_below_threshold(self):
        self.verified_engine.apply_penalty(10)
        self.assertTrue(self.verified_engine.verified)

unittest.main(argv=[''], exit=False, verbosity=2)