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
 
inline int power(int a, int b)
{
  int x = 1;
  while (b)
  {
    if (b & 1) x *= a;
    a *= a;
    b >>= 1;
  }
  return x;
}
 
template <typename Arg1>
void __f (const char* name, Arg1&& arg1) { cout << name << " : " << arg1 << endl; }
template <typename Arg1, typename... Args>
void __f (const char* names, Arg1&& arg1, Args&&... args)
{
  const char* comma = strchr (names + 1, ',');
  cout.write (names, comma - names) << " : " << arg1 << " | "; __f (comma + 1, args...);
}
 
const int N = 200005;
 
void solve() {
 
int n;cin>>n;
int total=(n*(n+1))/2;
if(total%2)cout<<"NO"<<endl;
else{
    vi v(n,0);
    for(int i=0; i<n; i++)v[i]=i+1;
    set<int>s1,s2;
    if(n%4==0){
      int i=0;
      int k=n/4;
      for(i=0; i<k; i++)s1.insert(v[i]);
      for(int i=k; i<3*k; i++)s2.insert(v[i]);
      for(int i=3*k; i<n; i++)s1.insert(v[i]);
      cout<<"YES"<<endl;
      cout<<n/2<<endl;
      print(s1);
      cout<<n/2<<endl;
      print(s2); 
    }
    else if(n%4==3){
      s1.insert(1);s1.insert(2);s2.insert(3);
      if(n>3){
        int k=(n-3)/4;
        for(int i=3; i<k+3; i++)s1.insert(v[i]);
        for(int i=(k+3); i<(3*k+3); i++)s2.insert(v[i]);
        for(int i=(3*k+3); i<n; i++)s1.insert(v[i]);
      }
        cout<<"YES"<<endl;
        cout<<(n/2)+1<<endl;
        print(s1);
        cout<<n/2<<endl;
        print(s2);
    }
}
 
 
 
 
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