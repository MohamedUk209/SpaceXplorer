import subprocess
import threading
import time

def run_test(test_name, inputs, expected_outputs):
    print(f"Running Test: {test_name}")
    output_collector = []

    def reader_thread_func(pipe, collector):
        try:
            for line in iter(pipe.readline, ''):
                collector.append(line)
        except Exception:
            pass

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

        # Send each line slowly
        for line in inputs:
            process.stdin.write(line + '\n')
            process.stdin.flush()
            time.sleep(0.2)

        # Wait extra time to collect stdout before killing
        time.sleep(3)
        process.kill()
        reader_thread.join()

        full_output = ''.join(output_collector)

        with open('test_log/integration_test_log.txt', 'a', encoding='utf-8') as f:
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

# === INTEGRATION TESTS ===

def test_movement_and_map_update():
    run_test(
        test_name="Movement and Map Update Integration",
        inputs=["Tester", "W", "A", "D", "S"],
        expected_outputs=[
            "WELCOME TO SPACEXPLORER",
            "--- Space Map ---",
            "Fuel:",
            "Score:",
            "Health:"
        ]
    )

def test_status_and_movement_together():
    run_test(
        test_name="System Status + Movement Integration",
        inputs=["Tester", "W", "H", "D", "H"],
        expected_outputs=[
            "Ship Status",
            "Fuel:",
            "Score:",
            "Health:",
            "--- Space Map ---"
        ]
    )

def test_junk_collection_and_score():
    run_test(
        test_name="Junk Collection and Score Integration",
        inputs=["Tester", "D", "D", "D", "D", "F"],
        expected_outputs=[
            "You collected space junk",
            "+5 fuel",
            "Score:"
        ]
    )

if __name__ == "__main__":
    test_movement_and_map_update()
    test_status_and_movement_together()
    test_junk_collection_and_score()
