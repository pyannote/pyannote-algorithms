#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2013-2014 CNRS (Hervé BREDIN - http://herve.niderb.fr)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals

from collections import namedtuple


class HACIteration(
    namedtuple('HACIteration',
               ['merge', 'similarity', 'into'])
):

    """Iteration of hierarchical agglomerative clustering

    Parameters
    ----------
    merge : iterable
        Unique identifiers of merged clusters
    similarity : float
        Similarity between merged clusters
    into : hashable
        Unique identifier of resulting clusters

    """
    def __new__(cls, merge, similarity, into):
        return super(HACIteration, cls).__new__(
            cls, merge, similarity, into)


class HACHistory(object):
    """History of hierarchical agglomerative clustering

    Parameters
    ----------
    starting_point : Annotation
        Starting point
    iterations : iterable, optional
        HAC iterations in chronological order
    """

    def __init__(self, starting_point, iterations=None):
        super(HACHistory, self).__init__()
        self.starting_point = starting_point.copy()
        if iterations is None:
            self.iterations = []
        else:
            self.iterations = iterations

    def __len__(self):
        return len(self.iterations)

    def add_iteration(self, merge, similarity, into):
        """Add new iteration

        Parameters
        ----------
        merge : iterable
            Unique identifiers of merged clusters
        similarity : float
            Similarity between merged clusters
        into : hashable
            Unique identifier of resulting clusters

        """
        iteration = HACIteration(
            merge=merge,
            similarity=similarity,
            into=into
        )
        self.iterations.append(iteration)

    def __getitem__(self, n):
        """Get clustering status after `n` iterations

        Parameters
        ----------
        n : int
            Number of iterations

        Returns
        -------
        annotation : Annotation
            Clustering status after `n` iterations

        """

        # support for history[-1], history[-2]
        # i = -1 ==> after last iteration
        # i = -2 ==> after penultimate iteration
        # ... etc ...
        if n < 0:
            n = len(self) + 1 + n

        # i = 0 ==> starting point
        # i = 1 ==> after first iteration
        # i = 2 ==> aftr second iterations
        # ... etc ...
        for i, annotation in enumerate(self):
            if i+1 > n:
                break

        return annotation

    def __iter__(self):
        """"""
        annotation = self.starting_point.copy()
        yield annotation
        for iteration in self.iterations:
            translation = {c: iteration.into
                           for c in iteration.merge}
            annotation = annotation % translation
            yield annotation
