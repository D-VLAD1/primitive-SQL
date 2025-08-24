"""
The AVL Tree implementation
"""

from collections import deque


class AVLTree:
    class TreeNode:
        def __init__(self, key, value, left=None, right=None):
            """
            Initializes a tree node with a value and optional left and right children.
            """
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __repr__(self):
            """
            Returns a string representation of the node (its value).
            """
            return str(self.key)

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

    def get_node(self, key) -> tuple[TreeNode, TreeNode] | tuple[None, None]:
        """
        Finds the node with the given value.
        Returns a tuple of (parent, node) if found, or (None, None) if not found.
        """
        curr = self.root
        prev = None
        while True:
            if curr is None:
                return prev, None
            if curr.key == key:
                return prev, curr
            elif key <= curr.key:
                curr = curr.left
            else:
                curr = curr.right
            prev = curr

    def insert(self, key, value):
        """
        Inserts a new value into the AVL tree.
        Raises ValueError if the value already exists.
        Automatically rebalances the tree after insertion.
        """
        if self.root is None:
            self.root = self.TreeNode(key, value)
            return

        if self.get_node(key) != (None, None):
            raise ValueError('The element already exists!')

        new_node = self.TreeNode(key, value)
        curr, visited = self.root, deque([])
        while True:
            visited.appendleft(curr)
            if curr.key < key:
                if curr.right is None:
                    curr.right = new_node
                    break
                curr = curr.right
            else:
                if curr.left is None:
                    curr.left = new_node
                    break
                curr = curr.left

        self.balance(visited)

    def delete(self, key):
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

        def delete(node: 'AVLTree.TreeNode', key):
            if node is None:
                return None

            if key < node.key:
                node.left = delete(node.left, key)
                visited.appendleft(node)
            elif key > node.key:
                node.right = delete(node.right, key)
                visited.appendleft(node)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    successor = get_successor(node)
                    node.key, node.value = successor.key, successor.value
                    node.right = delete(node.right, successor.key)

            return node

        visited = deque([])
        self.root = delete(self.root, key)
        if visited:
            self.balance(visited)

    def edit(self, key: str, new_node):
        prev_old_node, old_node = self.get_node(key)
        if old_node is None:
            raise ValueError("The element doesn't exists!")

        new_node.left, new_node.right = old_node.left, old_node.right
        if prev_old_node is None:
            self.root = new_node
            return

        if prev_old_node.left == old_node: prev_old_node.left = new_node
        else: prev_old_node.right = new_node


class AVLTable(AVLTree):
    def __init__(self, attrs: list, root=None):
        super().__init__(root)
        self.attrs = attrs

    def insert(self, key, values: dict):
        if not (len(self.attrs) == len(values) and all(val in self.attrs for val in values)):
            raise ValueError("Values doesn't fit.")

        super().insert(key, values)
