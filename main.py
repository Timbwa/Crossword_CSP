from os import path


# TODO think about backtracking strategy and problem formulation
# degree heuristic -> number of connected neighbors. For first time solving
# Variable ordering heuristic -> Minimum remaining variables
# Least constraining heuristic -> Least constraining value


# class representing the node in a CSP graph - similar to blanks in the crossword
# they will be the variables with constraints
class Node(object):
    __rec_count = 0  # to prevent infinite recursion of neighbors

    def __init__(self, word, x_coordinate, y_coordinate, word_size, orientation):
        self.word = word
        self.coordinates = (x_coordinate, y_coordinate)
        self.word_size = word_size
        self.orientation = orientation

        # list of immediate Node neighbors, where a neighbor is a blank whose starting position is part of another
        # blank For the neighbors dict, the key is the coordinate of the first char of the neighbor, value is the
        # neighboring node object
        self.neighbors = {}

    # override the __str__ functions to print the Node
    def __str__(self):
        # only print immediate neighbors
        if self.__rec_count == 1:
            self.__rec_count = 0
            return f'First Letter Coordinates: {self.coordinates}\n' \
                   f'Orientation: {self.orientation}\n'
        else:
            return f'\nWord: {self.word}\n' \
                   f'First Letter Coordinates: {self.coordinates}\n' \
                   f'Word size: {self.word_size}\n' \
                   f'Orientation: {self.orientation}\n' \
                   f'Neighbors: {self.neighbors}\n'

    def __repr__(self):
        self.__rec_count += 1
        return str(self)

    # override equality comparator. This assumes the starting char of a blank can't be in the same coordinates
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coordinates == other.coordinates

    # override hash function for faster lookup in dictionaries
    # hash the coordinates as I assume the starting char of a blank can't be in the same coordinates
    def __hash__(self):
        return hash(self.coordinates)


# A class representing the Crossword drawing with the blanks and their positions
class Crossword(object):
    def __init__(self, file_name, blanks_file_name):
        # a 2D array of characters representing the crossword drawing
        self.drawing = []
        # a list of blanks of type Nodes representing
        self.blanks = {}
        # file name of the .txt file with the crossword drawing
        self.file_name = file_name
        # try reading the crossword from the file
        self.__read_crossword(file_name)
        # try reading the blanks from blanks.txt file
        self.__read_blanks(blanks_file_name)
        # connect the neighbors
        self.connect_neighbors()

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

    # TODO connect neighbors
    # connect the neighbors of variables
    # noinspection DuplicatedCode
    def connect_neighbors(self):
        # find neighbors for all nodes
        for index, node in self.blanks.items():
            # look for nodes
            if node.orientation == 'across':
                # go over whole list of nodes ignoring current one
                for index1, ex_node in self.blanks.items():
                    if node == ex_node:
                        continue
                    else:
                        # check for nodes in the same row
                        if ex_node.coordinates[1] == node.coordinates[1] \
                                and ex_node not in node.neighbors \
                                and node not in ex_node.neighbors:
                            node.neighbors[ex_node.coordinates] = ex_node
                            ex_node.neighbors[node.coordinates] = node
            elif node.orientation == 'down':
                for index1, ex_node in self.blanks.items():
                    if node == ex_node:
                        continue
                    else:
                        # check for nodes in the same column
                        if ex_node.coordinates[1] == node.coordinates[1]\
                                and ex_node not in node.neighbors \
                                and node not in ex_node.neighbors:
                            node.neighbors[ex_node.coordinates] = ex_node
                            ex_node.neighbors[node.coordinates] = node

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

    crossword = Crossword(crossword_file_name, blanks_file_name)
    # print(crossword)
    crossword.print_blanks()

    words = read_words(words_file_name)


if __name__ == '__main__':
    main()
