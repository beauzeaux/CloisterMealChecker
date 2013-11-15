from evdevinput import getInputLine

def get_swipe():
    line = getInputLine()
    swipe = {}
    swipe["first"], swipe["last"] = line.split(';')[0].split("=")[1].split("/")[:2]
    swipe["id"] = line.split(';')[0].split("=")[0][7:-1]
    return swipe
    
    
