#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:10:49 2019

@author: joselynrodriguez


MTurk Answer Form XML cleaner

"""

import boto3
import xml.etree.ElementTree as ET
import pandas as pd



MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX)


############################################################
#   Helpers for accessing and cleaning questionnaire data  #
############################################################

#returns a list of available hits as HITIds
def get_hit_ids():
    available_hits = mturk.list_reviewable_hits(
        Status='Reviewable',
    )
    
    available_hits = available_hits['HITs']
    all_hits = []
    
    for hit in available_hits:
        hit = hit['HITId']
        all_hits.append(hit)
    return all_hits

# returns a list of answer dictionaries containing assignment ids, hit_ids, worker ids, and question xml data
def get_questionnaire_data(hit_list):
    
    all_answer_lists = []
    
    for hit in hit_list:
        answer_list = {}

        response = mturk.list_assignments_for_hit(
            HITId= hit,
            AssignmentStatuses=['Submitted'])
        for answer in response['Assignments']:
            answer_list["assignment_id"] = answer['AssignmentId'] 
            answer_list["hit_id"] = answer["HITId"]
            answer_list["worker_id"] = answer["WorkerId"]
            answer_list["quest_xml"] = answer["Answer"]
        all_answer_lists.append(answer_list)
        
    print("here")
    print(all_answer_lists)
    return all_answer_lists

def parse_question_data(answer_lists):

    for answer in answer_lists:
        questionnaire_raw = answer['quest_xml']
    
    root = ET.fromstring(questionnaire_raw)
    print(root)

    questionnaire = []

    for node in root.findall('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}Answer'):
        question = node.find('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}QuestionIdentifier')
        answer = node.find('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}FreeText')
        print(answer.text)
        questionnaire[question.text] = answer.text
    #questionnaire.append(questionnaire)
    #questionnaire.append(questionnaire_raw['assignment_id'])
    #questionnaire.append(questionnaire_raw['worker_id'])
    return questionnaire


def save_to_csv(questionnaire, filename):
    data_frame = pd.DataFrame.from_dict(data= questionnaire,orient= 'columns')
    csv = data_frame.to_csv(filename, header=True)
    return csv


def main():
    hit_ids = get_hit_ids()
    answer_lists = get_questionnaire_data(hit_ids)
    questionnaire = parse_question_data(answer_lists)
    save_to_csv(questionnaire, 'test_file.csv')
    


if __name__ == "__main__":
    main()
