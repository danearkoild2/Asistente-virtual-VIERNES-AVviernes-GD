import asyncio
import http.server
import socketserver
import threading
import base64
import os
import sys
import json

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os_dir = _CURRENT_DIR
frames_dir = os.path.join(_CURRENT_DIR, "frames")
os.makedirs(frames_dir, exist_ok=True)

# Comprehensive high-fidelity pose library: (filename, custom_params_dict)
poses = {
    # ── Neutral & Relaxed States ──
    "idle": {
        "ParamMouthForm": 0.25, "ParamMouthOpenY": 0.0,
        "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0,
        "ParamEyeLSmile": 0.0, "ParamEyeRSmile": 0.0,
        "ParamCheek": 0.15, "ParamAngleX": 0.0, "ParamAngleY": 0.0, "ParamAngleZ": 0.0,
        "ParamEyeBallX": 0.0, "ParamEyeBallY": 0.0,
        "ParamBrowLY": 0.0, "ParamBrowRY": 0.0,
    },
    "idle_smile": {
        "ParamMouthForm": 0.70, "ParamMouthOpenY": 0.05,
        "ParamEyeLOpen": 0.92, "ParamEyeROpen": 0.92,
        "ParamEyeLSmile": 0.45, "ParamEyeRSmile": 0.45,
        "ParamCheek": 0.35, "ParamAngleX": 1.5, "ParamAngleY": 1.0, "ParamAngleZ": -1.0,
    },
    "happy_cheer": {
        "ParamMouthForm": 1.0, "ParamMouthOpenY": 0.30,
        "ParamEyeLOpen": 0.0, "ParamEyeROpen": 0.0,
        "ParamEyeLSmile": 1.0, "ParamEyeRSmile": 1.0,
        "ParamCheek": 0.65, "ParamAngleX": 0.0, "ParamAngleY": 3.0, "ParamAngleZ": 1.5,
        "ParamBrowLY": 0.4, "ParamBrowRY": 0.4,
        "Param29": 0.6, "Param31": 0.6,
    },

    # ── Expressive & Interactive States ──
    "curious": {
        "ParamAngleZ": -6.5, "ParamAngleX": 6.0, "ParamAngleY": 2.0,
        "ParamBrowLY": 0.55, "ParamBrowLAngle": 0.2, "ParamBrowRY": -0.1,
        "ParamEyeLOpen": 1.15, "ParamEyeROpen": 1.05,
        "ParamEyeBallX": 0.25, "ParamEyeBallY": 0.15,
        "ParamMouthForm": 0.35, "ParamMouthOpenY": 0.15,
        "ParamCheek": 0.25,
    },
    "thinking": {
        "ParamAngleX": 9.0, "ParamAngleY": 14.0, "ParamAngleZ": 5.5,
        "ParamEyeBallX": 0.55, "ParamEyeBallY": 0.70,
        "ParamBrowLAngle": -0.25, "ParamBrowRAngle": -0.25,
        "ParamBrowLY": 0.1, "ParamBrowRY": 0.1,
        "ParamMouthForm": -0.25, "ParamMouthOpenY": 0.0,
        "ParamCheek": 0.15,
    },
    "listening": {
        "ParamAngleY": -5.0, "ParamBodyAngleY": -3.5,
        "ParamEyeLOpen": 1.15, "ParamEyeROpen": 1.15,
        "ParamBrowLY": 0.30, "ParamBrowRY": 0.30,
        "ParamMouthForm": 0.30, "ParamMouthOpenY": 0.02,
        "ParamCheek": 0.25,
    },
    "surprised": {
        "ParamEyeLOpen": 1.25, "ParamEyeROpen": 1.25,
        "ParamMouthOpenY": 0.45, "ParamMouthForm": 0.10,
        "ParamBrowLY": 0.65, "ParamBrowRY": 0.65,
        "ParamAngleY": 3.0, "ParamCheek": 0.35,
        "Param29": 0.7, "Param31": 0.7,
    },
    "wink_left": {
        "ParamEyeLOpen": 0.0, "ParamEyeLSmile": 1.0,
        "ParamEyeROpen": 1.05, "ParamEyeRSmile": 0.25,
        "ParamMouthForm": 0.75, "ParamMouthOpenY": 0.08,
        "ParamCheek": 0.45, "ParamAngleZ": -3.0,
    },
    "wink_right": {
        "ParamEyeROpen": 0.0, "ParamEyeRSmile": 1.0,
        "ParamEyeLOpen": 1.05, "ParamEyeLSmile": 0.25,
        "ParamMouthForm": 0.75, "ParamMouthOpenY": 0.08,
        "ParamCheek": 0.45, "ParamAngleZ": 3.0,
    },
    "ear_perk": {
        "Param29": 0.85, "Param31": 0.85, "Param33": -0.5, "Param34": -0.5,
        "ParamEyeLOpen": 1.10, "ParamEyeROpen": 1.10,
        "ParamMouthForm": 0.45, "ParamMouthOpenY": 0.05,
        "ParamCheek": 0.30, "ParamAngleY": 2.5,
    },
    "sleep": {
        "ParamEyeLOpen": 0.0, "ParamEyeROpen": 0.0,
        "ParamEyeLSmile": 0.0, "ParamEyeRSmile": 0.0,
        "ParamAngleY": -7.0, "ParamMouthForm": 0.10, "ParamMouthOpenY": 0.0,
        "ParamCheek": 0.15,
    },

    # ── Gaze / Head Yaw & Pitch ──
    "look_left": {
        "ParamAngleX": -22.0, "ParamBodyAngleX": -9.0, "ParamAngleZ": 4.5,
        "ParamEyeBallX": -0.90, "ParamMouthForm": 0.30, "ParamMouthOpenY": 0.0,
    },
    "look_right": {
        "ParamAngleX": 22.0, "ParamBodyAngleX": 9.0, "ParamAngleZ": -4.5,
        "ParamEyeBallX": 0.90, "ParamMouthForm": 0.30, "ParamMouthOpenY": 0.0,
    },
    "look_up": {
        "ParamAngleY": 18.0, "ParamEyeBallY": 0.85,
        "ParamMouthForm": 0.30, "ParamMouthOpenY": 0.0,
    },
    "look_down": {
        "ParamAngleY": -16.0, "ParamEyeBallY": -0.85,
        "ParamEyeLOpen": 0.85, "ParamEyeROpen": 0.85,
        "ParamCheek": 0.40, "ParamMouthForm": 0.30, "ParamMouthOpenY": 0.0,
    },

    # ── Natural Blinking ──
    "blink": {
        "ParamEyeLOpen": 0.0, "ParamEyeROpen": 0.0,
        "ParamEyeLSmile": 0.0, "ParamEyeRSmile": 0.0,
    },
    "blink_half": {
        "ParamEyeLOpen": 0.45, "ParamEyeROpen": 0.45,
        "ParamEyeLSmile": 0.1, "ParamEyeRSmile": 0.1,
    },

    # ── Speech / Phoneme Mouth Visemes ──
    "mouth_1": {
        "ParamMouthOpenY": 0.32, "ParamMouthForm": 0.35,
        "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0,
        "ParamCheek": 0.25,
    },
    "mouth_2": {
        "ParamMouthOpenY": 0.68, "ParamMouthForm": 0.50,
        "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0,
        "ParamCheek": 0.30,
    },
    "mouth_3": {
        "ParamMouthOpenY": 1.15, "ParamMouthForm": 0.70,
        "ParamEyeLOpen": 1.05, "ParamEyeROpen": 1.05,
        "ParamBrowLY": 0.25, "ParamBrowRY": 0.25,
        "ParamCheek": 0.35,
    },
    "talk_smile": {
        "ParamMouthOpenY": 0.55, "ParamMouthForm": 0.95,
        "ParamEyeLOpen": 0.95, "ParamEyeROpen": 0.95,
        "ParamEyeLSmile": 0.40, "ParamEyeRSmile": 0.40,
        "ParamCheek": 0.45,
    },
    "talk_pensive": {
        "ParamMouthOpenY": 0.40, "ParamMouthForm": 0.0,
        "ParamEyeBallX": -0.35, "ParamEyeBallY": 0.30,
        "ParamAngleZ": 3.0, "ParamCheek": 0.20,
    },
    "smile": {
        "ParamMouthForm": 0.85, "ParamMouthOpenY": 0.12,
        "ParamEyeLSmile": 0.50, "ParamEyeRSmile": 0.50,
        "ParamCheek": 0.40,
    },

    # ── Advanced Actions & Emotions ──
    "dizzy": {
        "Param14": 1.0, "ParamAngleZ": 8.0, "ParamAngleY": -4.0,
        "ParamMouthForm": -0.25, "ParamMouthOpenY": 0.28,
        "ParamCheek": 0.55, "Param29": -0.4, "Param31": 0.4,
    },
    "cross_eyes": {
        "Param13": 1.0, "ParamMouthOpenY": 0.35, "ParamAngleZ": -5.0,
        "ParamBrowLY": 0.35, "ParamBrowRY": 0.35, "ParamCheek": 0.35,
    },
    "crying_tears": {
        "Param28": 1.0, "ParamBrowLY": -0.45, "ParamBrowRY": -0.45,
        "ParamBrowLAngle": 0.35, "ParamBrowRAngle": 0.35,
        "ParamEyeLOpen": 0.85, "ParamEyeROpen": 0.85,
        "ParamMouthForm": -0.45, "ParamMouthOpenY": 0.18,
        "ParamCheek": 0.70, "ParamAngleY": -6.0,
    },
    "blush_shy": {
        "ParamCheek": 0.95, "ParamEyeLSmile": 0.65, "ParamEyeRSmile": 0.65,
        "ParamEyeBallX": -0.55, "ParamEyeBallY": -0.35,
        "ParamAngleZ": -7.5, "ParamAngleY": -5.0, "ParamAngleX": -6.0,
        "ParamMouthForm": 0.45, "ParamMouthOpenY": 0.05,
    },
    "pout": {
        "ParamMouthForm": -0.85, "ParamMouthOpenY": 0.02,
        "ParamBrowLY": -0.38, "ParamBrowRY": -0.38,
        "ParamBrowLAngle": 0.38, "ParamBrowRAngle": 0.38,
        "ParamCheek": 0.70, "ParamAngleZ": 6.5, "ParamAngleX": -4.0,
    },
    "proud_smug": {
        "ParamEyeLSmile": 0.95, "ParamEyeRSmile": 0.95,
        "ParamEyeLOpen": 0.10, "ParamEyeROpen": 0.10,
        "ParamMouthForm": 0.95, "ParamMouthOpenY": 0.08,
        "ParamAngleY": 7.0, "ParamBrowLY": 0.45, "ParamBrowRY": 0.45,
        "ParamCheek": 0.50, "ParamBodyAngleY": 4.0,
    },
    "excited_sparkle": {
        "ParamEyeLOpen": 1.25, "ParamEyeROpen": 1.25,
        "ParamBrowLY": 0.55, "ParamBrowRY": 0.55,
        "ParamMouthForm": 1.0, "ParamMouthOpenY": 0.45,
        "ParamCheek": 0.75, "ParamAngleY": 4.0,
        "Param29": 0.90, "Param31": 0.90,
    },
    "greeting_wave": {
        "ParamAngleZ": -6.0, "ParamAngleX": 5.0,
        "ParamEyeLSmile": 0.65, "ParamEyeRSmile": 0.65,
        "ParamMouthForm": 0.85, "ParamMouthOpenY": 0.22,
        "ParamCheek": 0.45, "ParamBodyAngleX": 4.0,
    },
    "apology_bow": {
        "ParamAngleY": -16.0, "ParamBodyAngleY": -7.0,
        "ParamEyeLOpen": 0.40, "ParamEyeROpen": 0.40,
        "ParamBrowLY": -0.30, "ParamBrowRY": -0.30,
        "ParamMouthForm": -0.20, "ParamMouthOpenY": 0.05,
        "ParamCheek": 0.35,
    },
    "shocked_gasp": {
        "ParamEyeLOpen": 1.35, "ParamEyeROpen": 1.35,
        "ParamBrowLY": 0.75, "ParamBrowRY": 0.75,
        "ParamMouthOpenY": 0.75, "ParamMouthForm": -0.30,
        "ParamCheek": 0.15, "ParamAngleY": 4.0,
    },
    "sleepy_yawn": {
        "ParamEyeLOpen": 0.15, "ParamEyeROpen": 0.15,
        "ParamMouthOpenY": 0.85, "ParamMouthForm": 0.10,
        "ParamCheek": 0.35, "ParamAngleZ": 5.0,
        "Param29": -0.60, "Param31": -0.60,
    },
    "giggle": {
        "ParamEyeLOpen": 0.0, "ParamEyeROpen": 0.0,
        "ParamEyeLSmile": 1.0, "ParamEyeRSmile": 1.0,
        "ParamMouthForm": 0.92, "ParamMouthOpenY": 0.28,
        "ParamCheek": 0.85, "ParamAngleZ": 6.5, "ParamAngleY": 3.0,
    },
    "nod_yes": {
        "ParamAngleY": 8.0, "ParamBodyAngleY": 5.0,
        "ParamEyeLSmile": 0.60, "ParamEyeRSmile": 0.60,
        "ParamMouthForm": 0.75, "ParamCheek": 0.35,
    },
    "shake_no": {
        "ParamAngleX": -16.0, "ParamAngleZ": 5.5,
        "ParamBrowLY": -0.25, "ParamBrowRY": -0.25,
        "ParamMouthForm": -0.35, "ParamCheek": 0.20,
    },
    "listen_attentive": {
        "ParamAngleY": -6.5, "ParamAngleX": 4.5, "ParamAngleZ": -4.0,
        "ParamEyeLOpen": 1.20, "ParamEyeROpen": 1.20,
        "Param29": 0.95, "Param31": 0.95,
        "ParamBrowLY": 0.35, "ParamBrowRY": 0.35, "ParamCheek": 0.25,
    }
}

