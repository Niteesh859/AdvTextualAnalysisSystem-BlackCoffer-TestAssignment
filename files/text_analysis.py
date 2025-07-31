import re
import pandas as pd
import os
import argparse
from tqdm import tqdm


def extract_words(file_path):
    """Extract words from file, one per line."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        words = [line.split()[0] for line in content.lower().splitlines() if line.strip()]
        return words
    except:
        return []


def extract_sentences(file_path):
    """Extract sentences from text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.lower().replace('\n', ' ')
        content = re.sub(r'https://\S+', '', content)
        sentences = re.split(r'[.?!:;]\s+', content)
        return [s.strip() for s in sentences if s.strip()]
    except:
        return []


def syllable_count(word):
    """Count syllables in a word."""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    
    if word and word[0] in vowels:
        count += 1
    
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    
    if word.endswith("e"):
        count -= 1
    
    return max(count, 1)


def analyze_text(sentences, positive_words, negative_words, stop_words):
    """Analyze text and return metrics."""
    if not sentences:
        return [0] * 13
    
    # Get all words
    all_words = []
    for sent in sentences:
        words = re.findall(r'\b\w+\b', sent)
        all_words.extend(words)
    
    if not all_words:
        return [0] * 13
    
    # Calculate scores
    pos_score = sum(1 for word in all_words if word in positive_words)
    neg_score = sum(1 for word in all_words if word in negative_words)
    
    polarity = (pos_score - neg_score) / (pos_score + neg_score + 0.000001)
    
    clean_words = [w for w in all_words if w not in stop_words]
    subjectivity = (pos_score + neg_score) / (len(clean_words) + 0.000001)
    
    avg_sent_len = len(all_words) / len(sentences)
    
    complex_words = sum(1 for word in all_words if syllable_count(word) >= 3)
    perc_complex = complex_words / len(all_words)
    
    fog_index = 0.4 * (avg_sent_len + perc_complex)
    
    avg_syllables = sum(syllable_count(w) for w in all_words) / len(all_words)
    avg_word_len = sum(len(w) for w in all_words) / len(all_words)
    
    pronouns = sum(1 for w in all_words if w in ['i', 'my', 'we', 'us', 'our'])
    
    return [
        pos_score,           # POSITIVE SCORE
        neg_score,           # NEGATIVE SCORE  
        polarity,            # POLARITY SCORE
        subjectivity,        # SUBJECTIVITY SCORE
        avg_sent_len,        # AVG SENTENCE LENGTH
        perc_complex,        # PERCENTAGE OF COMPLEX WORDS
        fog_index,           # FOG INDEX
        avg_syllables,       # AVG NUMBER OF WORDS PER SENTENCE
        complex_words,       # COMPLEX WORD COUNT
        len(all_words),      # WORD COUNT
        avg_syllables,       # SYLLABLE PER WORD
        pronouns,            # PERSONAL PRONOUNS
        avg_word_len         # AVG WORD LENGTH
    ]


def main():
    parser = argparse.ArgumentParser(description='Text Analysis using Excel template')
    parser.add_argument('root_dir', help='Root directory path')
    args = parser.parse_args()
    
    root_dir = args.root_dir
    
    # Load template
    template_file = os.path.join(root_dir, 'Output Data Structure.xlsx')
    if not os.path.exists(template_file):
        print(f"Template file not found: {template_file}")
        return
    
    df = pd.read_excel(template_file)
    
    # Load word lists
    stop_words = []
    stopwords_dir = os.path.join(root_dir, 'StopWords')
    if os.path.exists(stopwords_dir):
        for file in os.listdir(stopwords_dir):
            words = extract_words(os.path.join(stopwords_dir, file))
            stop_words.extend(words)
    stop_words = list(set(stop_words))
    
    # Load positive/negative words
    pos_file = os.path.join(root_dir, 'MasterDictionary', 'positive-words.txt')
    neg_file = os.path.join(root_dir, 'MasterDictionary', 'negative-words.txt')
    
    positive_words = list(set(extract_words(pos_file)) - set(stop_words)) if os.path.exists(pos_file) else []
    negative_words = list(set(extract_words(neg_file)) - set(stop_words)) if os.path.exists(neg_file) else []
    
    # Find articles directory
    articles_dir = os.path.join(root_dir, 'Article_txt_files')
    if not os.path.exists(articles_dir):
        articles_dir = os.path.join(root_dir, 'Aritcle_txt_files')
    
    # Process each row
    for i, row in tqdm(df.iterrows(), total=len(df)):
        url_id = row['URL_ID']
        txt_file = os.path.join(articles_dir, f'{url_id}.txt')
        
        if os.path.exists(txt_file):
            sentences = extract_sentences(txt_file)
            results = analyze_text(sentences, positive_words, negative_words, stop_words)
            
            # Fill results into DataFrame (matching column order)
            columns = ['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 
                      'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
                      'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
                      'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
            
            for j, col in enumerate(columns):
                if col in df.columns:
                    df.at[i, col] = results[j]
    
    # Save output
    output_file = os.path.join(root_dir, 'Output.csv')
    df.to_csv(output_file, index=False)
    print(f"Analysis complete! Output saved to: {output_file}")


if __name__ == "__main__":
    main()