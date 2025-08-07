import json
import unittest
from src.normaliser import Normalizer
from src.allocator import Allocator

# You'll need to define your test JSON data here or load it from files
# For simplicity, we'll embed the data directly.

standard_case_data = [
    {"id": 101, "performance": 85, "target_achieved": 75, "active_clients": 50, "experience": 3},
    {"id": 102, "performance": 95, "target_achieved": 35, "active_clients": 65, "experience": 5},
    {"id": 103, "performance": 70, "target_achieved": 73, "active_clients": 40, "experience": 2},
    {"id": 104, "performance": 90, "target_achieved": 56, "active_clients": 60, "experience": 4}
]
standard_case_amount = 10000

edge_case_data = [
    {"id": 201, "performance": 100, "target_achieved": 100, "active_clients": 1, "experience": 1}
]
edge_case_amount = 5000

same_scores_data = [
    {"id": 301, "performance": 80, "target_achieved": 100, "active_clients": 30, "experience": 2},
    {"id": 302, "performance": 80, "target_achieved": 100, "active_clients": 30, "experience": 2},
    {"id": 303, "performance": 80, "target_achieved": 100, "active_clients": 30, "experience": 2}
]
same_scores_amount = 6000

class TestAllocator(unittest.TestCase):
    
    def test_standard_case(self):
        normalizer = Normalizer(standard_case_data)
        normalized_agents = normalizer.normalize_metrics()
        allocator = Allocator(normalized_agents, standard_case_amount)
        results = allocator.allocate_bonus()
        
        # basic assertions
        self.assertEqual(results[0]['agent_id'], 104)
        self.assertGreater(results[0]['agent_bonus'], 2500)
        self.assertEqual(results[-1]['justification'], "Poor performance, no bonus.")

    def test_edge_case(self):
        normalizer = Normalizer(edge_case_data)
        normalized_agents = normalizer.normalize_metrics()
        allocator = Allocator(normalized_agents, edge_case_amount)
        results = allocator.allocate_bonus()

        # Assertion that the single agent receives the full amount
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['agent_bonus'], 5000)
        self.assertEqual(results[0]['justification'], "Amazing performance, well deserving.")

    def test_same_scores_case(self):
        normalizer = Normalizer(same_scores_data)
        normalized_agents = normalizer.normalize_metrics()
        allocator = Allocator(normalized_agents, same_scores_amount)
        results = allocator.allocate_bonus()

        # Assertion that the bonuses are equal and sum to the total amount
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['agent_bonus'], 2000.0)
        self.assertEqual(results[1]['agent_bonus'], 2000.0)
        self.assertEqual(results[2]['agent_bonus'], 2000.0)
        self.assertEqual(sum(r['agent_bonus'] for r in results), 6000.0)
        self.assertTrue(all(r['justification'] == "Amazing performance, well deserving." for r in results))

if __name__ == '__main__':
    unittest.main()