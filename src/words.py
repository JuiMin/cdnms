# Global holding all the words
WORDBANK = None


def load_words():
    """
    This loads a set of words into memory from file.
    There shouldn't be that many of them so this shouldn't be a too bad on perf
    """
    words = set()
    f = open("./resources/words.txt", "r")
    line = f.readline()
    while line:
        words.add(line.rstrip())
        line = f.readline()
    return words
