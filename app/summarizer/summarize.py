from string import punctuation
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest


def summarize(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract tokens, excluding stop words and punctuation
    tokens = [
        token.text.lower()
        for token in doc
        if token.text.lower() not in STOP_WORDS and token.text not in punctuation
    ]

    # Calculate word frequencies
    word_frequencies = {}
    for word in tokens:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

    # Extract sentences and convert generator to list
    sentences = list(doc.sents)

    # Calculate scores for each sentence
    sentence_scores = {}
    for sentence in sentences:
        for word in sentence:
            if word.text.lower() in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sentence] += word_frequencies[word.text.lower()]

    # Ratio for summarization
    ratio = 0.1
    select_length = max(
        1, int(len(sentences) * ratio)
    )  # Ensure at least one sentence is selected

    # Select the top sentences based on their scores
    summary_sentences = nlargest(
        select_length, sentence_scores, key=sentence_scores.get
    )

    # Create the final summary by joining the selected sentences
    final_summary = [sentence.text for sentence in summary_sentences]
    return " ".join(final_summary)
