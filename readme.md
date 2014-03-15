# forest

`forest` is a python hierarchical configuration structure designed for scientific experiments.

    import forest

    t = trees.Tree()
    t.temperature = 10
    t._branch('experiment1')
    t.experiment1.duration = 3600.0

### Design

`forest` has been designed to be easy to use while ensuring data integrity. It features many ways to protect the tree data against badly programmed piece of code. Because the main goal of the library authors was to ensure that their scientific experiments were correct, some of the design choices led to an characteristically unpythonic interface.

#### Tree branches have to be explicitely declared

Is applies if you use to attribute interface. You can implicitly declare branch using the dict interface.

    import forest

    t = trees.Tree()
    t.temperature = 10
    t._branch('experiment1')
    t.experiment1.duration = 3600.0     # attribute interface
    t['experiment2.duration'] = 1800.0  # dict interface

#### Underscore are reserved to methods

Node and element names cannot start with an underscore. Inversely, all public methods start with an underscore. This ensure a clean separation between user-defined data and instance methods.

#### `Tree` is not a `dict`

It is not inherited from `dict` either. `Tree` offers most of the dict methods, but is not a drop-in replacement since their names are all prefixed with an underscore : `_update`, `_get`, `_setdefault`, etc.

#### Value can be validated when they are set.

They can be validated either by their type:

    t._isinstance('temperature', int)
    t.temperature = 10    # isinstance(10, int) is run
    t.temperature = "25"  # raises TypeError

Or using a custom defined function that returns `True` when check passes.

    def check_byte(value):
        return 0 <= value < 256

    t._validate('flag', check_bytes)
    t.flag = 150
    t.flag = 300 # raises TypeError
