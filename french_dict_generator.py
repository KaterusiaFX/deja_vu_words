import re

from translate import Translator
from open_french_textfile import french_words_to_translate
from webapp.dictionary.models import FrenchWord
from webapp import create_app

translator = Translator(from_lang='fr', to_lang='ru')
app = create_app()


def french_dict_generator():
    french_list = french_words_to_translate

    russian_list = []

    french_dict = {}
    for word in french_list:
        with app.app_context():
            word_exist = FrenchWord.query.filter(FrenchWord.word_itself == word).count()
            try:
                if not word_exist:
                    try:
                        translated = translator.translate(word)
                        # check if the translation consists of words without figures and typographical symbols
                        # example: translation {'is': '-'} is wrong
                        letters_and_hyphens_in_translated = re.findall('[а-яА-Я-]+', translated)
                        not_only_hyphens_in_translated = re.findall('[а-яА-Я]+', translated)
                        if letters_and_hyphens_in_translated and not_only_hyphens_in_translated:
                            translated_result = ' '.join(letters_and_hyphens_in_translated)
                            french_dict[word] = translated_result.lower()
                            russian_list.append(translated_result.lower())
                        else:
                            raise ValueError
                    except ValueError:
                        print(f'Bad translation for the word "{word}" - "{translated}" ')
                else:
                    raise ValueError
            except ValueError:
                print(f'    The word "{word}" is already in the database.')

    return french_dict


if __name__ == '__main__':
    print(french_dict_generator())