
# coding: utf-8

# In[68]:


clientResultsFilename = 'client-results.txt'
serverResultsFilename = 'server-results.txt'
paramsFilename = 'params.txt'
parsedResultsFilename = 'parsed-results.csv'

print(clientResultsFilename, serverResultsFilename, paramsFilename, parsedResultsFilename)


# In[ ]:





# In[69]:


clientResultsFile = open(clientResultsFilename, "r")

# Search in client-results
currentRun = None
netIO = None
bandwidth = None
responseTime = None
results = dict()
for line in clientResultsFile.readlines():
    line = line.rstrip()
    if currentRun == None and line.startswith("run"):
        currentRun = line.split(" ")[1]
    elif line.startswith("Net I/O"):
        netIO = line.split(": ")[1].split("KB/s")[0]
    elif line.startswith("[  3]") and line.endswith("Mbits/sec"):
        bandwidth = line.split("   ")[2].split(" ")[0]
    elif line.startswith("Reply time [ms]"):
        responseTime = line.split(": ")[1].split(" ")[1]
    elif currentRun != None and line.startswith("run"):
        results[currentRun] = { "responseTime": responseTime, "netIO": netIO, "bandwidth": bandwidth }
#         print(currentRun, responseTime, netIO, bandwidth)
        currentRun = line.split(" ")[1]

# print(currentRun, responseTime, netIO, bandwidth)
results[currentRun] = { "responseTime": responseTime, "netIO": netIO, "bandwidth": bandwidth }


# In[70]:


serverResultsFile = open(serverResultsFilename, "r")

currentServerRun = None
utilIsNextLine = False
util = None
for line in serverResultsFile.readlines():
    line = line.rstrip()
    if currentServerRun == None and line.startswith("run"):
        currentServerRun = line.split(" ")[1]
    elif line.startswith("Utilization of core 0 is:"):
        utilIsNextLine = True
    elif utilIsNextLine == True:
        utilIsNextLine = False
        util = line
    elif currentServerRun != None and line.startswith("run"):
        results[currentServerRun]["CpuUtilization"] = util
        currentServerRun = line.split(" ")[1]
results[currentServerRun]["CpuUtilization"] = util


# In[71]:


paramsFile = open(paramsFilename, "r")

for line in paramsFile.readlines():
    line = line.rstrip()
    splitted = line.split(" ")
    run = splitted[1][:-1]
    sessions = splitted[2].split("=")[1]
    period = splitted[3].split("=")[1]
    i = 0
    for i in range(0, 4):
        id = run + "-" + str(i)
        results[id]["Sessions"] = sessions
        results[id]["Period"] = period
        i = i + 1


# In[80]:


parsedResultsFile = open(parsedResultsFilename, "w")

parsedResultsFile.write("Run #, Period, Number of Sessions, Response Time, CPU Utilization, Network Bandwidth, Network I/O\n")
for key, value in results.items():
    parsedResultsFile.write(key.replace("-", "_") + ",")
    parsedResultsFile.write(value["Period"] + ",")
    parsedResultsFile.write(value["Sessions"] + ",")
    parsedResultsFile.write(value["responseTime"] + ",")
    parsedResultsFile.write(value["CpuUtilization"] + ",")
    parsedResultsFile.write(value["bandwidth"] + ",")
    parsedResultsFile.write(value["netIO"] + "\n")

parsedResultsFile.close()


# In[110]:


parsedResultsFile = open(parsedResultsFilename, "r")

currentResultsRun = None
periodSum = 0
sessionsSum = 0
responseSum = 0
cpuUtilSum = 0
bandwidthSum = 0
networkSum = 0 
count = 0

def addToValues(p, s, r, u, b, n):
    global periodSum, sessionsSum, responseSum, cpuUtilSum, bandwidthSum, networkSum, count
    periodSum = periodSum + float(p)
    sessionsSum = sessionsSum + float(s)
    responseSum = responseSum + float(r)
    cpuUtilSum = cpuUtilSum + float(u)
    bandwidthSum = bandwidthSum + float(b)
    networkSum = networkSum + float(n)
    count = count + 1

def clearValues():
    global periodSum, sessionsSum, responseSum, cpuUtilSum, bandwidthSum, networkSum, count
    periodSum = 0
    sessionsSum = 0
    responseSum = 0
    cpuUtilSum = 0
    bandwidthSum = 0
    networkSum = 0 
    count = 0
    
def calculateAverage(num, count):
    return str(num / count)

def generateAverages():
    global periodSum, sessionsSum, responseSum, cpuUtilSum, bandwidthSum, networkSum, count
    periodAvg = calculateAverage(periodSum, count)
    sessionsAvg = calculateAverage(sessionsSum, count)
    responseAvg = calculateAverage(responseSum, count)
    cpuUtilAvg = calculateAverage(cpuUtilSum, count)
    bandwidthAvg = calculateAverage(bandwidthSum, count)
    networkAvg = calculateAverage(networkSum, count)
    return {
        "Period": periodAvg,
        "Sessions": sessionsAvg,
        "responseTime": responseAvg,
        "CpuUtilization": cpuUtilAvg,
        "bandwidth": bandwidthAvg,
        "netIO": networkAvg
    }
    
finalResults = dict()
for line in parsedResultsFile.readlines():
    line = line.rstrip()
    if line.startswith("Run"):
        continue
    run, period, sessions, response, cpuUtil, bandwidth, network = line.split(",")
    resultsRun = run.split("_")[0]
    if currentResultsRun == None:
        currentResultsRun = resultsRun
        addToValues(period, sessions, response, cpuUtil, bandwidth, network)
    elif currentResultsRun == resultsRun:
        addToValues(period, sessions, response, cpuUtil, bandwidth, network)
    elif currentResultsRun != resultsRun:
        finalResults[currentResultsRun] = generateAverages()
        currentResultsRun = resultsRun 
        clearValues()
        addToValues(period, sessions, response, cpuUtil, bandwidth, network)

finalResults[currentResultsRun] = generateAverages()
print(finalResults)


# In[111]:


averagedResultsFile = open("AveragedResults.csv", "w")

averagedResultsFile.write("Run #, Period, Number of Sessions, Average Response Time, Average CPU Utilization, Average Network Bandwidth, Average Network I/O\n")
for key, value in finalResults.items():
    averagedResultsFile.write(key + ",")
    averagedResultsFile.write(value["Period"] + ",")
    averagedResultsFile.write(value["Sessions"] + ",")
    averagedResultsFile.write(value["responseTime"] + ",")
    averagedResultsFile.write(value["CpuUtilization"] + ",")
    averagedResultsFile.write(value["bandwidth"] + ",")
    averagedResultsFile.write(value["netIO"] + "\n")

averagedResultsFile.close()


# In[ ]:


averagedResultsFile = open("AveragedResults.csv", "r")
averagedResultsFile.read()

