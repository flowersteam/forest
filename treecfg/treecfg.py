"""
A tree module with dynamic attribute interface.
"""
from __future__ import print_function, division

import copy

class TreeCfg(object):
    """
    A TreeCfg is a set of elements, some of which are other TreeCfg.
    """

    def __init__(self):
        object.__setattr__(self, "_data", {})

    def _copy(self, deep=False):
        """convenience copy method

        :param deep:  if True, perform a deep copy
        """
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def _node(self, name, override=False, prefix=True):
        """
        Create a new node in the tree. Any node is a fully independent tree.
        Can create nested node in one call

        :param name:      the name of the node
        :param prefix:    if True, create intermediate nodes as needed.
                          Note that if override is True, existing intermediate nodes
                          will not be recreated.
        :raise KeyError:  if the node already exists, and override is False
        """
        self._check_name(name)
        path = name.split('.', 1)
        parent_node = self
        while len(path) == 2:
            if prefix and path[0] not in parent_node._data:
                parent_node._data[path[0]] = TreeCfg()
            parent_node = parent_node._data[path[0]]
            path = path[1].split('.', 1)


        if not override and path[0] in parent_node._data:
            raise KeyError(("an element with this name ({}) is already present"
                            " in the tree").format(path[0]))
        parent_node._data[path[0]] = TreeCfg()

    @staticmethod
    def _check_name(name):
        """filter acceptable element names"""
        try:
            assert type(name) is str and name[0] != '_'
        except (AssertionError, IndexError):
            raise ValueError(("element names should not start with an "
                              "underscore, {} was provided").format(name))

    def __getattr__(self, key):
        return self._data[key]

    def __getitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return self._data[key]
        else:
            return self._data[path[0]].__getitem__(path[1])

    def __setattr__(self, key, value):
        """
        Set a new item in the tree.

        :param key:  must be a string, and can't start with an underscore.
        """
        if key == '_newnode':
            return self._node(value)
        self._check_name(key)
        self._data[key] = value # key cannot contains dots here

    def __setitem__(self, key, value):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            self._data[key] = value
        else:
            self._data[path[0]].__setitem__(path[1], value)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return key in self._data
        else:
            return path[0] in self._data and path[1] in self._data[path[0]]

    def __delitem__(self, key):
        self._check_name(key)
        path = key.split('.', 1)
        if len(path) == 1:
            del self._data[key]
        else:
            return self._data[path[0]].__delitem__(path[1])

    def __delattr__(self, key):
        self._check_name(key)
        del self._data[key]
