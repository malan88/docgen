"""Foobar is a test class
@TODO What
"""


class Foo:
    """A testing base class
    # props
    - foo -int
    """
    foo = 4


class InheritTest(Foo):
    """An inheritance test.

    # props
    - bar -int
    @TODO define foo
    """

    def foobar(self):
        """Returns 4"""
        return 4

    @property
    def foobarprop(self):
        """@prop Testing a property docstring"""
        return 4


def foobar(t):
    """A function test
    @TODO define foo
    """
    return t
