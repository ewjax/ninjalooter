from ninjalooter import models
from ninjalooter.tests import base


class TestModels(base.NLTestBase):
    def test_Auction_base_model(self):
        auc = models.Auction('COPPER DISC')
        self.assertRaises(NotImplementedError, auc.add, 1, 'Jim')
        self.assertRaises(NotImplementedError, auc.highest)

    def test_DKPAuction_model(self):
        auc = models.DKPAuction('COPPER DISC')
        self.assertIsNone(auc.highest())

        # First bid, valid
        result = auc.add(10, 'Peter')
        self.assertTrue(result)
        self.assertEqual(1, len(auc.highest()))
        self.assertIn(('Peter', 10), auc.highest())

        # Second bid, lower than first bid
        result = auc.add(8, 'Paul')
        self.assertFalse(result)
        self.assertEqual(1, len(auc.highest()))
        self.assertIn(('Peter', 10), auc.highest())

        # Third bid, higher than first bid
        result = auc.add(12, 'Mary')
        self.assertTrue(result)
        self.assertEqual(1, len(auc.highest()))
        self.assertIn(('Mary', 12), auc.highest())

        # Fourth bid, tied with highest bid
        result = auc.add(12, 'Dan')
        self.assertFalse(result)
        self.assertEqual(1, len(auc.highest()))
        self.assertIn(('Mary', 12), auc.highest())

        # Invalid bid
        result = auc.add(None, 'Fred')
        self.assertFalse(result)

    def test_RandomAuction_model(self):
        auc = models.RandomAuction('COPPER DISC')
        self.assertIsNone(auc.highest())

        # First roll, valid
        result = auc.add(10, 'Peter')
        self.assertTrue(result)
        self.assertEqual(1, len(tuple(auc.highest())))
        self.assertIn(('Peter', 10), tuple(auc.highest()))

        # Second roll, lower than first roll
        result = auc.add(8, 'Paul')
        self.assertTrue(result)
        self.assertEqual(1, len(tuple(auc.highest())))
        self.assertIn(('Peter', 10), tuple(auc.highest()))

        # Third roll, higher than first roll
        result = auc.add(12, 'Mary')
        self.assertTrue(result)
        self.assertEqual(1, len(tuple(auc.highest())))
        self.assertIn(('Mary', 12), tuple(auc.highest()))

        # Fifth roll, player rolls a second time
        result = auc.add(18, 'Paul')
        self.assertFalse(result)
        self.assertEqual(1, len(tuple(auc.highest())))
        self.assertIn(('Mary', 12), tuple(auc.highest()))

        # Fifth roll, tied with highest roll
        result = auc.add(12, 'Dan')
        self.assertTrue(result)
        self.assertEqual(2, len(tuple(auc.highest())))
        self.assertIn(('Mary', 12), tuple(auc.highest()))
        self.assertIn(('Dan', 12), tuple(auc.highest()))

        # Invalid roll
        result = auc.add(None, 'Fred')
        self.assertFalse(result)

        # All rolls should be tracked
        self.assertDictEqual(
            {'Dan': 12, 'Mary': 12, 'Paul': 8, 'Peter': 10},
            auc.rolls)
