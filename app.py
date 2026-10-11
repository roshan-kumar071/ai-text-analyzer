from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

positive_words = [
    "good", "great", "happy", "excellent", "amazing",
    "love", "best", "wonderful", "success", "beautiful"
]

negative_words = [
    "bad", "sad", "hate", "worst", "terrible",
    "poor", "angry", "awful", "failure", "disappointing"
]

stop_words = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "in", "on", "for", "it", "this", "that", "was",
    "are", "i", "you", "he", "she", "we", "they"
}


def analyze_text(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower())

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

    positive_count = sum(
        word_counts[word] for word in positive_words
    )

    negative_count = sum(
        word_counts[word] for word in negative_words
    )

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "word_count": len(words),
        "character_count": characters,
        "characters_without_spaces": characters_without_spaces,
        "sentence_count": sentences,
        "paragraph_count": len(paragraphs),
        "frequent_words": frequent_words,
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