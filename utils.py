import pandas as pd
import numpy as np

import json
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context('paper')
sns.set_style('ticks')

import glob
import re

from statsmodels.api import OLS, MNLogit, Logit
from scipy.stats import ttest_ind

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import classification_report, confusion_matrix


def print_filenames(filenames, title="English"):
    print "%s Files:\n%s\n" % (
        title, "\n".join("[%s] %s" % k for k in enumerate(filenames)))
    
def filter_filenames(filenames, pattern=None):
    if pattern is not None:
        for fname in filenames:
            if pattern.match(fname):
                yield fname
                
def get_tweet_ids(fp):
    for line in fp:
        yield line.split("\t")[0]
        
def get_id_set(files):
    tids = set()
    for fid, fname in enumerate(files):
        old_count = len(tids)
        with open(fname) as fp:
            tids.update(tid for tid in get_tweet_ids(fp))
            print "[%s] New ids in %s: %s" % (fid, fname, len(tids) - old_count)
    return tids

def map_id_sets(files, fetched_tweet_ids):
    tids = set()
    missing_tids = set()
    for fid, fname in enumerate(files):
        missing_ids = 0
        total_ids = 0
        with open(fname) as fp:
            for tid in get_tweet_ids(fp):
                tid = int(tid)
                tids.add(tid)
                total_ids += 1
                if tid not in fetched_tweet_ids:
                    missing_ids += 1
                    missing_tids.add(tid)
            print "[%s] %s:\n\t%s [Total] %s [Found] %s [Missing] (%.3f %% missing)" % (
                fid, fname, total_ids, total_ids - missing_ids, missing_ids,
                missing_ids * 100./total_ids
            )
    print "Overall: %s [Total] %s [Found] %s [Missing] (%.3f %% missing)\n%s" % (
        len(tids), len(tids) - len(missing_tids), len(missing_tids),
        len(missing_tids) * 100./len(tids), '=='*20
    )
                    
                
def simple_extractor_func(t_data, line):
    user_info = t_data[u'user']
    return (t_data[u'id'],
            t_data[u'favorite_count'],
            t_data[u'is_quote_status'],
            t_data[u'in_reply_to_status_id'] is None,
            t_data[u'retweet_count'],
            user_info[u'followers_count'],
            user_info[u'friends_count'],
            user_info[u'listed_count'],
            user_info[u'statuses_count'],
           ) + tuple(line)

def get_training_data(fname, TWEET_ID2DATA, extractor_func=simple_extractor_func,
                     line_extractor=lambda x: x[1:2], sep='\t', header=False):
    training_data = []
    missing_ids = 0
    with open(fname) as fp:
        for line in fp:
            line = tuple(line.strip().split(sep))
            if header:
                print "Reading header: ", line
                header = False
                continue
            tid = int(line[0])
            line = line_extractor(line)
            if tid not in TWEET_ID2DATA:
                missing_ids += 1
                continue
            t_data = TWEET_ID2DATA[tid]
            training_d = extractor_func(t_data, line)
            training_data.append(training_d)
    print "Missing data: %s, number of annotater items: %s" % (missing_ids, len(line))
    return training_data

def parse_classification_report(report, to_df=True):
    report_list = []
    for i, line in enumerate(report.split("\n")):
        if i == 0:
            report_list.append(["label_class", "precision", "recall", "f1-score", "support"])
        else:
            line = line.strip()
            if line:
                if line.startswith("avg"):
                    line = line.replace("avg / total", "avg/total")
                line = re.split(r'\s+', line)
                line = line[:1] + map(float, line[1:-1]) + map(int, line[-1:])
                report_list.append(tuple(line))
    if not to_df:
        return report_list
    return pd.DataFrame(report_list[1:], columns=report_list[0]).set_index("label_class")


def xboost_compat_df_cols(cols):
    up_cols = []
    for c in cols:
        c = re.sub(r'[\[\]]', '_', c)
        c = re.sub(r'<', '_lt_', c)
        up_cols.append(c)
    return up_cols
            
