"""
Various utility classes
"""


class VersionTuple(tuple):
    """
    Representation of version X.Y.Z
    """

    def __new__(cls, s):
        return super().__new__(cls, map(int, s.split(".")))

    def __repr__(self):
        return ".".join(map(str, self))

    def __str__(self):
        return self.__repr__()
