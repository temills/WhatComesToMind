#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import random

numCats = 10
categories = ['types of furniture', 'vegetables', 'chain restaurants', 'breakfast foods', 'sports', 'clothing items', 'zoo animals', 'jobs', 'holidays', 'kitchen appliances']
cats = ['vegetables', 'restaurants', 'sports', 'animals1', 'animals2', 'jobs', 'holidays', 'kitchen']
info = {'age': [], 'gender': []}
for c in cats:
  print(c)
  with open('timed-item-generations/response_data/'+ c+ '.json') as f:
    data = json.load(f)

  n=0
  for trial in data:
    if trial['q_order']==8:
      info['age'].append(int(trial['age']))
      info['gender'].append(trial['gender'])
      n=n+1
  print(n)
print(np.mean(info['age']))
print(np.std(info['age']))
print(len([x for x in info['gender'] if x=='Female']))
print(len([x for x in info['gender'] if x=='Male']))
print(len([x for x in info['gender'] if (x!='Female' and x!='Male')]))
