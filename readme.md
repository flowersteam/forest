# trees

`trees` implements hierarchical dictionaries in python, with an attribute syntax.

    import trees
    t = trees.Tree()    
    
    t.a = 1
    t._newnode = 'b'
    t.b.c = 2

### Design
    
`Tree` was designed to hold configuration data, and has build-in constraints in order to avoid common bugs:

1. Tree nodes have to be explicitely declared.
2. Node and element names cannot start with an underscore.
3. Conversely, all `Tree` methods are prefixed with an underscore, ensuring a clean separation between the tree methods and the tree structure. 
4. While a `Tree` offers most of the functionality of a `dict`, it is not a drop-in replacement.
5. Two `Trees` can be combined, but it has to be done explicitely.

Most methods happen by default in a recursive manner on the node of the tree, but can be executed only on direct node and leaves.

### API 
