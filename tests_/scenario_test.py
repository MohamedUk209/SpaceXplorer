import subprocess

def run_test(test_name, inputs, expected_outputs):
    print(f"Running Test: {test_name}")
    
    try:
        # Combine all input into a single string with newlines
        input_str = '\n'.join(inputs) + '\n'

        # Launch the game and send all input at once
        process = subprocess.Popen(
            ['./game'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send all input, wait up to 10 seconds
        output, _ = process.communicate(input=input_str, timeout=10)

        # Save output to log
        with open('test_log/scenario_test_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n=== {test_name} ===\n")
            f.write(output)
            f.write("\n----------------------\n")

        # Check expected outputs
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

# === SCENARIO TEST ===

def full_gameplay_scenario():
    run_test(
        test_name="Full Gameplay Scenario (Movement, Status, Junk, Collision)",
        inputs=[
            "Tester",
            "W", "W", "D", "D",
            "H",
            "D", "D", "D", "D",
            "F",
            "D", "D", "D", "D"
        ],
        expected_outputs=[
            "WELCOME TO SPACEXPLORER",
            "Ship Status",
            "Fuel:",
            "Score:",
            "Health:",
            "You collected space junk!",
            "You gained +5 fuel!",
            "Game Over",
            "collided with the asteroid"
        ]
    )

if __name__ == "__main__":
    full_gameplay_scenario()
