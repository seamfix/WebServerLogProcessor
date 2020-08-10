#!/usr/bin/env python3


import cx_Oracle
import random
from datetime import datetime


# Below function establishes connection with the database
def createOracleDBConnection():
    # Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
    return cx_Oracle.connect("biocapture", "s3@MF1x#SEP!B1OMTn*s3PT17", "10.1.232.232:1521/bsm_p1_stb.mtn.com.ng")
    

# Below function retrieves SSL logs from the database.
def get_SSL_Log(dbCursor, param):

    try:
        dbCursor.execute("""
                SELECT msisdn, unique_id,create_date, activationstatusenum FROM bfp_sync_log
                WHERE msisdn = :msisdn""",msisdn = '08030491762')
        
        for msisdn, unique_id,create_date, activation_status in dbCursor:
            print("Values:", msisdn, unique_id,create_date, activation_status)

    except:
        # Rollback in case there is any error
        dbCursor.rollback()
        
def writeManySSLLogs(connection, logList):
    
    sql = """INSERT INTO web_server_ssl_logs(source_ip,destination_ip,destination_port,
        request_date,request_time,request_method,request,request_size)
        VALUES ( :createDate, :reqDate, :reqHour, :reqMethod, :req , :sourceServer)"""
    try:
        connection.cursor().executemany(sql, logList)
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        connection.rollback()


def writeManySSLLogs2(connection, logList):
    
    sql = """INSERT INTO web_server_ssl_logs(create_date, request_date, request_hour,
        request_method, request, source_server)
        VALUES ( :createDate, :reqDate, :reqHour, :reqMethod, :req , :sourceServer)"""
    try:
        connection.cursor().executemany(sql, logList)
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        connection.rollback()


def writeManyErrorLogs(connection, logList):
    
    sql = """INSERT INTO web_server_error_logs(create_date, root_cause, error_message,
         request_date, source_ip)
        VALUES ( :createDate, :rootCause, :errorMessage, :reqDate, :sourceIP)"""
    try:
        connection.cursor().executemany(sql, logList)
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        connection.rollback()


# Below function writes SSL logs from the database.
def write_SSL_Log(connection, param):
    # Prepare SQL query to INSERT a record into the database.
    "insert into MyTable values (:idbv, :nmbv)", [1, "Fredico"]
    sql = "INSERT INTO web_server_ssl_logs(create_date, request_date, request_hour, \
        request_method, request, source_server) \
        VALUES ( :createDate, :reqDate, :reqHour, :reqMethod, :req , :sourceServer)"
    try:
        connection.cursor().execute(sql, [ datetime.today(), param[0], param[1], param[2], param[3], param[4]])
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        connection.rollback()

def commitOperation(connection):
    connection.commit()

def closeDBConnection(connection):
    connection.close()

    


