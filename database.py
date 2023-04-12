def selectUser(username, cursor):
    query = "SELECT pmkUsername FROM tblUsers WHERE pmkUsername = \"" + username + "\""
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result[0] if len(result) > 0 else ""
    
def insertNewInvite(fromPlayer, toPlayer, connection, cursor):
    query = "INSERT INTO GameRequests (requester_id, addressee_id) VALUES (\""
    query += fromPlayer + "\", \"" + toPlayer + "\")"
    
    cursor.execute(query)
    connection.commit() 
  
    
# def acceptInvite(fromPlayer, toPlayer):