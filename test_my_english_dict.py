# пример тестового файла, удалить в будущем

from my_english_dict import webapp_engdict_insert


def test_no_user():
    """Не введено имя пользователя"""
    right_answer = 'Вы не ввели имя пользователя.'
    assert webapp_engdict_insert('word', None) == right_answer


def test_no_word():
    """Не введено слово"""
    right_answer = 'Вы не ввели слово.'
    assert webapp_engdict_insert(None, 'user') == right_answer


def test_no_user_no_word():
    """Не введено имя пользователя и слово"""
    right_answer = 'Вы не ввели слово и имя пользователя.'
    assert webapp_engdict_insert(None, None) == right_answer


def test_nonexistent_user():
    """Введено имя несуществующего пользователя"""
    user = 'nonexistent'
    right_answer = f'Пользователь {user} не зарегистрирован на сайте.'
    assert webapp_engdict_insert('word', user) == right_answer


def test_word_already_in_your_dict():
    """Введено слово, которое уже есть у этого пользователя в его персональном словаре"""
    user, word, translation = 'earlinn', 'cloud', 'облако'
    right_answer = f'Слово "{word}" уже есть в вашем словаре, перевод: {translation}.'
    assert webapp_engdict_insert(word, user) == right_answer


def test_word_in_common_dict_translation_agree():
    """Слова нет в персональном словаре пользователя,
    но оно есть в общем словаре, и он согласен с предложенным переводом,
    (надо ответить N)"""
    user, word, translation = 'earlinn', 'here', 'здесь'
    right_answer = f'Слово "{word}" добавлено в ваш словарь, перевод: {translation}.'
    assert webapp_engdict_insert(word, user) == right_answer


def test_word_in_common_dict_translation_disagree_admin():
    """Слова нет в персональном словаре пользователя,
    но оно есть в общем словаре, но он согласен с предложенным переводом,
    (надо ответить Y) и он админ, слово заменяется в общем словаре
    (надо ответить: иметь возможность)"""
    user, word = 'earlinn', 'can'
    right_answer = f'Слово "{word}" добавлено в ваш словарь, перевод: иметь возможность.'
    assert webapp_engdict_insert(word, user) == right_answer
