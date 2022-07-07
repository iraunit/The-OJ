#include<bits/stdc++.h>
using namespace std;
 
#define vv vector<long long > v;
 
 
 
 
 
int main(){
 
 
 
    long long  n;
    cin>>n;
    vector<long long >v;
    while(n>1){
    	if(n%2==0){
    		v.push_back(n);
    		n=n/2;
    	}
    	else{
    		v.push_back(n);
    		n=n*3;
    		n+=1;
    	}
    }
    v.push_back(1);
    for(auto a:v){
    	cout<<a<<" ";
    }
 
 
 
    return 0;
 
}