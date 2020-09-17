"""Class that creates terms from subexpression int the expression"""

class Term:

    def __init__(self, expr, parent):
        """pointer to the parent term, the contents formed from the subexpression
        and a list for the potential children"""
        self.parent = parent
        self.expr = expr
        self.children = []

    def update_children(self, child):
        """add a new child to the term"""
        self.children.append(child)

    def get_level(self):
        """return the level of the term in the tree"""

        if self.parent:

            parent_p = str(self.parent.get_level())

            children_p = str(self.parent.children.index(self) + 1)
            if parent_p == "":
                return str(children_p)
            else:
                return str(parent_p + " - " + children_p)
        else:
            #if no parent -> root
            return ""

    def recursive_form_tree(self, prefix, pos):
        """print the term and its children in a visualized form"""
        tree_str = ""
        for child in self.children:
            if pos:
                p =  child.get_level()
            else:
                p = ""
            if child == self.children[-1]:
                tree_str = tree_str + (prefix + "|-> " + child.expr) + "   ------ Position: " + p + "\n"
                tree_str = tree_str + child.recursive_form_tree(prefix + "    ", pos)
            else:
                tree_str = tree_str + (prefix + "|-> " + child.expr) + "   ------ Position: " +  p + "\n"
                tree_str = tree_str + child.recursive_form_tree(prefix + "│   ", pos)

        return tree_str

    def tree_string(self, pos=False):
        """helper class for the tree visualizer"""
        if pos:
            return self.expr + "   ------ Position: ROOT" + self.get_level()  + "\n" + \
                   self.recursive_form_tree("", pos)
        else:
            return self.expr + self.get_level() + "\n" + self.recursive_form_tree("", pos)