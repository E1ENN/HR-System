from hr_system_project.repository import CandidateRepository, Candidate
import unittest

class TestCandidateRepository(unittest.TestCase):

    def setUp(self):
        self.repository = CandidateRepository()
        self.repository.candidates = dict()


    def test_add_candidate(self):
        candidate = self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        self.assertEqual(len(self.repository.candidates), 1)
        self.assertEqual(candidate.full_name, "Иван Иванов")

    def test_find_by_name(self):
        self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        results = self.repository.find_by_name("Иван")
        self.assertTrue(any("Иван Иванов" in r for r in results))

    def test_find_by_id(self):
        candidate = self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        res = self.repository.find_by_id(1)
        self.assertEqual(res.full_name, "Иван Иванов")

    def test_filter_by_status(self):
        self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        filtered = self.repository.filter_by_status("NEW")
        self.assertTrue(any("Иван Иванов" in c for c in filtered))

    def test_update_candidate(self):
        candidate = self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        updated = self.repository.update_candidate("Пётр Петров", "40", "petr321@mail.com", "HIRED", candidate)
        self.assertEqual(updated.full_name, "Пётр Петров")
        self.assertEqual(updated.age, 40)
        self.assertEqual(updated.status, "HIRED")

    def test_delete_by_id(self):
        self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        self.repository.delete_by_id(1)
        self.assertEqual(len(self.repository.candidates), 0)

    def test_delete_by_full_name(self):
        self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        self.repository.delete_by_full_name("Иван Иванов")
        self.assertEqual(len(self.repository.candidates), 0)

    def test_incorrect_update_raises(self):
        candidate = self.repository.add_candidate("Иван Иванов", 30, "ivan123@mail.com", "NEW")
        with self.assertRaises(ValueError):
            self.repository.update_candidate("", "", "", "", candidate)

    def test_incorrect_status_filter_raises(self):
        with self.assertRaises(ValueError):
            self.repository.filter_by_status("INCORRECT_STATUS")

if __name__ == '__main__':
    unittest.main()