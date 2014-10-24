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
      if sums[sums_pointer] != 0:
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

  # Early fancy-ification
  shakespeare = re.sub("[\.!]", random_sentence_end, shakespeare)

  return shakespeare

def get_shakespeare(text):
  shakespeare = ""
  parentheses = {}
  shakespeare += "The Interpreted Brainfuck.\n\n"
  shakespeare += "Romeo, a stack that represents the present and past.\n"
  shakespeare += "Juliet, a stack that represents the future.\n"
  shakespeare += "Lady Macbeth, a zero that is only good for comparison.\n"
  shakespeare += "Macduff, who keeps track of our future.\n\n"
  shakespeare += "Act I: Our main performance.\n\n"
  shakespeare += "Scene I: It begins here.\n\n"
  shakespeare += "[Enter Romeo and Juliet]\n\n"
  shakespeare += bf_to_shakespeare(text)
  shakespeare += "\n[Exeunt]\n"
  return shakespeare

def decrement_stack_count():
  command = ""
  command += "[Exit Romeo]\n"
  command += "[Enter Macduff]\n"
  command += "Juliet: Are secondperson as posadj as nothing?\n"
  command += "Macduff: If so, remember nothing. Am I as posadj as nothing?\n"
  command += "Juliet: If not, secondperson are as negadj as the sum of yourself and a negnoun!\n"
  command += "[Exit Macduff]\n"
  command += "[Enter Romeo]\n"
  return command

def increment_stack_count():
  command = ""
  command += "[Exit Romeo]\n"
  command += "[Enter Macduff]\n"
  command += "Juliet: Secondperson are as posadj as the sum of thyself and a cat!\n"
  command += "[Exit Macduff]\n"
  command += "[Enter Romeo]\n"
  return command

def forward_pointer():
  command = decrement_stack_count()
  command += "Juliet: Remember yourself!\n"
  command += "Romeo: Recall recalltext\n"
  command += "Juliet: Secondperson are as posadj as me.\n"
  return command

def backward_pointer():
  command = increment_stack_count()
  command += "Romeo: Secondperson are as posadj as me! Remember yourself.\n"
  command += "Juliet: Recall recalltext\n"
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
  adjective = "posadj" if positive_noun else "negadj"
  operator = "sum of " if positive_sum else "difference between "
  command = "Secondperson are as " + adjective + " as the " + operator + \
"yourself and a "
  for x in range(power):
    if positive_noun:
      command += "posadj "
    else:
      command += "negadj "
  if positive_noun:
    command += "posnoun! "
  else:
    command += "negnoun! "
  return command

def open_bracket(pointer, parentheses):
  command = ""
  open_paren, close_paren = parentheses[pointer]
  command += "\nScene " + numeral(open_paren) + ": scenename\n\n"
  command += "[Exeunt]\n\n"
  command += "[Enter Lady Macbeth and Romeo]\n\n"
  command += "Lady Macbeth: Are secondperson as posadj as me?\n"
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
  command += "Lady Macbeth: Are secondperson as negadj as me?\n"
  command += "Romeo: If not, let us proceed to scene " + \
        numeral(open_paren) + ".\n\n"
  command += "[Exeunt]\n\n"
  command += "Scene " + numeral(close_paren) + ": scenename\n\n"
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
def random_scene_name(arg):
  scene_name = random.choice(['A posadj posnoun',
                              'A posadj negnoun',
                              'A negadj posnoun',
                              'A negadj negnoun'])
  return scene_name + "."

def random_recall_text(arg):
  recall_text = random.choice(['the posadj question, and whether it is to be or not to be.',
                              'the posadj negnoun in the mind\'s eye.',
                              'the negadj madness and the method in it.',
                              'the negadj negnoun on the negadj winter of our discontent.'])
  return recall_text

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
  return random.choice(['Heaven',
'King',
'Lord',
'angel',
'flower',
'happiness',
'joy',
'plum',
'summer\'s day',
'hero',
'rose',
'kingdom',
'pony'])

def random_negative_noun(arg):
  return random.choice(['Hell',
'Microsoft',
'bastard',
'beggar',
'blister',
'codpiece',
'coward',
'curse',
'death',
'devil',
'draught',
'famine',
'flirt-gill',
'goat',
'hate',
'hog',
'hound',
'leech',
'lie',
'pig',
'plague',
'starvation',
'toad',
'war',
'wolf'])

def random_positive_comparative(arg):
  return random.choice(['better'
'bigger',
'fresher',
'friendlier',
'nicer',
'jollier'
])

def random_negative_comparative(arg):
  return random.choice(['punier',
'smaller',
'worse'])

def random_second_person(arg):
  return random.choice(['Thou', 'You'])

def random_second_person_lower(arg):
  return random.choice(['thou', 'you'])

def random_second_person_possessive(arg):
  return random.choice(['thyself', 'yourself'])

def random_sentence_end(arg):
  return random.choice(['.',
'!'])

def random_character():
  character = random.choice(random_character.characters)
  random_character.characters.remove(character)
  return character

def replace_scene_names(text):
  text = re.sub('scenename', random_scene_name, text)
  return text

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

