import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
first date = None  # день добавления первого англ/фр слова в список new
# отсчитываем по 1 дню. Даты по оси х, по у - количество len() слов familiar
# результат складываем в словарь
df = pd.DataFrame(dict(time=np.arange(500),
                       value=np.random.randn(500).cumsum()))
g = sns.relplot(x="time", y="value", kind="line", data=df)
g.fig.autofmt_xdate()
plt.show()
