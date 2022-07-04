
#include <bits/stdc++.h>

using namespace std;

#define int            long long int
#define F              first
#define S              second
#define pb             push_back
#define si             set <int>
#define vi             vector <int>
#define pii            pair <int, int>
#define vpi            vector <pii>
#define vpp            vector <pair<int, pii>>
#define mii            map <int, int>
#define mpi            map <pii, int>
#define spi            set <pii>
#define endl           "\n"
#define sz(x)          ((int) x.size())
#define all(p)         p.begin(), p.end()
#define double         long double
#define que_max        priority_queue <int>
#define que_min        priority_queue <int, vi, greater<int>>
#define bug(...)       __f (#__VA_ARGS__, __VA_ARGS__)
#define print(a)       for(auto x : a) cout << x << " "; cout << endl
#define print1(a)      for(auto x : a) cout << x.F << " " << x.S << endl
#define print2(a,x,y)  for(int i = x; i < y; i++) cout<< a[i]<< " "; cout << endl

const int N = 1e9+7;

class cmp {
public:
	bool operator()(pair<int,int>&A,pair<int,int>&B) {
		if(A.first==B.first)return A.second<B.second;
        return A.first>B.first;
	}
};

bool comp(pair<int,int>&A,pair<int,int>&B) {
		if(A.first==B.first)return A.second<B.second;
        return A.first>B.first;
	}

void solve() {

int n;
cin>>n;
int ans=1;
for (int i = 1; i <=n; i++)
{
  ans*=i;
}

cout<<123;


}

int32_t main()
{
  ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);


  clock_t z = clock();

  int t = 1;
//   cin >> t; 
  while (t--) solve();



  return 0;
}
