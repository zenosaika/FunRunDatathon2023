import pymysql

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

from scipy.stats import uniform

import warnings
warnings.filterwarnings('ignore')

from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RandomizedSearchCV

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sksurv.ensemble import RandomSurvivalForest

###########################################################

conn = pymysql.connect(
    host = '172.29.70.66',
    port = 53308,
    user = 'group9',
    passwd = 'group9@54tMa!',
    db = 'datathon',
    charset = 'utf8mb4',
)

###########################################################

tables = [
    'Q4_vitalsign', 
    'Q4_blood_transfusion',
    'Q4_characteristics',
    'Q4_lab',
    'Q4_admit',
    'Q4_death',
    'Q4_blood_gas',
    'Q4_trauma_data',
]

mydb = {}

for table in tables:
    if table not in mydb:
        mydb[table] = pd.read_sql_query(f'SELECT * FROM {table}', conn)

###########################################################

db = mydb.copy()

###########################################################

for n, x in db.items():
    print(n, x.shape)
db['Q4_trauma_data']['id_an'].value_counts().unique()

###########################################################

db['Q4_trauma_data']['hosdcgos'].value_counts() # discharge status

###########################################################

data = db['Q4_trauma_data'][['id_an', 'hosdcgos']] # main dataframe

# clean data
data['hosdcgos'] = data['hosdcgos'].fillna(0).values.astype(object).astype('float')

###########################################################

data = db['Q4_trauma_data'][['id_an', 'hosdcgos']] # main dataframe

# clean data
data['hosdcgos'] = data['hosdcgos'].fillna(0).values.astype(object).astype('float')

###########################################################

### ISS
iss = db['Q4_trauma_data'][['id_an', 'iss']]

# clean data
iss['iss'].replace('n/a', 0, inplace=True)
iss['iss'].replace('N/A', 0, inplace=True)
iss['iss'].replace('ืn/a', 0, inplace=True)
iss['iss'] = iss['iss'].astype(int)

# merge data
data = data.merge(iss, on='id_an')

data

###########################################################

### Vital Sign
vitalsign = db['Q4_vitalsign']
cols = ['temp', 'pulse', 'resp', 'sbp', 'dbp']

# clean data
tmp = pd.DataFrame()

for c in cols:
    tmp[c] = pd.DataFrame(vitalsign.groupby('id_an')[c].apply(list))
    tmp[c] = tmp[c].apply(lambda x: [i for i in x if i==i]) # remove nan (nan == nan -> False)
    tmp[f'min_{c}'] = tmp[c].apply(lambda x: min(x) if x else 0)
    tmp[f'max_{c}'] = tmp[c].apply(lambda x: max(x) if x else 0)
    tmp[f'avg_{c}'] = tmp[c].apply(lambda x: np.average(x) if x else 0)

# merge data
data = data.merge(tmp.drop(cols, axis=1), left_on='id_an', right_on=tmp.index)

data

###########################################################

# age
birthdate = db['Q4_characteristics'][['id', 'bdate']]
admitdate = db['Q4_admit'][['id', 'id_an', 'adm_d']]

# clean data
admitdate['bdate'] = admitdate['id'].apply(lambda x: birthdate[birthdate['id']==x][['bdate']].values[0][0])
admitdate['adm_d'] = pd.to_datetime(admitdate['adm_d'], errors = 'coerce')
admitdate['bdate'] = pd.to_datetime(admitdate['bdate'], errors = 'coerce')
admitdate['age'] = (admitdate['adm_d'] - admitdate['bdate']) / pd.Timedelta(days=1) // 365

# merge data
data = data.merge(admitdate[['id_an', 'age']], on='id_an')

data

###########################################################

table = db['Q4_trauma_data']
cols = ['helmet', 'belt', 'drug', 'alc', 'mec', 'rtf', 'esi', 'prehos', 'precon', 'phone', 'arrgcse', 'arrgcsv', 'arrgcsm']

for c in cols:
    onehot = OneHotEncoder().fit_transform(pd.DataFrame(table[c]))
    tmp = pd.DataFrame(onehot.toarray(), columns=[f'{c}{i}' for i in range(1, onehot.shape[1]+1)])
    tmp['id_an'] = table['id_an']
    data = data.merge(tmp, on='id_an')

data

###########################################################

# Classification ทำนายได้ว่่าผู้ป่วยน่าจะหายดี หรือว่าต้องนอนรักษาไปเรื่อย ๆ แต่อาจจะไม่รอด หรือช่วยเหลือตัวเองไม่ได้
# เพื่อให้บุคลากรทางการแพทย์ และญาติผู้ป่วย สามารถเตรียมความพร้อมได้
X = data.drop(['id_an', 'hosdcgos'], axis=1)
y = data[['hosdcgos']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = RandomForestClassifier()

rf_param_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=1, stop=100, num=20)],
    'max_depth': [int(x) for x in np.linspace(start=10, stop=120, num=12)],
    'min_samples_split': [2, 6, 10],
    'min_samples_leaf': [1, 3, 4],
    'bootstrap': [True, False],
}

# hyperparameters optimization
search = RandomizedSearchCV(clf, rf_param_grid, cv=5, scoring='f1_micro', n_iter=100, n_jobs=-1, refit=True)
search.fit(X_train, np.ravel(y_train))
clf = search.best_estimator_ # select the best model

search.best_score_

###########################################################

importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
forest_importances = pd.Series(importances, index=X.columns)

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Feature importances using MDI")
ax.set_ylabel("Mean decrease in impurity")
fig.tight_layout()

###########################################################

gos =['recovery', 'Death', 'Vegetable Stage', 'Severe Disability', 'Moderate Recovery']
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=gos))

###########################################################