# -*- Mode: Python; test-case-name: testsuite.test_probe -*-
# vi:si:et:sw=4:sts=4:ts=4

import sys
from common import gst, unittest

class ProbeTest(unittest.TestCase):
    def testWrongNumber(self):
        self.assertRaises(TypeError, gst.Probe, True)

    def testWrongType(self):
        # bool is int type
        self.assertRaises(TypeError, gst.Probe, "noint", lambda x: "x")
        # second arg should be callable
        self.assertRaises(TypeError, gst.Probe, True, "nocallable")

    def testPerformNoData(self):
        probe = gst.Probe(True, self._probe_callback, "yeeha")
        self.assertRaises(TypeError, probe.perform, None)
        self.assertRaises(TypeError, probe.perform, "nodata")

    def testPerform(self):
        probe = gst.Probe(True, self._probe_callback, "yeeha")
        buffer = gst.Buffer()
        probe.perform(buffer)
        self.assertEqual(self._probe_result, "yeeha")

    def _probe_callback(self, probe, data, result):
        self._probe_result = result
        return True
   
if __name__ == "__main__":
    unittest.main()
