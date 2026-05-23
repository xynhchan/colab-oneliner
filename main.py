import subprocess
import sys
import time
import os
from threading import Thread

# ====================== KONFIGURASI ======================
SCRIPT1 = "postparam.py"   # Ganti dengan nama file script kamu
SCRIPT2 = "getparam.py"
SCRIPT3 = "merge.py"

# Warna untuk membedakan output (optional)
COLORS = {
    "script1": "\033[91m",  # Merah
    "script2": "\033[92m",  # Hijau
    "script3": "\033[94m",  # Biru
    "reset": "\033[0m"
}

def run_script(script_name, color_key):
    """Menjalankan satu script dan menampilkan output dengan prefix"""
    try:
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"{COLORS[color_key]}[{script_name}] Started{ COLORS['reset']}")
        
        for line in process.stdout:
            line = line.strip()
            if line:
                print(f"{COLORS[color_key]}[{script_name}] {line}{COLORS['reset']}")
        
        process.wait()
        print(f"{COLORS[color_key]}[{script_name}] Finished (Exit Code: {process.returncode}){COLORS['reset']}")
        
    except FileNotFoundError:
        print(f"❌ File {script_name} tidak ditemukan!")
    except Exception as e:
        print(f"❌ Error menjalankan {script_name}: {e}")


def main():
    print("="*70)
    print("🚀 MULTI SCRIPT RUNNER")
    print("="*70)
    print(f"Menjalankan:\n1. {SCRIPT1}\n2. {SCRIPT2}\n3. {SCRIPT3}\n")


    # Jalankan 3 script secara paralel menggunakan Thread
    t1 = Thread(target=run_script, args=(SCRIPT1, "script1"), daemon=True)
    t2 = Thread(target=run_script, args=(SCRIPT2, "script2"), daemon=True)
    t3 = Thread(target=run_script, args=(SCRIPT3, "script3"), daemon=True)

    t1.start()
    t2.start()
    t3.start()

    try:
        while True:
            time.sleep(0.5)
            # Cek apakah semua thread sudah mati
            if not (t1.is_alive() or t2.is_alive() or t3.is_alive()):
                break
    except KeyboardInterrupt:
        print("\n\n⛔ Semua proses dihentikan oleh user.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\n✅ Program selesai.")


if __name__ == "__main__":
    main()
