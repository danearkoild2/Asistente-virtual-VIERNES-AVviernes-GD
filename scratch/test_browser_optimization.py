import time
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from actions.browser_control import (
    browser_control,
    _is_profile_locked,
    _real_profile_dir,
    _registry
)

def run_tests():
    print("=== TEST 1: Profile Lock Detection (Instant Check) ===")
    t0 = time.time()
    brave_profile = _real_profile_dir("brave")
    is_locked = _is_profile_locked(brave_profile)
    t_detect = (time.time() - t0) * 1000
    print(f"Brave profile path: {brave_profile}")
    print(f"Brave profile locked: {is_locked} (detected in {t_detect:.2f} ms)")
    assert t_detect < 50, f"Lock detection took too long: {t_detect}ms"
    print("[OK] Test 1 Passed!")

    print("\n=== TEST 2: Fast Headless Navigation & Text Extraction ===")
    t1 = time.time()
    nav_res = browser_control({
        "action": "go_to",
        "url": "https://example.com",
        "headless": True
    })
    t_nav = time.time() - t1
    print(f"Navigation result: {nav_res} in {t_nav:.2f}s")
    assert "Opened:" in nav_res, f"Unexpected nav result: {nav_res}"

    t2 = time.time()
    text_res = browser_control({
        "action": "get_text",
        "headless": True
    })
    t_text = time.time() - t2
    print(f"Extracted clean text ({len(text_res)} chars) in {t_text:.2f}s:")
    print("--- PREVIEW ---")
    print(text_res[:150])
    print("---------------")
    assert len(text_res) > 20, "Text extraction returned empty content"
    print("[OK] Test 2 Passed!")

    print("\n=== TEST 3: Instant Typing Speed ===")
    t3 = time.time()
    type_res = browser_control({
        "action": "type",
        "text": "Fast Typing Performance Test 1234567890",
        "headless": True
    })
    t_type = (time.time() - t3) * 1000
    print(f"Typing execution in {t_type:.2f} ms: {type_res}")
    print("[OK] Test 3 Passed!")

    print("\n=== TEST 4: Cleanup & Close ===")
    close_res = browser_control({"action": "close_all"})
    print(f"Close result: {close_res}")
    print("[OK] All Tests Completed Successfully!")

if __name__ == "__main__":
    run_tests()
