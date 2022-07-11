#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import matplotlib.pyplot as plt
import math

def get_data():
    #load data
    with open('trials.json') as f:
        data = json.load(f)
    #parse responses
    other_items = {'carrots': ["carrot", "a carrot"], "peas": ["pea", "a pea"], "potatoes": ["potato", "a potato"], "onions": ["onion", "an onion"], "green beans": ["green bean"], "tomatoes": ["tomato", "a tomato"], "cucumbers": ["cucumber", "a cucumber"], "squash": ["a squash"], "peppers": ["pepper", "a pepper"], "eggplant": ["eggplants"], "cabbage": ["cabbages", "a cabbage"], "brussel sprouts": ["brussel sprout", "a brussel sprout"]}
    for t in data:
        gens = t['gen_data']
        new_gens = []
        for g in gens:
            g2 = g.lower()
            for k, l in other_items.items():
                if g2 in l:
                    g2 = k
            new_gens.append(g2)
        t['gen_data'] = new_gens
    #remove subjects who gave same rating for all veg for one of the featurs, so correlation is nan)
    data = [s for s in data if s['row_id'] not in ['5d7e5e9b377dc300014335de', '5f03e4a77df42060e6b3dd13']]
    data = removeOutliers(data)
    return data

def removeOutliers(data):
    new_data = []
    for d in data:
        d2 = {}
        d2['row_id'] = d['row_id']
        d2['gen_data'] = d['gen_data']
        d2['gen_data_rt'] = d['gen_data_rt']
        d2['scores_per_ft'] = {}
        for ft, scores in d['scores_per_ft'].items():
            d2['scores_per_ft'][ft] = []
            for s in scores:
                if s[2]==0:
                    print("here")
                    continue
                if s[2] < 10000:
                    d2['scores_per_ft'][ft].append([s[0], s[1], math.log(s[2])])
        new_data.append(d2)
    return new_data

#reformat data for easier analysis
def reformat_data(data):
    new_data = []
    for d in data:
        d2 = {}
        d2['row_id'] = d['row_id']
        d2['gen_data'] = eval(d['gen_data'])
        d2['gen_data_rt'] = float(d['gen_data_rt'])
        d2['scores_per_ft'] = eval(d['animal_scores_per_feature'])
        for k in d2['scores_per_ft'].keys():
            for l in d2['scores_per_ft'][k]:
                l[1] = int(l[1])
        new_data.append(d2)
    with open('trials.json', 'w') as f:
        json.dump(new_data, f)

#returns each feature's predictiveness of coming to mind for the given subject
def get_ft_corr_w_gen(subj):
    ft_corr = {}
    gens = subj['gen_data']
    
    for ft, res_list in subj['scores_per_ft'].items():
        #for each veg, score for this ft
        ft_scores = {}
        for res in res_list:
            ft_scores[res[0]] = res[1]
        x, y = [], []
        for veg, score in ft_scores.items():
            x.append(score)
            #prob of gen = 1 if generated, 0 if not ... maybe need to do this differently
            y.append(int(veg in gens))
        if subj['row_id']=='5f03e4a77df42060e6b3dd13' and ft=='think':
            print(x)
            print(y)
        ft_corr[ft] = np.corrcoef(x,y)[0][1]
    return ft_corr

# returns speed of response to that feature for the given subject
def get_ft_speed(subj):
    #want to get average speed of response to each feature
    ft_speed = {}
    for ft, res_list in subj['scores_per_ft'].items():
        ft_speed[ft] = np.mean([res[2] for res in res_list])
    
    return ft_speed

#get correlation bt coming to mind and speed of response for that item
def get_gen_prob_corr_w_speed(subj):
    it_speed = {}
    for ft, res_list in subj['scores_per_ft'].items():
        #for each item, score for this ft
        for res in res_list:
            it_speed[res[0]] = it_speed.get(res[0], [])
            it_speed[res[0]].append(res[2])
    
    gens = subj['gen_data']
    x, y = [], []
    for it, speed in it_speed.items():
        #mean response time for this item
        x.append(np.mean(speed))
        #prob of gen = 1 if generated, 0 if not ... maybe need to do this differently
        y.append(int(it in gens))
    return(np.corrcoef(x,y)[0][1])

#get correlation between values of two dicts w same keys
def get_dict_corr(d1,d2):
    x, y = [], []
    for k, v in d1.items():
        x.append(v)
        y.append(d2[k])
    return np.corrcoef(x,y)[0][1]

