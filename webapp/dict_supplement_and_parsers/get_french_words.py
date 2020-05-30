from datetime import datetime
import re
from translate import Translator

from webapp.db import db
from webapp.dictionary.models import FrenchWord

translator = Translator(from_lang='fr', to_lang='ru')


def french_dict_generator():
    french_list = []
    with open('webapp/dict_supplement_and_parsers/fr.txt', 'r') as f:
        for line_with_word in f:
            line_with_word = line_with_word.split()
            if len(line_with_word) == 2:
                word = line_with_word[0]
                if word.isalpha():
                    french_list.append(word)
    russian_list = []
    french_dict = {}
    for word in french_list:
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


def save_frenchwords_in_db(words_dict):
    for word in words_dict:
        word_exist = FrenchWord.query.filter(FrenchWord.word_itself == word).count()
        if not word_exist:
            new_word = FrenchWord(
                word_itself=word,
                translation_rus=words_dict[word],
                imported_time=datetime.now()
                )
            db.session.add(new_word)
    db.session.commit()
