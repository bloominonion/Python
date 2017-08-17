import pandas as pd
import numpy as np 
import  matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta


principal = 5000
minPmt = -500
rate = 3.5/100/12
nPmts = np.nper(rate, minPmt, principal)

startDate = datetime.date.today() - datetime.timedelta(days=30)
rng = pd.date_range(startDate, periods=nPmts, freq='MS')
rng.name = "Payment_Date"
df = pd.DataFrame(index=rng,columns=['Payment', 'Principal', 'Interest', 'Addl_Principal', 'Balance'], dtype='float')
df.reset_index(inplace=True)
df.index += 1
df.index.name = "Period"

df['Principal'] = np.ppmt(rate, df.index, nPmts, principal)
df['Interest'] = np.ipmt(rate, df.index, nPmts, principal)
df['Payment'] = df['Principal'] + df['Interest']
df['Addl_Principal'] = 0
df.loc[5:,('Addl_Principal')] = -200

df['Balance'] = principal + df['Principal'].cumsum() + df['Addl_Principal'].cumsum()
df = df[df['Balance'] > 0]
print (df)
df['Balance'].plot()
plt.show()

duration = df.size
payoffDate = datetime.date.today() + relativedelta(months=duration)
print ("Payoff date: {}".format(payoffDate))