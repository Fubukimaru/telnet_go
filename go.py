import subprocess


class Go:

    def get_output(self, skip=0):
        output = ""
        for line in iter(self.game.stdout.readline, ''):
            line = line.rstrip().decode()
            if not line:
                break
            if skip > 0:
                skip -= 1
            else:
                output += line + '\n'
        return(output)

    def correct_move(self, line):
        return(line.split()[0] == "=")

    def print_board(self):
        # Show board
        self.game.stdin.write(b"showboard\n")
        self.game.stdin.flush()
        # Get board and remove first line
        output = self.get_output(skip=1)
        return(output)

    def get_move(self):
        self.game.stdin.write(b"genmove white\n")
        self.game.stdin.flush()
        return(self.get_output())

    def do_move(self, move):
        move = "black {}\n".format(move)
        self.game.stdin.write(move.encode())
        self.game.stdin.flush()
        return(self.get_output())

    def print_move(self, move):
        # First is =
        return(move.split()[1]+"\n")

    def go_black_round_init(self):
        return("Black's turn. Enter your move:\n")

    def go_black_round(self, move_in):
        # Move black
        move = self.do_move(move_in)
        msg_back = ""
        correct = self.correct_move(move)
        msg_back += self.print_board()
        if not correct:
            msg_back += move + "\n"
        else:
            self.status = 1
        return(msg_back)

    def go_white_round(self):
        # Move white
        msg_back = ""
        msg_back += "White's turn\n"
        msg_back += self.print_move(self.get_move())
        # if output == '' and game.poll() is not None:
        #     break
        msg_back += "Board status:\n"
        msg_back += self.print_board()
        # rc = self.game.poll()
        # return rc
        self.status = 0
        return(msg_back)

    def __init__(self, size=9):
        command = ['gnugo', '--mode', 'gtp']
        self.game = subprocess.Popen(command, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        self.status = 0
        query = "boardsize {}\n".format(size)
        self.game.stdin.write(query.encode())
        self.game.stdin.flush()
        self.get_output()
