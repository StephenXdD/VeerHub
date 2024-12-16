class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def get_all_nodes(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        return nodes

    def get_previous(self, current_node):
        return current_node.prev

    def get_next(self, current_node):
        return current_node.next