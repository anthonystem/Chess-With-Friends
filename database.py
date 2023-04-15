from passlib.hash import bcrypt
from datetime import datetime

def verifyPassword(username, inputPassword, cursor):
    # Get password hash from database.
    userData = selectUser(username, cursor)
    # Return False is no user exists.
    if len(userData) == 0:
        return False
    
    encrypted = userData[0][1]
    print(encrypted)

    # Verify input password.
    if not bcrypt.verify(inputPassword, encrypted):
        return False
    
    return True

##### Functions to SELECT/FETCH Data #####
def selectUser(username, cursor):
    query = "SELECT * FROM tblUsers "
    query += f"WHERE pmkUsername = \"{username}\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return list(result)

def selectSearchUsers(searchString, termLimit, cursor):
    # Do not apply a query limit if supplied limit < 0.
    if termLimit < 0:
        query = "SELECT * FROM tblUsers "
        query += f"WHERE pmkUsername LIKE \"{searchString}%\""
    else:
        query = "SELECT * FROM tblUsers "
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

# Update User Statistics
def updateUserWins(username, delta, cursor, connection):
    query = "UPDATE tblUsers "
    query += f"SET fldWins = fldWins + {str(delta)} "
    query += f"WHERE pmkUsername = \"{username}\""

    cursor.execute(query)
    connection.commit()

def updateUserLosses(username, delta, cursor, connection):
    query = "UPDATE tblUsers "
    query += f"SET fldLosses = fldLosses + {str(delta)} "
    query += f"WHERE pmkUsername = \"{username}\""

    cursor.execute(query)
    connection.commit()

def updateUserStalemates(username, delta, cursor, connection):
    query = "UPDATE tblUsers "
    query += f"SET fldStalemates = fldStalemates + {str(delta)} "
    query += f"WHERE pmkUsername = \"{username}\""

    cursor.execute(query)
    connection.commit()


##### Functions to INSERT/CREATE New Data #####
def insertNewGameInvite(fromPlayer, toPlayer, cursor, connection):

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    query = "INSERT INTO tblGameInvites (pfkRequester, pfkAddressee, fldRequestTimestamp) "
    query += f"VALUES (\"{fromPlayer}\", \"{toPlayer}\", \"{time}\")"
    
    cursor.execute(query)
    connection.commit() 