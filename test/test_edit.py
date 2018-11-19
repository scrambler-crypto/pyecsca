from unittest import TestCase

import numpy as np

from pyecsca import Trace, trim, reverse, pad


class EditTests(TestCase):

    def setUp(self):
        self._trace = Trace(None, None, np.array([10, 20, 30, 40, 50], dtype=np.dtype("i1")))

    def test_trim(self):
        result = trim(self._trace, 2)
        self.assertIsNotNone(result)
        np.testing.assert_equal(result.samples, np.array([30, 40, 50], dtype=np.dtype("i1")))

    def test_reverse(self):
        result = reverse(self._trace)
        self.assertIsNotNone(result)
        np.testing.assert_equal(result.samples,
                                np.array([50, 40, 30, 20, 10], dtype=np.dtype("i1")))

    def test_pad(self):
        result = pad(self._trace, 2)
        self.assertIsNotNone(result)
        np.testing.assert_equal(result.samples,
                                np.array([0, 0, 10, 20, 30, 40, 50, 0, 0], dtype=np.dtype("i1")))
