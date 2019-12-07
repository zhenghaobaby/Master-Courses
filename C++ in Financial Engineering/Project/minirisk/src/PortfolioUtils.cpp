#include "Global.h"
#include "PortfolioUtils.h"
#include "TradePayment.h"
#include "TradeFXForward.h"

#include <numeric>
#include <cmath>
#include <set>
using namespace std;


namespace minirisk {

void bump_risk_factors(const double bump_size,
                       std::vector<std::pair<std::string, double>>*bump_up,
                       std::vector<std::pair<std::string, double>>*bump_dn) {
    for (auto& p : *bump_up) {
        p.second += bump_size;
    }
    for (auto& p : *bump_dn) {
        p.second -= bump_size;
    }
}

std::pair<double,string> is_pv01_nan(std::pair<double,string>&hi,
        std::pair<double,string>&lo,double dr){
    if(std::isnan(hi.first))
        return std::make_pair(NAN_d,hi.second);
    if(std::isnan(lo.first))
        return std::make_pair(NAN_d,lo.second);
    return std::make_pair((hi.first-lo.first)/dr,"");
}


void print_portfolio(const portfolio_t& portfolio)
{
    std::for_each(portfolio.begin(), portfolio.end(), [](auto& pt){ pt->print(std::cout); });
}

std::vector<ppricer_t> get_pricers(const portfolio_t& portfolio,const std::string&ccy_base)
{
    std::vector<ppricer_t> pricers(portfolio.size());
    std::transform( portfolio.begin(), portfolio.end(), pricers.begin()
                  , [ccy_base](auto &pt) -> ppricer_t { return pt->pricer(ccy_base); } );
    return pricers;
}

portfolio_values_t compute_prices(const std::vector<ppricer_t>& pricers, Market& mkt,std::shared_ptr<const FixingDataServer> fds)
{
    portfolio_values_t prices;

    for(auto&pr:pricers){
        try{
            prices.push_back(std::make_pair(pr->price(mkt,fds.get()),""));
        }catch (std::exception&e) {
            prices.push_back(std::make_pair(NAN_d, e.what()));
        }
    }
    return prices;
}

pair<double,std::vector<std::pair<size_t,string>>> portfolio_total(const portfolio_values_t& values)
{
    double total = 0.0;
    std::vector<std::pair<size_t, std::string>> errors;

    for (int i = 0; i < values.size(); ++i) {
        const auto& value = values[i];
        if (std::isnan(value.first)) {
            errors.push_back(std::make_pair(i, value.second));
        } else {
            total += value.first;
        }
    }
    return std::make_pair(total, errors);
}

std::vector<std::pair<string,portfolio_values_t>> PV01Parallel(const std::vector<ppricer_t>& pricers, const Market& mkt,
                                                               std::shared_ptr<const FixingDataServer> fds){
    std::vector<std::pair<string, portfolio_values_t>> pv01;  // PV01 per trade
    std::vector<std::pair<double,string>> pv_up, pv_dn;
    const double bump_size = 0.01 / 100;

    std::set<string> ccyname;
    auto base = mkt.get_risk_factors(ir_rate_prefix + "[0-9]+(D|W|M|Y)\\.[A-Z]{3}");
    for(const auto&rf: base){
        string ccy_ = rf.first.substr(rf.first.length()-3);
        ccyname.insert(ccy_);
    }

    Market tmpmarket(mkt);
    for(const auto&ccy_:ccyname){
        auto base = mkt.get_risk_factors(ir_rate_prefix + "[0-9]+(D|W|M|Y)\\."+ccy_);
        std::vector<std::pair<std::string, double>>bump_up(base);
        std::vector<std::pair<std::string, double>>bump_dn(base);
        bump_risk_factors(bump_size,&bump_up,&bump_dn);
        tmpmarket.set_risk_factors(bump_up);
        pv_up = compute_prices(pricers,tmpmarket,fds);
        tmpmarket.set_risk_factors(bump_dn);
        pv_dn = compute_prices(pricers,tmpmarket,fds);

        tmpmarket.set_risk_factors(base); // stote the original bump

        pv01.push_back(std::make_pair("parallel " + ir_rate_prefix + ccy_,
                                      std::vector<std::pair<double,string>>(pricers.size())));

        double dr = 2.0 * bump_size;
        std::transform(pv_up.begin(), pv_up.end(), pv_dn.begin(), pv01.back().second.begin()
                , [dr](auto&hi, auto&lo) -> std::pair<double,string>{ return is_pv01_nan(hi,lo,dr); });

    }
    return pv01;

}


std::vector<std::pair<string,portfolio_values_t>> PV01Bucketed(const std::vector<ppricer_t>& pricers, const Market& mkt,
                                                               std::shared_ptr<const FixingDataServer> fds){
    std::vector<std::pair<string, portfolio_values_t>> pv01;  // PV01 per trade
    const double bump_size = 0.01 / 100;
    // filter risk factors related to IR
    auto base = mkt.get_risk_factors(ir_rate_prefix + "[0-9]+(D|W|M|Y)\\.[A-Z]{3}");
    // Make a local copy of the Market object, because we will modify it applying bumps
    // Note that the actual market objects a
    // re shared, as they are referred to via pointers
    Market tmpmkt(mkt);

    for (const auto& rf : base) {
        std::vector<std::pair<double,string>> pv_up, pv_dn;
        std::vector<std::pair<string, double>> bumped(1, rf);
        pv01.push_back(std::make_pair(rf.first, std::vector<std::pair<double,string>>(pricers.size())));

        // bump down and price
        bumped[0].second = rf.second - bump_size;
        tmpmkt.set_risk_factors(bumped);
        pv_dn = compute_prices(pricers, tmpmkt,fds);

        // bump up and price
        bumped[0].second = rf.second + bump_size;
        tmpmkt.set_risk_factors(bumped);
        pv_up = compute_prices(pricers, tmpmkt,fds);


        // restore original market state for next iteration
        // (more efficient than creating a new copy of the market at every iteration)
        bumped[0].second = rf.second;
        tmpmkt.set_risk_factors(bumped);

        // compute estimator of the derivative via central finite differences
        double dr = 2.0 * bump_size;
        std::transform(pv_up.begin(), pv_up.end(), pv_dn.begin(), pv01.back().second.begin()
                , [dr](auto&hi, auto&lo) -> std::pair<double,string>{ return is_pv01_nan(hi,lo,dr); });
    }
    return pv01;
}


std::vector<std::pair<string,portfolio_values_t>> fx_delta(const std::vector<ppricer_t>& pricers,const Market&mkt,
                                                           std::shared_ptr<const FixingDataServer> fds){
    std::vector<std::pair<string, portfolio_values_t>> delta;  // delta per trade

    // filter risk factors related to fx
    auto fx_spot = mkt.get_risk_factors(fx_spot_prefix + "[A-Z]{3}");
    Market tmpmkt(mkt);


    for (const auto& fp : fx_spot) {
        std::vector<std::pair<double,string>> pv_up, pv_dn;
        std::vector<std::pair<string, double>> bumped(1, fp);
        delta.push_back(std::make_pair(fp.first, std::vector<std::pair<double,string>>(pricers.size())));

        // bump down and price
        const double bump_size = bumped[0].second*0.1/100;
        bumped[0].second = fp.second - bump_size;
        tmpmkt.set_risk_factors(bumped);
        pv_dn = compute_prices(pricers, tmpmkt,fds);

        // bump up and price
        bumped[0].second = fp.second + bump_size;
        tmpmkt.set_risk_factors(bumped);
        pv_up = compute_prices(pricers, tmpmkt,fds);


        // restore original market state for next iteration
        // (more efficient than creating a new copy of the market at every iteration)
        bumped[0].second = fp.second;
        tmpmkt.set_risk_factors(bumped);

        // compute estimator of the derivative via central finite differences
        double dr = 2.0 * bump_size;
        std::transform(pv_up.begin(), pv_up.end(), pv_dn.begin(), delta.back().second.begin()
                , [dr](auto&hi, auto&lo) -> std::pair<double,string>{ return is_pv01_nan(hi,lo,dr); });
    }
    return delta;
}




ptrade_t load_trade(my_ifstream& is)
{
    string name;
    ptrade_t p;

    // read trade identifier
    guid_t id;
    is >> id;

    if (id == TradePayment::m_id)
        p.reset(new TradePayment);
    else if(id == TradeFXForward::m_id)
        p.reset(new TradeFXForward);
    else
        THROW("Unknown trade type:" << id);


    p->load(is);

    return p;
}

void save_portfolio(const string& filename, const std::vector<ptrade_t>& portfolio)
{
    // test saving to file
    my_ofstream of(filename);
    for( const auto& pt : portfolio) {
        pt->save(of);
        of.endl();
    }
    of.close();
}

std::vector<ptrade_t> load_portfolio(const string& filename)
{
    std::vector<ptrade_t> portfolio;

    // test reloading the portfolio
    my_ifstream is(filename);
    while (is.read_line())
        portfolio.push_back(load_trade(is));

    return portfolio;
}

void print_price_vector(const string& name, const portfolio_values_t& values)
{
    const auto& output = portfolio_total(values);
    std::cout
        << "========================\n"
        << name << ":\n"
        << "========================\n"
        << "Total: " << output.first<<"\n"
        << "Errors: "<< output.second.size()<<"\n"
        << "\n========================\n";

    for (size_t i = 0, n = values.size(); i < n; ++i)
        if(std::isnan(values[i].first))
            std::cout << std::setw(5) << i << ": " << values[i].second <<"\n";
        else
            std::cout << std::setw(5) << i << ": " << values[i].first << "\n";
    std::cout << "========================\n\n";
}

} // namespace minirisk
