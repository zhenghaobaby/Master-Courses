#pragma once

#include <memory>
#include "FixingDataSever.h"
#include "IObject.h"
#include "Market.h"

namespace minirisk {

struct IPricer : IObject
{
//    virtual double price(Market& m) const = 0;
    virtual double price(Market& m, const FixingDataServer* fds) const = 0;
};


typedef std::shared_ptr<const IPricer> ppricer_t;

} // namespace minirisk
