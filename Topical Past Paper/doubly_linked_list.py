import random


class Node:
    """
    A node in the doubly linked list.
    """
    def __init__(self, data):
        self.data = data  # Store (question_path, answer_path) tuple
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    A doubly linked list to store and navigate PDF paths.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, question_path, answer_path):
        """
        Add a new node with the given data (question and answer paths).
        """
        new_node = Node((question_path, answer_path))
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def shuffle(self):
        """
        Shuffle the doubly linked list nodes randomly.
        """
        nodes = self.get_all_nodes()
        random.shuffle(nodes)

        self.head = None
        self.tail = None
        for node in nodes:
            self.append(*node.data)

    def get_all_nodes(self):
        """
        Return a list of all nodes in the linked list.
        """
        current = self.head
        nodes = []
        while current:
            nodes.append(current)
            current = current.next
        return nodes

    def get_previous(self, node):
        """
        Get the previous node of the current node.
        """
        return node.prev if node and node.prev else None

    def get_next(self, node):
        """
        Get the next node of the current node.
        """
        return node.next if node and node.next else None
