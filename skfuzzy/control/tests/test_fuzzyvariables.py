import numpy as np
import numpy.testing as tst
import nose

try:
    from collections import OrderedDict
except ImportError:
    from skfuzzy.control.ordereddict import OrderedDict

from skfuzzy.control import Antecedent, Consequent


def setup():
    global ant
    global con
    global universe

    universe0 = np.linspace(0, 5, 6)
    universe1 = np.linspace(0, 9, 10)
    ant_label = 'service'
    con_label = 'TIP'

    ant = Antecedent(universe0, ant_label)
    con = Consequent(universe1, con_label)


def assert_empty_ordereddict(obj):
    assert len(obj) is 0
    assert isinstance(obj, OrderedDict)


def test_instantiate_incorrect():
    # Require two arguments to instantiate
    tst.assert_raises(TypeError, Antecedent)
    tst.assert_raises(TypeError, Consequent)

    universe = np.linspace(0, 5, 7)
    tst.assert_raises(TypeError, Antecedent, universe)
    tst.assert_raises(TypeError, Consequent, universe)


def test_instantiate_antecedent():
    # Correctly create a minimal Antecedent
    universe = np.linspace(0, 5, 7)
    label = 'test-Antecedent Labeling 130948@!!"'
    ant = Antecedent(universe, label)

    # Assure expected behavior
    tst.assert_equal(universe, ant.universe)
    assert ant.label == label
    assert ant.active is None
    assert ant.input is None
    assert ant._id == id(ant)
    assert_empty_ordereddict(ant.output)
    assert_empty_ordereddict(ant.mf)
    assert_empty_ordereddict(ant.connections)
    assert ant.__name__ == 'Antecedent'
    assert ant.__repr__() == 'Antecedent: {0}'.format(label)


def test_instantiate_consequent():
    # Correctly create a minimal Consequent
    universe = np.linspace(0, 5, 7)
    label = 'test-Consequent Labeling ??$%&dwlkj234!"'
    con = Consequent(universe, label)

    # Assure expected behavior
    tst.assert_equal(universe, con.universe)
    assert con.label == label
    assert con.active is None
    assert con._id == id(con)
    assert con.output is None
    assert_empty_ordereddict(con.mf)
    assert_empty_ordereddict(con.connections)
    assert_empty_ordereddict(con.cuts)
    assert_empty_ordereddict(con.cut_mfs)
    assert con.__name__ == 'Consequent'
    assert con.__repr__() == 'Consequent: {0}'.format(label)


@nose.with_setup(setup)
def test_automf3():
    global ant  # universe: [0, 1, 2, 3, 4, 5]
    global con  # universe: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    label3 = ['poor', 'average', 'good']
    mfs3 = [np.r_[1., 0.6, 0.2, 0., 0., 0.],
            np.r_[0., 0.4, 0.8, 0.8, 0.4, 0.],
            np.r_[0., 0., 0., 0.2, 0.6, 1.]]
    alt_label3 = ['low', 'average', 'high']

    # Test Antecedent
    ant.automf(3)
    assert ant.mf.keys() == label3
    for arr0, arr1 in zip(ant.mf.values(), mfs3):
        tst.assert_allclose(arr0, arr1)

    ant.automf(3, variable_type='quant')
    assert ant.mf.keys() == alt_label3

    ant.automf(3, invert=True)
    assert ant.mf.keys() == label3[::-1]

    ant.automf(3, variable_type='quant', invert=True)
    assert ant.mf.keys() == alt_label3[::-1]

    # Test Consequent
    mfs3b = [np.r_[1., 7/9., 5/9., 3/9., 1/9., 0., 0., 0., 0., 0.],
             np.r_[0., 2/9., 4/9., 6/9., 8/9., 8/9., 6/9., 4/9., 2/9., 0.],
             np.r_[0., 0., 0., 0., 0., 1/9., 3/9., 5/9., 7/9., 1.]]

    con.automf(3)
    assert con.mf.keys() == label3
    for arr0, arr1 in zip(con.mf.values(), mfs3b):
        tst.assert_allclose(arr0, arr1)

    con.automf(3, variable_type='quant')
    assert con.mf.keys() == alt_label3

    con.automf(3, invert=True)
    assert con.mf.keys() == label3[::-1]

    con.automf(3, variable_type='quant', invert=True)
    assert con.mf.keys() == alt_label3[::-1]


