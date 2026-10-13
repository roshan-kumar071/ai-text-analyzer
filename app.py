from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

positive_words = {
    "good", "great", "happy", "excellent", "amazing",
    "love", "best", "wonderful", "success", "beautiful",
    "awesome", "fantastic", "perfect", "enjoy", "helpful",
    "kind", "brilliant", "positive", "delightful", "superb"
}

negative_words = {
    "bad", "sad", "hate", "worst", "terrible", "dislike",
    "poor", "angry", "awful", "failure", "disappointing",
    "horrible", "wrong", "useless", "negative", "annoying",
    "boring", "difficult", "problem", "painful", "unhappy"
}


negation_words = {
    "not", "no", "never", "neither", "nor",
    "hardly", "barely", "scarcely",
    "isn't", "aren't", "wasn't", "weren't",
    "don't", "doesn't", "didn't",
    "can't", "couldn't", "won't", "wouldn't",
    "shouldn't", "haven't", "hasn't", "hadn't"
}


stop_words = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "in", "on", "for", "it", "this", "that", "was",
    "are", "i", "you", "he", "she", "we", "they",
    "my", "your", "our", "with", "as", "at", "be",
    "by", "from", "have", "has", "had", "not", "but"
}


def analyze_text(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower())

    sentiment_tokens = re.findall(
        r"[.!?]+|[a-zA-Z]+(?:['’-][a-zA-Z]+)*",
        text.lower()
    )


    characters = len(text)
    characters_without_spaces = len(re.sub(r"\s", "", text))

    sentences = len(re.findall(r"[.!?]+", text))
    if text.strip() and sentences == 0:
        sentences = 1

    paragraphs = [
        paragraph for paragraph in text.splitlines()
        if paragraph.strip()
    ]

    word_counts = Counter(words)

    frequent_words = [
        {"word": word, "count": count}
        for word, count in word_counts.most_common()
        if word not in stop_words
    ][:5]
    
    normalized_text = text.lower().replace("’", "'")

    complex_negative_phrases = [
        "don't think",
        "do not think",
        "doesn't think",
        "does not think",
        "didn't think",
        "did not think",
    ]

    has_complex_negation = any(
        phrase in normalized_text
        for phrase in complex_negative_phrases
    )
    
    positive_count = 0
    negative_count = 0
    negation_window = 3
    sentence_boundaries = {".", "!", "?"}
    contrast_words = {"but", "however"}

    for index, word in enumerate(sentiment_tokens):
        if word in sentence_boundaries:
            continue

        if word in contrast_words:
            continue

        previous_words = sentiment_tokens[
            max(0, index - negation_window):index
        ]

        is_negated = False

        
        previous_words = sentiment_tokens[
            max(0, index - negation_window):index
        ]

        is_negated = False

        for previous_word in previous_words:
            if previous_word in sentence_boundaries:
                is_negated = False

            elif previous_word in contrast_words:
                is_negated = False

            elif previous_word in negation_words:
                is_negated = True

        segment_start = 0

        for previous_index in range(index - 1, -1, -1):
            if sentiment_tokens[previous_index] in (
                sentence_boundaries | contrast_words
            ):
                segment_start = previous_index + 1
                break

        segment_words = sentiment_tokens[segment_start:index]

        
        for phrase in complex_negative_phrases:
            phrase_words = phrase.split()
            phrase_length = len(phrase_words)

            for start in range(
                len(segment_words) - phrase_length + 1
            ):
                if segment_words[start:start + phrase_length] == phrase_words:
                    is_negated = True
                    break

            if is_negated:
                break

        if word in positive_words:
            if is_negated:
                negative_count += 1
            else:
                positive_count += 1

        elif word in negative_words:
            if is_negated:
                positive_count += 1
            else:
                negative_count += 1

    sentiment_total = positive_count + negative_count

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"


    if sentiment_total:
        positive_percentage = round(
            positive_count / sentiment_total * 100, 1
        )
        negative_percentage = round(
            negative_count / sentiment_total * 100, 1
        )
    else:
        positive_percentage = 0
        negative_percentage = 0

    return {
        "word_count": len(words),
        "character_count": characters,
        "characters_without_spaces": characters_without_spaces,
        "sentence_count": sentences,
        "paragraph_count": len(paragraphs),
        "frequent_words": frequent_words,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "sentiment": sentiment,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        result = analyze_text(text)

    return render_template(
        "index.html",
        result=result,
        text=text
    )


if __name__ == "__main__":
    app.run(debug=True)