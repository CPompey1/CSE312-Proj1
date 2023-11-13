from datetime import datetime, timedelta
import sys
def timeLeft(endDate):
    timeDelta = endDate - datetime.now()
    daysLeft = timeDelta.days
    totalSeconds = timeDelta.seconds
    hoursLeft = totalSeconds // 3600
    minutesLeft = (totalSeconds % 3600) // 60
    secondsLeft = totalSeconds % 60
    timeLeft = "%dd %dh %dm %ds" %(daysLeft,hoursLeft,minutesLeft,secondsLeft)
    return timeLeft

def isAuctionOver(endDate):
    timeDelta = endDate - datetime.now()
    daysLeft = timeDelta.days
    if daysLeft < 0:
        return True
    else:
        return False
