import json

class Normalizer:
    """
    A class to handle the normalization of agent metrics.
    It performs max normalization on specified parameters.
    """
    def __init__(self, agents_data):
        self.agents = agents_data
        self.params = [
            "performance",
            "target_achieved",
            "active_clients",
            "experience"
        ]

    def _get_min_max(self, param):
        """Helper to get min and max values for a parameter."""
        values = [agent[param] for agent in self.agents]
        return max(values), min(values)

    def normalize_metrics(self):
        """
        1) Normalizes using max scaling an brings the whole range b/w 0 and 1.
        2) calculates and normalizes 'net_achieved'.
        """
        if not self.agents:
            return []

        # Step 1: Normalize all initial parameters
        normalized_agents = []
        for agent in self.agents:
            normalized_agent = {"id": agent["id"]}
            # Copy original fields needed for later calculations
            for field in ["target_achieved", "active_clients"]:
                normalized_agent[field] = agent[field]
            for param in self.params:
                max_val, min_val = self._get_min_max(param)
                if max_val == min_val:
                    normalized_agent[param] = 1
                else:
                    normalized_agent[param] = (agent[param] - min_val) / (max_val - min_val)
            normalized_agents.append(normalized_agent)
        
        # Step 2: Calculate 'net_achieved' from the normalized values
        for agent in normalized_agents:
            agent["net_achieved"] = (agent["target_achieved"] * agent["active_clients"])

        # Step 3: Normalize 'net_achieved' across all agents
        net_achieved_values = [agent["net_achieved"] for agent in normalized_agents]
        max_na,min_na =max(net_achieved_values),min(net_achieved_values)
        for agent in normalized_agents:
            if max_na==min_na:
               agent["net_achieved"]=1
            else:
                agent["net_achieved"] = (agent["net_achieved"]-min_na)/(max_na-min_na)
        
        return normalized_agents

if __name__ == '__main__':
    # Example usage for testing
    sample_data = [
        {"id": 101, "performance": 85, "target_achieved": 86, "active_clients": 50, "experience": 3},
        {"id": 102, "performance": 95, "target_achieved":84, "active_clients": 65, "experience": 5},
        {"id": 103, "performance": 70, "target_achieved": 78, "active_clients": 40, "experience": 2},
    ]
    normalizer = Normalizer(sample_data)
    normalized_agents = normalizer.normalize_metrics()
    print(json.dumps(normalized_agents, indent=2))