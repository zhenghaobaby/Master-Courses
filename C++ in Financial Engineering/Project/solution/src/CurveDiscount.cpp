#include "CurveDiscount.h"
#include "Market.h"
#include "Streamer.h"
#include "algorithm"

#include <cmath>


namespace minirisk {

CurveDiscount::CurveDiscount(Market *mkt, const Date& today, const string& curve_name)
    : m_today(today)
    , m_name(curve_name)
    , m_rate(mkt->get_yield(curve_name.substr(ir_curve_discount_prefix.length(),3)))
{
}
//should consider some day has no lower_bound,or upper bound
double  CurveDiscount::df(const Date& t) const
{
    auto last_delivery = m_rate.cend();
    last_delivery--;

    Date last_tenor(m_today.serial()+last_delivery->first*365);

    double dt = time_frac(m_today, t);

//    MYASSERT((!(t < m_today)), "cannot get discount factor for date in the past: " << t);
    MYASSERT((!(t < m_today)),"Curve " << m_name << ", DF not available before anchor date " << m_today
                      << ", requested " << t);

    MYASSERT((!(dt>(last_delivery->first))),"Curve " << m_name << ", DF not available beyond last tenor date "
                                << last_tenor.to_string() << ", requested " << t)

    map<double,double>::const_iterator upper = m_rate.upper_bound(dt);
    map<double,double>::const_iterator lower = upper--;

    double local_rate = (upper->first*upper->second-lower->first*lower->second)/(upper->first-lower->first);
    return std::exp(-lower->second*lower->first-local_rate*(dt-lower->first));
}

} // namespace minirisk
