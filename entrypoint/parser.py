"""Create a tree based on the levels of the expression"""
import sys
sys.path.append('../')

from entrypoint.term import Term

class ParsedTree:

    def __init__(self, expression, function_list, variable_list, substition_variable_list, substition_function_list, constant_list):

        print("New expression \n ============================\n")

        self.substition_variable_list = substition_variable_list
        self.substition_function_list = substition_function_list
        self.function_list = function_list
        self.variable_list = variable_list
        self.constant_list = constant_list
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
        term = Term(sub_expr, self.crr, self.get_term_type(sub_expr))

        if self.root is None:
            self.root = term

        return term

    def open_bracket(self, sub_expr, index):
        """if an open bracket is detected then it is the start of a new term"""
        term = self.create_term(sub_expr, index)

        if self.crr:
            self.crr.update_children(term)

        self.crr = term

    def get_term_type(self, sub_expr):
        term_type = ""
        if sub_expr.strip() in self.variable_list:
            term_type = "VARIABLE"
        elif sub_expr.strip() in self.function_list:
            term_type = "FUNCTION"

        return term_type

    def comma(self, sub_expr, index):
        """if a comma is detected the a child in the previous parent is detected"""
        if sub_expr:

            new_term = Term(sub_expr, self.crr, self.get_term_type(sub_expr))
            self.crr.update_children(new_term)

    def closed_bracket(self, sub_expr, index):
        """if a closed bracket is detected than the the end of a term is detected"""

        self.func_num_of_variables(self.crr, len(self.crr.children))

        if sub_expr:
            new_term = Term(sub_expr, self.crr, self.get_term_type(sub_expr))
            # Update the number of children the function had when it was first encountered

            self.crr.update_children(new_term)

        if self.crr:
            self.crr = self.crr.parent

    def substitution(self, subst_map):
        """helper class for the expression substitution"""
        return self.substitute__term(subst_map, self.expression)

    def substitute__term(self, substitution_map, expr):
        """Recursivelly substitute in the tree from a map of substitute terms"""

        if self.check_correct_substitution(substitution_map):

            new_expr = expr
            for key in substitution_map.keys():
                new_expr = new_expr.replace(key, substitution_map[key])
                print("The term: " + key + " has been replaced with: " +substitution_map[key])

            print("The new expression is: " + new_expr + "\n")

            substitute_tree = ParsedTree(new_expr, self.function_list, self.variable_list, self.substition_variable_list, self.substition_function_list, self.constant_list)
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

        if len(sub_expr) > 0 and self.root is None:
            # for the case when the expression has no delimitators
            self.create_term(sub_expr, i)

        if self.crr is not None:
            print("Current", self.crr)
            print("Root", self.root)

            # If parsing stops at a term which is not the root, then it did not
            # close all the parentheses / did not make its way back to the top.
            print("Invalid expression. Try closing all parentheses.")
            return False

    def print_tree(self):
        """helper function to print the tree from root"""
        print("Term tree for the expression: " + self.expression + " is\n")

        if self.root:
            print(self.root.tree_string(True))

    def get_root_func(self):
        return self.root

    def get_root(self):
        """return current root of the program"""
        print("The root is: " + self.root.expr + "()\n")

    def get_first_item_before_open_bracket(self, expr):
        if expr[expr.find('(')-1] == expr[len(expr)-1]:
            print("Function is badly defined")
            sys.exit(0)
        else:
            return expr[expr.find('(')-1]

    def check_correct_substitution(self, subst_map):

        pre_subst = subst_map.keys()
        post_subst = []

        for p_temp in subst_map.values():

            if p_temp.find('(') != -1:
                post_subst.append(p_temp[p_temp.find('(')-1] + '-')
            else:
                post_subst.append(p_temp)

        for index, p_temp in enumerate(post_subst):
            if p_temp.find('-') != -1:
                p_temp = p_temp.replace('-','')

                if p_temp in pre_subst:
                    print("Cannot have a variable and a function with the same notation")
                    sys.exit(0)
                post_subst[index] = p_temp

        for s in pre_subst:
            if s not in self.substition_variable_list and s not in self.constant_list:
                print("Variable to be substituted not defined")
                sys.exit(0)

            if s.find('(') != -1:
                print("A function cannot be the target of a substitution")
                sys.exit(0)

        for p in post_subst:
            print(p)
            if p not in self.substition_variable_list and p not in self.substition_function_list and p not in self.constant_list:
                print("Variable or function to be substituted not defined")
                sys.exit(0)

        return 1