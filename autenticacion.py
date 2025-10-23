from ldap3 import Server, Connection, ALL, NTLM


def usuarioldap(username,passw):

    try:

        #dccra01.ayuntamiento.svq 10.70.17.180
        #dccra02.ayuntamiento.svq 10.70.24.190
        #dcran01.ayuntamiento.svq 10.70.24.180
        server = Server('ldap://10.70.24.190:389', get_info=ALL)
        print (server)
        conn = Connection(server, user="ayuntamiento.svq\\"+username, password=passw, authentication=NTLM)
        print (conn)
        salida=conn.bind()
        print (salida)
        conn.closed

        print (salida)

        return salida

    except:

        return False

print (usuarioldap("ranavang","Cigarreras03"))

