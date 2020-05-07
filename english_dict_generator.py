import re
from translate import Translator

from open_eng_textfile import eng_words_to_translate
from webapp.dictionary.models import EnglishWord
from webapp import create_app

translator = Translator(to_lang="ru")  # always translate into Russian
app = create_app()


def eng_dict_generator():
    english_list = eng_words_to_translate

    russian_list = []

    english_dict = {}
    for word in english_list:
        with app.app_context():
            word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).count()
            try:
                if not word_exist:
                    try:
                        translated = translator.translate(word)
                        # then we check that the translation consists of words, not icons and numbers
                        # for example, translation type  {'is': '-'} will be considered incorrect
                        letters_and_hyphens_in_translated = re.findall('[а-яА-Я-]+', translated)
                        not_only_hyphens_in_translated = re.findall('[а-яА-Я]+', translated)
                        if letters_and_hyphens_in_translated and not_only_hyphens_in_translated:
                            translated_result = ' '.join(letters_and_hyphens_in_translated)
                            english_dict[word] = translated_result.lower()
                            russian_list.append(translated_result.lower())
                        else:
                            raise ValueError
                    except ValueError:
                        print(f'Bad translation for the word "{word}" - "{translated}" ')
                else:
                    raise ValueError
            except ValueError:
                print(f'    The word "{word}" is already in the database.')

    return english_dict


if __name__ == '__main__':
    print(eng_dict_generator())
