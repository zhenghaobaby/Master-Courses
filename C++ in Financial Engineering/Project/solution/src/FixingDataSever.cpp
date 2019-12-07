//
// Created by zhenghaobaby on 2019/11/2.
//
#include "FixingDataSever.h"
#include "Macros.h"
#include "Streamer.h"


namespace minirisk{

    FixingDataServer::FixingDataServer(const string &filename) {
        std::ifstream is(filename);
        MYASSERT(!is.fail(), "Could not open file " << filename);
        string name;
        string date;
        double value;
        while(is>>name>>date>>value){
            unsigned y = std::atoi(date.substr(0, 4).c_str());
            unsigned m = std::atoi(date.substr(4, 2).c_str());
            unsigned d = std::atoi(date.substr(6, 2).c_str());
            m_data.emplace(name, std::map<Date, double>());
            auto ins = m_data[name].emplace(Date(y,m,d), value);
            MYASSERT(ins.second, "Duplicated fixing: " << name<<" "<<date<<" "<<value<<'\n');
        }
    }
    double FixingDataServer::get(const string &name, const Date &t) const {

            auto iter = m_data.find(name);
            MYASSERT(iter != m_data.end(), "Market data not found: "
            << name<<","<<t.to_string());
            auto Date_iterator = iter->second.find(t);
            MYASSERT(Date_iterator!=iter->second.end(),"Fixing not found: "
            <<name<<","<<t.to_string());
            return Date_iterator->second;
    }

    std::pair<double, bool> FixingDataServer::lookup(const string &name, const Date &t) const {
        auto iter = m_data.find(name);
        if(iter != m_data.end()) {
            auto Date_iterator = iter->second.find(t);
            if (Date_iterator != iter->second.end()) //found
                return std::make_pair(Date_iterator->second, true);
        }
        return std::make_pair(std::numeric_limits<double>::quiet_NaN(), false);
    }

}