#for a pair of subjects, returns correlation between
#difference in feature speed of response and in feature pred of coming to mind
def compare_subjects(subj1, subj2):
        #each feature's predictiveness of coming to mind
        ft_corr_w_gen1 = get_ft_corr_w_gen(subj1)
        ft_corr_w_gen2 = get_ft_corr_w_gen(subj2)

        #speed of response to each feature
        ft_speed1 = get_ft_speed(subj1)
        ft_speed2 = get_ft_speed(subj2)
        
        x, y = [], []
        #correlation between differences in pred and differences in speed
        for ft in ft_speed1:
            x.append(ft_corr_w_gen1[ft] - ft_corr_w_gen2[ft])
            y.append(ft_speed1[ft] - ft_speed2[ft])

        return np.corrcoef(x,y)[0][1]

#also, are there any features for which participant speed predicts participant pred of coming to mind?
def compare_ft_across_subjects(ft, data):
    #speed for this feature for each subject
    x = []
    #pred of this feature for each subject
    y = []
    for subj in data:
        ft_corr_w_gen = get_ft_corr_w_gen(subj)
        ft_speed = get_ft_speed(subj)
        x.append(ft_speed[ft])
        y.append(ft_corr_w_gen[ft])
    return np.corrcoef(x,y)[0][1]

#did speed of response correlate with predictiveness of coming to mind across participants?
    #for each response
        #average rating for each feature
        #prob of coming to mind across all participants
    #get correlation bt rating and prob of coming to mind for each feature
    #also speed of response to each feature across participants
    #does speed correlate w predictiveness of coming to mind?
def all_subj_data():
    data = get_data()
    #get gen counts
    gen_counts = {}
    for subj in data:
        for gen in subj['gen_data']:
            gen_counts[gen] = gen_counts.get(gen, 0) + 1
    for res in data[0]['scores_per_ft']['likes']:
        gen_counts[res[0]] = gen_counts.get(res[0], 0)
    #print(gen_counts)
    #now get ave rating for each item across participants - fine to just do ratings for subjects who saw that item
    #also get ave speed of response to each feature
    ratings = {}
    speeds = {}
    for ft in data[0]['scores_per_ft'].keys():
        ratings[ft] = {}
        speeds[ft] = []
        for gen in gen_counts.keys():
            ratings[ft][gen] = []
    for subj in data:
        for ft, res_list in subj['scores_per_ft'].items():
            for res in res_list:
                it = res[0]
                score = res[1]
                rt = res[2]
                ratings[ft][it].append(score)
                speeds[ft].append(rt)
    for ft, score_list in ratings.items():
        speeds[ft] = np.mean(speeds[ft])
        for it in ratings[ft].keys():
            ratings[ft][it] = np.mean(ratings[ft][it])
    #print(ratings)
    #now get each features predictiveness of coming to mind (mean rating of each item vs prob of being generated)
    ft_pred = {}
    x, y = [], []
    for ft, ft_ratings in ratings.items():
        for it, rating in ft_ratings.items():
            x.append(rating)
            y.append(gen_counts[it])
        ft_pred[ft] = np.corrcoef(x,y)[0][1]
    print("each features predictiveness of coming to mind:")
    print(ft_pred)
    print("speed of response to each feature:")
    print(sorted(speeds.items(), key=lambda x: x[1], reverse=True))
    #now get correlation between a feature's pred of coming to mind and speed of response to feature
    pred_speed_corr = get_dict_corr(ft_pred, speeds)
    print("correlation between a feature's predictiveness of coming to mind, and speed of response to that feature:")
    print(pred_speed_corr)
#all_subj_data()

#over all the subjects, which features predicted coming to mind?
"""
{'large': -0.0641153124735296, 'healthy': -0.019831518684910877, 'calories': 0.006344653270413262,
'dishes': 0.025906336057867053, 'heavy': 0.03127251534753701, 'fragrant': 0.013951224854021605,
'crunchy': 0.025178677323245798, 'popular': 0.0456126707098879, 'sweet': 0.03690550638786234,
'available': 0.05595641212749722, 'warm': 0.05191265700818865, 'colorful': 0.04106680154598035,
'think': 0.04267021614574105, 'likes': 0.04878236859217297}
"""
#what was correlation with speed of response?
"""
0.10038528118820983
"""

#did differences in participants for speed of response to each/certain features
#predict differences in their predictiveness of coming to mind?
    #can look at pairs of participants, compare speed and pred of all features
    #take average of each pair
"""
0.011102376831402192
"""

#average of, for each subject, feature predictivity corr w speed
"""
0.041447578488886264
"""

