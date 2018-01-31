from flask import Flask
from flask import render_template
import urllib, json

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
    projectResponse = urllib.urlopen(projectURL)
    projectData = json.loads(projectResponse.read())
    
    #get project job data
    projectJobsURL = "http://gitlab.healthnow.org/api/v4/projects/"+str(application_id)+"/jobs?private_token=6Qg85yGzGV_hGCyLxWts";
    projectJobsResponse = urllib.urlopen(projectJobsURL)
    projectJobsData = json.loads(projectJobsResponse.read())
    numberOfRuns = len(projectJobsData)
    #get test case data
    
    
    
    return render_template('applications.html', projectData=projectData, projectJobsData=projectJobsData, numberOfRuns=numberOfRuns)