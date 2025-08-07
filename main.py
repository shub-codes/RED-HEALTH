import argparse
import json
from src.normaliser import Normalizer
from src.allocator import Allocator

def main():
    """
    Main function to run the bonus allocation script.
    """
    parser = argparse.ArgumentParser(description="Allocate bonus funds to sales agents.")
    parser.add_argument("total_amount", type=float, help="Total bonus amount available.")
    parser.add_argument("agents_file", type=str, help="Path to the JSON file with agent data.")
    
    args = parser.parse_args()
    
    try:
        with open(args.agents_file, 'r') as f:
            agents_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{args.agents_file}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{args.agents_file}' is not a valid JSON file.")
        return

    if not isinstance(agents_data, list):
        print("Error: JSON data must be a list of agents.")
        return

    # Normalize agent data
    normalizer = Normalizer(agents_data)
    normalized_agents = normalizer.normalize_metrics()
    
    # Allocate bonus based on normalized data
    allocator = Allocator(normalized_agents, args.total_amount)
    bonus_allocations = allocator.allocate_bonus()
    
    # Print the final results
    print(json.dumps(bonus_allocations, indent=2))

if __name__ == "__main__":
    main()