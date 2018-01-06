#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 10:59:40 2018

@author: Jared
"""

## Import steem-python's Blog class
from steem.blog import Blog
## Pandas to make the info look pretty
import pandas as pd
## replace 'UserName' with the steemit username you are looking up
b = Blog('UserName')

## I think there is a better way to pull blog posts, as this can take some time. 
## Beneficiary payouts didn't start until HF18, so if we limit this to only posts that occurred after that,
## it would take less time and bandwidth to run it. For now, it is what it is.
history=list(b.all())

## We will use this DataFrame later
allpostDf=pd.DataFrame([])

## Here we begin iterating through every post
for x in range(len(history)):
## Defines p as the current post for each iteration    
    p=history[x]
## Separates the title for labeling purposes 
    postName=p.export()['root_title']
## Just so we know which post we're currently on, not necessary really
    print(postName)
## p.export() produces every detail on each post, we only need certain
## details. Like beneficiary and payout.
    postBeneficiary=p.export()['beneficiaries']
## There are a few payout values associated with a post, total_payout_value is the amount
## of SBD that actually went (0 for pending payouts) to the author/beneficiaries
    postPay=p.export()['total_payout_value']
## Here we make sure we are not working with posts that haven't paid out yet.
    if postPay['amount'] > 0.0:
## Here we check to make sure we are not working with posts that don't have a beneficiary
        if postBeneficiary:
## This section does the dirty work, separating the data we need into columns, and calculating the actual amount
## for the beneficiary.            
            for beneficiary in postBeneficiary:
                print(p.export())
                benePercent=((beneficiary['weight']/100)/100)
## We put it all in a pandas DataFrame
                tempDf=pd.DataFrame({'post':postName,
                                 'beneficiary':beneficiary['account'],
                                 'beneficiarypercentage':beneficiary['weight']/100,
                                 'SBD Payout':postPay['amount'],
                                 'SBD to Beneficiary':postPay['amount']*benePercent
                                 }, index=[x])
                print(tempDf)
## Here we append it to the DataFrame we made earlier 
               allpostDf=allpostDf.append(tempDf)
        else:
            print('No beneficiary')
    else:
        print('Post has not paid out yet')        

## Now we put it in a csv, where it can be played with in your favorite spreadsheet program
    allpostDf.to_csv('beneficiaryRewards.csv')