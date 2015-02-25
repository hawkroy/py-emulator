import sys
import logging

from simparse import *

#############################
#           Test prog       #
#############################
def test():
    if len(sys.argv) == 2:
        data = open(sys.argv[1]).read()

        # logging.basicConfig(
        #                 level = logging.DEBUG,
        #                 filename = "parselog.txt",
        #                 filemode = "w",
        #                 format = "%(filename)10s:%(lineno)4d:%(message)s"
        # )
        # log = logging.getLogger()
        prog = parse(data, debug=0)

        print prog
        # while True:
        #     tok = lexer.token()
        #     if not tok:
        #         break
        #     print tok

if __name__ == "__main__":
    test()
