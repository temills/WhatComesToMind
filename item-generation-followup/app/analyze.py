#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import matplotlib.pyplot as plt
import math


#reformat data for easier analysis
def reformat_data():
    with open('trials.json') as f:
        data = json.load(f)
    new_data = []
    for d in data:
        d2 = d
        d2['answer_rt'] = float(d['answer_rt'])
        d2['considerations'] = [c for c in eval(d['considerations']) if c.lower().strip() not in ["na","n a","n/a"]]
        if d['ft_dict']=={}:
            continue
        d2['ft_dict'] = eval(d['ft_dict'])
        d2['opp_ft_dict'] = eval(d['opp_ft_dict'])
        for k, v in d2['ft_dict'].items():
            d2['ft_dict'][k] = float(v)
        for k, v in d2['opp_ft_dict'].items():
            d2['opp_ft_dict'][k] = float(v)
        new_data.append(d2)
    with open('trials2.json', 'w') as f:
        json.dump(new_data, f)

with open('trials2.json') as f:
    data = json.load(f)

#get average scores for feature and opposite feature for considerations for each feature
def print_scores_per_ft():
    scores = {}
    for trial in data:
        ft = trial["ft"]
        scores[ft] = scores.get(ft, {"self":[],"opposite":[]})
        scores[ft]["self"].append(np.mean(list(trial["ft_dict"].values())))
        scores[ft]["opposite"].append(np.mean(list(trial["opp_ft_dict"].values())))
    for ft in scores.keys():
        scores[ft]["self"] = np.mean(scores[ft]["self"])
        scores[ft]["opposite"] = np.mean(scores[ft]["opposite"])
    for ft in ['striking', 'unremarkable', 'long-lived', 'short-lived', 'large', 'small', 'cool', 'boring', 'dangerous','harmless']:
        print(ft + ": " + "self=" + str(scores[ft]["self"]) + ", opp=" + str(scores[ft]["opposite"]))
    

def plot_intrusion_prob():
    scores = {}
    for trial in data:
        ft = trial["ft"]
        scores[ft] = scores.get(ft, {"self":[],"opp":[]})
        scores[ft]["self"].append(np.mean(list(trial["ft_dict"].values())))
        scores[ft]["opp"].append(np.mean(list(trial["opp_ft_dict"].values())))
    intrusion_prob1 = {}
    intrusion_prob2 = {}
    for ft in scores.keys():
	    intrusion_prob1[ft] = len([s for s in scores[ft]["self"] if s < 50])/len(scores[ft]["self"])
	    intrusion_prob2[ft] = len([s for s in scores[ft]["opp"] if s > 50])/len(scores[ft]["opp"])
    labels = ["large","small","dangerous","harmless","long-lived","short-lived","cool","boring","striking","unremarkable"]
    y = [intrusion_prob1[ft] for ft in labels]
    x = [0.3,0.8,0.3,0.8,0.3,0.8,0.3,0.8,0.3,0.8]

    fig, ax = plt.subplots()
    #plt.scatter(x, y, color=['blue','blue','orange','orange','green','green','red','red','purple','purple'])
    #plt.scatter(x + [0,1], y + [.7,.7], color=['blue','blue','orange','orange','green','green','red','red','purple','purple','white','white'])
    plt.scatter(x, y, color=['blue','blue','white','white','white','white','white','white','white','white'])


    #ax.boxplot([[y[0], y[2], y[4], y[6], y[8]], [y[1], y[3], y[5], y[7], y[9]]], positions=[0.3,0.8],whis=(0, 100))

    ax.set_ylabel('Probability of Intrusion',fontweight='bold')

    #for i, txt in enumerate(labels):
    #    ax.annotate(txt, (x[i], y[i]))
    
    #plt.scatter(x,y)
    #for i in range(0,len(x)-1,2):
    for i in range(0,2,2):
        line, = plt.plot([x[i],x[i+1]],[y[i],y[i+1]])
        line.set_label(labels[i] + "-" + labels[i+1])
    
    plt.xticks([0.3,0.8], ['Predictive\nEnd', 'Non Predictive\nEnd'], fontweight='bold')
    #plt.xticks([])
    plt.legend(loc='upper left')

    plt.show()

plot_intrusion_prob()

"""
fig, ax = plt.subplots()
ax.scatter(z, y)

for i, txt in enumerate(n):
    ax.annotate(txt, (z[i], y[i]))
"""

"""
for predictive features...
features predictiveness of coming to mind vs rating of considerations in terms of that feature
features predictiveness of coming to mind vs rating of considerations in terms of opposite feature

for predictive features, 2 bars for each feature, one average rating for that feature, other for opposite feature
then for opposite of predictive features, same thing

for opposite features...
considerations in terms of that feature
considerations in terms of opposite feature
other has a features predictiveness of coming to mind vs rating of that feature for considerations for opposite feature

{
    "large": 0.3306496004568212, 
    "cool": 0.30742969481011206,
    "striking": 0.3832161668667744,
    "dangerous": 0.2821509839494638,
    "lifespan": 0.34378931056051143,
}
"""
