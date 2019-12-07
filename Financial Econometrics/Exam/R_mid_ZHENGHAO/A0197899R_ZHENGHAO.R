library(fGarch)
library(tseries)
library(ggplot2)
library(scales)
library(forecast)
library(car)
library(MASS)
##Q1
data = read.table("A0197899R.csv", sep="\t", header=FALSE)
data_1 = data[,2]
data_1 = ts(data_1,frequency = frequency(data))
par(mfrow=c(1,2))
plot(data_1)
acf(data_1)
adf.test(data_1)
kpss.test(data_1)

data_1_diff = diff(data_1)
par(mfrow=c(1,1))
plot(data_1_diff)
adf.test(data_1_diff)
kpss.test(data_1_diff)

##1.2
par(mfrow=c(1,2))
acf(data_1_diff)
pacf(data_1_diff)
fit_1 = arima(data_1_diff,order=c(0,0,1))
summary(fit_1)
acf(residuals(fit_1))
acf(residuals(fit_1)^2)
##garchfit_choose model
gfit_1 = garchFit(~arma(0,1)+garch(1,1),data=data_1_diff)
gfit_2 = garchFit(~arma(1,0)+garch(1,1),data=data_1_diff)
gfit_3 = garchFit(~arma(1,1)+garch(1,1),data=data_1_diff)
summary(gfit_1)
summary(gfit_2)
summary(gfit_3)
###gfit_3 is used,we then consider the residuals
par(mfrow=c(1,2))
res_std = residuals(gfit_3)/gfit_3@sigma.t
n = length(data_1_diff)
grid = (1:n)/(n+1)

qqnorm(res_std,datax = T,ylab= "Standardized residual quantiles", 
       main="(a) normal plot",xlab="normal quantiles")
qqline(res_std,datax=T)
qqplot(sort(res_std), qt(grid,df=4),
       main="(b) t plot, df=4",xlab= "Standardized residual quantiles",
       ylab="t-quantiles")
abline(   lm(   qt(c(.25,.75),df=4)~quantile(res_std,c(.25,.75))   )   )
###Thus we change the distrbution assumption
gfit_4 = garchFit(~arma(1,1)+garch(1,1),data=data_1_diff,cond.dist = 'std')
summary(gfit_4)

##Q2
data_2 = data[,3]
data_2 = ts(data_2)
par(mfrow=c(1,2))
plot(data_2)
acf(data_2)
adf.test(data_2)
kpss.test(data_2)
auto.arima(data_2)
fit_2 = arima(data_2,order=c(1,0,4))
acf(residuals(fit_2))
acf(residuals(fit_2)^2) ## have garch effect

fit_2_g = garchFit(~arma(1,4)+garch(1,1),data=data_2)
res_std_2 = residuals(fit_2_g)/fit_2_g@sigma.t
acf(res_std_2)
acf(res_std_2^2)
summary(fit_2_g)

forecast = predict(fit_2_g,n.ahead=2)
interval_low = forecast$meanForecast-1.96*forecast$standardDeviation
interval_high = forecast$meanForecast+1.96*forecast$standardDeviation
interval_1 = c(interval_low[1],interval_high[1])
interval_2 = c(interval_low[2],interval_high[2])
interval_1
interval_2


##Q3
data_3 = read.table("d-cdsALL.txt", sep="", header=FALSE)
dim(data_3)
data_3 = data_3$V2
data_3 = data_3[-1]
data_3 = as.vector(data_3)
data_3 = as.numeric(data_3)
data_3 = data_3*100
data_3_diff = diff(data_3)
plot(data_3_diff)

auto.arima(data_3_diff)
fit_3 = arima(data_3_diff,order=c(5,0,5))
acf(residuals(fit_3))
acf(residuals(fit_3)^2)##garch effects
fit_3_g = garchFit(~arma(5,5)+garch(1,1),data=data_3_diff)
summary(fit_3_g)

library(faraway)
halfnorm(abs(data_3_diff),nlab=4)
data_3_diff_mend = data_3_diff
data_3_diff_mend[c(1257,1254,1240,1275)]=0
auto.arima(data_3_diff_mend)
fit_3_1 = arima(data_3_diff_mend,order=c(0,0,5))
acf(residuals(fit_3_1))
acf(residuals(fit_3_1)^2) ##garch effects
fit_3_g_mend = garchFit(~arma(0,5)+garch(1,1),data=data_3_diff_mend)
summary(fit_3_g_mend)

at = residuals(fit_3_g)
acf(at)
Box.test(at,lag=10,type="Ljung-Box")

at_std = residuals(fit_3_g)/fit_3_g@sigma.t
acf(at_std)
Box.test(at_std,lag=10,type="Ljung-Box")


