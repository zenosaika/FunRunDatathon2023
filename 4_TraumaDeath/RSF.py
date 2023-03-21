import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline 

# from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sksurv.ensemble import RandomSurvivalForest

# set_config(display='text')

X, y = load_gbsg2()

# X.loc[:, "tgrade"].values -> select column 'tgrade' then get its values
# [:, np.newaxis] -> convert it to column vector (m, )
grade_str = X.loc[:, "tgrade"].values[:, np.newaxis]

grade_num = OrdinalEncoder(categories=[["I", "II", "III"]]).fit_transform(grade_str)

X_no_grade = X.drop("tgrade", axis=1)
Xt = OneHotEncoder().fit_transform(X_no_grade)
Xt.loc[:, "tgrade"] = grade_num # add new column

X_train, X_test, y_train, y_test = train_test_split(Xt, y, test_size=0.25)

rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           )

rsf.fit(X_train, y_train)
print(f'RSF score: {rsf.score(X_test, y_test)}')


X_test_sorted = X_test.sort_values(by=['pnodes', 'age'])
X_test_sel = pd.concat((X_test_sorted.head(3), X_test_sorted.tail(3)))

surv = rsf.predict_survival_function(X_test_sel, return_array=True)

for i, s in enumerate(surv):
    plt.step(rsf.event_times_, s, where='post', label=str(i))
plt.ylabel('Survival probability')
plt.xlabel('Time in days')
plt.legend()
plt.grid(True)
plt.show()
