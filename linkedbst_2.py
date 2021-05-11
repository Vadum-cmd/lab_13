"""
File: linkedbst.py
Author: Ken Lambert
"""
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from time import time
from random import randint


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""
    def __init__(self, sourceCollection=None):
        """
        Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present.
        """
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """
        Returns a string representation with the tree rotated
        90 degrees counterclockwise.
        """
        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "- " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """
        If item matches an item in self, returns the
        matched item, or None otherwise.
        """

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        # Helper function to search for item's position
        def recurse(node):
            """New item is less, go left until spot is found."""
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            """
            Replace top's datum with the maximum datum in the left subtree
            Pre:  top has a left child
            Post: the maximum node in top's left subtree
                  has been removed
            Post: top.data = maximum value in top's left subtree.
            """
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:
            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            # Check if this node even exists.
            if not top:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        result = self.height() < (2 * log(self._size + 1, 2) - 1)
        return result

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        temp_lst = []
        for element in self:
            if low <= element <= high:
                temp_lst.append(element)
        return list(sorted(temp_lst))

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        # So, we just make temporary list for all the words in our tree.
        temp_lst = [element for element in self]
        # Make the original one empty.
        self.clear()

        def insert_item(temp_lst):
            """
            This function divides 'temp_lst' by 2 to define the root,
            then, recursively, adds another nodes to our binary tree.
            """
            middle_ind = len(temp_lst) // 2

            if len(temp_lst) == 0:
                return None

            self.add(temp_lst[middle_ind])
            insert_item(temp_lst[ : middle_ind])
            insert_item(temp_lst[middle_ind + 1 : ])

        insert_item(temp_lst)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # It just must be the bigest number.
        successor = 9999999
        for element in self:
            if element > item and element < successor:
                successor = element
        return successor if successor != 9999999 else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # It just must be the smallest number.
        predecessor = -9999999
        for element in self:
            if element < item and element > predecessor:
                predecessor = element
        return predecessor if predecessor != -9999999 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # Firs of all we open file using given path.
        # Then we read it's content and put it in list.
        with open(path) as words:
            words_lst = words.readlines()[:900]
        length = len(words_lst)
        # Creating an sorted list with our content.
        lst_of_words_sort = list(sorted(words_lst))
        # Creating new binary tree obj. Preparing to fill it with our content, but unsorted.
        tree_of_words_unsort = LinkedBST()

        for word in words_lst:
            # Filling it up with our content from ordinary list of words.
            tree_of_words_unsort.add(word)

        # Based on sorted list of words creating sorted binary tree.
        tree_of_words_sort = LinkedBST(lst_of_words_sort)
        # This tree is sorted and additionaly rebalanced.
        tree_of_words_bal = LinkedBST(lst_of_words_sort).rebalance()
        # Defining, which words we will be searching.
        random_indices = [randint(0, length-1) for num in range(10000)]
        # Just defining start time of all trees and lists to zero.
        lst_of_words_sort_time = 0
        tree_of_words_unsort_time = 0
        tree_of_words_sort_time = 0
        tree_of_words_bal_time = 0

        for ind in random_indices:
            word = words_lst[ind]

            # ---------------------------------
            # Searching in sorted list.
            # ---------------------------------
            # Defining start time.
            rght_now = time()
            # Searching the word.
            index = lst_of_words_sort.index(word)
            # Defining, how much time did pass.
            lst_of_words_sort_time += time() - rght_now

            # ---------------------------------
            # Searching in unsorted binary tree.
            # ---------------------------------
            # Defining start time.
            rght_now = time()
            # Searching the word.
            word = tree_of_words_unsort.find(word)
            # Defining, how much time did pass.
            tree_of_words_unsort_time += time() - rght_now

            # ---------------------------------
            # Searching in sorted binary tree.
            # ---------------------------------
            # Defining start time.
            rght_now = time()
            # Searching the word.
            word = tree_of_words_sort.find(word)
            # Defining, how much time did pass.
            tree_of_words_sort_time += time() - rght_now

            # ---------------------------------
            # Searching in balanced binary tree.
            # ---------------------------------
            # Defining start time.
            rght_now = time()
            # Searching the word.
            word = tree_of_words_bal.find(word)
            # Defining, how much time did pass.
            tree_of_words_bal_time += time() - rght_now

        # Printing the results.
        print(f"Sorted list: found 10000 random words in {lst_of_words_sort_time//10**3} miliseconds." )
        print(f"Unsorted tree: found 10000 random words in {tree_of_words_unsort_time//10**3} miliseconds." )
        print(f"Sorted tree: found 10000 random words in {tree_of_words_sort_time//10**3} miliseconds." )
        print(f"Balanced tree: found 10000 random words in {tree_of_words_bal_time//10**3} miliseconds." )
