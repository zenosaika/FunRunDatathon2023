###########################################################

import pymysql

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

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

limit = ''

db = {
    'Q6_anesthetic': pd.read_sql_query(f'SELECT * FROM Q6_anesthetic {limit}', conn),
    'Q6_death': pd.read_sql_query(f'SELECT * FROM Q6_death {limit}', conn),
    'Q6_diag_ipd': pd.read_sql_query(f'SELECT * FROM Q6_diag_ipd {limit}', conn),
    'Q6_diag_opd': pd.read_sql_query(f'SELECT * FROM Q6_diag_opd {limit}', conn),
    'Q6_icd10': pd.read_sql_query(f'SELECT * FROM Q6_icd10 {limit}', conn),
    'Q6_lab': pd.read_sql_query(f'SELECT * FROM Q6_lab {limit}', conn),
    'Q6_main_data': pd.read_sql_query(f'SELECT * FROM Q6_main_data {limit}', conn),
    'Q6_operative_complication': pd.read_sql_query(f'SELECT * FROM Q6_operative_complication {limit}', conn),
    'Q6_timeline': pd.read_sql_query(f'SELECT * FROM Q6_timeline {limit}', conn),
    'Q6_ventilator': pd.read_sql_query(f'SELECT * FROM Q6_ventilator {limit}', conn),
}

###########################################################

used_id = 'id_an'
groups = []

print('table name / unique id / unique admit id')
for name, table in db.items():
    if name == 'Q6_icd10': # don't have unique id
        continue
    if name == 'Q6_death' or name == 'Q6_ventilator':
        continue
    print(f"{name} / {table['id'].unique().shape[0]} / {table['id_an'].unique().shape[0]}")
    groups.append(table[used_id].unique())

all_intersect_id = []
groups.sort(key=lambda x: len(x))
smallest_group, other_group = groups[0], [id for group in groups[1:] for id in group]

for id in smallest_group:
    if id in other_group:
        all_intersect_id.append(id)

print(f'len(all intersect id) = {len(all_intersect_id)}')

###########################################################

prepare_df = pd.DataFrame()
prepare_df['id'] = all_intersect_id

db['Q6_main_data']['bdate'] = pd.to_datetime(db['Q6_main_data']['bdate'], errors = 'coerce')
db['Q6_main_data']['ordate'] = pd.to_datetime(db['Q6_main_data']['ordate'], errors = 'coerce')
db['Q6_main_data']['age'] = (db['Q6_main_data']['ordate'] - db['Q6_main_data']['bdate']) / pd.Timedelta(days=1) // 365

temp_df = db['Q6_main_data'][[used_id, 'age']].drop_duplicates(subset=[used_id], keep='first')
temp_df.rename(columns = {used_id:'id'}, inplace = True)
prepare_df = prepare_df.merge(temp_df, on='id')
prepare_df.describe()

###########################################################

db['Q6_main_data']['admitdate'] = pd.to_datetime(db['Q6_main_data']['admitdate'], errors = 'coerce')
db['Q6_main_data']['disdate'] = pd.to_datetime(db['Q6_main_data']['disdate'], errors = 'coerce')
db['Q6_main_data']['days_to_discharge'] = (db['Q6_main_data']['disdate'] - db['Q6_main_data']['admitdate']) / pd.Timedelta(days=1)

temp_df = db['Q6_main_data'][[used_id, 'days_to_discharge']].drop_duplicates(subset=[used_id], keep='first')
temp_df.rename(columns = {used_id:'id'}, inplace = True)
prepare_df = prepare_df.merge(temp_df, on='id')

###########################################################

y = OrdinalEncoder().fit_transform(pd.DataFrame(db['Q6_operative_complication']['cname']))
temp_df = pd.DataFrame(db['Q6_operative_complication'][used_id])
temp_df['y'] = y

temp_df = pd.DataFrame(temp_df.groupby(used_id)['y'].apply(list))
temp_df

###########################################################

prepare_df = prepare_df.merge(temp_df, left_on='id', right_on=used_id)
prepare_df

###########################################################

temp_df = pd.DataFrame(prepare_df['y']) # 5137
prepare_df = prepare_df.drop('y', axis=1) # 5137
prepare_df

###########################################################

mlb = MultiLabelBinarizer(sparse_output=True)

y = temp_df.join(pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(temp_df.pop('y')),
                index=temp_df.index,
                columns=mlb.classes_)
            )
y

###########################################################

X = prepare_df.drop('id', axis=1)
X

###########################################################

X['days_to_discharge'] = X['days_to_discharge'].fillna(5)
X['days_to_discharge'].unique()

###########################################################

X_train, X_test, y_train, y_test = train_test_split(X, np.array(y).squeeze(), test_size=0.1)
y_test[1]

###########################################################

clf = MultiOutputClassifier(RandomForestClassifier()).fit(X_train, y_train)
score = clf.score(X_test, y_test)
f'Accuracy : {score:.3%}'

###########################################################
