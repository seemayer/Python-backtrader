import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

import math
import datetime
from pandas_datareader import data as pdr
import matplotlib

################## STRATEGIES ########################
class BuyAndHold(bt.Strategy):
    def start(self):
        self.val_start = self.broker.get_cash()

    def nextstart(self):
        size = math.floor( (self.broker.get_cash()-10) / self.data[0])
        self.buy(size=size)

    def stop(self):
        #calc returns
        self.roi = (self.broker.get_value() / self.val_start) - 1
        print('-'*50)
        print('Buy and Hold')
        print('Starting value:   ${:,.2f}'.format(self.val_start))
        print('Ending value  :   ${:,.2f}'.format(self.broker.get_value()))
        print('Gross Return  :   ${:,.2f}'.format(self.broker.get_value()-self.val_start))
        print('ROI           :    {:,.2f}%'.format(self.roi * 100.0))
        print('Annualised    :    {:,.2f}%'.format(100*(1+self.roi)**(365/(endDate-actualStart).days)-1))

        




class FixedCommissionScheme(bt.CommInfoBase):
    paras = (
        ('commission', 10),
        ('stockllike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED)        
    )

    def _getcommission(self, size, price, pseudoexec):
        return self.p.commission


def get_data(stock_list, days):
    
    endDate = datetime.datetime.now()
    startDate = endDate - datetime.timedelta(days=days)
    
    stockData = pdr.get_data_yahoo(stock_list, startDate, endDate)
    
    return stockData


stock_list = ['ORCL']
data = get_data(stock_list[0], days=5000)
actualStart = data.index[0]
endDate = data.index[-1]
datafeed = btfeeds.PandasData(dataname = data)     
print(data, actualStart)


cerebro = bt.Cerebro()
cerebro.addstrategy(BuyAndHold)
cerebro.adddata(datafeed)

# set up broker
broker_args = dict(coc=True)
cerebro.broker = bt.brokers.BackBroker(**broker_args)
comminfo = FixedCommissionScheme()
cerebro.broker.addcommissioninfo(comminfo)
cerebro.broker.set_cash(100000)

cerebro.run()
# cerebro.plot(style='candlestick', iplot=False)
