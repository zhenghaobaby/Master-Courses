//
// Created by zhenghaobaby on 2019/11/2.
//

#include "CurveFXForward.h"
#include "Market.h"


namespace minirisk{
    CurveFXForward::CurveFXForward(Market *mkt,
            const Date &today, const string &curve_name):
        m_today(today), m_name(curve_name){
        string base = curve_name.substr(curve_name.length()-3,3);
        string quote = curve_name.substr(curve_name.length()-7,3);
        this->spot_fx = mkt->get_spot_fx_curve(fx_spot_name(quote,base));
        this->disc_ccy1 = mkt->get_discount_curve(ir_curve_discount_name(quote));
        this->disc_ccy2 = mkt->get_discount_curve(ir_curve_discount_name(base));
    }

    double CurveFXForward::fwd(const Date &t) const {
        return spot_fx->spot()*disc_ccy1->df(t)/disc_ccy2->df(t);
    }



}// namespace minirisk
