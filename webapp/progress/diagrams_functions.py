import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import locale
import platform

from webapp.dictionary.dict_functions import process_user_engdict_index
from webapp.user.models import User

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


def engword_dataframe(username):
    username = User.query.filter_by(username=username).first_or_404()
    userdict = process_user_engdict_index(username)
    if userdict:
        first_date = userdict[-1][2]
        today = datetime.now()
        delta = today - first_date
        add_data = {
            'дни': [],
            'добавленные слова за день': [],
            'добавленные слова': [],
            'изученные слова за день': [],
            'изученные слова': []
            }
        for day in range(delta.days + 2):
            next_day = first_date + timedelta(days=day)
            date = next_day.strftime('%d.%m.%Y')
            add_data['дни'].append(next_day)
            words_der_day, familiar_words_per_day = 0, 0
            for word in userdict:
                if word[2].strftime('%d.%m.%Y') == date:
                    words_der_day += 1
                if word[4]:
                    if word[4].strftime('%d.%m.%Y') == date:
                        familiar_words_per_day += 1
            add_data['добавленные слова за день'].append(words_der_day)
            accumulated_words_added = sum(add_data['добавленные слова за день'])
            add_data['добавленные слова'].append(accumulated_words_added)
            add_data['изученные слова за день'].append(familiar_words_per_day)
            accumulated_familiar_words_per_day = sum(add_data['изученные слова за день'])
            add_data['изученные слова'].append(accumulated_familiar_words_per_day)
        return(add_data)
    return {}


def new_engwords_accumulated(username):
    sns.set(style="ticks", palette="colorblind", font="Arial")
    df_dict = engword_dataframe(username)
    if df_dict:
        df = pd.DataFrame(df_dict)
        new_engwords_accumulation = sns.relplot(
            x="дни",
            y="добавленные слова",
            kind="line",
            data=df,
            height=6,
            aspect=1
            )
        new_engwords_accumulation.fig.autofmt_xdate()
        new_engwords_accumulation.set_xticklabels(rotation=90, horizontalalignment='center')
        plt.savefig(f'webapp/static/progress/new_engwords_{username}.png')
        return f'progress/new_engwords_{username}.png'
    return None


def familiar_engwords_accumulated(username):
    sns.set(style="ticks", palette="colorblind", font="Arial")
    df_dict = engword_dataframe(username)
    if df_dict:
        if sum(df_dict['изученные слова']):
            df = pd.DataFrame(df_dict)
            familiar_engwords_accumulation = sns.relplot(
                x="дни",
                y="изученные слова",
                kind="line",
                data=df,
                height=6,
                aspect=1
                )
            familiar_engwords_accumulation.fig.autofmt_xdate()
            familiar_engwords_accumulation.set_xticklabels(rotation=90, horizontalalignment='center')
            plt.savefig(f'webapp/static/progress/familiar_engwords_{username}.png')
            return f'progress/familiar_engwords_{username}.png'
        return None
    return None


def difficult_engwords_catplot(username):
    username = User.query.filter_by(username=username).first_or_404()
    userdict = process_user_engdict_index(username)
    failure_dict = {'слова': [], 'неудачные попытки': []}
    if userdict:
        for word in userdict:
            failures = 0
            # убрать повторения, рефакторинг
            if word[5]:
                failures += word[5]
            if word[6]:
                failures += word[6]
            if word[7]:
                failures += word[7]
            if word[8]:
                failures += word[8]
            if word[9]:
                failures += word[9]
            if failures:
                failure_dict['слова'].append(word[0].word_itself)
                failure_dict['неудачные попытки'].append(failures)
        df = pd.DataFrame(failure_dict)
        df = df.sort_values('неудачные попытки')
        df = df.tail(20)
        # когда слов станет много, надо будет выводить не все, а, например, первые 20
        sns.set(style="ticks", palette="colorblind", font="Arial")
        difficult_engwords = sns.catplot(
                x="слова",
                y="неудачные попытки",
                kind="bar",
                data=df,
                height=6,
                aspect=1
                )
        difficult_engwords.fig.autofmt_xdate()
        difficult_engwords.set_xticklabels(rotation=90, horizontalalignment='center')
        plt.savefig(f'webapp/static/progress/difficult_engwords_{username.username}.png')
        return f'progress/difficult_engwords_{username.username}.png'
    return None
