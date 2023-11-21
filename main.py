import os
import csv
from textfile_wrapper import TextFile
from word_data import WordData
from sia_data import SiaData

# uncomment for first run
# import nltk
# nltk.download('vader_lexicon')

# translate raw form data to WordData format
def format_csv(form_path, out_path: str) -> None:
    textfile = TextFile()
    with open(form_path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            textfile.set_input(row[1], row[0])
            textfile.parse_into_tree()

    textfile.print_words(out_path)

def main():
    os.chdir(os.path.dirname(__file__))

    # configure input and output files
    DATA_DIR = './data/'
    FORM_PATH = f'{DATA_DIR}foo.csv'
    WORDS_PATH = f'{DATA_DIR}words.csv'
    WORDS_ALPHA_JSON = f'{DATA_DIR}words_alpha.json'
    WORDS_COUNT_JSON = f'{DATA_DIR}words_count.json'
    WORDS_ALPHA_PNG = f'{DATA_DIR}words_alpha.png'
    WORDS_COUNT_PNG = f'{DATA_DIR}words_count.png'
    SENTIMENT_INFO_JSON = f'{DATA_DIR}sentiment_info.json'
    SENTIMENT_SUMMARY_JSON = f'{DATA_DIR}sentiment_summary.json'
    SENTIMENT_SUMMARY_PNG = f'{DATA_DIR}sentiment_summary.png'

    format_csv(FORM_PATH, WORDS_PATH)

    # comment out as needed
    word_data = WordData(WORDS_PATH)
    word_data.dump(WORDS_ALPHA_JSON)
    word_data.plot_words('Word Frequencies by Alphabetical Order', WORDS_ALPHA_PNG)
    word_data.sort_by_count()
    word_data.dump(WORDS_COUNT_JSON)
    word_data.plot_words('Word Frequencies by Number of Occurences', WORDS_COUNT_PNG)

    siaInfo = SiaData(FORM_PATH)
    siaInfo.dump_info(SENTIMENT_INFO_JSON)
    siaInfo.dump_summary(SENTIMENT_SUMMARY_JSON)
    siaInfo.plot_summary(SENTIMENT_SUMMARY_PNG)

if __name__ == "__main__":
    main()