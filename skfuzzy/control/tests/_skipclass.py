import collections.abc
import functools
import types
try:
    from unittest import SkipTest, TestCase
except Exception:
    from nose import SkipTest
    from nose.case import Test as TestCase


def _id(obj):
    return obj


def skip(reason):
    """Unconditionally skip a test."""
    def decorator(test_item):
        try:
            types.ClassType
            testagainst = (type, types.ClassType)
        except AttributeError:
            testagainst = type
        if not isinstance(test_item, testagainst):
            @functools.wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item = skip_wrapper
        elif issubclass(test_item, TestCase):
            @classmethod
            @functools.wraps(test_item.setUpClass)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item.setUpClass = skip_wrapper
        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator


def skipclassif(condition, reason):
    """Skip a test if the condition is true."""
    if condition:
        return skip(reason)
    return _id


def skipif(skip_condition, msg=None):
    """
    Copied from numpy < 1.25

    Make function raise SkipTest exception if a given condition is true.

    If the condition is a callable, it is used at runtime to dynamically
    make the decision. This is useful for tests that may require costly
    imports, to delay the cost until the test suite is actually executed.

    Parameters
    ----------
    skip_condition : bool or callable
        Flag to determine whether to skip the decorated test.
    msg : str, optional
        Message to give on raising a SkipTest exception. Default is None.

    Returns
    -------
    decorator : function
        Decorator which, when applied to a function, causes SkipTest
        to be raised when `skip_condition` is True, and the function
        to be called normally otherwise.

    Notes
    -----
    The decorator itself is decorated with the ``nose.tools.make_decorator``
    function in order to transmit function name, and various other metadata.

    """

    def skip_decorator(f):
        # Local import to avoid a hard nose dependency and only incur the
        # import time overhead at actual test-time.
        import nose

        # Allow for both boolean or callable skip conditions.
        if isinstance(skip_condition, collections.abc.Callable):
            skip_val = lambda: skip_condition()
        else:
            skip_val = lambda: skip_condition

        def get_msg(func, msg=None):
            """Skip message with information about function being skipped."""
            if msg is None:
                out = 'Test skipped due to test condition'
            else:
                out = msg

            return f'Skipping test: {func.__name__}: {out}'

        # We need to define *two* skippers because Python doesn't allow both
        # return with value and yield inside the same function.
        def skipper_func(*args, **kwargs):
            """Skipper for normal test functions."""
            if skip_val():
                raise SkipTest(get_msg(f, msg))
            else:
                return f(*args, **kwargs)

        def skipper_gen(*args, **kwargs):
            """Skipper for test generators."""
            if skip_val():
                raise SkipTest(get_msg(f, msg))
            else:
                yield from f(*args, **kwargs)

        # Choose the right skipper to use when building the actual decorator.
        if nose.util.isgenerator(f):
            skipper = skipper_gen
        else:
            skipper = skipper_func

        return nose.tools.make_decorator(f)(skipper)

    return skip_decorator
