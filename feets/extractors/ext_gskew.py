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

__doc__ = """"""


# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np

from .core import Extractor


# =============================================================================
# EXTRACTOR CLASS
# =============================================================================

class Gskew(Extractor):
    """Median-based measure of the skew"""

    data = ['magnitude']
    features = ["Gskew"]

    def fit(self, magnitude):
        median_mag = np.median(magnitude)
        F_3_value = np.percentile(magnitude, 3)
        F_97_value = np.percentile(magnitude, 97)

        skew = (np.median(magnitude[magnitude <= F_3_value]) +
                np.median(magnitude[magnitude >= F_97_value]) - 2 * median_mag)
        return {"Gskew": skew}
