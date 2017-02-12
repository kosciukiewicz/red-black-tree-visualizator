from Tkinter import *

class Node(object):

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.color = RBTree.red

    def __str__(self):
        return "%d%s" % (self.key, "R" if self.color else "B")


class RBTree(object):
    red = True
    black = False
    width_start = 400
    height_start = 10
    default_size = 40
    width_spacing = 60
    height_spacing = 60

    def __init__(self):
        self.root = None

    @staticmethod
    def insert_to_node(key, root):
        if root is None:
            root = Node(key)
        else:
            if RBTree.is_red(root.left) and RBTree.is_red(root.right):
                RBTree.color_flip(root)
            if key < root.key:
                root.left = RBTree.insert_to_node(key, root.left)
            elif key > root.key:
                root.right = RBTree.insert_to_node(key, root.right)
            else:
                print "Duplicate key"
        root = RBTree.fix_up(root)
        return root

    def insert(self, key):
        self.root = self.insert_to_node(key=key, root=self.root)
        self.root.color = RBTree.black

    @staticmethod
    def fix_up(node):
        if RBTree.is_red(node.left) and RBTree.is_red(node.right) and (RBTree.check_children_redness(node.left) or RBTree.check_children_redness(node.right)):
            RBTree.color_flip(node)
        if (not RBTree.is_red(node.right)) and RBTree.is_red(node.left) and RBTree.is_red(node.left.right):
            node.left = RBTree.rotate_left(node.left)
        if (not RBTree.is_red(node.left)) and RBTree.is_red(node.right) and RBTree.is_red(node.right.left):
            node.right = RBTree.rotate_right(node.right)
        if (not RBTree.is_red(node.right)) and RBTree.is_red(node.left) and RBTree.is_red(node.left.left):
            node = RBTree.rotate_right(node)
        if (not RBTree.is_red(node.left)) and RBTree.is_red(node.right) and RBTree.is_red(node.right.right):
            node = RBTree.rotate_left(node)
        return node

    @staticmethod
    def rotate_left(node):
        help_node = node.right
        node.right = help_node.left
        help_node.left = node
        help_node.color = node.color
        node.color = RBTree.red
        return help_node

    @staticmethod
    def rotate_right(node):
        help_node = node.left
        node.left = help_node.right
        help_node.right = node
        help_node.color = node.color
        node.color = RBTree.red
        return help_node

    @staticmethod
    def check_children_redness(node):
        return RBTree.is_red(node.right) or RBTree.is_red(node.left)
    @staticmethod
    def is_red(node):
        return node is not None and node.color

    @staticmethod
    def color_flip(node):
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def print_level_order(self, depth):
        for i in range(1, depth + 1):
            print "%s%s%s" % ("Level ", i, ":"),
            level_nodes = RBTree.print_level(self.root, i)
            print level_nodes

    @staticmethod
    def print_level(node, level):
        string = ""
        if level == 1:
            if node is None:
                string = "* "
            else:
                string = str(node)
                string += ", "
        elif level > 1:
            if node is None:
                string = "* * "
            else:
                left_string = RBTree.print_level(node.left, level-1)
                right_string = RBTree.print_level(node.right, level - 1)
                string = left_string + right_string
        return string

    @staticmethod
    def height(node):
        i = 0
        if node is None:
            i = -1
        else:
            left = RBTree.height(node.left)
            right = RBTree.height(node.right)

            if left > right:
                i = left + 1
            else:
                i = right + 1
        return i

    def draw_tree_on_canvas(self, canvas):
        canvas.delete(ALL)
        RBTree.draw_node(self.root, canvas, RBTree.height_start, RBTree.width_start)

    @staticmethod
    def draw_spacing_to_left(canvas, start_height, start_width, height):
        canvas.create_line(start_width, start_height + RBTree.default_size/2, start_width - height*RBTree.width_spacing,
                           start_height + RBTree.height_spacing + RBTree.default_size/2, fill="black", width="2")

    @staticmethod
    def draw_spacing_to_right(canvas, start_height, start_width, height):
        canvas.create_line(start_width, start_height + RBTree.default_size/2, start_width + height*RBTree.width_spacing,
                           start_height + RBTree.height_spacing + RBTree.default_size/2, fill="black", width="2")

    @staticmethod
    def draw_node(node, canvas, start_height, start_width):
        if node is not None:
            start = start_width - (RBTree.default_size/2)
            height = RBTree.height(node)
            if node.left is not None:
                RBTree.draw_spacing_to_left(canvas, start_height, start_width, height)
                RBTree.draw_node(node.left, canvas, (start_height + RBTree.height_spacing), (start_width - RBTree.width_spacing*height))
            if node.right is not None:
                RBTree.draw_spacing_to_right(canvas, start_height, start_width, height)
                RBTree.draw_node(node.right, canvas, (start_height + RBTree.height_spacing), (start_width + RBTree.width_spacing*height))
            canvas.create_oval(start, start_height, (start + RBTree.default_size), (start_height + RBTree.default_size),
                               fill="red" if node.color else "black")
            canvas.create_text(start_width, start_height + RBTree.default_size / 2,
                               fill="black" if node.color else "white", text=str(node.key))


def insert_and_print_tree(rbtree, entry, canvas):
    rbtree.insert(int(entry.get()))
    rbtree.print_level_order(tree.height(tree.root) + 1)
    e.delete(0, END)
    rbtree.draw_tree_on_canvas(canvas)


tree = RBTree()
root = Tk()
root.geometry("1000x1000")
root.resizable(0, 0)
e = Entry(root)
e.pack()
b = Button(root, text="insert", command=lambda: insert_and_print_tree(tree, e, canvas))
b.pack()
canvas = Canvas(root, bg="white", height=800, width=800)
canvas.pack()
root.mainloop()
