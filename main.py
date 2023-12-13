import sys
import os
import csv
from textfile_wrapper import TextFile
from word_data import WordData
from sia_data import SiaData

# comment out after first run
import nltk
nltk.download('vader_lexicon')

# interpret command-line arguments
def get_options() -> dict[str, bool]:    
    if '-h' in sys.argv or '--help' in sys.argv: 
        print('\nUsage: python main.py [options]\n-c\t\tSort by total number of occurences for each word\n-d\t\tSpecify if the input file has headers\n-h, --help\tDisplay this message\n-n\t\tSpecify if the input file has names in the first column\n-p\t\tparse words as 2-letter phrases\n-s\t\tSort by number of people using at least one of each word (default)\n')
        sys.exit(0)
 
    options: dict[str, bool] = {}
    if '-c' in sys.argv:
        if '-s' in sys.argv: 
            print('Conflicting arguments. Try -h or --help for more info.')
            sys.exit(0)
        options['sort by people'] = False
    else: options['sort by people'] = True

    if '-p' in sys.argv: options['phrases'] = True
    else: options['phrases'] = False

    if '-n' in sys.argv: options['names'] = True
    else: options['names'] = False

    if '-d' in sys.argv: options['headers'] = True
    else: options['headers'] = False

    return options

# translate raw form data to WordData format
def format_csv(form_path: str, out_path: str, phrases: bool, names: bool, headers: bool) -> None:
    textfile = TextFile()
    with open(form_path) as csvfile:
        reader = csv.reader(csvfile)
        if headers: next(reader)
        for i, row in enumerate([r for r in reader if len(r) != 0], 1):
            if names: textfile.set_input(row[1], row[0])
            else: textfile.set_input(row[0], str(i))
            textfile.parse_into_tree(phrases)

    textfile.print_words(out_path)

def main():
    options = get_options()

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

    format_csv(FORM_CSV, WORDS_CSV, options['phrases'], options['names'], options['headers'])

    # comment out as needed
    word_data = WordData(WORDS_CSV, options['sort by people'])
    word_data.dump(WORDS_ALPHA_JSON)
    # word_data.plot_words('Word Frequencies by Alphabetical Order', WORDS_ALPHA_PNG)
    word_data.sort_by_count()
    word_data.dump(WORDS_COUNT_JSON)
    # word_data.plot_words('Word Frequencies by Number of Occurences', WORDS_COUNT_PNG)

    siaInfo = SiaData(FORM_CSV, options['names'], options['headers'])
    siaInfo.dump_info(SENTIMENT_INFO_JSON)
    siaInfo.dump_summary(SENTIMENT_SUMMARY_JSON)
    siaInfo.plot_summary(SENTIMENT_SUMMARY_PNG)

if __name__ == "__main__":
    main()