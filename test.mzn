include "globals.mzn";



var float : x;



function var float : atan_fun_2(var float: x, var float : x_res, var float: res, var int : iter) =

  if iter == 0 then res else res + pow(-1+0.0,iter)*x_res*x*x/(2*iter+1) + atan_fun_2(x,  x_res*x*x, res + pow(-1+0.0,iter)*x_res*x*x/(2*iter+1), iter-1) endif;
  
function var float : atan_fun(var float: x) =
  x-x*x*x/3+x*x*x*x*x/5+x*x*x*x*x*x*x/7-x*x*x*x*x*x*x*x*x/9+x*x*x*x*x*x*x*x*x*x*x/11-x*x*x*x*x*x*x*x*x*x*x*x/12+x*x*x*x*x*x*x*x*x*x*x*x*x*x/14;

function var float : atan_fun_3(var float: x) =
sum(i in 1..20) (
         pow(-1,i)*pow(x,2*i+1)/(2*i+1)
  );
  
var float : d; 
var float : c;
var float : i=5;
constraint d == 2+x;
%constraint c=atan_fun_2(x,x,x,2);
%constraint c= pow(-1,i)*x*x*x/(2*i+1);
constraint c=atan_fun(x);
constraint x<=0.5;
constraint x>=0;

%solve satisfy;
solve::float_search(
  [x,d,c], 
  0.00000000, 
  dom_w_deg, 
  indomain, 
  complete)

minimize x;


output [ "x =", show(x) ];