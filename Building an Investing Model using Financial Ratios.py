#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
companies=[]
marketcap=str(10000000)


# In[4]:


url=(f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={marketcap}&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=1000&apikey=5440fa1b83055823728a35b8988f31eb')
screener=requests.get(url).json()
for item in screener:
    companies.append(item['symbol'])


# In[17]:


value_ratios={}
count=0
for company in companies:
    try:
        if count<10:
            fin_ratios=requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey=5440fa1b83055823728a35b8988f31eb').json()
            count+=1
            value_ratios[company]={}
            value_ratios[company]['ROE']=fin_ratios[0]['returnOnEquity']
            value_ratios[company]['ROA']=fin_ratios[0]['returnOnAssets']
            value_ratios[company]['Debt_Ratio']=fin_ratios[0]['debtRatio']
            value_ratios[company]['Interest_Coverage']=fin_ratios[0]['interestCoverage']
            value_ratios[company]['Payout_Ratio']=fin_ratios[0]['payoutRatio']
            value_ratios[company]['Dividend_Payout_Ratio']=fin_ratios[0]['dividendPayoutRatio']
            value_ratios[company]['PB']=fin_ratios[0]['priceToBookRatio']
            value_ratios[company]['PS']=fin_ratios[0]['priceToSalesRatio']
            value_ratios[company]['Dividend_Yield']=fin_ratios[0]['dividendYield']
            value_ratios[company]['Grossprofit_Margin']=fin_ratios[0]['grossProfitMargin']
            # more financials on Growth
            growth_ratios=requests.get(f'https://financialmodelingprep.com/api/v3/financial-growth/{company}?apikey=5440fa1b83055823728a35b8988f31eb').json()
            value_ratios[company]['Revenue_Growth']=growth_ratios[0]['revenueGrowth']
            value_ratios[company]['NetIncome_Growth']=growth_ratios[0]['netIncomeGrowth']
            value_ratios[company]['EPS_Growth']=growth_ratios[0]['epsgrowth']
            value_ratios[company]['RD_Growth']=growth_ratios[0]['rdexpenseGrowth']
    except:
        pass


# In[18]:


DF=pd.DataFrame.from_dict(value_ratios,orient='index')
DF


# In[19]:


ROE=1.2 
ROA=1.1
Debt_Ratio=-1.1#how much company have of debt
Interest_Coverage=1.05# how many time the company can pay the interest
Dividend_Payout_Ratio=1.01
PB=-1.10# if company has a big price to book ratio it mean may be the company is overvalue is traded at price to high compared to the value in their books 
PS=-1.05
Revenue_Growth=1.25
Net_Income_Growth=1.10
ratios_mean=[]
for item in DF.columns:
    ratios_mean.append(DF[item].mean())



# In[21]:


DF=DF/ratios_mean
DF['ranking']=DF['NetIncome_Growth']*Net_Income_Growth+DF['Revenue_Growth']*Revenue_Growth+DF['ROE']*ROE+DF['ROA']*ROA+DF['Debt_Ratio']*Debt_Ratio+DF['Interest_Coverage']*Interest_Coverage+DF['Dividend_Payout_Ratio']*Dividend_Payout_Ratio+DF['PB']*PB+DF['PS']*PS


# In[22]:


print(DF.sort_values(by=['ranking'],ascending=False))


# In[ ]:




