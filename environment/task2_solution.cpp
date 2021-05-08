#include <iostream>

using namespace std;


signed main(int argc, char const *argv[])
{
	int n;
	cin >> n;
	int ans = 0;
	for (int i = 0; i < n; ++i) {
		int a;
		cin >> a;
		ans += a;
	}
	cout << ans;
	return 0;
}