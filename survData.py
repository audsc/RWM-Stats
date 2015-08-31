# -*- coding: utf-8 -*-

import urllib2
import csv
import codecs
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls
import numpy as np
from scipy import stats
import pandas as pd
import graph_functions as g
import data as d


class Survey:
    def __init__(self, info):
        self.name = ''
        self.survey = ['---place holder---', info[9], info[10], info[11], info[12], info[13], info[14], info[15], info[16], info[17], info[18], info[19]]
        self.ID = info[0]
    
    def makeName(self, first, last):
        first = first.lower()
        last = last.lower()
        name = (first + last).replace(" ", "")
        ids = ['3856740724', '3860877379', '3862687708']
        if self.ID in ids:
            name = ''
        self.name = name
        return self.name

    def answers(self, index):
        i = 1
        while (i<7):
            option = 0
            for item in index[i]:
                if (self.survey[i] == item):
                    self.numbs[i] = option
                option+=1
            i+1
        print self.numbs
                
class Respondent:
    def __init__(self, survey, runner):
        self.ID = survey.ID
        self.name = survey.name
        self.survey = survey.survey
        self.runner = runner
        self.runs = runner.runs
        self.count = runner.count
        self.races = runner.races
        self.num = runner.num
        self.total = runner.total
        self.avg = runner.avg
        self.dur = runner.dur
        self.mpd = runner.mpd
        self.rpd = runner.rpd
        self.median = runner.median
        #from the survey:
        self.age = 0 #age
        self.sex = None
        self.starter = 0

    def makeAge(self):
        input = self.survey[10]
        input = input.replace(" ", "")
        if (input!= ""):
            age = int(input)
            self.age = age

    def makeGender(self):
        input = self.survey[11]
        ll = input.lower().replace(" ", "")
        if (len(ll)==1):
            if 'f' in ll:
                sex = 'female'
            if 'm' in ll:
                sex = 'male'
        else:
            if 'female' in ll:
                sex = 'female'
            if 'male' in ll:
                sex = 'male'
            else:
                sex = None
        self.sex = sex

    def addRuns(self, runs):
        self.runs = sorted(runs)
        return runs

    def getRuns(self):
        return self.runs

    def getSurvey(self):
        return self.survey

    def get_start(self):
        if (self.survey[5] == 'Yes'):
            self.starter = 1
        elif (self.survey[5] == 'No'):
            self.starter = 0
        else:
            self.starter = 2
    
    def __repr__(self):
        string = self.name
        return string
'''
Has all of the respondents and also can put them into groups.
'''
class SurveyData:
    '''
    responses contains the list of respondent objects
    index contains the list of questions
    '''
    def __init__(self, index, respondents, names):
        self.INDEX = index
        self.QA = []
        self.responses = respondents
        self.names = names
        self.solo = []
        self.mid = []
        self.social = []
        self.no = []
        self.yes = []
        self.plan = []
        self.nr = []
        self.oa = []
        self.one = []
        self.small = []
        self.mid = []
        self.large = []
        
    def makeDictionary(self):
        QA = []
        for question in self.INDEX:
            print "printing question: ", question
            cat = {}
            for answer in question:
                #each question has a dictionary w/ range of options
                cat[answer] = []
            QA.append(cat)
        self.QA = QA
        return self.QA

    def groupSocial(self):
        mylist = self.INDEX
        print mylist
        solo = []
        mid = []
        social = []
        q1 = mylist[1]
        q2 = mylist[2]
        for response in self.responses:
            a1 = response.survey[1]
            a2 = response.survey[2]
            if ((a1 == q1[0]) | (a2 == q2[0])):
                solo.append(response)
            elif ((a1 == q1[1]) | (a2 == q2[1])):
                mid.append(response)
            else:
                social.append(response)
        self.solo = solo
        self.mid = mid
        self.social = social

    def groupQ2(self):
        mylist = self.INDEX
        q1 = mylist[2]
        one = []
        small = []
        mid = []
        large = []
        for response in self.responses:
            a1 = response.survey[2]
            if (a1 == q1[0]):
                one.append(response)
            if (a1 == q1[1]):
                small.append(response)
            if (a1 == q1[2]):
                mid.append(response)
            if (a1 == q1[3]):
                large.append(response)
        self.small = small
        self.mid = mid
        self.large = large

    def groupQ1(self):
        mylist = self.INDEX
        q1 = mylist[1]
        nr = []
        oa = []
        for response in self.responses:
            a1 = response.survey[1]
            if (a1 == q1[0]):
                nr.append(response)
            if (a1 == q1[1]):
                nr.append(response)
            if (a1 == q1[2]):
                oa.append(response)
            if (a1 == q1[3]):
                oa.append(response)
        self.nr = nr
        self.oa = oa

    def groupStarter(self):
        mylist = self.INDEX
        no = []
        yes = []
        plan = []
        for response in self.responses:
            if (response.starter == 0):
                no.append(response)
            elif (response.starter == 1):
                yes.append(response)
            else:
                plan.append(response)
        self.no = no
        self.yes = yes
        self.plan = plan

