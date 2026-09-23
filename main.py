import sys
import json
import subprocess
import argparse
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from collections import defaultdict

def get_video_id(url):
    """Mengekstrak YouTube Video ID dari berbagai variasi URL."""
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        if "live" in parsed_url.path:
            return parsed_url.path.split("/")[-1]
        elif "v" in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)["v"][0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
    return "Unknown_ID"

def get_video_title(video_id):
    """Mengambil judul asli video menggunakan endpoint publik oEmbed tanpa API Key."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("title", f"Video {video_id}")
    except Exception:
        return f"Video {video_id}"

def generate_notes(url, start_min, end_min, output_file=None):
    video_id = get_video_id(url)
    if video_id == "Unknown_ID":
        print("[!] Format URL YouTube tidak valid atau tidak dikenali.")
        return

    filename = output_file or f"catatan_rentang_{video_id}.md"
    
    try:
        print("[*] Mengambil informasi dan subtitle video...")
        title = get_video_title(video_id)

        cmd = [
            sys.executable, "-m", "youtube_transcript_api", 
            video_id, "--languages", "id", "en", "--format", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        parsed_data = json.loads(result.stdout)
        
        # Pengaman struktur data JSON
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
        
        grouped_text = defaultdict(list)
        total_words = 0
        
        for item in transcript_data:
            if isinstance(item, dict) and "start" in item and "text" in item:
                item_start = item["start"]
                if start_sec <= item_start <= end_sec:
                    current_minute = int(item_start // 60)
                    clean_text = item["text"].replace("\n", " ").strip()
                    grouped_text[current_minute].append(clean_text)
                    total_words += len(clean_text.split())

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"# {title}\n\n")
            file.write(f"- **URL Referensi:** [{url}]({url})\n")
            file.write(f"- **Video ID:** `{video_id}`\n")
            file.write(f"- **Rentang Waktu:** Menit {start_min} s/d Menit {end_min}\n")
            file.write(f"- **Total Kata Terekam:** ~{total_words} kata\n\n")
            file.write("---\n\n")
            file.write("## 📝 Rangkuman Transkrip Per Menit\n\n")
            
            if not grouped_text:
                file.write("*Tidak ada percakapan terdeteksi pada rentang waktu ini.*\n")
            else:
                for minute in sorted(grouped_text.keys()):
                    # Tautan waktu langsung ke detik video YouTube
                    timestamp_sec = minute * 60
                    timestamp_link = f"https://youtu.be/{video_id}?t={timestamp_sec}"
                    
                    file.write(f"### [Menit ke-{minute:02d}:00]({timestamp_link})\n\n")
                    content = " ".join(grouped_text[minute])
                    file.write(f"{content}\n\n")
                
        print(f"[+] Berhasil! Catatan terstruktur tersimpan di: {filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"[!] Gagal mengambil subtitle. Error log:\n{e.stderr}")
    except Exception as e:
        print(f"[!] Terjadi kesalahan sistem: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Note Generator - Ekstraksi subtitle terstruktur per menit ke Markdown"
    )
    parser.add_argument("-u", "--url", type=str, help="URL video YouTube")
    parser.add_argument("-s", "--start", type=int, help="Menit awal ekstraksi")
    parser.add_argument("-e", "--end", type=int, help="Menit akhir ekstraksi")
    parser.add_argument("-o", "--output", type=str, help="Nama file output .md (opsional)")

    args = parser.parse_args()

    # Jika argument lengkap disediakan lewat terminal flag
    if args.url and args.start is not None and args.end is not None:
        generate_notes(args.url.strip(), args.start, args.end, args.output)
    else:
        # Fallback interaktif jika dijalankan tanpa flags
        print("--- Pembuat Catatan YouTube Otomatis (Format Per Menit) ---")
        url_input = input("Masukkan URL YouTube: ")
        start_input = input("Mulai dari menit ke berapa?: ")
        end_input = input("Sampai menit ke berapa?: ")
        
        if url_input and start_input and end_input:
            generate_notes(url_input.strip(), start_input.strip(), end_input.strip())
        else:
            print("[-] Input tidak boleh ada yang kosong.")

if __name__ == "__main__":
    main()