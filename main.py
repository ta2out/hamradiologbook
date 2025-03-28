import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

class HamRadioLogBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Amatör Radyo Günlük Defteri")
        self.root.geometry("360x500")
        self.root.configure(bg="#2C3E50")

        self.entries = []
        
        self.appdata_path = os.path.join(os.getenv("APPDATA"), "ham_radio_log")
        os.makedirs(self.appdata_path, exist_ok=True)
        self.log_file = os.path.join(self.appdata_path, "log.csv")
        
        self.load_previous_logs()
        
        frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        
        tk.Label(frame, text="Çağrı İşareti:", fg="white", bg="#34495E").grid(row=0, column=0, pady=5, sticky="w")
        self.callsign_entry = tk.Entry(frame)
        self.callsign_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(frame, text="Frekans (MHz):", fg="white", bg="#34495E").grid(row=1, column=0, pady=5, sticky="w")
        self.freq_entry = tk.Entry(frame)
        self.freq_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(frame, text="Sinyal Raporu:", fg="white", bg="#34495E").grid(row=2, column=0, pady=5, sticky="w")
        self.signal_entry = tk.Entry(frame)
        self.signal_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(frame, text="Modülasyon Türü:", fg="white", bg="#34495E").grid(row=3, column=0, pady=5, sticky="w")
        self.modulation_entry = tk.Entry(frame)
        self.modulation_entry.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(frame, text="Çıkış Gücü (W):", fg="white", bg="#34495E").grid(row=4, column=0, pady=5, sticky="w")
        self.power_entry = tk.Entry(frame)
        self.power_entry.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Button(frame, text="QSO Kaydet", command=self.log_qso, bg="#1ABC9C", fg="white").grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
        tk.Button(frame, text="Günlüğü Kaydet", command=self.save_log, bg="#E74C3C", fg="white").grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
        tk.Button(frame, text="Günlükleri Sil", command=self.clear_logs, bg="#D35400", fg="white").grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")
        
        self.log_listbox = tk.Listbox(frame, width=50, height=15)
        self.log_listbox.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.display_previous_logs()
    
    def log_qso(self):
        callsign = self.callsign_entry.get().strip()
        freq = self.freq_entry.get().strip()
        signal = self.signal_entry.get().strip()
        modulation = self.modulation_entry.get().strip()
        power = self.power_entry.get().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not callsign or not freq or not signal or not modulation or not power:
            messagebox.showwarning("Giriş Hatası", "Tüm alanlar doldurulmalıdır!")
            return
        
        if not freq.replace('.', '', 1).isdigit():
            messagebox.showwarning("Giriş Hatası", "Frekans sadece rakam içermelidir!")
            return
        
        if not power.isdigit():
            messagebox.showwarning("Giriş Hatası", "Çıkış gücü sadece sayı olmalıdır!")
            return
        
        entry = [timestamp, callsign, freq, signal, modulation, power]
        self.entries.append(entry)
        self.log_listbox.insert(tk.END, f"{timestamp} - {callsign} - {freq} MHz - {signal} - {modulation} - {power} W")
        
        self.callsign_entry.delete(0, tk.END)
        self.freq_entry.delete(0, tk.END)
        self.signal_entry.delete(0, tk.END)
        self.modulation_entry.delete(0, tk.END)
        self.power_entry.delete(0, tk.END)
    
    def save_log(self):
        with open(self.log_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tarih-Saat", "Çağrı İşareti", "Frekans", "Sinyal Raporu", "Modülasyon Türü", "Çıkış Gücü"])
            writer.writerows(self.entries)
        messagebox.showinfo("Kaydedildi", f"Günlük başarıyla kaydedildi! Konum: {self.log_file}")
    
    def clear_logs(self):
        if messagebox.askyesno("Onay", "Tüm günlükleri silmek istediğinize emin misiniz?"):
            self.entries = []
            self.log_listbox.delete(0, tk.END)
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            messagebox.showinfo("Silindi", "Tüm günlükler başarıyla silindi.")
    
    def load_previous_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                reader = csv.reader(file)
                next(reader, None)
                self.entries = [row for row in reader]
    
    def display_previous_logs(self):
        self.log_listbox.delete(0, tk.END)
        for entry in self.entries:
            self.log_listbox.insert(tk.END, f"{entry[0]} - {entry[1]} - {entry[2]} MHz - {entry[3]} - {entry[4]} - {entry[5]} W")

if __name__ == "__main__":
    root = tk.Tk()
    app = HamRadioLogBook(root)
    root.mainloop()
