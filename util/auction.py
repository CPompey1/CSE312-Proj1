def highestBid(bids: dict, startingBid):
    if len(bids) == 0:
        return ("Starting Bid",startingBid)
    else:
        highestBidder = max(bids.items(), key=lambda x: x[1])
        return ("Highest Bid", highestBidder[1])
    

def winningBid(bids: dict, startingBid):
    if len(bids) == 0:
        return ("NO WINNER", startingBid)
    else:
        highestBidder = max(bids.items(), key=lambda x: x[1])
        return (highestBidder[0], highestBidder[1])
