import numpy as np

class Allocator:
    # ... (rest of the class code remains the same) ...
    def __init__(self, normalized_agents, total_amount):
        self.agents = normalized_agents
        self.total_amount = total_amount
        self.num_agents = len(self.agents)
        self.weightages = {
            "performance": 0.25,
            "net_achieved": 0.25,
            "active_clients": 0.2,
            "target_achieved": 0.2,
            "experience": 0.1
        }
        self.bonus_results = []
        
    def calculate_scores(self):
        """Calculates a weighted score for each agent."""
        if not self.agents:
            return 0
            
        total_score = 0
        for agent in self.agents:
            score = (
                agent["performance"] * self.weightages["performance"] +
                agent["net_achieved"] * self.weightages["net_achieved"] +
                agent["active_clients"] * self.weightages["active_clients"] +
                agent["target_achieved"] * self.weightages["target_achieved"] +
                agent["experience"] * self.weightages["experience"]
            )
            agent["score"] = score
            total_score += score
        return total_score

    def get_justification(self, score_percentile):
        """Returns a justification string based on the agent's score percentile."""
        if score_percentile > 70:
            return "Amazing performance, well deserving."
        elif score_percentile > 50:
            return "Good performance, score for improvement."
        else:
            return "Poor performance, no bonus."
            
    def allocate_bonus(self):
        """
        Distributes the total amount amongst agents based on scores.
        """
        if self.num_agents == 0:
            return []

        total_score = self.calculate_scores()
        
        # Calculate basic pay for all agents
        basic_pay_portion = self.total_amount * 0.5
        basic_pay = basic_pay_portion / self.num_agents
        
        # Determine performance bonus pool
        performance_bonus_pool = self.total_amount * 0.5

        # Get all scores for percentile calculation
        all_scores = [agent["score"] for agent in self.agents]
        if not all_scores:
            return []
            
        # Calculate the total score of all agents for proportional distribution
        total_agent_score = sum(all_scores)

        for agent in self.agents:
            # Calculate bonus before applying percentile multiplier
            # This is the "achieved bonus" for each agent
            if total_agent_score > 0:
                achieved_bonus = (agent["score"] / total_agent_score) * performance_bonus_pool
            else:
                achieved_bonus = 0

            # Calculate score percentile for the current agent
            score_percentile = np.mean(np.array(all_scores) < agent["score"]) * 100
            
            # Handle max score case
            if agent["score"] == np.max(all_scores):
                score_percentile = 100
            
            # Apply multiplier based on percentile rank
            if score_percentile > 70:
                multiplier = 1.0  # 100% of achieved bonus
                justification = "Amazing performance, well deserving."
            elif score_percentile > 30:
                multiplier = 0.6  # 60% of achieved bonus
                justification = "Good performance, score for improvement."
            else:
                multiplier = 0.3  # 30% of achieved bonus
                justification = "Poor performance, no bonus."

            final_performance_bonus = achieved_bonus * multiplier
            final_bonus = basic_pay + final_performance_bonus
            
            self.bonus_results.append({
                "agent_id": agent["id"],
                "agent_bonus": round(final_bonus, 2),
                "justification": justification
            })
        # Sort results by agent_bonus descending for test compatibility
        self.bonus_results.sort(key=lambda x: x["agent_bonus"], reverse=True)
        return self.bonus_results