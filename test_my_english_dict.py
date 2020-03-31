from my_english_dict import webapp_engdict_insert


def test_no_user():
    right_answer = 'Вы не ввели имя пользователя.'
    assert webapp_engdict_insert('word', None) == right_answer


def test_no_word():
    right_answer = 'Вы не ввели слово.'
    assert webapp_engdict_insert(None, 'user') == right_answer


def test_no_user_no_word():
    right_answer = 'Вы не ввели слово и имя пользователя.'
    assert webapp_engdict_insert(None, None) == right_answer


def test_nonexistent_user():
    user = 'nonexistent'
    right_answer = f'Пользователь {user} не зарегистрирован на сайте.'
    assert webapp_engdict_insert('word', user) == right_answer


def test_word_already_in_your_dict():
    user, word, translation = 'earlinn', 'cloud', 'облако'
    right_answer = f'Слово "{word}" уже есть в вашем словаре, перевод: {translation}.'
    assert webapp_engdict_insert(word, user) == right_answer


def test_word_in_common_dict_translation_agree():
    user, word, translation = 'earlinn', 'here', 'здесь'
    right_answer = f'Слово "{word}" добавлено в ваш словарь, перевод: {translation}.'
    assert webapp_engdict_insert(word, user) == right_answer
