#!/usr/bin/env python3

import re
import operator
import csv
import os
from base.db.db_calls import createDBConnection
from base.db.db_calls import writeManySSLLogs
from base.db.db_calls import closeDBConnection
from datetime import datetime
import subprocess

connection = None
rowCount = 0
regex = r'([\d]{1,2}\/[\a-zA-Z]{3,}\/[\d]{2,4}):([\d]{1,2}).*"([A-Z]+) ([\/\w-]+)'
logList = []

def loadDB():
  return createDBConnection()


def read_SSL_Log(file):
  global rowCount
  global logList
  rowCount = 0
  logList = []

  with open(file, mode='r',encoding='UTF-8') as log:
    for line in log.readlines():
      result = re.search(regex, line)
      
      if result == None :
        continue

      request = result[4]
      if "/biocapture/config/settings" in result[4]:
        request = "/biocapture/config/settings"

      if "/biocapture/resync" in request:
        request = "/biocapture/resync"

      logList.append( (datetime.today(),result[1],result[2],result[3],request,'172.16.5.232') )
      rowCount = rowCount + 1
      
    log.close()




def loadLogs():
  log_files = os.listdir("logs/") 
  
  for log in log_files:
    if "ssl" not in log :
      continue
    
    #reading successful SSL logs
    read_SSL_Log("logs/" + log)

    #below line inserts each log entry into an Oracle database
    writeManySSLLogs(connection, logList)
    connection.commit()
    print("Row count for file {} is {}".format("logs/" + log, rowCount))

    #below line backs up the logfilethat was processed
    backupLogFile(log)
    

def backupLogFile(file):
  subprocess.call(["mv", "logs/"+file, "logs/backup/"+file])
  print("file move completed")

connection = loadDB()
loadLogs()
closeDBConnection(connection)
