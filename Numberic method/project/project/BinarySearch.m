   function pos = BinarySearch(t,x)
        left = 1;
        right = length(x);
        while left<=right
            mid = fix((left+right)/2);
            if x(mid)==t
                pos = mid;
                return
            elseif x(mid)>t
                right = mid-1;
            else
                left = mid+1;
            end
        end
        pos = right+1;    
    end