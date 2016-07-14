# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("square", help="squares input number", type=int)
# # arser.add_argument("-v", "--verbose", help="increase output verbosity",
# #                     action="store_true") # action= count
# parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
#                     help="increase output verbosity")
# args = parser.parse_args()
# if args.verbose:
#     print "verbosity turned on"
#     print args.verbose
# print args.square ** 2

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--size", type=tuple, help="frame size")
args = parser.parse_args()
if args.size:
    print len(args.size)
    print args.size
