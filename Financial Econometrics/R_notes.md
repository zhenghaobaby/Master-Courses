## R_notes

[TOC]

### normal distribution

- dnorm-density. 密度函数

- pnorm-Probability. 分布函数，如果lower.tail 设置为FALSE，那么pnorm()函数返回的积分是q到正无穷

- qnorm, 是CDF的反函数，即pnorm的反函数，分位数函数。即给出z-score值后找出对应的分位数。

  ![](1.png)

- rnorm, 随机生产一系列的正态分布函数
- qqnorm: 即假设给的样本是正态分布，求出一个递增的Z-score，使用qnorm求出其分位数后与样本作图，如果近似满足线性关系，那可以说样本满足正态分布

### halfnorm

- 检测异常值，偏离过大的那种，具体用法如下

  ```R
  halfnorm(abs(diffdm), main="changes in DM/dollar exchange rate",ylab="Sorted data",nlab = 3)
  ```


### shapiro-check

- 同样检测数据是否满足正态分布，返回P值。原理是检查y值与一个正太分布的x的相关性，相关性高就可以，相关性低的话，拒绝原假设，不是正态分布

- 关于正态分布的检测方法，**一个是shapiro-check，一个是qqnorm方法，看是否满足线性关系**，qt是t分布的分位数分布，用于检测小样本的正态分布，**qqplot与qqnorm**类似，你也可以指定对应的分位数分布。

  ```R
  shapiro.test(x)
  ```

### Mad

- R 里面的一种中性化方法，不是均值方差中性化：

  ```R
  xls = (x1-median(x1))/mad(x1)
  ```

### plot

- ```
  plot(x,y,xlab=,ylab=,main=)
  ```

### density

- 消除偏度的数据，使数据更为对称
  $$
  y^{(a)}=\lbrace^{\frac{y^a-1}{a}\quad a>0}_{log(a)\quad a=0}
  $$

  $$
  当数据左偏，a>1, 数据右偏，a<1
  $$

  ```R
  plot(density((x1^2-1)/2),main=expression(alpha == 2) )
  
  ```

### pdf

- 将画图结果保存到pdf

  ```R
  pdf("EuStocks.pdf",width=6,height=5)
  plot(EuStockMarkets)
  graphics.off()
  ```


### Time Series 

- ACF，acf(vector), you can use as.vector to transform

- Ljung-Box-TEST:Box.test(diff(y), lag = 10, type = "Ljung-Box")

### cut and delete
```
> x
[1]  7 10  4  8  3
> x[-2]
[1] 7 4 8 3
上面为删除第二个元素，那么如果要删除一个子集该如何做呢，如下：
> x[-(2:4)]
[1] 7 3
```

### tapply

```
##分类统计
但是如果我们想得到每个日期标签的分类均值怎么办呢，方法当然是有的，并且很方便如下：
> tapply(y,names(y),mean)
      fir      mon       thu       tue      wen 
 3.98501910.356011 10.739871  7.121114  6.880396
```

### 运算符%in%

```
当我们有一个子集，想要知道你子集中的元素是否在你的目标集合中包含的时候该如何做呢，如下：
> c(10,5) %in% x_numeric
```

### min and pmin

```R
现在我们得到了三个数字类型得向量，我们希望找到每个向量第一个维度的值里面得最小值，和最大值怎么办呢
> pmin(x,y,z)
[1]35 43  3 4 35 27 11
> pmax(x,y,z)
[1] 70 99 41 66 86 90 64

方法二：
> apply(rbind(x,y,z),2,min)
[1] 35 43  3  4 35 27 11
这里这个rbind是行合并，也有cbind，你懂我意思吧
```

### Matrix

```
从数组创建
x = sample(1:100,16)
m = matrix(x)
改变维度：
dim(m)=c(4,4)
也可以创建时直接指定
m = martix(x,4,4)
改成按照行来采集数据
m = matrix(x,4,4,byrow=True)
矩阵乘法
%*%
矩阵转置
t(m)
解矩阵m1 %*% X = m2
> solve(m1,m2)
特征值和特征向量
> res <- eigen(m1)
该函数返回一个list，第一个元素为values即特征值，第二个元素为vectors即特征向量
```

### Array

```R
> a <- array(1:30,c(2,5,3))
后面的这个是维度
```

### DataFrame

```R
##创建
df.data <-data.frame(matrix(sample(1:20,16),c(4,4))) 
##或者直接创建
df.web <- data.frame(date = c('20150301','20150302','20150303','20150304'),pv=c(10234,20119,9087,15899),times=c(30.98,20.09,22.98,40.09))
##行名列名的查看
row.names()
colnames()
names()
##条件索引
 subset(df.web,pv>10000&pv<20000,c(times,pv))

```

### TimeSeries

```R
##创建时间序列
t <-ts(data[1:16],frequency=4,start=c(2006))
frequency代表是年度，还是季度，还是月度
##分解
plot(decompose(t))
```

### Rlab summary

