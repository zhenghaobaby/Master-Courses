//
// Created by zhenghaobaby on 2019/11/3.
//

#include "PricePaymentForward.h"
#include <cmath>
#include "Global.h"
#include "Macros.h"



namespace minirisk{

    PricePaymentForward::PricePaymentForward(const TradeFXForward&trd, const string &ccy_base):
    m_amt(trd.quantity()),
    m_strike(trd.strike()),
    m_ccy1(trd.ccy1()),
    m_ccy2(trd.ccy2()),
    m_base_ccy(ccy_base),
    fixing_date(trd.fixing_date()),
    settle_date(trd.settle_date()){}

    double PricePaymentForward::price(Market &m, const FixingDataServer *fds) const {

        //get the discount rate in ccy2 at T2
        auto disc = m.get_discount_curve(ir_curve_discount_prefix+m_ccy2);
        double df = disc->df(settle_date);

        double forward_rate=std::numeric_limits<double>::quiet_NaN();
        if (fds && (fixing_date<m.today()||fixing_date==m.today())){  // T0>=T1, thus get data from fds
            string name = fx_spot_name(m_ccy1,m_ccy2);
            if(fixing_date<m.today()){
                forward_rate = fds->get(name,fixing_date);
            }
            else {
                auto ins = fds->lookup(name, fixing_date);
                if (ins.second)
                    forward_rate = ins.first;
                else
                {
                    auto spot_fxforward = m.get_fwd_fx_curve(fwd_spot_name(m_ccy1,m_ccy2));
                    forward_rate = spot_fxforward->fwd(fixing_date);
                }
            }
        }
        else{ //can not get from fixing ,use forwardsopt
            auto spot_fxforward = m.get_fwd_fx_curve(fwd_spot_name(m_ccy1,m_ccy2));
            forward_rate = spot_fxforward->fwd(fixing_date);
        }

        MYASSERT(!std::isnan(forward_rate), "FX forward or fixing not available "
                << m_ccy1 << m_ccy2 << " for " << fixing_date.to_string());
        MYASSERT(!std::isnan(df), "Disc factor not available "
                << m_ccy1 << m_ccy2 << " for " << settle_date.to_string());

        ptr_spot_fx_curve_t spot_fx_curve = m.get_spot_fx_curve(fx_spot_name(m_ccy2,m_base_ccy));
        double spot_fx = spot_fx_curve->spot();

        return spot_fx*df*(forward_rate-m_strike)*m_amt;
    }
}// namespace minirisk