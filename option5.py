import subprocess
import sys
import shutil
import os
import urllib.request
import zipfile
import platform

def clear_console():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

# Call the function to clear the console
clear_console()

def run(cmd):
    subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_and_setup_packages():
    print("Installing requirements...")
    packages = ["yt-dlp", "pytube"]
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))  # try importing
        except Exception:
            try:
                run(f"{sys.executable} -m pip uninstall -y {pkg}")
            except: pass
            run(f"{sys.executable} -m pip install {pkg}")

def ffmpeg_works(ffmpeg_path):
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def cleanup_ffmpeg_folder(ffmpeg_root):
    # Keep only the first ffmpeg folder, delete extras
    folders = [f.path for f in os.scandir(ffmpeg_root) if f.is_dir()]
    if len(folders) > 1:
        for folder in folders[1:]:
            shutil.rmtree(folder, ignore_errors=True)

def download_ffmpeg(dest_folder):
    system = platform.system()
    if system != "Windows":
        print("❌ Only Windows is supported for FFmpeg auto-install.")
        sys.exit(1)

    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path and ffmpeg_works(ffmpeg_path):
        return ffmpeg_path  # already installed and working

    # Cleanup existing folders first
    if os.path.exists(dest_folder):
        cleanup_ffmpeg_folder(dest_folder)
    else:
        os.makedirs(dest_folder, exist_ok=True)

    print("📥 Downloading FFmpeg...'may take some time'")
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(dest_folder, "ffmpeg.zip")
    urllib.request.urlretrieve(ffmpeg_url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)

    # Find the bin folder containing ffmpeg.exe
    for root, dirs, files in os.walk(dest_folder):
        if "ffmpeg.exe" in files:
            ffmpeg_bin = root
            break
    else:
        print("❌ FFmpeg extraction failed.")
        sys.exit(1)

    os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ["PATH"]
    return shutil.which("ffmpeg")

# ---------- Setup ----------
check_and_setup_packages()

import yt_dlp

ffmpeg_path = download_ffmpeg(os.path.join(os.getcwd(), "ffmpeg"))

last_percent = 0
def progress(d):
    global last_percent
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        percent = int(d.get('downloaded_bytes', 0) / total * 100)
        if percent // 10 > last_percent // 10:
            last_percent = percent
            print(f"⬇️ Download progress: {percent}%")

print("===========================================")
print("        🎬 YouTube Video Downloader        ")
print("===========================================\n")

url = input("Enter YouTube URL: ").strip()
if not url:
    print("❌ No URL provided. Exiting.")
    sys.exit(1)

res_input = input("Enter max resolution (e.g., 720) or leave blank for best: ").strip()
resolution = res_input if res_input else "best"

ydl_opts = {
    'format': f'bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/best',
    'merge_output_format': 'mp4',
    'ffmpeg_location': ffmpeg_path,
    'progress_hooks': [progress],
    'noplaylist': True,
    'quiet': True,
}

print("\n🔽 Starting download...\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        print(f"\n✅ Download completed: {info.get('title', 'Unknown title')}")
except Exception as e:
    print(f"\n❌ Download failed. Details: {e}")
