import re, sys, random

# Read in the BF file
f = open("test.txt", "r")
text = f.read()
text = re.sub('[^><\+\-\.,\[\]]', '', text)
f.close()

# Read in the names file
names = []
f = open("characters.txt", "r")
for line in f:
  line = line.strip()
  names.append(line)
random.shuffle(names)

def get_parentheses(text, parentheses):
  stack = []
  for idx, instr in enumerate(text):
    if instr == '[':
      stack.append(idx)
    elif instr == ']':
      old_idx = stack.pop()
      parentheses[old_idx] = idx
      parentheses[idx] = old_idx

def get_character(pointer, characters):
  global names
  if pointer not in characters:
    characters[pointer] = names[pointer]
  return characters[pointer]

def interpret_bf(instructions, memory, paranthesies, characters, scenes):
  MOVE_POINTER = 0
  CHANGE_VALUE = 1
  PRINT_VALUE = 2

  instr_pointer = 0
  pointer = 0
  shakespeare = []
  characters_on_stage = []
  scene_number = 1
  current_instr_type = 0

  while instr_pointer < len(instructions):
    instr = text[instr_pointer]
    if instr == '>':
      pointer += 1
    elif instr == '<':
      pointer -= 1
    elif instr == '.':
      sys.stdout.write(chr(memory[pointer]))
    elif instr == '[':
      if memory[pointer] == 0:
        instr_pointer = paranthesies[instr_pointer]
    elif instr == ']':
      if memory[pointer] != 0:
        instr_pointer = paranthesies[instr_pointer]
    elif instr == '+':
      memory[pointer] += 1
      get_character(pointer, characters)
      summing = True
    elif instr == '-':
      memory[pointer] -= 1
      get_character(pointer, characters)
      summing = True
    instr_pointer += 1

def print_shakespeare(text):
  memory = {}
  for x in range(1024):
    memory[x] = 0
  parentheses = {}
  characters = {}
  scenes = {}
  get_parentheses(text, parentheses)
  interpret_bf(text, memory, parentheses, characters, scenes)
  print "The Interpreted Brainfudge.\n"
  for idx, character in characters.iteritems():
    print "{character}, a big baloo.".format(character=character)
  print ""
  print "Act I: The Default."

def run_bf(instructions):
  memory = {}
  for x in range(1024):
    memory[x] = 0
  parentheses = {}
  characters = {}
  get_parentheses(text, parentheses)
  instr_pointer = 0
  pointer = 0
  while instr_pointer < len(instructions):
    instr = text[instr_pointer]
    if instr == '>':
      pointer += 1
    elif instr == '<':
      pointer -= 1
    elif instr == '+':
      memory[pointer] += 1
    elif instr == '-':
      memory[pointer] -= 1
    elif instr == '.':
      sys.stdout.write(chr(memory[pointer]))
    elif instr == '[':
      if memory[pointer] == 0:
        instr_pointer = parentheses[instr_pointer]
    elif instr == ']':
      if memory[pointer] != 0:
        instr_pointer = parentheses[instr_pointer]
    instr_pointer += 1

print_shakespeare(text)
#run_bf(text)