from string import punctuation
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest


def summarize(text, max_words=50):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    tokens = [
        token.text.lower()
        for token in doc
        if token.text.lower() not in STOP_WORDS and token.text not in punctuation
    ]

    word_frequencies = {}
    for word in tokens:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    sentences = list(doc.sents)

    sentence_scores = {}
    for sentence in sentences:
        for word in sentence:
            if word.text.lower() in word_frequencies:
                sentence_scores[sentence] = (
                    sentence_scores.get(sentence, 0)
                    + word_frequencies[word.text.lower()]
                )

    summary_sentences = []
    total_words = 0

    for sentence in nlargest(
        len(sentence_scores), sentence_scores, key=sentence_scores.get
    ):
        sentence_word_count = len(sentence.text.split())
        if total_words + sentence_word_count > max_words:
            continue
        summary_sentences.append(sentence.text)
        total_words += sentence_word_count
        if total_words >= max_words:
            break

    return " ".join(summary_sentences)
