#pragma once

#include "Macros.h"
#include <string>
#include <array>
#include <algorithm>
using namespace std;

namespace minirisk {

struct Date
{
public:
    static const unsigned first_year = 1900;
    static const unsigned last_year = 2200;
    static const unsigned n_years = last_year - first_year;

private:
    static std::string padding_dates(unsigned);

    // number of days elapsed from beginning of the year
    //unsigned day_of_year() const;

    friend long operator-(const Date& d1, const Date& d2);

    static const std::array<unsigned, 12> days_in_month;  // num of days in month M in a normal year
    static const std::array<unsigned, 12> days_ytd;      // num of days since 1-jan to 1-M in a normal year
    static const std::array<unsigned, n_years> days_epoch;   // num of days since 1-jan-1900 to 1-jan-yyyy (until 2200)

public:
    // Default constructor
    //Date() : m_y(1970), m_m(1), m_d(1), m_is_leap(false) {}
    Date() : serial_(20000){}
    // Constructor where the input value is checked.
    Date(unsigned serial_)
    {
        init(serial_);
    }
    Date(unsigned year, unsigned month, unsigned day)
    {
        init(year,month,day);
    }

    void init(unsigned serial_)
    {
        check_valid(serial_);
        this->serial_ = serial_;
    }
    void init(unsigned year, unsigned month, unsigned day)
    {
        check_valid(year,month,day);
        bool m_is_leap = is_leap_year(year);

        this->serial_ = days_epoch[year - 1900] +
                        days_ytd[month - 1] + ((month > 2 && m_is_leap) ? 1 : 0) + (day - 1);
    }


    static void check_valid(unsigned y, unsigned m, unsigned d);
    static void check_valid(unsigned serial);

    bool operator<(const Date& d) const
    {
        //return (m_y < d.m_y) || (m_y == d.m_y && (m_m < d.m_m || (m_m == d.m_m && m_d < d.m_d)));
        return serial_<d.serial_;
    }

    bool operator==(const Date& d) const
    {
        //return (m_y == d.m_y) && (m_m == d.m_m) && (m_d == d.m_d);
        return serial_==d.serial_;
    }

    bool operator>(const Date& d) const
    {
        //return d < (*this);
        return serial_>d.serial_;
    }

    // number of days since 1-Jan-1900
    unsigned serial() const
    {
        //return days_epoch[m_y - 1900] + day_of_year();
        return this->serial_;
    }

    static bool is_leap_year(unsigned yr);

    // In YYYYMMDD format
    std::string to_string(bool pretty = true) const
    {
        unsigned short m_y;
        bool m_is_leap;
        unsigned char m_m;
        unsigned char m_d;

        int year_position = upper_bound(days_epoch.cbegin(),days_epoch.cend(),serial_)-days_epoch.cbegin();
        m_y = year_position+1900-1;
        if (serial_-days_epoch[m_y-1900]<0)
        {
            m_y-=1;
            m_is_leap = is_leap_year(m_y);
        }
        else m_is_leap = is_leap_year(m_y);

        int m_position = lower_bound(days_ytd.cbegin(),days_ytd.cend(),serial_-days_epoch[m_y-1900]+1)-days_ytd.cbegin();
        m_m =(unsigned char)m_position;
        m_d =(unsigned char)(serial_-days_epoch[m_y-1900]-days_ytd[m_m-1]-((m_m > 2 && m_is_leap) ? 1 : 0)+1);


        return pretty
            ? std::to_string((int)m_d) + "-" + std::to_string((int)m_m) + "-" + std::to_string(m_y)
            : std::to_string(m_y) + padding_dates((int)m_m) + padding_dates((int)m_d);
    }

private:
    //unsigned short m_y;
    //unsigned char m_m;
    //unsigned char m_d;
    //bool m_is_leap;
    unsigned serial_;

};

long operator-(const Date& d1, const Date& d2);

inline double time_frac(const Date& d1, const Date& d2)
{
    return static_cast<double>(d2 - d1) / 365.0;
}

} // namespace minirisk
