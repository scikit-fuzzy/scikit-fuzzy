import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from random import randint
from skfuzzy.membership import trapmf
from skfuzzy.fuzzymath import (cartadd, cartprod, classic_relation, contrast,
                               interp10, maxmin_composition,
                               maxprod_composition, interp_membership,
                               relation_min, relation_product,
                               fuzzy_add, fuzzy_sub, fuzzy_min, fuzzy_mult,
                               fuzzy_div, fuzzy_compare, inner_product,
                               modus_ponens, outer_product, fuzzy_similarity, partial_dMF)


def test_cartadd():
    a = np.r_[0, 0, 0, 0.3, 0.7, 1, 0.9, 0]
    b = np.r_[0, 0, 1, 0.2, 0.1, 0, 0]
    z = cartadd(a, b)

    expected = np.r_[[[0. ,  0. ,  1. ,  0.2,  0.1,  0. ,  0. ],
                      [0. ,  0. ,  1. ,  0.2,  0.1,  0. ,  0. ],
                      [0. ,  0. ,  1. ,  0.2,  0.1,  0. ,  0. ],
                      [0.3,  0.3,  1.3,  0.5,  0.4,  0.3,  0.3],
                      [0.7,  0.7,  1.7,  0.9,  0.8,  0.7,  0.7],
                      [1. ,  1. ,  2. ,  1.2,  1.1,  1. ,  1. ],
                      [0.9,  0.9,  1.9,  1.1,  1. ,  0.9,  0.9],
                      [0. ,  0. ,  1. ,  0.2,  0.1,  0. ,  0. ]]]

    assert_allclose(z, expected)


def test_cartprod():
    a = np.r_[0, 0, 0, 0.3, 0.7, 1, 0.9, 0]
    b = np.r_[0, 0, 1, 0.2, 0.1, 0, 0]
    z = cartprod(a, b)

    expected = np.r_[[[0.,  0.,  0. ,  0. ,  0. ,  0.,  0.],
                      [0.,  0.,  0. ,  0. ,  0. ,  0.,  0.],
                      [0.,  0.,  0. ,  0. ,  0. ,  0.,  0.],
                      [0.,  0.,  0.3,  0.2,  0.1,  0.,  0.],
                      [0.,  0.,  0.7,  0.2,  0.1,  0.,  0.],
                      [0.,  0.,  1. ,  0.2,  0.1,  0.,  0.],
                      [0.,  0.,  0.9,  0.2,  0.1,  0.,  0.],
                      [0.,  0.,  0. ,  0. ,  0. ,  0.,  0.]]]

    assert_allclose(z, expected)


def test_classic_relation():
    a = np.r_[0, 0, 0, 0.3, 0.7, 1, 0.9, 0]
    b = np.r_[0, 0, 1, 0.2, 0.1, 0, 0]
    z = classic_relation(a, b)

    expected = np.r_[[[1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ],
                      [1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ],
                      [1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ],
                      [0.7,  0.7,  0.7,  0.7,  0.7,  0.7,  0.7],
                      [0.3,  0.3,  0.7,  0.3,  0.3,  0.3,  0.3],
                      [0. ,  0. ,  1. ,  0.2,  0.1,  0. ,  0. ],
                      [0.1,  0.1,  0.9,  0.2,  0.1,  0.1,  0.1],
                      [1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ]]]

    assert_allclose(z, expected)


