library(tseries)
library(forecast)
library(rugarch)
library(forecast)
library(xts)

#Date	Symbol	rv5_ss	open_time	rk_twoscale	nobs	close_price	bv_ss	rv10	open_price	
#bv	close_time	rv5	rsv_ss	medrv	rsv	open_to_close	rk_th2	rv10_ss	rk_parzen


## Data_processing
data = read.csv('.AEX.csv')
Date = data$Date
Date = as.POSIXlt(Date)

outDate = Date[2002:length(Date)]

## get the data you want
get_data = function(columnindex,columnname){
  temp = data[,columnindex]
  temp = data.frame(temp)
  rownames(temp) = Date
  result = as.xts(temp)
  colnames(result)=columnname
  return(result)
}

## get data we need 
close_price = get_data(7,'close_price')
rvs = get_data(3,'rvs')
bvs = get_data(8,'bvs')
rk = get_data(20,'rk')
open_to_close = get_data(17,'open_close')


diff_close = diff(close_price)
close_ = lag(close_price,1)
close_ = close_[-1]
close_to_close = diff_close[-1]/close_ ##close_to_close return 
logret = log(1+close_to_close)

length(close_)
length(open_to_close)

###transfer close-close to open-close
uoc = sum(log(open_to_close+1))/length(close_price)
ucc = sum(log(close_to_close+1))/length(close_)
transfer_factor = (1/length(close_)*sum((log(close_to_close+1)-ucc)^2))/
  (1/length(open_to_close)*sum((log(open_to_close+1)-uoc)^2))
cc_rvs = transfer_factor*rvs
cc_bvs = transfer_factor*bvs
cc_rk = transfer_factor*rk


###stationary test
adf.test(logret)
kpss.test(logret)
acf(logret)
acf(logret^2)  #garch effect obvious


### Model 
benchmark = as.numeric(cc_rk)
benchmark = benchmark[2002:length(benchmark)]
rk_out = cc_rk[2002:length(cc_rk)]

MSE = rep(c(0),14)
QLIKE = rep(c(0),14)

##GRARCH(1,1)
garch=ugarchspec(variance.model = list(model = "sGARCH", garchOrder=c(1,1)), #波动方程
                 mean.model = list(armaOrder = c(1,0)), #均值方程
                 distribution.model = "norm")
garchfit=ugarchfit(spec=garch,data=logret,solver = "solnp")
garchfit
plot(garchfit)
qqnorm(residuals(garchfit))
BIC = infocriteria(garchfit)[2]# 这个可以BIC存储下来

