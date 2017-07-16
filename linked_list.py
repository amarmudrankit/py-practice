import random
import sys
from enum import Enum
import copy

class Node(object):

	def __init__(self, key, val):
		self.key  = key
		self.val  = val
		self.next = None

class SinglyLinkedList(object):

	def __init__(self):
		self.head = None
		self.num_nodes = 0

	def size(self):
		self.num_nodes = 0
		current = self.head
		while current is not None:
			self.num_nodes += 1
			current = current.next

		return self.num_nodes

	def get_tail_node(self):
		if self.head == None:
			return None

		current = self.head
		while current.next != None:
			current = current.next

		return current

	def find_node_at_pos(self, pos):
		if pos > self.num_nodes:
			return self.get_tail_node()

		count = 1
		current = self.head
		while count < pos:
			current = current.next
			count += 1

		return current

	def delete(self, key):
		prev, node = self.search(key)
		if node == None:
			print("Key not found: " + str(key))
			return

		if prev == None:
			self.head = node.next
		else:
			prev.next = node.next
		del node

	def search(self, key):
		current = self.head
		prev = None
		while current != None:
			if current.key == key:
				return [prev, current]

			prev = current
			current = current.next

		return [None, None]

	def print_reverse(self, node):
		if self.num_nodes > 1000:
			print("Total number of nodes:", self.num_nodes)
			return

		if node == None:
			return

		self.print_reverse(node.next)
		print(str(node.key), end = ' --> ')

	def print(self, force = False):
		if force == False and self.num_nodes > 1000:
			print("Total number of nodes:", self.num_nodes)
			return

		current = self.head
		while current != None:
			arrow = ""
			if current.next != None:
				arrow = " --> "
			print(str(current.key), arrow, end = '')
			current = current.next
		print("EOL")

	def reverse(self):
		current = self.head
		prev = None
		while current != None:
			next_node = current.next
			current.next = prev
			prev = current
			current = next_node

		self.head = prev

	def has_loop(self):
		if self.head == None:
			return False

		ptr1 = self.head
		ptr2 = self.head
		while ptr1 is not None and ptr2 is not None:
			ptr1 = ptr1.next
			ptr2 = ptr2.next
			if ptr2 == None:
				return False
			ptr2 = ptr2.next

			if ptr1 == ptr2:
				return True

		return False

class SimpleList(SinglyLinkedList):

	def insert_head(self, node):
		node.next = self.head
		self.head = node
		self.num_nodes += 1

	def insert_tail(self, node):
		if self.head == None:
			self.insert_head(node)
			return

		tail_node = self.get_tail_node()
		tail_node.next = node
		self.num_nodes += 1

	def insert_at(self, node, pos):
		if pos < 1:
			raise Exception("Invalid position specified")

		if pos == 1:
			self.insert_head(node)
			return

		prev_node = self.find_node_at_pos(pos - 1)
		node.next = prev_node.next
		prev_node.next = node
		self.num_nodes += 1

class Order(Enum):
	ASCENDING	= 1
	DESCENDING	= 2

class SortedList(SinglyLinkedList):
	def __init__(self):
		super().__init__()
		self.order = Order.ASCENDING.value

	def reverse(self):
		if self.order == Order.ASCENDING.value:
			self.order = Order.DESCENDING.value
		else:
			self.order = Order.ASCENDING.value
		super().reverse()

	def insert(self, node):
		self.num_nodes += 1
		if self.head == None:
			self.head = node
			return

		if self.order == Order.ASCENDING.value:
			self.__insert_ascending(node)
		else:
			self.__insert_descending(node)

		if self.ordered():
			return

		raise Exception("Order does not seem to be right")

	# Private method not available to consumers
	def __insert_descending(self, node):
		current = self.head
		prev = None
		while current != None:
			if current.key < node.key:
				if prev == None:
					node.next = self.head
					self.head = node
					return
				else:
					prev.next = node
					node.next = current
					return

			prev = current
			current = current.next

		# Inserting at the tail of the list
		prev.next = node

	def __insert_ascending(self, node):
		current = self.head
		prev = None
		while current != None:
			if current.key >= node.key:
				if prev == None:
					node.next = self.head
					self.head = node
					return
				else:
					prev.next = node
					node.next = current
					return

			prev = current
			current = current.next

		# Inserting at the tail of the list
		prev.next = node

	def __ordered_ascending(self):
		current = self.head
		prev = None
		while current != None:
			if prev != None:
				if current.key < prev.key:
					print("Not in ascending order current:", \
									current.key, "Prev: ", prev.key)
					return False
			prev = current
			current = current.next

		return True

	def __ordered_descending(self):
		current = self.head
		prev = None
		while current != None:
			if prev != None:
				if current.key > prev.key:
					print("Not in descending order current:", \
									current.key, "Prev: ", prev.key)
					return False
			prev = current
			current = current.next

		return True

	def ordered(self):
		if self.head == None:
			return True

		if self.order == Order.ASCENDING.value:
			return self.__ordered_ascending()
		else:
			return self.__ordered_descending()

	# Delete the duplicate nodes:
	def deduplicate(self):
		if self.head == None:
			return

		num_nodes_removed = 0
		current = self.head
		while current is not None:
			node = current.next
			while node is not None and node.key == current.key:
				__node = node.next
				del node
				num_nodes_removed += 1
				node = __node
			current.next = node		# Establish link
			current = node			# Start processing from there

		if not self.ordered():
			raise Exception("Deduplication broke the list order")

		if self.has_loop():
			raise Excpetion("Deduplication introduced the loop")

		print("List deduplicated, nodes removed:", num_nodes_removed)

