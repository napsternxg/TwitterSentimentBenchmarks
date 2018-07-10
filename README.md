# TwitterSentimentBenchmarkDataAnalysis
Analysis on twitter sentiment analysis benchmark datasets as described in the paper [Shubhanshu Mishra and Jana Diesner. 2018. Detecting the Correlation between Sentiment and User-level as well as Text-Level Meta-data from Benchmark Corpora. In Proceedings of the 29th on Hypertext and Social Media (HT '18). ACM, New York, NY, USA, 2-10. DOI: https://doi.org/10.1145/3209542.3209562](https://dl.acm.org/citation.cfm?id=3209562)

If you plan to use this analysis please cite the following paper:
```
@inproceedings{Mishra2018,
  doi = {10.1145/3209542.3209562},
  url = {https://doi.org/10.1145/3209542.3209562},
  year  = {2018},
  publisher = {{ACM} Press},
  author = {Shubhanshu Mishra and Jana Diesner},
  title = {Detecting the Correlation between Sentiment and User-level as well as Text-Level Meta-data from Benchmark Corpora},
  booktitle = {Proceedings of the 29th on Hypertext and Social Media  - {HT} {\textquotesingle}18}
}
```

## Data sources:
* SemEval - http://alt.qcri.org/semeval2017/task4/
* Airline - https://www.kaggle.com/crowdflower/twitter-airline-sentiment
* GOP Debate - https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment
* Clarin - https://www.clarin.si/repository/xmlui/handle/11356/1054 
* HCR - https://bitbucket.org/speriosu/updown/wiki/Getting%20Started
* Obama - https://bitbucket.org/speriosu/updown/wiki/Getting%20Started

## Detecting the correlation between sentiment and user-level as well as text-level meta-data from benchmark corpora

Code for this analysis will can be seen in following files:
* [Prepare all data for analysis - Join_all_data.ipynb](./Join_all_data.ipynb)
* [Analyze the original benchmark datasets - Empirical_Analysis.ipynb](./Empirical_Analysis.ipynb)
* [Models based on meta, text, and joint features - Text_models.ipynb](./Text_models.ipynb)
* [Get user's timeline tweets - Get_user_timelines.ipynb](./Get_user_timelines.ipynb)
* [Predict timeline tweets using Vader Sentiment - Vader_sentiment_prediction.ipynb](./Vader_sentiment_prediction.ipynb)
* [Analyze the timeline data - Time_line_aggregates.ipynb](./Time_line_aggregates.ipynb)

Code released under [GNU General Public License v3.0](./LICENSE)
