"""
Ultra-fast, lightweight Screen Recorder for Heru's Windows Desktop using FFmpeg.
Runs with minimal CPU overhead (ultrafast preset) to capture screen sessions without lag.
"""

import sys
import os
import subprocess
import signal
import time

RECORD_PID_FILE = r"d:\SecondBrain\00_system\recorder.pid"
OUTPUT_DIR = r"d:\SecondBrain\01_knowledge\resources\screen_recordings"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def start_recording(output_filename=None):
    if os.path.exists(RECORD_PID_FILE):
        print("[SCREEN RECORDER] Perekaman sudah berjalan!")
        return

    if not output_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = f"screen_rec_{timestamp}.mp4"
    elif not output_filename.endswith(".mp4"):
        output_filename += ".mp4"

    out_path = os.path.join(OUTPUT_DIR, output_filename)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "gdigrab",
        "-framerate", "30",
        "-i", "desktop",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-crf", "26",
        "-pix_fmt", "yuv420p",
        out_path
    ]

    # Run in background without showing console window
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    with open(RECORD_PID_FILE, "w", encoding="utf-8") as f:
        f.write(f"{proc.pid}:{out_path}")

    print(f"[SCREEN RECORDER] Perekaman dimulai (PID: {proc.pid})")
    print(f"[OUTPUT] File tersimpan ke: {out_path}")

def stop_recording():
    if not os.path.exists(RECORD_PID_FILE):
        print("[SCREEN RECORDER] Tidak ada rekaman yang sedang aktif.")
        return

    with open(RECORD_PID_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    pid_str, out_path = content.split(":", 1)
    pid = int(pid_str)

    try:
        # Gracefully send 'q' to ffmpeg to finish mp4 container properly
        subprocess.run(["taskkill", "/PID", str(pid)], capture_output=True)
        time.sleep(1)
    except Exception as e:
        print(f"[WARN] Error stopping process: {e}")

    if os.path.exists(RECORD_PID_FILE):
        os.remove(RECORD_PID_FILE)

    print(f"[SCREEN RECORDER] Perekaman selesai!")
    print(f"[SAVED] File siap ditonton di: {out_path}")

def record_duration(seconds=10, filename=None):
    start_recording(filename)
    print(f"[RECORDING] Merekam selama {seconds} detik...")
    time.sleep(seconds)
    stop_recording()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan:")
        print("  python screen_recorder.py start [nama_file]")
        print("  python screen_recorder.py stop")
        print("  python screen_recorder.py record <durasi_detik> [nama_file]")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "start":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        start_recording(name)
    elif action == "stop":
        stop_recording()
    elif action == "record":
        dur = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        name = sys.argv[3] if len(sys.argv) > 3 else None
        record_duration(dur, name)
