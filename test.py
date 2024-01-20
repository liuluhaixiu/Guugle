import pandas as pd
df = pd.read_excel("样本.xlsx",sheet_name="Sheet2")
dic = {}
for i in range(len(df)):
    type = df.iloc[i,0].split('.')[-1]
    df.iloc[i,1] = type
    df.iloc[i,2] = df.iloc[i,0].split('.')[-2]
df.to_csv("test.csv")