garchroll = ugarchroll(spec = garch,data = logret,n.ahead=1,
                       refit.every = 100,n.start = 2000,refit.window = "moving",window.size = 1000,
                           calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
#plot(garchroll)
garch_pred = garchroll@forecast[["density"]][["Sigma"]]^2
garch_pred = data.frame(garch_pred)
rownames(garch_pred) = outDate
garch_pred = as.xts(garch_pred)
colnames(garch_pred) = 'GARCH'
a = merge(rk_out,garch_pred)

#plot(benchmark,main='GARCH',type='l',lwd=0.5,xlab='time index',ylab='Volativity')
#lines(garch_pred,col='red')
MSE[1] = mean((garch_pred-benchmark)^2)
QLIKE[1] = mean(log(garch_pred)+benchmark/garch_pred)


##EGARCH(1,1)
egarch=ugarchspec(variance.model = list(model = "eGARCH", garchOrder=c(1,1)), #波动方程
                  mean.model = list(armaOrder = c(1,0)), #均值方程
                  distribution.model = "std")
#egarchfit=ugarchfit(spec=egarch,data=logret,solver = "solnp")
egarchroll = ugarchroll(spec = egarch,data = logret,n.ahead=1,
                       refit.every = 100,n.start = 2000,refit.window = "moving",window.size = 1000,
                       calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
plot(egarchroll,main='EGARCH')
egarch_pred = egarchroll@forecast[["density"]][["Sigma"]]^2
egarch_pred = data.frame(egarch_pred)
rownames(egarch_pred) = outDate
egarch_pred = as.xts(egarch_pred)
colnames(egarch_pred) = 'EGARCH'
a = merge(a,egarch_pred)




MSE[2] = mean((egarch_pred-benchmark)^2)
QLIKE[2] = mean(log(egarch_pred)+benchmark/egarch_pred)


realgarch=ugarchspec(variance.model = list(model = "realGARCH", garchOrder=c(1,1)),
                     mean.model = list(armaOrder = c(1,0),include.mean=FALSE),	distribution.model = "std")
rgarchfit=ugarchfit(spec=realgarch,data=logret,solver = "solnp",realizedVol=cc_rvs[-1])
rgarchfit 



##Realized GARCH(1,1) function
Realized_GARCH = function(realize_vol,name){
  realgarch=ugarchspec(variance.model = list(model = "realGARCH", garchOrder=c(1,1)),
                       mean.model = list(armaOrder = c(1,0),include.mean=FALSE),	distribution.model = "std")
  rgarchfit=ugarchfit(spec=realgarch,data=logret,solver = "solnp",realizedvol=realize_vol)
  rgarchfit 
  regarchroll = ugarchroll(spec = realgarch,data = logret,n.ahead=1,realizedVol = realize_vol,
                               refit.every = 100,n.start = 2000,refit.window = "moving",window.size = 1000,
                               calculate.VaR = TRUE, VaR.alpha = c(0.05, 0.01))
  regarchroll_pred = regarchroll@forecast[["density"]][["Sigma"]]^2
  regarchroll_pred = data.frame(regarchroll_pred)
  rownames(regarchroll_pred) = outDate
  regarchroll_pred = as.xts(regarchroll_pred)
  colnames(regarchroll_pred) = name
  rgarchfit=ugarchfit(spec=realgarch,data=logret,solver = "solnp",realizedvol=realize_vol)
  rgarchfit 
  #MSE= mean((regarchroll_pred-benchmark)^2)
  #QLIKE = mean(log(regarchroll_pred)+benchmark/regarchroll_pred)
  #return(c(MSE,QLIKE))
  return(regarchroll_pred)
}
##Realized GARCH(1,1)-RVS
output=Realized_GARCH(cc_rvs[-1],'RGRACH_RVS')
a = merge(a,output)

#MSE[3] = output[1]
#QLIKE[3]=output[2]

output = Realized_GARCH(cc_bvs[-1],'RGRACH_BVS')
a = merge(a,output)

#MSE[4] = output[1]
#QLIKE[4]= output[2]

output = Realized_GARCH(cc_rk[-1],'RGRACH_RK')
a = merge(a,output)


MSE[5] = output[1]
QLIKE[5] = output[2]

## RW
RW = function(realized_vol){
  realized_vol = realized_vol[2001:length(realized_vol)]
  pred = lag(realized_vol,1)
  MSE = mean(sum(benchmark-pred[-1])^2)
  QLIKE = mean(log(pred)+benchmark/pred[-1])
  return(c(MSE,QLIKE))
}
output = RW(cc_rvs)
MSE[6] = output[1]
QLIKE[6] = output[2]

output = RW(cc_bvs)
MSE[7] = output[1]
QLIKE[7] = output[2]

output = RW(cc_rk)
MSE[8] = output[1]
QLIKE[8] = output[2]



## MA
MA = function(realized_vol){
  realized_vol = realized_vol[1997:length(realized_vol)]
  for(i in 1:length(benchmark))
  {
    pred[i]=mean(realized_vol[i:i+4])
  }
  MSE = mean(sum(benchmark-pred)^2)
  QLIKE = mean(log(pred)+benchmark/pred)
  return(c(MSE,QLIKE))
}
output = RW(cc_rvs)
MSE[9] = output[1]
QLIKE[9] = output[2]

output = RW(cc_bvs)
MSE[10] = output[1]
QLIKE[10] = output[2]

output = RW(cc_rk)
MSE[11] = output[1]
QLIKE[11] = output[2]

## EW
LAMBDA_OPTIMIZED=0.4
EW = function(realized_vol){
  realized_vol = realized_vol[2001:length(realized_vol)]
  pred[1]=realized_vol[1]
  for(i in 2:length(benchmark))
  {
    pred[i]=LAMBDA_OPTIMIZED*realized_vol[i]+(1-LAMBDA_OPTIMIZED)*pred[i-1]
  }
  MSE = mean(sum(benchmark-pred)^2)
  QLIKE = mean(log(pred)+benchmark/pred)
  return(c(MSE,QLIKE))
}
output = RW(cc_rvs)
MSE[12] = output[1]
QLIKE[12] = output[2]

output = RW(cc_bvs)
MSE[13] = output[1]
QLIKE[13] = output[2]

output = RW(cc_rk)
MSE[14] = output[1]
QLIKE[14] = output[2]



### ouput

result = data.frame(
  ID=c('GARCH','EGARCH','RG-RVS','RG-BVS','RG-RK',
       'EW-RVS','EW-BVS','EW-RK','RW-RVS','RW-RVS',
       'RW-RK','MA-RVS','MA-BVS','MA-RK'),
  MSE = MSE,
  QLIKE = QLIKE,
  Residual = rep(c(0),14)
)




output = data.frame(
  ID=
)


write.csv(a,file='C:/Users/zhenghaobaby/Desktop/Forecast.csv',row.names =outDate)














