#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:05:58 2019

@author: joselynrodriguez
"""

import boto3


MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX)

########################################
#  Some helpter functions using boto3  #
########################################

# create qualifications
def create_qualification(Name, keywords, description, autogrant_stat, qual_status):
    
    response = mturk.create_qualification_type(
        Name= Name,
        Keywords=keywords,
        Description=description,
        QualificationTypeStatus=qual_status,
        AutoGranted=autogrant_stat,
        AutoGrantedValue=123
    )
    
    #add new qualification to a text file in current directory for easy access
    qual_list_file = open("qual_list_file.txt", "a")
    qual_list_file.writelines(response)
    return response

# list all qualification types

def list_qual_types(qual_query):
   response = mturk.list_qualification_types(
        Query=qual_query,
        MustBeRequestable=False,
        MustBeOwnedByCaller=True
        )
   return response

# delete qualifications
    
def delete_qual_type(qual_query):
    qual_to_delete = list_qual_types(qual_query)
    response = mturk.delete_qualification_type(
        QualificationTypeId=qual_to_delete
    )
    return response

# delete HITs
    
def delete_HIT(HIT_id):
    response = mturk.delete_hit(
        HITId='string'
    )
    return response

    









