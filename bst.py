# Binary Search Tree Operations

import random
import sys
from enum import Enum
import copy

class bst_node:

	def __init__(self, key, val):
		self.key 	= key
		self.val 	= val
		self.left	= None
		self.right	= None

	def is_leaf(self):
		if self.left == None and self.right == None:
			return True
		return False

	def has_both_children(self):
		if self.left != None and self.right != None:
			return True
		return False

	def has_only_left_child(self):
		if self.left != None and self.right == None:
			return True
		return False

	def has_only_right_child(self):
		if self.left == None and self.right != None:
			return True
		return False

	def __str__(self):
		string = "%6d|%6d " % (self.key, self.val)
		return string

	def pprint(self):
		if self.is_leaf():
			print(str(self) + " L: %6s R: %6s" % ("None", "None"))
		elif self.has_only_left_child():
			print(str(self) + " L: %6d R: %6s" % (self.left.key, "None"))
		elif self.has_only_right_child():
			print(str(self) + " L: %6s R: %6d" % ("None", self.right.key))
		elif self.has_both_children():
			print(str(self) + " L: %6d R: %6d" % (self.left.key, self.right.key))
		else:
			raise Exception("Invalid node format")

class bst:

	def __init__(self):
		self.root = None
		self.inorder_list = []
		self.inorder_list_updated = False
		self.node_count = 0
		self.height = 0
		self.level_dict = {}
		self.serialized_list = []
		self.__all_paths = []

	def insert(self, node):
		self.inorder_list_updated = False
		self.node_count += 1
		if self.root == None:
			self.root = node
			return

		current = self.root
		while current != None:
			if node.key <= current.key:
				if current.left != None:
					current = current.left
				else:
					current.left = node
					return
			else:
				if current.right != None:
					current = current.right
				else:
					current.right = node
					return

	def search(self, key):
		current = self.root
		while current != None:
			if current.key == key:
				return current.val
			if key < current.key:
				current = current.left
			else:
				current = current.right

		print("Search: Key not found")
		return None

	def inorder(self, node):
		if node != None:
			self.inorder(node.left)
			self.inorder_list.append(node)
			self.inorder(node.right)

	def pprint(self):
		if not self.inorder_list_updated:
			self.inorder(self.root)
			self.inorder_list_updated = True

		for node in self.inorder_list:
			node.pprint()
		print("Root: " + str(self.root) + " Nodes: " + str(self.node_count) + " Height: " + str(self.bst_height(self.root)))
		print("------------------------")

	'''
	This is interesting.  If the node has a right subtree, then we find the
	leftmost node in the right subtree.

	But, if node does not have a right subtree, then its inorder successor
	is the root of the subtree which has this node in its left subtree. eg
	(8: L:4,R:9 and 4: L:3,R:5 and 5: L:2(no right subtree of 5), then inorder
	successor of 5 is 8)

	The way to find the inorder successor is then, search the node O(log(n))
	and keep track of parent if we are going to left while searching.  This is
	because inorder == left, root and then right, so if we are going to left
	subtree, next we will visit the root of the left subtree, but if we go
	in the right subtree, then we go to parent of the root of right subtree

	Technically, it is going up the tree and finding that parent who has this
	node in its left subtree

	'''
	def inorder_successor(self, node):
		# Simple case, node has a right subtree
		'''
		Interesting thing is if this method is called in the context of delete
		node, it will be called when node has both children, so the node will
		always have right child, so only following if clause will be executed
		in context of delete node.
		'''
		if node.right != None:
			parent = node
			current = node.right
			while current.left != None:
				parent = current
				current = current.left
			return [parent, current]

		'''
		The following code won't execute in context of delete node.  It will
		only execute if somebody queries the inorder successor of a node with
		no right child
		'''
		parent = None
		current = self.root
		successor_parent = parent
		successor = current

		while current != None:
			if node.key < current.key:
				successor_parent = parent
				successor = current
				parent = current
				current = current.left
			elif node.key > current.key:
				parent = current
				current = current.right
			else:
				return [successor_parent, successor]

	def is_bst(self):
		if not self.inorder_list_updated:
			self.inorder(self.root)
			self.inorder_list_updated = True

		min_key = -32769
		for node in self.inorder_list:
			if node.key >= min_key:
				min_key = node.key
			else:
				self.pprint()
				print("Found key " + str(node.key) + " smaller than min " + str(min_key))
				return False

		return True

	def max_height(self):
		return self.bst_height(self.root)

	def min_subtree_ht(self, node):
		if node == None:
			return -1

		if node.is_leaf():
			return 0

		return 1 + min(self.min_subtree_ht(node.left), self.min_subtree_ht(node.right))

	def min_height(self):
		return self.min_subtree_ht(self.root)

	def bst_height(self, node):
		if node == None:
			return -1

		if node.is_leaf():
			return 0

		return 1 + max(self.bst_height(node.left), self.bst_height(node.right))

	def delete_leaf(self, node, parent):
		# Deleting the root node and is the only node in tree
		if parent == None:
			self.root = None
		elif parent.left == node:
			parent.left = None
		else:
			parent.right = None

		del node

	def delete_node_with_only_one_child(self, node, parent):
		if node.has_only_left_child():
			subtree = node.left
		else:
			subtree = node.right

		if parent == None:
			self.root = subtree
		elif parent.left == node:
			parent.left = subtree
		else:
			parent.right = subtree

		del node

	def delete(self, key):
		self.node_count -= 1
		self.inorder_list_updated = False
		current = self.root
		parent = None
		while current != None:
			if current.key == key:
				break

			parent = current
			if key < current.key:
				current = current.left
			else:
				current = current.right

		if current == None:
			print("Delete: Key not found")
			return

		# Simple case deleting leaf
		if current.is_leaf():
			self.delete_leaf(current, parent)
			return

		# Case: Only 1 child
		if not current.has_both_children():
			self.delete_node_with_only_one_child(current, parent)
			return

		# Both children, find inorder successor
		successor_parent, successor = self.inorder_successor(current)
		current.key = successor.key
		current.val = successor.val

		if successor.is_leaf():
			self.delete_leaf(successor, successor_parent)
			del successor
			return

		if successor.has_both_children():
			self.pprint()
			raise Exception("This should not be possible")
		else:
			self.delete_node_with_only_one_child(successor, successor_parent)
			del successor
			return

		raise Exception("Invalid delete case")

	def level_inorder_traversal(self, node, level):
		if node != None:
			self.level_inorder_traversal(node.left, level + 1)
			if level not in self.level_dict:
				self.level_dict[level] = []
			self.level_dict[level].append(node.key)
			self.level_inorder_traversal(node.right, level + 1)

	'''
	Logic is to do inorder traversal with the variable tracking the current level
	Add the node in the dictionary and create lists of the dictionary
	'''
	def linked_list_per_level(self):
		self.level_inorder_traversal(self.root, 0)
		print(str(self.level_dict))

	def lr_nodes(self, node):
		if node == None:
			return []

		left_list = self.lr_nodes(node.left)
		right_list = self.lr_nodes(node.right)
		print("Node: " + str(node.key))
		print("Left: " + str(left_list))
		print("Right: " + str(right_list))
		print("-----------")
		return [node.key] + left_list + right_list

	def print_lr_subtrees(self):
		self.lr_nodes(self.root)

	# Destroy the tree, we probably are going to build new one
	# We are not deleting the nodes, we just reset their pointers
	def destroy(self):
		for node in self.inorder_list:
			node.left = None
			node.right = None

		self.root = None
		self.height = 0
		self.level_dict = {}

	'''
	Balance the tree, this will change the root.  The logic is to do an inorder
	traversal and then choose midpoint of the list as root and then build the
	left and right subtrees accordingly.
	'''
	def prepare_tree(self, low, high):
		if low == high:
			return self.inorder_list[low]

		if high - low == 1:
			parent = self.inorder_list[high]
			parent.left = self.inorder_list[low]
			return parent

		mid = int((low + high) / 2)
		parent = self.inorder_list[mid]
		parent.left = self.prepare_tree(low, mid - 1)
		parent.right = self.prepare_tree(mid + 1, high)
		return parent

	def balance(self):
		if not self.inorder_list_updated:
			self.inorder(self.root)
			self.inorder_list_updated = True

		self.destroy()

		self.root = self.prepare_tree(0, len(self.inorder_list) - 1)
		self.height = self.bst_height(bst.root)
		self.pprint()
		self.print_lr_subtrees()

	def serialize(self, node):
		entry = {}
		if node == None:
			self.serialized_list.append(entry)
			return

		entry['key'] = node.key
		entry['value'] = node.val
		self.serialized_list.append(entry)
		self.serialize(node.left)
		self.serialize(node.right)
		del node

	def serialize_tree(self):
		self.serialize(self.root)

		self.destroy()

		return self.serialized_list

	def deserialize(self, parent, serialized_list):
		if len(serialized_list) == 0:
			return

		entry = serialized_list.pop(0)
		#print("Got left entry: " + str(entry) + " for parent "  + str(parent.key))
		if 'key' not in entry:
			parent.left = None
		else:
			node = bst_node(entry['key'], entry['value'])
			self.deserialize(node, serialized_list)
			parent.left = node

		entry = serialized_list.pop(0)
		#print("Got right entry: " + str(entry) + " for parent "  + str(parent.key))
		if 'key' not in entry:
			parent.right = None
		else:
			node = bst_node(entry['key'], entry['value'])
			self.deserialize(node, serialized_list)
			parent.right = node

	def deserialize_tree(self, serialized_list):
		entry = serialized_list.pop(0)
		if 'key' not in entry:
			self.root = None
			return

		self.root = bst_node(entry['key'], entry['value'])
		self.deserialize(self.root, serialized_list)
		self.inorder_list_updated = False

	def find_all_paths(self, node, path):
		if node == None:
			return

		# Tricky thing in python is all objects are passed by
		# reference, so when 1 recursive call returns, path variable
		# still has the node appended from previous call
		#
		# Or try to send the index as an argument, so that it
		# would know how long the path at particular level of recursion.
		deep_path = copy.deepcopy(path)

		deep_path.append(node.key)
		if node.is_leaf():
			final_path = copy.deepcopy(deep_path)
			self.__all_paths.append(final_path)
			print(str(len(final_path)) + "  "  + str(final_path))
			return

		self.find_all_paths(node.left, deep_path)
		self.find_all_paths(node.right, deep_path)
		del deep_path

	'''
	Find all paths from root to leaf
	'''
	def all_paths(self):
		self.find_all_paths(self.root, [])

	def distance_from_root(self, a):
		if self.root == None:
			return 0

		if self.root.key == a.key:
			return 0

		distance = 0
		current = self.root
		while current.key != a.key:
			if a.key < current.key:
				current = current.left
			else:
				current = current.right
			distance += 1

		return distance

	def find_lca(self, a, b):
		if self.root == None:
			return None

		current = self.root
		while current != None:
			if a.key < current.key and b.key < current.key:
				current = current.left
			elif a.key > current.key and b.key > current.key:
				current = current.right
			else:
				return current

		return None
	'''
	Distance between 2 nodes in BST = distance of node1 from root +
	distance of node2 from root - 2 * distance between root and the
	lowest common ancestor of node1 and node2.  If you picture the
	diagram you would understand the math pretty easily.
	'''
	def distance_between_2_nodes(self, a, b):

		dist_a = self.distance_from_root(a)
		dist_b = self.distance_from_root(b)

		lca = self.find_lca(a, b)
		print("LCA of %d and %d is %d" % (a.key, b.key, lca.key))
		dist_lca = self.distance_from_root(lca)

		return dist_a + dist_b - (2 * dist_lca)

	def diameter(self, node):
		if node == None:
			return 0

		left_height = self.bst_height(node.left)
		right_height = self.bst_height(node.right)

		left_diameter = self.diameter(node.left)
		right_diameter = self.diameter(node.right)

		return max(max(left_diameter, right_diameter), left_height + right_height + 1)

	'''
	Diameter of the BST = max(diameter of left, diameter of right subtree,
								left_height + right_height + 1)
	'''
	def diameter_of_bst(self):
		return self.diameter(self.root)

	def mirror(self, node):
		if node == None:
			return

		self.mirror(node.left)
		self.mirror(node.right)
		temp = node.left
		node.left = node.right
		node.right = temp

