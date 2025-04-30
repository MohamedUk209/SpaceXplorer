import subprocess
import threading
import time

def run_test(test_name, inputs, expected_outputs):
    print(f"Running Test: {test_name}")
    output_collector = []

    def reader_thread_func(pipe, collector):
        while True:
            line = pipe.readline()
            if not line:
                break
            collector.append(line)

    try:
        process = subprocess.Popen(
            ['./game'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        reader_thread = threading.Thread(target=reader_thread_func, args=(process.stdout, output_collector))
        reader_thread.start()

        # Feed input line by line
        for line in inputs:
            process.stdin.write(line + '\n')
            process.stdin.flush()
            time.sleep(0.2)  # delay helps simulate real typing

        # Let it print output for a few seconds
        time.sleep(3)
        process.kill()

        # Combine collected output
        full_output = ''.join(output_collector)

        with open('test_log/unit_test_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n=== {test_name} ===\n")
            f.write(full_output)
            f.write("\n----------------------\n")

        passed = all(expected.lower() in full_output.lower() for expected in expected_outputs)
        if passed:
            print("PASS")
        else:
            print("FAIL")
            for expected in expected_outputs:
                if expected.lower() not in full_output.lower():
                    print(f"Missing: {expected}")
        print("-" * 60)

    except Exception as e:
        print(f"Error in test '{test_name}': {e}")
        print("-" * 60)

# === Test Cases ===

def test_intro_display():
    run_test("Intro Display", ["Tester"], ["WELCOME TO SPACEXPLORER"])

def test_invalid_key():
    run_test("Invalid Input", ["Tester", "Z", "W", "W", "W"], ["Invalid input"])

def test_status_check():
    run_test("System Status", ["Tester", "H"], ["Ship Status", "Fuel:", "Score:", "Health:"])

def test_boundary_block():
    run_test("Boundary Block", ["Tester"] + ["A"] * 10, ["You hit the boundary"])

if __name__ == "__main__":
    test_intro_display()
    test_invalid_key()
    test_status_check()
    test_boundary_block()