def test_contrast():
    a = np.r_[0, 0, 0, 0.3, 0.7, 1, 0.9, 0]
    z = contrast(a, 1.8)

    # Legacy slower code which should produce identical result
    p = 1.8
    m = 0.5
    ymin = np.fmin(a, m)
    ymax = np.fmax(a, m)
    w = np.arange(len(a))
    wmax = w[ymax > m]
    wmin = w[ymax <= m]
    ymin = 2 ** (p - 1) * ymin ** p
    ymax = 1 - 2 ** (p - 1) * (1 - ymax) ** p
    ymin[wmax] = 0
    ymax[wmin] = 0

    assert_allclose(z, ymin + ymax)

    # Legacy slower code which should produce identical result
    p = 0.5
    m = 0.5
    z = contrast(a, 0.5)
    ymin = np.fmin(a, m)
    ymax = np.fmax(a, m)
    w = np.arange(len(a))
    wmax = w[ymax > m]
    wmin = w[ymax <= m]
    ymin = 2 ** (p - 1) * ymin ** p
    ymax = 1 - 2 ** (p - 1) * (1 - ymax) ** p
    ymin[wmax] = 0
    ymax[wmin] = 0

    assert_allclose(z, ymin + ymax)

    # Legacy slower code which should produce identical result
    p = 2.
    m = 0.5
    z = contrast(a, 2.)
    ymin = np.fmin(a, m)
    ymax = np.fmax(a, m)
    w = np.arange(len(a))
    wmax = w[ymax > m]
    wmin = w[ymax <= m]
    ymin = 2 ** (p - 1) * ymin ** p
    ymax = 1 - 2 ** (p - 1) * (1 - ymax) ** p
    ymin[wmax] = 0
    ymax[wmin] = 0

    assert_allclose(z, ymin + ymax)


def test_contrast_offcenter():
    a = np.r_[0, 0, 0, 0.3, 0.7, 1, 0.9, 0]
    z = contrast(a, 1.8, m=0.75)

    # Legacy slower code which produces correct results
    p = 1.8
    m = 0.75
    ymin = np.fmin(a, m)
    ymax = np.fmax(a, m)
    w = np.arange(len(a))
    wmax = w[ymax > m]
    wmin = w[ymax <= m]
    ymin = 2 ** (p - 1) * ymin ** p
    ymax = 1 - 2 ** (p - 1) * (1 - ymax) ** p
    ymin[wmax] = 0
    ymax[wmin] = 0

    assert_array_equal(z, ymin + ymax)


def test_fuzzy_add():
    x = np.r_[0:8]
    A = np.r_[0, .3, .6, .8, 1, .7, .2, 0]
    B = np.r_[0,  1, .9, .5, .2, .1, 0, 0]

    test_u, test_mf = fuzzy_add(x ** 2, A, x ** 2, B)
    expected_u = np.r_[0., 1., 2., 4., 5., 8., 9., 10., 13., 16., 17., 18.,
                       20., 25., 26., 29., 32., 34., 36., 37., 40., 41., 45.,
                       49., 50., 52., 53., 58., 61., 65., 72., 74., 85., 98.]
    expected_mf = np.r_[0., 0., 0.3, 0., 0.6, 0.6, 0., 0.8, 0.8, 0., 1., 0.5,
                        0.9, 0.5, 0.7, 0.7, 0.2, 0.5, 0., 0.2, 0.2, 0.2, 0.2,
                        0., 0.1, 0.2, 0., 0., 0.1, 0., 0., 0., 0., 0.]
    assert_allclose(test_u, expected_u)
    assert_allclose(test_mf, expected_mf)


def test_fuzzy_compare():
    pair = np.r_[[[1, 0.6, 0.7, 0.5],
                  [0.2, 1, 0.8, 0.6],
                  [0.3, 0.2, 1, 0.4],
                  [0.9, 0.5, 0.8, 1]]]

    test = fuzzy_compare(pair)
    expected = np.r_[[[63., 21., 27.  , 63. ],
                      [63., 63., 15.75, 52.5],
                      [63., 63., 63.  , 63. ],
                      [35., 63., 31.5 , 63. ]]] / 63.
    assert_allclose(test, expected)


def test_fuzzy_sub():
    x = np.r_[0:8]
    A = np.r_[0, .3, .6, .8, 1, .7, .2, 0]

    test_u, test_mf = fuzzy_sub(x, A, x, A)

    expected_u = np.r_[-7., -6., -5., -4., -3., -2., -1., 0., 1., 2., 3., 4.,
                       5., 6., 7.]
    expected_mf = np.r_[0., 0., 0.2, 0.3, 0.6, 0.7, 0.8, 1., 0.8, 0.7, 0.6,
                        0.3, 0.2, 0., 0.]
    assert_allclose(test_u, expected_u)
    assert_allclose(test_mf, expected_mf)


