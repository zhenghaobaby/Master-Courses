#include "PricerPayment.h"
#include "TradePayment.h"
#include "CurveDiscount.h"
#include "CurveFXSpot.h"

namespace minirisk {

PricerPayment::PricerPayment(const TradePayment& trd,const string&ccy_base)
    : m_amt(trd.quantity())
    , m_dt(trd.delivery_date())
    , m_ir_curve(ir_curve_discount_name(trd.ccy()))
    , m_fx_ccy(fx_spot_name(trd.ccy(),ccy_base))
{
}

double PricerPayment::price(Market& mkt,const FixingDataServer* fds) const
{
    ptr_disc_curve_t disc = mkt.get_discount_curve(m_ir_curve);
    ptr_spot_fx_curve_t spot_fx_curve = mkt.get_spot_fx_curve(m_fx_ccy);

    double df = disc->df(m_dt); // this throws an exception if m_dt<today

    // This PV is expressed in m_ccy. It must be converted in USD.
//    if (!m_fx_ccy.empty())
//        df *= mkt.get_fx_spot(m_fx_ccy);

    double spot_fx = spot_fx_curve->spot();


    return m_amt * df*spot_fx;
}

} // namespace minirisk


