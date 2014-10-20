#!/usr/bin/env python

import re, sys, roman, math

def get_parentheses(text):
  stack = []
  parentheses = {}
  scene_number = 2
  for idx, instr in enumerate(text):
    if instr == '[':
      stack.append(idx)
    elif instr == ']':
      old_idx = stack.pop()
      parentheses[old_idx] = (scene_number, scene_number + 1)
      parentheses[idx] = (scene_number, scene_number + 1)
      scene_number += 2
  return parentheses

def bf_to_shakespeare(instructions):
  instr_pointer = 0
  scene_number = 2
  sums_pointer = 0

  sums = group_sums(instructions)
  instructions = remove_groups(instructions)
  parentheses = get_parentheses(instructions)

  sums = list(sums)

  while instr_pointer < len(instructions):
    instr = instructions[instr_pointer]
    if instr == '>':
      forward_pointer()
    elif instr == '<':
      backward_pointer()
    elif instr == '?':
      modify_value(sums[sums_pointer])
      sums_pointer += 1
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
  print("The Interpreted Brainfuck.\n")
  print("Romeo, a stack that represents man's present and past.")
  print("Juliet, a stack that represents woman's future.")
  print("Lady Macbeth, a zero that is only good for comparison.\n")
  print("Act I: An egregious abuse.")
  print("Scene I: The fattening of Juliet.") # Build up the Juliet stack
  print("[Enter Romeo and Juliet]\n")
  sys.stdout.write("Romeo: ")
  for x in range(1024):
    sys.stdout.write("Remember thyself! ")
  sys.stdout.write("\n")
  print("[Exeunt]\n")
  print("Act II: Our main performance.\n")
  print("Scene I: It begins here.\n")
  print("[Enter Romeo and Juliet]\n")
  bf_to_shakespeare(text)
  print("\n[Exeunt]")

def forward_pointer():
  print("Juliet: Remember thyself!")
  print("Romeo: Recall the sins of the fathers.")
  print("Juliet: You are as good as me.")

def backward_pointer():
  print("Romeo: You are as good as me! Remember thyself.")
  print("Juliet: Recall yourself.")

def modify_value(value):
  print(sum_up_or_subtract_down(value, value > 0))

def sum_up_or_subtract_down(value, incrementing):
  command = "Juliet: "
  # There's some bit math here, so abandon all hope all ye who enter here.
  if not incrementing:
    value = -value
  next_highest_power_of_two = math.ceil(math.log(value, 2))
  subtraction = (2**next_highest_power_of_two) - value

  subtraction_powers_of_two = get_powers_of_two(subtraction)
  value_powers_of_two = get_powers_of_two(value)

  # The fewer 1s in the representation, the fewer operations
  if (bin(subtraction).count('1') < bin(value).count('1')):
    if incrementing:
      # If we're adding, we'll add the next biggest power of two
      # and subtract down to our target value
      command += generate_summation_statement(next_highest_power_of_two, True)
      for power_of_two in subtraction_powers_of_two:
        command += generate_summation_statement(power_of_two, False)
    else:
      # If we're subtracting, we'll subtract the highest power and add back up
      command += generate_summation_statement(next_highest_power_of_two, False)
      for power_of_two in subtraction_powers_of_two:
        command += generate_summation_statement(power_of_two, True)
  else:
    if incrementing:
      # If we're adding, we'll just add all the bits in our target value
      for power_of_two in value_powers_of_two:
        command += generate_summation_statement(power_of_two, True)
    else:
      # If we're subtracting, it's easier to just subtract down
      for power_of_two in value_powers_of_two:
        command += generate_summation_statement(power_of_two, False)
  return command

def get_powers_of_two(value):
  binary_representation  = bin(value)[2:]
  powers_of_two = []
  for idx, digit in enumerate(binary_representation):
    if int(digit):
      powers_of_two.append(len(binary_representation) - idx - 1)
  return powers_of_two

def generate_summation_statement(power, incrementing):
  command = "You are as large as the " + ("sum of " if incrementing else \
"difference between ") + "yourself and a "
  for x in range(power):
    command += "big "
  command += "cat! "
  return command

def open_bracket(pointer, parentheses):
  open_paren, close_paren = parentheses[pointer]
  print("\nScene " + numeral(open_paren) + ": Another scene.\n")
  print("[Exeunt]\n")
  print("[Enter Lady Macbeth and Romeo]\n")
  print("Lady Macbeth: Are you as good as me?")
  print("Romeo: If so, let us proceed to scene " + \
        numeral(close_paren) + ".\n")
  print("[Exit Lady Macbeth]\n")
  print("[Enter Juliet]\n")

def close_bracket(pointer, parentheses):
  open_paren, close_paren = parentheses[pointer]
  print("\n[Exit Juliet]\n")
  print("[Enter Lady Macbeth]\n")
  print("Lady Macbeth: Are you as bad as me?")
  print("Romeo: If not, let us proceed to scene " + \
        numeral(open_paren) + ".")
  print("[Exeunt]\n")
  print("Scene " + numeral(close_paren) + ": Another scene.\n")
  print("[Exeunt]\n")
  print("[Enter Romeo and Juliet]\n")

def print_value():
  print("Juliet: Speak your mind!")

def get_value():
  print("Juliet: Open your mind!")

def numeral(number):
  return roman.toRoman(number)

def group_sums_helper(string):
  total_minuses = string.count('-')
  total_pluses = string.count('+')
  return total_pluses - total_minuses

def group_sums(text):
  pluses = re.sub('[^\+\-]', '?', text).split('?')
  filtered = filter(None, pluses)
  totals = map(group_sums_helper, filtered)
  return totals

def remove_groups(text):
  text = re.sub('[\+\-]', '?', text)
  text = re.sub('\?+', '?', text)
  return text

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