#For each feature, did differences in speed predict differences in pred of coming to mind across participants?
"""
large: 0.15389811344180013
healthy: 0.33667800939164566
calories: 0.18247679129525315
dishes: 0.13556806223546433
heavy: 0.03392778779945416
fragrant: 0.13262841247827495
crunchy: 0.3068694696789049
popular: 0.3914800482858189
sweet: 0.17958448016776304
available: 0.32796914511684594
warm: 0.03568783509095232
colorful: 0.14188018573945954
think: 0.33031620732644773
likes: 0.02124234351336861
"""




#certain features predict differences across participants
#for some, rated the vegetables they thought of as healthy, and responded faster about healthiness
#others rated the vegetables they thought of as less healthy, and responded slower about healthiness
#certain features which are more or less central to reps of vegetables predict what comes to mind
    #problem is, speed of response doesn't predict pred of coming to mind

#did average speed for each feature predict average predictiveness of coming to mind?

ave_speed = {'large': 1695.74872106912, 'healthy': 1441.0580998834441, 'calories': 1654.7109622441099, 'dishes': 1945.1120584748037, 'heavy': 1867.9580998690221, 'fragrant': 1697.6576126704024, 'crunchy': 1714.4981729641022, 'popular': 1522.6511571217593, 'sweet': 1695.5408039019144, 'available': 1622.1475030499096, 'warm': 1779.584774665453, 'colorful': 1640.9933008568823, 'think': 1746.4544458099517, 'likes': 1524.426187585707}

#for each feature, plot for each person, speed of response vs predictiveness of coming to mind
    #varies person to person?
def plot_features():
    preds = []
    speeds = []
    data = get_data()
    #for each subject, get ft pred and ft speed
    for subj in data:
        ft_corr_w_gen = get_ft_corr_w_gen(subj)
        ft_speed = get_ft_speed(subj)
        pred_corr_w_speed = get_dict_corr(ft_speed, ft_corr_w_gen)
        preds.append(ft_corr_w_gen)
        speeds.append(ft_speed)
    #get x, y list for each ft (pred, speed)
    for ft in preds[0].keys():
        x,y=[],[]
        #go thru each subject
        for i in range(len(preds)):
            x.append(preds[i][ft])
            y.append(speeds[i][ft])
        plt.scatter(x,y)
        plt.title(ft)
        plt.xlabel("predictiveness of coming to mind")
        plt.ylabel("speed of response")
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*np.array(x) + b)
        plt.show()

    

def main():
    data = get_data()
    pred_corr_w_speed_list = []
    pred_list = []
    for subj in data:
        #each feature's predictiveness of coming to mind
        ft_corr_w_gen = get_ft_corr_w_gen(subj)
        pred_list.append(ft_corr_w_gen)
        #speed of response to each feature
        ft_speed = get_ft_speed(subj)
        #for ft, speed in ft_speed.items():
         #   ft_speed[ft] = ave_speed[ft] - speed
        #correlation between a feature's predictiveness of coming to mind, and speed of response to that feature
        pred_corr_w_speed = get_dict_corr(ft_speed, ft_corr_w_gen)
        pred_corr_w_speed_list.append(pred_corr_w_speed)
        #get correlation bt coming to mind and speed of response for that animal
        #gen_prob_corr_w_speed = get_gen_prob_corr_w_speed(subj)
    print("for each subjects, predictiveness of each feature corr w rt")
    print(pred_corr_w_speed_list)
    print(np.mean(pred_corr_w_speed_list))
    #see on average which features were predictive of coming to mind
    #print("features predictiveness of coming to mind on average across subjects:")
    #for ft in pred_list[0].keys():
    #    print(ft + ": " + str(np.mean([subj[ft] for subj in pred_list])))

    print("correlation bt mean difference in rts for features, and difference in predictivenss for pairs of subjects")
    diff_corrs = []
    for subj1 in data:
        for subj2 in data:
            if subj1['row_id']!=subj2['row_id']:
                diff_corr = compare_subjects(subj1, subj2)
                diff_corrs.append(diff_corr)
    mean_dif_corr = np.mean(diff_corrs)
    print(diff_corrs)
    print(mean_dif_corr) #0.011102376831402192
    
    print("correlation of rt/pred of each feature across participants")
    for ft in data[0]['scores_per_ft'].keys():
        print(ft)
        print(compare_ft_across_subjects(ft, data))
    
main()

def checkOutliers():
    data = get_data()
    all_rts = []
    for d in data:
        for ft, scores in d['scores_per_ft'].items():
            for s in scores:
                all_rts.append(s[2])
    print(np.mean(all_rts))
    print(max(all_rts))
    all_rts = [x for x in all_rts if x > 5000]
    plt.hist(all_rts, bins=60)
    plt.show()
    #rts = data
    #for d

#check outliers
#log rt?