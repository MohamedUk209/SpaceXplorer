import subprocess
import time

def run_scenario(name, steps, expected_outputs):
    print(f"Running Scenario: {name}")
    try:
        process = subprocess.Popen(
            ['./game'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for s in steps:
            process.stdin.write(s + '\n')
            process.stdin.flush()
            time.sleep(0.3)
        time.sleep(2)
        process.terminate()
        output, _ = process.communicate()

        with open('test_log/scenario_test_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n=== Scenario: {name} ===\n")
            f.write(output)
            f.write("\n----------------------\n")

        passed = all(exp.lower() in output.lower() for exp in expected_outputs)
        print("PASS" if passed else "FAIL")
        if not passed:
            for exp in expected_outputs:
                if exp.lower() not in output.lower():
                    print(f"Missing: {exp}")
        print("-" * 60)
    except Exception as e:
        print(f"Scenario failed: {e}")

def full_journey():
    run_scenario(
        "Full Gameplay Scenario",
        ["PlayerOne", "2", "D", "S", "H", "A", "W", "H"],
        ["WELCOME TO SPACEXPLORER", "--- Space Map ---", "Fuel:", "Score:", "Health:"]
    )

if __name__ == "__main__":
    full_journey()
