function delta = getStrikeFromDelta_test(fwd, T, cp, sigma,K)
   Nd1 = normcdf((log(fwd)-log(K))/(sigma*sqrt(T))+0.5*sigma*sqrt(T));
   if cp == 1
       delta = Nd1;
   elseif cp == -1
       delta = 1-Nd1;
   else
       error('invalid cp in getStrikeFromDelta_test');
   end
end