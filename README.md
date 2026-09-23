# YouTube Note Generator

A versatile Command-Line Interface (CLI) application designed to help students automatically extract YouTube subtitles, retrieve original video metadata, and generate structured Markdown notes grouped minute-by-minute with clickable timestamp links.

## Features

- **Dual Interaction Modes**: Supports non-interactive CLI flags (`argparse`) for automation/pipelining and interactive prompts for casual terminal usage.
- **Automated Metadata Extraction**: Fetches the video title via YouTube's public oEmbed endpoint without requiring an API key.
- **Minute-by-Minute Grouping**: Dynamically calculates and groups extracted subtitles into clean minute blocks using `collections.defaultdict`.
- **Clickable Timestamp Links**: Automatically embeds direct YouTube video timestamps for every minute block.
- **Reading Statistics**: Calculates total captured words to gauge reading and study time.
- **Robust Subprocess Execution**: Bypasses local import shadowing by executing the transcript API directly via the Python shell.
- **JSON Auto-Parsing**: Flattens nested JSON payloads from multi-language subtitle queries.

## Prerequisites

- Python: Version 3.8 or higher.
- Git: To clone the repository to your local machine.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/Alif-fiansyah/yt-note-generator.git](https://github.com/Alif-fiansyah/yt-note-generator.git)
   cd yt-note-generator
2.   **Setup Virtual Environment & Install Dependencies for Windows:**
     ```bash
     python -m venv env
     env\Scripts\activate
     pip install youtube-transcript-api
3.  **For macOS and Linux (Bash/Zsh):**
     ```bash
     python -m venv env
     source env/bin/activate
     pip install youtube-transcript-api
4.  **Run the script:**
     ```bash
    python main.py

---

## Usage Examples

### Interactive Prompt

| Prompt | Description | Example |
| :--- | :--- | :--- |
| `Masukan URL YouTube`| YouTube video URL (standard, shortened, or live) | `https://youtu.be/VeDdROBN25Q` |
| `Mulai dari menit ke berapa?` |Starting extraction minute| `2` |
| `Sampai menit ke berapa?` | Ending extraction minute | `6` |

---
### Sample Output

Output preview inside `catatan_rentang_VwDrR0BIG5Q.md`:

````markdown
# Pengenalan Arsitektur Jaringan Komputer

- **URL Referensi:** [https://youtu.be/VwDrR0BIG5Q](https://youtu.be/VwDrR0BIG5Q)
- **Video ID:** `VwDrR0BIG5Q`
- **Rentang Waktu:** Menit 2 s/d Menit 6
- **Total Kata Terekam:** ~420 kata

---

## 📝 Rangkuman Transkrip Per Menit

### [Menit ke-02:00](https://youtu.be/VwDrR0BIG5Q?t=120)
Transkrip percakapan materi kuliah yang dibahas pada menit kedua...

### [Menit ke-03:00](https://youtu.be/VwDrR0BIG5Q?t=180)
Kelanjutan penjelasan materi kuliah yang dibahas pada menit ketiga...
````
## Tech Stack

- **Language**: Python 3
- **Library**: `youtube-transcript-api` (Executed via shell wrapper)
- **CLI Parser**: `argparse`
- **Core Modules**: `subprocess, json, collections.defaultdict, urllib.parse, urllib.request`
- **Storage**: Local Markdown (`.md`) File System
---

## License

This project is licensed under the [MIT License](LICENSE).
