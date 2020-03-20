eng_words_to_translate = []

with open('en_100.txt', 'r') as f:
    for line_with_word in f:
        line_with_word = line_with_word.split()
        if len(line_with_word) == 2:
            word, frequency = line_with_word[0], int(line_with_word[1])
            if word.isalpha():
                eng_words_to_translate.append(word)


if __name__ == "__main__":
    print(f'This list contains {len(eng_words_to_translate)} popular English words.')
    print(eng_words_to_translate)
