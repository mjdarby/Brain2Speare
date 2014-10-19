#!/usr/bin/env python

import re, sys, roman

def get_parentheses(text, parentheses):
  stack = []
  scene_number = 2
  for idx, instr in enumerate(text):
    if instr == '[':
      stack.append(idx)
    elif instr == ']':
      old_idx = stack.pop()
      parentheses[old_idx] = scene_number
      parentheses[idx] = scene_number + 1
      scene_number += 2

def bf_to_shakespeare(instructions, parentheses):
  instr_pointer = 0
  scene_number = 2

  while instr_pointer < len(instructions):
    instr = text[instr_pointer]
    if instr == '>':
      forward_pointer()
    elif instr == '<':
      backward_pointer()
    elif instr == '+':
      increment()
    elif instr == '-':
      decrement()
    elif instr == '.':
      print_value()
    elif instr == ',':
      get_value()
    elif instr == '[':
      open_bracket(instr_pointer, parentheses)
    elif instr == ']':
      close_bracket(instr_pointer, parentheses)
    instr_pointer += 1

def print_shakespeare(text):
  parentheses = {}
  get_parentheses(text, parentheses)
  print("The Interpreted Brainfudge.\n")
  print("Romeo, a stack.")
  print("Juliet, a stack from THE FUTURE.")
  print("Lady Macbeth, a zero.\n")
  print("Act I: An egregious abuse.")
  print("Scene I: The fattening of Juliet.") # Build up the Juliet stack
  print("[Enter Romeo and Juliet]\n")
  sys.stdout.write("Romeo: ")
  for x in range(1024):
    sys.stdout.write("Remember thyself! ")
  sys.stdout.write("\n")
  print("[Exeunt]\n")
  print("Act II: Our main erformance.\n")
  print("Scene I: It begins and ends here.\n")
  print("[Enter Romeo and Juliet]\n")
  bf_to_shakespeare(text, parentheses)
  print("\n[Exeunt]")

def forward_pointer():
  print("Juliet: Remember thyself!")
  print("Romeo: Recall the sins of the fathers.")
  print("Juliet: You are as good as me.")

def backward_pointer():
  print("Romeo: You are as good as me! Remember thyself.")
  print("Juliet: Recall yourself.")

def increment():
  print("Juliet: You are as handsome as the sum of thyself and a cat.")

def decrement():
  print("Juliet: You are as handsome as the sum of thyself and a pig.")

def open_bracket(pointer, parentheses):
  print("\n[Exeunt]\n")
  print("Scene " + numeral(pointer) + ": Another scene.\n")
  print("[Exeunt]\n")
  print("[Enter Lady Macbeth and Romeo]\n")
  print("Lady Macbeth: Are you as good as me?")
  print("Romeo: If so, let us proceed to scene " + \
        numeral(parentheses[pointer]) + ".\n")
  print("[Exit Lady Macbeth]\n")
  print("[Enter Juliet]\n")

def close_bracket(pointer, parentheses):
  print("\n[Exit Juliet]\n")
  print("[Enter Lady Macbeth]\n")
  print("Lady Macbeth: Are you as bad as me?")
  print("Romeo: If not, let us proceed to scene " + \
        numeral(parentheses[pointer]) + ".")
  print("[Exeunt]\n")
  print("Scene " + numeral(pointer) + ": Another scene.\n")
  print("[Exeunt]\n")
  print("[Enter Romeo and Juliet]\n")

def print_value():
  print("Juliet: Speak your mind!")

def get_value():
  print("Juliet: Open your mind!")

def numeral(number):
  return roman.toRoman(number)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: ./brain2speare.py input.b > output.spl")
    sys.exit(2)
  filename = sys.argv[1]
  # Read in the BF file
  f = open(filename, "r")
  text = f.read()
  text = re.sub('[^><\+\-\.,\[\]]', '', text)
  f.close()

  print_shakespeare(text)
