#pragma once

#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <regex>
#include <inttypes.h>




#include "Global.h"
#include "Date.h"
#include "Macros.h"

namespace minirisk {

// streaming separator
const char separator = ';';

//
// Overload classes
//

struct my_ofstream
{
    my_ofstream(const string& fn)
        : m_of(fn)
    {
    }
    void endl() { m_of << std::endl; }
    void close() { m_of.close(); }
    std::ofstream m_of;
};

struct my_ifstream
{
    my_ifstream(const string& fn)
        : m_if(fn)
    {
        MYASSERT(!m_if.fail(), "Could not open file " << fn);
    }

    bool read_line()
    {
        std::getline(m_if, m_line);  // read a line and store it in m_line
        m_line_stream.str(m_line);   // associate a string stream with m_line
        return m_line.length() > 0;
    }

    inline string read_token()
    {
        string tmp;
        std::getline(m_line_stream, tmp, separator);
        return tmp;
    }

private:
    string m_line;
    std::istringstream m_line_stream;
    std::ifstream m_if;
};

//
// Generic file streamer
//

template <typename T>
inline my_ifstream& operator>>(my_ifstream& is, T& v)
{
    string tmp = is.read_token();
    std::istringstream(tmp) >> v;
    return is;
}

template <typename T>
inline my_ofstream& operator<<(my_ofstream& os, const T& v)
{
    os.m_of << v << separator;
    return os;
}

//
// Double streamer overloads
//


//when saving a double to a file in text format, use the maximum possible precision
//inline my_ofstream& operator<<(my_ofstream& os, double v)
//{
//    std::stringstream buffer;
//    uint64_t* pointer_v = reinterpret_cast<uint64_t*>(&v);
//    buffer << std::hex << *pointer_v;
//    os << buffer.str();
//    return os;
//}
//
//inline my_ifstream& operator>>(my_ifstream& is, double& v)
//{
//    std::string hex_string;
//    is >> hex_string;
//    int base = 16;
//    char* end;
//    unsigned long long int number;
//    number = strtoull(hex_string.c_str(), &end, base);
//    double* pointer_v = reinterpret_cast<double*>(&number);
//    v = *pointer_v;
//    return is;
//}


inline my_ofstream& operator<<(my_ofstream& os, double v)
{
    union { double x; uint64_t u; } tmp;
    tmp.x = v;
//  os.m_of << std::scientific << std::setprecision(16) << v << separator;
    os.m_of<<hex<< tmp.u << separator;
    return os;
}

inline my_ifstream& operator>>(my_ifstream& is, double&v)
{
    std::string input;
    is>>input;
    std::istringstream converter(input.c_str());
    uint64_t value;
    converter >> std::hex >> value;
    union {double d; uint64_t u;} tmp;
    tmp.u = value;
    v = tmp.d;
    return is;

    //sscanf(str.c_str(), "%X", &tmp.u);

}



//
// Vector streamer overloads
//

template <typename T, typename A>
inline std::ostream& operator<<(std::ostream& os, const std::vector<T, A>& v)
{
    for (const T& i : v)
        os << i << " ";
    return os;
}

template <typename T>
inline my_ofstream& operator<<(my_ofstream& os, const std::vector<T>& v)
{
    os << v.size();
    for (const T& i : v)
        os << i;
    return os;
}


template <typename T, typename A>
inline my_ifstream& operator>>(my_ifstream& is, std::vector<T, A>& v)
{
    size_t sz;
    is >> sz; // read size (this will call the general overload for >>)
    v.resize(sz);
    for (size_t i = 0; i < sz; ++i)
        is >> v[i];  // read i-th value
    return is;
}


//
// Date streamer overloads
//

inline std::ostream& operator<<(std::ostream& os, const Date& d)
{
    os << d.to_string(true);
    return os;
}

inline my_ofstream& operator<<(my_ofstream& os, const Date& d)
{
    os << d.to_string(false);
    return os;
}

inline my_ifstream& operator>>(my_ifstream& is, Date& v)
{
    string tmp;
    is >> tmp;
    //if you enter the date like 20200201
    if(tmp.length()>6) {
        unsigned y = std::atoi(tmp.substr(0, 4).c_str());
        unsigned m = std::atoi(tmp.substr(4, 2).c_str());
        unsigned d = std::atoi(tmp.substr(6, 2).c_str());
        v.init(y, m, d);
    }
    //else we assume you enter the serial
    else{
        unsigned serial_ = std::atoi(tmp.c_str());
        v.init(serial_);
    }

    return is;
}

} // namespace minirisk

