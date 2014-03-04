"""
A tree structure with dynamic attribute interface.
"""
from __future__ import print_function, division

import copy

class Tree(object):
    """
    A Tree is a set of elements, some of which are other trees.
    """

    def __init__(self):
        object.__setattr__(self, "_leaves", {})
        object.__setattr__(self, "_branches", {})
        object.__setattr__(self, "_freeze_", False)
        object.__setattr__(self, "_freeze_struct_", False)

    def _copy(self, deep=False):
        """convenience copy method

        :param deep:  if True, perform a deep copy
        """
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def _branch(self, name, overwrite=False, nested=True):
        """
        Create a new branch in the tree. Any branch is a fully independent tree.
        Can create nested branch in one call

        :param name:      the name of the branch
        :param nested:    if True, create intermediate branchs as needed.
                          Note that if override is True, existing intermediate branchs
                          will not be recreated.
        :raise KeyError:  if a branch or leaf already exists with this name
        """
        if self._freeze_:
            raise ValueError("Can't add a branch to a frozen tree")
        if self._freeze_struct_:
            raise ValueError("Can't add a branch to a tree whose structure is frozen")
        self._check_name(name)
        path = name.split('.', 1)

        if len(path) == 2 and (not nested) and path[0] not in self._branches:
            raise ValueError("Can't created non-existent intermediary branches with nested = False")
        if path[0] in self._branches:
            if len(path) == 1:
                raise ValueError("A branch named '{}' already exists.".format(path[0]))
        else:
            self._branches[path[0]] = Tree()
        if len(path) == 2:
            self._branches[path[0]]._branch(path[1], overwrite=overwrite, nested=nested)

        return self._branches[path[0]]

    @staticmethod
    def _check_name(name):
        """filter acceptable element names"""
        try:
            assert isinstance(name, str) and name != ''
        except (AssertionError, IndexError):
            raise ValueError(("element names should be non-empty strings, "
                              "{} was provided").format(name))
        if name[0] == '_':
            raise ValueError(("element names should not start with an "
                              "underscore, {} was provided").format(name))

    def __getattr__(self, key):
        try:
            return self._branches[key]
        except KeyError:
            return self._leaves[key]

    def __getitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return self.__getattr__(key)
        else:
            return self._branches[path[0]].__getitem__(path[1])

    def __setattr__(self, key, value):
        """
        Set a new item in the tree.

        :param key:  must be a string, and can't start with an underscore.
        """
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        self._check_name(key)
        if self._freeze_struct_ and key not in self._leaves:
            raise ValueError("Can't modify the frozen structure of the tree")
        self._leaves[key] = value

    def __setitem__(self, key, value):
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        self._check_name(key)
        path = key.split('.', 1)

        if len(path) == 1:
            if self._freeze_struct_ and key not in self._leaves:
                raise ValueError("Can't modify the frozen structure of the tree")
            self._leaves[key] = value
        else:
            self._branches[path[0]].__setitem__(path[1], value)

    def __len__(self):
        """Return the number of direct branchs and leaves"""
        return len(self._branches) + len(self._leaves)

    def __contains__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return key in self._leaves or key in self._leaves
        else:
            return path[0] in self._branches and path[1] in self._branches[path[0]]

    def __delitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            try:
                del self._leaves[key]
            except KeyError:
                del self._branches[key]
        else:
            return self._branches[path[0]].__delitem__(path[1])

    def __delattr__(self, key):
        self._check_name(key)
        try:
            del self._leaves[key]
        except KeyError:
            del self._branches[key]

    def __iter__(self):
        """Iter over non-nested attributes."""
        for leaf in self._leaves.__iter__():
            yield leaf
        for branch in self._branches.__iter__():
            yield branch

    def __eq__(self, tree):
        return (self._leaves == tree._leaves
                and self._branches == tree._branches)



    def _freeze(self, recursive=True):
        object.__setattr__(self, "_freeze_", True)
        if recursive:
            for branch in self._branches.values():
                branch._freeze(recursive=True)

    def _unfreeze(self, recursive=True):
        object.__setattr__(self, "_freeze_", False)
        if recursive:
            for branch in self._branches.values():
                branch._unfreeze(recursive=True)

    def _freeze_struct(self, recursive=True):
        object.__setattr__(self, "_freeze_struct_", True)
        if recursive:
            for branch in self._branches.values():
                branch._freeze_struct(recursive=True)

    def _unfreeze_struct(self, recursive=True):
        object.__setattr__(self, "_freeze_struct_", False)
        if recursive:
            for branch in self._branches.values():
                branch._unfreeze_struct(recursive=True)

    def _update(self, tree, overwrite=True):
        """\
        Update the tree with values of another tree. If the other tree possess
        branches not present in this one (and structure is not frozen), those
        branches will be created as well.

        :param overwrite:  if False, value already present in the tree will not
                           be modified (default True).

        ..raise:: TypeError if the tree is frozen and an assignement is needed,
                  or the structure is frozen and an element of the other tree
                  is not present on this one. Branches will generate TypeError
                  based on their own frozen status, so it is possible to update
                  a frozen tree if assignement happen on an unfrozen branch.
        """
        if isinstance(tree, Tree):
            for key, value in tree._leaves.items():
                if key in self._leaves:
                    if overwrite:
                        self.__setattr__(key, value)
                else:
                    self.__setattr__(key, value)
            for branchname, branch in tree._branches.items():
                if branchname not in self._branches:
                    self._branch(branchname)
                self._branches[branchname]._update(branch, overwrite=overwrite)
        else:
            raise NotImplementedError
            for key, value in tree.items():
                pass

