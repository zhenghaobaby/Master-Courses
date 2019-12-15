## Project of Financial Econometrics
## Author: Equator Quant
## Team members: Zheng Hao, Xiao Chao, Zheng Pin, Liu Yonghao, Shan Changhan
## 2019.11.02

# install.packages('tseries')
# install.packages('forecast')
# install.packages('rugarch')
# install.packages('xts')
library(tseries)
library(forecast)
library(rugarch)
library(xts)
library(ggplot2)

cat('\f')
rm(list = ls())
graphics.off()
setwd('/Users/shan/NUS/FinancialEconometrics/PJ_Econometrics')
options(max.print = 15)

nameList = c('Date' = 1, 'closePrice' = 7, 'openToClose' = 17,
             'rvs' = 3, 'bvs' = 8, 'rk' = 20)
modelList = c('Garch','EGarch','RGarch_rvs','RGarch_bvs','RGarch_rk',
              'RW_rvs','RW_bvs','RW_rk','MA_rvs','MA_bvs','MA_rk',
              'EW_rvs','EW_bvs','EW_rk')
volList = c('rvs','bvs','rk')
tickerList = c('FTSE','N225','GDAXI','DJI','FCHI','KS11',
               'AEX','SSMI','IBEX','NSEI','MXX','STOXX50E')
# missed index 'FTSTI', 'AORD', 'BVSP', 'FTMIB'

fill_NA = function(df,a){df[is.na(df)] = a;return(df)}
MSEquant = function(pred,bench){mean((bench-pred)^2)}
QLIKEquant = function(pred,bench){mean(log(pred)+(bench/pred))}

