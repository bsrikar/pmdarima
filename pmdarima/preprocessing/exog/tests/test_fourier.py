# -*- coding: utf-8 -*-

import numpy as np
from numpy.testing import assert_array_almost_equal

from pmdarima.preprocessing.exog import FourierFeaturizer
import pmdarima as pm


class TestFourierREquivalency:

    # The following R code is what we want to reproduce:
    #   > set.seed(99)
    #   > n = 20
    #   > m = 5
    #   > y <- ts(rnorm(n) + (1:n)%%100/30, f=m)
    #   > library(forecast)
    #   > exog = fourier(y, K=2)
    #   > head(exog, 2)
    #             S1-5      C1-5       S2-5      C2-5
    #   [1,] 0.9510565  0.309017  0.5877853 -0.809017
    #   [2,] 0.5877853 -0.809017 -0.9510565  0.309017

    def test_r_equivalency(self):
        y = pm.c(
            0.24729584, 0.54632480, 0.18782870, 0.57719184, -0.19617125,
            0.32267403, -0.63051185, 0.75629093, -0.06411691, -0.96090867,
            -0.37910238, 1.32155036, 1.18338768, -2.04188735, -2.54093410,
            0.53359913, 0.17264767, -1.14502766, 1.13196478, 0.93762046)

        expected = np.array([
            [0.9510565, 0.309017, 0.5877853, -0.809017],
            [0.5877853, -0.809017, -0.9510565, 0.309017],
            [-0.5877853, -0.809017, 0.9510565, 0.309017],
            [-0.9510565, 0.309017, -0.5877853, -0.809017],
            [0.0000000, 1.000000, 0.0000000, 1.000000],
            [0.9510565, 0.309017, 0.5877853, -0.809017],
            [0.5877853, -0.809017, -0.9510565, 0.309017],
            [-0.5877853, -0.809017, 0.9510565, 0.309017],
            [-0.9510565, 0.309017, -0.5877853, -0.809017],
            [0.0000000, 1.000000, 0.0000000, 1.000000],
            [0.9510565, 0.309017, 0.5877853, -0.809017],
            [0.5877853, -0.809017, -0.9510565, 0.309017],
            [-0.5877853, -0.809017, 0.9510565, 0.309017],
            [-0.9510565, 0.309017, -0.5877853, -0.809017],
            [0.0000000, 1.000000, 0.0000000, 1.000000],
            [0.9510565, 0.309017, 0.5877853, -0.809017],
            [0.5877853, -0.809017, -0.9510565, 0.309017],
            [-0.5877853, -0.809017, 0.9510565, 0.309017],
            [-0.9510565, 0.309017, -0.5877853, -0.809017],
            [0.0000000, 1.000000, 0.0000000, 1.000000],
        ])

        trans = FourierFeaturizer(m=5, k=2).fit(y)
        _, xreg = trans.transform(y)
        assert_array_almost_equal(expected, xreg)


def test_hyndman_blog():
    # This is the exact code Hyndman ran in his blog post on the matter:
    # https://robjhyndman.com/hyndsight/longseasonality/
    n = 2000
    m = 200
    y = np.random.RandomState(1).normal(size=n) + \
        (np.arange(1, n + 1) % 100 / 30)

    trans = FourierFeaturizer(m=m, k=5).fit(y)
    _, xreg = trans.transform(y)

    arima = pm.auto_arima(y, exogenous=xreg, seasonal=False)  # type: pm.ARIMA

    # Show we can forecast 10 in the future
    _, xreg_test = trans.transform(y, n_periods=10)
    arima.predict(n_periods=10, exogenous=xreg_test)