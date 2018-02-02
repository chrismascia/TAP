from flask import Flask
from flask import render_template
import urllib2, json, xmltodict
import xml.etree.ElementTree as ET
from urllib2 import Request, urlopen


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/applications')
def applications():
    return 'Applications'

@app.route('/applications/<int:application_id>')
def show_application(application_id):
        
    #get project data
    projectURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"?private_token=6Qg85yGzGV_hGCyLxWts";
    projectResponse = urllib2.urlopen(projectURL)
    projectData = json.loads(projectResponse.read())
    
    #get project job data
    projectJobsURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs?private_token=6Qg85yGzGV_hGCyLxWts";
    projectJobsResponse = urllib2.urlopen(projectJobsURL)
    projectJobsData = json.loads(projectJobsResponse.read())
    numberOfRuns = len(projectJobsData)
    
    #get test case data
    #get test output.xml
    outputXMLURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs/"+str(projectJobsData[0]["id"])+"/artifacts/artifacts/output.xml"
    outputXMLRequest = Request(outputXMLURL)
    outputXMLRequest.add_header('PRIVATE-TOKEN', '6Qg85yGzGV_hGCyLxWts')
    try:
        outputXMLFile = urllib2.urlopen(outputXMLRequest)
        outputXMLData = outputXMLFile.read()
        outputXMLFile.close()
        outputXMLData = xmltodict.parse(outputXMLData)
        testCaseCount = len(outputXMLData["robot"]["statistics"]["suite"]["stat"])
    except IOError, e:
        outputXMLData = ""
        testCaseCount = 0
    
    
    
   
    return render_template('application.html', projectData=projectData, projectJobsData=projectJobsData, numberOfRuns=numberOfRuns, testCaseCount=testCaseCount)

@app.route('/applications/<int:application_id>/job/<int:job_id>')
def show_job(application_id, job_id):

    #get project data
    projectURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"?private_token=6Qg85yGzGV_hGCyLxWts";
    projectResponse = urllib2.urlopen(projectURL)
    projectData = json.loads(projectResponse.read())

    #get the job details
    jobURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs/"+str(job_id)+"?private_token=6Qg85yGzGV_hGCyLxWts";
    jobResponse = urllib2.urlopen(jobURL)
    jobData = json.loads(jobResponse.read())
    
    print "printing!"
    
    #get test output.xml
    outputXMLURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs/"+str(job_id)+"/artifacts/artifacts/output.xml"
    outputXMLRequest = Request(outputXMLURL)
    outputXMLRequest.add_header('PRIVATE-TOKEN', '6Qg85yGzGV_hGCyLxWts')
    try:
        outputXMLFile = urllib2.urlopen(outputXMLRequest)
        outputXMLData = outputXMLFile.read()
        outputXMLFile.close()
        outputXMLData = xmltodict.parse(outputXMLData)
        testCaseCount = len(outputXMLData["robot"]["statistics"]["suite"]["stat"])
    except IOError, e:
        outputXMLData = ""
        testCaseCount = 0
           
    return render_template('job.html', outputXMLData=outputXMLData, jobData=jobData, projectData=projectData, testCaseCount=testCaseCount)

@app.route('/applications/<int:application_id>/job/<int:job_id>/details')
def show_report(application_id, job_id):
    reportURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs/"+str(job_id)+"/artifacts/artifacts/log.html"
    reportRequest = Request(reportURL)
    reportRequest.add_header('PRIVATE-TOKEN', '6Qg85yGzGV_hGCyLxWts')
    reportHTML = urllib2.urlopen(reportRequest).read()
    reportHTML = reportHTML.replace("selenium-screenshot-", "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs/"+str(job_id)+"/artifacts/artifacts/selenium-screenshot-");
    
    return reportHTML