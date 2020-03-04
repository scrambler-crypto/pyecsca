import weakref
from typing import Optional, Any, Mapping, Sequence
from copy import copy, deepcopy

from numpy import ndarray
import numpy as np
from public import public


@public
class Trace(object):
    """A trace, which has an optional title, optional data bytes and mandatory samples."""
    title: Optional[str]
    data: Optional[bytes]
    meta: Mapping[str, Any]
    samples: ndarray

    def __init__(self, samples: ndarray, title: Optional[str], data: Optional[bytes],
                 meta: Mapping[str, Any] = None, trace_set: Any = None):
        self.title = title
        self.data = data
        self.meta = meta
        self.samples = samples
        self.trace_set = trace_set

    def __len__(self):
        """Length of the trace, in samples."""
        return len(self.samples)

    def __getitem__(self, index):
        """Get the sample at `index`."""
        return self.samples[index]

    def __setitem__(self, key, value):
        """Set the sample at `key`."""
        self.samples[key] = value

    def __iter__(self):
        """Iterate over the samples."""
        yield from self.samples

    @property
    def trace_set(self) -> Any:
        if self._trace_set is None:
            return None
        return self._trace_set()

    @trace_set.setter
    def trace_set(self, trace_set: Any):
        if trace_set is None:
            self._trace_set = None
        else:
            self._trace_set = weakref.ref(trace_set)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_trace_set"]
        return state

    def __eq__(self, other):
        if not isinstance(other, Trace):
            return False
        return np.array_equal(self.samples, other.samples) and self.title == other.title and self.data == other.data and self.meta == other.meta

    def with_samples(self, samples: ndarray) -> "Trace":
        return Trace(samples, deepcopy(self.title), deepcopy(self.data), deepcopy(self.meta), deepcopy(self.trace_set))

    def __copy__(self):
        return Trace(copy(self.samples), copy(self.title), copy(self.data), copy(self.meta), copy(self.trace_set))

    def __deepcopy__(self, memodict={}):
        return Trace(deepcopy(self.samples, memo=memodict), deepcopy(self.title, memo=memodict), deepcopy(self.data, memo=memodict), deepcopy(self.meta, memo=memodict), deepcopy(self.trace_set, memo=memodict))

    def __repr__(self):
        return f"Trace(title={self.title!r}, data={self.data!r}, samples={self.samples!r}, trace_set={self.trace_set!r})"


@public
class CombinedTrace(Trace):
    """A trace that was combined from other traces, `parents`."""

    def __init__(self, samples: ndarray, title: Optional[str], data: Optional[bytes],
                 meta: Mapping[str, Any] = None, trace_set: Any = None,
                 parents: Sequence[Trace] = None):
        super().__init__(samples, title, data, meta, trace_set=trace_set)
        self.parents = None
        if parents is not None:
            self.parents = weakref.WeakSet(parents)

    def __repr__(self):
        return f"CombinedTrace(title={self.title!r}, data={self.data!r}, samples={self.samples!r}, trace_set={self.trace_set!r}, parents={self.parents})"
