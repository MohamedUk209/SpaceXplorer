import subprocess
import time

def run_test(test_name, inputs, expected_outputs, log_file):
    print(f"Running {test_name}...")
    try:
        process = subprocess.Popen(
            ['./game'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in inputs:
            process.stdin.write(line + '\n')
            process.stdin.flush()
            time.sleep(0.2)

        time.sleep(2)
        process.terminate()
        output, _ = process.communicate()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n--- {test_name} ---\n")
            f.write(output)
            f.write("\n----------------------\n")

        passed = all(expected.lower() in output.lower() for expected in expected_outputs)
        if passed:
            print("PASS")
        else:
            print("FAIL")
            for expected in expected_outputs:
                if expected.lower() not in output.lower():
                    print(f"Missing expected output: {expected}")
        print("-" * 50)

    except Exception as e:
        print(f"Error in {test_name}: {e}")
        print("-" * 50)

# INTEGRATION TESTS FOR FULL INTERACTION FLOWS
def test_intro_and_map():
    run_test(
        "Intro and Map Display",
        ["Ali", "2", "H"],
        ["WELCOME TO SPACEXPLORER", "--- Space Map ---", "P", "A"],
        "test_log/integration_test_log.txt"
    )

def test_movement_and_fuel_drop():
    run_test(
        "Movement + Fuel Reduction",
        ["Ali", "2", "D", "H"],
        ["Fuel:"],
        "integration_test_log.txt"
    )

def test_alien_encounter():
    run_test(
        "Alien Encounter Simulation",
        ["Ali", "2", "D", "S", "D", "S", "D", "S", "D", "S", "H"],
        ["An alien attacked you!", "health"],
        "integration_test_log.txt"
    )

def test_junk_collection_effects():
    run_test(
        "Junk Collection + Action",
        ["Ali", "2", "D", "D", "S", "S", "D", "S", "F"],
        ["You collected space junk!", "+5 fuel", "+2 health", "Invalid choice"],
        "integration_test_log.txt"
    )

if __name__ == "__main__":
    test_intro_and_map()
    test_movement_and_fuel_drop()
    test_alien_encounter()
    test_junk_collection_effects()
