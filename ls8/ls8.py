#!/usr/bin/env python3

# """Main."""

# import sys
# from cpu import *

# cpu = CPU()
# if len(sys.argv) != 2:
#     print("there are no files")
#     sys.exit()

# print(sys.argv[1])

# cpu.load(sys.argv[1])
# cpu.run()


"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()


