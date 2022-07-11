#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from scipy import stats

#should also predict
#differences in similarity judgements predicted by 

#useful to learn that the things that are worth calling to mind are in these parts of space

#certain features are predictive of calling to mind
#means that in the past, you learned that it's good to call to mind things with this feature
#which also means that you would have learned to represent category members along that dimensoon - so that you can call the right ones to mind
#represent along BC it's useful for coming to mind

#other features we also represent along

#for novel feature, call to mind task in which that feature is relevant
#would then have ease of response increase, or maybe semantic space would be warped?

#weighted 





#if large predicts what comes to mind, then assigning variable large values to new creatures would predict what comes to mind
    #subcategory
#

#want to know why certain features predict what comes to mind
#want to manipulate process of calling them to mind
#think of category members with relevant end of some dimension
#then people should do this later

#there's dif sorts of tasks 

#land vs sea
#not predictive of what comes to mind, both come to mind
#relevant feature - respond easily, predicts differences

#ease of response - things you can respond easily about even if they're not rlly relevant - color
#if predictive, then can answer easily!

#land/sea is useful to rep, but not
#uniformity 

#useful feature for calling things to mind
#so we will represent it along this feature




#find what comes to mind from THIS study

#for each subject, want:
#what comes to mind
#ratings in terms of features for each item that comes to mind (10 or whatever)
#either:
    #or between animals and ratings judgements for these animals
#if second way, say we have 63 animals, that's 1953 comparisons
#just want, for each subject, to get a good idea of how each feature relates to these comparisons
#15 choose 2 is 105, so like 100 comparisons, then rate 15 + max of 10 animals according to features
#is 15 enough?

#go thru trials, get ave difference for each feature
#by getting dif bt each animal and that persons feature ratings for both animals
#then can get correlation of feature sim w reported sim

#for each item pair, compare difference in average rating for each feature to true difference
def get_feature_rel_dict(sims, ratings):
    ft_rel_dict = {}
    for ft, d in ratings.items():
        true_dif = []
        ft_dif = []
        for i1, d2 in sims.items():
            for i2, s in d2.items():
                true_dif.append(s)
                ft_dif.append(abs(ratings[ft][i1] - ratings[ft][i2]))
        ft_rel_dict[ft] = -np.corrcoef(true_dif, ft_dif)[0][1]
    return ft_rel_dict

#average similarity judgement between items across subjects
#dict w items as keys, dict w items as keys and ave sim judgement as values as values
def get_item_sims():
    item_sims = {}
    for trial in data:
        for i1, d in trial["sim_dict"].items():
            for i2, s in d.items():
                item_sims[i1] = item_sims.get(i1, {})
                item_sims[i1][i2] = item_sims[i1].get(i2, []) + [s]
    for i1 in item_sims.keys():
        for i2 in item_sims[i1].keys():
            item_sims[i1][i2] = np.mean(item_sims[i1][i2])
    return item_sims

#get average rating for each item for each feature across subjects
#dict w features as keys, dict w items as key and ave rating as values as values 
def get_item_ratings():
    item_ratings = {}
    for trial in data:
        for ft, d in trial["rate_dict"].items():
            item_ratings[ft] = item_ratings.get(ft, {})
            for it, v in d.items():
                item_ratings[ft][it] = item_ratings[ft].get(it, []) + [v]
    for ft in item_ratings.keys():
        for it in item_ratings[ft].keys():
            item_ratings[ft][it] = np.mean(item_ratings[ft][it])
    return item_ratings

#see if differences in what comes to mind between subjects can predict differences in item similarity ratings
def ind_dif():
    for s1 in data:
        #get average rating for each ft for what comes to mind - should do this relative to other ratings?
        #get corr of ft sim with item sim (ft rel)
        for s2 in data:
        #same
        #for each feature, get corr of dif bt pred of coming to mind and dif bt ft rel
            print("blah")
        

def print_comparison(ft_pred, ft_eor, ft_rel):
    pred = []
    eor = []
    rel = []
    for k in ft_rel.keys():
        pred.append(ft_pred[k])
        eor.append(ft_eor[k])
        rel.append(ft_rel[k])
    print("corr bt predictiveness of coming to mind and ease of response:")
    print(np.corrcoef(pred, eor)[0][1])
    print("corr bt predictiveness of coming to mind and relevance:")
    print(np.corrcoef(pred, rel)[0][1])
    print("ease of response and relevance:")
    print(np.corrcoef(rel, eor)[0][1])

#also predict individual differences