async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        page = await browser.new_page(viewport={"width": 800, "height": 1350})
        page.on("console", lambda msg: print(f"[BROWSER] {msg.text.encode('ascii', 'replace').decode()}", flush=True))
        page.on("pageerror", lambda err: print(f"[BROWSER ERROR] {str(err).encode('ascii', 'replace').decode()}", flush=True))
        print("Navigating to avatar page...", flush=True)
        await page.goto("http://127.0.0.1:8877/avatar.html", wait_until="domcontentloaded")
        print("Waiting for Live2D model to initialize...", flush=True)
        await page.wait_for_function("() => window.__MODEL_READY__ === true", timeout=90000)
        print("Live2D model ready in browser!", flush=True)
        await asyncio.sleep(1.0)

        for name, params in poses.items():
            out_file = os.path.join(frames_dir, f"{name}.png")
            if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
                print(f"Skipping existing {name}.png")
                continue

            params_json = json.dumps(params)
            await page.evaluate(f"""() => {{
                window.resetParams();
                window.setCustomParams({params_json});
            }}""")
            await asyncio.sleep(0.18)

            data_url = await page.evaluate("""() => {
                const c = document.getElementById('canvas');
                return c.toDataURL('image/png');
            }""")

            header, encoded = data_url.split(",", 1)
            data = base64.b64decode(encoded)
            with open(out_file, "wb") as f:
                f.write(data)
            print(f"Generated {name}.png ({len(data)} bytes)")

        await browser.close()

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    handler = lambda *args: http.server.SimpleHTTPRequestHandler(*args, directory=os_dir)
    server = ThreadingHTTPServer(("127.0.0.1", 8877), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(run())
    finally:
        server.shutdown()
    print("All professional pose frames generated successfully!")
