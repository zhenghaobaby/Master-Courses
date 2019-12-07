### 计量project

---

#### Data

- 16个国家的31个指数数据

- 文章提到了五种衡量波动率的方法，有RV，RVS，BV，BVS, RK

  其中RVS,BVS貌似原数据没找到，有可能是rv5_ss这一列，但是我发现他和rv5是一模一样的，所以不make sense。 如果能够找到return的原数据，可以自己subsample出来的这个也不难。这是一个可以优化的地方。RK统一使用rk_parzen这一列就好

#### Model

- 文章一共提到了要用六个模型

  GARCH , EGARCH, Realized GARCH,  RW, EW, MA

  GARCH 模型大家很熟悉了，这里我不多说

  EGARCH 我也没有用过，不过我觉得R有包大家可以研究下

  Realized GARCH 这个我找到package了， 你们R install.packages('rugarch') 就行，具体用法需要研究

  RW 模型，我不知道R有没有包

  EW 模型，我也不知道有没有包

  MA 模型，这个好说

- 想扩展的： 我想加上一个VAR(1)模型

#### Forecast evaluation

- **MSE  and QLIKE  loss function**， 根据论文后者会更好，因为金融对过高预测和过低预测的敏感度不同，后者会对过低预测的波动率加更大的惩罚项。
- **Diedbold-Mariano test** , 检验不同model的loss function是否有明显差异，简单来说是判定模型好坏的一个统计量。

#### 分工

- GARCH,EGARCH ---A
- Realized GARCH---B
- RW,EW---C
- MA , Diedbold-Mariano test---D
- MSE and QLIKE loss function---E

