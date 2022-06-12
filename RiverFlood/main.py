# A python file to create a river and make some queries

import river as riv
import read

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    north, south, islands = read.readFromFile("../rivers/rectangle.riv")
    river = riv.River(north, south, islands)
    print("successfully created a river")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
