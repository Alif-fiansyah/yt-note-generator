import sys
import json
import subprocess
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

def get_video_id(url):
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        if "live" in parsed_url.path:
            return parsed_url.path.split("/")[-1]
        elif "v" in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)["v"][0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
    return "Unknown_ID"

def generate_notes(url, start_min, end_min):
    video_id = get_video_id(url)
    filename = f"catatan_rentang_{video_id}.md"
    
    try:
        print("[*] Sedang mengekstrak subtitle (mohon tunggu)...")
        cmd = [
            sys.executable, "-m", "youtube_transcript_api", 
            video_id, "--languages", "id", "en", "--format", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        parsed_data = json.loads(result.stdout)
        
        # --- PENGAMAN STRUKTUR DATA JSON ---
        transcript_data = []
        if isinstance(parsed_data, dict):
            for key, val in parsed_data.items():
                if isinstance(val, list):
                    transcript_data.extend(val)
        elif isinstance(parsed_data, list):
            if len(parsed_data) > 0 and isinstance(parsed_data[0], list):
                transcript_data = parsed_data[0]
            else:
                transcript_data = parsed_data
                
        start_sec = int(start_min) * 60
        end_sec = int(end_min) * 60
        
        # Dictionary otomatis untuk mengelompokkan teks per menit
        grouped_text = defaultdict(list)
        
        for item in transcript_data:
            if isinstance(item, dict) and "start" in item and "text" in item:
                item_start = item["start"]
                if item_start >= start_sec and item_start <= end_sec:
                    # Menghitung blok menit saat ini (misal: detik 185 // 60 = menit ke-3)
                    current_minute = int(item_start // 60)
                    grouped_text[current_minute].append(item["text"].replace("\n", " "))

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"# Catatan Video YouTube\n")
            file.write(f"**URL Referensi:** {url}\n")
            file.write(f"**Video ID:** {video_id}\n\n")
            file.write("## Ringkasan Sesi\n\n")
            
            if not grouped_text:
                file.write(f"### Rentang Waktu: Menit {start_min} - {end_min}\n")
                file.write("*Tidak ada percakapan yang terdeteksi pada rentang waktu ini.*\n")
            else:
                # Mengurutkan kunci agar urutan menit selalu dari yang terkecil
                for minute in sorted(grouped_text.keys()):
                    file.write(f"### Menit ke-{minute}\n")
                    content = " ".join(grouped_text[minute])
                    file.write(f"{content}\n\n")
                
        print(f"[+] Berhasil! Catatan per menit telah dibuat: {filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"[!] Gagal mengambil subtitle. Pastikan URL benar. Error log:\n{e.stderr}")
    except Exception as e:
        print(f"[!] Terjadi kesalahan sistem: {e}")

if __name__ == "__main__":
    print("--- Pembuat Catatan YouTube Otomatis (Format Per Menit) ---")
    url_input = input("Masukkan URL YouTube: ")
    start_input = input("Mulai dari menit ke berapa?: ")
    end_input = input("Sampai menit ke berapa?: ")
    
    if url_input and start_input and end_input:
        generate_notes(url_input.strip(), start_input.strip(), end_input.strip())
    else:
        print("[-] Input tidak boleh ada yang kosong.")