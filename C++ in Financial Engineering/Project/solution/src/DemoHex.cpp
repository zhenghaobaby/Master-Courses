#include <iostream>
#include <iomanip>
#include <cstdint>
#include <string>

using namespace std;

//void out_char_as_hex(int c)
//{
//    cout << hex << setw(2) << setfill('0') << c;
//}

int main()
{
    union { double d; uint64_t u; } tmp;

    std::istringstream converter("bfc3ff583a53b8e5");
    uint64_t value;
    converter >> std::hex >> value;
    tmp.u = value;
    cout<<tmp.d<<endl;

//    sscanf(s.c_str(),"%X",&tmp.u);
//    cout<<tmp.d<<endl;

    double x = -0.15623;
    tmp.d = x;
    cout << hex << tmp.u << endl;
    return 0;
}
