import random
import pandas as pd
import matplotlib.pyplot as plt

n = 10
day_start = []
day_end = []

for i in range(n):
    start, end = sorted([random.randint(1, 31), random.randint(1, 31)])
    day_start.append(f'{start} Jan 2023')
    day_end.append(f'{end} Jan 2023')

df = pd.DataFrame({
    'start': pd.to_datetime(day_start),
    'end': pd.to_datetime(day_end),
})

df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
df['days_to_end'] = (df['end'] - df['start'].min()).dt.days
df['duration'] = df['days_to_end'] - df['days_to_start']

df = df.sort_values(['days_to_start', 'days_to_end'])
df['task'] = [f'Task {i}' for i in range(1, n+1)]

print(df)

fig, ax = plt.subplots()

for idx, row in df.iterrows():
    ax.barh(y=row['task'], width=row['duration'], left=row['days_to_start'], alpha=0.4)

ax.invert_yaxis()
ax.axvline(x=15, color='r', linestyle='dashed')
plt.title('OPD Scheduling - GANTT Chart', fontsize='10')
plt.show()
