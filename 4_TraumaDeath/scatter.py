import random
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

X = [[random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)] for _ in range(200)]
y = [x[0]**3*3+x[1]**2*4+x[2] for x in X]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = DecisionTreeRegressor()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(clf.score(X_test, y_test))

plt.scatter(y_pred, y_test)
plt.show()
