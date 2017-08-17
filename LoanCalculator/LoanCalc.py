import pandas as pd
import datetime
import numpy as np
import  matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta


def main():
    nPer = 1
    l1 = Loan(10000,2.5,len_mos=60, Addl_Principal=50)
    l1.AddOneTimePmt(1000)
    print (l1)
#     print(l1.CalcPV(nPer,500))
#     print(l1.CalcFV(nPer,pmt=500))

# # numpy.fv(rate, nper, pmt, pv, when='end')[source]
#     print (np.fv(0.025/12, nPer, -500, 10000))


class Loan():
    principal = 0.0
    interest = 0.0
    minPmt = 0.0
    nPmts = 0.0
    duration = 0

    def __init__(self, principal, interest, min_payment=None, num_pmts=None, len_mos=None, len_yrs=None, Addl_Principal=0.0):
        
        if principal > 0:
            self.principal = principal
        else:
            self.principal = principal * -1

        if interest > 1:
            self.interest = interest / 100.0
        else:
            self.interest = interest

        if len_yrs is None and len_mos is None and min_payment is None:
            raise ValueError("Must have either a minimum payment, or payment period defined.")

        if len_mos is None:
            if len_yrs is not None:
                self.duration = len_yrs*12
        else:
            self.duration = len_mos

        self.rate = self.interest/12

        if min_payment is None:
            if len_mos is not None:
                self.minPmt = np.pmt(self.rate, len_mos, self.principal)
        else:
            if min_payment < 0:
                self.minPmt = min_payment
            else:
                self.minPmt = min_payment * -1

        if num_pmts is None:
            self.nPmts = np.nper(self.rate, self.minPmt, self.principal)
        else:
            self.nPmts = num_pmts

        self.addl = Addl_Principal if Addl_Principal < 0 else Addl_Principal * -1

        startDate = datetime.date.today()- datetime.timedelta(days=30)
        rng = pd.date_range(startDate, periods=self.nPmts, freq='MS')
        rng.name = "Payment_Date"
        self.df = pd.DataFrame(index=rng,columns=['Payment', 'Principal', 'Interest', 'Addl_Principal', 'Balance'], dtype='float')
        self.df.reset_index(inplace=True)
        self.df.index += 1
        self.df.index.name = "Period"

        self.df['Addl_Principal'] = self.addl

        self.Calculate()

    def __str__(self):
        return str(self.df)

    def Calculate(self):
        self.df['Principal'] = np.ppmt(self.rate, self.df.index, self.nPmts, self.principal)
        self.df['Interest'] = np.ipmt(self.rate, self.df.index, self.nPmts, self.principal)
        self.df['Payment'] = self.df['Principal'] + self.df['Interest']

        self.df['Balance'] = self.principal + self.df['Principal'].cumsum() + self.df['Addl_Principal'].cumsum()
        self.df['BaseBal'] = self.principal + self.df['Principal'].cumsum()
        self.principalSavings = self.df['Interest'].sum() * -1
        self.df = self.df[self.df['Balance'] > 0]
        self.duration = self.df.axes[0].size
        self.payoffDate = datetime.date.today() + relativedelta(months=self.duration)

    def CalculateWithAddl(self, addl, startPeriod = 0):
        addl = addl if addl < 0 else addl * -1
        self.df.loc[startPeriod:,('Addl_Principal')] = addl
        self.Calculate()

    def AddOneTimePmt(self, addl, period=0):
        addl = addl if addl < 0 else addl * -1
        self.df.loc[period:period+1,('Addl_Principal')] += addl
        self.Calculate()
        
class Snowball():
    ranking = []
    interestList = []
    principalList = []
    loans = []

    def __init__(self, loans, totalPmt):
        self.loans = loans
        self.totalPmt = totalPmt
        self.totalMinPmt = sum(x.minPmt for x in loans)
        self.initialTotal = sum(x.principal for x in loans)
        if totalPmt < self.totalMinPmt:
            print("Total payment less than total of minimum payment. Value applied as additional to minimum.")
            self.totalPmt = self.totalMinPmt + totalPmt
        self.BuildRankingList()
        
    def BuildRankingList(self):
        tmpInt, tmpPrin = [],[]
        for loan in self.loans:
            tmpInt.append(loan.interest)
            tmpPrin.append(loan.principal)

        tmpLoans = self.loans + []
        while len(tmpLoans) >= 1:
            idx = 0
            for loan in tmpLoans:
                intr = loan.interest
                isMaxInterest = intr == max(tmpInt)

                # Add the highest interest loans first, then move to balances
                # if there are multiple loans at the same interest.
                if tmpInt.count(intr) == 1 and isMaxInterest:
                    self.ranking.append(loan)
                    self.interestList.append(loan.interest)
                    self.principalList.append(loan.principal)

                    del tmpInt[idx]
                    del tmpPrin[idx]
                    tmpLoans.remove(loan)

                # Only add next interest level if there are muliples of it and this is the current
                # highest interest class.
                elif tmpInt.count(intr) > 1 and isMaxInterest and loan.principal == max(tmpPrin):
                    self.ranking.append(loan)
                    self.interestList.append(loan.interest)
                    self.principalList.append(loan.principal)

                    del tmpInt[idx]
                    del tmpPrin[idx]
                    tmpLoans.remove(loan)
                idx += 1

        self.ProcessSnowball()

    def ProcessSnowball(self):
        payoffPer = 0
        for loan in self.ranking:
            addl = self.totalPmt + self.totalMinPmt
            loan.CalculateWithAddl(addl, payoffPer)
            payoffPer = loan.duration
            self.totalMinPmt = self.totalMinPmt - loan.minPmt
            self.maxPer = loan.duration
            self.payoffDate = loan.payoffDate

    def Graph(self, attr):
        for loan in self.loans:
            loan.df[attr].plot()
        plt.show()

    def GetTallyDF(self, attr):
        x = []
        for loan in self.loans:
            x.append(loan.df[attr])
        idx = ["{}_{}".format(attr, x) for x in range(len(self.loans))]
        tmp = pd.concat(x, keys=idx, axis=1)
        tmp.fillna(0, inplace=True)
        startDate = datetime.date.today()- datetime.timedelta(days=30)
        tmp['Date'] = pd.date_range(startDate, periods=tmp.axes[0].size, freq='MS')
        colList = [len(self.loans)] + [x for x in range(len(self.loans))]
        tmp = tmp[colList]
        return tmp

    @property
    def PayoffDate(self):
        return pd.to_datetime(self.payoffDate, format='%Y-%m-%d')

    @property
    def Duration(self):
        return self.maxPer

    def SaveToCSV(self, filename, attr="Balance"):
        df = self.GetTallyDF(attr)
        df.to_csv(filename)

    def __str__(self):
        payoffStr = "Payoff Date: {}\n".format(self.payoffDate)
        return payoffStr + str(self.GetTallyDF("Balance"))


if __name__ == '__main__':
    main()