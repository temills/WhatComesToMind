from flask import render_template, request, make_response, session
from . import app, db
from .models import Subject, Trial
import datetime
import json



# Views
#@app.route('/botstudy', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def experiment():
    if request.method == 'GET':
        return render_template('experiment.html')
    if request.method == 'POST':
        dd = request.get_json(force=True)['data']
        #subject information
        if dd['exp_phase'] == 'subject_info':
            print('recording subject data')
            ret = Subject( subject_id= str(dd['subject_id']),
                           completion_code = str(dd['completion_code']),
                           age= str(dd['age']),
                           gender= str(dd['gender']),
                           nationality= str(dd['nationality']),
                           country= str(dd['country']),
                           student= str(dd['student']),
                           language= str(dd['language']),
                           education= str(dd['education']))
        #trial response
        else:
            print('recording trial data')
            ret = Trial( row_id = str(dd['subject_id']) + "_" + str(dd['res_num']),
                           answer= str(dd['answer']),
                           answer_rt= str(dd['answer_rt']),
                           considerations = str(dd['considerations']),
                           ft=str(dd['ft']),
                           opp_ft = str(dd['opp_ft']),
                           ft_dict = str(dd['ft_dict']),
                           ft_dict_rt = str(dd['ft_dict_rt']),
                           opp_ft_dict = str(dd['opp_ft_dict']),
                           opp_ft_dict_rt = str(dd['opp_ft_dict_rt']))

        db.session.add(ret)
        db.session.commit()
        return make_response("", 200)