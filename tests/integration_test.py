import subprocess
import time

# Function to run the integration test
def run_integration_test(test_name, inputs, expected_outputs):
    print(f"Running Integration Test: {test_name}")
    try:
        # Start game.exe
        process = subprocess.Popen(
            [r'C:\Users\omarm\OneDrive\Desktop\Eva - Mini C Game\Game\SpaceXplorer\game.exe'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Feed the input step-by-step
        for line in inputs:
            process.stdin.write(line + '\n')
            process.stdin.flush()
            time.sleep(0.5)  # Allow some time for game to respond

        # Give some time then close
        time.sleep(2)
        process.terminate()

        # Collect output
        output, error = process.communicate(timeout=5)

        # Save to a log file for evidence
        with open("scenario_test_log.txt", "a", encoding="utf-8") as f:
            f.write(f"--- Integration Test: {test_name} ---\n{output}\n")

        # Validate expected output
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
        print(f"Integration Test '{test_name}' failed due to exception: {e}")
        print("-" * 60)

# Now define tests matching what your real program does now

def test_intro_and_map_display():
    run_integration_test(
        "Intro and Map Display Test",
        ["James"],  # Only name input needed
        [
            "WELCOME TO SPACEXPLORER",  # Check intro appeared
            "--- Space Map ---",         # Check map printed
            "P",                         # Check player placed
            "A"                          # Check asteroid placed
        ]
    )

# Run the integration tests
if __name__ == "__main__":
    test_intro_and_map_display()
