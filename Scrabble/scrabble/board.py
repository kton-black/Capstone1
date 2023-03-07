import pygame
import ConfigParser

class Scrabble_Board(object):

    def __init__(self):
        pass

    def load_file(self, file="board.ini"):
        self.board = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(file)
        #self.tileset = parser.get("board","image")
        self.board = parser.get("board","board")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return
        try:
            return self.key[char]
        except KeyError:
            return {}