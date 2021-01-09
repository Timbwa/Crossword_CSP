from os import path
# TODO think about backtracking strategy and problem formulation


# class representing the node in a CSP graph - similar to blanks in the crossword
class Node(object):
    def __init__(self, word, x_coordinate, y_coordinate, word_size, orientation):
        self._word = word
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.word_size = word_size
        self.orientation = orientation

        # list of immediate Node neighbors, where a neighbor is a blank whose starting position is part
        # of another blank
        self.neighbors = []


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
        if path.exists(file_name):
            with open(file_name, 'r') as f:
                for line in f:
                    # remove trailing new-line char
                    line = line.rstrip('\n')
                    # skip lines starting with '#' as they are comments in the file
                    if line.startswith('#'):
                        continue
                    else:
                        my_list = line.split(';')
                        print(my_list)

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


def main():
    # relevant filenames
    crossword_file_name = 'crossword.txt'
    words_file_name = 'words.txt'
    blanks_file_name = 'blanks.txt'

    crossword = Crossword(crossword_file_name)
    # print(crossword)
    crossword.read_blanks(blanks_file_name)


if __name__ == '__main__':
    main()
