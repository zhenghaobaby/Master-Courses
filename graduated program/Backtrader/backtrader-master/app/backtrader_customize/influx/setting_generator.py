# Author : zhenghaobaby
# Time : 2020/3/13 18:31
# File : setting_generator.py
# Ide : PyCharm


import pandas as pd
import itertools
from numpy import prod
import copy
import numpy as np

"""
the script aims to generate backtest_setting.xlsx with least effort
key concept:

variables: setting items that occupy a column
paras: setting in the 'paras' column, always a dictionary

free variables: list, the item you want to iterate through, change through the list
fixed variables: constant in the setting file.    can be used as      free [fixed variable]        as well
dependent variables: dict, variable that depend on 1 free or fixed variable. need to specify a dictionary 
explaining which free/fixed variable it's based on, and how its value is determined by the free var
it can also depend on previous set dependent vars

free paras: same as free var, just in the paras column
fixed paras: same as fixed var, just in the paras column
dependent variables: similar, can depend on free/fixed var as well as paras
DependentFreePara: list. fixed on certain var, but is 'free' within the fixed var, e.g. strategy periods

"""



def generate_setting(strategy,underlying,target_freq,start_date,end_date):
    class DependentVar:
        def __init__(self, v_dict):
            self.v_dict = v_dict

        def add2df(self, name, df):
            self.name = name
            for r_idx, rcd in df.iterrows():
                for k in self.v_dict:
                    df.loc[r_idx, self.name] = self.v_dict[k][rcd[k]]
            return df

    class DependentPara:
        def __init__(self, v_dict):
            self.v_dict = v_dict

        def add2df(self, name, paras_list, df):
            self.name = name
            if 'paras' not in df.columns:
                df['paras'] = [{} for _ in range(len(df))]

            for r_idx, rcd in df.iterrows():
                cur_fixed_para = paras_list[r_idx % len(paras_list)]
                df.loc[r_idx, 'paras'].update(cur_fixed_para)

                for k, v in self.v_dict.items():
                    if k not in df.columns:
                        df.loc[r_idx, 'paras'].update({self.name: self.v_dict[k][cur_fixed_para[k]]})
                    else:
                        df.loc[r_idx, 'paras'].update({self.name: self.v_dict[k][rcd[k]]})
            return df

    class DependentFreePara:
        def __init__(self, v_dict):
            self.v_dict = v_dict

        def add2df(self, name, df):
            self.name = name
            df = df.copy()
            if 'paras' not in df.columns:
                df['paras'] = [{} for _ in range(len(df))]
            new_df = []
            for r_idx, rcd in df.iterrows():
                for k in self.v_dict:
                    df_val = rcd[k]
                    add_to_para = self.v_dict[k][df_val]

                    found_tuple = any([type(i) == tuple for i in add_to_para.keys()])

                    if not found_tuple:
                        add_to_para = [{i: v for i, v in zip(tuple(add_to_para.keys()), k)} for k in \
                                       itertools.product(*list(add_to_para.values()))]

                    elif found_tuple:
                        add_to_para_list = {i: add_to_para[i] for i in add_to_para.keys() if type(i) is not tuple}
                        add_to_para_list = [{i: v for i, v in zip(tuple(add_to_para_list.keys()), k)} for k in \
                                            itertools.product(*list(add_to_para_list.values()))]

                        add_to_para_tuple_out = []
                        for tup in add_to_para.keys():
                            if type(tup) == tuple:
                                add_to_para_tuple = add_to_para[tup]
                                add_to_para_tuple = [{tup_k: v for tup_k, v in zip(tup, tup_v)} for tup_v in
                                                     add_to_para_tuple]
                                add_to_para_tuple_out.append(add_to_para_tuple)
                        add_to_para_tuple_out = [i[0] for i in itertools.product(*add_to_para_tuple_out)]
                        add_to_para = [{**i[0], **i[1]} for i in
                                       itertools.product(add_to_para_list, add_to_para_tuple_out)]

                for para in add_to_para:
                    # temp_rcd = rcd.to_dict()
                    temp_rcd = copy.deepcopy(rcd.to_dict())
                    temp_rcd['paras'].update(para)
                    new_df.append(temp_rcd)

            a = pd.DataFrame(new_df, columns=df.columns)
            return a

    free_var = {'strategy': strategy,
                'underlying': underlying,
                'target_freq': target_freq}
    fixed_var = {'check_freq': '1min','start_date':start_date, 'end_date':end_date}

    slippage = DependentVar(v_dict={'underlying': {'NZDUSD': 0.4, 'EURUSD': 0.3, 'AUDUSD':0.3, 'USDJPY':0.3,'USDTHB':0.3,'USDCNH':0.3,'USDINR':0.3,
                                             'SGDJPY':0.3,'USDHKD':0.3,'USDSGD':0.3}},)
    db = DependentVar(v_dict={'underlying': {'NZDUSD': 'fx_1m', 'EURUSD': 'fx_1m', 'AUDUSD':'fx_1m', 'USDJPY': 'fx_1m','USDTHB':'fx_tick','USDCNH':'fx_tick','USDINR':'fx_tick',
                                             'SGDJPY':'fx_1m','USDHKD':'fx_1m','USDSGD':'fx_1m'}},)
    source = DependentVar(v_dict={
        'underlying': {'NZDUSD': 'HISTDATA', 'EURUSD': 'HISTDATA', 'AUDUSD': 'HISTDATA', 'USDJPY': 'HISTDATA', 'USDTHB': 'ECOM',
                       'USDCNH': 'ECOM', 'USDINR': 'ECOM',
                       'SGDJPY': 'HISTDATA', 'USDHKD': 'HISTDATA', 'USDSGD': 'HISTDATA'}}, )



    dependent_var = {'slippage': slippage,'db':db,'source':source}

    df = pd.DataFrame(itertools.product(*[i for i in free_var.values()]), columns=free_var.keys())
    for k, v in fixed_var.items():
        df[k] = v
    for k, v in dependent_var.items():
        df = v.add2df(k, df)


    free_paras =  {}
    paras_list = [{i:v for i, v in zip(tuple(free_paras.keys()), k)}for k in itertools.product(*list(free_paras.values()))]
    fixed_paras = {'maxpos':20,'minpos':-20}
    _ = [i.update(fixed_paras) for i in paras_list]
    SL = DependentPara(v_dict={'target_freq': {'5min': 20, '15min': 20, '30min': 30, '60min': 30, '120min':30,'240min': 30,'1D':60}},)
    TP = DependentPara(v_dict={'target_freq': {'5min': 30, '15min': 30, '30min': 50, '60min': 50, '120min':60,'240min': 60,'1D':120}},)
    start_time = DependentPara(v_dict={'underlying':{'USDCNH':'09:30','USDSGD':'09:30','USDHKD':'09:30','SGDJPY':'09:30','USDINR':'09:30','USDTHB':'09:30',
                                                     'EURUSD':'07:00','USDJPY':'07:00','AUDUSD':'07:00','NZDUSD':'07:00'}})
    end_time = DependentPara(v_dict={'underlying':{'USDCNH':'16:45','USDSGD':'16:45','USDHKD':'16:45','SGDJPY':'16:45','USDINR':'16:45','USDTHB':'16:45',
                                                     'EURUSD':'23:45','USDJPY':'23:45','AUDUSD':'23:45','NZDUSD':'23:45'}})
    force_time = DependentPara(v_dict={'underlying':{'USDCNH':'16:59','USDSGD':'16:59','USDHKD':'16:59','SGDJPY':'16:59','USDINR':'16:59','USDTHB':'16:59',
                                                     'EURUSD':'23:59','USDJPY':'23:59','AUDUSD':'23:59','NZDUSD':'23:59'}})


    strat_specs = DependentFreePara(v_dict={'strategy':\
                    {'ADO': {'period': [5,10,20,60,120]},
                     'AroonOscillator': {'period':[5,10,20,60,120]},
                     'AwesomeOscillator': {('fast','slow'):[(5,10),(10,20),(60,120)]},
                     'CMCI': {'period':[5,10,20,60,120]},
                     'DV2': {'period': [5,10,20,60,120]},
                     'FibonacciPivotPoint': {'period':[5,10,20,60,120]},
                     'Fractal': {'period':[5,10,20,60,120]},
                     'HurstExponent':{'period':[5,10,20,50,60,120]},
                     'Ichimoku':{},
                     'KST':{},
                     'LaguerreRSI':{'period':[5,10,20,60,120]},
                     'ParabolicSAR':{'period':[5,10,20,60,120]},
                     'PercentagePriceOscillator':{('period1','period2'):[(5,10),(10,20),(60,120)]},
                     'PercentagePriceOscillatorshort':{'maxpos':[20],'minpos':[-20]},
                     'PrettyGoodOscillator':{'period':[5,10,20,60,120]},
                     'RMI':{'period':[5,10,20,60,120]},
                     'Trix':{('period','sigperiod'):[(5,3),(10,5),(20,10),(60,30),(120,60)]},
                     'TSI':{('period1','period2','sigperiod'):[(10,5,3),(20,10,5),(60,30,15),(120,60,30)]},
                     'UltimateOscillator':{('p1','p2','p3'):[(5,10,15),(10,20,30),(20,40,80),(60,80,120)]},
                     'Vortex':{'period':[5,10,20,60,120]},
                     'WilliamsAD':{'period':[5,10,20,60,120]},
                     'Zerolagindicator':{'maxpos':[20],'minpos':[-20]},
                     'ZLI_Envelope':{'period':[5,10,20,60,120]},
                     'ZLI_Oscillator':{'period':[5,10,20,60,120]},
                     'CMI':{'period':[5,10,20,30,60]},
                     'Hammer':{('period','shadow_ratio'):[(5,0.05),(5,0.1),(5,0.15),(5,0.2),(10,0.05),(10,0.1),(10,0.15),(10,0.2),
                                                          (20,0.05),(20,0.1),(20,0.15),(20,0.2),(30,0.05),(30,0.1),(30,0.15),(30,0.2),
                                                          (60,0.05),(60,0.1),(60,0.15),(60,0.2)]},
                     },
                                            },)


    dependent_paras = {'SL': SL, 'TP': TP,'start_time':start_time,'end_time':end_time,'force_time':force_time}

    fixed_free_paras = {'strat_specs': strat_specs}



    for k, v in fixed_free_paras.items():
        df = v.add2df(k, df)
    df = pd.concat([df]*max(1, (prod([len(v) for v in free_paras.values()])-1)), ignore_index=True)
    for k, v in dependent_paras.items():
        df = v.add2df(k, paras_list, df)


    cols = ['id','underlying','start_date','end_date','target_freq','check_freq','db','source','strategy','slippage']
    #df.drop_duplicates(keep='first',inplace=True)
    df['id'] = [i for i in range(1, len(df)+1)]
    cols = ['id','underlying','start_date','end_date','target_freq','check_freq','db','source','strategy','paras','slippage']
    df = df[cols]



    df[df['strategy']=='CMI']['paras'].apply(lambda x:x.update({'start_time':'09:30','end_time':"17:00",'force_time':"14:00",'SL':2000,'TP':2000}))
    df.loc[df['strategy']=='CMI','check_freq'] = df['target_freq']

    df[df['strategy'] == 'Hammer']['paras'].apply(
        lambda x: x.update({'start_time': '00:00', 'end_time': "23:59", 'force_time': "14:00", 'SL': 2000, 'TP': 2000}))
    df.loc[df['strategy'] == 'Hammer', 'check_freq'] = df['target_freq']


    # df.to_excel('auto_setting.xlsx', index=None)
    return df

def generate_total_setting(strategy,underlying,target_freq,start_date,end_date):
    date_range = pd.date_range(start=start_date,end=end_date,freq='AS',closed='left')
    date_list = []
    for i in range(len(date_range.values)):
        date_list.append(str(date_range.values[i]).replace("T", " ")[:10])

    date_list.append(end_date)

    data = []
    for i in range(len(date_list)-1):
        temp = generate_setting(strategy, underlying,target_freq, date_list[i], date_list[i+1])
        data.append(temp)
    data = pd.concat(data)
    data['id'] = np.arange(len(data))
    data.index = data['id']
    return  data



m=generate_total_setting(strategy = ['Hammer'],underlying =['EURUSD'],target_freq=['1D'],start_date='2014-01-01',end_date='2019-01-01')
m.to_excel('auto_setting.xlsx',index=None)
