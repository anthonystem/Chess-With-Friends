##### Functions to SELECT/FETCH Data #####
def selectUser(username, cursor):
    query = "SELECT pmkUsername FROM tblUsers WHERE pmkUsername = \"" + username + "\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result[0] if len(result) > 0 else ""


def selectInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites WHERE fldAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 

def selectSentInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites WHERE fldRequester = \"" + fromPlayer + "\" AND fldAddressee = \"" + toPlayer + "\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return results 


##### Functions to UPDATE/MODIFY Existing Data #####
def updateAcceptInvite(fromPlayer, toPlayer, cursor, connection):
    query = "UPDATE tblGameInvites WHERE fldRequester = \"" + fromPlayer + "\" AND fldAddressee = \"" + toPlayer + "\" SET fldIsAccepted = 1"

    cursor.execute(query)
    connection.commit()


##### Functions to INSERT/CREATE New Data #####
def insertNewInvite(fromPlayer, toPlayer, connection, cursor):
    query = "INSERT INTO GameRequests (requester_id, addressee_id) VALUES (\""
    query += fromPlayer + "\", \"" + toPlayer + "\")"
    
    cursor.execute(query)
    connection.commit() 