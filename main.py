import sys
from urllib.parse import urlparse, parse_qs

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

def generate_notes_template(url, start_min, end_min):
    video_id = get_video_id(url)
    filename = f"catatan_rentang_{video_id}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"# Catatan Video YouTube\n")
            file.write(f"**URL Referensi:** {url}\n")
            file.write(f"**Video ID:** {video_id}\n\n")
            file.write("## Ringkasan Sesi\n\n")
            file.write(f"### Rentang Waktu: Menit {start_min} - {end_min}\n")
            file.write("- [Tulis poin-poin penting atau ringkasan materi dari sesi ini...]\n")
            file.write("- [Tambahkan poin lainnya di sini...]\n\n")
                
        print(f"[+] Berhasil! Template catatan telah dibuat: {filename}")
    except Exception as e:
        print(f"[!] Terjadi kesalahan saat membuat file: {e}")

if __name__ == "__main__":
    print("--- Pembuat Template Catatan YouTube (Mode Rentang Waktu) ---")
    url_input = input("Masukkan URL YouTube: ")
    start_input = input("Mulai dari menit ke berapa?: ")
    end_input = input("Sampai menit ke berapa?: ")
    
    if url_input and start_input and end_input:
        generate_notes_template(url_input.strip(), start_input.strip(), end_input.strip())
    else:
        print("[-] Input tidak boleh ada yang kosong.")
