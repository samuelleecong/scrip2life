import os
import cohere
import json
import re

# Initialize the Cohere SDK
COHERE_API_KEY = os.environ['COHERE_API_KEY']
co = cohere.Client(COHERE_API_KEY)

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
      #entity, content = line.split(': ')
      #if entity in characters:
      #  lines[entity] += [content[0].replace('"', "'")]
      if line.startswith(character):
        line = line.split(': ')[1].replace('"', "'")
        lines[character].append(line)

  print(lines)

  return lines


def get_character_traits(character_lines, characters):
  '''
  Takes a list containing all the lines of the characters in the script
  and returns a dictionary containing the back stories for the characters
  in the characters list

  args:\n
  character_lines - (list) list containing the dialogue\n
  characters - list of characters
  '''
  #character_lines = get_character_lines(script, characters)
  character_story = {}

  for character in characters:
    if len(character_lines[character]
           ) > 3:  # filter for characters with a considerable number of lines
      print(f"Get character traits {character}")
      prompt = f"Generate a succinct summary of the character {character}, summarizing the character traits of {character} based on their lines and interactions with other characters in the following dialogue:{character_lines[character]}\n\nCharacter traits in a paragraph:"

      response = co.generate(model='command-xlarge-20221108',
                             prompt=prompt,
                             max_tokens=60,
                             temperature=0.2,
                             k=0,
                             p=0.65,
                             frequency_penalty=0.3,
                             presence_penalty=0.5,
                             stop_sequences=[],
                             return_likelihoods='NONE')
      traits = response.generations[0].text
      # Take only output up to the last period
      traits = re.sub(r"\.[^\.]*$", ". ", traits)
      
      character_story[character] = traits

  return character_story


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
    # filter for characters with a considerable number of lines
    if len(character_lines[character]) > 3:
      prompt = f"Generate succinct history and background of a character {character} in a movie, based on their lines in the script for the movie:\n\n {character_lines[character]}\n\nBackground:"

      print(f"Get character backstory {character}")
      print(f"prompt len: for {character}: {len(prompt)}")
      #print(f'{character}: {len(character_lines[character])} lines')
      response = co.generate(model='command-xlarge-20221108',
                             prompt=prompt,
                             max_tokens=60,
                             temperature=0.5,
                             k=0,
                             p=0.65,
                             frequency_penalty=0.3,
                             presence_penalty=0.5,
                             stop_sequences=[],
                             truncate='end',
                             return_likelihoods='NONE')
      background = response.generations[0].text
      # Take only output up to the last period
      background = re.sub(r"\.[^\.]*$", ". ", background)
      
      back_story[character] = background

  return back_story


# def get_character_back_story_old(character_lines, characters):
#   '''
#   Takes a list containing all the lines of the characters in the script
#   and returns a dictionary containing the back stories for the characters
#   in the characters list

#   args:\n
#   script - list containing the dialogue\n
#   characters - list of characters
#   '''
#   back_story = {}
#   for character in characters:
#     print(f"Get character backstory {character}")
#     response = co.generate(
#       model='command-xlarge-20221108',
#       prompt=
#       f"Concisely explain the childhood of a character {character} that talks like this: {character_lines[character]}",
#       max_tokens=300,
#       temperature=0.5,
#       k=0,
#       p=0.75,
#       frequency_penalty=0,
#       presence_penalty=0,
#       stop_sequences=[],
#       truncate='end',
#       return_likelihoods='NONE')

#     back_story[character] = response.generations[0].text
#   print(back_story)
#   return back_story

# def get_script_summary(script):
#  '''
#  Takes a list containing all the lines of the characters in the script
#  and returns the summary.

#  args:\n
#  script - list containing the script
#  '''
#   # Set max tokens
#   max_tokens = 320

#   # Define the prompt for the summary
#   script_string = "\n".join(script)

#   # Set maximum tokens
#   max_tokens = 320

#   # check if the prompt exceeds the maximum number of tokens

#   # max tokens is 4097 tokens

#   if len(script_string.split()) > max_tokens:
#     # Split the prompt into words
#     words = script_string.split()

#     truncated_prompt_start = words[:max_tokens - 20]

#   # Generate the summary using the OpenAI API
#   prompt = "Generate a succint summary of the following movie script:\n\n"
#   for line in truncated_prompt_start:
#     prompt += line
#   model_engine = "text-davinci-002"
#   print("Get summary from OpenAI")
#   completions = openai.Completion.create(
#     engine=model_engine,
#     prompt=prompt,
#     max_tokens=max_tokens,
#     n=1,
#     stop=None,
#     temperature=0.5,
#   )

#   return completions.choices[0].text


def get_summary_chunk_list(script):
  '''
  Splits the script into chunks that meet the maximum token size

  Args:
  script - (list) list containing the dialogue of the movie

  returns:
  list
  '''
  # Define the prompt for the summary
  script_string = ""
  chunk_prompt = ""
  chunk_list = []
  pre_prompt = "Generate a succinct summary of the scene, summarizing the main points of conversation and character interactions in the following dialogue:\n\n"
  post_prompt = "Summary:"

  # Set max tokens
  max_tokens = 2048

  while len(script) >= 1:
    while len(script_string) < max_tokens - len(pre_prompt.split()) - len(
        post_prompt.split()):
      try:
        script_string += script[0] + '\n'
        script.pop(0)
      except IndexError:
        break

    chunk_prompt = pre_prompt + script_string + post_prompt
    chunk_list.append(chunk_prompt)
    script_string = ""
  return chunk_list


# Summarize the script
def get_chunk_summary(prompt, model='command-xlarge-20221108'):
  '''
  Takes in a prompt and model and returns the result of the prompt as a string

  args:
  prompt - (string) The instruction to summarize the model
  model - (string) The cohere model to be used. Defaults to 'command-xlarge-20221108'
  '''
  response = co.generate(model=model,
                         prompt=prompt,
                         max_tokens=60,
                         temperature=0.5,
                         k=0,
                         p=0.75,
                         frequency_penalty=0,
                         presence_penalty=0,
                         stop_sequences=[],
                         return_likelihoods='ALL',
                         truncate='END')

  return response.generations[0].text

def get_script_summary(script):
  '''
  Generates and combines the summaries for each chunk into a single paragraph
  '''
  chunk_list = get_summary_chunk_list(script)
  print(len(chunk_list))
  script_summary = ""
  for prompt in chunk_list:
    chunk_summary = get_chunk_summary(prompt)
    chunk_summary = re.sub(r"\.[^\.]*$", ". ", chunk_summary)
    chunk_summary = re.sub(r'\n', '', chunk_summary)
    script_summary += chunk_summary

  return script_summary