def test_fuzzy_min():
    x = np.r_[0:8]
    A = np.r_[0, .3, .6, .8, 1, .7, .2, 0]
    B = np.r_[0,  1, .9, .5, .2, .1, 0, 0]

    testu_, test_mf = fuzzy_min(x, A, x, B)

    expected_u = np.r_[0., 1., 2., 3., 4., 5., 6., 7.]
    expected_mf = np.r_[0., 1., 0.9, 0.5, 0.2, 0.1, 0., 0.]
    assert_allclose(testu_, expected_u)
    assert_allclose(test_mf, expected_mf)


def test_fuzzy_mult():
    vol  = np.r_[.5, .75, 1, 1.25, 1.5]
    V    = np.r_[0, .5, 1, .5, 0]
    pa   = np.r_[.5, 1.75, 2, 2.25, 2.5]
    P    = V.copy()

    test_u, test_mf = fuzzy_mult(pa, P, vol, V)
    expected_u = np.r_[0.25, 0.375, 0.5,0.625, 0.75, 0.875, 1., 1.125, 1.25,
                       1.3125, 1.5,1.6875, 1.75, 1.875, 2., 2.1875, 2.25, 2.5,
                       2.625, 2.8125, 3., 3.125, 3.375, 3.75]
    expected_mf = np.r_[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.5, 0.5, 0.5,
                        0.5, 0., 1., 0.5, 0.5, 0.5, 0., 0.5, 0., 0., 0., 0.]
    assert_allclose(test_u, expected_u)
    assert_allclose(test_mf, expected_mf)


def test_fuzzy_div():
    vol  = np.r_[.5, .75, 1, 1.25, 1.5]
    V    = np.r_[0, .5, 1, .5, 0]
    pa   = np.r_[.5, 1.75, 2, 2.25, 2.5]
    P    = V.copy()

    test_u, test_mf = fuzzy_div(pa, P, vol, V)
    expected_u = np.r_[2., 2.4, 3., 4., 6., 7., 8., 8.4, 9., 9.6, 10., 10.5,
                       10.8, 12., 13.5, 14., 15., 16., 18., 20., 21., 24.,
                       27., 30.] / 6.
    expected_mf = np.r_[0., 0., 0., 0., 0., 0., 0., 0.5, 0., 0.5, 0., 0.5,
                        0.5, 1., 0.5, 0.5, 0., 0.5, 0.5, 0., 0., 0., 0., 0.]
    assert_allclose(test_u, expected_u)
    assert_allclose(test_mf, expected_mf)


def test_inner_product():
    A = [0.3, 0.2, 0.1, 0, 0.7, 0.9, 1]
    B = [0.5, 0.5, 0.6, 0.4, 0.6, 0.3, 0.2]
    c = inner_product(A, B)
    assert_allclose(np.r_[c], np.r_[0.6])
    c = inner_product(np.asarray(A), np.asarray(B))
    assert_allclose(np.r_[c], np.r_[0.6])


def test_interp10():
    x = np.r_[0, 1, 0.5, 0.25]
    z = interp10(x)
    expected = np.r_[0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.,
        0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.475,
        0.45, 0.425, 0.4, 0.375,  0.35, 0.325,  0.3, 0.275,  0.25]

    # ~1e-16 float errors from interpolation
    assert_allclose(z, expected)


def test_maxmin_composition():
    mfI = np.r_[0.4, 0.7, 1.0, 0.8, 0.6]
    mfV = np.r_[0.2, 0.6, 1.0, 0.9, 0.7]
    mfC = np.r_[0.4, 1.0, 0.8]

    P = cartprod(mfV, mfI)
    S = cartprod(mfI, mfC)

    test = maxmin_composition(P, S)
    expected = np.r_[[[0.2,  0.2,  0.2],
                      [0.4,  0.6,  0.6],
                      [0.4,  1. ,  0.8],
                      [0.4,  0.9,  0.8],
                      [0.4,  0.7,  0.7]]]
    assert_allclose(test, expected)

    A = np.r_[0.3, 0.2, 0.1, 0, 0.7, 0.9, 1]
    B = np.r_[0.5, 0.5, 0.6, 0.4, 0.6, 0.3, 0.2]
    c = maxmin_composition(A, B)
    assert (1, 1) == c.shape
    assert_allclose(c, np.r_[[[0.6]]])