def replace_comparatives(text):
  text = re.sub('negcomp', random_negative_comparative, text)
  text = re.sub('poscomp', random_positive_comparative, text)
  return text

def replace_nouns(text):
  text = re.sub('negnoun', random_negative_noun, text)
  text = re.sub('posnoun', random_positive_noun, text)
  return text

def replace_recall_text(text):
  text = re.sub('recalltext', random_recall_text, text)
  return text

def fix_grammar(text):
  text = re.sub('A ([aeiou])', r'An \1', text)
  text = re.sub('a ([aeiou])', r'an \1', text)
  return text

def collapse_juliet_lines(text):
  lines = text.split('\n')
  result = []
  for idx, line in enumerate(lines):
    if (idx + 1) < len(text):
      # Pull together all Juiliet lines after this one if it's the first
      if line.startswith("Juliet:") and not lines[idx-1].startswith("Juliet:"):
        result_line = line
        checked_line = idx + 1
        while lines[checked_line].startswith("Juliet:"):
          result_line += " " + lines[checked_line][8:]
          checked_line += 1
        result.append(result_line)
      # As long as the current line isn't a Juliet line, we can keep it
      elif not line.startswith("Juliet:"):
        result.append(line)
    else:
      result.append(line)
  text = '\n'.join(result)
  return text

def replace_characters(text):
  romeo_replace = random_character()
  text = re.sub("Romeo", romeo_replace, text)
  juliet_replace = random_character()
  text = re.sub("Juliet", juliet_replace, text)
  macbeth_replace = random_character()
  text = re.sub("Lady Macbeth", macbeth_replace, text)
  macduff_replace = random_character()
  text = re.sub("Macduff", macduff_replace, text)
  return text

def improve_shakespeare(text):
  # Replace scene names + recall text first because the other replacements
  # will improve them further
  text = replace_scene_names(text)
  text = replace_recall_text(text)

  text = replace_yous(text)
  text = replace_yourselfs(text)
  text = replace_comparatives(text)
  text = replace_adjectives(text)
  text = replace_nouns(text)
  text = fix_grammar(text)
  text = collapse_juliet_lines(text)
  text = replace_characters(text)
  return text

# Work the magic of translating and sprucing!

if __name__ == "__main__":
  random_character.characters = ['Achilles',
'Adonis',
'Adriana',
'Aegeon',
'Aemilia',
'Agamemnon',
'Agrippa',
'Ajax',
'Alonso',
'Andromache',
'Angelo',
'Antiochus',
'Antonio',
'Arthur',
'Autolycus',
'Balthazar',
'Banquo',
'Beatrice',
'Benedick',
'Benvolio',
'Bianca',
'Brabantio',
'Brutus',
'Capulet',
'Cassandra',
'Cassius',
'Christopher Sly',
'Cicero',
'Claudio',
'Claudius',
'Cleopatra',
'Cordelia',
'Cornelius',
'Cressida',
'Cymberline',
'Demetrius',
'Desdemona',
'Dionyza',
'Doctor Caius',
'Dogberry',
'Don John',
'Don Pedro',
'Donalbain',
'Dorcas',
'Duncan',
'Egeus',
'Emilia',
'Escalus',
'Falstaff',
'Fenton',
'Ferdinand',
'Ford',
'Fortinbras',
'Francisca',
'Friar John',
'Friar Laurence',
'Gertrude',
'Goneril',
'Hamlet',
'Hecate',
'Hector',
'Helen',
'Helena',
'Hermia',
'Hermonie',
'Hippolyta',
'Horatio',
'Imogen',
'Isabella',
'John of Gaunt',
'John of Lancaster',
'Julia',
'Juliet',
'Julius Caesar',
'King Henry',
'King John',
'King Lear',
'King Richard',
'Lady Capulet',
'Lady Macbeth',
'Lady Macduff',
'Lady Montague',
'Lennox',
'Leonato',
'Luciana',
'Lucio',
'Lychorida',
'Lysander',
'Macbeth',
'Macduff',
'Malcolm',
'Mariana',
'Mark Antony',
'Mercutio',
'Miranda',
'Mistress Ford',
'Mistress Overdone',
'Mistress Page',
'Montague',
'Mopsa',
'Oberon',
'Octavia',
'Octavius Caesar',
'Olivia',
'Ophelia',
'Orlando',
'Orsino',
'Othello',
'Page',
'Pantino',
'Paris',
'Pericles',
'Pinch',
'Polonius',
'Pompeius',
'Portia',
'Priam',
'Prince Henry',
'Prospero',
'Proteus',
'Publius',
'Puck',
'Queen Elinor',
'Regan',
'Robin',
'Romeo',
'Rosalind',
'Sebastian',
'Shallow',
'Shylock',
'Slender',
'Solinus',
'Stephano',
'Thaisa',
'The Abbot of Westminster',
'The Apothecary',
'The Archbishop of Canterbury',
'The Duke of Milan',
'The Duke of Venice',
'The Ghost',
'Theseus',
'Thurio',
'Timon',
'Titania',
'Titus',
'Troilus',
'Tybalt',
'Ulysses',
'Valentine',
'Venus',
'Vincentio',
'Viola']

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
