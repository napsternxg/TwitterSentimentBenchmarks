
# coding: utf-8

# In[1]:

from twarc import Twarc
import json as json

import pandas as pd
import tqdm
import requests



def collect_timelines(input_file, output_file, credentials_file):
    with open(credentials_file) as fp:
        credentials = tuple(map(str.strip, fp.readlines()))
    twarc_obj = Twarc(*credentials)
    df = pd.read_csv(input_file, sep="\t")
    with open(output_file, "w+") as fp:
        total = 0
        found_users = 0
        pbar = tqdm.tqdm(df.values)
        for uid, tid, u_statuses in pbar:
            found = 0
            pbar.set_description("User {}".format(uid))
            try:
                for tweet_json in twarc_obj.timeline(user_id="{}".format(uid)):
                    found += 1
                    if found > 190:
                        break
                    total += 1
                    print(json.dumps(tweet_json), file=fp)
                    pbar.set_postfix(found=found_users+1, total=total)
            except requests.exceptions.HTTPError as e:
                pbar.write("Error for uid={}. {}".format(uid, e))
            else:
                found_users += 1
        pbar.close()
    print("Collected {} tweets.".format(total))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get user timelines')
    parser.add_argument('--input-file', type=str, required=True,
            help='tab seperated input file with 3 columns where 1st column should be user id. Should have a header.')
    parser.add_argument('--output-file', type=str, required=True,
            help='path to the file to store json output.')
    parser.add_argument('--cred-file', type=str, required=True,
            help='path to twitter credentials text file.')

    args = parser.parse_args()
    collect_timelines(args.input_file, args.output_file, args.cred_file)
