#include <iostream>
#include <string>
using namespace std;
signed main(int argc, char const *argv[])
{
	int n, d;
	cin >> n >> d;
	bool res = true;
	if (to_string(d).length()!=n||d<2)
		res = false;
	for (int i=2; i*i<=d;++i) {
		if (!(d%i)) {
			res = false;
		}
	}
	cout<<(res?1:0);
	return 0;
}