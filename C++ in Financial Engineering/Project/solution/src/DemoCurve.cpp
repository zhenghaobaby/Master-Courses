//
// Created by zhenghaobaby on 2019/10/25.
//
#include <CurveDiscount.h>
#include "MarketDataServer.h"
#include "ICurve.h"
#include "Market.h"
using namespace minirisk;
using namespace std;

int main(){
    Date testDate;
    string filename="risk_factors_5.txt";
    std::shared_ptr<const MarketDataServer> mds(new MarketDataServer(filename));
    Market *mr = new Market(mds,testDate);
    string curname("IR.EUR");
    CurveDiscount*cur = new CurveDiscount(mr, testDate, curname);
    cout<<cur->df(testDate);

    return 0;
}

