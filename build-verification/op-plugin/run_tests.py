import os
import subprocess
import glob
import time

os.environ["ASCEND_HOME"] = "/usr/local/Ascend"

test_dir = "/opt/test-run/test/test_base_ops"
test_files = sorted(glob.glob(os.path.join(test_dir, "test_*.py")))[:20]

results = []
for tf in test_files:
    name = os.path.basename(tf).replace(".py", "")
    start = time.time()
    try:
        r = subprocess.run(["python3", tf], capture_output=True, text=True, timeout=120)
        elapsed = round(time.time() - start, 1)
        status = "PASS" if r.returncode == 0 else "FAIL"
    except subprocess.TimeoutExpired:
        elapsed = 120.0
        status = "TIMEOUT"
    results.append((name, status, elapsed))
    print("%s: %s (%.1fs)" % (status, name, elapsed))

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
timeout = sum(1 for _, s, _ in results if s == "TIMEOUT")
total = len(results)
total_time = sum(t for _, _, t in results)
print("\nSummary: %d tests, %d passed, %d failed, %d timeout, %.0fs total" % (total, passed, failed, timeout, total_time))
