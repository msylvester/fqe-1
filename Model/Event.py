  def __init__(self, name, start, end, doorsDate, topLineInfo, ageLimitCode, ageLimit, eventStatusCode, eventStatus, eventStatusMessage, ticketPurchaseUrl, ticketprice):
        self.name = name
        #name of button
        self.start = start
        self.end = end 
        self.doorsDate = doorsDate
        self.topLineInfo = topLineInfo
        self.ageLimitCode = ageLimitCode
        self.ageLimit = ageLimit
        self.eventStatusCode = eventStatusCode
        self.eventStatus = eventStatus
        self.eventStatusMessage = eventStatusMessage
        self.ticketPurchaseUrl = ticketPurchaseUrl 
        self.ticketprice = ticketprice
        self.image = image 

    def getName(self):
        return self.name
    def getStart(self):
        return self.start

    def getTopLineInfo(self):
    	return self.topLineInfo

    def getAgeLimitCode(self):
    	return self.ageLimitCode

    def getAgeLimit(self):
    	return self.ageLimit
    def getEventStatusCode(self):
    	return self.eventStatusCode

    def getEventStatus(self):
    	return self.eventStatus

    def getEventStatusMessage(self):
    	return self.eventStatusMessage

    def getTicketPriceUrl(self):
    	return self.ticketPurchaseUrl

    def getTicketPrice(self):
    	return self.ticketprice

