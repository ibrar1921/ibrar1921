import unittest
from engine import Progress

class EngineTests(unittest.TestCase):
    def test_next_question_is_stable(self):
        state = Progress()
        self.assertEqual(state.next_question().id,state.next_question().id)
    def test_correct_answer_updates_state(self):
        state = Progress(); q = state.next_question()
        r = state.answer(q.id,q.correct)
        self.assertTrue(r["correct"])
        self.assertEqual(state.turn,1)
        self.assertGreater(r["next_review_turn"],1)
    def test_wrong_answer_retries_soon(self):
        state = Progress(); q = state.next_question()
        r = state.answer(q.id,(q.correct+1)%len(q.options))
        self.assertFalse(r["correct"])
        self.assertEqual(r["next_review_turn"],2)
    def test_rejects_duplicate_or_out_of_order(self):
        state = Progress(); q = state.next_question()
        with self.assertRaises(ValueError): state.answer(q.id,100)
        state.answer(q.id,q.correct)
        with self.assertRaises(ValueError): state.answer(q.id,q.correct)
    def test_mastery_range(self):
        self.assertTrue(all(0 <= x <= 1 for x in Progress().skill_mastery().values()))

if __name__=="__main__": unittest.main()
