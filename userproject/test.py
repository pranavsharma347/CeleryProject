
import pandas as pd

data = pd.read_csv('/home/admin1/Desktop/10.csv')
data.dropna(subset=['username'], inplace=True)
data.dropna(subset=['name'], inplace=True)
data.dropna(subset=['email'], inplace=True)
data.dropna(subset=['phone'], inplace=True)
print(data)

for index,row in data.iterrows():
    print(row['username'],row['name'],row['email'],row['phone'])



