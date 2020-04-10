# Author : zhenghaobaby
# Time : 2020/1/25 17:09
# File : Trigger.py
# Ide : PyCharm


from __future__ import (absolute_import,division,print_function,unicode_literals)

from backtrader_customize.untils.backtest_setting import backtest_setting
from backtrader_customize.Analysis.Trade_log_analysis import Trade_Analysis
from backtrader_customize.influx.process_data import process_data
import  pandas as pd
import os
import sys
from functools import partial
import multiprocessing as mp
import time



result_file = "test_rst"
setting_file = "backtest_setting.xlsx"

def run_single_strat(parameter,data):
    underlying = parameter['underlying']
    strategy = parameter['strategy']
    start_date = parameter['start_date']
    end_date = parameter['end_date']
    check_freq = parameter['check_freq']
    target_freq = parameter['target_freq']
    paras = parameter['paras']
    out_path = parameter['out_path']
    id = parameter['id']
    order_log = parameter['order_log']
    slippage = parameter['slippage']


    if 'JPY' in underlying:
        slippage *= 0.01
    else:
        slippage *= 0.0001

    try:
        start_time = time.time()
        df = data.loc[start_date:end_date,:]

        cerebo = backtest_setting(df,order_log,check_freq_check=check_freq,tgt_freq=target_freq,slip_pct=slippage)

        if target_freq==check_freq:
            time_grid = None
        else:
            df['time_stamp'] = df.index.tolist()
            if target_freq =="1D":
                time_grid = df.resample(target_freq).last()['time_stamp'].dropna().tolist()
            else:
                time_grid = df.resample(target_freq).first()['time_stamp'].dropna().tolist()
            time_grid = [i.tz_localize(None) for i in time_grid]

        cerebo.addstrategy(strategy,grid= time_grid, **paras)
        cerebo.run(stdstats=False, runonce = True, optdatas= True, opreturns = True)


        ##deal with order log
        order_log = pd.DataFrame(order_log)
        flag = Trade_Analysis(underlying=underlying,file_path=out_path,log_file=order_log,id=id)
        end_time = time.time()
        del cerebo
        cost_time = end_time-start_time

    ## for log
        if flag:
            with open(out_path+"\\Total_log.txt",'a+') as file:
                file.write(f"{id} {str(strategy)} {start_date} to {end_date} freq:{target_freq} succeed cost {cost_time}")
                file.write('\n')
                file.close()
        else:
            with open(out_path+"\\Total_log.txt",'a+') as file:
                file.write(f"{id} {str(strategy)} {start_date} to {end_date} freq:{target_freq} no trades")
                file.write('\n')
                file.close()


    except Exception as e:
        with open(out_path+"\\Total_log.txt",'a+') as file:
                file.write(f"{id} {str(strategy)} {start_date} to {end_date} freq:{target_freq} failed !!!")
                file.write(str(e))
                file.write("\n")
                file.close()

if __name__ == '__main__':
    start_time = time.time()
    if not os.path.exists(result_file):
        os.makedirs(result_file)

    out_path = os.path.join(os.getcwd(),f"{result_file}\\"+pd.datetime.now().strftime("%y%m%d_%H%M"))
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    else:
        print("please wait for one minute to re run the project")
        sys.exit()


    ##dynamic import
    df = pd.read_excel(f"{setting_file}",index_col='id')
    strats = list(set(df['strategy'].values))
    for strat in strats:
        exec(f"from backtrader_customize.Strategy.{strat} import {strat}")



    ##backtest setting load
    df['start_date'] = df['start_date'].apply(lambda x:pd.to_datetime(x))
    df['end_date'] = df['end_date'].apply(lambda x:pd.to_datetime(x))
    df['start_date'] = df['start_date'].dt.strftime("%Y-%m-%d")
    df['end_date'] = df['end_date'].dt.strftime("%Y-%m-%d")

    for pair_name, temp in df.groupby('underlying'):
        parameter_list = []
        start = temp['start_date'].min()
        end = temp['end_date'].max()
        row_data = process_data(start=start, end=end)


        ##multipossing
        for index, row in temp.iterrows():
            temp_dict = dict(zip(df.columns,row.values))
            temp_dict['strategy'] = eval(temp_dict['strategy'])
            temp_dict['paras'] = eval(temp_dict['paras'])
            temp_dict['paras']['underlying'] = temp_dict['underlying']
            temp_dict['out_path'] = out_path
            temp_dict['id'] = index
            order_log = {
                "datetime":[],
                "open":[],
                "close":[],
                "high":[],
                "low":[],
                "ref":[],
                "createdPrice":[],
                "createdSize":[],
                "executedPrice":[],
                "executedValue":[],
                "executedSize":[],
                "OrderType":[],
                "Status":[],
                "StopLoss":[],
                "TargetValue":[],
                "tradeid":[],
                "pos":[]
            }
            temp_dict['order_log']=order_log
            parameter_list.append(temp_dict)

        i = 0
        branch = 12
        while(i*branch<=len(parameter_list)):
            if (i+1)*branch>len(parameter_list):
                temp_parameter_list = parameter_list[i*branch:len(parameter_list)]
            else:
                temp_parameter_list = parameter_list[i*branch:(i+1)*branch]
            if len(temp_parameter_list)==0:
                break
            else:
                run_single_strat_partial = partial(run_single_strat,data=row_data)
                pool = mp.Pool(processes=6)
                pool.map(run_single_strat_partial,temp_parameter_list)
                # pool.close()
                # pool.join()
            i+=1

        print("start analyse the total results!!!")

    total_analysis = []
    file_name_list = os.listdir(out_path)
    for document_name in file_name_list:
        if not (document_name.endswith('.txt')) or document_name.endswith(".xlsx"):
            for file_name in os.listdir(out_path+"\\"+document_name):
                if file_name == 'Trade_analysis.csv':
                    log = pd.read_csv(out_path+"\\"+document_name+"\\"+file_name)
                    total_analysis.append(log)


    total_analysis = pd.concat(total_analysis)
    total_analysis.index = total_analysis['id']
    del total_analysis['id']
    end_time = time.time()
    cost_time = end_time-start_time

    with open(out_path+"\\Total_log.txt","a+") as file:
        file.write(f"Baacktest finished, total cost :{cost_time}")
        file.close()

    total_analysis = pd.concat([df,total_analysis],axis=1)
    total_analysis.to_csv(out_path+"\\Total_analysis.csv",index=True,header=True)
    print("ALL finished!!!")






