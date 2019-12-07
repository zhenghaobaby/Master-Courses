//
// Created by zhenghaobaby on 2019/11/2.
//
#pragma once

#include <map>
#include <regex>
#include "Date.h"
#include "Global.h"

namespace minirisk {

    struct FixingDataServer
    {
    public:
        FixingDataServer(const string& filename);

        // queries
        double get(const string& name,const Date&t) const;

        std::pair<double, bool> lookup(const string& name,const Date&t) const;


    private:
        std::map<string, std::map<Date,double>> m_data;
    };



} // namespace minirisk


