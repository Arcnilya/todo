import sys
import os
import json
import operator

file_name = "test.json"

JSON_404_MSG = "File not found, creating new set of items"
ERR_ARGLEN_MSG = "Not enough arguments"
ERR_NOKEY_MSG = "Command not found"
ERR_INDEX_MSG = "Index out of bounds"

class Item:
  def __init__(self, name, weight, score):
    self.name = name
    self.weight = int(weight)
    self.score = int(score)
  def update(self):
    self.score = self.score + (10 * self.weight)
  def reset(self):
    self.score = 0
  def change(weigth):
    self.weight = weight

def items2JSON(items):
  temp_json = []
  for item in items:
    temp_json.append(item.__dict__)
  return temp_json

def JSON2items(json):
  temp_list = []
  for item in json:
    temp_list.append(Item(item['name'], item['weight'], item['score']))
  return temp_list

def reader():
  with open(file_name, 'r') as f:
    return JSON2items(json.load(f))

def writer(items):
  with open(file_name, 'w') as f:
    json.dump(items2JSON(items), f, indent=4)

# Adds a new item with Item(name, weight, score)
def add(args, items):
  if len(args) < 3:
    exit(ERR_ARGLEN_MSG)
  items.append(Item(args[0], args[1], args[2]))
  return show(args, items)

# Displays all items
def show(args, items):
  items.sort(key=operator.attrgetter('score'), reverse=True)
  index = 0
  print("Index  Name      Weight  Score")
  for item in items:
    print("{}      {}     {}       {}".format(index, item.name, item.weight, item.score))
    index = index + 1
  return items

# Selects item on given index
def select(args, items):
  if int(args[0]) > len(items) or int(args[0]) < 0:
    exit(ERR_INDEX_MSG)
  for item in items:
    item.update()               # Update all item scores
  items[int(args[0])].reset()   # Reset selected item
  return show(args, items)

# Removes item on given index
def remove(args, items):
  if int(args[0]) > len(items) or int(args[0]) < 0:
    exit(ERR_INDEX_MSG)
  items.remove(items[int(args[0])])
  return show(args, items)

def main():
  items = []
  
  # Parameters: args & items
  commands = {
    'add': add,
    'show': show,
    'select': select,
    'remove': remove,
  }

  if len(sys.argv) < 2:
    exit(ERR_ARGLEN_MSG)

  if not sys.argv[1] in commands.keys():
    exit(ERR_NOKEY_MSG)

  try:
    items = reader()
  except:
    print(JSON_404_MSG)
  
  items = commands[sys.argv[1]](sys.argv[2:], items)  
  writer(items)

if __name__ == "__main__":
  main()
