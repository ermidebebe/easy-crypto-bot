from dataclasses import dataclass
@dataclass
class settings:
    ticker: list
    interval: int
    Source:str
    macd_fastLength:float
    macd_slowLength: float 
    macd_signalLength:float
    buy_amount:float
    sell_amount:float
    williams_period:int
    overBought:float
    overSold:float
    instruction_period:str
    buy_condition:dict
    sell_condition:dict
    hold_condition:dict
    stay_out_condition:dict
    password:str
    email:str
setting = settings(ticker = ['AAPL','TSLA','BTC-USD'],interval= 1,
                   Source='Close',macd_fastLength=52, macd_slowLength=100, 
                   macd_signalLength=15,buy_amount=0.000000001,sell_amount=0.000000001,
                   williams_period=50,overBought=-20,overSold=-80,
                   instruction_period='1m',
                   buy_condition={'action_status':['SELL','STAY OUT','HOLD','BUY'],
                                  'relative_status':['Below 0','Above 0'],
                                  'williams_status':['BUY','HOLD']
                                  },
                   sell_condition={'action_status':['SELL'],
                                  'relative_status':['Above 0','Below 0'],
                                  'williams_status':['SELL','STAY OUT','HOLD']
                                  },
                   hold_condition={'action_status':['HOLD'],
                                  'relative_status':['Above 0','Below 0'],
                                  'williams_status':['HOLD']
                                  },
                   stay_out_condition={'action_status':['STAY OUT'],
                                  'relative_status':['Above 0','Below 0'],
                                  'williams_status':['STAY OUT']
                                  },
                   password='',
                   email='')