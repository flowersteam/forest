"""
A tree structure with dynamic attribute interface.
"""
from __future__ import print_function, division

import collections
import copy
import re

# a unique object
_uid = object()
# valid keys and leaves names
_valid_leaf = re.compile("[A-Za-z][_a-zA-Z0-9]*$")
_valid_key  = re.compile("[A-Za-z][_a-zA-Z0-9]*(\.[A-Za-z][_a-zA-Z0-9]*)*$")

class Tree(object):
    """
    A Tree is a set of elements, some of which are other trees.
    """

    def __init__(self, tree=None, strict=False):
        """
        :param tree: an existing tree or dictionary to copy value from.
        """
        object.__setattr__(self, '_leaves_', {})
        object.__setattr__(self, '_isinstance_', {})
        object.__setattr__(self, '_validate_', {})
        object.__setattr__(self, '_docstrings_', {})
        object.__setattr__(self, '_coverage_', {})
        object.__setattr__(self, '_history_', {})
        object.__setattr__(self, '_branches_', {})
        object.__setattr__(self, '_freeze_', False)
        object.__setattr__(self, '_freeze_struct_', False)
        object.__setattr__(self, '_strict_', strict)
        if tree is not None:
            self._update(tree, overwrite=True)

    def __copy__(self):
        new_tree = Tree()
        object.__setattr__(new_tree, '_leaves_', self._leaves_)
        object.__setattr__(new_tree, '_isinstance_', self._isinstance_)
        object.__setattr__(new_tree, '_validate_', self._validate_)
        object.__setattr__(new_tree, '_docstrings_', self._docstrings_)
        object.__setattr__(new_tree, '_coverage_', self._coverage_)
        object.__setattr__(new_tree, '_history_', self._history_)
        object.__setattr__(new_tree, '_branches_', self._branches_)
        object.__setattr__(new_tree, '_freeze_', self._freeze_)
        object.__setattr__(new_tree, '_freeze_struct_', self._freeze_struct_)
        object.__setattr__(new_tree, '_strict_', self._strict_)
        return new_tree

    def __deepcopy__(self, memo):
        new_tree = Tree()
        memo[id(self)] = new_tree
        object.__setattr__(new_tree, '_leaves_', copy.deepcopy(self._leaves_, memo))
        object.__setattr__(new_tree, '_isinstance_', copy.deepcopy(self._isinstance_, memo))
        object.__setattr__(new_tree, '_validate_', copy.deepcopy(self._validate_, memo))
        object.__setattr__(new_tree, '_docstrings_', copy.deepcopy(self._docstrings_, memo))
        object.__setattr__(new_tree, '_coverage_', copy.deepcopy(self._coverage_, memo))
        object.__setattr__(new_tree, '_history_', copy.deepcopy(self._history_, memo))
        object.__setattr__(new_tree, '_branches_', copy.deepcopy(self._branches_, memo))
        object.__setattr__(new_tree, '_freeze_', self._freeze_)
        object.__setattr__(new_tree, '_freeze_struct_', self._freeze_struct_)
        object.__setattr__(new_tree, '_strict_', self._strict_)
        return new_tree

    def _copy(self, deep=False):
        """\
        Convenience copy method.

        :param deep:  if True, perform a deep copy
        """
        if deep:
            return self.__deepcopy__({})
        return self.__copy__()

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

    def _coverage(self, key):
        """Return the number of time the value of the key was accessed."""
        path = key.split('.', 1)
        if len(path) == 1:
            return self._coverage_[key]
        else:
            return self._branches_[path[0]]._coverage(path[1])

    def _history(self, key):
        """Return the successive values that the key was set to."""
        path = key.split('.', 1)
        if len(path) == 1:
            return self._history_[key]
        else:
            return self._branches_[path[0]]._history(path[1])

    def _branch(self, name, value=None, overwrite=False, nested=True):
        """\
        Create a new branch in the tree if it does not already exists.
        Can create nested branches.

        :param name:      the name of the branch
        :param value:     optionally, an existing `Tree` instance instead of creating
                          a new empty `Tree`.
        :param nested:    if True, create intermediate branchs as needed.
                          Note that if override is True, existing intermediate branchs
                          will not be recreated.
        :raise KeyError:  if leaf already exists with this name
        """
        if self._freeze_:
            raise ValueError("Can't add a branch to a frozen tree")
        if self._freeze_struct_:
            raise ValueError("Can't add a branch to a tree whose structure is frozen")
        self._check_key(name)
        path = name.split('.', 1)

        if len(path) == 2 and (not nested) and path[0] not in self._branches_:
            raise ValueError("Can't created non-existent intermediary branches with nested = False")
        if path[0] in self._leaves_:
            if len(path) == 1:
                raise ValueError("Can't create a branch named '{}': a leaf "
                                 "with that name already exists.".format(path[0]))
        elif (path[0] in self._docstrings_ or
              path[0] in self._validate_ or
              path[0] in self._isinstance_):
            raise ValueError("Can't create a branch named '{}': a leaf "
                                 "with that name is already described.".format(path[0]))
        else:
            if path[0] not in self._branches_.keys():
                if value is not None:
                    self._branches_[path[0]] = value
                else:
                    self._branches_[path[0]] = Tree(strict=self._strict_)
        if len(path) == 2:
            self._branches_[path[0]]._branch(path[1], value=value, overwrite=overwrite, nested=nested)

        return self._branches_[path[0]]

    def _isinstance(self, key, cls=_uid):
        path = key.split('.', 1)
        if len(path) == 1:
            if cls is not _uid:
                self._isinstance_[key] = cls
            return self._isinstance_.get(key, None)
        else:
            if path[0] not in self._branches_ and cls is not _uid:
                self._branch(path[0])
            return self._branches_[path[0]]._isinstance(path[1], cls)

    def _validate(self, key, validate=_uid):
        path = key.split('.', 1)
        if len(path) == 1:
            if validate is not _uid:
                self._validate_[key] = validate
            return self._validate_.get(key, None)
        else:
            if path[0] not in self._branches_ and validate is not _uid:
                self._branch(path[0])
            return self._branches_[path[0]]._validate(path[1], validate)

    def _docstring(self, key, docstring=_uid):
        path = key.split('.', 1)
        if len(path) == 1:
            if docstring is not _uid:
                self._docstrings_[key] = docstring
            return self._docstrings_.get(key, None)
        else:
            if path[0] not in self._branches_ and docstring is not _uid:
                self._branch(path[0])
            return self._branches_[path[0]]._docstring(path[1], docstring=docstring)

    def _default(self, key, default=_uid):
        path = key.split('.', 1)
        if len(path) == 1:
            if default is not _uid and key not in self:
                self[key] = default
            return self._get(key, None)
        else:
            if path[0] not in self._branches_ and validate is not _uid:
                self._branch(path[0])
            return self._branches_[path[0]]._default(path[1], default)


    def _describe(self, key, docstring=_uid, instanceof=_uid, validate=_uid, default=_uid):
        return (self._docstring(key, docstring),
                self._isinstance(key, instanceof),
                self._validate(key, validate),
                self._default(key, default))

    def _unset(self):
        """Return all described attributes that are not set"""
        notset = set(self._docstrings_.keys())
        notset.update(self._validate_.keys())
        notset.update(self._isinstance_.keys())
        notset.difference_update(self._leaves_.keys())
        for branchname, branch in self._branches_.items():
            notset.update(('{}.{}'.format(branchname, e) for e in branch._unset()))
        return notset

    def _check_value(self, key, value):
        """Check a value against defined instance and custom checks
        if the tree is strict, then a check must be defined
        """
        check_exists = False
        if key in self._isinstance_:
            if self._isinstance_[key] is not None:
                check_exists = True
                if not isinstance(value, self._isinstance_[key]):
                    raise TypeError(("value for leaf {} must be an instance of {};"
                                     " got {} instead.").format(key,
                                     self._isinstance_[key], type(value))) # TODO correct relative path error
        if key in self._validate_:
            if self._validate_[key] is not None:
                check_exists = True
                try:
                    check = self._validate_[key](value)
                except Exception:
                    check = False
                if not check:
                    raise TypeError(("value for leaf {} did not pass user-defined "
                                     "validating function").format(key)) # TODO correct relative path error
        if self._strict_ and not check_exists: # FIXME: is this the correct place to do this
            raise TypeError(("can't create new leaf '{}' in a strict tree without a "
                             "type or validation function declared.").format(key)) # TODO correct relative path error

    def _check(self, tree=None, struct=False):
        """Check conformity with another tree type checks and validate functions

        :param struct:      if True, verifies that both tree have the same branches
        :raises TypeError:  if check fails
        """
        if tree is None:
            tree = self
        for key, leaf in self._leaves_.items():
            tree._check_value(key, leaf)
        if struct and set(self._branches_.keys()) != set(tree._branches_.keys()):
            diff = set(self._branches_.keys()).symmetric_difference(set(tree._branches_.keys()))
            raise TypeError('({}) branches are not present in both trees'.format(diff)) # TODO: 2 differences instead of symmetric
        for key, branch in self._branches_.items():
            if key in tree._branches_:
                branch._check(tree._branches_[key], struct=struct)

    @staticmethod
    def _check_key(key, leaf=False):
        """filter acceptable element keys"""
        try:
            assert isinstance(key, str) and key != ''
        except AssertionError:
            raise ValueError(("element keys should be non-empty strings, "
                              "{} was provided").format(key))

        regex = _valid_key
        if leaf:
            regex = _valid_leaf
        if regex.match(key) is None:
            if key[0] == '_':
                raise ValueError(("leaf names should not start with an "
                                  "underscore, '{}' was provided").format(key))
            raise ValueError(("leaf not a valid attribute name, '{}'"
                              " was provided").format(key))

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
            self._check_key(key, leaf=True)
            try:
                return self._branches_[key]
            except KeyError:
                self._coverage_[key] = self._coverage_.get(key, 0) + 1
                return self._leaves_[key]
        except ValueError:
            object.__getattribute__(self, key)

    def __getitem__(self, key):
        self._check_key(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return self.__getattr__(key)
        else:
            return self._branches_[path[0]].__getitem__(path[1])

    def __setattr__(self, key, value):
        """
        Set a new item in the tree.

        :param key:  must be a string, and can't start with an underscore.
        """
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        self._check_key(key, leaf=True)
        if self._freeze_struct_ and key not in self._leaves_ and key not in self._branches_:
            raise ValueError("Can't modify the frozen structure of the tree")
        self._check_value(key, value)
        if isinstance(value, Tree):
            if key in self._leaves_:
                raise ValueError('branch cannot be added: a leaf already '
                                 'exists with name {}'.format(key))
            self._branches_[key] = value
        else:
            if key in self._branches_:
                raise ValueError('leaf cannot be added: a branch already '
                                 'exists with name {}'.format(key))
            self._history_.setdefault(key, [])
            self._history_[key].append(value)
            self._coverage_[key] = self._coverage_.get(key, 0)
            self._leaves_[key] = value

    def __setitem__(self, key, value):
        if self._freeze_:
            raise ValueError("Can't modify a frozen tree")
        self._check_key(key)
        path = key.split('.', 1)

        if len(path) == 1:
            self.__setattr__(key, value)
        else:
            if path[0] not in self._branches_:
                self._branch(path[0])
            self._branches_[path[0]].__setitem__(path[1], value)

    def _pop(self, key, d=_uid):
        """\
        Remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is
        raised.
        """
        self._check_key(key)
        path = key.split('.', 1)

        if len(path) == 1:
            if d != _uid:
                return self._leaves_.pop(key, d)
            else:
                return self._leaves_.pop(key)
        else:
            return self._branches_[path[0]]._pop(path[1], d)

    def _popitem(self):
        """\
        Remove and return a tuple (key, value) from the tree.

        :raise KeyError:  when tree is empty.

        ..note:: direct leaves will always be popped first.
        """

        if len(self._leaves_) > 0:
            return self._leaves_.popitem()
        else:
            for branchname, branch in self._branches_.items():
                try:
                    k, v = branch._popitem()
                    return ('{}.{}'.format(branchname, k), v)
                except KeyError:
                    pass
        raise KeyError('tree is empty')

    @classmethod
    def _fromkeys(cls, keys, value=None):
        """\
        Creates a new dictionary with keys from seq and values set to value.
        """
        t = cls()
        for key in keys:
            t[key] = value
        return t

    def _clear(self, struct=True, typecheck=False):
        """Remove all leaves and branch from the tree.

        :param struct:    if False, does not remove the branches.
        :param typecheck: if True, does remove the typecheck of the leaves.
                          Note that, as typecheck is kept locally in each node,
                          if struct is True and typecheck is False, only the typecheck
                          of the direct leaves will be kept.
        """
        self._leaves_.clear()
        for branch in self._branches_.values:
            branch._clear(struct=struct, typecheck=typecheck)
        if struct:
            self._branches_.clear()
        if typecheck:
            self._isinstance_.clear()
            self._validate.clear()

    # pop, popitem,

    def __len__(self):
        """Return the number of direct branchs and leaves""" #FIXME is that what we expect ?
        return len(self._branches_) + len(self._leaves_)

    def __contains__(self, key):
        self._check_key(key)
        path = key.split('.', 1)
        if len(path) == 1:
            return key in self._leaves_ or key in self._branches_
        else:
            return path[0] in self._branches_ and path[1] in self._branches_[path[0]]

    def __delitem__(self, key):
        self._check_key(key)
        path = key.split('.', 1)
        if len(path) == 1:
            try:
                del self._leaves_[key]
            except KeyError:
                del self._branches_[key]
        else:
            return self._branches_[path[0]].__delitem__(path[1])

    def __delattr__(self, key):
        self._check_key(key, leaf=True)
        try:
            del self._leaves_[key]
        except KeyError:
            del self._branches_[key]

    def __eq__(self, tree):
        return (self._leaves_ == tree._leaves_
                and self._branches_ == tree._branches_)

    def _freeze(self, freeze, recursive=True):
        """\
        Freeze and unfreeze the tree.

        We a tree is frozen, attributes can't be modified, created or deleted.
        :param freeze:     True for freezing, False for unfreezing
        :param recursive:  to apply the change on branches as well.
        """
        object.__setattr__(self, "_freeze_", freeze)
        if recursive:
            for branch in self._branches_.values():
                branch._freeze(freeze, recursive=True)

    def _freeze_struct(self, freeze, recursive=True):
        """\
        Freeze and unfreeze the branches.

        We a tree is frozen, branches can't be modified, created or deleted.
        :param freeze:     True for freezing, False for unfreezing
        :param recursive:  to apply the change on subbranches as well.
        """
        object.__setattr__(self, "_freeze_struct_", freeze)
        if recursive:
            for branch in self._branches_.values():
                branch._freeze_struct(freeze, recursive=True)

    def _strict(self, strict=True, recursive=True):
        """\
        Make a tree strict or not.

        In a strict tree, attributes cannot be created unless they have been
        described using the method `_describe()`. When the tree is made strict,
        existing leaves will be checked, and TypeError will be raised if not
        all are described.
        :param freeze:     True for strict, False for unstrict
        :param recursive:  to apply the change on subbranches as well.
        """
        object.__setattr__(self, "_strict_", strict)
        if recursive:
            for branch in self._branches_.values():
                branch._strict(strict, recursive=True)
        if strict:
            self._check()

    def _described_set(self, docstring=True):
        described = set(self._docstrings_.keys())
        described.update(self._validate_.keys())
        described.update(self._isinstance_.keys())
        for branchname, branch in self._branches_.items():
            described.update(('{}.{}'.format(branchname, e) for e in branch._described_set()))
        return described

    def _described(self, leaf=None, docstring=True):
        """\
        Return True if the leaf is described by a docstring, a instance check or
        a validation function.

        :param docstring:  if False, does not consider only a docstring a proper
                           description.
        """
        described = leaf in self._isinstance_ or leaf in self._validate_
        if docstring:
            described = described or leaf in self._docstrings_
        return described


    def _update(self, tree, overwrite=True, descriptions=True, described_only=False):
        """\
        Update the tree with values of another tree. If the other tree possess
        branches not present in this one (and structure is not frozen), those
        branches will be created as well.

        :param overwrite:      if False, value already present in the tree will not
                               be modified (default True).
        :param descriptions:   if True, copy the descriptions as well
        :param described_only: if True, only update leaves that are described in self,
                               or, if `description` is True, descriptions coming from
                               tree, as long a they don't necessitate new branches in
                               self (cheap way to avoid nasty loops).

        ..raise:: TypeError if the tree is frozen and an assignement is needed,
                  or the structure is frozen and an element of the other tree
                  is not present on this one. Branches will generate TypeError
                  based on their own frozen status, so it is possible to update
                  a frozen tree if assignement happen on an unfrozen branch.
        """
        if isinstance(tree, Tree):
            if descriptions:
                for key, value in tree._isinstance_.items():
                    if overwrite or key not in self._isinstance_:
                        self._isinstance_[key] = value
                for key, value in tree._validate_.items():
                    if overwrite or key not in self._validate_:
                        self._validate_[key] = value
                for key, value in tree._docstrings_.items():
                    if overwrite or key not in self._docstrings_:
                        self._docstrings_[key] = value

            for key, value in tree._leaves_.items():
                if not described_only or (described_only and self._described(key)):
                    if key in self._leaves_:
                        if overwrite:
                            self.__setattr__(key, value)
                    else:
                        self.__setattr__(key, value)

            for branchname, branch in tree._branches_.items():
                if branchname not in self._branches_:
                    if not described_only:
                        self._branch(branchname)
                    else:
                        continue
                self._branches_[branchname]._update(branch, overwrite=overwrite,
                                                            descriptions=descriptions,
                                                            described_only=described_only)
        else:
            if described_only:
                raise NotImplementedError
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

    def __iter__(self):
        """Iter over keys."""
        for key in self.keys():
            yield key

    def _keys(self):
        return (key for key, value in self._items())

    def _values(self):
        return (value for key, value in self._items())

    def _items(self):
        for item in self._leaves_.items():
            yield item
        for branchname, branch in self._branches_.items():
            for key, value in branch._items():
                yield ('{}.{}'.format(branchname, key), value)

    def __lt__(self, a):
        return NotImplemented

    def __le__(self, a):
        return NotImplemented

    def __ge__(self, a):
        return NotImplemented

    def __gt__(self, a):
        return NotImplemented

