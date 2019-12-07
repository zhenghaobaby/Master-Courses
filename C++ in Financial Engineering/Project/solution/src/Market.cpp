#include "Market.h"
#include "CurveDiscount.h"
#include "CurveFXSpot.h"
#include "CurveFXForward.h"
#include "MarketDataServer.h"
#include <string>

#include <vector>

namespace minirisk {

template <typename I, typename T>
std::shared_ptr<const I> Market::get_curve(const string& name)
{
    ptr_curve_t& curve_ptr = m_curves[name];
    if (!curve_ptr.get())
        curve_ptr.reset(new T(this, m_today, name));
    std::shared_ptr<const I> res = std::dynamic_pointer_cast<const I>(curve_ptr);
    MYASSERT(res, "Cannot cast object with name " << name << " to type " << typeid(I).name());
    return res;
}

const ptr_disc_curve_t Market::get_discount_curve(const string& name)
{
    return get_curve<ICurveDiscount, CurveDiscount>(name);
}

const ptr_spot_fx_curve_t Market::get_spot_fx_curve(const string &name) {
    return get_curve<ICurveFXSpot,CurveFXSpot>(name);
}

const ptr_fwd_fx_curve_t Market::get_fwd_fx_curve(const string &name){
    return get_curve<ICurveFXForward,CurveFXForward>(name);
}


double Market::from_mds(const string& objtype, const string& name)
{
    auto ins = m_risk_factors.emplace(name, std::numeric_limits<double>::quiet_NaN());
    if (ins.second) { // just inserted, need to be populated
        MYASSERT(m_mds, "Cannot fetch " << objtype << " " << name << " because the market data server has been disconnnected");
        ins.first->second = m_mds->get(name);
    }
    return ins.first->second;
}
//vector<doule,double>//
//const double Market::get_yield(const string& ccyname)
std::map<double,double> Market::get_yield(const string& ccyname)
{
    std::vector<std::pair<string, double>> matched;
    string forward_time;
    double base = 365.0;
    double factor,index;
    std::map<double,double> result;

    std::string regex = ir_rate_prefix + "[0-9]+(D|W|M|Y)\\." + ccyname;
    if(!this->m_mds.get())
        matched = this->get_risk_factors(regex);

    else {
        matched = m_mds->match(regex);
    }

    for(const auto&p:matched){
        std::string::size_type nPos1 = std::string::npos;
        std::string::size_type nPos2 = std::string::npos;
        nPos1 = p.first.find_last_of(".");
        nPos2 = p.first.find_last_of(".", nPos1 - 1);
        if(nPos1 !=-1 && nPos2 != -1){
            forward_time = p.first.substr(nPos2 + 1, nPos1 - nPos2 - 1);
        }
        if(forward_time.back()=='Y')
            factor = 365.0;
        else if (forward_time.back()=='M')
            factor = 30.0;
        else if (forward_time.back()=='W')
            factor = 7.0;
        index = std::atof(forward_time.substr(0,forward_time.length()-1).c_str())*factor/base;
        result.emplace(index,from_mds("yield curve",p.first));
    }
    result.emplace(0.0,0.0);
    return result;

//    string name(ir_rate_prefix + ccyname);
//    return from_mds("yield curve", name);
};

const double Market::get_fx_spot(const string& name)
{
    string base = name.substr(name.length()-3,3);
    string quote = name.substr(name.length()-7,3);

    if(base=="USD"){
        if(quote=="USD")
            return 1.0;
        else
            return from_mds("fx spot",mds_spot_name(name));
    }
    else if(quote=="USD"){
        return 1.0/from_mds("fx spot",fx_spot_prefix+base);
    }

    else{
        double base_rate = from_mds("fx spot",fx_spot_prefix+base);
        double quote_rate = from_mds("fx spot",fx_spot_prefix+quote);
        return quote_rate/base_rate;
    }
}

void Market::set_risk_factors(const vec_risk_factor_t& risk_factors)
{
    clear();
    for (const auto& d : risk_factors) {
        auto i = m_risk_factors.find(d.first);
        MYASSERT((i != m_risk_factors.end()), "Risk factor not found " << d.first);
        i->second = d.second;
    }
}

Market::vec_risk_factor_t Market::get_risk_factors(const std::string& expr) const
{
    vec_risk_factor_t result;
    std::regex r(expr);
    for (const auto& d : m_risk_factors)
        if (std::regex_match(d.first, r))
            result.push_back(d);
    return result;
}



} // namespace minirisk
