#Brainfuck interpreter -- ascii bene
import sys

class Brnfck():

    def __init__(self, tape_size):

        # number of cells
        self.tape_size=tape_size
        # buffer (or tape) the brainfuck program manipulates
        self.__tape = bytearray([0] * tape_size)

        # pointer to the write/read head on the buffer
        self.__tape_ptr = 0

        # current position in the program (charnumber)
        self.__cmd_ptr = 0

        # current position on the input (hen reading input)
        self.__ipt_ptr = 0

        # loop tape pointer stack for loop count pointer positions
        self.__lp_cnt_ptr_stk = []

        # loop command pointer stack for jumpback pointer positions
        self.__lp_cmd_ptr_stk = []

        # loop skiping flag if loop counter is zero to start with (False = skip)
        self.__lp_skp_flg = True


    # execute a brainfuck programm, optionally with an input
    def run(self, prg, ipt=""):
        # output of the program
        opt = ""

        # evaluate each command from the brainfuck program
        while (self.__cmd_ptr <= len(prg)):
            # get current command (chat) from program string
            cmd = prg[self.__cmd_ptr]
            
            # move the tape pointer one position to the righht
            if self.__lp_skp_flg and cmd == ">":
                if self.__tape_ptr < self.tape_size:
                    self.__tape_ptr += 1
                elif self.__tape_ptr >= self.tape_size:
                    self.__tape_ptr=0

            # move the tape pointer one position to the left
            elif self.__lp_skp_flg and cmd == "<":
                if self.__tape_ptr > 0:
                    self.__tape_ptr -= 1
                else:
                    self.__tape_ptr = self.tape_size          

            # increase the current buffer cell by one
            elif self.__lp_skp_flg and cmd == "+":
                self.__tape[self.__tape_ptr] += 1

            # decrease the current buffer cell by one
            elif self.__lp_skp_flg and cmd == "-":
                self.__tape[self.__tape_ptr] -= 1

            # print the current buffer cell as the respective ASCII character
            elif self.__lp_skp_flg and cmd == ".":
                opt += chr(self.__tape[self.__tape_ptr])

            # read the current input character and store in the the current buffer cell
            elif self.__lp_skp_flg and cmd == ",":
                self.__tape[self.__tape_ptr] = ord(ipt[self.__ipt_ptr])
                self.__ipt_ptr += 1

        3    # loop over the enclosed commands until the current buffer cell is 0
            elif self.__lp_skp_flg and cmd == "[":

                # store the loop counter for the current loop
                self.__lp_cnt_ptr_stk.append(self.__tape_ptr)

                # store the jumpback address for the current loop
                self.__lp_cmd_ptr_stk.append(self.__cmd_ptr)

                # set loop skipping flag, if initial loop counter is zero
                if self.__tape[self.__tape_ptr] == 0:
                    self.__lp_skp_flg = False

            elif cmd == "]":

                # reset loop skipping flag
                self.__lp_skp_flg = True

                # check for left iterations of loop
                if self.__tape[self.__lp_cnt_ptr_stk[-1]] == 0:

                    # remove cell adress from loop count pointer stack
                    self.__lp_cnt_ptr_stk.pop()
                    # remove program "adress" from loop jumpback pointer stack
                    self.__lp_cmd_ptr_stk.pop()
                    
                else:
                    # jump back to the jumpback address of the most inner loop
                    self.__cmd_ptr = self.__lp_cmd_ptr_stk[-1]

            # move pointer to next command in brainfuck program
            self.__cmd_ptr += 1

        # print the program's output at the end
        print("%s" % (opt))
        # TODO print execution time

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("================ brnfck -- Rebooted v0.12 ================")
        print("USAGE: python brnfck.py \"<program>\" [\"<input>\"]")
    elif len(sys.argv) >= 2:
        bf = Brnfck(30)
        bf.run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
