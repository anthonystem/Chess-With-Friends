def selectUserId(username, cursor):
    query = "SELECT user_id FROM Users WHERE username = \"" + username + "\""
    
    cursor.execute(query)
    result = cursor.fetchall()[0]
    
    return result
    
def insertNewInvite(fromPlayer, toPlayer, connection, cursor):
    query = "INSERT INTO GameRequests (requester_id, addressee_id) VALUES (\""
    query += fromPlayer + "\", \"" + toPlayer + "\")"
    
    cursor.execute(query)
    connection.commit() 
  
    
# def acceptInvite(fromPlayer, toPlayer):