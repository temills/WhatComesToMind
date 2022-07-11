#!/usr/bin/env python3

import json

with open('/Users/traceymills/panoptic-toolbox/outfiles/171204_pose1_outfile.json') as f:
    d = json.load(f)
print(d.keys())
print(d['goodCams'])