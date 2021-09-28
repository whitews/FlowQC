"""
Unit tests for FlowQC
"""
import unittest
import numpy as np
from flowkit import Sample


class QCTestCase(unittest.TestCase):
    def test_filter_anomalous_events(self):
        # there are 2 negative SSC-A events in this file (of 65016 total events)
        fcs_file_path = "flowqc/tests/test_data/100715.fcs"
        sample = Sample(fcs_path_or_data=fcs_file_path)
        sample.subsample_events(50000)
        sample.filter_anomalous_events(reapply_subsample=False)

        # using the default seed, the 2 negative events are in the subsample
        common_idx = np.intersect1d(sample.subsample_indices, sample.anomalous_indices)
        self.assertGreater(len(common_idx), 0)

        sample.filter_anomalous_events(reapply_subsample=True)
        common_idx = np.intersect1d(sample.subsample_indices, sample.anomalous_indices)
        self.assertEqual(len(common_idx), 0)

        self.assertGreater(sample.anomalous_indices.shape[0], 0)
