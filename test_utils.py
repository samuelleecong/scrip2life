import cohere
import openai
import json
import re

# Initialize the Cohere SDK

PLACEHOLDER_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sagittis felis eget eros porttitor, id blandit nulla interdum. Etiam ante tortor, posuere rhoncus ultricies dapibus, gravida eu ante. Donec condimentum semper nunc, eu lacinia massa tincidunt sed. Duis tempor ultricies quam, eget viverra tellus accumsan ut. Nam ut tortor sapien. Pellentesque sed semper augue. Pellentesque orci justo, maximus non lobortis a, eleifend vitae massa. Phasellus vel euismod orci. Quisque diam elit, pulvinar sit amet dui vel, varius sagittis libero. Donec non ullamcorper mauris, non fermentum urna."


def load_script(path):
  '''
    Takes a .txt file as input and returns the transcript

    Args:\n
    path - path to text file containing the movie script
    '''

  file = open(path).read()
  script_dict = json.loads(file)
  script = script_dict['Transcript']

  return script


def get_script_characters(script):
  '''
  Takes a list containing all the lines of the characters in the script
  and returns the set containing all the characters

  args:\n
  script - list containing the script
  '''
  characters = []

  # create a set of stop words to ensure non character names are not extracted
  stop_words = {'SCENE'}

  script = script

  for line in script:
    # Use regular expression to find all title case words followed by a
    ## colon in the script
    for word in re.findall(r'(\w+):', line):
      # Add word to the list if it is not a stop word
      if word.upper() not in stop_words:
        # Check that word is not already in the list
        if word not in characters:
          characters.append(word)
  return characters


def get_character_lines(script, characters):
  '''
    Takes a list containing all the lines of the characters in the script
    and returns a dictionary containing the lines for the characters in the
    characters list

    args:\n
    script - list conatining the dialogue\n
    characters - list of characters
    '''

  # initialize a dictionary with empty lists for each character
  lines = {}
  for character in characters:
    lines[character] = []

  for line in script:
    entity, *content = line.split(': ')
    if entity in characters:
      lines[character] += [content[0].replace('"', "'")]

  return lines


def get_character_traits(character_lines, characters):
  '''
    Takes a list containing all the lines of the characters in the script
    and returns a dictionary containing the traits for the characters in the
    characters list

    args:\n
    script - list conatining the dialogue\n
    characters - list of characters
    '''
  traits = {}
  for character in characters:
    print(f"Get character trait {character}")
    # response = co.generate(
    #   model='command-xlarge-20221108',
    #   prompt=
    #   f"Concisely explain the traits of a character that would say these lines: {character_lines[character]}",
    #   max_tokens=300,
    #   temperature=0.5,
    #   k=0,
    #   p=0.75,
    #   frequency_penalty=0,
    #   presence_penalty=0,
    #   stop_sequences=[],
    #   truncate='end',
    #   return_likelihoods='NONE')

    traits[character] = PLACEHOLDER_TEXT

  return traits


def get_character_back_story(character_lines, characters):
  '''
  Takes a list containing all the lines of the characters in the script
  and returns a dictionary containing the back stories for the characters
  in the characters list

  args:\n
  script - list containing the dialogue\n
  characters - list of characters
  '''
  back_story = {}
  for character in characters:
    print(f"Get character backstory {character}")
    # response = co.generate(
    #   model='command-xlarge-20221108',
    #   prompt=
    #   f"Concisely explain the childhood of a character {character} that talks like this: {character_lines[character]}",
    #   max_tokens=300,
    #   temperature=0.5,
    #   k=0,
    #   p=0.75,
    #   frequency_penalty=0,
    #   presence_penalty=0,
    #   stop_sequences=[],
    #   truncate='end',
    #   return_likelihoods='NONE')

    back_story[character] = PLACEHOLDER_TEXT

  return back_story


def get_script_summary(script):
  '''
  Takes a list containing all the lines of the characters in the script
  and returns the summary.

  args:\n
  script - list containing the script
  '''
  # Set max tokens
  max_tokens = 320

  # Define the prompt for the summary
  script_string = "\n".join(script)

  # Set maximum tokens
  max_tokens = 320

  # check if the prompt exceeds the maximum number of tokens

  # max tokens is 4097 tokens

  if len(script_string.split()) > max_tokens:
    # Split the prompt into words
    words = script_string.split()

    truncated_prompt_start = words[:max_tokens - 20]

  # Generate the summary using the OpenAI API
  prompt = "Generate a succint summary of the following movie script:\n\n"
  for line in truncated_prompt_start:
    prompt += line
  model_engine = "text-davinci-002"
  print("Get summary from OpenAI")
  # completions = openai.Completion.create(
  #   engine=model_engine,
  #   prompt=prompt,
  #   max_tokens=max_tokens,
  #   n=1,
  #   stop=None,
  #   temperature=0.5,
  # )

  return PLACEHOLDER_TEXT  # completions.choices[0].text
