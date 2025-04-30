import subprocess

def run_test(test_name, inputs, expected_outputs):
    print(f"Running Test: {test_name}")
    
    try:
        input_str = '\n'.join(inputs) + '\n'

        process = subprocess.Popen(
            ['./game'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, _ = process.communicate(input=input_str, timeout=10)

        with open('test_log/scenario_test_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n=== {test_name} ===\n")
            f.write(output)
            f.write("\n----------------------\n")

        passed = all(expected.lower() in output.lower() for expected in expected_outputs)

        if passed:
            print("PASS")
        else:
            print("FAIL")
            for expected in expected_outputs:
                if expected.lower() not in output.lower():
                    print(f"Missing: {expected}")
        print("-" * 60)

    except subprocess.TimeoutExpired:
        process.kill()
        print(f"FAIL: {test_name} - Timed out")
        print("-" * 60)
    except Exception as e:
        print(f"Error in test '{test_name}': {e}")
        print("-" * 60)

# === SCENARIO  ===

def full_gameplay_scenario_fuel_win():
    run_test(
        test_name="Scenario 1: Collect Junk, Use Fuel Bonus, Die to Asteroid",
        inputs=[
            "Tester", "2",                 # Name + Medium Difficulty
            "W", "W", "D", "D",            # Move
            "H",                           # Status check
            "D", "D", "D", "D",            # Move to junk
            "F",                           # Fuel bonus
            "D", "D", "D", "D"             # Asteroid collision
        ],
        expected_outputs=[
            "WELCOME TO SPACEXPLORER",
            "You chose MEDIUM mode",
            "Ship Status", "Fuel:", "Score:", "Health:",
            "You collected space junk!",
            "You gained +5 fuel!",
            "Game Over", "collided with the asteroid"
        ]
    )

if __name__ == "__main__":
    full_gameplay_scenario_fuel_win()
