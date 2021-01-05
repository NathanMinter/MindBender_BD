import sys
import pickle

## Class for creating shelves of the fridge
class FridgeShelf:
    def __init__(self, shelf):
        self.shelf = shelf
        ## Contents of shelf start as empty list
        self.contents = []
        ## How full is the shelf, based on size of items on that shelf
        self.fullness = 0
        ## Set max fullness of the shelf based on which shelf it is
        if (self.shelf == "small"):
            self.maxItems = 1
        elif (self.shelf == "medium"):
            self.maxItems = 2
        elif (self.shelf == "large"):
            self.maxItems = 3
        else:
            raise ValueError("FridgeShelf shelf must be small, medium, or large")

    ## Function to put items onto shelf
    def put(self, item, size):
        if ((self.fullness + size) > self.maxItems):
            print("No room on {} shelf.".format(self.shelf))
        else:
            self.contents.append(item)
            self.fullness += size
            print("{} has been placed on {} shelf.".format(item, self.shelf))

    ## Function to list items on shelf
    def list(self):
        print("{} shelf contains {}".format(self.shelf, self.contents))

try:
    with open('/home/n/opt/MindBender_BD/task-fridge/small.pydata', 'rb') as s:
        smallShelf = pickle.load(s)
except:
    smallShelf = FridgeShelf("small")

try:
    with open('/home/n/opt/MindBender_BD/task-fridge/medium.pydata', 'rb') as m:
        mediumShelf = pickle.load(m)
except:
    mediumShelf = FridgeShelf("medium")

try:
    with open('/home/n/opt/MindBender_BD/task-fridge/large.pydata', 'rb') as l:
        largeShelf = pickle.load(l)
except:
    largeShelf = FridgeShelf("large")

shelves = [largeShelf, mediumShelf, smallShelf]

def get(item, size):
    for shelf in shelves:
        if item in shelf.contents:
            shelf.contents.remove(item)
            shelf.fullness = max(0, shelf.fullness - size)
            print("{} taken from {} shelf.".format(item, shelf.shelf))
            break
        else:
            print("{} not found on {} shelf.".format(item, shelf.shelf))

def check():
    for shelf in shelves:
        shelf.list()


## Check for parameters when calling python script
try:
    action = sys.argv[1].lower()
    ## If put, then item will be put into fridge
    if (action == "put"):
        ## Requires shelf to put item on
        try:
            shelf = sys.argv[2].lower()
            if (shelf == "small") or (shelf == "medium") or (shelf == "large"):
                ## Requires item name to be put into fridge
                try:
                    item = sys.argv[3].lower()
                except:
                    print("No item parameter")
                ## Requires size of item to be put into fridge
                try:
                    size = int(sys.argv[4])
                    if (size > 0) and (size < 4):
                        ## Run put function
                        if (shelf == "small"):
                            smallShelf.put(item, size)
                        elif (shelf == "medium"):
                            mediumShelf.put(item, size)
                        elif (shelf == "large"):
                            largeShelf.put(item, size)
                    else:
                        print("Size must be 1, 2, or 3")
                except:
                    print("No size parameter")

            else:
                print("Shelf must be small, medium, or large")
        except:
            print("No shelf parameter")

    ## If get, then item will be taken from fridge
    elif (action == "get"):
        ## Requires name of item to take from fridge
        try:
            item = sys.argv[2].lower()
        except:
            print("No item parameter")
        ## Requires size of item to be taken from fridge
        try:
            size = int(sys.argv[3])
            if (size > 0) and (size < 4):
                ## Run get function
                get(item, size)
            else:
                print("Size must be 1, 2, or 3")
        except:
            print("No numerical size parameter")

    ## If check, then contents of fridge will be checked
    elif (action == "check"):
        ## Run check function
        check()
    else:
        print("Action must be put, get, or check")

except:
    print("No action parameter")

## Update shelf files
with open('/home/n/opt/MindBender_BD/task-fridge/small.pydata', 'wb') as s:
    pickle.dump(smallShelf, s)
with open('/home/n/opt/MindBender_BD/task-fridge/medium.pydata', 'wb') as m:
    pickle.dump(mediumShelf, m)
with open('/home/n/opt/MindBender_BD/task-fridge/large.pydata', 'wb') as l:
    pickle.dump(largeShelf, l)