def merge(l1, l2):
	if type(l1) is not SortedList or type(l2) is not SortedList:
		raise Exception("Invalid type of list", type(list_to_merge))

	if not l1.ordered():
		raise Exception("First list in the argument not ordered")

	if not l2.ordered():
		raise Exception("Second list in the argument not ordered")

	if l1.head == None:
		return l2

	if l2.head == None:
		return l1

	if l1.order != l2.order:
		print("Order of the list differs for 2 lists, re-ordering")
		if l1.order == Order.DESCENDING.value:
			l1.reverse()
		else:
			l2.reverse()

	# This method returns the merged list in the ascending order.
	current_a = l1.head
	current_b = l2.head
	if l1.head.key < l2.head.key:
		new_list = l1
		current_a = current_a.next
	else:
		new_list = l2
		current_b = current_b.next

	current = new_list.head

	while current_a is not None and current_b is not None:
		if current_a.key < current_b.key:
			current.next = current_a
			current_a = current_a.next
		else:
			current.next = current_b
			current_b = current_b.next
		current = current.next

	if current_a is not None:
		current.next = current_a
	else:
		current.next = current_b

	if not new_list.ordered():
		raise Exception("New list is not ordered")

	return new_list

class Operations(Enum):
	INSERT_HEAD 	= 1
	INSERT_TAIL 	= 2
	INSERT_AT		= 3
	DELETE 			= 4
	SEARCH 			= 5
	PRINT  			= 6
	PRINT_REVERSE 	= 7
	REVERSE 		= 8

def get_node_to_insert():
	key = random.randint(-32768, 32768)
	val = random.randint(-32768, 32768)
	node = Node(key, val)
	return node

def perform_random_operations(sll):
	keys = []
	ops = random.randint(1, 20000)
	for i in range(ops):
		op = random.randint(1, 8)
		if op == Operations.PRINT.value:
			print("Printing the list")
			sll.print()
		elif op == Operations.PRINT_REVERSE.value:
			print("Printing the list in reverse")
			sll.print_reverse(sll.head)
			print("EOL")
		else:
			if sll.has_loop():
				raise Exception("Loop detected in the list: ")
			if op == Operations.INSERT_HEAD.value:
				node = get_node_to_insert()
				if isinstance(sll, SimpleList):
					print("Inserting at head key:", node.key)
					sll.insert_head(node)
				else:
					print("Inserting in sorted list:", node.key)
					sll.insert(node)
				keys.append(node.key)
			elif op == Operations.INSERT_TAIL.value:
				node = get_node_to_insert()
				if isinstance(sll, SimpleList):
					print("Inserting at tail key:", node.key)
					sll.insert_tail(node)
				else:
					print("Inserting in sorted list:", node.key)
					sll.insert(node)
				keys.append(node.key)
			elif op == Operations.INSERT_AT.value:
				node = get_node_to_insert()
				if isinstance(sll, SimpleList):
					pos  = random.randint(1, len(keys) + 1)
					print("Inserting at position ", pos, "key:", node.key)
					sll.insert_at(node, pos)
					_node = sll.find_node_at_pos(pos)
					if node.key != _node.key:
						sll.print()
						raise Exception("Insert at position failed")
				else:
					print("Inserting in sorted list:", node.key)
					sll.insert(node)
				keys.append(node.key)
			elif op == Operations.DELETE.value:
				if len(keys) == 0:
					continue

				index = random.randint(0, len(keys) - 1)
				print(" Deleting key: " + str(keys[index]))
				sll.delete(keys[index])
				keys.pop(index)
			elif op == Operations.SEARCH.value:
				if len(keys) == 0:
					continue

				index = random.randint(0, len(keys) - 1)
				print("Searching key: " + str(keys[index]))
				prev, current = sll.search(keys[index])
				if current == None:
					raise Exception("Node not found")
			elif op == Operations.REVERSE.value:
				print("Reversing thelist")
				sll.reverse()
				sll.print()
			else:
				raise Exception("Invalid operation")

	if type(sll) is SortedList:
		sll.print(True)

def create_sorted_list():
	list_size = random.randint(0, 1000)
	sll = SortedList()
	for i in range(list_size):
		node = get_node_to_insert()
		sll.insert(node)

	if not sll.ordered():
		raise Exception("List is not sorted")

	print("Created sorted list of size:", list_size)
	return sll

if __name__ == "__main__":
	#sll = SimpleList()
	#sll = SortedList()
	#perform_random_operations(sll)

	l1 = create_sorted_list()
	l2 = create_sorted_list()
	l = merge(l1, l2)
	print("Size of merged list:", l.size())
	l.deduplicate()
	print("Size of deduplicated list:", l.size())
