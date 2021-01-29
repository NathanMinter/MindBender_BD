s = "1102021222"
k = 2

## Check if a specific substring is perfect according to k
def CheckPerfection(substring, k):
    for c in set(substring):
        if substring.count(c) != k:
            return False
    ## function will only reach this return if it hasn't already returned false in the loop
    return True

## Iterate through all substrings to check and increment counter
def PerfectSubstring(s, k):
    substrings = [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
    count = 0
    for s in substrings:
        ## Save time by skipping any substrings that aren't a multiple of k - these obviously can't be perfect
        if len(s) % k == 0:
            if CheckPerfection(s, k) == False:
                continue
            else:
                count += 1
    print(count)
    return count

PerfectSubstring(s, k)
