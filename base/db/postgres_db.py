#!/usr/bin/env python3

import psycopg2


# Below function establishes connection with the database
def createPostgresDBConnection():
    # Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
    print("...trying to connect to postgres db")
    connection = psycopg2.connect(user = "biocapture",
                                  password = "W3lcomeB10sm@t2019#",
                                  host = "10.152.89.180",
                                  port = "5445",
                                  database = "biocapture")
    #cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print("...database connection successful... details below")
    print ( connection.get_dsn_parameters(),"\n")
    return connection


def commitOperation(connection):
    if(connection):
        connection.commit()


def closeDBConnection(connection):
    if(connection):
        connection.close()
        print("PostgreSQL connection is closed")


def getDBCursor(connection):
    if(connection):
        return connection.cursor()


def writeManySSLLogs(connection, logList):
    
    sql = """INSERT INTO web_server_logs(source_ip,destination_ip,destination_port,
        request_date,request_time,request_method,request,request_size)
        VALUES ( :sourceIp, :destinationIp, :destinationPort, :requestDate, :requestTime , 
        :requestMethod, :request, :responseCode)"""
    try:
        connection.cursor().executemany(sql, logList)
        connection.commit()
    except (Exception, psycopg2.Error) :
        # Rollback in case there is any error
        print("Error while writing to the postgres database")
        connection.rollback()

