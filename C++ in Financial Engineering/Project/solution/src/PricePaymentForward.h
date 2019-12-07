//
// Created by zhenghaobaby on 2019/11/3.
//

#pragma once

#include "Date.h"
#include "IPricer.h"
#include "TradeFXForward.h"

namespace minirisk {

    struct PricePaymentForward : IPricer
    {
        PricePaymentForward(const TradeFXForward&trd, const string&ccy_base);



//    virtual double price(Market& m) const;
        virtual double price(Market& m, const FixingDataServer* fds) const;

    private:
        double m_amt, m_strike;
        string m_ccy1,m_ccy2,m_base_ccy;
        Date fixing_date;
        Date settle_date;

    };

} // namespace minirisk

