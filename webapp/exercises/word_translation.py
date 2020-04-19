from random import choice, randint
from english_dict_generator import eng_dict_generator

def game(user_answer):

    # making initial dictionary
    english_dict = eng_dict_generator()
    english_list = [key for key in english_dict]
    russian_list = [english_dict[key] for key in english_dict]

    # choosing 10 word from the dictionary for a game
    play_set = set()
    while len(play_set) < 10:
        play_set.add(choice(english_list))
    list_to_play = list(play_set)

    # the game itself
    for word in list_to_play:
        right_answer = english_dict[word]
        
        # getting 4 possible translations into russian
        answers = set()
        answers.add(right_answer)
        while len(answers) < 4:
            answers.add(choice(russian_list))
        answers_list = list(enumerate(answers))
        answers = {}
        for element in answers_list:
            answers[element[0] + 1] = element[1]

        # printing a word in english
        print('\n' + word)

        # printing its possible translations into russian
        for prompt in answers:
            print(f'{prompt}: {answers[prompt]}')
        print()

        # asking a user to guess the correct translation, then showing the correct translation
        try:
            user_answer = int(input('Чтобы выбрать ответ, введите целое число от 1 до 4: '))
            if user_answer not in [1, 2, 3, 4]:
                raise ValueError
            if english_dict[word] == answers[user_answer]:
                print('Верно :)')
            else:
                print(f'Неверно :( Правильный ответ - {english_dict[word]}.')
        except ValueError:
            print('Это не целое число от 1 до 4')
            print()


if __name__ == '__main__':
    start_a_game = input('Чтобы начать игру, введите любой текст: ')
    game(start_a_game)
