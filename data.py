# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 14:43:59 2015
@author: Audrey
GUI
"""

import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.tools as tls
import urllib2
from plotly.graph_objs import *
import graph_functions as g

class Race:
    
    def __init__(self, name):
        self.name = name
        self.runs = []
        self.runners = []
        self.distance = 0
        
    def add_runner(self, runner):
        self.runners.append(runner)
        
    def add_run(self, run):
        self.runs.append(run)
    
    def race_distance(self, distance):
        self.distance = distance
        
    def get_runners(self):
        all_runners = []
        for run in self.runs:
            all_runners.append(run.name)
        self.runners = set(all_runners)
        #sort(self.runs, key = attrgetter('age'))
        return sorted(self.runners)    
        
    def __repr__(self):
        return self.name
        
    def __cmp__(self, other):
        if (self.name < other.name):
            return -1
        if (self.name > other.name):
            return 1
        else:
            return 0
    
class Runner:
    
    def __init__(self, name):
        self.name = name
        self.runs = []
        self.median = 0 #median
        self.races = [] #list of races
        self.num = 0 #number of races
        self.total = 0 #total miles
        self.count = 0 #count of runs
        self.avg = 0 #average mileage/run
        self.dur = 0 #duration
        self.mpd = 0 #miles/total days
        self.rpd = 0 #runs/total days

    def add_run(self, run):
        self.runs.append(run)

    def make_data(self):
        self.avg_miles()
        self.num_races()
        self.running_time()
        self.frequencies()

    def frequencies(self):
        if (self.dur != 0):
            mpd = self.total/self.dur
            rpd = float(self.count)/self.dur
            self.mpd = mpd
            self.rpd = rpd

    def avg_miles(self):
        run_distances = []
        miles = 0.00
        count = 0
        counted = []
        for run in self.runs:
            if run.date not in counted:
                counted.append(run.date)
                miles += float(run.distance)
                count += 1
                run_distances.append(run.distance)
        self.median = np.median(run_distances)
        print self.median
        self.count = count
        self.total = miles
        self.avg = miles/count
        return miles/count

    def num_races(self):
        races = 0
        race_names = []
        for run in self.runs:
            if run.race not in race_names:
                races += 1
                race_names.append(run.race)
        self.num = races
        self.races = race_names
        return races 

    def running_time(self):
        FIRST = self.runs[0]
        LAST = self.runs[-1]
        x = LAST.date - FIRST.date
        self.dur = x.days
        return self.dur
        
    def __cmp__(self, other):
        
        if (self.name < other.name):
            return -1
        if (self.name > other.name):
            return 1
        else:
            return 0

class Run:
    
    miles = True
    
    def __init__(self, race, name, date, distance):
        self.race = race
        self.name = name.lower()
        self.date = date
        self.distance = distance
        
        #make these point to the class objects not strings
             
    def make_date(self):        
        date_time = self.date.split(' ')
        date_time = filter(lambda x: x.strip(' ')!='', date_time)
        d = date_time[0].split('-')
        time = date_time[1] #time, unused for now
        self.date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    
    def miles(self):
        self.distance = self.distance*(0.000621371)
        
    def kilometers(self):
        self.distance = self.distance/1000
        
    def get_runner(self):
        return self.name
        
    def race(self):
        """race that run is in"""
        return self.race
    
    def toString(self):
        string = self.race + self.name + str(self.date) + str(self.distance)
        return string
        
    def __repr__(self):
        string = self.race + self.name + str(self.date) + str(self.distance)
        return string
        
    def __cmp__(self, other):
        '''runs are compared by date'''
        if (self.date < other.date):
            return -1
        if (self.date > other.date):
            return 1
        else:
            return 0

class Data:
    dataFile = 'submissions.csv'
    #pass true if you want to read from URL
    newFile = False
    miles = True
    x = []
    
    def __init__(self, newFile, miles):
        '''boolean newFile and miles. runs, races, and runners are lists that hold the raw data information'''
        self.newFile = newFile
        self.miles = miles
        self.runs = []
        self.races = []
        self.race_names = []
        self.runners = []
        self.runner_names = []
         
    def read_data(self, dataFile, *args):
        #read from URL
        if (self.newFile == True):
            print 'reading from url to csv'
            csv_writer = open(dataFile, 'wb')
            print "Starting to read from url"
            if args:
                url = args[0]
            else:
                #Get everything
                url = 'http://runwithme.blogads.com/api/list_submissions'
            csv_writer.write(urllib2.urlopen(url).read())
            csv_writer.close()
            print "Done reading from url"
        with open(dataFile, 'rb') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                this_run = Run(row[0], row[1].strip(' '), row[2], float(row[3]))
                if (self.miles == True):
                    this_run.miles()
                this_run.make_date()
                self.runs.append(this_run)
                self.people_list(this_run)
                self.race_list(this_run)
                #print this_run.toString()
            print 'done reading in file'
            #print 'Races: \n' + self.print_list(self.race_names)
            #print 'Runners: \n' + self.print_list(self.runner_names)
    
    def race_runners(self):
        for race in self.races:
            print race.get_runners()
            
    
    def race_list(self, this_run):
        """returns a list of races"""
        for race in self.races:
            if (race.name == str(this_run.race)):
                race.add_run(this_run)
                race.add_runner(this_run.get_runner())
        if str(this_run.race) not in self.race_names:
            this_race = Race(this_run.race)
            self.races.append(this_race)
            self.race_names.append(this_race.name)
            this_race.add_run(this_run)
            
        
    def people_list(self, this_run):
        """returns a list of people"""
        for runner in self.runners:
            if (runner.name == str(this_run.name)):
                runner.add_run(this_run)
        if str(this_run.name) not in self.runner_names:
            this_runner = Runner(this_run.name)
            self.runners.append(this_runner)
            self.runner_names.append(this_runner.name)
            this_runner.add_run(this_run)
    
    def print_list(self, x):
        to_string = ''
        n = 1
        x = sorted(x)
        for i in range(1, len(x)):
            to_string += str(n) + '. ' + x[i] + '\n'
            n = n+1
        return to_string
     
    def get_runner(self, x):
        for runner in self.runners:
            if (runner.name == x):
                #print runner.runs
                return runner
    
    def plot_now(self, x, y):
        print "printing x: \n"
        print x
        print "printing y: \n"
        print y
        trace = Scatter(
            x=x,
            y=y,
            mode='lines+markers'
        )
        data = Data([trace])
        return data

def main():
    try:
        credentials = tls.get_credentials_file()
    except:
        ## except credentials error and print for them to enter something
        credentials = {}
        credentials['username'] = raw_input("Plotly Username: ") ## get username
        credentials['api_key'] = raw_input("api key: ") ### get password
    try:
        py.sign_in(credentials['username'], credentials['api_key']) 
        print "let's read some data"        
        #data object
        t = Data(False, True)
        #read from file
        t.read_data('submissions.csv')
        return t
    except:
        print "was not able to sign into plotly"

