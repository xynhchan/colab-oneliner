#!/usr/bin/env python3
import time
import os
from datetime import datetime
from pathlib import Path

# ====================== PATH CONFIG ======================
BASE_DIR = Path(__file__).parent.parent

# File paths (semua di parent folder)
file_path1 = BASE_DIR / "post_params.txt"   # File pertama
file_path2 = BASE_DIR / "get_params.txt"    # File kedua
merged_file = BASE_DIR / "dua.txt"          # File hasil gabungan

def tail_and_merge(file1, file2, output_file, interval=0.3):
    """
    Monitor 2 file secara real-time dan satukan isinya
    """
    pos1 = 0
    pos2 = 0
   
    print(f"🚀 Mulai monitoring merge...")
    print(f"   File 1 : {file1}")
    print(f"   File 2 : {file2}")
    print(f"   Output : {output_file}")
    print("-" * 70)
   
    with open(output_file, 'a', encoding='utf-8') as out:
        while True:
            updated = False
           
            # Cek File 1 (post_params.txt)
            if os.path.exists(file1):
                try:
                    with open(file1, 'r', encoding='utf-8') as f1:
                        f1.seek(pos1)
                        new_content1 = f1.read()
                        if new_content1:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            out.write(f"\n--- [POST PARAMS] {timestamp} ---\n")
                            out.write(new_content1)
                            out.flush()
                            pos1 = f1.tell()
                            updated = True
                            print(f"📌 [POST] {len(new_content1.strip())} karakter ditambahkan")
                except Exception as e:
                    print(f"⚠️ Error membaca File 1: {e}")
           
            # Cek File 2 (get_params.txt)
            if os.path.exists(file2):
                try:
                    with open(file2, 'r', encoding='utf-8') as f2:
                        f2.seek(pos2)
                        new_content2 = f2.read()
                        if new_content2:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            out.write(f"\n--- [GET PARAMS] {timestamp} ---\n")
                            out.write(new_content2)
                            out.flush()
                            pos2 = f2.tell()
                            updated = True
                            print(f"📌 [GET]  {len(new_content2.strip())} karakter ditambahkan")
                except Exception as e:
                    print(f"⚠️ Error membaca File 2: {e}")
           
            if updated:
                print(f"✅ Merge berhasil | {datetime.now().strftime('%H:%M:%S')}")
           
            time.sleep(interval)


# ================== PENGGUNAAN ==================
if __name__ == "__main__":
    try:
        # Cek apakah file input ada
        if not file_path1.exists() and not file_path2.exists():
            print(f"❌ Error: Tidak ada file yang ditemukan di {BASE_DIR}")
            print("Pastikan post_params.txt dan/atau get_params.txt ada di folder di atas.")
        else:
            tail_and_merge(file_path1, file_path2, merged_file, interval=0.3)
            
    except KeyboardInterrupt:
        print("\n\n⛔ Monitoring dihentikan oleh user.")
    except Exception as e:
        print(f"❌ Error: {e}")
