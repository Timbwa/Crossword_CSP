from os import path
# TODO think about backtracking strategy and problem formulation


# class representing the node in a CSP graph - similar to blanks in the crossword
class Node(object):
    __rec_count = 0  # to prevent infinite recursion of neighbors

    def __init__(self, word, x_coordinate, y_coordinate, word_size, orientation):
        self.word = word
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.word_size = word_size
        self.orientation = orientation

        # list of immediate Node neighbors, where a neighbor is a blank whose starting position is part
        # of another blank
        self.neighbors = []

    # override the __str__ functions to print the Node
    def __str__(self):
        # only print immediate neighbors
        if self.__rec_count == 1:
            self.__rec_count = 0
            return f'Word: {self.word}\n' \
                   f'First Letter Coordinates: {(self.x_coordinate, self.y_coordinate)}\n' \
                   f'Word size: {self.word_size}\n' \
                   f'Orientation: {self.orientation}\n'
        else:
            return f'Word: {self.word}\n' \
                   f'First Letter Coordinates: {(self.x_coordinate, self.y_coordinate)}\n' \
                   f'Word size: {self.word_size}\n' \
                   f'Orientation: {self.orientation}'

    def __repr__(self):
        self.__rec_count += 1
        return str(self)


# A class representing the Crossword drawing with the blanks and their positions
class Crossword(object):
    def __init__(self, file_name):
        # a 2D array of characters representing the crossword drawing
        self.drawing = []
        # a list of blanks of type Nodes representing
        self.blanks = []
        # file name of the .txt file with the crossword drawing
        self.file_name = file_name
        # try reading the crossword from the file
        self.__read_crossword(file_name)

    # read the crossword drawing from .txt file and represent it using 2D array
    def __read_crossword(self, file_name):
        if path.exists(file_name):
            with open(file_name, 'r') as f:
                for line in f:
                    self.drawing.append([el for index, el in enumerate(line.rstrip('\n'))])
        else:
            print(f'Error opening {file_name}. Check if it exists.')

    # create nodes representing the blanks in the crossword
    def read_blanks(self, file_name):
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
                                new_node = Node('',                     # empty word
                                                eval(line_list[1])[0],  # x_coordinate
                                                eval(line_list[1])[1],  # y_coordinate
                                                eval(line_list[2]),     # blank size
                                                line_list[3])           # orientation

                                # add the node to the blanks list
                                self.blanks.append(new_node)

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


def main():
    # relevant filenames
    crossword_file_name = 'crossword.txt'
    words_file_name = 'words.txt'
    blanks_file_name = 'blanks.txt'

    crossword = Crossword(crossword_file_name)
    # print(crossword)
    crossword.read_blanks(blanks_file_name)
    crossword.print_blanks()


if __name__ == '__main__':
    main()
