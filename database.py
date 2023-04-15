from datetime import datetime

##### Functions to SELECT/FETCH Data #####
def selectUser(username, cursor):
    query = "SELECT pmkUsername FROM tblUsers "
    query += "WHERE pmkUsername = \"" + username + "\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result[0] if len(result) > 0 else ""


# Invite Select Functions

def selectAllIncomingGameInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 
    
    
def selectIncomingGameInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkAddressee = \"" + toPlayer + "\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectAllOutgoingGameInvites(fromPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkRequester = \"" + fromPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectOutgoingGameInvites(fromPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkRequester = \"" + fromPlayer + "\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectAllGameInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 
    
def selectGameInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += "WHERE pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

##### Functions to UPDATE/MODIFY Existing Data #####
def updateAcceptInvite(gameInviteID, fromPlayer, toPlayer, cursor, connection):
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "UPDATE tblGameInvites "
    query += "SET fldIsAccepted = 1, fldAcknowledgeTimestamp = \"" + time + "\", pfkRequester = \"" + fromPlayer + "\", pfkAddressee = \"" + toPlayer + "\" "
    query += "WHERE pmkGameInviteId = " + str(gameInviteID) + " AND pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)    
    connection.commit()

def updateRejectInvite(gameInviteID, fromPlayer, toPlayer, cursor, connection):
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "UPDATE tblGameInvites "
    query += "SET fldIsRejected = 1, fldAcknowledgeTimestamp = \"" + time + "\", pfkRequester = \"" + fromPlayer + "\", pfkAddressee = \"" + toPlayer + "\" "
    query += "WHERE pmkGameInviteId = " + str(gameInviteID) + " AND pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)    
    connection.commit()

##### Functions to INSERT/CREATE New Data #####
def insertNewGameInvite(fromPlayer, toPlayer, cursor, connection):

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "INSERT INTO tblGameInvites (pfkRequester, pfkAddressee, fldRequestTimestamp) "
    query += "VALUES (\""
    query += fromPlayer + "\", \"" + toPlayer + "\", \"" + time + "\")"
    
    cursor.execute(query)
    connection.commit() 