from datetime import datetime

##### Functions to SELECT/FETCH Data #####
def selectUser(username, cursor):
    query = "SELECT pmkUsername FROM tblUsers WHERE pmkUsername = \"" + username + "\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result[0] if len(result) > 0 else ""


# Invite Select Functions
def selectIncomingInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites WHERE pfkAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectOutgoingInvites(fromPlayer, cursor):
    query = "SELECT * FROM tblGameInvites WHERE pfkRequester = \"" + fromPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites WHERE pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

##### Functions to UPDATE/MODIFY Existing Data #####
def updateAcceptInvite(fromPlayer, toPlayer, cursor, connection):

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "UPDATE tblGameInvites SET fldIsAccepted = 1, fldAcceptanceTimestamp = \"" + time + "\" WHERE pfkRequester = \"" + fromPlayer + "\" AND pfkAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)    
    connection.commit()


##### Functions to INSERT/CREATE New Data #####
def insertNewGameInvite(fromPlayer, toPlayer, cursor, connection):

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "INSERT INTO tblGameInvites (pfkRequester, pfkAddressee, fldRequestTimestamp) VALUES (\""
    query += fromPlayer + "\", \"" + toPlayer + "\", \"" + time + "\")"
    
    cursor.execute(query)
    connection.commit() 