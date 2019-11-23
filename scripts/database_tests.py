from protocol import Server
from database import Database

if __name__ == "__main__":
    database = Database()
    #server = Server()
    print("--- happy path ---")
    #insert
    auto_key = database.insert("valor con clave autogenerada")
    print("insert",auto_key)
    #insert
    print("insert",database.insert("valor con clave de usuario",123))
    #list
    print("list",database.list())
    #peek
    print("peek",database.peek(auto_key))
    #peek
    print("peek",database.peek(123))
    #get
    print("get",database.get(auto_key))
    #get
    print("get",database.get(123))
    #update
    print("update",database.update(auto_key,"valor actualizado 1"))
    #update
    print("update",database.update(123,"valor actualizado 2"))
    #get
    print("get",database.get(auto_key))
    #get
    print("get",database.get(123))
    #delete
    print("delete",database.delete(auto_key))
    #delete
    print("delete",database.delete(123))
    #peek
    print("peek",database.peek(auto_key))
    #peek
    print("peek",database.peek(123))


    print("--- errors ---")
    #insert
    print("insert",database.insert("valor con clave de usuario",321))
    #insert
    print("insert",database.insert("valor con clave de usuario",321))
    #insert
    print("insert",database.insert("valor con clave de usuario","str key"))
    #insert
    print("insert",database.insert("valor con clave de usuario",-123))
    #insert
    print("insert",database.insert("valor con clave de usuario",0))
    #get
    print("get",database.get("str key"))
    #get
    print("get",database.get(-123))
    #get
    print("get",database.get(None))
    #get
    print("get",database.get(0))
    #update
    print("update",database.update("str key","valor actualizado"))
    #update
    print("update",database.update(-123,"valor actualizado"))
    #update
    print("update",database.update(None,"valor actualizado"))
    #update
    print("update",database.update(0,"valor actualizado"))
    #delete
    print("delete",database.delete("str key"))
    #delete
    print("delete",database.delete(-123))
    #delete
    print("delete",database.delete(0))
    #delete
    print("delete",database.delete(None))
    #list
    print("list",database.list())
    #peek
    print("peek",database.peek("str key"))
    #peek
    print("peek",database.peek(-123))
    #peek
    print("peek",database.peek(0))
    #peek
    print("peek",database.peek(None))
