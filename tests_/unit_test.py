import subprocess
import time

def run_test(test_name, inputs, expected_outputs):
    print(f"Running Test: {test_name}")
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

        with open('test_log/unit_test_log.txt', 'a', encoding='utf-8') as f:
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
                    print(f"Missing expected output: {expected}")
        print("-" * 60)
    except Exception as e:
        print(f"Error in test '{test_name}': {e}")
        print("-" * 60)

def test_intro_display():
    run_test("Intro Display", ["TestUser", "2", "H"], ["WELCOME TO SPACEXPLORER"])

def test_invalid_key():
    run_test("Invalid Key Handling", ["TestUser", "2", "Z"], ["Invalid input"])

def test_system_check():
    run_test("System Check", ["TestUser", "2", "H"], ["Ship Status", "Fuel:", "Health:", "Score:"])

def test_boundary_hit():
    run_test("Boundary Check", ["TestUser", "2"] + ["A"] * 25, ["You hit the boundary! No movement made."])

def test_alien_simulated():
    run_test("Alien Encounter", ["TestUser", "2", "D", "S", "D", "S", "D"], ["An alien attacked you!", "health"])

if __name__ == "__main__":
    test_intro_display()
    test_invalid_key()
    test_system_check()
    test_boundary_hit()
    test_alien_simulated()
