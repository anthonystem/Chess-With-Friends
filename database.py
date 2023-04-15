from datetime import datetime

##### Functions to SELECT/FETCH Data #####
def selectUser(username, cursor):
    query = "SELECT pmkUsername FROM tblUsers "
    query += f"WHERE pmkUsername = \"{username}\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result[0] if len(result) > 0 else ""

# Search for Users
def selectSearchUsers(searchString, termLimit, cursor):
    # Do not apply a query limit if supplied limit < 0.
    if termLimit < 0:
        query = "SELECT pmkUsername FROM tblUsers "
        query += f"WHERE pmkUsername LIKE \"{searchString}%\""
    else:
        query = "SELECT pmkUsername FROM tblUsers "
        query += f"WHERE pmkUsername LIKE \"{searchString}%\" LIMIT {termLimit}"

    cursor.execute(query)
    result = cursor.fetchall()

    return list(result)

# Invite Select Functions
def selectAllIncomingGameInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkAddressee = \"{toPlayer}\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results)
    
    
def selectIncomingGameInvites(toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkAddressee = \"{toPlayer}\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results)

def selectAllOutgoingGameInvites(fromPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkRequester = \"{fromPlayer}\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results)

def selectOutgoingGameInvites(fromPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkRequester = \"{fromPlayer}\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results)

def selectAllGameInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkRequester = \"{fromPlayer}\" AND pfkAddressee = \"{toPlayer}\""
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results)
    
def selectGameInvites(fromPlayer, toPlayer, cursor):
    query = "SELECT * FROM tblGameInvites "
    query += f"WHERE pfkRequester = \"{fromPlayer}\" AND pfkAddressee = \"{toPlayer}\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)
    results = cursor.fetchall()

    return list(results) 

##### Functions to UPDATE/MODIFY Existing Data #####
def updateAcceptInvite(gameInviteID, fromPlayer, toPlayer, cursor, connection):
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "UPDATE tblGameInvites "
    query += f"SET fldIsAccepted = 1, fldAcknowledgeTimestamp = \"{time}\", pfkRequester = \"{fromPlayer}\", pfkAddressee = \"{toPlayer}\" "
    query += f"WHERE pmkGameInviteId = {str(gameInviteID)} AND pfkRequester = \"{fromPlayer}\" AND pfkAddressee = \"{toPlayer}\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)    
    connection.commit()

def updateRejectInvite(gameInviteID, fromPlayer, toPlayer, cursor, connection):
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "UPDATE tblGameInvites "
    query += f"SET fldIsRejected = 1, fldAcknowledgeTimestamp = \"{time}\", pfkRequester = \"{fromPlayer}\", pfkAddressee = \"{toPlayer}\" "
    query += f"WHERE pmkGameInviteId = {str(gameInviteID)} AND pfkRequester = \"{fromPlayer}\" AND pfkAddressee = \"{toPlayer}\" AND fldIsAccepted = 0 AND fldIsRejected = 0"
    
    cursor.execute(query)    
    connection.commit()

##### Functions to INSERT/CREATE New Data #####
def insertNewGameInvite(fromPlayer, toPlayer, cursor, connection):

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "INSERT INTO tblGameInvites (pfkRequester, pfkAddressee, fldRequestTimestamp) "
    query += f"VALUES (\"{fromPlayer}\", \"{toPlayer}\", \"{time}\")"
    
    cursor.execute(query)
    connection.commit() 