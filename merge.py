import time
import threading
import os
from datetime import datetime

def tail_and_merge(file1, file2, output_file, interval=0.5):
    """
    Monitor 2 file secara real-time dan satukan isinya ke output_file
    """
    
    # Simpan posisi terakhir yang sudah dibaca
    pos1 = 0
    pos2 = 0
    
    print(f"🚀 Mulai monitoring merge")
    
    with open(output_file, 'a', encoding='utf-8') as out:
        while True:
            updated = False
            
            # Cek File 1
            if os.path.exists(file1):
                with open(file1, 'r', encoding='utf-8') as f1:
                    f1.seek(pos1)
                    new_content1 = f1.read()
                    if new_content1:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        out.write(f"\n--- [FILE 1] {timestamp} ---\n")
                        out.write(new_content1)
                        out.flush()          # Langsung tulis ke disk
                        pos1 = f1.tell()
                        updated = True
            
            # Cek File 2
            if os.path.exists(file2):
                with open(file2, 'r', encoding='utf-8') as f2:
                    f2.seek(pos2)
                    new_content2 = f2.read()
                    if new_content2:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        out.write(f"\n--- [FILE 2] {timestamp} ---\n")
                        out.write(new_content2)
                        out.flush()
                        pos2 = f2.tell()
                        updated = True
            
            if updated:
                print(f"✅ Merge berhasil | {datetime.now().strftime('%H:%M:%S')}\n")
            
            time.sleep(interval)


# ================== PENGGUNAAN ==================

if __name__ == "__main__":
    # Ganti dengan nama file kamu
    file_path1 = "post_params.txt"      # File pertama yang sedang ditulis
    file_path2 = "get_params.txt"      # File kedua yang sedang ditulis
    merged_file = "dua.txt"
    
    try:
        tail_and_merge(file_path1, file_path2, merged_file, interval=0.3)
    except KeyboardInterrupt:
        print("\n⛔ Monitoring dihentikan oleh user.")
    except Exception as e:
        print(f"❌ Error: {e}")