'''Compare all runners with the survey respondents'''
def compare_resp_all(sR, nR, aR):
    '''non responders'''
    all_avgs = []
    all_durs = []
    all_totals = []
    all_counts = []
    mpd_n = []
    all_runfreq = []
    all_names = []

    '''responders'''
    res_avgs = []
    res_durs  = []
    total_miles_list= []
    run_count_list = []
    duration_list = []
    mpd_s = []

    '''all'''
    durations = []
    totals = []
    mpds = []
    
    nn = 0
    print 'non responders \n'
    for runner in nR:
        #remove far outliers for total and duration
        if (runner.dur<185 and runner.total < 653 and runner.mpd<6.13):
        	all_avgs.append(runner.avg)
        	all_durs.append(runner.dur)
        	all_totals.append(runner.total)
        	all_counts.append(runner.count)
        	mpd_n.append(runner.mpd)
        	all_runfreq.append(runner.rpd)
        	all_names.append(runner.name)
        else:   
            print "Error on: " , runner.name , "duration: ", runner.dur, "total: ", runner.total, "run count: ", runner.count
        nn += 1
    ns = 0  
    print 'responders \n'   
    for response in sR:
        #remove outliers for duration and far outliers for distance
        if (response.dur<264 and response.total < 838 and response.mpd<4.82):
            res_avgs.append(response.avg)
            res_durs.append(response.dur)
            total_miles_list.append(response.total)
            run_count_list.append(response.count)
            duration_list.append(response.dur)
            mpd_s.append(response.mpd)
            ns += 1
            if (response.total > 2000):
                print 'name: ', response.name, 'total: ', response.total
    print 'all \n'
    for response in aR:
        durations.append(response.dur)
        totals.append(response.total)
        mpds.append(response.mpd)
        if (response.total > 2000):
            print 'name: ', response.name, 'total: ', response.total

    print "non responders: " , nn
    print "responders: " , ns

    t_statistic, p_value = stats.ttest_ind(mpd_n, mpd_s,equal_var=0)
    print "t-statistic: " , t_statistic
    print "p-value: " , p_value
    
    print 'NON-RESPONDENTS: '
    print 'count:' , len(mpd_n)
    print 'mean: ', np.mean(mpd_n)
    print 'std: ', np.std(mpd_n)

    #print 'lower: ', l , ' upper: ', u , ' IQR: ', iqr

    print 'SURVEY RESPONDENTS: '
    print 'count: ', len(mpd_s)
    print 'mean: ', np.mean(mpd_s)
    print 'std: ', np.std(mpd_s)
    fig = g.histogramT(all_durs, res_durs, durations, 'Non-responders', 'Responders', 'All')
    #plot_url = py.plot(fig, filename='Distribution of Duration of Use')

    #fig = histogramT(all_totals, total_miles_list, totals, 'Non-responders', 'Responders', 'All')
    #plot_url = py.plot(fig, filename='Distribution of Total Mileage')

    fig = g.histogramT(mpd_n, mpd_s, mpds, 'Non-responders', 'Responders', 'All')
    #fig = histogram(durations)
    plot_url = py.plot(fig, filename='Overall Mileage per Day  (without outliers')

    ####graph the average run length vs. the duration of RWM use
    title = 'average run length vs. duration of rwm use'
    #fig = scatterPlot(all_avgs, all_durs, 'average miles', 'duration on RWM', title, all_names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the frequency of runs (#runs/duration) vs. the duration of RWM use

    title = 'frequency vs. duration'
    #fig = scatterPlot(all_runfreq, all_durs, 'frequency', 'duration on RWM', title, all_names)
    #plot_url = py.plot(fig, filename=title)

