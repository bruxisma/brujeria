from collections.abc import Hashable
from functools import partialmethod
from abc import ABC, abstractmethod

import operator

class KeyBase(ABC):
    @abstractmethod
    def __key__ (self) -> tuple: pass

class HashableMixin(Hashable, KeyBase):
    def __hash__ (self): return hash(self.__key__())

class ComparableMixin(KeyBase):
    def __compare__ (self, op, other):
        if not isinstance(other, KeyBase): return NotImplemented
        return op(self.__key__(), other.__key__())

class LessThanComparableMixin(ComparableMixin):
    __ge__ = partialmethod(ComparableMixin.__compare__, operator.ge)
    __le__ = partialmethod(ComparableMixin.__compare__, operator.le)
    __gt__ = partialmethod(ComparableMixin.__compare__, operator.gt)
    __lt__ = partialmethod(ComparableMixin.__compare__, operator.lt)

class EqualityComparableMixin(ComparableMixin):
    __eq__ = partialmethod(ComparableMixin.__compare__, operator.eq)
    __ne__ = partialmethod(ComparableMixin.__compare__, operator.ne)

class OrderedMixin(EqualityComparableMixin, LessThanComparableMixin):
    pass

class ValueMixin(HashableMixin, OrderedMixin):
    pass