## function to calculate criterion
Criterion = function(ticker = 'FTSE'){
  rawData = read.csv(paste0('./data_split/',ticker,'.csv')) # raw data from csv
  Date = as.POSIXlt(rawData$Date) 
  beginDate = '2000-01-01'
  endDate = '2019-09-20'
  dateRange = sum(Date <= endDate) # date range of data
  Date = Date[1:dateRange]
  rawData = rawData[1:dateRange,]
  
  dfData = rawData[nameList[-1]] # data as dataframe
  names(dfData) = names(nameList[-1])
  rownames(dfData) = Date
  tData = as.xts(dfData) # data as time series
  len = dim(tData)[1]
  
  closeDiff = diff(tData[,'closePrice'])
  closeLag = lag(tData[,'closePrice'],1)
  closeToClose = closeDiff/closeLag; names(closeToClose) = 'closeToClose'
  closeToClose = fill_NA(closeToClose,0)
  logRe = log(closeToClose+1); names(logRe) = 'logRe'
  tData = merge(tData,closeToClose,logRe)
  
  Uoc = sum(log(tData[,'openToClose']+1))/len
  Ucc = sum(log(tData[,'closeToClose']+1))/len
  scalingFactor = sum((log(tData[,'closeToClose']+1)-Ucc)^2)/
    sum((log(tData[,'openToClose']+1)-Uoc)^2)
    
  
  tData[,volList] = tData[,volList]*scalingFactor
  dfData = data.frame(tData)
  
  # ## stationary test
  # adf.test(tData[,'logRe'])
  # kpss.test(tData[,'logRe'])
  # acf(dfData['logRe'],main = 'log return')
  # acf(dfData['logRe']^2,main = 'square of log return')  # garch effect obvious
  
  ### Model
  benchMark = dfData[2001:len,'rk']
  criterion = data.frame(matrix(0,3,14))
  rownames(criterion) = c('MSE','QLIKE','BIC')
  names(criterion) = modelList
  
  ## GRARCH(1,1)
  garch = ugarchspec(variance.model = list(model = "sGARCH", garchOrder=c(1,1)),
                     mean.model = list(armaOrder = c(1,0)),
                     distribution.model = "std")
  garchRoll = ugarchroll(spec = garch,data = dfData['logRe'],n.ahead=1,
                         refit.every = 100,n.start = 2000,
                         refit.window = "moving",window.size = 1000,
                         calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
  # I'd better figure out the meanings
  garchFit=ugarchfit(spec = garch,data = dfData['logRe'],solver = "solnp")
  BIC = infocriteria(garchFit)[2]
  garchPred = garchRoll@forecast[["density"]][["Sigma"]]^2
  dfData[2001:len,'Garch'] = garchPred
  criterion['MSE','Garch'] = MSEquant(garchPred,benchMark)
  criterion['QLIKE','Garch'] = QLIKEquant(garchPred,benchMark)
  criterion['BIC','Garch'] = BIC
  cat('Garch done. ')
  
  ## EGARCH(1,1)
  egarch = ugarchspec(variance.model = list(model = "eGARCH", garchOrder=c(1,1)),
                      mean.model = list(armaOrder = c(1,0)),
                      distribution.model = "std")
  egarchRoll = ugarchroll(spec = egarch,data = dfData['logRe'],n.ahead=1,
                          refit.every = 100,n.start = 2000,refit.window = "moving",window.size = 1000,
                          calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
  egarchFit=ugarchfit(spec = egarch,data = dfData['logRe'],solver = "solnp")
  BIC = infocriteria(egarchFit)[2]
  egarchPred = egarchRoll@forecast[["density"]][["Sigma"]]^2
  dfData[2001:len,'EGarch'] = egarchPred
  criterion['MSE','EGarch'] = MSEquant(egarchPred,benchMark)
  criterion['QLIKE','EGarch'] = QLIKEquant(egarchPred,benchMark)
  criterion['BIC','EGarch'] = BIC
  cat('EGarch done. ')
  
  ## Realized GARCH(1,1)
  for(i in volList){
    rgarch=ugarchspec(variance.model = list(model = "realGARCH", garchOrder=c(1,1)),
                      mean.model = list(armaOrder = c(1,0),include.mean=FALSE),
                      distribution.model = "std")
    rgarchRoll = ugarchroll(spec = rgarch,data = tData[,'logRe'],n.ahead=1,
                            realizedVol = tData[,i],
                            refit.every = 100,n.start = 2000,
                            refit.window = "moving",window.size = 1000,
                            calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
    regarchFit = ugarchfit(spec = rgarch,data = dfData['logRe'],realizedVol = tData[,i],solver = "solnp")
    BIC = infocriteria(regarchFit)[2]
    rgarchPred = rgarchRoll@forecast[["density"]][["Sigma"]]^2
    dfData[2001:len,paste0('RGarch_',i)] = rgarchPred
    criterion['MSE',paste0('RGarch_',i)] = MSEquant(rgarchPred,benchMark)
    criterion['QLIKE',paste0('RGarch_',i)] = QLIKEquant(rgarchPred,benchMark)
    criterion['BIC',paste0('RGarch_',i)] = BIC
  }
  cat('RGarch done. ')
  
  ## RW
  for(i in volList){
    realizedVolLag = lag(tData[,i],1)
    pred = realizedVolLag[2001:len]
    dfData[2001:len,paste0('RW_',i)] = pred
    criterion['MSE',paste0('RW_',i)] = MSEquant(pred,benchMark)
    criterion['QLIKE',paste0('RW_',i)] = QLIKEquant(pred,benchMark)
  }

  ## MA
  ma <- function(x, n = 5){filter(x, rep(1 / n, n), sides = 1)}
  for(i in volList){
    realizedVolLag = lag(tData[,i],1)
    pred = ma(realizedVolLag,5)
    pred = pred[2001:len]
    dfData[2001:len,paste0('MA_',i)] = pred
    criterion['MSE',paste0('MA_',i)] = MSEquant(pred,benchMark)
    criterion['QLIKE',paste0('MA_',i)] = QLIKEquant(pred,benchMark)
  }


  ## EW
  lambda = 0.4
  for(i in volList){
    realizedVol = tData[,i]
    pred = c()
    pred[1]=realizedVol[1]
    for(j in 2:len)
    {
      pred[j]=lambda*realizedVol[j-1]+(1-lambda)*pred[j-1]
    }
    pred = pred[2001:len]
    dfData[2001:len,paste0('EW_',i)] = pred
    criterion['MSE',paste0('EW_',i)] = MSEquant(pred,benchMark)
    criterion['QLIKE',paste0('EW_',i)] = QLIKEquant(pred,benchMark)
  }

  write.csv(dfData, file = paste0('./quantData_191030/',ticker,'_pred.csv'))
  write.csv(criterion, file = paste0('./quantData_191030/',ticker,'_criterion.csv'))
  cat(ticker,'done.\n')
}

######################################################
### data output
for(ticker in tickerList){Criterion(ticker)}


######################################################
### data process
MSE = data.frame()
QLIKE = data.frame()
BIC = data.frame()

for(ticker in tickerList){
  rawData = read.csv(paste0('./quantData_191030/',ticker,'_criterion.csv'))
  newData = rawData[2:15]
  rownames(newData) = c('MSE','QLIKE','BIC')
  tmpMSE = newData[1,]
  tmpQLIKE = newData[2,]
  tmpBIC = newData[3,]
  rownames(tmpMSE) = ticker
  rownames(tmpQLIKE) = ticker
  rownames(tmpBIC) = ticker
  MSE = rbind(MSE,tmpMSE)
  QLIKE = rbind(QLIKE,tmpQLIKE)
  BIC = rbind(BIC,tmpBIC)
}

MSE = data.frame(t(MSE))
QLIKE = data.frame(t(QLIKE))
BIC = data.frame(t(BIC))
BIC = BIC[1:5,]

# MSE, QLIKE output
write.csv(MSE, file = paste0('./quantData_191030/MSE.csv'))
write.csv(QLIKE, file = paste0('./quantData_191030/QLIKE.csv'))
write.csv(BIC, file = paste0('./quantData_191030/BIC.csv'))

modelListGarch = modelList[1:5]

MSErank = data.frame(row.names = modelList)
QLIKErank = data.frame(row.names = modelList)
BICrank = data.frame(row.names = modelListGarch)

for(ticker in tickerList){
  tmpMSE = data.frame(rank(MSE[ticker]))
  tmpQLIKE = data.frame(rank(QLIKE[ticker]))
  tmpBIC = data.frame(rank(BIC[ticker]))
  rownames(tmpMSE) = modelList
  rownames(tmpQLIKE) = modelList
  rownames(tmpBIC) = modelListGarch
  MSErank = cbind(MSErank,tmpMSE)
  QLIKErank = cbind(QLIKErank,tmpQLIKE)
  BICrank = cbind(BICrank,tmpBIC)
}

names(MSErank) = tickerList
MSEmean = data.frame(rowMeans(MSErank))
MSEmean = data.frame(rank(MSEmean))
rownames(MSEmean) = modelList
names(MSEmean) = 'mean'
MSErank = cbind(MSErank,MSEmean)

names(QLIKErank) = tickerList
QLIKEmean = data.frame(rowMeans(QLIKErank))
QLIKEmean = data.frame(rank(QLIKEmean))
rownames(QLIKEmean) = modelList
names(QLIKEmean) = 'mean'
QLIKErank = cbind(QLIKErank,QLIKEmean)

names(BICrank) = tickerList
BICmean = data.frame(rowMeans(BICrank))
BICmean = data.frame(rank(BICmean))
rownames(BICmean) = modelListGarch
names(BICmean) = 'mean'
BICrank = cbind(BICrank,BICmean)

# rank of MSE,QLIKE,BIC output
write.csv(MSErank, file = paste0('./quantData_191030/MSE_rank.csv'))
write.csv(QLIKErank, file = paste0('./quantData_191030/QLIKE_rank.csv'))
write.csv(BICrank, file = paste0('./quantData_191030/BIC_rank.csv'))

MSErankMatrix = data.matrix(MSErank)
QLIKErankMatrix = data.matrix(QLIKErank)
BICrankMatrix = data.matrix(BICrank)

MSErankMatrixReverse = MSErankMatrix[seq(dim(MSErankMatrix)[1],1),]
QLIKErankMatrixReverse = QLIKErankMatrix[seq(dim(QLIKErankMatrix)[1],1),]
BICrankMatrixReverse = BICrankMatrix[seq(dim(BICrankMatrix)[1],1),]

# postscript('./quantData_191030/Heatmap_MSE.eps')
# heatmap(MSErankMatrixReverse,Rowv = NA,Colv = NA,scale = 'column',
#         col= gray.colors(15,start = 0.1,end = 0.9),
#         main = 'Heatmap of MSE',
#         # ColSideColors = gray.colors(13,start = 0.1,end = 0.9),
#         RowSideColors = gray.colors(14,start = 0.1,end = 0.9))
# graphics.off()
# 
# postscript('./quantData_191030/Heatmap_QLIKE.eps')
# heatmap(QLIKErankMatrixReverse,Rowv = NA,Colv = NA,scale = 'column',
#         col= gray.colors(15,start = 0.1,end = 0.9),
#         main = 'Heatmap of QLIKE',
#         # ColSideColors = gray.colors(13,start = 0.1,end = 0.9),
#         RowSideColors = gray.colors(14,start = 0.1,end = 0.9))
# graphics.off()

pdf(file="./quantData_191030/Heatmap_MSE.pdf", bg="transparent")
heatmap(MSErankMatrixReverse,Rowv = NA,Colv = NA,scale = 'column',
        col= gray.colors(15,start = 0.1,end = 0.9),
        main = 'Heatmap of MSE',
        # ColSideColors = gray.colors(13,start = 0.1,end = 0.9),
        RowSideColors = gray.colors(14,start = 0.1,end = 0.9))
dev.off()

pdf(file="./quantData_191030/Heatmap_QLIKE.pdf", bg="transparent")
heatmap(QLIKErankMatrixReverse,Rowv = NA,Colv = NA,scale = 'column',
        col= gray.colors(15,start = 0.1,end = 0.9),
        main = 'Heatmap of QLIKE',
        # ColSideColors = gray.colors(13,start = 0.1,end = 0.9),
        RowSideColors = gray.colors(14,start = 0.1,end = 0.9))
dev.off()

pdf(file="./quantData_191030/Heatmap_BIC.pdf", bg="transparent",
    width = 6, height = 5)
heatmap(BICrankMatrixReverse,Rowv = NA,Colv = NA,scale = 'column',
        col= gray.colors(15,start = 0.1,end = 0.9),
        main = 'Heatmap of BIC',
        # ColSideColors = gray.colors(13,start = 0.1,end = 0.9),
        RowSideColors = gray.colors(5,start = 0.1,end = 0.9))
dev.off()