@nose.with_setup(setup)
def test_automf5():
    global ant  # universe: [0, 1, 2, 3, 4, 5]
    global con  # universe: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    label5 = ['poor', 'mediocre', 'average', 'decent', 'good']
    mfs5 = [np.r_[1., 0.2, 0., 0., 0., 0.],
            np.r_[0., 0.8, 0.4, 0., 0., 0.],
            np.r_[0., 0., 0.6, 0.6, 0., 0.],
            np.r_[0., 0., 0., 0.4, 0.8, 0.],
            np.r_[0., 0., 0., 0., 0.2, 1.]]
    alt_label5 = ['lower', 'low', 'average', 'high', 'higher']

    # Test Antecedent
    ant.automf(5)
    assert ant.mf.keys() == label5
    for arr0, arr1 in zip(ant.mf.values(), mfs5):
        tst.assert_allclose(arr0, arr1)

    ant.automf(5, variable_type='quant')
    assert ant.mf.keys() == alt_label5

    ant.automf(5, invert=True)
    assert ant.mf.keys() == label5[::-1]

    ant.automf(5, variable_type='quant', invert=True)
    assert ant.mf.keys() == alt_label5[::-1]

    # Test Consequent
    mfs5b = [np.r_[1., 5/9., 1/9., 0., 0., 0., 0., 0., 0., 0.],
             np.r_[0., 4/9., 8/9., 6/9., 2/9., 0., 0., 0., 0., 0.],
             np.r_[0., 0., 0., 3/9., 7/9., 7/9., 3/9., 0., 0., 0.],
             np.r_[0., 0., 0., 0., 0., 2/9., 6/9., 8/9., 4/9., 0.],
             np.r_[0., 0., 0., 0., 0., 0., 0., 1/9., 5/9., 1.]]

    con.automf(5)
    assert con.mf.keys() == label5
    for arr0, arr1 in zip(con.mf.values(), mfs5b):
        tst.assert_allclose(arr0, arr1)

    con.automf(5, variable_type='quant')
    assert con.mf.keys() == alt_label5

    con.automf(5, invert=True)
    assert con.mf.keys() == label5[::-1]

    con.automf(5, variable_type='quant', invert=True)
    assert con.mf.keys() == alt_label5[::-1]


@nose.with_setup(setup)
def test_automf7():
    global ant  # universe: [0, 1, 2, 3, 4, 5]
    global con  # universe: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    label7 = ['dismal', 'poor', 'mediocre', 'average',
              'decent', 'good', 'excellent']
    mfs7 = [np.r_[1., 0., 0., 0., 0., 0.],
            np.r_[0., 0.8, 0., 0., 0., 0.],
            np.r_[0., 0.2, 0.6, 0., 0., 0.],
            np.r_[0., 0., 0.4, 0.4, 0., 0.],
            np.r_[0., 0., 0., 0.6, 0.2, 0.],
            np.r_[0., 0., 0., 0., 0.8, 0.],
            np.r_[0., 0., 0., 0., 0., 1.]]
    alt_label7 = ['lowest', 'lower', 'low', 'average',
                  'high', 'higher', 'highest']

    # Test Antecedent
    ant.automf(7)
    assert ant.mf.keys() == label7
    for arr0, arr1 in zip(ant.mf.values(), mfs7):
        tst.assert_allclose(arr0, arr1)

    ant.automf(7, variable_type='quant')
    assert ant.mf.keys() == alt_label7

    ant.automf(7, invert=True)
    assert ant.mf.keys() == label7[::-1]

    ant.automf(7, variable_type='quant', invert=True)
    assert ant.mf.keys() == alt_label7[::-1]

    # Test Consequent
    mfs7b = [np.r_[1., 3/9., 0., 0., 0., 0., 0., 0., 0., 0.],
             np.r_[0., 6/9., 6/9., 0., 0., 0., 0., 0., 0., 0.],
             np.r_[0., 0., 3/9., 1., 3/9., 0., 0., 0., 0., 0.],
             np.r_[0., 0., 0., 0., 6/9., 6/9., 0., 0., 0., 0.],
             np.r_[0., 0., 0., 0., 0., 3/9., 1., 3/9., 0., 0.],
             np.r_[0., 0., 0., 0., 0., 0., 0., 6/9., 6/9., 0.],
             np.r_[0., 0., 0., 0., 0., 0., 0., 0., 3/9., 1.]]

    con.automf(7)
    assert con.mf.keys() == label7
    for arr0, arr1 in zip(con.mf.values(), mfs7b):
        tst.assert_allclose(arr0, arr1)

    con.automf(7, variable_type='quant')
    assert con.mf.keys() == alt_label7

    con.automf(7, invert=True)
    assert con.mf.keys() == label7[::-1]

    con.automf(7, variable_type='quant', invert=True)
    assert con.mf.keys() == alt_label7[::-1]