'''basic graphs for the responses'''
def graph_responses(surveyResponders):
    real_races = []
    num_known_list = []
    gender_list = []
    run_avg_list = []
    run_count_list = []
    total_miles_list = []
    duration_list = []
    num_rwmRace_list = []
    total_frequencies = []
    run_frequency = []
    r_d = []
    names = []

    q1q3_durs = []
    q1q3_races = []
    q1q3_names = []
    q1q3_run_frequency = []
    q1q3_tf = []
    q1q3_totals = []

    for response in surveyResponders:
        #from survey:
        r = response.survey[3]
        r = int(r.strip('+'))
        real_races.append(r)
        
        num_known = response.survey[6]
        num_known = int(num_known.strip('+'))
        num_known_list.append(num_known)

        rd = response.survey[4]
        r_d.append(rd)
        
        gender = response.sex
        if (gender == None):
            gender = 'other/no response'
        gender_list.append(gender)

        #from the submissions data:

        run_avg_list.append(response.avg)
        total_miles_list.append(response.total)
        run_count_list.append(response.count)
        duration_list.append(response.dur)
        total_frequencies.append(response.mpd)
        run_frequency.append(response.rpd)
        num_rwmRace_list.append(response.num)

        names.append(response.name)

        if (response.dur<264 and response.total < 838):
            q1q3_durs.append(response.dur)
            q1q3_run_frequency.append(response.rpd)
            q1q3_tf.append(response.mpd)
            q1q3_races.append(r)
            q1q3_names.append(response.name)
            q1q3_totals.append(response.total)
    ####graph the number of real world races vs. the count
    
    title = '# of Real Races vs. # of RWM Runs'
    #fig = scatterPlot(real_races, run_count_list, '# of Races (in past year)', '# of RWM Runs', title, names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the number of real world races vs. the duration of use
    
    title = '# of Real Races vs. Time on RunWithMe'
    #fig = scatterPlot(real_races, duration_list, '# of Races (in past year)', 'Time on RWM (in days)', title, names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the number of real world races vs. the duration of use (limiting duration to q1-q3)
    
    title = '# of Real Races vs. Time on RunWithMe (based on Q1-Q3)'
    #fig = scatterPlot(q1q3_races, q1q3_durs, '# of Races (in past year)', 'Time on RWM (in days)', title, q1q3_names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the number of real world races vs. the duration of use (IQR)
    
    title = '# of Real Races vs. Run Frequency (inner quartile of duraton)'
    #fig = scatterPlot(q1q3_races, q1q3_run_frequency, '# of Races (in past year)', 'Run Frequency', title, q1q3_names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the number of real world races vs. the duration of use
    
    title = '# of Real Races vs. Overall Miles/Day (excluding outliers)'
    fig = g.scatterPlot(q1q3_races, q1q3_tf, '# of Races (in past year)', 'Overall Miles/Day', title, q1q3_names)
    #plot_url = py.plot(fig, filename=title)

    title = 'Total Distance vs. Days on RWM (without outliers for time and far outliers for distance)'
    fig = g.scatterPlot(q1q3_durs, q1q3_totals, 'Days', 'Total Distance (in miles)', title, q1q3_names)
    linear_reg(q1q3_durs, q1q3_totals)
    #plot_url = py.plot(fig, filename=title)

    title = 'Total Distance vs. Days on RWM (full data)'
    fig = g.scatterPlot(duration_list, total_miles_list, 'Days', 'Total Distance (in miles)', title, names)
    #plot_url = py.plot(fig, filename=title)
    ####graph the number of RWM users someone knows, and the number of races they are in
    
    #title = 'number known vs. number of races'
    #fig = scatterPlot(num_known_list, num_rwmRace_list, 'number known', 'number of races', title, names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the average run length vs. the duration of RWM use
    #title = 'average run length vs. duration of rwm use'
    #fig = fig = scatterPlot(run_avg_list, duration_list, 'average miles', 'duration on RWM', title, names)
    #plot_url = py.plot(fig, filename=title)

    ####graph the frequency of runs (#runs/duration) vs. the duration of RWM use

    #title = 'frequency'
    #fig = fig = scatterPlot(run_frequency, duration_list, 'frequency', 'duration on RWM', title, names)
    #plot_url = py.plot(fig, filename=title)


