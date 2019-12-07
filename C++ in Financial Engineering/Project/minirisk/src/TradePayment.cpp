#include "TradePayment.h"
#include "PricerPayment.h"

namespace minirisk {

ppricer_t TradePayment::pricer(const std::string&ccy_base) const
{
    return ppricer_t(new PricerPayment(*this,ccy_base));
}

} // namespace minirisk
