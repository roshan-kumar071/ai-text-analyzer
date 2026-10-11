
import unittest
from app import app, analyze_text


class TestTextAnalyzer(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_positive_sentiment(self):
        result = analyze_text(
            "I love this amazing project. It is excellent."
        )
        self.assertEqual(result["sentiment"], "Positive")
        self.assertEqual(result["positive_count"], 3)
        self.assertEqual(result["negative_count"], 0)

    def test_negative_sentiment(self):
        result = analyze_text(
            "This is a terrible and awful failure."
        )
        self.assertEqual(result["sentiment"], "Negative")

    def test_neutral_sentiment(self):
        result = analyze_text(
            "The book is on the table."
        )
        self.assertEqual(result["sentiment"], "Neutral")

    def test_word_count(self):
        result = analyze_text("Python is great.")
        self.assertEqual(result["word_count"], 3)

    
    def test_negated_positive_word(self):
        result = analyze_text("This is not good.")
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["positive_count"], 0)
        self.assertEqual(result["sentiment"], "Negative")

    def test_negated_negative_word(self):
        result = analyze_text("This is not bad.")
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["negative_count"], 0)
        self.assertEqual(result["sentiment"], "Positive")

    
    def test_negation_with_extra_word(self):
        result = analyze_text("This is not very good.")
        self.assertEqual(result["sentiment"], "Negative")

    def test_negation_with_extra_words(self):
        result = analyze_text("This is not bad at all.")
        self.assertEqual(result["sentiment"], "Positive")

    
    def test_negation_does_not_affect_later_sentence(self):
        result = analyze_text("This is not good. This is excellent.")
        self.assertEqual(result["sentiment"], "Neutral")
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["negative_count"], 1)

    
    def test_negation_resets_after_exclamation(self):
        result = analyze_text("This is not good! This is excellent.")
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["sentiment"], "Neutral")

    def test_negation_resets_after_but(self):
        result = analyze_text("This is not good, but excellent.")
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["sentiment"], "Neutral")

    
    def test_negation_does_not_affect_unrelated_word(self):
        result = analyze_text("This is not good, but the movie is excellent.")
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["sentiment"], "Neutral")


    def test_empty_text(self):
        result = analyze_text("")
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["sentiment"], "Neutral")

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_analysis_form(self):
        response = self.client.post(
            "/",
            data={"text": "I love this amazing project."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Positive", response.data)


if __name__ == "__main__":
    unittest.main()
