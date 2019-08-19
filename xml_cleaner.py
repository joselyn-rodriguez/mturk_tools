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

# returns a list of answers
def get_questionnaire_data(hit_list):
    answer_list = []
    for hit in hit_list:
        response = mturk.list_assignments_for_hit(
            HITId= hit,
            AssignmentStatuses=['Submitted'])
        print(response)
        for answer in response['Assignments']:
            print(answer)
            answer_list.append( { answer['AssignmentId'] : answer['Answer'] })
        
    print("here")
    print(answer_list)
    return answer_list


def parse_question_data(question_dictionary):
    for pair in question_dictionary:
        ans_id = pair.keys() #it is keys but there is only one
        questionnaire_raw = pair.values() #once again, only one
    
    root = ET.fromstring(questionnaire_raw)

    questionnaire = []
    #creating a dictionary for the question and answer data
    questionnaire_data = {}

    for node in root.findall('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}Answer'):
        question = node.find('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}QuestionIdentifier')
        answer = node.find('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd}FreeText')
        questionnaire_data[question.text] = answer.text
    questionnaire.append(questionnaire_data)
    questionnaire.append("assignmentId" + "," + ans_id)
    return questionnaire


def save_to_csv(questionnaire, filename):
    data_frame = pd.DataFrame.from_dict(data= questionnaire,orient= 'columns')
    csv = data_frame.to_csv(filename, header=True)
    return csv


def main():
    hit_ids = get_hit_ids()
    print(hit_ids)
    get_questionnaire_data(hit_ids)


if __name__ == "__main__":
    main()
