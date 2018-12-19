# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import scipy.stats.stats as stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math


# 定义自动分箱函数
def mono_bin(Y, X, n = 20):
    r = 0
    good=Y.sum()
    bad=Y.count()-good
    while np.abs(r) < 1:
        d1 = pd.DataFrame({"X": X, "Y": Y, "Bucket": pd.qcut(X, n)})
        d2 = d1.groupby('Bucket', as_index = True)
        print d2.mean()
        print d2.mean().X
        r, p = stats.spearmanr(d2.mean().X, d2.mean().Y)
        n = n - 1
    d3 = pd.DataFrame(d2.X.min(), columns = ['min'])
    d3['min']=d2.min().X
    d3['max'] = d2.max().X
    d3['sum'] = d2.sum().Y
    d3['total'] = d2.count().Y
    d3['rate'] = d2.mean().Y
    d3['woe']=np.log((d3['rate']/(1-d3['rate']))/(good/bad))
    d3['goodattribute']=d3['sum']/good
    d3['badattribute']=(d3['total']-d3['sum'])/bad
    iv=((d3['goodattribute']-d3['badattribute'])*d3['woe']).sum()
    d4 = (d3.sort_values(by = 'min'))
    print("=" * 60)
    print(d4)
    cut=[]
    cut.append(float('-inf'))
    for i in range(1,n+1):
        qua=X.quantile(i/(n+1))
        cut.append(round(qua,4))
    cut.append(float('inf'))
    woe=list(d4['woe'].round(3))
    return d4,iv,cut,woe

#自定义分箱函数



if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    pinf = float('inf')  # 正无穷大
    ninf = float('-inf')  # 负无穷大
    dfx1, ivx1, cutx1, woex1 = mono_bin(data.SeriousDlqin2yrs, data.RevolvingUtilizationOfUnsecuredLines, n=10)
    dfx2, ivx2, cutx2, woex2 = mono_bin(data.SeriousDlqin2yrs, data.age, n=10)
    dfx4, ivx4, cutx4, woex4 = mono_bin(data.SeriousDlqin2yrs, data.DebtRatio, n=20)
    dfx5, ivx5, cutx5, woex5 = mono_bin(data.SeriousDlqin2yrs, data.MonthlyIncome, n=10)
    # 连续变量离散化
