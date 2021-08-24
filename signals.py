import pandas as pd
import datetime
import numpy as np
from yfinance.utils import auto_adjust
import private
import settings
import pandas as pd
import numpy as np
import yfinance as yf
import schedule
import warnings
from easy_crypto import EasyCrypto
warnings.filterwarnings('ignore')

class signals:

    def __init__(self) -> None:
       self.easy_crypto = EasyCrypto()
    def macd_signal(self,Source, FastLength, SlowLength,  SignalLength):
        exp1 = Source.ewm(span=FastLength, adjust=False).mean()
        exp2 = Source.ewm(span=SlowLength, adjust=False).mean()
        macd = exp1-exp2
        signal = macd.ewm(span=SignalLength, adjust=False).mean()
        return pd.DataFrame({'macd': macd, 'signal': signal, })
    def williams(self,location):
        #calculate williams_%R
        williams=(self.data['High'].iloc[-location:-(settings.setting.williams_period+location):-1].max()-self.data['Close'].iloc[-1])/ \
            (self.data['High'].iloc[-location:-(settings.setting.williams_period+location):-1].max()\
                -self.data['Low'].iloc[-location:-(settings.setting.williams_period+location):-1].min())
        return williams
    def macd_status(self,result):
        '''
        This method is used to calculate mcd_status by using macd and signal indicators
        Parameters:
        result:-Dataframe dataframe that contains macd and signal data.
        '''
        action_status= ''
        relative_status= ''
        current_macd=result['macd'].iloc[-1] 
        previous_macd=result['macd'].iloc[-2] 
        current_signal=result['signal'].iloc[-1]
        # calculate buy and hold action status
        if current_macd > current_signal:
            if (current_macd < 0 and current_signal < 0) and (previous_macd < current_signal):
                    action_status= 'BUY'
            else:
                action_status= 'HOLD'
        # calculate sell and stay out
        if current_macd < current_signal:
            if (current_macd > 0 and current_signal > 0) and ( previous_macd> current_signal):
                action_status= 'SELL'
            else:
                action_status= 'STAY OUT'
        # calculate crossed down and crossed up relative status
        if (np.sign(previous_macd)*np.sign(current_macd) == -1):
                if np.sign(current_macd) == -1:
                    relative_status= 'CROSSED DOWN'
                else:
                    relative_status = 'CROSSED UP'
        # calculate above 0 and below 0 relative status
        elif current_macd > 0:
                relative_status= 'Above 0'
        elif current_macd < 0:
                relative_status = 'Below 0'

        return action_status,relative_status
    def williams_status(self):
        '''
        Is used to calculate williams_%R status using williams indicator and overbought and oversold lines
        '''
        current=self.williams(1)
        previous=self.williams(2)
        status=''
        # calculate buy and hold status
        if current>settings.setting.overSold:
            if previous<settings.setting.overSold:
                status='BUY'
            else:
                status='HOLD'
        # calculate sell and stay out status
        if current<settings.setting.overSold:
            if previous>settings.setting.overSold:
                status='SELL'
            else:
                status='STAY OUT'
        return status
    def write_to_google_sheet(self,data):
        client = private.authorize('client_secret.json')
        trading = client.open("trading")
        sheet = trading.worksheet("Sheet1")
        trading.values_clear("Sheet1!A1:"+f"W{len(settings.setting.ticker*2)+1}")
        sheet.insert_row(list(data.columns))
        send = []
        for row in data.values:
            send.append(list(row))
        sheet.insert_rows(send, row=2)
    def signal(self):
        result = pd.DataFrame(columns=['INSTRUMENT', 'INDICATOR','1M','1M(R)',
        '1W','1W(R)','1D','1D(R)','4H','4H(R)','1H','1H(R)','30m','30m(R)','15m','15m(R)','5m','5m(R)','2m','2m(R)','1m','1m(R)','INSTRUCTION'])
        for ticker in settings.setting.ticker:
            final_status=''
            macd = {'INSTRUMENT': ticker,
                     'INDICATOR': 'MACD',
                     '4H(R)':'',
                     '4H':''}
            williams_r={'INSTRUMENT': '',
                     'INDICATOR': '%R',
                     '1M(R)':'',
                     '1W(R)':'',
                     '1D(R)':'',
                     '4H(R)':'',
                     '4H':'',
                     '1H(R)':'',
                     '30m(R)':'',
                     '15m(R)':'',
                     '5m(R)':'',
                     '2m(R)':'',
                     '1m(R)':'',
                     'INSTRUCTION':''
            }
            for interval in ['1mo', '1wk', '1d','1h','30m','15m','5m','2m','1m']:
                if interval in ['1d','1wk','1mo']:
                    period='7y'
                elif interval=='1m':
                    period='7d'
                else:
                    period='30d'
                Ticker = yf.Ticker(ticker)
                self.data = Ticker.history(period=period,interval=interval)
                        
                action_status,relative_status = self.macd_status(self.macd_signal(self.data[settings.setting.Source], settings.setting.macd_fastLength,
                                               settings.setting.macd_slowLength, settings.setting.macd_signalLength))
                williams=self.williams_status()
                if interval=='1d':
                    macd['1D'] = action_status
                    macd['1D(R)'] = relative_status
                    williams_r['1D']=williams
                elif interval=='1wk':
                    macd['1W'] = action_status
                    macd['1W(R)'] = relative_status
                    williams_r['1W']=williams

                elif interval == '1h':
                    macd['1H'] = action_status
                    macd['1H(R)'] = relative_status
                    williams_r['1H'] = williams
                # elif interval == '4h':
                #     macd['4H'] = action_status
                #     macd['4H'] = relative_status
                #     williams_r['4H'] = williams
                elif interval=='1mo':
                    macd['1M'] = action_status
                    macd['1M(R)'] = relative_status
                    williams_r['1M'] = williams
                elif interval=='30m':
                    macd['30m'] = action_status
                    macd['30m(R)'] = relative_status
                    williams_r['30m'] = williams
                elif interval=='15m':
                    macd['15m'] = action_status
                    macd['15m(R)'] = relative_status
                    williams_r['15m'] = williams
                elif interval=='5m':
                    macd['5m'] = action_status
                    macd['5m(R)'] = relative_status
                    williams_r['5m'] = williams
                elif interval=='2m':
                    macd['2m'] = action_status
                    macd['2m(R)'] = relative_status
                    williams_r['2m'] = williams
                else:
                    macd['1m'] = action_status
                    macd['1m(R)'] = relative_status
                    williams_r['1m'] = williams
                # Determine the final status
                # BUY:
                if interval==settings.setting.instruction_period:
                    if (action_status in settings.setting.buy_condition['action_status'] \
                        and relative_status in settings.setting.buy_condition['relative_status']\
                        and williams in settings.setting.buy_condition['williams_status']):
                        macd['INSTRUCTION']='BUY'
                        if ticker=='BTC-USD':
                            self.easy_crypto.login()
                            self.easy_crypto.buy(settings.setting.buy_amount)
                #SELL:
                    elif (action_status in settings.setting.sell_condition['action_status'] \
                        and relative_status in settings.setting.sell_condition['relative_status']\
                        and williams in settings.setting.sell_condition['williams_status']):
                        macd['INSTRUCTION']='SELL'
                        if ticker=='BTC-USD':
                            self.easy_crypto.login()
                            self.easy_crypto.sell(settings.setting.sell_amount)
                #HOLD:

                    elif (action_status in settings.setting.hold_condition['action_status'] \
                        and relative_status in settings.setting.hold_condition['relative_status']\
                        and williams in settings.setting.hold_condition['williams_status']):
                        macd['INSTRUCTION']='HOLD'
                #STAY OUT
                    elif (action_status in settings.setting.stay_out_condition['action_status'] \
                        and relative_status in settings.setting.stay_out_condition['relative_status']\
                        and williams in settings.setting.stay_out_condition['williams_status']):
                        macd['INSTRUCTION']='STAY OUT'
                    else:
                        macd['INSTRUCTION']=''

            result = result.append(macd, ignore_index=True)
            result = result.append(williams_r, ignore_index=True)
        self.write_to_google_sheet(result)

signal=signals()
signal.signal()
while True:
    if datetime.datetime.now().minute % settings.setting.interval == 0:
        break
schedule.every(settings.setting.interval*60).seconds.do(signal.signal)
while True:
    schedule.run_pending()
