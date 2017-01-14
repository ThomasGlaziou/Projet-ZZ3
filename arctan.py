

if __name__ == '__main__':


    fct = "function var float : atan_fun(var float: x) =\n"
    for i in range(10):
        fct += "("+str((-1)**i)+")"
        fct += "*"+"x*"*(2*i+1)
        fct = fct[:-1]
        
        fct += "/"+str(2*i+1)+"+"

    fct = fct[:-1]
    fct+=";"
    
    with open("atan_fun.mzn", 'w') as f:
        f.write(fct)

