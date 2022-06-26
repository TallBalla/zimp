
import unittest

import unittest

from tests.gameUnittests import GameTestMethods
from tests.playerUnittests import PlayerTestMethods
from tests.tileUnittests import TileTestMethods
from triggerAttackBranchTests import TriggerAttackBranchTests
from tests.triggerDevCardBranchTests import TriggerDevCardBranchTests


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TriggerAttackBranchTests())
    suite.addTest(TriggerDevCardBranchTests())

    suite.addTest(PlayerTestMethods())
    suite.addTest(GameTestMethods())
    suite.addTest(TileTestMethods())
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())


