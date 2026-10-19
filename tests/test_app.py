
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


    def test_complex_negation(self):
        result = analyze_text("I don't think this is good.")
        self.assertEqual(result["sentiment"], "Negative")

    
    def test_complex_negation_with_extra_word(self):
        result = analyze_text("I don't really think this is good.")
        self.assertEqual(result["sentiment"], "Negative")

    def test_negated_negative_word_in_longer_phrase(self):
        result = analyze_text("I don't dislike this.")
        self.assertEqual(result["sentiment"], "Positive")


    def test_mixed_sentiment(self):
        result = analyze_text(
            "The movie is good, but the ending is terrible."
        )
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["sentiment"], "Negative")


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
        self.assertEqual(result["sentiment"], "Positive")


    def test_negation_does_not_affect_unrelated_word(self):
        result = analyze_text("This is not good, but the movie is excellent.")
        self.assertEqual(result["positive_count"], 1)
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["sentiment"], "Positive")


    def test_intensifier_increases_positive_score(self):
        normal = analyze_text("This is good.")
        intensified = analyze_text("This is very good.")

        self.assertGreater(
            intensified["positive_score"],
            normal["positive_score"]
        )

    def test_downtoner_reduces_positive_score(self):
        normal = analyze_text("This is good.")
        weakened = analyze_text("This is slightly good.")

        self.assertLess(
            weakened["positive_score"],
            normal["positive_score"]
        )


    def test_intensifier_increases_negative_score(self):
        normal = analyze_text("This is bad.")
        intensified = analyze_text("This is very bad.")

        self.assertGreater(
            intensified["negative_score"],
            normal["negative_score"]
        )

    def test_downtoner_reduces_negative_score(self):
        normal = analyze_text("This is bad.")
        weakened = analyze_text("This is slightly bad.")

        self.assertLess(
            weakened["negative_score"],
            normal["negative_score"]
        )


    def test_negation_with_intensifier(self):
        result = analyze_text("This is not very good.")

        self.assertEqual(result["sentiment"], "Negative")
        self.assertGreater(
            result["negative_score"],
            result["positive_score"]
        )


    def test_weighted_sentiment_after_but(self):
        result = analyze_text(
            "This is very bad, but the ending is good."
        )

        self.assertGreater(
            result["positive_score"],
            result["negative_score"]
        )

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
