from LoanCalc import *


L22 = Loan(19094.00,3.5,136.95)
L24 = Loan(17121.00,4.25,131.94)
L20 = Loan(1172.96,3.5,16.62)
L23 = Loan(17754.57,3.5,129.46)
# L23.AddOneTimePmt(15000)

Loans = [L22,L24,L23]

sn = Snowball(Loans, 0)
print ("{},{:.2f}".format(sn.PayoffDate, sn.Duration/12))
exit()

total = sum(x.principal for x in Loans)
print ("${:,}".format(total, "10.2f"))

EvalPayoffs = [x for x in range(500,2100,100)]

results = []
print ("Pmt,Payoff,Duration")
for pmt in EvalPayoffs:
    sn = Snowball(Loans, pmt)
    results.append([pmt, sn.PayoffDate])
    res = "{},{},{:.2f}".format(pmt, sn.PayoffDate, sn.Duration/12)
    print (res)
