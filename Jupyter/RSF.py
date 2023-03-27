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

# Survival Analysis เพื่อดูความน่าจะเป็นที่จะรอดชีวิต ณ เวลา t ใด ๆ ซึ่งจะเอาไปประกอบกับการใช้ regression ทำนาย
surv_data = data.copy()
date = db['Q4_admit'][['id_an', 'adm_d', 'disc_d', 'disc_status']]

# clean data
date['adm_d'] = pd.to_datetime(date['adm_d'], errors = 'coerce')
date['disc_d'] = pd.to_datetime(date['disc_d'], errors = 'coerce')
date['days_to_discharge'] = (date['disc_d'] - date['adm_d']) / pd.Timedelta(days=1)
date['disc_status'] = date['disc_status'].apply(lambda x: x=='Dead')
date['status_and_days'] = date.apply(lambda x: tuple([x['disc_status'], x['days_to_discharge']]), axis=1)

# merge data
surv_data = surv_data.merge(date[['id_an', 'status_and_days']], on='id_an')

X = surv_data.drop(['id_an', 'hosdcgos', 'status_and_days'], axis=1)
y = np.array(surv_data['status_and_days'], dtype=[('Status', '?'), ('Survival_in_days', '<f8')])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rsf = RandomSurvivalForest(n_estimators=100,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           )

rsf.fit(X_train, y_train)
rsf.score(X_test, y_test)

###########################################################

surv = rsf.predict_survival_function(X_test, return_array=True)

for i, s in enumerate(surv):
    plt.step(rsf.event_times_, s, where='post', label=str(i))
plt.title('[Survival Analysis] - Random Survival Forest (RSF)')
plt.ylabel('Survival Probability')
plt.xlabel('Time (Day)')
plt.grid(True)
plt.show()

###########################################################

test_data = X.head(1)
test_data['iss'] = 42
y_pred = rsf.predict(test_data)
print(y_pred)

surv = rsf.predict_survival_function(test_data, return_array=True)

for i, s in enumerate(surv):
    plt.step(rsf.event_times_, s, where='post', label=str(i))
plt.title('[Survival Analysis] - Random Survival Forest (RSF)')
plt.ylabel('Survival Probability')
plt.xlabel('Time (day)')
plt.axvline(x=40, color='r', linestyle='dashed')
plt.text(x=41, y=0.8, s='Discharge')
plt.grid(True)
plt.show()

###########################################################