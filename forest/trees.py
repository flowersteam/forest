"""
A tree structure with dynamic attribute interface.
"""
from __future__ import print_function, division

import copy

# a unique object
_uid = object()


class Tree(object):
    """
    A Tree is a set of elements, some of which are other trees.
    """

    def __init__(self, existing=None):
        """
        :param existing: an existing tree or dictionary.
        """
        object.__setattr__(self, '_leaves', {})
        object.__setattr__(self, '_instance_check', {})
        object.__setattr__(self, '_validate_check', {})
        object.__setattr__(self, '_docstrings', {})
        object.__setattr__(self, '_branches', {})
        object.__setattr__(self, '_freeze_', False)
        object.__setattr__(self, '_freeze_struct_', False)
        object.__setattr__(self, '_strictmode', False)
        if existing is not None:
            self._update(existing, overwrite=True)

    @classmethod
    def _from_file(cls, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        d = {}
        for line in lines:
            try:
                key, value = line.split('=')
                key = key.strip()
                value = eval(value.strip(), {}, {})
                d[key] = value
            except ValueError:
                pass
        t = cls()
        t._update(d, overwrite=True)
        return t

    def _to_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join(line for line in self._lines()))

    def _copy(self, deep=False):
        """convenience copy method

        :param deep:  if True, perform a deep copy
        """
        if deep:
            return self.__deepcopy__()
        return self.__copy__()

    def __copy__(self):
        new_tree = Tree()
        object.__setattr__(new_tree, '_leaves', self._leaves)
        object.__setattr__(new_tree, '_instance_check', self._instance_check)
        object.__setattr__(new_tree, '_validate_check', self._validate_check)
        object.__setattr__(new_tree, '_branches', self._branches)
        object.__setattr__(new_tree, '_freeze_', self._freeze_)
        object.__setattr__(new_tree, '_freeze_struct_', self._freeze_struct_)
        object.__setattr__(new_tree, '_strictmode', self._strictmode)
        return new_tree

    def __deepcopy__(self):
        new_tree = Tree()
        object.__setattr__(new_tree, '_leaves', copy.deepcopy(self._leaves))
        object.__setattr__(new_tree, '_instance_check', copy.deepcopy(self._instance_check))
        object.__setattr__(new_tree, '_validate_check', copy.deepcopy(self._validate_check))
        object.__setattr__(new_tree, '_branches', {key: b.__deepcopy__() for key, b in self._branches.items()})
        object.__setattr__(new_tree, '_freeze_', self._freeze_)
        object.__setattr__(new_tree, '_freeze_struct_', self._freeze_struct_)
        object.__setattr__(new_tree, '_strictmode', self._strictmode)
        return new_tree

    def _branch(self, name, overwrite=False, nested=True):
        """
        Create a new branch in the tree if it does not already exists.
        Can create nested branches.

        :param name:      the name of the branch
        :param nested:    if True, create intermediate branchs as needed.
                          Note that if override is True, existing intermediate branchs
                          will not be recreated.
        :raise KeyError:  if leaf already exists with this name
        """
        if self._freeze_:
            raise ValueError("Can't add a branch to a frozen tree")
        if self._freeze_struct_:
            raise ValueError("Can't add a branch to a tree whose structure is frozen")
        self._check_name(name)
        path = name.split('.', 1)

        if len(path) == 2 and (not nested) and path[0] not in self._branches:
            raise ValueError("Can't created non-existent intermediary branches with nested = False")
        if path[0] in self._leaves:
            if len(path) == 1:
                raise ValueError("Can't create a branch named '{}': a leaf "
                                 "with that name already exists.".format(path[0]))
        else:
            if path[0] not in self._branches.keys():
                self._branches[path[0]] = Tree()
        if len(path) == 2:
            self._branches[path[0]]._branch(path[1], overwrite=overwrite, nested=nested)

        return self._branches[path[0]]

    def _isinstance(self, name, cls=_uid):
        path = name.split('.', 1)
        if len(path) == 1:
            if cls is not _uid:
                self._instance_check[name] = cls
            return self._instance_check.get(name, None)
        else:
            return self._branches[path[0]]._isinstance(path[1], cls)

    def _validate(self, name, validate=_uid):
        path = name.split('.', 1)
        if len(path) == 1:
            if validate is not _uid:
                self._validate_check[name] = validate
            return self._validate_check.get(name, None)
        else:
            return self._branches[path[0]]._validate(path[1], validate)

    def _docstring(self, name, docstring=_uid):
        path = name.split('.', 1)
        if len(path) == 1:
            if docstring is not _uid:
                self._docstrings[name] = docstring
            return self._docstrings.get(name, None)
        else:
            return self._branches[path[0]]._docstring(path[1], docstring=docstring)

    def _describe(self, name, docstring=_uid, instanceof=_uid, validate=_uid):
        return (self._docstring(name, docstring),
                self._isinstance(name, instanceof),
                self._validate(name, validate))

    def _check_value(self, name, value):
        """Check a value against defined instance and custom checks
        if the tree is strict, then a check must be defined
        """
        check_exists = False
        if name in self._instance_check:
            if self._instance_check[name] is not None:
                check_exists = True
                if not isinstance(value, self._instance_check[name]):
                    raise TypeError(("value for leaf {} must be an instance of {};"
                                     " got {} instead.").format(name,
                                     self._instance_check[name], type(value))) # TODO correct relative path error
        if name in self._validate_check:
            if self._validate_check[name] is not None:
                check_exists = True
                try:
                    check = self._validate_check[name](value)
                except Exception:
                    check = False
                if not check:
                    raise TypeError(("value for leaf {} did not pass user-defined "
                                     "validating function").format(name)) # TODO correct relative path error
        if self._strictmode and not check_exists:
            raise TypeError(("can't create new leaf '{}' in a strict tree without a "
                             "type or validation function declared.").format(name)) # TODO correct relative path error


    def _strict(self, state=True):
        object.__setattr__(self, "_strictmode", state)

    def _check(self, tree, struct=False):
        """Check conformity with another tree type checks and validate functions

        :param struct:      if True, verifies that both tree have the same branches
        :raises TypeError:  if check fails
        """
        for key, leaf in self._leaves.items():
            tree._check_value(key, leaf)
        if struct and set(self._branches.keys()) != set(tree._branches.keys()):
            diff = set(self._branches.keys()).symmetric_difference(set(tree._branches.keys()))
            raise TypeError('({}) branches are not present in both trees'.format(diff)) # TODO: 2 differences instead of symmetric
        for key, branch in self._branches.items():
            if key in tree._branches:
                branch._check(tree._branches[key], struct=struct)

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


    def _get(self, key, default):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def _setdefault(self, key, value):
        if key not in self:
            self[key] = value

    def __getattr__(self, key):
        try:
            self._check_name(key)
            try:
                return self._branches[key]
            except KeyError:
                return self._leaves[key]
        except ValueError:
            object.__getattribute__(self, key)

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
        if self._freeze_struct_ and key not in self._leaves and key not in self._branches:
            raise ValueError("Can't modify the frozen structure of the tree")
        self._check_value(key, value)
        if isinstance(value, Tree):
            if key in self._leaves:
                raise ValueError('branch cannot be added: a leaf already '
                                 'exists with name {}'.format(key))
            self._branches[key] = value
        else:
            if key in self._branches:
                raise ValueError('leaf cannot be added: a branch already '
                                 'exists with name {}'.format(key))
            self._leaves[key] = value

    def __setitem__(self, key, value):
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        self._check_name(key)
        path = key.split('.', 1)

        if len(path) == 1:
            self.__setattr__(key, value)
        else:
            if path[0] not in self._branches:
                # TODO correct message branch name
                assert path[0] not in self._leaves, "Can't create branch {}, a leaf already exists with that name".format(path[0])
                self._branches[path[0]] = Tree()
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
            if not overwrite:
                for key, value in tree.items():
                    if not key in self:
                        self[key] = value
            else:
                for key, value in tree.items():
                    self[key] = value

    def _lines(self):
        lines = []
        for key, value in self._items():
            try:
                r = value.__repr__()
            except (AttributeError, TypeError):
                r = value
            lines.append('{}={}'.format(key, r))
        return lines

    def __str__(self):
        return '\n'.join(line for line in self._lines())

    def _keys(self):
        return (key for key, value in self._items())

    def _values(self):
        return (value for key, value in self._items())

    def _items(self):
        for item in self._leaves.items():
            yield item
        for branchname, branch in self._branches.items():
            for key, value in branch._items():
                yield ('{}.{}'.format(branchname, key), value)
