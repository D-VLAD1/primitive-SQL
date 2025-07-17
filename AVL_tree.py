"""
The AVL Tree implementation
"""

from collections import deque


class AVLTree:
    class TreeNode:
        def __init__(self, value, left=None, right=None):
            """
            Initializes a tree node with a value and optional left and right children.
            """
            self.value = value
            self.left = left
            self.right = right

        def __repr__(self):
            """
            Returns a string representation of the node (its value).
            """
            return str(self.value)

        @staticmethod
        def get_height(node):
            """
            Returns the height of a node. If the node is None, returns 0.
            """
            return node.height if node else 0

        @property
        def height(self):
            """
            Calculates the height of the current node based on its children.
            """
            return 1 + max(self.get_height(self.left), self.get_height(self.right))

        @property
        def balance(self):
            """
            Computes the balance factor of the node: left height - right height.
            """
            return self.get_height(self.left) - self.get_height(self.right)

    def __init__(self, root=None):
        """
        Initializes an empty AVL tree or sets the root if provided.
        """
        self.root = root

    def balance(self, visited: deque):
        """
        Rebalances the AVL tree after insertions or deletions.
        Takes a deque of visited nodes from the modification path.
        Applies rotations from the bottom up to maintain AVL property.
        """
        def left_rotate(x: 'AVLTree.TreeNode') -> 'AVLTree.TreeNode':
            y = x.right
            t2 = y.left
            y.left = x
            x.right = t2
            return y

        def right_rotate(x: 'AVLTree.TreeNode') -> 'AVLTree.TreeNode':
            y = x.left
            t2 = y.right
            y.right = x
            x.left = t2
            return y

        def rotate(node: 'AVLTree.TreeNode') -> 'AVLTree.TreeNode':
            if node.balance > 1:
                if node.left.balance < 0:
                    node.left = left_rotate(node.left)
                return right_rotate(node)
            elif node.balance < -1:
                if node.right.balance > 0:
                    node.right = right_rotate(node.right)
                return left_rotate(node)
            return node

        prev_visited = visited.copy()
        prev_visited.popleft()
        prev_visited.append(None)

        for curr, prev in zip(visited, prev_visited):
            if curr is None:
                break
            subtree = rotate(curr)
            if prev is None:
                self.root = subtree
            elif prev.left == curr:
                prev.left = subtree
            elif prev.right == curr:
                prev.right = subtree

    def get_node(self, value) -> tuple[TreeNode, TreeNode] | tuple[None, None]:
        """
        Finds the node with the given value.
        Returns a tuple of (parent, node) if found, or (None, None) if not found.
        """
        curr = self.root
        while True:
            if curr is None:
                return None, None
            if curr.left and curr.left.value == value:
                return curr, curr.left
            if curr.right and curr.right.value == value:
                return curr, curr.right
            if value <= curr.value:
                curr = curr.left
            else:
                curr = curr.right

    def insert_value(self, value):
        """
        Inserts a new value into the AVL tree.
        Raises ValueError if the value already exists.
        Automatically rebalances the tree after insertion.
        """
        if self.root is None:
            self.root = self.TreeNode(value)
            return

        if self.get_node(value) != (None, None):
            raise ValueError('The element already exists!')

        curr, visited = self.root, deque([])
        while True:
            visited.appendleft(curr)
            if curr.value < value:
                if curr.right is None:
                    curr.right = self.TreeNode(value)
                    break
                curr = curr.right
            else:
                if curr.left is None:
                    curr.left = self.TreeNode(value)
                    break
                curr = curr.left

        self.balance(visited)

    def delete_value(self, value):
        """
        Deletes the node with the specified value from the AVL tree.
        Handles standard BST deletion cases (0, 1, or 2 children).
        Rebalances the tree after deletion.
        """
        def get_successor(node: 'AVLTree.TreeNode') -> 'AVLTree.TreeNode':
            """
            Finds and returns the in-order successor (leftmost node of right subtree).
            """
            curr = node.right
            while curr.left:
                curr = curr.left
            return curr

        def delete(node: 'AVLTree.TreeNode', value):
            if node is None:
                return None

            visited.appendleft(node)

            if value < node.value:
                node.left = delete(node.left, value)
            elif value > node.value:
                node.right = delete(node.right, value)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    successor = get_successor(node)
                    node.value = successor.value
                    node.right = delete(node.right, successor.value)

            return node

        visited = deque([])
        self.root = delete(self.root, value)
        self.balance(visited)

