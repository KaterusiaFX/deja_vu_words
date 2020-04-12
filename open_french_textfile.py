french_words_to_translate = []

with open('fr.txt', 'r') as f:
    for line_with_word in f:
        line_with_word = line_with_word.split()
        if len(line_with_word) == 2:
            word, frequency = line_with_word[0], int(line_with_word[1])
            if word.isalpha():
                french_words_to_translate.append(word)


if __name__ == "__main__":
    print(f'This list contains {len(french_words_to_translate)} popular French words.')
    print(french_words_to_translate)
