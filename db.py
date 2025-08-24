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
        return self.tree.get_node(name)[1].value

    def delete_table(self, name: str):
        """
        Deletes the table with the given name.
        """
        self.tree.delete(name)

    def edit_table(self, name: str, new_table: AVLTable):
        """
        Edits table with the given name.
        """
        self.tree.edit(name, new_table)

    @staticmethod
    def to_dict(node: AVLTree.TreeNode) -> dict:
        """
        Transforms tree to a dict

        :param node: TreeNode
        :return: dict
        """
        if node is None:
            return {}

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
    def dict_to_tree(tree_dict: dict) -> AVLTree:
        """
        Transforms dict to a tree

        :param tree_dict: dict
        :return: AVLTree
        """
        if not tree_dict:
            return AVLTree()

        left = DB.dict_to_tree(tree_dict['left']) if tree_dict.get('left') else None
        right = DB.dict_to_tree(tree_dict['right']) if tree_dict.get('right') else None

        value = None
        if 'attrs' in tree_dict:
            value = AVLTable(tree_dict['attrs'])
            if isinstance(tree_dict['value'], dict) and 'left' in tree_dict['value']:
                val_info = tree_dict['value']
                value.insert(val_info['key'], val_info['value'])

        node = AVLTree.TreeNode(tree_dict['key'], value, left, right)
        tree = AVLTree(node)
        return tree

    @classmethod
    def read_json(cls, filename: str = 'db.json'):
        """
        Reads JSON and composes a tree

        :param filename: str
        :return: DB
        """
        try:
            with open(filename, 'r') as file:
                tree_dict = json.load(file)

            new_db = cls()
            new_db.tree = cls.dict_to_tree(tree_dict)
            return new_db

        except Exception as e:
            print('Error occurred during reading file: ', e)
