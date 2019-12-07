#include <iostream>
#include <algorithm>

#include "MarketDataServer.h"
#include "FixingDataSever.h"
#include "PortfolioUtils.h"

using namespace::minirisk;

void run(const string& portfolio_file, const string& risk_factors_file,const string&ccy_base,const string&fix_path)
{
    // load the portfolio from file
    portfolio_t portfolio = load_portfolio(portfolio_file);
    // save and reload portfolio to implicitly test round trip serialization
    save_portfolio("portfolio.tmp", portfolio);
    portfolio.clear();
    portfolio = load_portfolio("portfolio.tmp");

    // display portfolio
    print_portfolio(portfolio);

    // get pricers

    std::vector<ppricer_t> pricers(get_pricers(portfolio, ccy_base));

    // initialize market data server
    std::shared_ptr<const MarketDataServer> mds(new MarketDataServer(risk_factors_file));
    std::shared_ptr<const FixingDataServer> fds;
    try{
    if (!fix_path.empty())
        fds.reset(new FixingDataServer(fix_path));}
    catch (exception&e){
        cout<<e.what();
    }


    // Init market object
    Date today(2017,8,5);
    Market mkt(mds, today);

    // Price all products. Market objects are automatically constructed on demand,
    // fetching data as needed from the market data server.
    {
        auto prices = compute_prices(pricers, mkt,fds);
        print_price_vector("PV", prices);
    }

    // disconnect the market (no more fetching from the market data server allowed)
    mkt.disconnect();

    // display all relevant risk factors
    {
        std::cout << "Risk factors:\n";
        auto tmp = mkt.get_risk_factors(".+");
        for (const auto& iter : tmp)
            std::cout << iter.first << "\n";
        std::cout << "\n";
    }

    {   // Compute PV01 Bucketed (i.e. sensitivity with respect to interest rate dV/dr)
        std::vector<std::pair<string, portfolio_values_t>> pv01(PV01Bucketed(pricers,mkt,fds));  // PV01 per trade

        // display PV01 per currency
        for (const auto& g : pv01)
            print_price_vector("PV01 bucketed " + g.first, g.second);
    }


    {   // Compute PV01 Parallel (i.e. sensitivity with respect to interest rate dV/dr)
        std::vector<std::pair<string, portfolio_values_t>> pv01(PV01Parallel(pricers,mkt,fds));  // PV01 per trade

        // display PV01 per currency
        for (const auto& g : pv01)
            print_price_vector("PV01 " + g.first, g.second);
    }

    {   // Compute fx Delta  (i.e. sensitivity with respect to fx spot rate dV/ds)
        std::vector<std::pair<string, portfolio_values_t>> delta(fx_delta(pricers,mkt,fds));

        // display delta
        for (const auto& g : delta)
            print_price_vector("FX delta " + g.first, g.second);
    }


}

void usage()
{
    std::cerr
        << "Invalid command line arguments\n"
        << "Example:\n"
        << "DemoRisk -p portfolio.txt -f risk_factors.txt\n";
    std::exit(-1);
}

int main(int argc, const char **argv)
{
    // parse command line arguments
    string portfolio, riskfactors,ccy_base,fix_path;
    if (argc % 2 == 0)
        usage();
    for (int i = 1; i < argc; i += 2) {
        string key(argv[i]);
        string value(argv[i+1]);
        if (key == "-p")
            portfolio = value;
        else if (key == "-f")
            riskfactors = value;
        else if (key == "-b")
            ccy_base = value;
        else if (key == "-x")
            fix_path = value;
        else
            usage();
    }
    if (portfolio == "" || riskfactors == "")
        usage();
    if (ccy_base == "")
        ccy_base = "USD";


    try {
        run(portfolio, riskfactors,ccy_base,fix_path);
        return 0;  // report success to the caller
    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << "\n";
        return -1; // report an error to the caller
    }
    catch (...)
    {
        std::cerr << "Unknown exception occurred\n";
        return -1; // report an error to the caller
    }
}
