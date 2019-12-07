//
// Created by zhenghaobaby on 2019/11/2.
//

#pragma once

#include <map>
#include "ICurve.h"

namespace minirisk {

    struct Market;

    struct CurveFXSpot : ICurveFXSpot {
        virtual string name() const { return m_name; }

        CurveFXSpot(Market *mkt, const Date &today, const string &curve_name);

        // get the fx spot
        double spot() const ;

        virtual Date today() const { return m_today; }

    private:
        Date m_today;
        string m_name;
        double m_rate;
    };
}