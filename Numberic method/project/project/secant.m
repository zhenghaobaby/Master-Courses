% secant method for root search
function x1=secant(f,x0,x1,xAcc,nIter)
    fx0 = f(x0);
    found = 0;
    for i=1:nIter
        x101d = x1;
        fx1 = f(x1);
        x1 = x1-fx1*(x1-x0)/(fx1-fx0);
        
        if(abs(x1-x101d)<xAcc)
            found = 1;
            break;
        end
        x0 = x101d;
        fx0 = fx1;
    end
    
    if(~found)
        error("Maxium number of iterations exceeded");
    end
end
