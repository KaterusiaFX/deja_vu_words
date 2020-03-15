eng_words_to_translate = []

with open('en_100.txt', 'r') as f:
    for line in f:
        line = line.split()
        if len(line) == 2:
            word, frequency = line[0], int(line[1])
            if word.isalpha():
                eng_words_to_translate.append(word)


if __name__ == "__main__":
    print(f'This list contains {len(eng_words_to_translate)} popular English words.')
    print(eng_words_to_translate)
