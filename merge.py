#!/usr/bin/env python3
import time
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

file_path1 = BASE_DIR / "post_params.txt"
file_path2 = BASE_DIR / "get_params.txt"
merged_file = BASE_DIR / "dua.txt"

def tail_and_merge(file1, file2, output_file, interval=0.3):
    pos1 = 0
    pos2 = 0
  
    print("🚀 Mulai monitoring merge...")
    print(f" File 1 : {file1}")
    print(f" File 2 : {file2}")
    print(f" Output : {output_file}")
    print("-" * 70)
  
    with open(output_file, 'a', encoding='utf-8') as out:
        while True:
            updated = False
          
            if os.path.exists(file1):
                try:
                    with open(file1, 'r', encoding='utf-8') as f1:
                        f1.seek(pos1)
                        new_content1 = f1.read()
                        if new_content1:
                            out.write(new_content1)
                            out.flush()
                            pos1 = f1.tell()
                            updated = True
                            print(f"📌 [POST] {len(new_content1.strip())} karakter ditambahkan")
                except:
                    pass
          
            if os.path.exists(file2):
                try:
                    with open(file2, 'r', encoding='utf-8') as f2:
                        f2.seek(pos2)
                        new_content2 = f2.read()
                        if new_content2:
                            out.write(new_content2)
                            out.flush()
                            pos2 = f2.tell()
                            updated = True
                            print(f"📌 [GET] {len(new_content2.strip())} karakter ditambahkan")
                except:
                    pass
          
            if updated:
                print(f"✅ Merge berhasil | {datetime.now().strftime('%H:%M:%S')}")
          
            time.sleep(interval)


if __name__ == "__main__":
    try:
        tail_and_merge(file_path1, file_path2, merged_file, interval=0.3)
    except KeyboardInterrupt:
        print("\n\n⛔ Monitoring dihentikan oleh user.")
    except Exception as e:
        print(f"❌ Error: {e}")
