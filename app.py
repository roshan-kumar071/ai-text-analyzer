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
        "don't really think",
        "do not think",
        "do not really think",
        "doesn't think",
        "doesn't really think",
        "does not think",
        "does not really think",
        "didn't think",
        "didn't really think",
        "did not think",
        "did not really think",
    ]
    
    has_complex_negation = any(
        phrase in normalized_text
        for phrase in complex_negative_phrases
    )


    positive_count = 0
    negative_count = 0
    positive_score = 0
    negative_score = 0

    intensifiers = {
        "very": 1.5,
        "extremely": 2.0,
        "really": 1.5,
        "incredibly": 2.0,
        "absolutely": 2.0,
    }

    downtoners = {
        "slightly": 0.5,
        "somewhat": 0.75,
        "mildly": 0.5,
    }


    negation_window = 3
    sentence_boundaries = {".", "!", "?"}
    contrast_words = {"but", "however"}
    contrast_weight = 2.0

    for index, word in enumerate(sentiment_tokens):
        if word in sentence_boundaries or word in contrast_words:
            continue

        previous_words = sentiment_tokens[
            max(0, index - negation_window):index
        ]

        is_negated = False

        for previous_word in reversed(previous_words):
            if previous_word in sentence_boundaries or previous_word in contrast_words:
                break

            if previous_word in negation_words:
                is_negated = True
                break

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

        modifier = 1.0

        if previous_words:
            previous_word = previous_words[-1]

            if previous_word in intensifiers:
                modifier *= intensifiers[previous_word]
            elif previous_word in downtoners:
                modifier *= downtoners[previous_word]

        for previous_index in range(index - 1, -1, -1):
            previous_token = sentiment_tokens[previous_index]

            if previous_token in sentence_boundaries:
                break

            if previous_token in contrast_words:
                modifier *= contrast_weight
                break

        if word in positive_words:
            if is_negated:
                negative_count += 1
                negative_score += modifier
            else:
                positive_count += 1
                positive_score += modifier

        elif word in negative_words:
            if is_negated:
                positive_count += 1
                positive_score += modifier
            else:
                negative_count += 1
                negative_score += modifier

    sentiment_total = positive_count + negative_count

    if positive_score > negative_score:
        sentiment = "Positive"
    elif negative_score > positive_score:
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
        "positive_score": round(positive_score, 2),
        "negative_score": round(negative_score, 2),
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
