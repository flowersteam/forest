import copy

class TreeCfg(object):

    def __init__(self, tc=None):
        object.__setattr__(self, "_data", {})

    def _deepcopy(self, tc):
        return copy.deepcopy(tc)

    def _copy(self, tc):
        return copy.copy(tc)

    def _node(self, name, override=False):
        """
        Create a new node in the tree. Any node is a fully independent tree.

        :param name:      the name of the node
        :raise KeyError:  if the node already exists, and override is False
        """
        self._check_name(name)
        if not override and name in self._data:
            raise KeyError("an element with this name ({}) is already present in the tree".format(name))
        self._data[name] = TreeCfg()

    def _check_name(self, name):
        try:
            assert type(name) is str and name[0] != '_'
        except (AssertionError, IndexError):
            raise ValueError("element names should not start with an underscore, {} was provided".format(key))

    def __getattr__(self, key):
        return self._data[key]

    def __setattr__(self, key, value):
        """
        Set a new item in the tree.

        :param key:  must be a string, and can't start with an underscore.
        """
        if key == '_newnode':
            return self._node(value)
        self._check_name(key)
        self._data[key] = value
