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
    first_date = userdict[-1][2]
    today = datetime.now()
    delta = today - first_date
    add_data = {'дни': [], 'добавленные слова за день': [], 'добавленные слова': []}
    for day in range(delta.days + 2):
        next_day = first_date + timedelta(days=day)
        date = next_day.strftime('%d.%m.%Y')
        add_data['дни'].append(date)
        words_der_day = 0
        for word in userdict:
            if word[2].strftime('%d.%m.%Y') == date:
                words_der_day += 1
        add_data['добавленные слова за день'].append(words_der_day)
        accumulated_words_added = sum(add_data['добавленные слова за день'])
        add_data['добавленные слова'].append(accumulated_words_added)
    return(add_data)


def new_engwords_accumulated(username):
    sns.set(style="ticks", palette="colorblind", font="Arial")
    df = pd.DataFrame(engword_dataframe(username))
    new_engwords_accumulation = sns.relplot(
        x="дни",
        y="добавленные слова",
        kind="line",
        data=df,
        height=6,
        aspect=1
        )
    new_engwords_accumulation.fig.autofmt_xdate()
    new_engwords_accumulation.set_xticklabels(rotation=90, horizontalalignment='right')
    plt.savefig('webapp/media/progress/new_engwords_accumulated.png')
