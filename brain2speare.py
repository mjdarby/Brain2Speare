#!/usr/bin/env python

import re, sys, roman, math, random

# Functions to convert the BF to Shakespeare

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
  shakespeare = ""

  sums = group_sums(instructions)
  instructions = remove_groups(instructions)
  parentheses = get_parentheses(instructions)

  sums = list(sums)

  while instr_pointer < len(instructions):
    instr = instructions[instr_pointer]
    if instr == '>':
      shakespeare += forward_pointer()
    elif instr == '<':
      shakespeare += backward_pointer()
    elif instr == '?':
      shakespeare += modify_value(sums[sums_pointer])
      sums_pointer += 1
    elif instr == '.':
      shakespeare += print_value()
    elif instr == ',':
      shakespeare += get_value()
    elif instr == '[':
      shakespeare += open_bracket(instr_pointer, parentheses)
    elif instr == ']':
      shakespeare += close_bracket(instr_pointer, parentheses)
    instr_pointer += 1

  return shakespeare

def get_shakespeare(text):
  shakespeare = ""
  parentheses = {}
  shakespeare += "The Interpreted Brainfuck.\n\n"
  shakespeare += "Romeo, a stack that represents man's present and past.\n"
  shakespeare += "Juliet, a stack that represents woman's future.\n"
  shakespeare += "Lady Macbeth, a zero that is only good for comparison.\n\n"
  shakespeare += "Act I: An egregious abuse.\n"
  shakespeare += "Scene I: The fattening of Juliet.\n" # Build up the Juliet stack
  shakespeare += "[Enter Romeo and Juliet]\n\n"
  shakespeare += "Romeo: "
  for x in range(1024):
    shakespeare += "Remember yourself! "
  shakespeare += "\n"
  shakespeare += "[Exeunt]\n\n"
  shakespeare += "Act II: Our main performance.\n\n"
  shakespeare += "Scene I: It begins here.\n\n"
  shakespeare += "[Enter Romeo and Juliet]\n\n"
  shakespeare += bf_to_shakespeare(text)
  shakespeare += "\n[Exeunt]\n"
  return shakespeare

def forward_pointer():
  command = ""
  command += "Juliet: Remember yourself!\n"
  command += "Romeo: Recall the sins of the fathers.\n"
  command += "Juliet: You are as good as me.\n"
  return command

def backward_pointer():
  command = ""
  command += "Romeo: You are as good as me! Remember yourself.\n"
  command += "Juliet: Recall yourself.\n"
  return command

def modify_value(value):
  command = sum_up_or_subtract_down(value, value > 0)
  return command

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
  return command + "\n"

def get_powers_of_two(value):
  binary_representation  = bin(value)[2:]
  powers_of_two = []
  for idx, digit in enumerate(binary_representation):
    if int(digit):
      powers_of_two.append(len(binary_representation) - idx - 1)
  return powers_of_two

def generate_summation_statement(power, incrementing):
  choices = [(incrementing, True), (not incrementing, False)]
  positive_sum, positive_noun = random.choice(choices)
  command = "Secondperson are as large as the " + ("sum of " if \
positive_sum else "difference between ") + "yourself and a "
  for x in range(power):
    if positive_noun:
      command += "posadj "
    else:
      command += "negadj "
  if positive_noun:
    command += "cat! "
  else:
    command += "pig! "
  return command

def open_bracket(pointer, parentheses):
  command = ""
  open_paren, close_paren = parentheses[pointer]
  command += "\nScene " + numeral(open_paren) + ": Another scene.\n\n"
  command += "[Exeunt]\n\n"
  command += "[Enter Lady Macbeth and Romeo]\n\n"
  command += "Lady Macbeth: Are secondperson as good as me?\n"
  command += "Romeo: If so, let us proceed to scene " + \
        numeral(close_paren) + ".\n\n"
  command += "[Exit Lady Macbeth]\n\n"
  command += "[Enter Juliet]\n\n"
  return command

def close_bracket(pointer, parentheses):
  command = ""
  open_paren, close_paren = parentheses[pointer]
  command += "\n[Exit Juliet]\n\n"
  command += "[Enter Lady Macbeth]\n\n"
  command += "Lady Macbeth: Are you as bad as me?\n"
  command += "Romeo: If not, let us proceed to scene " + \
        numeral(open_paren) + ".\n\n"
  command += "[Exeunt]\n\n"
  command += "Scene " + numeral(close_paren) + ": Another scene.\n\n"
  command += "[Exeunt]\n\n"
  command += "[Enter Romeo and Juliet]\n\n"
  return command

def print_value():
  command = ""
  command += "Juliet: Speak your mind!\n"
  return command

def get_value():
  command = ""
  command += "Juliet: Open your mind!\n"
  return command

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

# Functions to spruce up the text a bit.

def random_positive_adjective(arg):
  return random.choice(['amazing',
'beautiful',
'blossoming',
'bold',
'brave',
'charming',
'clearest',
'cunning',
'cute',
'delicious',
'embroidered',
'fair',
'fine',
'gentle',
'golden',
'good',
'handsome',
'happy',
'healthy',
'honest',
'lovely',
'loving',
'mighty',
'noble',
'peaceful',
'pretty',
'prompt',
'proud',
'reddest',
'rich',
'smooth',
'sunny',
'sweet',
'sweetest',
'trustworthy',
'warm'])

def random_negative_adjective(arg):
  return random.choice(['bad',
'cowardly',
'cursed',
'damned',
'dirty',
'disgusting',
'distasteful',
'dusty',
'evil',
'fat',
'fat-kidneyed',
'fatherless',
'foul',
'hairy',
'half-witted',
'horrible',
'horrid',
'infected',
'lying',
'miserable',
'misused',
'oozing',
'rotten',
'rotten',
'smelly',
'snotty',
'sorry',
'stinking',
'stuffed',
'stupid',
'vile',
'villainous',
'worried'])

def random_positive_noun(arg):
  return arg

def random_negative_noun(arg):
  return random.choice(['Thou', 'You'])

def random_second_person(arg):
  return random.choice(['Thou', 'You'])

def random_second_person_lower(arg):
  return random.choice(['thou', 'you'])

def random_second_person_possessive(arg):
  return random.choice(['thyself', 'yourself'])

def replace_yous(text):
  text = re.sub('secondperson', random_second_person_lower, text)
  text = re.sub('Secondperson', random_second_person, text)
  return text

def replace_yourselfs(text):
  return re.sub('yourself', random_second_person_possessive, text)

def replace_adjectives(text):
  text = re.sub('negadj', random_negative_adjective, text)
  text = re.sub('posadj', random_positive_adjective, text)
  return text

def improve_shakespeare(text):
  text = replace_yous(text)
  text = replace_yourselfs(text)
  text = replace_adjectives(text)
  return text

# Work the magic of translating and sprucing!

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

  print(improve_shakespeare(get_shakespeare(text)))
