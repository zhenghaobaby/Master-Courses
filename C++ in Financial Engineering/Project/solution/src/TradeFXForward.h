//
// Created by zhenghaobaby on 2019/11/3.
//
#pragma once

#include "Trade.h"
#include "Date.h"

namespace minirisk {

    struct TradeFXForward : Trade<TradeFXForward>
    {
        friend struct Trade<TradeFXForward>;

        static const guid_t m_id;
        static const std::string m_name;

        TradeFXForward() {}

        void init(const std::string& ccy1,const std::string& ccy2,
                const double quantity,const double strike, const Date& fixing_date, const Date&settle_date)
        {
            Trade::init(quantity);
            m_ccy1 = ccy1;
            m_ccy2 = ccy2;
            m_strike = strike;
            m_fixing_date = fixing_date;
            m_settle_date = settle_date;
        }

        virtual ppricer_t pricer(const std::string&ccy_base) const;

        const string& ccy1() const
        {
            return m_ccy1;
        }
        const string& ccy2() const{
            return m_ccy2;
        }
        const double strike() const
        {
            return m_strike;
        }
        const Date& fixing_date() const
        {
            return m_fixing_date;
        }
        const Date& settle_date() const
        {
            return m_settle_date;
        }


    private:
        void save_details(my_ofstream& os) const
        {
            os << m_ccy1 << m_ccy2 << m_strike << m_fixing_date << m_settle_date;
        }

        void load_details(my_ifstream& is)
        {
            is >>  m_ccy1 >> m_ccy2 >> m_strike >> m_fixing_date >> m_settle_date;
        }

        void print_details(std::ostream& os) const
        {
            os << format_label("Strike level")<<m_strike<<std::endl;
            os << format_label("Base Currency") << m_ccy1 << std::endl;
            os << format_label("Quote Currency") << m_ccy2 << std::endl;
            os << format_label("Fixing Date")<<m_fixing_date<<std::endl;
            os << format_label("Settlement Date")<<m_settle_date<<std::endl;
        }

    private:
        std::string m_ccy1;
        std::string m_ccy2;
        double m_strike;
        Date m_fixing_date;
        Date m_settle_date;

    };

} // namespace minirisk