def test_maxprod_composition():
    mfI = np.r_[0.4, 0.7, 1.0, 0.8, 0.6]
    mfV = np.r_[0.2, 0.6, 1.0, 0.9, 0.7]
    mfC = np.r_[0.4, 1.0, 0.8]

    P = cartprod(mfV, mfI)
    S = cartprod(mfI, mfC)

    test = maxprod_composition(P, S)
    expected = np.r_[[[0.08,  0.2 ,  0.16],
                      [0.24,  0.6 ,  0.48],
                      [0.4 ,  1.  ,  0.8 ],
                      [0.36,  0.9 ,  0.72],
                      [0.28,  0.7 ,  0.56]]]
    assert_allclose(test, expected)

    A = np.r_[0.3, 0.2, 0.1, 0, 0.7, 0.9, 1]
    B = np.r_[0.5, 0.5, 0.6, 0.4, 0.6, 0.3, 0.2]
    c = maxprod_composition(A, B)
    assert (1, 1) == c.shape
    assert_allclose(c, np.r_[[[0.42]]])


def test_interp_membership():
    x = np.r_[0:4.1:0.1]
    mfx = trapmf(x, [0, 1, 2, 4])

    yy = interp_membership(x, mfx, 0)
    assert yy == 0

    yy = interp_membership(x, mfx, 0.535)
    assert_allclose(np.r_[yy], np.r_[0.535])

    yy = interp_membership(x, mfx, np.pi / 3.)
    assert yy == 1

    yy = interp_membership(x, mfx, 2.718)
    assert_allclose(np.r_[yy], np.r_[0.641])


def test_modus_ponens():
    A = np.r_[0, 0.6, 1, 0.2]
    B = np.r_[0, 0.4, 1, 0.8, 0.3, 0]
    C = np.r_[0.3, 0.5, 0.6, 0.6, 0.5, 0.3]
    Aprime = np.r_[0.5, 1, 0.3, 0]

    R_expected = np.r_[[[  1,   1,   1,   1,   1,   1],
                        [0.4, 0.4, 0.6, 0.6, 0.4, 0.4],
                        [  0,  0.4,   1, 0.8, 0.3,  0],
                        [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]]]
    Bprime_expected = np.r_[0.5, 0.5, 0.6, 0.6, 0.5, 0.5]

    R, Bprime = modus_ponens(A, B, Aprime)
    assert_allclose(R, R_expected)
    assert_allclose(Bprime, Bprime_expected)

    R_expected = np.r_[[[ 0.3,  0.5,  0.6,  0.6,  0.5,  0.3],
                        [ 0.3,  0.4,  0.6,  0.6,  0.4,  0.3],
                        [ 0. ,  0.4,  1. ,  0.8,  0.3,  0. ],
                        [ 0.3,  0.5,  0.6,  0.6,  0.5,  0.3]]]
    Bprime_expected = np.r_[ 0.3,  0.5,  0.6,  0.6,  0.5,  0.3]

    R, Bprime = modus_ponens(A, B, Aprime, C)
    assert_allclose(R, R_expected)
    assert_allclose(Bprime, Bprime_expected)


def test_outer_product():
    A = [0.3, 0.2, 0.1, 0, 0.7, 0.9, 1]
    B = [0.5, 0.5, 0.6, 0.4, 0.6, 0.3, 0.2]
    c = outer_product(A, B)
    assert_allclose(np.r_[c], np.r_[0.4])
    c = outer_product(np.asarray(A), np.asarray(B))
    assert_allclose(np.r_[c], np.r_[0.4])


