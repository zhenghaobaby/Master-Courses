#include "Date.h"
#include <vector>
#include <string>
#include <ctime>
using namespace minirisk;
using namespace std;

int create(const unsigned& x, const unsigned& y, const unsigned& z, int& counter)
{
    try
    {
        Date d(x, y, z);
    }
    catch (const std::invalid_argument& msg)
    {
        counter++;
		cout << msg.what() << endl;
    }
    return counter;
}

std::vector<Date> generate_date(const unsigned& startyear, const unsigned& endyear)
{
    std::vector<Date> date_vector;
    std::vector<unsigned> year, month, day;
    int i;
    for (i = startyear;i <= endyear;i++)
    {
        year.push_back(i);
    }
    for (i = 1;i <= 12;i++)
    {
        month.push_back(i);
    }
    for (i = 1;i <= 32;i++)  //为了iterator操作方便
    {
        day.push_back(i);
    }
    vector<unsigned>::iterator iter_y = year.begin();
    vector<unsigned>::iterator iter_m = month.begin();
    vector<unsigned>::iterator iter_d = day.begin();

    int dayct[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    int dayctl[12] = { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    while (true)
    {
        if (not((*iter_y % 4 != 0) ? false : (*iter_y % 100 != 0) ? true : (*iter_y % 400 != 0) ? false : true))  //not leap year
        {
            //cout << "not leap" << endl;
            if (*iter_d > dayct[*iter_m - 1])
            {
                iter_d = day.begin();
                iter_m++;
                //d.push_back((*iter_y, *iter_m, *iter_d));
            }
            if (iter_m == month.end())
            {
                iter_m = month.begin();
                iter_y++;
            }
        }
        else //leap
        {
            //cout << "leap" << endl;

            if (*iter_d >= dayctl[*iter_m - 1])
            {
                iter_d = day.begin();
                iter_m++;
                //d.push_back((*iter_y, *iter_m, *iter_d));
            }

            if (iter_m == month.end())
            {
                iter_m = month.begin();
                iter_y++;
            }
        }
        if (iter_y == year.end()) break;
        minirisk::Date d(*iter_y, *iter_m, *iter_d);
        date_vector.push_back(d);
        iter_d++;
    }
    //while结束
    return date_vector;
}

void test1()
{
    srand(time(NULL));
    int generator = rand();
    srand(generator);
    int dayct[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    int dayctl[12] = { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    int i,j=0;
    int invalid_counter=0,test_counter=0;
    bool leap = false;
    vector<int> year, month, day;

    for (i = 0;i <= 10000;i++)
    {
        year.push_back(rand() % 350 + 1875);
    }
    for (i = 0;i <= 10000;i++)
    {
        month.push_back(rand() % 15 + 1);
    }
    for (i = 0;i <= 10000;i++)
    {
        day.push_back(rand() % 35 + 1);
    }
    while (invalid_counter<1000)
    {
        if (year[j]<1900 | year[j] >= 2200)
        {
            invalid_counter++;
            test_counter = create(year[j], month[j], day[j], test_counter);
            j++;
            continue;
        }
        if (month[j] >= 13)
        {
            invalid_counter++;
            test_counter = create(year[j], month[j], day[j], test_counter);
            j++;
            continue;
        }

        leap = (year[j] % 4 != 0) ? false : (year[j] % 100 != 0) ? true : (year[j] % 400 != 0) ? false : true;
        if (leap == false)
        {
            if (day[j]>dayct[month[j] - 1])
            {
                invalid_counter++;

                test_counter = create(year[j], month[j], day[j], test_counter);
                j++;
                continue;
            }
        }
        else
        {
            if (day[j]>dayctl[month[j] - 1])
            {
                invalid_counter++;
                test_counter = create(year[j], month[j], day[j], test_counter);
                j++;
                continue;
            }
        }
        j++;
    }
    cout << "The generator of srand():" << generator << endl;
    if (test_counter != invalid_counter)
    {
        string str = "Test1 Failed!";
        throw(str);
    } else
        cout<<"Test 1 SUCCESS"<<endl;

}

void test2()
{
    std::vector<Date> date_vector = generate_date(1900, 2199);
    vector<Date>::iterator date_iter = date_vector.begin();
    int date_counter = -1;
    int true_counter = 0;
    for (;date_iter != date_vector.end();date_iter++)
    {

        //cout << (*date_iter).serial() << endl;    //transfer
        minirisk::Date d((*date_iter).serial()); //用得到的数字生成日期
        //cout << d.to_string(false) << endl;  //将数字形式变成日历形式
        date_counter++;
        if (((*date_iter).serial() == date_counter) & (Date(date_counter).to_string(false) == (*date_iter).to_string(false)))
            true_counter++;
    }
    if (true_counter != date_counter + 1)
    {
        string str = "Test2 Failed!";
        throw(str);
    } else
        cout<<"Test2 SUCCESS"<<endl;
}

void test3()
{
    std::vector<Date> date_vector = generate_date(1900, 2199);
    vector<Date>::iterator date_iter = date_vector.begin();
    int i = 0, true_counter = 0;
    for (;date_iter != date_vector.end()-1;date_iter++)
    {
        i = (*(date_iter+1)).serial() - (*date_iter).serial();
        if (i == 1) true_counter++;
    }
    if (true_counter != date_vector.size()-1)
    {
        string str= "Test3 Failed!";
        throw(str);
    } else
        cout<<"Test3 SUCCESS"<<endl;
}



void test4(){
    Date a = Date(1519);
    cout<<a.to_string()<<endl;
    Date b = Date(1904,2,29);
    cout<<b.serial()<<endl;
}


int main()
{
    try
    {
//        test1();
//        test2();
//        test3();
          test4();
    }
    catch (const string& msg)
    {
        cout << msg << endl;
        return 0;
    }
    cout << "Success" << endl;
    return 0;
}

