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
