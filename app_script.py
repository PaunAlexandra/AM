# app_script.py
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class LyricsVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyrics Video Generator")
        self.root.geometry("500x400")
        self.root.configure(bg="#ffe6f0")  

        self.audio_path = None
        self.lyrics_path = None
        self.output_basename = None

        button_frame = tk.Frame(root, bg="#ffe6f0")
        button_frame.pack(expand=True)
        tk.Button(button_frame, text="Încarcă fișierul .mp3", command=self.incarca_audio, bg="#add8e6", width=30).pack(pady=10)
        tk.Button(button_frame, text="Încarcă fișierul .txt", command=self.incarca_versuri, bg="#add8e6", width=30).pack(pady=10)
        tk.Button(button_frame, text="Începe sincronizarea (WhisperX)", command=self.sincronizeaza_whisperx, bg="#add8e6", width=30).pack(pady=10)
        tk.Button(button_frame, text="Generează Video", command=self.genereaza_video, bg="#add8e6", width=30).pack(pady=10)
        tk.Button(button_frame, text="Vizualizează biblioteca", command=self.vizualizeaza_biblioteca, bg="#add8e6", width=30).pack(pady=10)

    def incarca_audio(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if path:
            self.audio_path = path
            self.output_basename = os.path.splitext(os.path.basename(path))[0]
            messagebox.showinfo("Selectat", f"Audio: {os.path.basename(path)}")

    def incarca_versuri(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.lyrics_path = path
            messagebox.showinfo("Selectat", f"Versuri: {os.path.basename(path)}")

    def afiseaza_ecran_incarcare(self, message="Se proceseaza..."):
        self.loading = tk.Toplevel(self.root)
        self.loading.title("Așteaptă")
        self.loading.configure(bg="#ffe6f0")
        tk.Label(self.loading, text=message, fg="black", bg=self.loading["bg"]).pack(padx=20, pady=20)
        self.loading.geometry("300x200")
        self.loading.transient(self.root)
        self.loading.grab_set()
        self.root.update()

    def ascunde_ecran_incarcare(self):
        if hasattr(self, 'loading'):
            self.loading.destroy()

    def sincronizeaza_whisperx(self):
        if not self.audio_path or not self.lyrics_path:
            messagebox.showerror("Eroare", "Selecteaza versuri si audio.")
            return

        self.afiseaza_ecran_incarcare("Se sincronizează cu WhisperX...")

        self.output_basename = os.path.splitext(os.path.basename(self.audio_path))[0]
        output_dir = os.path.join("output_spleeter", self.output_basename)

        subprocess.run([
            "conda", "run", "-n", "spleeter_env",
            "spleeter", "separate", "-o", "output_spleeter", "-p", "spleeter:2stems", self.audio_path,
        ], check=True, stderr=subprocess.STDOUT)

        vocals_path = os.path.join("output_spleeter", self.output_basename, "vocals.wav")

        os.makedirs("mapare", exist_ok=True)

        map_file = os.path.join("mapare", f"mapare_{self.output_basename}.json")
        result = subprocess.run([
            "conda", "run", "-n", "whisperx_env", "python", "whisperx_script.py",
            vocals_path, self.lyrics_path, map_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        self.ascunde_ecran_incarcare()

        messagebox.showinfo("Gata!", "S-a finalizat sincronizarea WhisperX!")

    def genereaza_video(self):
        if not self.audio_path:
            messagebox.showerror("Eroare", "Încarcă fișierul audio.")
            return

        map_file = os.path.join("mapare", f"mapare_{self.output_basename}.json")
        if not os.path.exists(map_file):
            messagebox.showerror("Eroare", "Încarcă fișierul text.")
            return

        self.afiseaza_ecran_incarcare("Se generează video-ul...")
        video_file = f"lyrics_{self.output_basename}.mp4"
        subprocess.run([
            "conda", "run", "-n", "am", "python", "video_generator.py",
            self.audio_path, map_file, video_file
        ], check=True)
        self.ascunde_ecran_incarcare()
        messagebox.showinfo("Gata!", f" Video-ul '{video_file}' a fost generat!")

        self.reda_video(video_file)

    def reda_video(self, path):
        subprocess.run(["open", path])

    def vizualizeaza_biblioteca(self):
        library_window = tk.Toplevel(self.root)
        library_window.title("Bibliotecă videoclipuri")
        library_window.geometry("500x400")
        library_window.configure(bg="#ffe6f0")

        label = tk.Label(library_window, text="Videoclipuri generate:", bg="#ffe6f0", fg="black", font=("Helvetica", 14, "bold"))
        label.pack(pady=10)

        listbox = tk.Listbox(library_window, bg="#d3e6eb", fg="black", font=("Helvetica", 14), width=50)
        listbox.pack(pady=10, expand=True)

        video_files = [f for f in os.listdir(os.getcwd()) if f.endswith(".mp4")]
        for video in video_files:
            listbox.insert(tk.END, video)

        def redare_selectie_biblioteca():
            selected = listbox.curselection()
            if selected:
                filename = listbox.get(selected[0])
                self.reda_video(filename)

        play_button = tk.Button(library_window, text="Redă videoclipul selectat", command=redare_selectie_biblioteca, bg="#add8e6", font=("Helvetica", 12))
        play_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsVideoApp(root)
    root.mainloop()
