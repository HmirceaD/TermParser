"""main class of the program"""
import sys
sys.path.append('../')

substitute_terms = {"y": "z(y, H)", "x": "z"}

from entrypoint.parser import ParsedTree

term_tree1 = ParsedTree("f(x,g(z,y))")
term_tree1.print_tree()
new_tree = term_tree1.substitution(substitute_terms)

new_tree.print_tree()
#term_tree3 = ParsedTree("f(x)")

# term_tree4 = ParsedTree("")
# term_tree5 = ParsedTree("f(x,)")
# term_tree6 = ParsedTree("f(,z)")
# term_tree7 = ParsedTree("f(z,x))")
# term_tree8 = ParsedTree("f((z,x)")