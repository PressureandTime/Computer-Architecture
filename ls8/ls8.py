#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
# if len(sys.argv) != True:
#     print("there are no files")
#     sys.exit()

cpu.load()
cpu.run()
