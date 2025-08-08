# Agent Bonus Allocator

This is a CLI-based Python script that allocates a total bonus amount among a group of sales agents. The distribution is based on a scoring system that evaluates each agent's performance across multiple metrics.

## Creator Information
    Name: Shubham Mundhra
    NIT Jamspedpur
    Contact- 8700104865
    Email- 2023pgcsca111@nitjsr.ac.in

## Features

- **Modular Design:** The project is split into three main modules: `Normalizer`, `Allocator`, and `Main` for clear separation of concerns.
    ├── src/
    │   ├── allocator.py
    │   └── normalizer.py
    ├── main.py
    ├── agents.json
    └── README.md
- **Min-Max Normalization:** All raw agent metrics are normalized to a 0-1 scale before scoring.
- **Weighted Scoring:** A composite score is calculated using pre-defined weightages for each metric.
    1. Performance(w=0.25) is highest metric with defined legibility
    2. Addition of a new parameter Net_achieved(w= 0.25)=target_achieved*active clients to balance the combined effect of these two factors.
    3. target achived and active clients have been given same weightage
    4. Seniority, though holding due consideration, gets the lowest weightage of 0.1. It has not been apped to account for fact that constant gain in seniority should be rewarded as loyalty
- **Two-Tier Bonus System:**
    -**Basic Pay**-
    1. A basic pay(50 % of total) is distributed equally among all agents. It ensures certain payout irrespective of parameters
    -**Bonus Distribution**-
    1. Bonus is calculated as multiplier*(agent_score)/(total score of all agents)
    2. multiplier= 1 for top 70 percentile, 0.6 for 30-70 percentile and 0.3 for botton 30 percentile.
- **Justification:** Each bonus allocation includes a justification based on the agent's percentile rank.
-** Tester**- it contains 3 test cases 
    1. general case- varied parameters
    2. Edge case- single agent
    3. All agents same: everyagent has same parameter

## Assumptions and Thoughts
    1. Performance and net_target_achived are most credible signals of agents prowess, skils and contribution.Hence hold highest weightage
    2.  net_target-achieved is added to account for fact that high targetAchieved and low clients and vice versa can give a deceptive picture.
    3. Each agent should get a bascic pay as salary. Its just ethical.
    4. Percentile based multiplier serves two purpose.
        a. It ensures that each agent is motivated to improve performance in competitive spirit
        b. multiplier accounts for fact that even if a agent lies in bottom percentiles, their performance may not be poor as per say. just poor in comparison.So they get some bonus nonetheless
    5. Justification are also ditributed along the percentile splits



    

## How to Run

1.  Make sure you have Python installed.
2.  Save the Python files (`normalizer.py`, `allocator.py`) in a directory named `src`.
3.  Create a JSON file (e.g., `agents.json`) with your agent data.
4. Keep the main file outside

**Command:**
To run the script, use the following command from the root directory, replacing `<total_amount>` with the available funds and `<agents_file.json>` with your input file.
example 'python main.py 30000 agents.json'

```bash
python -m main.py <total_amount> <agents_file.json>