@nose.with_setup(setup)
def test_automf_bad():
    global ant
    global con

    tst.assert_raises(ValueError, ant.automf, 4)
    tst.assert_raises(ValueError, ant.automf, 13)
    tst.assert_raises(ValueError, con.automf, 4)
    tst.assert_raises(ValueError, con.automf, 13)


def test_set_active():
    universe = np.linspace(0, 5, 7)
    ant_label = 'service'
    con_label = 'TIP'

    ant = Antecedent(universe, ant_label)
    con = Consequent(universe, con_label)

    ant.automf(5)
    for label in ant.mf.keys():
        ant[label]
        assert ant.active == label

    con.automf(7)
    for label in con.mf.keys():
        con[label]
        assert con.active == label


@nose.with_setup(setup)
def test_bad_set_active():
    global ant
    global con

    # Test error raised if label does not exist
    tst.assert_raises(ValueError, ant.__getitem__, 'nope')
    tst.assert_raises(ValueError, con.__getitem__, 'nope')


def test_add_mf():
    universe = np.linspace(0, 7, 21)
    ant_label = 'service'
    con_label = 'TIP'

    ant = Antecedent(universe, ant_label)
    con = Consequent(universe, con_label)

    mf0 = np.sin(universe / 7. * 4 * np.pi) / 2. + 0.5
    mf1 = np.arange(ant.universe.size) / ant.universe.size

    # Assign mfs to Antecedent
    ant['wavy'] = mf0
    ant['high'] = mf1

    # Ensure they were added correctly
    assert ant.mf.keys() == ['wavy', 'high']
    tst.assert_equal(ant.mf['wavy'], mf0)
    tst.assert_equal(ant.mf['high'], mf1)

    # Assign mfs to Consequent
    con['wavy'] = mf0
    con['high'] = mf1

    # Ensure they were added correctly
    assert con.mf.keys() == ['wavy', 'high']
    tst.assert_equal(con.mf['wavy'], mf0)
    tst.assert_equal(con.mf['high'], mf1)


@nose.with_setup(setup)
def test_set_patch():
    global con

    # Consequent only test, the analogue of Antecedent's input
    con.automf(3)

    # Setting a patch
    con.set_patch('average', 0.4)
    assert con.cuts['average'] == 0.4

    # Overriding it with a higher patch
    con.set_patch('average', 0.55)
    assert con.cuts['average'] == 0.55

    # Setting the other patches
    con.set_patch('good', 0.3)
    con.set_patch('poor', 0.88)
    assert con.cuts['good'] == 0.3
    assert con.cuts['poor'] == 0.88

    con.compute()
    tst.assert_allclose(con.output, 3.6644951140065136)


@nose.with_setup(setup)
def test_set_input():
    global ant
    ant.automf(3)
    ant.set_input(2.3)

    assert ant.input == 2.3


@nose.with_setup(setup)
def test_add_bad_mf():
    global ant
    global con

    tst.assert_raises(ValueError, ant.__setitem__, 'new_mf', np.ones(30))
    tst.assert_raises(ValueError, ant.__setitem__, 'low', np.arange(6))

    tst.assert_raises(ValueError, con.__setitem__, 'new_mf', np.ones(30))
    tst.assert_raises(ValueError, con.__setitem__, 'low', np.arange(10))


@nose.with_setup(setup)
def test_cannot_compute():
    global ant
    global con
    tst.assert_raises(ValueError, ant.compute)
    tst.assert_raises(ValueError, con.compute)


if __name__ == '__main__':
    tst.run_module_suite()
