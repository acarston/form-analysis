from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import json
from numpy import mean
from numpy import sum
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

class SiaData:
    def __init__(self, form_path: str) -> None:
        self.form_path = form_path
        self.__set_sentiment_info()
        self.__set_sentiment_summary()

    # store sentiment analysis scores for each response
    def __set_sentiment_info(self) -> None:
        sia = SentimentIntensityAnalyzer()
        self.sia_info: list[dict[str, str | float]] = []
        with open (self.form_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                ps = sia.polarity_scores(row[1])
                self.sia_info.append({
                    'name': row[0],
                    'neg': ps['neg'],
                    'neu': ps['neu'],
                    'pos': ps['pos'],
                    'compound': ps['compound']
                })
    
    # categorize reponses into pos, neu, neg based on compound score
    def __set_sentiment_summary(self) -> None:
        # set thresholds arbitrarily
        BIAS = 0.4
        # count negative, neutral, positive responses
        self.summary: list[int] = [0, 0, 0]
        for block in self.sia_info:
            com: float = block['compound']
            if com < -BIAS: self.summary[0] += 1
            elif com < BIAS: self.summary[1] += 1
            else: self.summary[2] += 1

    def plot_summary(self, out_path: str) -> None:
        fig, ax = plt.subplots(figsize=(8, 5))

        xlabels = 'negative', 'neutral', 'positive'
        ax.bar(xlabels, self.summary)
        ax.set_xlabel('Sentiment')
        ax.set_xticks(range(len(self.summary)), labels=xlabels, rotation='vertical')
        ax.set_ylabel('Occurences')
        loc = plticker.MultipleLocator(base=1)
        ax.yaxis.set_major_locator(loc)
        ax.set_title('Responses by Estimated Sentiment')

        plt.savefig(out_path, dpi=600, bbox_inches='tight')
    
    def dump_info(self, out_path: str):
        json.dump({
            'people': self.sia_info,
            'averages': {
                'neg': mean([block['neg'] for block in self.sia_info]),
                'neu': mean([block['neu'] for block in self.sia_info]),
                'pos': mean([block['pos'] for block in self.sia_info])
            }
        }, open(out_path, 'w'))

    def dump_summary(self, out_path: str):
        json.dump({
            'responses': {
                'negative': self.summary[0],
                'neutral': self.summary[1],
                'positive': self.summary[2],
                'total': int(sum(self.summary))
            }
        }, open(out_path, 'w'))