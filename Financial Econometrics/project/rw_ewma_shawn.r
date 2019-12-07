install.packages("tseries")
install.packages("fGarch")
install.packages("Metrics")
library(forecast)
library(timeDate)
library(timeSeries)
library(fBasics)
library(MASS)
library(fGarch)
library(tseries)
library(Metrics)
dat=read.csv("AEX.csv",header=TRUE)
attach(dat)


date1 <- as.POSIXct(paste("2001-1-1","00:00:00"))
date2 <- as.POSIXct(paste("2014-9-11","24:00:00"))
int <- interval(date1, date2)
Date=as.Date(dat$Date)
subT <- dat[Date %within% int,]

RV=ts(subT$rv5)
RVS=subT$rv5_ss
BV=subT$bv
BVS=subT$bv_ss
RK=subT$rk_parzen

T=length(subT$Date)
rt=log((subT$close_price[2:T]/subT$close_price[1:T-1]))
rt[1:length(rt)+1]=rt
rt[0]=0
roc=log(subT$open_price/subT$close_price)
ucc=sum(rt)/T
uoc=sum(roc)/T
eta=(sum((rt-ucc)^2)/T)/(sum((roc-uoc)^2)/T)

variance_RV=eta*RV
variance_RVS=eta*RVS
variance_BV=eta*BV
variance_BVS=eta*BVS
variance_RK=eta*RK


#RW
forcast_length=dim(dat)[1]-2000
RW_forcast_variance_RV=variance_RV[2000:(length(variance_RV)-1)]
RW_forcast_variance_RVS=variance_RVS[2000:(length(variance_RVS)-1)]
RW_forcast_variance_BV=variance_BV[2000:(length(variance_BV)-1)]
RW_forcast_variance_BVS=variance_BVS[2000:(length(variance_BVS)-1)]
RW_forcast_variance_RK=variance_RK[2000:(length(variance_RK)-1)]

##EW
EW_forcast_variace_RV=variance_RV[1:2000]
lamda_optimized=1:(length(variance_RV)-2000)
#for(i in (2001:(length(variance_RV)-1)))
for(i in (2001:(length(variance_RV)-1)))
{ 
  temp_min=1000
  for(lamda_estimated in seq(0.2,0.95,0.01))
  {
    for(m in (i-1999):(i-1))
    {
      EW_forcast_variace_RV[m]=lamda_estimated*variance_RV[m-1]+(1-lamda_estimated)*EW_forcast_variace_RV[m-1]
    }
    
    temp_mse=mse(variance_RV[(i-2000):(i-1)],EW_forcast_variace_RV[(i-2000):(i-1)])
    
    if(temp_mse<temp_min)
    { 
      temp_min=temp_mse
      temp_lamda=lamda_estimated
    }
  }
  EW_forcast_variace_RV[i]=temp_lamda*variance_RV[i-1]+(1-temp_lamda)*EW_forcast_variace_RV[i-1]
  lamda_optimized[i-2000]=temp_lamda
}
