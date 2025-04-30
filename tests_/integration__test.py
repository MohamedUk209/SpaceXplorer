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

        for line in inputs:
            try:
                process.stdin.write(line + '\n')
                process.stdin.flush()
                time.sleep(0.2)
            except:
                break

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
        inputs=["Tester", "2", "W", "A", "D", "S"],
        expected_outputs=["WELCOME TO SPACEXPLORER", "--- Space Map ---", "Fuel:", "Score:", "Health:"]
    )

def test_status_and_movement_together():
    run_test(
        test_name="System Status + Movement Integration",
        inputs=["Tester", "2", "W", "H", "D", "H"],
        expected_outputs=["Ship Status", "Fuel:", "Score:", "Health:", "--- Space Map ---"]
    )

def test_junk_collection_and_score():
    run_test(
        test_name="Junk Collection and Score Integration",
        inputs=["Tester", "2", "D", "D", "D", "D", "F"],
        expected_outputs=["You collected space junk", "+5 fuel", "Score:"]
    )

def test_alien_attack_and_health_drop():
    run_test(
        test_name="Alien Attack and Health Drop",
        inputs=["Tester", "2", "D", "D"],
        expected_outputs=["An alien attacked you!", "-5 health", "Health:"]
    )

def test_fuel_exhaustion_and_termination():
    run_test(
        test_name="Fuel Depletion and Game Over",
        inputs=["Tester", "2"] + ["W", "D", "D", "D", "A", "A", "A", "W", "W","D"],
        expected_outputs=["Game Over!", "You ran out of fuel."]
    )

def test_boundary_detection_with_status_check():
    run_test(
        test_name="Boundary and Status After Block",
        inputs=["Tester", "2"] + ["A"] * 10 + ["H"],
        expected_outputs=["You hit the boundary! No movement made.", "Ship Status", "Fuel:", "Score:"]
    )

def test_health_zero_game_end():
    run_test(
        test_name="Alien Collision and Death",
        inputs=["Tester", "2", "D", "D", "D", "D", "D", "D", "D", "D"],  # Let alien reach player
        expected_outputs=["Game Over! You were killed by an alien."]
    )

if __name__ == "__main__":
    test_movement_and_map_update()
    test_status_and_movement_together()
    test_junk_collection_and_score()
    test_alien_attack_and_health_drop()
    test_fuel_exhaustion_and_termination()
    test_boundary_detection_with_status_check()
    test_health_zero_game_end()
