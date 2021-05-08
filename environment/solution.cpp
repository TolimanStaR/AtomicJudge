#include <iostream>
#include <vector>

using namespace std;


signed main(int argc, char const *argv[])
{
	int n;
	cin >> n;

	vector <int> a(n);

	for (int i = 0; i < n; ++i)
		cin >> a[i];

	int answer = 0;

	for (int i = 0; i < n; ++i) 
		answer += a[i];

	cout << answer;

	return 0;
}
