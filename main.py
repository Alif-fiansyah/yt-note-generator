import sys
import os
import json
import subprocess
import argparse
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from collections import defaultdict
import markdown

# Setup opsional untuk AI Summarizer (Gemini API)
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

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
    """Mengambil judul asli video menggunakan endpoint oEmbed."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("title", f"Video {video_id}")
    except Exception:
        return f"Video {video_id}"

def fetch_transcript_smart(video_id):
    """Mengambil transkrip dengan fallback id -> en -> format json via subprocess."""
    cmd = [
        sys.executable, "-m", "youtube_transcript_api", 
        video_id, "--languages", "id", "en", "--format", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    parsed_data = json.loads(result.stdout)
    
    # Ratakan struktur data jika bersarang
    if isinstance(parsed_data, dict):
        for key, val in parsed_data.items():
            if isinstance(val, list):
                return val
    elif isinstance(parsed_data, list):
        if len(parsed_data) > 0 and isinstance(parsed_data[0], list):
            return parsed_data[0]
        return parsed_data
        
    return []

def summarize_with_ai(full_text):
    """Meringkas transkrip menggunakan Gemini API jika key tersedia."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not HAS_GENAI:
        return None

    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            "Kamu adalah asisten akademis cerdas. Buatlah ringkasan terstruktur dan poin-poin "
            "penting (key takeaways) dari transkrip video perkuliahan/materi berikut:\n\n"
            f"{full_text[:12000]}"
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"[!] Gagal membuat ringkasan AI: {e}")
        return None

def save_output(filename, md_content, export_format):
    """Menyimpan hasil catatan sesuai format yang diminta (md, html, txt)."""
    base_name, _ = os.path.splitext(filename)
    
    if export_format == "html":
        target_file = f"{base_name}.html"
        body_html = markdown.markdown(md_content, extensions=['extra'])
        html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Catatan Kuliah YouTube</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            background-color: #0d1117;
            color: #c9d1d9;
            max-width: 850px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        h1, h2, h3 {{ color: #58a6ff; border-bottom: 1px solid #21262d; padding-bottom: 0.3em; }}
        a {{ color: #58a6ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{ border: 0; height: 1px; background: #30363d; margin: 24px 0; }}
        code {{ background: #161b22; padding: 0.2em 0.4em; border-radius: 6px; }}
        blockquote {{ border-left: 0.25em solid #388bfd; color: #8b949e; padding: 0 1em; margin: 0; }}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_template)
    elif export_format == "txt":
        target_file = f"{base_name}.txt"
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(md_content)
    else:
        target_file = f"{base_name}.md"
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(md_content)

    return target_file

def generate_notes(url, start_min, end_min, output_file=None, export_format="md", use_ai=False):
    video_id = get_video_id(url)
    if video_id == "Unknown_ID":
        print("[!] Format URL YouTube tidak valid.")
        return

    default_name = f"catatan_rentang_{video_id}"
    target_name = output_file or default_name

    try:
        print("[*] Mengambil informasi dan subtitle video...")
        title = get_video_title(video_id)
        transcript_data = fetch_transcript_smart(video_id)

        start_sec = int(start_min) * 60
        end_sec = int(end_min) * 60

        grouped_text = defaultdict(list)
        all_text_list = []
        total_words = 0

        for item in transcript_data:
            if isinstance(item, dict) and "start" in item and "text" in item:
                item_start = item["start"]
                if start_sec <= item_start <= end_sec:
                    current_minute = int(item_start // 60)
                    clean_text = item["text"].replace("\n", " ").strip()
                    grouped_text[current_minute].append(clean_text)
                    all_text_list.append(clean_text)
                    total_words += len(clean_text.split())

        # Buat dokumen Markdown
        md_lines = [
            f"# {title}\n",
            f"- **URL Referensi:** [{url}]({url})",
            f"- **Video ID:** `{video_id}`",
            f"- **Rentang Waktu:** Menit {start_min} s/d Menit {end_min}",
            f"- **Total Kata Terekam:** ~{total_words} kata\n",
            "---\n"
        ]

        # Fitur AI Summary opsional
        if use_ai:
            print("[*] Menganalisis dan menyusun ringkasan AI...")
            combined_text = " ".join(all_text_list)
            ai_summary = summarize_with_ai(combined_text)
            if ai_summary:
                md_lines.append("## 🤖 Ringkasan Cerdas AI (Key Takeaways)\n")
                md_lines.append(f"{ai_summary}\n")
                md_lines.append("---\n")

        md_lines.append("## 📝 Rangkuman Transkrip Per Menit\n")

        if not grouped_text:
            md_lines.append("*Tidak ada percakapan terdeteksi pada rentang waktu ini.*\n")
        else:
            for minute in sorted(grouped_text.keys()):
                timestamp_sec = minute * 60
                timestamp_link = f"https://youtu.be/{video_id}?t={timestamp_sec}"
                md_lines.append(f"### [Menit ke-{minute:02d}:00]({timestamp_link})\n")
                md_lines.append(f"{' '.join(grouped_text[minute])}\n")

        full_md_content = "\n".join(md_lines)
        saved_file = save_output(target_name, full_md_content, export_format)
        print(f"[+] Berhasil! Catatan tersimpan di: {saved_file}")

    except Exception as e:
        print(f"[!] Terjadi kesalahan: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Note Generator - Transkripsi otomatis per menit, Smart AI Summary, dan Multi-format Export."
    )
    parser.add_argument("-u", "--url", type=str, help="URL video YouTube")
    parser.add_argument("-s", "--start", type=int, help="Menit awal ekstraksi")
    parser.add_argument("-e", "--end", type=int, help="Menit akhir ekstraksi")
    parser.add_argument("-o", "--output", type=str, help="Nama file luaran (opsional)")
    parser.add_argument("-f", "--format", type=str, choices=["md", "html", "txt"], default="md", help="Format file: md, html, atau txt (default: md)")
    parser.add_argument("--ai", action="store_true", help="Gunakan AI untuk membuat ringkasan materi")

    args = parser.parse_args()

    if args.url and args.start is not None and args.end is not None:
        generate_notes(args.url.strip(), args.start, args.end, args.output, args.format, args.ai)
    else:
        print("--- Pembuat Catatan YouTube Otomatis (Pro Edition) ---")
        url_input = input("Masukkan URL YouTube: ")
        start_input = input("Mulai dari menit ke berapa?: ")
        end_input = input("Sampai menit ke berapa?: ")
        format_input = input("Format output (md/html/txt) [default: md]: ").strip().lower() or "md"
        ai_choice = input("Buat ringkasan cerdas dengan AI? (y/n) [default: n]: ").strip().lower()
        use_ai = ai_choice == 'y'

        if url_input and start_input and end_input:
            generate_notes(url_input.strip(), start_input.strip(), end_input.strip(), None, format_input, use_ai)
        else:
            print("[-] Input wajib tidak boleh kosong.")

if __name__ == "__main__":
    main()