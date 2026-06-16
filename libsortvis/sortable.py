class Sortable:
    def __init__(self, tracklist, i):
        self.tracklist, self.i = tracklist, i
        self.path = []

    def _other(self, other):
        """Counts each comparison and returns the comparable value of the
        other operand, whether it is a Sortable or a raw value."""
        self.tracklist.total_comparisons += 1
        return other.i if hasattr(other, "i") else other

    def __lt__(self, other):
        return self.i < self._other(other)

    def __le__(self, other):
        return self.i <= self._other(other)

    def __gt__(self, other):
        return self.i > self._other(other)

    def __ge__(self, other):
        return self.i >= self._other(other)

    def __eq__(self, other):
        return self.i == self._other(other)

    def __ne__(self, other):
        return self.i != self._other(other)

    # Keep identity-based hashing (defining __eq__ disables it by default).
    __hash__ = object.__hash__

    def __int__(self):
        return self.i

    def __repr__(self):
        return str(self.i)


class TrackList:
    """
    A list-like object that logs the positions of its elements every time
    the log() method is called.
    """

    def __init__(self, itms):
        self.lst = [Sortable(self, i) for i in itms]
        self.start = self.lst[:]
        self.total_comparisons = 0
        self.log()

    def wrap(self, wrapper):
        """Allows an additional wrapping of the inner list with the given
        wrapper. See algos.timsort as an example."""
        self.lst = [wrapper(i) for i in self.lst]
        self.start = self.lst[:]

    def reset(self):
        self.total_comparisons = 0
        self.lst = self.start[:]

    # In Python 3 the protocol dunders below must live on the type; they are
    # NOT resolved through __getattr__ the way they were in Python 2. Plain
    # list methods (pop, insert, sort, reverse, index, ...) are still picked
    # up by __getattr__. __getitem__/__setitem__ accept ints and slices,
    # because the underlying list does.
    def __iter__(self):
        return iter(self.lst)

    def __len__(self):
        return len(self.lst)

    def __getitem__(self, idx):
        return self.lst[idx]

    def __setitem__(self, idx, value):
        self.lst[idx] = value

    def __getattr__(self, attr):
        """Redirecting every lookup on this object that didn't succeed to
        the internal list (e.g., iterating over self iterates over list)."""
        return getattr(self.lst, attr)

    def log(self):
        for i, v in enumerate(self):
            if v is not None:
                v.path.append(i)


class DummySortable(object):
    def __init__(self, i):
        self.i = i
        self.path = []

    def __int__(self):
        return self.i


def read_paths(fp):
    """
    Reads a sorting history from a filepointer, and returns a list of Sortables.

    The sorting history is specified as a set of newline-terminated lists,
    with each list consisting of space-separated numbers.
    """
    sortables = {}
    for i in fp.readlines():
        n = i.split()
        if not sortables:
            for j in n:
                j = int(j)
                sortables[j] = DummySortable(j)
        for offset, j in enumerate(n):
            sortables[int(j)].path.append(offset)
    return list(sortables.values())
