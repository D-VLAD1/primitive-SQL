"""
The DataBase object implementation
"""
from AVL_tree import AVLTable, AVLTree
import json


class DB:
    def __init__(self, tree=AVLTree()):
        """
        Initializes the DB with an empty AVLTree to store tables.
        """
        self.tree = tree

    def insert_table(self, name: str, attrs: list[str]):
        """
        Adds a new table with the given name and attributes.
        """
        table = AVLTable(attrs)
        self.tree.insert(name, table)

    def get_table(self, name: str) -> AVLTable:
        """
        Retrieves the table with the given name.
        """
        return self.tree.get_node(name).value

    def delete_table(self, name: str):
        """
        Deletes the table with the given name.
        """
        self.tree.delete(name)

    @staticmethod
    def to_dict(node) -> dict | None:
        """
        Transforms tree to a dict

        :param node: TreeNode
        :return: dict
        """
        if node is None:
            return None

        output = {
            'key': node.key,
            'value': DB.to_dict(node.value.root) if isinstance(node.value, AVLTable) else node.value,
            'left': DB.to_dict(node.left),
            'right': DB.to_dict(node.right)
        }

        if isinstance(node.value, AVLTable):
            output['attrs'] = node.value.attrs

        return output

    def to_json(self, filename: str = 'db.json'):
        """
        Writes tree representation in JSON file

        :param filename: str
        :return: None
        """
        tree_dict = self.to_dict(self.tree.root)
        with open(filename, 'w') as file:
            json.dump(tree_dict, file, indent=4)

    @staticmethod
    def dict_to_tree(tree_dict: dict) -> AVLTree.TreeNode:
        """
        Transforms dict to a tree

        :param tree_dict: dict
        :return: TreeNode
        """
        left = DB.dict_to_tree(tree_dict['left']) if isinstance(tree_dict['left'], dict) and 'left' in tree_dict['left'] else tree_dict['left']
        right = DB.dict_to_tree(tree_dict['right']) if isinstance(tree_dict['right'], dict) and 'left' in tree_dict['right'] else tree_dict['right']

        value = AVLTable(tree_dict['attrs'])
        if isinstance(tree_dict['value'], dict) and 'left' in tree_dict['value']:
            val_info = tree_dict['value']
            value.insert(val_info['key'], val_info['value'])

        node = AVLTree.TreeNode(tree_dict['key'], value, left, right)
        return node

    @classmethod
    def read_json(cls, filename: str = 'db.json'):
        """
        Reads JSON and composes a tree

        :param filename: str
        :return: DB
        """
        with open(filename, 'r') as file:
            tree_dict = json.load(file)

        new_db = cls()
        new_db.tree = cls.dict_to_tree(tree_dict)
        return new_db
