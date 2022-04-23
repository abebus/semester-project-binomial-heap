class ItemRef:
    def __init__(self, node, get_heap):
        self.ref = node
        self.get_heap = get_heap
        self.in_tree = True

    def __str__(self):
        if self.in_tree:
            return f"<BinomialHeap Reference to '{str(self.ref.val)}'>"
        else:
            return "<stale BinomialHeap Reference>"

    def decrease(self, new_key):
        assert self.in_tree
        assert self.ref.ref == self
        self.ref.decrease(new_key)

    def delete(self):
        self.decrease(self)
        v = self.get_heap().extract_min()
        assert not self.in_tree
        assert v is self.ref.val

    def in_heap(self, heap):
        return self.in_tree and self.get_heap() == heap

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return False


class BinomialHeap:

    class Node:
        def __init__(self, get_heap, key, val=None):
            self.degree = 0
            self.parent = None
            self.next = None
            self.child = None
            self.key = key
            self.ref = ItemRef(self, get_heap)
            if val is None:
                val = key
            self.val = val

        def __str__(self):
            k = lambda x: str(x.key) if x else 'NIL'
            return f'({k(self)}, c:{k(self.child)}, n:{k(self.next)})'

        def link(self, other):
            other.parent = self
            other.next = self.child
            self.child = other
            self.degree += 1

        def decrease(self, new_key):
            node = self
            assert new_key < node.key
            node.key = new_key
            cur = node
            parent = cur.parent
            while parent and cur.key < parent.key:
                # need to bubble up
                # swap refs
                parent.ref.ref, cur.ref.ref = cur, parent
                parent.ref, cur.ref = cur.ref, parent.ref
                # now swap keys and payload
                parent.key, cur.key = cur.key, parent.key
                parent.val, cur.val = cur.val, parent.val
                # step up
                cur = parent
                parent = cur.parent

        @staticmethod
        def roots_merge(h1, h2):
            if not h1:
                return h2
            if not h2:
                return h1
            if h1.degree < h2.degree:
                h = h1
                h1 = h.next
            else:
                h = h2
                h2 = h2.next
            p = h
            while h2 and h1:
                if h1.degree < h2.degree:
                    p.next = h1
                    h1 = h1.next
                else:
                    p.next = h2
                    h2 = h2.next
                p = p.next
            if h2:
                p.next = h2
            else:
                p.next = h1
            return h

        @staticmethod
        def roots_reverse(h):
            if not h:
                return None
            tail = None
            _next = h
            h.parent = None
            while h.next:
                _next = h.next
                h.next = tail
                tail = h
                h = _next
                h.parent = None
            h.next = tail
            return h

    class __Ref:
        def __init__(self, h):
            self.heap = h
            self.ref = None

        def get_heap_ref(self):
            if not self.ref:
                return self
            else:
                # compact
                self.ref = self.ref.get_heap_ref()
                return self.ref

        def get_heap(self):
            return self.get_heap_ref().heap

    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self.head = None
        self.size = 0
        self.ref = BinomialHeap.__Ref(self)
        for x in lst:
            try:
                self.insert(x[0], x[1])
            except TypeError:
                self.insert(x)

    def insert(self, key, value=None):
        n = BinomialHeap.Node(self.ref.get_heap, key, value)
        self.__union(n)
        self.size += 1
        return n.ref

    def union(self, other):
        self.size = self.size + other.size
        h2 = other.head
        self.__union(h2)
        other.ref.ref = self.ref
        other.__init__()

    def min(self):
        pos = self.__min()
        return pos[0].val if pos else None

    def extract_min(self):
        # find mininum
        pos = self.__min()
        if not pos:
            return None
        else:
            (x, prev) = pos
            # remove from list
            if prev:
                prev.next = x.next
            else:
                self.head = x.next
            kids = BinomialHeap.Node.roots_reverse(x.child)
            self.__union(kids)
            x.ref.in_tree = False
            self.size -= 1
            return x.val

    def __nonzero__(self):
        return self.head is not None

    def __iter__(self):
        return self

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        """H[key] = H.insert(key, value)"""
        self.insert(key, value)

    def __iadd__(self, other):
        """a += b"""
        self.union(other)
        return self

    def next(self):
        if self.head:
            return self.extract_min()
        else:
            raise StopIteration

    __next__ = next

    def __contains__(self, ref):
        if type(ref) != ItemRef:
            raise TypeError("Expected an ItemRef")
        else:
            return ref.in_heap(self)

    def __min(self):
        if not self.head:
            return None
        minn = self.head
        min_prev = None
        prev = minn
        cur = minn.next
        while cur:
            if cur.key < minn.key:
                minn = cur
                min_prev = prev
            prev = cur
            cur = cur.next
        return minn, min_prev

    def __union(self, h2):
        if not h2:
            # nothing to do
            return
        h1 = self.head
        if not h1:
            self.head = h2
            return
        h1 = BinomialHeap.Node.roots_merge(h1, h2)
        prev = None
        x = h1
        next_ = x.next
        while next_:
            if x.degree != next_.degree or \
                    (next_.next and next_.next.degree == x.degree):
                prev = x
                x = next_
            elif x.key <= next_.key:
                # x becomes the root of next
                x.next = next_.next
                x.link(next_)
            else:
                # next becomes the root of x
                if not prev:
                    # update the "master" head
                    h1 = next_
                else:
                    # just update previous link
                    prev.next = next_
                next_.link(x)
                # x is not toplevel anymore, update ref by advancing
                x = next_
            next_ = x.next
        self.head = h1
