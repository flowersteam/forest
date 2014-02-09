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
        object.__setattr__(self, "_nodes", {})
        object.__setattr__(self, "_freeze_", False)
        object.__setattr__(self, "_freeze_struct_", False)

    def _copy(self, deep=False):
        """convenience copy method

        :param deep:  if True, perform a deep copy
        """
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def _node(self, name, overwrite=False, nested=True):
        """
        Create a new node in the tree. Any node is a fully independent tree.
        Can create nested node in one call

        :param name:      the name of the node
        :param nested:    if True, create intermediate nodes as needed.
                          Note that if override is True, existing intermediate nodes
                          will not be recreated.
        :raise KeyError:  if a node or leaf already exists with this name,
                          and overwrite is False
        """
        if self._freeze_:
            raise ValueError("Can't add a node to a frozen tree")
        if self._freeze_struct_:
            raise ValueError("Can't add a node to a tree whose structure is frozen")
        self._check_name(name)
        path = name.split('.', 1)
        parent_node = self
        while len(path) == 2:
            if nested and path[0] not in parent_node._nodes:
                parent_node._nodes[path[0]] = Tree()
            parent_node = parent_node._nodes[path[0]]
            path = path[1].split('.', 1)


        if not overwrite and path[0] in parent_node._nodes:
            raise KeyError(("an node with this name ({}) is already present"
                            " in the tree").format(name))
        if path[0] in parent_node._leaves:
            if not overwrite:
                raise KeyError(("an leaf with this name ({}) is already present"
                                " in the tree").format(name))
            else:
                del self._leaves[path[0]]

        parent_node._nodes[path[0]] = Tree()

    @staticmethod
    def _check_name(name):
        """filter acceptable element names"""
        try:
            assert type(name) is str and name[0] != '_'
        except (AssertionError, IndexError):
            raise ValueError(("element names should not start with an "
                              "underscore, {} was provided").format(name))

    def __getattr__(self, key):
        try:
            return self._nodes[key]
        except KeyError:
            return self._leaves[key]

    def __getitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return self.__getattr__(key)
        else:
            return self._nodes[path[0]].__getitem__(path[1])

    def __setattr__(self, key, value):
        """
        Set a new item in the tree.

        :param key:  must be a string, and can't start with an underscore.
        """
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        if key == '_newnode':
            return self._node(value)
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
            self._nodes[path[0]].__setitem__(path[1], value)

    def __len__(self):
        """Return the number of direct nodes and leaves"""
        return len(self._nodes) + len(self._leaves)

    def __contains__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return key in self._leaves or key in self._leaves
        else:
            return path[0] in self._nodes and path[1] in self._nodes[path[0]]

    def __delitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            try:
                del self._leaves[key]
            except KeyError:
                del self._nodes[key]
        else:
            return self._nodes[path[0]].__delitem__(path[1])

    def __delattr__(self, key):
        self._check_name(key)
        try:
            del self._leaves[key]
        except KeyError:
            del self._nodes[key]

    def __iter__(self):
        """Iter over non-nested attributes."""
        for e in self._leaves.__iter__():
            yield e
        for e in self._nodes.__iter__():
            yield e

    def _freeze(self, recursive=True):
        object.__setattr__(self, "_freeze_", True)
        if recursive:
            for node in self._nodes.values():
                node._freeze(recursive=True)

    def _unfreeze(self, recursive=True):
        object.__setattr__(self, "_freeze_", False)
        if recursive:
            for node in self._nodes.values():
                node._unfreeze(recursive=True)

    def _freeze_struct(self, recursive=True):
        object.__setattr__(self, "_freeze_struct_", True)
        if recursive:
            for node in self._nodes.values():
                node._freeze_struct(recursive=True)

    def _unfreeze_struct(self, recursive=True):
        object.__setattr__(self, "_freeze_struct_", False)
        if recursive:
            for node in self._nodes.values():
                node._unfreeze_struct(recursive=True)

