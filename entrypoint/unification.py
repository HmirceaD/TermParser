from entrypoint.parser import ParsedTree

class Unify:

    def __init__(self, variable_list, function_list, subst_var_list, subst_func_list, subst_map, constant_list):

        self.variable_list = variable_list
        self.function_list = function_list
        self.subst_var_list = subst_var_list
        self.subst_func_list = subst_func_list
        self.subst_map = subst_map
        self.constant_list = constant_list

    def unify(self, left_lst_exp, right_lst_exp, s):

        if len(left_lst_exp) == 1 and len(right_lst_exp) == 1:
            left_tree = ParsedTree(left_lst_exp[0], self.variable_list, self.function_list, self.subst_var_list, self.subst_func_list, self.constant_list)

            right_tree = ParsedTree(right_lst_exp[0], self.variable_list, self.function_list, self.subst_var_list, self.subst_func_list,self.constant_list)

            root_left = left_tree.get_root_func()
            root_right = right_tree.get_root_func()

            if root_left.print_expression() == root_right.print_expression():

                return s
            elif root_left.get_node_type() == 'VARIABLE':
                return self.unifyVar(root_left.print_expression(), root_right.print_expression(), s)

            elif root_right.get_node_type() == 'VARIABLE':
                return self.unifyVar(root_right.print_expression(), root_left.print_expression(), s)

            elif root_left.get_node_type() != 'VARIABLE' and root_right.get_node_type() != 'VARIABLE':
                if left_tree.get_root_func().expr == right_tree.get_root_func().expr:
                    left_sub_term_lst = []

                    for child in left_tree.get_root_func().get_children_list():
                        left_sub_term_lst.append(child.print_expression())

                    right_sub_term_lst = []

                    for child in right_tree.get_root_func().get_children_list():
                        right_sub_term_lst.append(child.print_expression())

                    return self.unify(left_sub_term_lst, right_sub_term_lst, s)
                else:
                    print('Clash Failure')
                    return
        else:
            first_left = []
            first_left.append(left_lst_exp[0])

            rest_left = []
            for i in range(1, len(left_lst_exp)):
                rest_left.append(left_lst_exp[i])

            first_right = []
            first_right.append(right_lst_exp[0])

            rest_right = []
            for i in range(1, len(right_lst_exp)):
                rest_right.append(right_lst_exp[i])

            return self.unify(rest_left, rest_right, self.unify(first_left, first_right, s))

        return None

    def unifyVar(self, var, x, s):

        if var in s:
            left = []
            left.append(s[var])

            right = []
            right.append(x)

            return self.unify(left, right, s)
        elif x in s:
            return self.unifyVar(var, s[x], s)
        elif self.occurCheck(var, x, s):
            print('Failure Occured with: ')
            print(var, x, s)
            return None
        else:

            return self.addSubstitution(var, x, s)

    def addSubstitution(self, var, x, s):
        s[var] = x
        for i in s:
            tree = ParsedTree(s[i], self.variable_list, self.function_list, self.subst_var_list, self.subst_func_list, self.constant_list)
            tree.substitution(self.subst_map)
            s[i] = tree.get_root_func().print_expression()

        print(str(tree.get_root_func()))
        return s

    def occurCheck(self, var, x, s):
        xTree = ParsedTree(x, self.variable_list, self.function_list, self.subst_var_list, self.subst_func_list, self.constant_list)

        if var == xTree.get_root_func().print_expression():
            return True

        elif xTree.get_root_func().print_expression() in s:
            return self.occurCheck(var, s[xTree.get_root_func().print_expression()], x)

        elif xTree.get_root_func().get_node_type == 'FUNCTION':
            for subTerm in xTree.get_root_func().get_children_list():
                if self.occurCheck(var, subTerm.print_expression(), s):
                    return True

        return False