import mysql.connector
from mysql.connector.constants import ClientFlag
import ssl

#db_password = 'William123'
def getsqlstring(index): 
    sql_query_template = {}
    sql_query_template['selectAll'] = "SELECT * FROM DCRUsers"
    sql_query_template['selectUser'] = "SELECT * FROM DCRUsers where Email = '{email}' "
    sql_query_template['insertUser'] = "INSERT INTO DCRUsers VALUES ('{uid}','{email}','Patient','Test') "
    sql_query_template['insertTreatment'] = "INSERT INTO behandlinger VALUES ({id},'{email}','Patient',300,0,'{treatment}','{description}') "
    sql_query_template['insertDiagnostic'] = "INSERT INTO diagnosticeringer VALUES ({id}, '{email}','Patient',300,0,'{treatment}','{description}') "
    sql_query_template['updateUID'] = "UPDATE DCRUsers SET UId = '{uid}' WHERE Email = '{email}' "
    sql_query_template['set'] = "SET SQL_SAFE_UPDATES = 0 "
    sql_query_template['getbehandlingerExpenses'] = "SELECT SUM(Price) from behandlinger where Email = '{email}' and Payed=0 GROUP BY Email"
    sql_query_template['getdiagnosticeringerExpenses'] = "SELECT SUM(Price) from diagnosticeringer where Email = '{email}' and Payed=0 GROUP BY Email"
    sql_query_template['getDiagnosticResults'] = "SELECT Price, Payed, Behandling, Beskrivelse from diagnosticeringer where Email = '{input}' "
    sql_query_template['getBehandlingsResults'] = "SELECT Price, Payed, Behandling, Beskrivelse from behandlinger where Email = '{input}' "
    
    sql_query_template['getDiagnosticResultsID'] = "SELECT Price, Payed, Behandling, Beskrivelse from diagnosticeringer where UId = {input} "
    sql_query_template['getBehandlingsResultsID'] = "SELECT Price, Payed, Behandling, Beskrivelse from behandlinger where UId = {input} "

    return sql_query_template[index]


def updateUid(_uid, _emailInput): 
    execute_query(getsqlstring("set"))
    execute_query(getsqlstring("updateUID").format(email=_emailInput, uid=_uid))
    

def getTotalExpenses(_email): 
    treatment = execute_query(getsqlstring("getbehandlingerExpenses").format(email=_email) ).fetchone()
    diagnostic = execute_query(getsqlstring("getdiagnosticeringerExpenses").format(email=_email) ).fetchone()
    res = 0 
    if treatment is not None: 
        res += treatment[0]
    if diagnostic is not None: 
        res += diagnostic[0]

    return res


def getDiagnosticResults(_input, id=False): 
    if id: 
        diagnostic = execute_query(getsqlstring("getDiagnosticResultsID").format(input=_input) ).fetchall()
    else:    
        diagnostic = execute_query(getsqlstring("getDiagnosticResults").format(input=_input) ).fetchall()
    return diagnostic

def getBehandlingsResults(_input, id=False): 
    if id: 
        BehandlingsResults = execute_query(getsqlstring("getBehandlingsResultsID").format(input=_input) ).fetchall()
    else: 
        BehandlingsResults = execute_query(getsqlstring("getBehandlingsResults").format(input=_input) ).fetchall()
    return BehandlingsResults


def insertTreatment(_uid, _emailInput,  _log, _description): 
    execute_query(getsqlstring("insertTreatment").format(id= _uid,  email=_emailInput , treatment = _log , description=_description))

def insertDiagnostic(_uid, _emailInput,  _log, _description): 
    execute_query(getsqlstring("insertDiagnostic").format(id= _uid, email=_emailInput, treatment = _log, description=_description))
    

def insertNewInstanceInDB(_uid, _emailInput): 
    execute_query(getsqlstring("insertUser").format(email=_emailInput, uid=_uid))
    

def getInstanceFromDB(_emailInput): 
    role = execute_query(getsqlstring("selectUser").format(email=_emailInput))
    return role.fetchall()


def db_connect():
    cnx = mysql.connector.connect(user="WAOST",
        password="William123",
        host="tasklistdatabase1.mysql.database.azure.com",
        port=3306,
        database="tasklistdatabase1",
        ssl_ca="C:\\Users\\toros\\Documents\\beeware-tutorial\\helloworld\\src\\helloworld\\resources\\DigiCertGlobalRootCA.crt.pem",
        ssl_disabled=False)
    print(f'[i] cnx is connected: {cnx.is_connected()}')
    return cnx



def execute_query(sqlString): 
    try:
        res = None
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        print('SQL STRING:  ',sqlString)

        cursor.execute(sqlString)
        if sqlString.startswith("SELECT"):
            res = cursor
        if sqlString.startswith("INSERT") or sqlString.startswith("UPDATE") or sqlString.startswith("SET"):
            cnx.commit()
        cursor.close()
        cnx.close()
        return res
    except Exception as ex:
        print(f'[x] error! {ex}')
        return None