def test_relation_min():
    A = np.r_[0, 0, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0]  # Fuzzy zero
    B = np.r_[0, 0, 0, 0, 0, 0, 0.6, 1, 0.6, 0, 0]  # Fuzzy +2

    mamdani = relation_min(A, B)
    expected = np.r_[[[0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.5, 0.5, 0.5, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.6, 1.,  0.6, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.5, 0.5, 0.5, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]]]

    assert_allclose(mamdani, expected)


def test_relation_product():
    A = np.r_[0, 0, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0]  # Fuzzy zero
    B = np.r_[0, 0, 0, 0, 0, 0, 0.6, 1, 0.6, 0, 0]  # Fuzzy +2

    product = relation_product(A, B)
    expected = np.r_[[[0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.3, 0.5, 0.3, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.6, 1.,  0.6, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.3, 0.5, 0.3, 0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                      [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]]]

    assert_allclose(product, expected)


def test_fuzzy_similarity():
    A = [0.3, 0.2, 0.1, 0, 0.7, 0.9, 1]
    B = [0.5, 0.5, 0.6, 0.4, 0.6, 0.3, 0.2]
    c = fuzzy_similarity(A, B)
    assert_allclose(np.r_[c], np.r_[0.6])
    c = fuzzy_similarity(A, B, mode='avg')
    assert_allclose(np.r_[c], np.r_[0.6])

def test_partial_dMF():

    gaussmf = 'gaussmf'
    mean = -1.5
    sigma = 0.75
    gaussmf_param_dict = {'mean':mean, 'sigma':sigma}
    test_int = randint(1,3)

    gaussmf_results = [partial_dMF(-1.5, gaussmf, gaussmf_param_dict, 'mean'),
                        partial_dMF(-1.5, gaussmf, gaussmf_param_dict, 'sigma'),
                        partial_dMF(-1.5, gaussmf, {'mean':mean, 'sigma':test_int * sigma}, 'mean') == \
                        -partial_dMF(-1.5, gaussmf, {'mean':mean, 'sigma':-test_int * sigma}, 'mean')]
    gaussmf_expected = [0., 0., True]
    assert_allclose(gaussmf_results, gaussmf_expected)


    gbellmf = 'gbellmf'
    a = 2.
    b = 1.
    c = 0.5
    gbellmf_param_dict = {'a':a, 'b':b, 'c':c}

    gbellmf_results = [partial_dMF(-1.5, gbellmf, gbellmf_param_dict, 'a'),
                        partial_dMF(2.5, gbellmf, gbellmf_param_dict, 'a'),
                        partial_dMF(-1.5, gbellmf, gbellmf_param_dict, 'b'),
                        partial_dMF(2.5, gbellmf, gbellmf_param_dict, 'b'),
                        partial_dMF(-1.5, gbellmf, gbellmf_param_dict, 'c'),
                        partial_dMF(2.5, gbellmf, gbellmf_param_dict, 'c')
                        ]
    gbellmf_expected = [0.25, 0.25, -0.0, -0.0, -0.25, 0.25]
    assert_allclose(gbellmf_results, gbellmf_expected)


    sigmf = 'sigmf'
    b_one = 1.0
    c_one = 3.0
    b_two = -1.0
    c_two = 0.5
    sigmf_param_dict_one = {'b':b_one, 'c':c_one}
    sigmf_param_dict_two = {'b':b_two, 'c':c_two}

    sigmf_results = [partial_dMF(1.0, sigmf, sigmf_param_dict_one, 'b'),
                      partial_dMF(-1.0, sigmf, sigmf_param_dict_two, 'b'),
                      partial_dMF(1.0, sigmf, sigmf_param_dict_one, 'c'),
                      partial_dMF(-1.0, sigmf, sigmf_param_dict_two, 'c')
                      ]
    sigmf_expected = [-0.75, -0.125, 0., 0.]
    assert_allclose(sigmf_results, sigmf_expected)


if __name__ == "__main__":
    np.testing.run_module_suite()
