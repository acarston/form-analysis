#include "pch.h"
#include "TextFile.h"

void TextFile::to_lower(std::string& str) {
    for (int i = 0; i < str.size(); ++i) {
        str[i] = tolower(str[i]);
    }
}

// sourced from https://stackoverflow.com/questions/4654636/
bool TextFile::is_number(const std::string& str) const {
    std::string::const_iterator it = str.begin();
    while (it != str.end() && std::isdigit(*it)) ++it;
    return !str.empty() && it == str.end();
}


int TextFile::compare(WordInfo*& current, WordInfo*& incoming) {
    if (incoming->word > current->word) return 1;
    else if (incoming->word < current->word) return -1;
    else return 0;
}

// add the incoming line number to a node already in the tree
// upon creation in parse_into_tree, WordInfo has exactly 1 element in its lines list
// so attempting to insert should yank this element and delete the created WordInfo
void TextFile::on_duplicate(WordInfo*& current, WordInfo*& incoming) {
    if (incoming->people.front() != current->people.back()) current->people.push_back(incoming->people.front());
    delete incoming;
    incoming = nullptr;
}

// specify the output upon traversal visit
void TextFile::to_console(WordInfo*& info) {
    info->count = info->people.size();
    std::cout << info->word << "(" << info->count << "): ";
    for (auto it = info->people.begin(); it != info->people.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}

void TextFile::to_file(WordInfo*& info, std::ofstream& fout) {
    info->count = info->people.size();
    fout << info->word + ",";

    auto it = info->people.begin();
    if (it != info->people.end()) fout << *it;
    for (it++; it != info->people.end(); ++it) {
        fout << ";" << *it;
    }

    fout << "," << info->count;
    fout << "\n";
}


void TextFile::remove_special_chars(std::string& word) const {
    while (true) {
        if (SPECIAL_CHARS.find(word[0]) != SPECIAL_CHARS.end()) word.replace(0, 1, "");
        else if (SPECIAL_CHARS.find(word[word.size() - 1]) != SPECIAL_CHARS.end()) word.replace(word.size() - 1, 1, "");
        else break;
    }
}

void TextFile::insert_word(std::string& word) {
    to_lower(word);
    remove_special_chars(word);

    if (THROW_WORDS.find(word) != THROW_WORDS.end()) return;

    WordInfo* wordInfo = new WordInfo(word, this->person);
    tree.insert(wordInfo, &compare, &on_duplicate);
}


void TextFile::set_input(const std::string& in, const std::string& person) {
    this->in = in;
    this->person = person;
}

// add each word in the file to the tree
void TextFile::parse_into_tree() {
    std::istringstream iss(this->in);
    std::string word;
    while (iss >> word) insert_word(word);
}

// output the words alphabetically
void TextFile::print_words() {
    tree.traverse_inorder(&to_console);
    std::cout << std::endl;
}

void TextFile::print_words(const std::string& filePath) {
    tree.traverse_inorder(&to_file, filePath);
}

void TextFile::print_input() const {
    std::cout << in << std::endl;
}