
array[1..9] of float: s;
%s=[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128];
%s=[256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256];

s=[94.0, 96.0, 96.0, 95.0, 93.10063136912974, 96.0, 95.0, 95.0, 96.0];
int: max=256;
float : alpha = 0.98;
int: pos=3;
float: val=93;
int: size=9;
array[1..size] of var float : delta;

var float : c1;
var float : c2;


function var float : atan_fun(var float: x) =
(1)*x/1+(-1)*x*x*x/3+(1)*x*x*x*x*x/5+(-1)*x*x*x*x*x*x*x/7+(1)*x*x*x*x*x*x*x*x*x/9+(-1)*x*x*x*x*x*x*x*x*x*x*x/11+(1)*x*x*x*x*x*x*x*x*x*x*x*x*x/13+(-1)*x*x*x*x*x*x*x*x*x*x*x*x*x*x*x/15+(1)*x*x*x*x*x*x*x*x*x*x*x*x*x*x*x*x*x/17;


var float: X;
var float: Xd;

%array[1..9] of 0..max: s=[0,0,0,0,0,0,0,0,0];
%int :t=5;

constraint (1-alpha)*atan_fun(sum(i in 1..size where i!=5)(s[i]-c1)/c1)+alpha*c1 == s[5];
constraint (1-alpha)*atan_fun(sum(i in 1..size where i!=5)(s[i]-c2)/c2)+alpha*c2 == s[5] + delta[5];

var 0..max: t;

constraint X = sum(i in 1..size)(s[i]-c1)/c1 ;
constraint Xd = sum(i in 1..size)(s[i]+delta[i]-c2)/(c2);
constraint X == Xd;

constraint forall(i in 1..9)(abs(delta[i]) < t);
constraint forall(i in 1..9)(delta[i] >= -max);
constraint forall(i in 1..9)(delta[i] <= max);
constraint forall(i in 1..9)(c1 >= 0);
constraint forall(i in 1..9)(c1 <= max);
constraint forall(i in 1..9)(c2 >= 0);
constraint forall(i in 1..9)(c2 <= max);
constraint delta[5] + c2 >= 0;
constraint delta[5] + c2 <= max;
constraint forall(i in 1..9 where i!=5)((delta[i]+s[i]) >= 0);
constraint forall(i in 1..9 where i!=5)((delta[i]+s[i]) <=max);



% Pixels à changer
constraint s[pos]+delta[pos]=val;

solve::float_search(
  [delta[i] | i in 1..9],
  0.00000000, 
  dom_w_deg, 
  indomain, 
  complete)
  
minimize t;

output [ "center : ",show(c1) ];
%output [ show(delta) ];
%output [ show(delta) ];