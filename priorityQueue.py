"""
I translated this code into python
from the java code in
"Algorithms" by Sedgewick and Wayne.
"""


class IndexMinPQ(object):
    "min priority queue where each key is referenced by an index i"
    def __init__(self, N):
        """
        create indexed PQ with indices 0 thru N-1

        # max number of keys
        # key = priority (ex: weight of an edge)
        # input: heap position     output: index
        # input: index             output: heap position
        # size of _pq
        """
        self._NMAX = N
        self._keys = [-1 for _ in range(N+1)]
        self._pq = [-1 for _ in range(N+1)]
        self._qp = [-1 for _ in range(N+1)]
        self._N = 0

    def insert(self, i, key):
        """
        insert key into PQ

        # 'contains' parameter is indexed from 0
        # add 1 to number of elements in PQ
        # key index is stored on pq at heap position N
        # index is stored at heap position N
        """
        assert (i >= 0 and i < self._NMAX), "i is out of bounds"
        if (not self.contains(i)):
            self._N = self._N + 1
            self._pq[self._N] = i + 1
            self._qp[i + 1] = self._N
            self._keys[i + 1] = key
            self._swim(self._N)
        else:
            print "index is already in PQ"

    def size(self):
        return self._N

    def isEmpty(self):
        return self._N == 0

    def minIndex(self):
        "return index associated with minimal key"
        # min index is stored in heap position 1;
        # subtract 1 so indexing is from 0
        return self._pq[1] - 1

    def minKey(self):
        "return minimal key"
        return self._keys[self._pq[1]]

    def decreaseKey(self, i, key):
        "decrease the key associated with index i to the specified value"
        assert (i >= 0 and i < self._NMAX), "i out of range"
        # 'contains' parameter is indexed from 0
        if (self.contains(i)):
            self._keys[i+1] = key
            # qp[i] is the heap position
            # since key is less than original key, swim it up
            self._swim(self._qp[i+1])
        else:
            print "index is not in PQ"

    def delMin(self):
        "delete a minimal key and return its associated index"
        assert (self._N > 0)
        if (self._N > 0):
            min_index = self._pq[1]
            self._exch(1, self._N)
            self._keys[min_index] = -1       # remove key from keys
            self._pq[self._N] = -1           # remove index from PQ
            self._qp[min_index] = -1         # free heap position in heap
            self._N = self._N - 1            # reduce size of PQ by 1
            self._sink(1)                    # heapify heap
            return min_index - 1             # subtract 1 so indexing is from 0

    def contains(self, i):
        "test whether pq contains index i"
        assert (i >= 0 and i < self._NMAX), "i out of range"
        # -1 means heap position has not been assigned
        return self._qp[i + 1] != -1

    def keyOf(self, i):
        "returns key associated with index i"
        assert (i >= 0 and i < self._NMAX), "i out of range"
        if self.contains(i):
            return self._keys[i+1]
        else:
            print "index is not in PQ"

    def __repr__(self):
        "Uniquely identifies IndexMinPQ"
        return "size=%r indices=%r keys=%r" % (self.size(), self._pq[1:], self._keys[1:])

    def _greater(self, i, j):
        "i, j are heap positions"
        return self._keys[self._pq[i]] > self._keys[self._pq[j]]

    def _exch(self, i, j):
        """
        i, j are heap positions

        # index in heap position i is copied to swap
        # index in heap position j is copied into heap position i
        # swap is copied to heap position j
        # update qp with heap position for index pq[i]
        # update qp with heap position for index pq[j]
        """
        # exch indexes in pq
        swap = self._pq[i]
        self._pq[i] = self._pq[j]
        self._pq[j] = swap
        # update heap positions for these indexes in qp
        self._qp[self._pq[i]] = i
        self._qp[self._pq[j]] = j

    def _swim(self, k):
        """
        k is position in heap

        swim key up in heap to maintain heap invariant
        """
        while (k > 1 and self._greater(k/2, k)):
            self._exch(k, k/2)
            k = k/2

    def _sink(self, k):
        """
        k is position in heap

        sink key down in heap to maintain heap invariant

        # check that node in heap position k has a child
        # j is heap position of child
        # set j to smallest child
        # compare parent to smallest child
        # set parent to heap position of child and repeat sink
        """
        while (2*k <= self._N):
            j = 2 * k
            if (j < self._N and self._greater(j, j+1)):
                j = j + 1
            if (not self._greater(k, j)):
                break
            else:
                self._exch(k, j)
                k = j
