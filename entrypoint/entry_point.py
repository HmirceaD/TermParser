"""main class of the program"""
import sys
sys.path.append('../')

substitute_terms = {"y": "v(y, x)", "x": "z"}
wrong_expression = "f(x,f(y))"
test_expression = "f(x,g(z,y))"
functions_list = ['f', 'g']
variable_list = ['z', 'x', 'y']
substition_variable_list = variable_list + []
substition_function_list = functions_list + ['v']

from entrypoint.parser import ParsedTree

term_tree1 = ParsedTree(test_expression, functions_list, variable_list, substition_variable_list, substition_function_list)
term_tree1.print_tree()
new_tree = term_tree1.substitution(substitute_terms)
new_tree.print_tree()

#term_tree3 = ParsedTree("f(x)")

# term_tree4 = ParsedTree("")
# term_tree5 = ParsedTree("f(x,)")
# term_tree6 = ParsedTree("f(,z)")
# term_tree7 = ParsedTree("f(z,x))")
# term_tree8 = ParsedTree("f((z,x)")