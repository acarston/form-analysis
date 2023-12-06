import sys
import os
import csv
from textfile_wrapper import TextFile
from word_data import WordData
from sia_data import SiaData

# comment out after first run
# import nltk
# nltk.download('vader_lexicon')

# interpret command-line arguments
def is_default() -> bool:
    if len(sys.argv) > 2:
        print("Too many arguments. Try -h or --help for more info.")
        sys.exit(0)

    if len(sys.argv) < 2 or sys.argv[1] == '-s': return True
    if sys.argv[1] == '-c': return False

    print('\nUsage: python main.py [option]\n-c\t\tTotal number of occurences for each word\n-h, --help\tDisplay this message\n-s\t\tNumber of people using at least one of each word (default)\n')
    sys.exit(0)

# translate raw form data to WordData format
def format_csv(form_path, out_path: str, names: bool = False, headers: bool = True) -> None:
    textfile = TextFile()
    with open(form_path) as csvfile:
        reader = csv.reader(csvfile)
        if headers: next(reader)
        for i, row in enumerate([r for r in reader if len(r) != 0], 1):
            if names: textfile.set_input(row[1], row[0])
            else: textfile.set_input(row[0], str(i))
            textfile.parse_into_tree()

    textfile.print_words(out_path)

def main():
    os.chdir(os.path.dirname(__file__))

    # configure input and output files
    DATA_DIR = './data/'
    FORM_CSV = f'{DATA_DIR}GE_size_comments.csv'
    WORDS_CSV = f'{DATA_DIR}words.csv'
    WORDS_ALPHA_JSON = f'{DATA_DIR}words_alpha.json'
    WORDS_COUNT_JSON = f'{DATA_DIR}words_count.json'
    WORDS_ALPHA_PNG = f'{DATA_DIR}words_alpha.png'
    WORDS_COUNT_PNG = f'{DATA_DIR}words_count.png'
    SENTIMENT_INFO_JSON = f'{DATA_DIR}sentiment_info.json'
    SENTIMENT_SUMMARY_JSON = f'{DATA_DIR}sentiment_summary.json'
    SENTIMENT_SUMMARY_PNG = f'{DATA_DIR}sentiment_summary.png'

    format_csv(FORM_CSV, WORDS_CSV)

    # comment out as needed
    word_data = WordData(WORDS_CSV, is_default())
    word_data.dump(WORDS_ALPHA_JSON)
    # word_data.plot_words('Word Frequencies by Alphabetical Order', WORDS_ALPHA_PNG)
    word_data.sort_by_count()
    word_data.dump(WORDS_COUNT_JSON)
    # word_data.plot_words('Word Frequencies by Number of Occurences', WORDS_COUNT_PNG)

    siaInfo = SiaData(FORM_CSV)
    siaInfo.dump_info(SENTIMENT_INFO_JSON)
    siaInfo.dump_summary(SENTIMENT_SUMMARY_JSON)
    siaInfo.plot_summary(SENTIMENT_SUMMARY_PNG)

if __name__ == "__main__":
    main()