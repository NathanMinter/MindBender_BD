bids = [[1,5,5,0], [2,7,8,1], [3,7,5,1], [4,10,3,3]]
totalShares = 18

## Count the number of shares owed to all bids higher than the given bid
def getHigherBidsCount(bid, bids):
    higherBidsCount = 0
    for b in bids:
        if b[2] > bid[2]:
            higherBidsCount += b[2]
        elif (b[2] == bid[2] & b[3] < bid[3]):
            higherBidsCount += b[2]
    return higherBidsCount

## Check, for each bid, whether the count of shares owed as above will take all of the available shares
def getUnallottedUsers(bids, totalShares):
    unallottedUsers = []
    for bid in bids:
        if getHigherBidsCount(bid, bids) >= totalShares:
            unallottedUsers.append(bid[0])
    return unallottedUsers

getUnallottedUsers(bids, totalShares)
