# form-analysis
## Functionality
Give the program a csv file with names (optional) and their respective text blobs (such as responses from a survey) and the program will:
- Record the words/2-word phrases that appear in the text blobs, alphabetically and/or by number of occurences
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
4. The program expects either the name in the first column and the text blob in the second column, or just the text blobs. Text blobs should be in quotes. Your file can have headers. Empty lines (if you have any) are ignored
5. Uncomment/comment functions in main.py according to instructions/preference
6. Run main.py. It is recommended to run ```python main.py --help``` first, so you know what flags to set (otherwise you may encounter undefined behavior). If you want to parse 2-word phrases instead of singular words, specify this with ```-p```. By default, the data will be organized according to how many respondents mentioned a particular word or phrase. To organize according to the total number of occurences of each word, specify this with ```-c```
