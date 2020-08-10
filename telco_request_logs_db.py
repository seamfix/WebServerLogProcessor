#!/usr/bin/env python3

import re
import operator
import csv
import os
from base.db.postgres_db import createPostgresDBConnection
from base.db.postgres_db import writeManySSLLogs
from base.db.postgres_db import closeDBConnection
from datetime import datetime
import subprocess
import sys

log_location = "logs"
backup_location = "logs/backup"
connection = None
rowCount = 0
#regex = r'([\d]{1,2}\/[\a-zA-Z]{3,}\/[\d]{2,4}):([\d]{1,2}).*"([A-Z]+) ([\/\w-]+)'
regex = r'^([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3})[ a-z:]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})[ a-z:\-\[]*(\d{1,2}/\w{3}/\d{4}):(\d{1,2}:\d{1,2})[ 0-9a-z:\]\+\"]*([A-Z]+)[ ]*([/\w-]+)[\w\W]*[A-Z]{4,5}[/\d\.\"]+ (\d{3,4})'
#complete = r'^([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3})[ a-z:]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})[ a-z:\-\[]*(\d{1,2}/\w{3}/\d{4}):(\d{1,2}:\d{1,2})[ 0-9a-z:\]\+\"]*([A-Z]+)[ ]*([/\w-]+)([\w\W]*)([A-Z]{4,5}[/\d\.\"]+) (\d{1,4})'
error_log_regex = r'^(\d{4}/\d{1,2}/\d{1,2}) (\d{1,2}:\d{1,2}).*client: ([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}).*request: \"([A-Z]+) ([/\w-]+).*upstream: \"[a-z:/]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})'
logList = []
channel = ""
header_set = False


def loadDB():
  return createPostgresDBConnection()


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

      request = result[7]
      if "/biocapture/config/settings" in result[7]:
        request = "/biocapture/config/settings"

      if "/biocapture/resync" in result[7]:
        request = "/biocapture/resync"

      #logList.append( (datetime.today(),result[1],result[2],result[3],request,'172.16.5.232') )
      #below line packs the request items into a tuple and append the tuple to the list
      logList.append( (result[1],result[2],result[3],result[4],result[5], result[6],request, result[8], channel ) )
      rowCount = rowCount + 1
      
    log.close()




def loadLogs():
  log_files = os.listdir(log_location) 
  
  for log in log_files:
    
    if ("ssl.log" not in log) and ("ssl-error.log" not in log) :
       continue

    if "ssl.log" in log :
      #reading successful SSL logs
      print(log)
      read_SSL_Log(log_location + "/" + log)

      #below line inserts each log entry into an Oracle database
      #writeManySSLLogs(connection, logList)
      #print(logList)
      generateReport()
      print("Row count for file {} is {}".format(log_location + "/" + log, rowCount))

    if "ssl-error.log" in log :
      #reading successful SSL logs
      print("No suppport yet for reading SSL error log files")
      

      #below line backs up the logfilethat was processed
    
    backupLogFile(log)
    
    
def generateReport():
  global header_set
  
  if not header_set :
    logList.insert(0,("source_ip","destination_ip","destination_port","request_date","request_time","request_method","request","response_code","channel"))
    header_set = True

   #os.path.expanduser('~') + '/report_file.csv'
  with open(log_location + "/" + 'reports/glo-ssl-requests_' + channel + '.csv', mode='a',encoding='UTF-8') as report_file :
    writer = csv.writer(report_file)
    writer.writerows(logList)
    report_file.close()
    print("Report generated")


def backupLogFile(file):
  subprocess.call(["mv", log_location + "/" + file, backup_location + "/" + file])
  print("File backup completed")




if __name__ == "__main__":
  print("The inputed arguments are : " + str( sys.argv ) )

  if len(sys.argv) <= 1 :
     print("No log or log folder was specified. Now using default log location")

  # You use the first parameter to specify whether the logs are either from DMZ or LAN server.
  if len(sys.argv) == 2 :
     channel = sys.argv[1]

  # You use the first parameter to specify the path to read the logs from
  if len(sys.argv) == 3 :
     channel = sys.argv[1]
     log_location = sys.argv[2]

  # You use the first parameter to specify the path to backup the processed logs
  if len(sys.argv) == 4 :
     channel = sys.argv[1]
     log_location = sys.argv[2]
     backup_location = sys.argv[3]
      

  #connection = loadDB()
  loadLogs()
  #closeDBConnection(connection)