- Rlab2

  ```R
  ##画出一系列散点图矩阵，可以看相关性
  pairs(cbind(x,y,z))
  ##查看置信区间值
  confint(fitmodel)
  ##Compute analysis of variance (or deviance) tables for one or more fitted model objects.
  ???????anova(fitmodel) ???sum sq???
  ##逐一减少变量，使用stepAIC
  library(MASS)
  fitLm2 = stepAIC(fitLm1)
  summary(fitLm2)
  ## Partial residual plots
  library(car)
  crPlot(model,variable)
  ## 看least-square lines和lowess curves的关系，如果说基本都horizon那么不显著，如果说curve和lines重合度很好并且lines有斜率，那么说明该变量影响时线性的。
  ```

- Rlab2_2

  ```R
  ##学生化残差或者标准化残差
  rstudent(model)
  rstandard(model)
  ##生成fit后序列
  model$fit
  ##画出每个点的残差图
  plot(model$fit,rstudent(model)) ????检查异方差性吗，还会做qqnorm和qqline。一般abs之后更好观察
  ##画出一个自变量与model的残差图,如果说我们对于该自变量的次幂选择正确，那么画出来的lowess应该时一条基本线性的线，但是如果存在弯曲，说明他的影响不是线性，可能是二次或者三次。
  plot(v1,rstudent(model)) 
  ？？？为何fit后有两个值——已经想通给，别人是二次多项式老哥
  
  
  ```

- Rlab3

  ```R
  ##求矩阵每一列或者行的某个性质,参数上1是行，2是列，这里需要掌握，前面也可也cbind或者rbind
  apply(matrix,2,mean)
  ##what percentage of the y variance is due the x?
  model = lm(y~x)
  summary(model)
  看R-suqared值
  ```

- Rlab5

  ```R
  ##预测的写法
  forecasts = predict(model,36)
  plot(pi,xlim=c(1980,2006),ylim=c(-7,12))
  lines(seq(from=1997,by=.25,length=36), forecasts$pred,col="red")
  lines(seq(from=1997,by=.25,length=36), forecasts$pred + 1.96*forecasts$se,
     col="blue")
  lines(seq(from=1997,by=.25,length=36), forecasts$pred - 1.96*forecasts$se,
     col="blue")
  ##auto arima是默认截距为零的。
  ##problem 7?第二问还是有点疑问？？？？？？
  ```

- Rlab6

  ```R
  ##计算概率，使用Pstd
  forecast = predict(results,n.ahead=1)
  probBlackMonday =pstd(returnBlMon,mean=forecast$meanForecast,sd=forecast$standardDeviation,nu=dfhat)
  round(probBlackMonday,7)
  ###option(digit=3) 这个什么意思？？？
```
  
- 一步预测方法的滚动模型函数

  ```R
  pred1 <- function(y=Gtemp, n.pred=200){
    T <- length(y)
    ypred <- rep(NA_real_, T)
    for(h in (T-n.pred):(T-1)){
      mod <- arima(y[1:h], order=c(1,1,2), 
               seasonal=list(order=c(0,0,2), period=12),
               fixed=c(NA, NA, NA, 0, NA))
      ypred[h+1] <- predict(mod, n.ahead=1, se.fit=FALSE)
    }
    
    ypred
  }
  ```

  

- 画出上下界限和均值的函数

  ```R
  pred.long1 <- function(y=Gtemp, n.pred=1200){
    T <- length(y)
    ypred <- ts(c(y, rep(NA_real_, n.pred)), 
                start=start(y), frequency = frequency(y))
    ntotal <- T + n.pred
    lb <- ts(rep(NA_real_, ntotal), 
             start=start(y), frequency = frequency(y))
    ub <- lb
    mod <- arima(
      y, order=c(1,1,2), 
      seasonal=list(order=c(0,0,2), period=12),
      fixed=c(NA, NA, NA, 0, NA))
    ypred0 <- predict(mod, n.ahead=n.pred, se.fit=TRUE)
    ypred[(T+1):(T+n.pred)] <- ypred0$pred
    lb[(T+1):(T+n.pred)] <- ypred0$pred - 2*ypred0$se
    ub[(T+1):(T+n.pred)] <- ypred0$pred + 2*ypred0$se
  
    list(pred=ypred, lb=lb, ub=ub)
  }
  
  plot.pred <- function(y=Gtemp, pred.long=pred.long1, n.pred=1200){
    ypred <- pred.long(y=Gtemp, n.pred=1200)
    ylim <- range(c(ypred$pred, ypred$lb, ypred$ub), na.rm=TRUE)
    times <- c(time(ypred$pred))
    plot(times, ypred$pred, type="l", xlab="year", ylab="Forcast",
         ylim=ylim)
    t1 <- length(y)+1
    t2 <- length(ypred$pred)
    lines(times[t1:t2], ypred$pred[t1:t2], col="red")
    lines(times[t1:t2], ypred$lb[t1:t2], lty=2, col="blue")
    lines(times[t1:t2], ypred$ub[t1:t2], lty=2, col="blue")
  }
  
  
  plot.pred(y=Gtemp, pred.long=pred.long1, n.pred=1200)
  ```

  