def linear_reg(x, y):
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	print 'slope: ', slope
	print 'intercept: ', intercept
	print 'r value: ', r_value
	print  'p_value: ', p_value
	print 'standard deviation: ', std_err

	line = slope*x+intercept
	return

def starters(SD):
    starters = SD.yes
    nonstart = SD.no
    maybe = SD.plan

    plan_mpd = []
    no_mpd = []
    yes_mpd = []

    plan_durs = []
    no_durs = []
    yes_durs = []
    
    plan_median = []
    no_median = []
    yes_median = []

    plan_rpd = []
    no_rpd = []
    yes_rpd = []

    plan_counts = []
    no_counts = []
    yes_counts = []
    
    plan_total = []
    no_total = []
    yes_total = []

    no_real = []
    plan_real = []
    yes_real = []

    no_known = []
    plan_known = []
    yes_known = []
    for response in nonstart:
        r = response.survey[3]
        r = int(r.strip('+'))
        no_real.append(r)

        num_known = response.survey[6]
        num_known = int(num_known.strip('+'))
        no_known.append(num_known)

        no_mpd.append(response.mpd)
        no_durs.append(response.dur)
        no_median.append(response.median)
        no_rpd.append(response.rpd)
        no_counts.append(response.count)
        no_total.append(response.total)
    for response in maybe:
        r = response.survey[3]
        r = int(r.strip('+'))
        plan_real.append(r)
        
        num_known = response.survey[6]
        num_known = int(num_known.strip('+'))
        plan_known.append(num_known)

        plan_mpd.append(response.mpd)
        plan_durs.append(response.dur)
        plan_median.append(response.median)
        plan_rpd.append(response.rpd)
        plan_counts.append(response.count)
        plan_total.append(response.total)
    for response in starters:
        r = response.survey[3]
        r = int(r.strip('+'))
        yes_real.append(r)
        
        num_known = response.survey[6]
        num_known = int(num_known.strip('+'))
        yes_known.append(num_known)

        yes_mpd.append(response.mpd)
        yes_durs.append(response.dur)
        yes_median.append(response.median)
        yes_rpd.append(response.rpd)
        yes_counts.append(response.count)
        yes_total.append(response.total)
    print 'mpd for no : ', np.mean(no_mpd)
    print 'mpd for maybe: ' , np.mean(plan_mpd)
    print 'mpd for yes: ' , np.mean(yes_mpd)
    print 'No vs. Planning to (mpd)'
    t_statistic, p_value = stats.ttest_ind(no_mpd, plan_mpd, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'dur for no : ', np.mean(no_durs)
    print 'dur for maybe: ' , np.mean(plan_durs)
    print 'dur for yes: ' , np.mean(yes_durs)
    print 'No vs. Planning to (duration)'
    t_statistic, p_value = stats.ttest_ind(no_durs, plan_durs, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'median for no : ', np.mean(no_median)
    print 'median for maybe: ' , np.mean(plan_median)
    print 'median for yes: ' , np.mean(yes_median)
    print 'No vs. Planning to (median)'
    t_statistic, p_value = stats.ttest_ind(no_median, plan_median, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value
    print 'rpd for no : ', np.mean(no_rpd)
    print 'rpd for maybe: ' , np.mean(plan_rpd)
    print 'rpd for yes: ' , np.mean(yes_rpd)
    print 'No vs. Planning to (rpd)'
    t_statistic, p_value = stats.ttest_ind(no_rpd, plan_rpd, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'count for no : ', np.mean(no_counts)
    print 'count for maybe: ' , np.mean(plan_counts)
    print 'count for yes: ' , np.mean(yes_counts)
    print 'No vs. Planning to (countation)'
    t_statistic, p_value = stats.ttest_ind(no_counts, plan_counts, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'total for no : ', np.mean(no_total)
    print 'total for maybe: ' , np.mean(plan_total)
    print 'total for yes: ' , np.mean(yes_total)
    print 'No vs. Planning to (total)'
    t_statistic, p_value = stats.ttest_ind(no_total, plan_total, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'races for no : ', np.mean(no_real)
    print 'races for maybe: ' , np.mean(plan_real)
    print 'races for yes: ' , np.mean(yes_real)
    print 'No vs. Planning to (countation)'
    t_statistic, p_value = stats.ttest_ind(no_real, plan_real, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    print 'known for no : ', np.mean(no_known)
    print 'known for maybe: ' , np.mean(plan_known)
    print 'known for yes: ' , np.mean(yes_known)
    print 'No vs. Planning to (known)'
    t_statistic, p_value = stats.ttest_ind(no_known, plan_known, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

'''breaks into the social groups'''
def plotSocial(SD):
    solo = SD.solo
    mid = SD.mid
    high = SD.social
    social = mid + high

    soloStarters = []
    socialStarters = []

    socialmpd = []
    solompd = []
    socialnames = []
    solonames = []
    
    solo_median_miles = []
    social_median_miles = []

    for response in solo:
        soloStarters.append(response.starter)
        if (response.dur<264 and response.total < 838):
            solompd.append(response.mpd)
            solonames.append(response.mpd)
            solo_median_miles.append(response.median)
    for response in social:
        socialStarters.append(response.starter)
        if (response.dur<264 and response.total < 838):
            socialmpd.append(response.mpd)
            socialnames.append(response.mpd)
            social_median_miles.append(response.median)
    
    ### Median Run Length by Social Running Habits
    title = 'Average Run Length by Social Running'
    fig = g.histogramTwo(solo_median_miles, social_median_miles, 'Solitary Runners', 'Social Runners')
    plot_url = py.plot(fig, filename='Comparing Social Running Habits and Median Run Distance')
    print 'Social Running Habits and Median Run Distance'
    print 'mean for solitary group: ', np.mean(solo_median_miles)
    print 'mean for social group: ', np.mean(social_median_miles)
    t_statistic, p_value = stats.ttest_ind(solo_median_miles, social_median_miles, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value
    ### Race Initiators vs. Social Running Habits
    #fig = histogramTwo(soloStarters, socialStarters)
    #plot_url = py.plot(fig, filename='Comparing Social Running Habits and Race Initiators')
    #t_statistic, p_value = stats.ttest_ind(solompd, socialmpd, equal_var=0)
    #print 't-statistic: ' , t_statistic
    #print 'p-value: ', p_value
    #fig = g.histogramTwo(solompd, socialmpd, 'Solitary Runners', 'Social Runners')
    #plot_url = py.plot(fig, filename='Comparing Miles/Day between Solo and Social Runners')

def plotQ1(SD):
    never_rarely = SD.nr
    often_always = SD.oa

    nr_med = []
    oa_med = []

    nr_rpd = []
    oa_rpd = []

    nr_races = []
    oa_races = []

    nr_r4 = []
    oa_r4 = []

    for response in never_rarely:
        nr_med.append(response.median)
        nr_rpd.append((response.rpd*7))
        
        r = response.survey[3]
        r = int(r.strip('+'))
        nr_races.append(r)

        a = response.survey[4]
        nr_r4.append(a)
    for response in often_always:
        oa_med.append(response.median)
        oa_rpd.append((response.rpd*7))
        
        r = response.survey[3]
        r = int(r.strip('+'))
        oa_races.append(r)

        a = response.survey[4]
        oa_r4.append(a)
    
    ### Median Run Length by Social Running Habits
    title = 'Median Run Length by Q1'
    fig = g.histogramTwo(nr_med, oa_med, 'Never/Rarely', 'Often/Always')
    plot_url = py.plot(fig, filename=title)
    print 'Median Run Length by Q1'
    print 'mean for never/rarely group: ', np.mean(nr_med)
    print 'mean for often/always group: ', np.mean(oa_med)
    t_statistic, p_value = stats.ttest_ind(nr_med, oa_med, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    title = 'rpd Run Length by Q1'
    fig = g.histogramTwo(nr_rpd, oa_rpd, 'Never/Rarely', 'Often/Always')
    plot_url = py.plot(fig, filename=title)
    print 'rpd by Q1'
    print 'mean for never/rarely group: ', np.mean(nr_rpd)
    print 'mean for often/always group: ', np.mean(oa_rpd)
    t_statistic, p_value = stats.ttest_ind(nr_rpd, oa_rpd, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    title = 'Num. Races by Q1'
    fig = g.histogramTwo(nr_races, oa_races, 'Never/Rarely', 'Often/Always')
    plot_url = py.plot(fig, filename=title)
    print 'Num. Races by Q1'
    print 'mean for never/rarely group: ', np.mean(nr_races)
    print 'mean for often/always group: ', np.mean(oa_races)
    t_statistic, p_value = stats.ttest_ind(nr_races, oa_races, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value

    title = 'Num. r4 by Q1'
    fig = g.histogramTwo(nr_r4, oa_r4, 'Never/Rarely', 'Often/Always')
    plot_url = py.plot(fig, filename=title)
    print 'Num. r4 by Q1'
    print 'mean for never/rarely group: ', np.mean(nr_r4)
    print 'mean for often/always group: ', np.mean(oa_r4)
    t_statistic, p_value = stats.ttest_ind(nr_r4, oa_r4, equal_var=0)
    print 't-statistic: ' , t_statistic
    print 'p-value: ', p_value
    ### Race Initiators vs. Social Running Habits
    #fig = histogramTwo(soloStarters, socialStarters)
    #plot_url = py.plot(fig, filename='Comparing Social Running Habits and Race Initiators')
    #t_statistic, p_value = stats.ttest_ind(solompd, socialmpd, equal_var=0)
    #print 't-statistic: ' , t_statistic
    #print 'p-value: ', p_value
    #fig = g.histogramTwo(solompd, socialmpd, 'Solitary Runners', 'Social Runners')
    #plot_url = py.plot(fig, filename='Comparing Miles/Day between Solo and Social Runners')



def plotQ2(SD):
    small = SD.small
    mid = SD.mid
    large = SD.large

    small_med = []
    mid_med = []
    large_mid = []

    for response in small:
        small_med.append(response.median)
    for response in mid:
        mid_med.append(response.median)
    for response in large:
        large_mid.append(response.median)

    print 'mean for small groups: ', np.mean(small_med)
    print 'mean for medium groups: ', np.mean(mid_med)
    print 'mean for large groups: ', np.mean(large_mid)

def writecsv(fileName, runners, responders = 0):
    outfile = open(fileName, 'wb')
    fieldnames = ['name', 'duration', 'count', 'total miles','avg. miles', 'miles_days', 'runs_days']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in runners:
        writer.writerow({'name': r.name , 'duration': r.dur, 'count': r.count, 'total miles': r.total, 'avg. miles': r.avg, 'miles_days': r.mpd, 'runs_days': r.rpd})
    responses.close()

def sort(run_data, SD):
    non_responders = []
    x = len(run_data.runners)
    y = len(SD.names)
    for runner in run_data.runners:
        if (runner.name not in SD.names):
            non_responders.append(runner)
    z = len(non_responders)
    print 'total: ' , x
    print 'responses: ', y
    print 'non-responders: ', z
    return non_responders


'''
Read survey from CSV file and make respondent objects.
Returns a SurveyData object that has access to all of the respondents 
'''
def read_survey(survey, run_data, INDEX):
    file = open(survey, 'rU') 
    #replace NULL values
    infile = csv.reader(x.replace('\0', '') for x in file)
    i = 0
    respondents = [] #list of respondent objects
    names = []
    for row in infile:
        if (i>1):
            myR = Survey(row)
            myR.makeName(row[6], row[7])
            # if survey name doesn't match rwm name
            if myR.name != '':
                runner = d.Data.get_runner(run_data, myR.name)
                respondent = Respondent(myR, runner)
                respondent.makeAge()
                respondent.get_start()
                respondent.makeGender()
                respondents.append(respondent)
                names.append(myR.name)
        i+=1
    file.close()
    SDATA = SurveyData(INDEX, respondents, names)
    return SDATA

'''returns an array of arrays, called by main and stored in INDEX variable'''

def completeSurvey():
        Q0 = []
        Q1 = ['Never', 'Rarely', 'Often', 'Always']
        Q2 = ['1 (I mostly run by myself)', '2-3 (I run with a buddy or two)', '3-6 (I\'m part of a group- it depends who shows up)', '>6 (The more the merrier)', 'It really varies.']
        Q3 = [0,1,2,3,4,5,6,7,8,9]
        Q4 = ['<20 miles', '21-50 miles', '51-100 miles', '101-200 miles', '201-300 miles', '301-500 miles', '501-700 miles', '701-1000 miles', '>1000 miles']
        Q5 = ['Yes', 'No', 'Not yet, but I am planning to.']
        Q6 = [0,1,2,3,4,5,6,7,8,9]
        Q7 =['Dedicated URL for my profile', 'Message board for each race','Display my bio photo as my avatar on the map', 'Automatically push my daily mileage to Facebook'] 
        Q8 = 'free format'
        Q9 = 'free format'
        Q10 = 'make integer'
        Q11 = ['male', 'female']
        Q = [Q0, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11]
        return Q

def main():
    try:
        credentials = tls.get_credentials_file()
    except:
        ## except credentials error and print for them to enter something
        credentials = {}
        credentials['username'] = raw_input("Plotly Username: ") ## get username
        credentials['api_key'] = raw_input("api key: ") ### get password
    py.sign_in(credentials['username'], credentials['api_key'])
    survey_file = "survey.csv"
    run_data = d.main()
    for runner in run_data.runners:
        runner.make_data()
        print runner.median
        #print runner.num , runner.total , runner.count, runner.avg, runner.dur, runner.mpd, runner.rpd
    
    INDEX = completeSurvey()
    #SD is a SurveyData object, has all of the respondents
    SD = read_survey(survey_file, run_data, INDEX)
    mydict = SD.makeDictionary()
    SD.groupSocial()
    SD.groupStarter()
    SD.groupQ1()
    SD.groupQ2()

    #list of runners that did not respond
    nonResponders = sort(run_data, SD)
    #list of runners that did respond
    surveyResponders = SD.responses
    plotQ1(SD)
    #plotQ2(SD)
    #starters(SD)
    plotSocial(SD)

    #df = pd.DataFrame(surveyResponders)
    #df.to_csv('stest1.csv')
    # graph = int(input('''Please select an option: 
    #     1. compare all vs. those that responded 
    #     2. graphs for respondents 
    #     3. compare between groups (of respondents)'''))
    # if (graph == 1):
    #     compare_resp_all(surveyResponders, nonResponders, run_data.runners)
    # if (graph == 2):
    #     graph_responses(surveyResponders)
    # if (graph == 3):
    # 	plotSocial(SD)
    # else:
    #     print "No graphing option selected"
    
main()
