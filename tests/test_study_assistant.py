import unittest
from study_assistant import answer_question, generate_quiz, summarize


NOTES = "Photosynthesis converts light energy into chemical energy. Chlorophyll absorbs sunlight in plant cells. The process releases oxygen."


class StudyAssistantTests(unittest.TestCase):
    def test_summary_only_returns_verbatim_evidence(self):
        summary = summarize(NOTES, 2)
        self.assertEqual(len(summary), 2)
        for sentence in summary:
            self.assertIn(sentence, NOTES)

    def test_quiz_answer_and_evidence_come_from_notes(self):
        questions = generate_quiz(NOTES)
        self.assertTrue(questions)
        for item in questions:
            self.assertIn(item.evidence, NOTES)
            self.assertIn(item.answer, item.evidence)
            self.assertIn("____", item.question)

    def test_zero_quiz_limit_returns_no_questions(self):
        self.assertEqual(generate_quiz(NOTES, limit=0), [])
    def test_question_answer_quotes_source_or_declines(self):
        answer = answer_question(NOTES, "What does photosynthesis convert?")
        self.assertIsNotNone(answer.evidence)
        self.assertIn(answer.evidence, NOTES)
        self.assertIn(answer.evidence, answer.text)
        unknown = answer_question(NOTES, "Who won the race?")
        self.assertIsNone(unknown.evidence)
        self.assertIn("can't answer", unknown.text)


if __name__ == "__main__":
    unittest.main()

