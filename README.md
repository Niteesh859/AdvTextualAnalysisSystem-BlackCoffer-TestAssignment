# Text Analysis of Articles

This project extracts articles from a list of URLs, performs textual analysis on the content, and outputs a structured data file with various text metrics.

## Objective

The primary objective of this project is to perform a comprehensive textual analysis of articles from given URLs. This involves:
1.  **Data Extraction:** Scraping article titles and content from the web.
2.  **Textual Analysis:** Calculating various metrics such as sentiment scores, readability indices, and word counts.
3.  **Output Generation:** Saving the results in a structured format (CSV) for further analysis.

## Project Structure

```
.
├── 20211030 Test Assignment
│   ├── Article_txt_files/      # Directory for storing extracted article text files
│   ├── MasterDictionary/       # Contains lists of positive and negative words
│   │   ├── negative-words.txt
│   │   └── positive-words.txt
│   ├── StopWords/              # Contains lists of stop words to be excluded from analysis
│   │   ├── StopWords_Auditor.txt
│   │   ├── StopWords_Currencies.txt
│   │   ├── StopWords_DatesandNumbers.txt
│   │   ├── StopWords_Generic.txt
│   │   ├── StopWords_GenericLong.txt
│   │   ├── StopWords_Geographic.txt
│   │   └── StopWords_Names.txt
│   ├── Input.xlsx              # Input file containing URLs to be analyzed
│   ├── Objective.docx          # Project objective description
│   ├── Output Data Structure.xlsx # Template for the output data
│   └── Output.csv              # Final output file with analysis results
└── files
    ├── extractor.py            # Script to extract articles from URLs
    └── text_analysis.py        # Script to perform text analysis
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    Make sure you have Python installed. Then, install the required libraries using pip:
    ```bash
    pip install pandas requests beautifulsoup4 tqdm openpyxl
    ```

## Usage

1.  **Run the extractor script:**
    This script will read the URLs from `20211030 Test Assignment/Input.xlsx`, scrape the articles, and save them as text files in the `20211030 Test Assignment/Article_txt_files` directory.

    ```bash
    python files/extractor.py
    ```

2.  **Run the text analysis script:**
    This script will perform the textual analysis on the extracted text files and generate the `Output.csv` file.

    ```bash
    python files/text_analysis.py "20211030 Test Assignment"
    ```

## Output

The final output is a CSV file named `Output.csv` located in the `20211030 Test Assignment` directory. The file contains the following columns for each article:

*   **URL_ID:** Unique identifier for each URL.
*   **URL:** The URL of the article.
*   **POSITIVE SCORE:** The number of positive words in the article.
*   **NEGATIVE SCORE:** The number of negative words in the article.
*   **POLARITY SCORE:** A score indicating the sentiment of the article (between -1 and +1).
*   **SUBJECTIVITY SCORE:** A score indicating the subjectivity of the article.
*   **AVG SENTENCE LENGTH:** The average length of sentences in the article.
*   **PERCENTAGE OF COMPLEX WORDS:** The percentage of words with three or more syllables.
*   **FOG INDEX:** The Gunning Fog Index, a readability measure.
*   **AVG NUMBER OF WORDS PER SENTENCE:** The average number of words per sentence.
*   **COMPLEX WORD COUNT:** The total number of complex words.
*   **WORD COUNT:** The total number of words in the article.
*   **SYLLABLE PER WORD:** The average number of syllables per word.
*   **PERSONAL PRONOUNS:** The number of personal pronouns.
*   **AVG WORD LENGTH:** The average length of words in the article.
