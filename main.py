from os import path
import numpy as np


# TODO think about backtracking strategy and problem formulation
# degree heuristic -> number of connected neighbors. For first time solving
# Variable ordering heuristic -> Minimum remaining variables
# Least constraining heuristic -> Least constraining value


# class representing the node in a CSP graph - similar to blanks in the crossword
# they will be the variables with constraints
class Node(object):
    def __init__(self, word, x_coordinate, y_coordinate, word_size, orientation):
        self.word = word
        self.coordinates = (x_coordinate, y_coordinate)
        self.word_size = word_size
        self.orientation = orientation

        # list of immediate Node neighbors, where a neighbor is a blank whose starting position is part of another
        # blank For the neighbors dict, the key is the coordinate of the first char of the neighbor, value is the
        # neighboring node object
        self.neighbors = {}
        # domain used in backtracking strategy
        self.domain = []

    # override the __str__ functions to print the Node
    def __str__(self):
        # only print immediate neighbors
        return f'\nWord: {self.word}\n' \
               f'First Letter Coordinates: {self.coordinates}\n' \
               f'Word size: {self.word_size}\n' \
               f'Orientation: {self.orientation}\n' \
               f'Domain: {self.domain}\n' \
               f'Neighbors with intersection: ' \
               f'{[(key, node.coordinates, node.orientation) for key, node in self.neighbors.items()]}\n '
        # for neighbors print coordinates of intersection then the coordinates of neighbor then its orientation

    def __repr__(self):
        return str(self)

    # override equality comparator. This assumes the starting char of a blank can't be in the same coordinates
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coordinates == other.coordinates

    # override hash function for faster lookup in dictionaries
    # hash the coordinates as I assume the starting char of a blank can't be in the same coordinates as another node
    def __hash__(self):
        return hash(self.coordinates)


# A class representing the Crossword drawing with the blanks and their positions
class Crossword(object):
    def __init__(self, file_name, blanks_file_name, words):
        # a 2D array of characters representing the crossword drawing
        self.drawing = []
        # a list of blanks of type `Node` representing the Variables of CSP graph
        self.blanks = {}
        # file name of the .txt file with the crossword drawing
        self.file_name = file_name
        # try reading the crossword from the file
        self.__read_crossword(file_name)
        # try reading the blanks from blanks.txt file
        self.__read_blanks(blanks_file_name)
        # words given by the wordlist
        self.words = words
        # determine the initial domains of the variables
        self.__initialize_domains()
        # connect the neighbors
        self.__connect_neighbors()

    # read the crossword drawing from .txt file and represent it using 2D array
    def __read_crossword(self, file_name):
        if path.exists(file_name):
            with open(file_name, 'r') as f:
                for line in f:
                    self.drawing.append([el for index, el in enumerate(line.rstrip('\n'))])
        else:
            print(f'Error opening {file_name}. Check if it exists.')

    # create nodes representing the blanks in the crossword
    def __read_blanks(self, file_name):
        allowed_orientations = {'across', 'down'}
        if path.exists(file_name):
            with open(file_name, 'r') as f:
                for line in f:
                    # remove trailing new-line char
                    line = line.rstrip('\n')

                    # skip lines starting with '#' as they are comments in the blanks.txt file
                    if line.startswith('#'):
                        continue
                    else:
                        line_list = line.split(';')

                        # check for correct format of the line parts
                        if len(line_list) != 4:
                            print(f'The {file_name} file doesn\'t have correct format as prescribed')
                        else:
                            # create a new Node and add it to the crossword list
                            # check each part before creating Node
                            if isinstance(eval(line_list[0]), int) and isinstance(eval(line_list[1]), tuple) \
                                    and isinstance(eval(line_list[2]), int) and (line_list[3] in allowed_orientations):
                                # Initialize the Node with empty word
                                new_node = Node('',  # empty word
                                                eval(line_list[1])[0],  # x_coordinate
                                                eval(line_list[1])[1],  # y_coordinate
                                                eval(line_list[2]),  # blank size
                                                line_list[3])  # orientation

                                # add the node to the blanks list
                                self.blanks[new_node.coordinates] = new_node
        else:
            print(f'Error opening {file_name}. Check if it exists.')

    # determine the domains using the wordlist where a word is in the domain of a variable if it's length is the same as
    # variable word size length
    def __initialize_domains(self):
        for key, node in self.blanks.items():
            for word in self.words:
                if node.word_size == len(word):
                    node.domain.append(word)

    # connect the neighbors of variables
    def __connect_neighbors(self):
        for i, node in self.blanks.items():
            for j, ex_node in self.blanks.items():
                # skip check for same node
                if node != ex_node:
                    # check if nodes have different orientation. Could lead to possible intersection
                    if node.orientation == 'across' and ex_node.orientation == 'down' and \
                            (ex_node not in node.neighbors or node not in ex_node.neighbors):
                        # check for intersection
                        if node.coordinates[1] in range(ex_node.coordinates[1],
                                                        (ex_node.coordinates[1] + ex_node.word_size)) \
                                and ex_node.coordinates[0] in range(node.coordinates[0],
                                                                    (node.coordinates[0] + node.word_size)):
                            # add ex_node as neighbor with the point of intersection as the key
                            node.neighbors[(ex_node.coordinates[0], node.coordinates[1])] = ex_node
                            ex_node.neighbors[(ex_node.coordinates[0], node.coordinates[1])] = node

    # determine if the crossword is empty. Needed in order to determine first variable to assign -> degree heuristic
    def is_empty(self):
        for node in self.blanks:
            if node.word != '':
                return False
        return True

    # print the crossword by overriding __str__ function. Use `print(crossword_object)` to print
    def __str__(self):
        string = ''
        for index, el in enumerate(self.drawing):
            for i, char in enumerate(el):
                string = string + char
            string = string + '\n'
        return string

    def __repr__(self):
        return str(self)

    def print_blanks(self):
        print(self.blanks)
        print(f'Number of blanks: {len(self.blanks)}')


