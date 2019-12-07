//
// Created by zhenghaobaby on 2019/11/2.
//
#pragma once

#include <map>
#include "ICurve.h"

namespace minirisk {

    struct Market;

    struct CurveFXForward : ICurveFXForward {
        virtual string name() const { return m_name; }

        CurveFXForward(Market *mkt, const Date &today, const string &curve_name);

        // get the fx forward spot
        double fwd(const Date& t) const ;

        virtual Date today() const { return m_today; }

    private:
        Date m_today;
        string m_name;
        ptr_disc_curve_t disc_ccy1;
        ptr_disc_curve_t disc_ccy2;
        ptr_spot_fx_curve_t spot_fx;

    };
}