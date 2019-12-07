#pragma once

#include "ITrade.h"
#include "Streamer.h"

namespace minirisk {

template <typename T>
struct Trade : ITrade
{
    virtual double quantity() const
    {
        return m_quantity;
    }

    void init(double quantity = 1.0)
    {
        m_quantity = quantity;
    }

    virtual const guid_t& id() const
    {
        return T::m_id;
    }

    virtual const std::string& idname() const
    {
        return T::m_name;
    }

protected:
    virtual void print(std::ostream& os) const
    {
        os << format_label("Id") << id() << std::endl;
        os << format_label("Name") << idname() << std::endl;
        os << format_label("Quantity") << quantity() << std::endl;
        static_cast<const T*>(this)->print_details(os);
        os << std::endl;
    }

    virtual void save(my_ofstream& os) const
    {
        os << id()
            << quantity();
        static_cast<const T*>(this)->save_details(os);
    }

    virtual void load(my_ifstream& is)
    {
        // read everything but id
        is >> m_quantity;
        static_cast<T*>(this)->load_details(is);
    }

private:
    double m_quantity;
};

} // namespace minirisk
