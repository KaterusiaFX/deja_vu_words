from open_text_file import eng_words_to_translate
from webapp.model import Words
from webapp import create_app

from translate import Translator
translator= Translator(to_lang="ru") # переводим всегда на русский

app = create_app()

def eng_dict_generator():
    english_list = eng_words_to_translate

    russian_list = []

    english_dict = {}
    for word in english_list:
        with app.app_context():
            word_exist = Words.query.filter(Words.word_itself == word).count()
            try:
                if word_exist == 0:
                    try:
                        translated = translator.translate(word)
                        # далее проверяем, что перевод состоит из слов, а не значков и цифр
                        # например, перевод типа {'is': '-'} будет считаться неверным
                        # переводы типа {'your': 'твой.'} тоже будут считаться неверными из-за значка в конце
                        translated_bool = filter(lambda x: x.isalpha(), translated.split())
                        if any(translated_bool): 
                            english_dict[word] = translated.lower()
                            russian_list.append(translated.lower())
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
