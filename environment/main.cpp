// #include <iostream>
// #include <vector>
// #include <random>
// #include <windows.h>
// #include <string>
// #include <clocale>

// using namespace std;

// const unsigned short DARK_BLUE = FOREGROUND_BLUE;
// const unsigned short BRIGHT_BLUE = FOREGROUND_BLUE | FOREGROUND_INTENSITY;

// static const int size = 50;

// static const string tie_fighter = "/   \\\n|-0-|\n\\   /";

// HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

// void setCursorPosition(int x, int y)
// {
//     static const HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
//     std::cout.flush();
//     COORD coord = { (SHORT)x, (SHORT)y };
//     SetConsoleCursorPosition(hOut, coord);
// }

// void setConsoleColour(unsigned short colour)
// {
//     static const HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
//     std::cout.flush();
//     SetConsoleTextAttribute(hOut, colour);
// }
// random_device gen;

// template<typename T>
// void out(std::vector<vector<T>> v, std::vector<vector<T>> p) {

// 	setConsoleColour(BRIGHT_BLUE);
// 	setConsoleColour(DARK_BLUE);

// 	SetConsoleTextAttribute(hConsole, gen() % (2 << 7) );

// 	for (int i = 0; i < size; ++i)
// 	{
// 		for (int j = 0; j < size; ++j)
// 		{
// 			if (v[i][j] != p[i][j]) {
// 				setCursorPosition(i, j);
// 				cout << v[i][j];
// 			}
// 		}
// 	}
// 	cout.flush();
// }

// signed main () {

// 	setlocale(LC_CTYPE, "rus");
// 	SetConsoleOutputCP(1251);
//     SetConsoleCP(1251);

// 	string s = "Привет";

// 	cout << s;

// 	vector<vector<char>>prev_field(size, vector<char>(size));
// 	vector<vector<char>>next_field(size, vector<char>(size));

// 	for (int i = 0; i < size; ++i)
// 	{
// 		for (int j = 0; j < size; ++j)
// 		{
// 			prev_field[i][j] = ' ';
// 			next_field[i][j] = ' ';
// 		}
// 	}

// 	random_device gen;

// 	for (int i = 0; i < 100; ++i)
// 	{
// 		for (int j = 0; j < 1000; ++j)
// 		{
// 			next_field[gen() % size][gen() % size] = gen() % 2 ? ' ' : '#';

// 		}
// 		out(next_field, prev_field);
// 		for (int j = 0; j < size; ++j)
// 		{
// 			for (int k = 0; k < size; ++k)
// 			{
// 				prev_field[j][k] = next_field[j][k];
// 			}
// 		}
// 		Sleep(1000);
// 	}


// 	return 0;
// }


#include <iostream>
#include <string>
#include <windows.h>
#include <fstream>

using namespace std;

static std::string to_dos(std::string from) {
    char buffer[1000];
    OemToChar(from.c_str(), buffer);
    return buffer;
}
static char* to_dos(char* from) {
    char *buffer;
    buffer = new char[1000];
    OemToCharA(from, buffer);
    return buffer;
}


signed main(int argc, char* argv[])
{
  int a = 10;
  float result = 0;
  float x;
  int i = 0;
  int j;
  int divider = 1;
  x =  (float)(1 - (float)a) / (float)(-1 - a);
  for ( ; i < 10; ++i) {
    j = 0;
    cout<<result<<endl;
    result += 2 * x / (float)divider;
    x *= (float)(1 - a) / (float)(-1 - a);
    x *= (float)(1 - a) / (float)(-1 - a);
    divider += 2;
  }

  cout<<result;
	
	// string s;	
	// cin>>s;
	// s=to_dos(s);





	 // HWND console = GetConsoleWindow();
  // RECT r;
  // GetWindowRect(console, &r); //stores the console's current dimensions

  // //MoveWindow(window_handle, x, y, width, height, redraw_window);
  // MoveWindow(console, r.left, r.top, 800, 600, TRUE);
  // for (int j = 0; j < 100; ++j)
  //   {
  //     for (int i = 0x41; i < 0x5B; ++i)
  //       cout << (char)i;
  //   }
  // cout << endl;
  // Sleep(1000);
  // MoveWindow(console, r.left, r.top, r.right - r.left, r.bottom - r.top, TRUE);

	// setlocale(LC_CTYPE, "rus");
 //    SetConsoleCP(1251);// установка кодовой страницы win-cp 1251 в поток ввода
 //    SetConsoleOutputCP(1251); // установка кодовой страницы win-cp 1251 в поток вывода
 
 //    char string[20];
 //    cin >> string; // вводим строку, используя Кириллицу
 //    cout << "\nвывод: "<< string << endl; // ввывод строки
 //    system("pause");
 //    return 0;
}
