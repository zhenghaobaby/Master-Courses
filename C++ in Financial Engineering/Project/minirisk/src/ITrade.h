#pragma once

#include <vector>
#include <memory>

#include "IObject.h"
#include "IPricer.h"
#include "Streamer.h"

namespace minirisk {

// NOTE: in a real world system this should be a proper serializable guid class
typedef unsigned guid_t;

struct ITrade : IObject
{
    // return the quantity of the trade (the sign determines if it is a buy or sell)
    virtual double quantity() const = 0;

    // returns the global unique identfier assigned to this trade
    virtual const guid_t& id() const = 0;

    // serialization funcions
    virtual void save(my_ofstream& os) const = 0;
    virtual void load(my_ifstream& is) = 0;

    // return option type in human readable format
    virtual const std::string& idname() const = 0;

    // print trade attributes
    virtual void print(std::ostream& os) const = 0;

    // Get pricer
    virtual ppricer_t pricer(const std::string&ccy_base) const = 0;
};

typedef std::shared_ptr<ITrade> ptrade_t;
typedef std::vector<ptrade_t> portfolio_t;

} // namespace minirisk

