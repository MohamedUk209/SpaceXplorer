import subprocess
import threading
import time
import os

os.makedirs("test_log", exist_ok=True)

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
            except Exception:
                break  # stdin likely closed, game ended

        time.sleep(3)
        process.kill()
        reader_thread.join()

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

# === Unit Test Cases ===

def test_intro_and_difficulty():
    run_test(
        "Intro + Difficulty Selection",
        ["Tester", "3", "H"],
        ["WELCOME TO SPACEXPLORER", "You chose HARD mode", "Fuel: 20", "Score to win: 7"]
    )

def test_status_panel():
    run_test(
        "System Status Panel",
        ["Tester", "2", "H"],
        ["Ship Status", "Fuel:", "Score:", "Health:"]
    )

def test_invalid_key_handling():
    run_test(
        "Invalid Key Handling",
        ["Tester", "2", "Z"],
        ["Invalid input"]
    )

def test_boundary_enforcement():
    run_test(
        "Boundary Movement Block",
        ["Tester", "2"] + ["A"] * 20,
        ["You hit the boundary"]
    )

def test_alien_attack():
    run_test(
        "Alien Attack",
        ["Tester", "2"] + ["W", "D"] * 6,
        ["An alien attacked you!", "-5 health!"]
    )

def test_fuel_depletion():
    run_test(
        "Fuel Exhaustion",
        ["Tester", "2"] + ["W"] * 40,
        ["Game Over!", "You ran out of fuel."]
    )

def test_asteroid_collision():
    run_test(
        "Asteroid Collision",
        ["Tester", "2"] + ["D"] * 20,
        ["Game Over!", "You collided with the asteroid!"]
    )

if __name__ == "__main__":
    test_intro_and_difficulty()
    test_status_panel()
    test_invalid_key_handling()
    test_boundary_enforcement()
    test_alien_attack()
    test_fuel_depletion()
    test_asteroid_collision()
