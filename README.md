# form-analysis
## Functionality
Give the program a csv file with names and their respective text blobs (such as responses from a survey) and the program will:
- Record the words that appear in the text blobs, alphabetically and/or by number of occurences
- Record the sentiment of each response
- Record the number of positive, neutral, and negative responses

All data is outputted to json, and a graph is saved as a png.
## Structure
- ```cpp_source```: C/C++ code to parse the text blobs 
- ```textfile_wrapper.py```: python wrapper for C functions
- ```textfile.dll```: dynamically linked library generated from ```cpp_source``` and used by ```textfile_wrapper.py```
- ```word_data.py```: organizes the words for output
- ```sia_data.py```: performs sentiment analysis using the ```nltk``` module
## Getting Started
1. Run ```pip install -r requirements.txt``` in your environment
2. In main.py, specify the directory to dump the data (DATA_DIR) and the path to the csv form (FORM_CSV). There is a test form you can use (data/foo.csv)
3. Optionally specify the data output paths
4. The input csv must not have headers. The program expects the name in the first column and the text blob in the second. Text blobs should be in quotes
5. Uncomment/comment functions in main.py according to instructions/preference
6. Run main.py
