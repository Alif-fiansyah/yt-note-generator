# YouTube Note Generator

A versatile Command-Line Interface (CLI) application designed to extract YouTube subtitles, retrieve original video metadata, generate AI-powered study summaries via Google Gemini, and export structured notes minute-by-minute into Markdown, HTML (Dark Mode), or Plain Text.

## Features

- **AI-Powered Summarization**: Integrates Google Gemini API (`google-genai`) to generate key takeaways and study summaries at the top of your notes.
- **Multi-Format Export**: Export your notes into Markdown (`.md`), styled Dark Mode HTML (`.html`), or clean Plain Text (`.txt`).
- **Smart Subtitle Fallback**: Automatically fetches Indonesian (`id`) or English (`en`) subtitles with fallback translation support.
- **Dual Interaction Modes**: Supports non-interactive CLI flags (`argparse`) for pipelines and interactive terminal prompts for daily use.
- **Automated Metadata Extraction**: Retrieves original video titles via YouTube's public oEmbed endpoint without requiring an API key.
- **Clickable Timestamp Links**: Embeds direct video timestamps for every minute block.
- **Reading Statistics**: Calculates total captured words to gauge reading and study duration.

## Prerequisites

- Python: Version 3.8 or higher.
- Git: To clone the repository.
- (Optional) Google Gemini API Key: For generating AI summaries.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/Alif-fiansyah/yt-note-generator.git](https://github.com/Alif-fiansyah/yt-note-generator.git)
   cd yt-note-generator
2.   **Setup Virtual Environment & Install Dependencies for Windows:**
     ```bash
     python -m venv env
     env\Scripts\activate
     pip install youtube-transcript-api google-genai markdown
3.  **For macOS and Linux (Bash/Zsh):**
     ```bash
     python -m venv env
     source env/bin/activate
     pip install youtube-transcript-api google-genai markdown
4.  **(Optional) Configure Gemini API Key:**
     Create a `.env` file in the root directory
    ```bash
    GEMINI_API_KEY=your_gemini_api_key_here 
     
4.  **Run the script:**
     ```bash
    python main.py

---

### Interactive Prompt

| Prompt | Description | Example |
| :--- | :--- | :--- |
| `Masukan URL YouTube`| YouTube video URL (standard, shortened, or live) | `https://youtu.be/VeDdROBN25Q` |
| `Mulai dari menit ke berapa?` |Starting extraction minute| `0` |
| `Sampai menit ke berapa?` | Ending extraction minute | `10` |
| `Format output (md/html/txt):` | Target export format | `md / html / txt` |
| `Buat ringkasan cerdas dengan AI?:` | Generate key takeaways using Gemini | `y / n` |


---
### Sample Output
````
# Apple September Event Recap

- **URL Referensi:** [https://youtu.be/mp3FOz5rdB8](https://youtu.be/mp3FOz5rdB8)
- **Video ID:** `mp3FOz5rdB8`
- **Rentang Waktu:** Menit 0 s/d Menit 10
- **Total Kata Terekam:** ~1437 kata

---

## 🤖 Ringkasan Cerdas AI (Key Takeaways)

- Pembahasan desain perangkat baru dan durabilitas material bodi.
- Peningkatan refresh rate layar dinamis 1–120Hz dan tingkat kecerahan 3000 nits.
- Sertifikasi ketahanan air dan debu IP68 hingga kedalaman 6 meter.

---

## 📝 Rangkuman Transkrip Per Menit

### [Menit ke-00:00](https://youtu.be/mp3FOz5rdB8?t=0)
Halo guys, David disini, dan semalem Apple baru aja ngenalin...

### [Menit ke-01:00](https://youtu.be/mp3FOz5rdB8?t=60)
Yang bikin saya penasaran, dan itu cuma bisa kejawab kalau...
## Tech Stack
````

- **Language**: Python 3
- **AI Engine**: Google Gemini API (`google-genai`)
- **Subtitle Parser**: `youtube-transcript-api` (Executed via shell wrapper)
- **Markdown & HTML Compiler**: : `markdown`
- **CLI Parser**: `argparse`
- **Core Modules**: `subprocess, json, collections.defaultdict, urllib.parse, urllib.request, os, sys`
---

## License

This project is licensed under the [MIT License](LICENSE).
