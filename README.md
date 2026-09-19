# YouTube Note Generator

A lightweight Command-Line Interface (CLI) application designed to help students automatically extract YouTube subtitles and generate structured Markdown notes, grouped precisely minute-by-minute based on specific time ranges.

---

## Features

- **Smart URL Parsing**: Extract Video IDs automatically from various formats including standard links, short links (youtu.be), and live streams.
- **Minute-by-Minute Grouping**: Dynamically calculates and groups extracted text into specific minute blocks using `collections.defaultdict`.
- **Robust Subprocess Execution**: Safely bypasses common Python import shadowing and environment bugs by executing the transcript API directly via shell.
- **JSON Auto-Parsing**: Automatically flattens and parses nested JSON arrays from multi-language subtitle requests.

---

## Prerequisites

- **Python**: Version 3.0 or higher.
- **Git**: To clone the repository to your local machine.

---

## Installation & Setup

1. **Clone the repository:**
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
| `Masukan URL YouTube`| Link video referensi yang ingin diambil teksnya | `https://youtu.be/VeDdROBN25Q` |
| `Mulai dari menit ke berapa?` |Menit awal ekstraksi teks dimulai | `3` |
| `Sampai menit ke berapa?` | Menit akhir ekstraksi teks selesai | `6` |

---
### Sample Output
Hasil *generate* otomatis di dalam file `catatan_rentang_VeDdROBN25Q.md`:

```text
# Catatan Video YouTube
**URL Referensi:** [https://youtu.be/VeDdROBN25Q](https://youtu.be/VeDdROBN25Q)
**Video ID:** VeDdROBN25Q

## Ringkasan Sesi

### Menit ke-3
Ini adalah teks percakapan asli yang diucapkan pada menit ketiga di dalam video tersebut secara otomatis.

### Menit ke-4
Dan ini adalah kelanjutan materi atau percakapan yang dibahas ketika video memasuki menit keempat, dipisahkan secara rapi.
```
---

## Tech Stack

- **Language**: Python 3
- **Library**: youtube-transcript-api (Executed via shell wrapper)
- **Core Modules**:subprocess, json, collections.defaultdict, urllib.parse
- **Storage**: Local Markdown (.md) File System
---

## License

This project is licensed under the [MIT License](LICENSE).
