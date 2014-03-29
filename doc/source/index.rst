:class:`forest.Tree` class
==========================

.. automodule:: forest

The motor classes all inherit from the :class:`Tree` class. The end-user class use multiple inheritance to adapt to the model specificities.

.. autoclass:: Tree
   :members:
   :undoc-members:
   :member-order: bysource


   Creating trees

   .. automethod:: __init__
   .. automethod:: _copy
   .. automethod:: _fromkeys
   .. automethod:: _from_file
   .. automethod:: _to_file
   

   Creating and modifying branches and leaves

   .. automethod:: _branch
   .. automethod:: _setdefault
   .. automethod:: _pop
   .. automethod:: _popitem
   .. automethod:: _clear
   .. automethod:: _update

   Accessing leaves

   .. automethod:: _get
   .. automethod:: _keys 
   .. automethod:: _values
   .. automethod:: _items


   Defining constraints

   .. automethod:: _freeze
   .. automethod:: _freeze_struct
   .. automethod:: _strict
   .. automethod:: _describe
   .. automethod:: _isinstance
   .. automethod:: _validate
   .. automethod:: _docstring


   Self check methods

   .. automethod:: _unset
   .. automethod:: _check
   .. automethod:: _coverage
   .. automethod:: _history


   Internal methods

   .. automethod:: _check_value
   .. automethod:: _check_key
   .. automethod:: _lines

