#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2017 Juan Cabral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# =============================================================================
# FUTURE
# =============================================================================

from __future__ import unicode_literals


# =============================================================================
# DOC
# =============================================================================

__doc__ = """FATS to feets compatibility testing"""


# =============================================================================
# IMPORTS
# =============================================================================

import os

import numpy as np

from .. import FeatureSpace, MPFeatureSpace, datasets

from .core import FeetsTestCase


# =============================================================================
# BASE CLASS
# =============================================================================

class FATSRegressionTestCase(FeetsTestCase):

    FeatureSpaceClass = FeatureSpace

    def setUp(self):
        # the paths
        self.data_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "data")
        self.FATS_result_path = os.path.join(self.data_path, "FATS_result.npz")

        self.lc = datasets.load_macho_example()

        # recreate the FATS result
        with np.load(self.FATS_result_path) as npz:
            self.features = npz["features"]
            self.features = self.features.astype("U")
            self.FATS_result = dict(zip(self.features, npz["values"]))

        # creates an template for all error, messages
        self.err_template = ("Feature '{feature}' missmatch.")

    def exclude_value_feature_evaluation(self, feature):
        return (
            "_harmonics_" in feature or
            feature in ["PeriodLS", "Period_fit", "Psi_CS", "Psi_eta"])

    def assertFATS(self, feets_result):
        for feature in self.features:
            if feature not in feets_result:
                self.fail("Missing feature {}".format(feature))
            if self.exclude_value_feature_evaluation(feature):
                continue
            feets_value = feets_result[feature]
            FATS_value = self.FATS_result[feature]
            err_msg = self.err_template.format(feature=feature)
            self.assertAllClose(feets_value, FATS_value, err_msg=err_msg)

    def test_FATS_to_feets_extract_one(self):
        fs = self.FeatureSpaceClass()
        result = fs.extract_one(self.lc)
        feets_result = dict(zip(*result))
        self.assertFATS(feets_result)

    def test_FATS_to_feets_extract(self):
        fs = self.FeatureSpaceClass()
        rfeatures, rdatas = fs.extract([self.lc] * 3)
        for result in rdatas:
            feets_result = dict(zip(rfeatures, result))
            self.assertFATS(feets_result)
        self.assertEqual(len(rdatas), 3)


class MPFATSRegressionTestCase(FATSRegressionTestCase):

    FeatureSpaceClass = MPFeatureSpace
