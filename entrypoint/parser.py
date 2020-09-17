"""Create a tree based on the levels of the expression"""
import sys
sys.path.append('../')

from expression_functions.term import Term

class ParsedTree:

    def __init__(self, expression, function_list, variable_list):

        print("New expression \n ============================\n")

        self.function_list = function_list
        self.variable_list = variable_list

        self.func_variable_count_dict = {}

        self.handler_functions = [self.open_bracket, self.comma ,self.closed_bracket]

        self.error_logs = {0: "Expression is empty", 1: "Parantheses missing",
                           2: "Extra parantheses added", 3: "Variable Missing",
                           4:"Number of arguments per function differ"}

        self.delim = {'(': 0,
            ',': 1,
            ')': 2}

        self.crr = None
        self.root = None
        self.expression = expression

        self.parse_expression()
        self.get_root()

    def func_num_of_variables(self, func_term, num_of_children):

        if func_term.expr in self.func_variable_count_dict.keys():
            if self.func_variable_count_dict[func_term.expr] != num_of_children:
                print(self.error_logs[4])
                sys.exit(0)
        else:
            self.func_variable_count_dict[func_term.expr] = num_of_children


    def create_term(self, sub_expr, index):
        """create a new term from a subexpression"""
        term = Term(sub_expr, self.crr)

        if self.root is None:
            self.root = term

        return term

    def open_bracket(self, sub_expr, index):
        """if an open bracket is detected then it is the start of a new term"""
        term = self.create_term(sub_expr, index)

        if self.crr:
            self.crr.update_children(term)

        self.crr = term

    def comma(self, sub_expr, index):
        """if a comma is detected the a child in the previous parent is detected"""
        if sub_expr:
            new_term = Term(sub_expr, self.crr)
            self.crr.update_children(new_term)

    def closed_bracket(self, sub_expr, index):
        """if a closed bracket is detected than the the end of a term is detected"""

        self.func_num_of_variables(self.crr, len(self.crr.children))

        if sub_expr:
            new_term = Term(sub_expr, self.crr)
            # Update the number of children the function had when it was first encountered

            self.crr.update_children(new_term)

        if self.crr:
            self.crr = self.crr.parent

    def substitution(self, subst_map):
        """helper class for the expression substitution"""
        return self.substitute__term(subst_map, self.expression)

    def substitute__term(self, substitution_map, expr):
        """Recursivelly substitute in the tree from a map of substitute terms"""
        new_expr = expr
        for key in substitution_map.keys():
            new_expr = new_expr.replace(key, substitution_map[key])
            print("The term: " + key + " has been replaced with: " +substitution_map[key])

        print("The new expression is: " + new_expr + "\n")

        substitute_tree = ParsedTree(new_expr, [], [])
        return substitute_tree

    def log_error_and_close(self,error_code):
        """Log all errors and close this section"""
        print(self.error_logs[error_code])
        print("\n=====================================\n")
        return 0

    def check_validity(self):
        """check if the expression is correct"""
        level = 0

        if len(self.expression) > 0:

            for i, ch in enumerate(self.expression):
                if ch == '(':
                    level += 1
                    try:
                        if self.expression[i+1] == ',':
                            return self.log_error_and_close(3)
                    except IndexError:
                        pass
                elif ch == ')':
                    level -= 1

                    try:
                        if self.expression[i-1] == ',':
                            return self.log_error_and_close(3)
                    except IndexError:
                        pass

            if level == 0:
                return 1
            elif level > 0:
                return self.log_error_and_close(2)
            elif level < 0:
                return self.log_error_and_close(1)

        else:
            return self.log_error_and_close(0)

    def parse_expression(self):
        """parse the expression if it is correct and break it into terms"""
        if self.check_validity() != 0:
            #print("The expression: " + self.expression + " is correct")
            print("Begin parsing")

        sub_expr = ""

        for i, ch in enumerate(self.expression):
            if ch in self.delim.keys():

                self.handler_functions[self.delim[ch]](sub_expr, i)

                sub_expr = ""
            else:
                sub_expr = sub_expr + ch


    def print_tree(self):
        """helper function to print the tree from root"""
        print("Term tree for the expression: " + self.expression + " is\n")

        if self.root:
            print(self.root.tree_string(True))

    def get_root(self):
        """return current root of the program"""
        print("The root is: " + self.root.expr + "()\n")