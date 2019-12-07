//
// Created by zhenghaobaby on 2019/11/3.
//

#include "TradeFXForward.h"
#include "PricePaymentForward.h"

namespace minirisk {
    ppricer_t TradeFXForward::pricer(const std::string &ccy_base) const
    {
        return ppricer_t(new PricePaymentForward(*this,ccy_base));
    }

} // namespace minirisk