#also want to predict similarity using betas from predicting what comes to mind
def compute_sim_w_betas(item_sims, ratings, weights):
    weighted, unweighted, true = [], [], []
    for i1 in item_sims.keys():
        for i2 in item_sims[i1].keys():
            #true sim bt the two
            true.append(item_sims[i1][i2])
            #ft based sim, unweighted
            #get all features for each item
            p1, p2, wp1, wp2 = [], [], [], []
            for ft in ratings.keys():
                p1.append(ratings[ft][i1])
                p2.append(ratings[ft][i2])
                #multiply these coordinates by feature weight
                wp1.append(ratings[ft][i1] * abs(weights[ft]))
                wp2.append(ratings[ft][i2] * abs(weights[ft]))
            unweighted.append(math.dist(p1, p2))
            weighted.append(math.dist(wp1, wp2))
    print("corr bt sim and unweighted ft based approach:")
    print(np.corrcoef(true, unweighted)[0][1])
    print("corr bt sim and weighted ft based approach:")
    print(np.corrcoef(true, weighted)[0][1])


#get correlation between distance similarity metric using given weights with true similarity
def sim_corr_for_weights(item_sims, ratings, weights):
    weighted, unweighted, true = [], [], []
    for i1 in item_sims.keys():
        for i2 in item_sims[i1].keys():
            #true sim bt the two
            true.append(item_sims[i1][i2])
            #ft based sim, unweighted
            #get all features for each item
            p1, p2 = [], []
            for ft in ratings.keys():
                #multiply these coordinates by feature weight
                p1.append(ratings[ft][i1] * weights[ft])
                p2.append(ratings[ft][i2] * weights[ft])
            weighted.append(math.dist(p1, p2))
    return -np.corrcoef(true, weighted)[0][1]


def shuffle_weights(weights):
    new_weights = {}
    vals = list(weights.values())
    random.shuffle(vals)
    for i, k in enumerate(weights.keys()):
        new_weights[k] = vals[i]
    return new_weights


def compute_sim_permutation(item_sims, ratings, weights):
    our_corr = sim_corr_for_weights(item_sims, ratings, weights)
    print(our_corr)
    print(weights)
    corrs = [our_corr]
    for i in range(100):
        shuf_weights = shuffle_weights(weights)
        corrs.append(sim_corr_for_weights(item_sims, ratings, shuf_weights))
    #print(corrs)
    print(stats.percentileofscore(corrs, our_corr))


#can also do permutation test for individual subjects - figure out which features are predictive and then use that as weights
def get_feature_pred():
    #for each subject get generations and their ratings for each feature
    ft_scores = {}
    #for each subject
    for trial in data:
        #for each feature
        for ft, d in trial["rate_dict"].items():
            ft_scores[ft] = ft_scores.get(ft, 0)
            #
            for g in trial['generations']:
                ft_scores[ft] = ft_scores[ft] + (d[g]/len(trial['generations']))
    for k,v in ft_scores.items():
        ft_scores[k] = np.mean(v)
    print(ft_scores)
    ax = plt.subplot()
    plt.bar(range(len(ft_scores.values())), sorted(ft_scores.values()))
    ax.set_xticklabels(sorted(ft_scores.keys(), key=lambda x: ft_scores[x]), rotation=90)
    plt.show()
    return ft_scores

    #average score for each ft for generations
    #then average across subjects

    #

    #


def main():
    sims = get_item_sims()
    ratings = get_item_ratings()
    #ft predictiveness of coming to mind
    with open('../../item-ratings/descriptor-generation-correlations/animals.json') as f:
        ft_pred = json.load(f)
    #ft ease of response
    with open('../../timed-item-generations/descriptor-speed-data/animals.json') as f:
        ft_eor = json.load(f)
    #ft relevance, or extent to which differences in this feature predict differences between items
    ft_rel = get_feature_rel_dict(sims, ratings)
    print(ft_rel)
    #compare ft rel, eor, pred
    print_comparison(ft_pred, ft_eor, ft_rel)
    #also see how well betas from predicting coming to mind can be used to predict item similarity
    ft_pred2 = get_feature_pred()
    compute_sim_w_betas(sims, ratings, ft_pred)
    compute_sim_permutation(sims, ratings, ft_pred)



#reformat data for easier analysis
def reformat_data():
    with open('trials.json') as f:
        data = json.load(f)
    new_data = []
    for d in data:
        d2 = d
        d2['items'] = eval(d['items'])
        d2['generations_rt'] = float(d['generations_rt'])
        d2['generations'] = eval(d['generations'])
        d2['features'] = eval(d['features'])
        d2['sim_dict'] = eval(d['sim_dict'])
        d2['sim_dict_rt'] = eval(d['sim_dict_rt'])
        d2['rate_dict'] = eval(d['rate_dict'])
        #for k, v in d2['sim_dict'].items():
        #    d2['sim_dict'][k] = float(v)
        #for k, v in d2['rate_dict'].items():
        #    d2['rate_dict'][k] = float(v)
        new_data.append(d2)
    with open('trials2.json', 'w') as f:
        json.dump(new_data, f)


with open('trials2.json') as f:
    data = json.load(f)

main()