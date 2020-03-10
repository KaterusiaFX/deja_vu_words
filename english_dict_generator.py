from googletrans import Translator
translator = Translator()


def eng_dict_generator():
    english_list = [
                    'cat',
                    'kitten',
                    'dog',
                    'duck',
                    'cow',
                    'puppy',
                    'goat',
                    'frog',
                    'chicken',
                    'bee',
                    'whale',
                    'insect',
                    'rabbit',
                    'beaver',
                    'camel',
                    'crocodile',
                    'dolphin',
                    'fox',
                    'gorilla',
                    'hamster'
    ]

    russian_list = []

    english_dict = {}
    for word in english_list:
        translated = translator.translate(word, dest='ru')
        english_dict[word] = translated.text.lower()
        russian_list.append(translated.text.lower())

    return english_dict

if __name__ == '__main__':
    print(eng_dict_generator())
