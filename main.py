import re, sys, random

# Read in the BF file
f = open("test_pointers.txt", "r")
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

def bf_to_shakespeare(instructions, parentheses):
  instr_pointer = 0
  scene_number = 2

  while instr_pointer < len(instructions):
    instr = text[instr_pointer]
    if instr == '>':
      forward_pointer()
    elif instr == '<':
      backward_pointer()
    instr_pointer += 1

def print_shakespeare(text):
  memory = {}
  for x in range(1024):
    memory[x] = 0
  parentheses = {}
  characters = {}
  get_parentheses(text, parentheses)
#  interpret_bf(text, memory, parentheses, characters)
  print "The Interpreted Brainfudge.\n"
  print "Romeo, a stack."
  print "Juliet, a stack from THE FUTURE."
  print "Lady Macbeth, a zero.\n"
  print "Act I: An egregious abuse."
  print "Scene I: The fattening of Juliet."
  print "[Enter Romeo and Juliet]"
  sys.stdout.write("Romeo: ")
  for x in range(1024):
    sys.stdout.write("Remember thyself! ")
  sys.stdout.write("\n")
  print "[Exeunt]"
  print "Act 2: Our Main Performance"
  print "[Enter Romeo and Juliet]"
  bf_to_shakespeare(text, parentheses)

def forward_pointer():
  print "Juliet: Remember thyself!"
  print "Romeo: Recall the sins of the fathers."
  print "Juliet: You are as good as me."

def backward_pointer():
  print "Romeo: You are as bad as me! Remember the days."
  print "Juliet: Remember yourself."
  
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