# function to determine if all variables have been assigned
def is_assignment_complete(crossword):
    for key, node in crossword.blanks.items():
        if node.word == '':
            return False
    return True


# determine the variable with most constraints on other variables. In this use case, it is the one with the most
# neighbors may change to return ordered list of nodes.
# should ONLY be called on the first call of backtracking algorithm
def degree_heuristic(crossword):
    # get first node in the list
    max_node = crossword.blanks.get((0, 0))
    for key, node in crossword.blanks.items():
        if max_node != node and (len(node.neighbors) > len(max_node.neighbors)):
            max_node = node
    return max_node


# function used in tie breaking between two nodes when using minimum remaining value.
def degree_heuristic_(this_node, that_node):
    if len(this_node.neighbors) > len(that_node.neighbors):
        return this_node
    else:
        return that_node


# returns the first occurrence of a node that is not assigned
def get_first_unassigned_node(crossword):
    if is_assignment_complete(crossword):
        return None
    else:
        for key, node in crossword.blanks.items():
            if node.word == '':
                return node


# AKA `fail first heuristic`returns the unassigned variable with the least number of possible values left. Hence failing
# early and pruning the search tree
def minimum_remaining_value_heuristic(crossword):
    min_node = get_first_unassigned_node(crossword)
    if min_node is None:
        print('All values assigned. --> MRV')
    else:
        for key, node in crossword.blanks.items():
            if len(node.domain) < len(min_node.domain) and node.word == '':
                min_node = node
    return min_node


# function used in the lambda function of sorted to sort values by least constraining to most constraining
def get_sum_neighbors_values(word, node):
    _sum = 0
    # calculate the total number of restrictions of each neighbor using the given word
    for key, nn in node.neighbors.items():
        # get the respective indices where they intersect
        if node.orientation == 'across':
            node_index = abs(key[0] - node.coordinates[0])
            neigh_index = abs(key[1] - nn.coordinates[1])
        elif node.orientation == 'down':
            node_index = abs(key[1] - node.coordinates[1])
            neigh_index = abs(key[0] - nn.coordinates[0])

        # if key == nn.coordinates:
        #     neigh_index = 0
        for word_nn in nn.domain:
            if word[node_index].lower() == word_nn[neigh_index].lower() and word != word_nn:
                _sum += 1
                print(f'word: {word}, word_nn {word_nn}, sum: {_sum}, node: {node.coordinates} neighbor: {nn.coordinates} n_nn: {node_index}, {neigh_index}')
    return _sum


# Use Least constraining value heuristic to order the values to try for current selected node. It maximizes the choices
# left for neighbors
def order_domain_values(node):
    return sorted(node.domain, key=lambda word: get_sum_neighbors_values(word, node), reverse=True)



""" 
backtracking algorithm
-----------------------
params:
crossword -> crossword object
is_first_call -> Boolean value to determine if function is on root call hence use degree heuristic if true else use 
                Minimum remaining value heuristic    
"""


def backtrack_solve_crossword(crossword, is_first_call=True):
    if is_assignment_complete(crossword):
        return crossword
    # do assignment for specific node. if it's first time the function is called, use degree heuristic to determine the
    # variable to start searching
    if is_first_call:
        node = degree_heuristic(crossword)
    else:
        node = minimum_remaining_value_heuristic(crossword)

    # after determining the node to search order the values to try
    # for word in order_domain_values(node, crossword):
    node = crossword.blanks.get((2, 3))
    domain = order_domain_values(node)
    print(domain)


# function to read the words used to solve the crossword
def read_words(file_name):
    words = []
    if path.exists(file_name):
        with open(file_name, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                words.append(line)
    else:
        print(f'Error opening {file_name}. Check if it exists.')
    return words


def main():
    # relevant filenames
    crossword_file_name = 'crossword.txt'
    words_file_name = 'words.txt'
    blanks_file_name = 'blanks.txt'

    words = read_words(words_file_name)
    crossword = Crossword(crossword_file_name, blanks_file_name, words)
    print(crossword)
    crossword.print_blanks()
    backtrack_solve_crossword(crossword)


if __name__ == '__main__':
    main()
