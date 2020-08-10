#!/usr/bin/env python3

import re
import operator
import csv
import os


file_types = ('SSL','ERROR','ACCESS')
regex = r'([\d]{1,2}\/[\a-zA-Z]{3,}\/[\d]{2,4}):([\d]{1,2}).*"[A-Z]+ ([\/\w-]+)'
total_daily_requests = {}
daily_request_count = {}
report_data = []
total_request_report_data = []
raw_data = []

def readFromLog(file):
  with open(file, mode='r',encoding='UTF-8') as log:
    for line in log.readlines():
      result = re.search(regex, line)
      #print(result)
      if result == None :
        continue

      if result[1] not in total_daily_requests :
        total_daily_requests[result[1]] = 0

      if result[1] not in daily_request_count :
        daily_request_count[result[1]] = {}
      
      request = result[3]
      if request not in daily_request_count[result[1]] :
        if "/biocapture/config/settings" in result[3]:
          request = "/biocapture/config/settings"

        if "/biocapture/resync" in request:
          request = "/biocapture/resync"

        daily_request_count[result[1]][request] = 0

      raw_data.append((result[1],result[2],result[3]))
      total_daily_requests[result[1]] = total_daily_requests[result[1]] + 1
      daily_request_count[result[1]][request] = daily_request_count[result[1]][request] + 1

    log.close()


def parseReportData():
  
  for day in daily_request_count:
    
    sorted_requests = sorted(daily_request_count[day].items(),key=operator.itemgetter(1), reverse=True)
    transformed_user_requests = []
    
    for user_row in sorted_requests :
        transformed_user_requests.append((day, user_row[0], user_row[1]))

    report_data.extend(transformed_user_requests)

  
  sorted_requests = sorted(total_daily_requests.items(),key=operator.itemgetter(0), reverse=True)
  total_request_report_data.extend(sorted_requests)
    


def generateReport():

  """Below code uses the daily request count data to generate a report in csv format"""
  report_data.insert(0,("Date","Request","Count"))
  
   #os.path.expanduser('~') + '/report_file.csv'
  with open('reports/ssl_requests.csv', mode='w',encoding='UTF-8') as report_file :
    writer = csv.writer(report_file)
    writer.writerows(report_data)
    report_file.close()

  """Below code uses the total daily request data to generate a report in csv format"""
  total_request_report_data.insert(0,("Date","Total Count"))
  
   #os.path.expanduser('~') + '/report_file.csv'
  with open('reports/total_ssl_requests.csv', mode='w',encoding='UTF-8') as report_file :
    writer = csv.writer(report_file)
    writer.writerows(total_request_report_data)
    report_file.close()


  raw_data.insert(0,("Date","Hour", "Request"))
  with open('reports/raw_requests.csv', mode='w',encoding='UTF-8') as report_file :
    writer = csv.writer(report_file)
    writer.writerows(raw_data)
    report_file.close()
  


def loadLogs():
  log_files = os.listdir("logs/") 
  
  for log in log_files:
    if "ssl" not in log :
      continue
    
    readFromLog("logs/" + log)




loadLogs()
parseReportData()
generateReport()