class Operations(Enum):
	INSERT = 1
	DELETE = 2
	SEARCH = 3

if __name__ == "__main__":
	keys = []
	bst = bst()
	ops = random.randint(1, 40000)
	for i in range(ops):
		op = random.randint(1, 3)
		if op == Operations.INSERT.value:
			key = random.randint(-32768, 32768)
			val = random.randint(-32768, 32768)
			print("Adding node: " + str(key) + "|" + str(val))
			node = bst_node(key, val)
			bst.insert(node)
			keys.append(key)
		elif op == Operations.DELETE.value:
			if len(keys) == 0:
				continue

			index = random.randint(0, len(keys) - 1)
			print(" Deleting key: " + str(keys[index]))
			bst.delete(keys[index])
			keys.pop(index)
		elif op == Operations.SEARCH.value:
			if len(keys) == 0:
				continue

			index = random.randint(0, len(keys) - 1)
			print("Searching key: " + str(keys[index]))
			bst.search(keys[index])
		else:
			raise Exception("Invalid operation")
		#bst.pprint()

	bst.pprint()
	if bst.is_bst():
		print("Cool its a valid BST")
	else:
		print("Something went wrong")

	max_ht = bst.bst_height(bst.root)
	min_ht = bst.min_height()
	print("Got Max Ht: %d Min Ht: %d" % (max_ht, min_ht))

	#bst.linked_list_per_level()
	#bst.print_lr_subtrees()

	# Balance the current tree
	#bst.balance()

	serialized = bst.serialize_tree()
	print(serialized)
	bst.deserialize_tree(serialized)
	bst.pprint()
	if bst.is_bst():
		print("Cool its a valid BST")
	else:
		print("Something went wrong")
	max_ht = bst.bst_height(bst.root)
	min_ht = bst.min_height()
	print("Got Max Ht: %d Min Ht: %d" % (max_ht, min_ht))

	bst.all_paths()
	if not bst.inorder_list_updated:
		bst.inorder(self.root)
		bst.inorder_list_updated = True

	a = random.choice(bst.inorder_list)
	b = random.choice(bst.inorder_list)
	dist = bst.distance_between_2_nodes(a, b)
	print("Distance between %d and %d is %d" % (a.key, b.key, dist))
	print("Diameter of the tree: %d" % (bst.diameter_of_bst()))

	bst.mirror(bst.root)
	bst.pprint()
