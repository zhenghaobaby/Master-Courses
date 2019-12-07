#include "Date.h"
#include <vector>
#include <string>
#include <ctime>
#include <tuple> 
using namespace minirisk;
using namespace std;

int create(const unsigned& x, const unsigned& y, const unsigned& z, int& counter)  //use year,month,day to create a date
{                                                                                  //if invalid, throw and catch, counter+1
    try
    {
        Date d(x, y, z);
    }
    catch (const std::invalid_argument& msg)
    {
        counter++;
		//cout << msg.what() << endl;
    }
    return counter;
}

auto generate_date(const unsigned& startyear, const unsigned& endyear)   //generate every valid date in [startyear,endyear)
{
    std::vector<Date> date_vector;
	std::vector<unsigned> year_vector, month_vector, day_vector;  //store year,month,day of every valid date(19000101,19000102..)
    std::vector<unsigned> year, month, day;   //store valid year(1900,1901,..),month(1,2,...),day
    int i;
    for (i = startyear;i < endyear;i++)
    {
        year.push_back(i);
    }
    for (i = 1;i <= 12;i++)
    {
        month.push_back(i);
    }
    for (i = 1;i <= 32;i++)  //Because some months' days are 31 and some are <31,so
    {                        //if i=31, there are two ways of ending a traversal, day_iter = day.end() 
        day.push_back(i);    //or *(day_iter)> this month's total days.Set i =32, so there is
    }                        //only one way of ending a traversal
    vector<unsigned>::iterator iter_y = year.begin();
    vector<unsigned>::iterator iter_m = month.begin();
    vector<unsigned>::iterator iter_d = day.begin();

    int dayct[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };   //for non-leap year
    int dayctl[12] = { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };  //for leap year
    while (true)
    {
        if (not((*iter_y % 4 != 0) ? false : (*iter_y % 100 != 0) ? true : (*iter_y % 400 != 0) ? false : true))  //not leap year
        {
            if (*iter_d > dayct[*iter_m - 1])     //days > this month's total days
            {
                iter_d = day.begin();
                iter_m++;
            }
            if (iter_m == month.end())   //traversal all months in a year
            { 
                iter_m = month.begin();
                iter_y++;
            }
        }
        else //leap year
        {
            if (*iter_d > dayctl[*iter_m - 1])
            {
                iter_d = day.begin();
                iter_m++;
            }
            if (iter_m == month.end())
            {
                iter_m = month.begin();
                iter_y++;
            }
        }
        if (iter_y == year.end()) break;
		year_vector.push_back(*iter_y);     //store the year of every valid date
		month_vector.push_back(*iter_m);	//store the month of every valid date
		day_vector.push_back(*iter_d);		//store the day of every valid date	
		minirisk::Date d(*iter_y, *iter_m, *iter_d);
        date_vector.push_back(d);   //store every valid date
        iter_d++;
    }
    //while loop ends
    return tuple<std::vector<Date>, std::vector<unsigned>, std::vector<unsigned>, std::vector<unsigned>> 
		(date_vector, year_vector, month_vector, day_vector);               
}

void test1()
{
    srand(time(NULL));
    int generator = rand(); //get random seed
    srand(generator); //use seed
    int dayct[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    int dayctl[12] = { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    int i,j=0;
    int invalid_counter=0,test_counter=0;
    bool leap = false;
    vector<int> year, month, day;
	// below let some year month day out of valid range
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
        string str = "Test1 FAILED!";
        throw(str);
    } else
        cout<<"Test1 SUCCESS!"<<endl;

}

void test2()
{
	std::vector<Date> date_vector;
	std::vector<unsigned> year_vector, month_vector, day_vector;
	tuple<std::vector<Date>, std::vector<unsigned>, std::vector<unsigned>, std::vector<unsigned>> t = generate_date(1900, 2200);
	std::tie(date_vector, year_vector, month_vector, day_vector) = t;   //date,year,month,day for every valid date 
    vector<Date>::iterator date_iter = date_vector.begin();
	vector<unsigned>::iterator year_iter = year_vector.begin();
	vector<unsigned>::iterator month_iter = month_vector.begin();
	vector<unsigned>::iterator day_iter = day_vector.begin();
	unsigned date_counter = 0;  //count totoal dates
	unsigned true_counter = 0;  //count dates that pass check
	unsigned y, m, d;       
	string str;
	Date temp_date;
    for (;date_iter != date_vector.end();date_iter++)  
	{	
        if ((*date_iter).serial() == date_counter) //if serial number of a date == date.serial()
		{	
			temp_date.init(date_counter);
			str= temp_date.to_string(false);
			y = atoi((str.substr(0,4)).c_str());
			m = atoi((str.substr(4,2)).c_str());
			d = atoi((str.substr(6,2)).c_str());
			if ((y == year_vector[date_counter]) & (m == month_vector[date_counter]) & (d == day_vector[date_counter]))
				//check whether the original calender == calender formal of the date generating from its serial number
			true_counter++;
		}
		date_counter++;
    }
    if (true_counter != date_counter)
    {
        string str = "Test2 FAILED!";
        throw(str);
    } else
        cout<<"Test2 SUCCESS!"<<endl;
}

void test3()
{	
	std::vector<Date> date_vector;
	std::vector<unsigned> year_vector, month_vector, day_vector;
	tuple<std::vector<Date>, std::vector<unsigned>, std::vector<unsigned>, std::vector<unsigned>> t = generate_date(1900, 2200);
	std::tie(date_vector, year_vector, month_vector, day_vector) = t;
    vector<Date>::iterator date_iter = date_vector.begin();
    int i = 0, true_counter = 0;
    for (;date_iter != date_vector.end()-1;date_iter++) //check every pair
    {
        i = (*(date_iter+1)).serial() - (*date_iter).serial();
        if (i == 1) true_counter++;
    }
    if (true_counter != date_vector.size()-1)  
    {
        string str= "Test3 Failed!";
        throw(str);
    } else
        cout<<"Test3 SUCCESS!"<<endl;
}




int main()
{
    try
    {
        test1();
        test2();
        test3();
    }
    catch (const string& msg)
    {
        cout << msg << endl;
        return 0;
    }
    cout << "Success" << endl;
    return 0;
}

