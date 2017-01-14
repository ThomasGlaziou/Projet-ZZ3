
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

var float: X;
var float: Xd;

%array[1..9] of 0..max: s=[0,0,0,0,0,0,0,0,0];
%int :t=5;

var 0..max: t;

constraint trace(show([s[i] |i in 1..9]), true);
constraint X = ((sum(i in 1..9)(s[i]))-(9*s[5]))/s[5] ;
constraint Xd = ((sum(i in 1..9)(s[i]+delta[i]))-(9*(s[5]+delta[5])))/
(s[5]+delta[5]);
constraint X == Xd;

constraint forall(i in 1..9)(abs(delta[i]) < t);
constraint forall(i in 1..9)(delta[i] >= -max);
constraint forall(i in 1..9)(delta[i] <= max);
constraint forall(i in 1..9)((delta[i]+s[i]) >= -5);
constraint forall(i in 1..9)((delta[i]+s[i]) <=max);



% Pixels à changer
constraint s[pos]+delta[pos]=val;

solve::float_search(
  [delta[i] | i in 1..9],
  0.00000000, 
  dom_w_deg, 
  indomain, 
  complete)
  
minimize t;

%output [ show(delta) ];