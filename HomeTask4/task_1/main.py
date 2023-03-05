
# Open file
file = open('aristotle.txt', 'r', encoding='utf-8-sig')

# Test read
text = file.read()
#print(text)
print(f'------> Symbols in text = {len(text)}')

# Spaces counter
spaces_counter = text.count(' ')
print(f'------> Symbols without spaces in text = {len(text) - spaces_counter}')

# Punctuation counter
punctuation_set = {'.', '?', '!', '...', ',', ';', ':', '-', '(', ')', '"'}
punctuation_counter = 0
for el in punctuation_set:
    punctuation_counter += text.count(el)

print(f'------> Symbols without punctuation = {len(text) - punctuation_counter}')

# Cleaning the text
character_map = {
    ord('\n'): ' ',
    ord('\t'): ' ',
    ord('\r'): None
}
replaced_text = text.translate(character_map)

# Words counter
words_list = replaced_text.split()
print(f'------> Words in text = {len(words_list)}')

# Sentence counter
start_sentence_flag = 0
sentence_counter = 0
for el in words_list:
    if el[0].isupper():
        start_sentence_flag = 1

    if start_sentence_flag and ((el[-1] == '.')
                                or (el[-1] == '?')
                                or (el[-1] == '!')):
        sentence_counter += 1
        start_sentence_flag = 0

print(f'------> Sentences in text = {sentence_counter}')

# Close file
file.close()

