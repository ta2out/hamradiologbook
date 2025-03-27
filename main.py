#    _______  _______  _______  _______  __   __  _______ 
#    |       ||   _   ||       ||       ||  | |  ||       |
#    |_     _||  |_|  ||____   ||   _   ||  | |  ||_     _|
#      |   |  |       | ____|  ||  | |  ||  |_|  |  |   |  
#      |   |  |       || ______||  |_|  ||       |  |   |  
#      |   |  |   _   || |_____ |       ||       |  |   |  
#      |___|  |__| |__||_______||_______||_______|  |___| 

import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

class HamRadioLogBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Amatör Radyo Günlük Defteri")
        self.root.geometry("360x500")  # Başlangıç boyutu
        self.root.configure(bg="#2C3E50")

        self.entries = []
        
        # Dosya yolu
        self.appdata_path = os.path.join(os.getenv("APPDATA"), "ham_radio_log")
        os.makedirs(self.appdata_path, exist_ok=True)
        self.log_file = os.path.join(self.appdata_path, "log.csv")
        
        # Önceki kayıtları yükle
        self.load_previous_logs()
        
        # Ana çerçeve
        frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Satır ve sütun yapılandırması, büyüme özelliği ekleniyor
        frame.grid_rowconfigure(0, weight=1, minsize=30)  # Çağrı İşareti satırı
        frame.grid_rowconfigure(1, weight=1, minsize=30)  # Frekans satırı
        frame.grid_rowconfigure(2, weight=1, minsize=30)  # Sinyal Raporu satırı
        frame.grid_rowconfigure(3, weight=1, minsize=30)  # Modülasyon Türü satırı
        frame.grid_rowconfigure(4, weight=1, minsize=30)  # Çıkış Gücü satırı
        frame.grid_rowconfigure(5, weight=2, minsize=40)  # QSO Kaydet butonu
        frame.grid_rowconfigure(6, weight=2, minsize=40)  # Günlüğü Kaydet butonu
        frame.grid_rowconfigure(7, weight=2, minsize=40)  # Günlükleri Sil butonu
        frame.grid_rowconfigure(8, weight=1, minsize=30)  # Arama Yap satırı
        frame.grid_rowconfigure(9, weight=2, minsize=40)  # Filtrele butonu
        frame.grid_rowconfigure(10, weight=5, minsize=100)  # Log listbox

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        
        # Etiketler ve Girişler
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
        
        # Butonlar
        tk.Button(frame, text="QSO Kaydet", command=self.log_qso, bg="#1ABC9C", fg="white").grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
        tk.Button(frame, text="Günlüğü Kaydet", command=self.save_log, bg="#E74C3C", fg="white").grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
        tk.Button(frame, text="Günlükleri Sil", command=self.clear_logs, bg="#D35400", fg="white").grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Arama çubuğu
        tk.Label(frame, text="Arama Yap:", fg="white", bg="#34495E").grid(row=8, column=0, pady=5, sticky="w")
        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=8, column=1, pady=5, padx=5, sticky="ew")
        tk.Button(frame, text="Filtrele", command=self.filter_logs, bg="#3498DB", fg="white").grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Logları göstermek için Listbox
        self.log_listbox = tk.Listbox(frame, width=50, height=15)  # Yükseklik arttırıldı
        self.log_listbox.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Önceki kayıtları listeye ekle
        self.display_previous_logs()
        
    def log_qso(self):
        callsign = self.callsign_entry.get()
        freq = self.freq_entry.get()
        signal = self.signal_entry.get()
        modulation = self.modulation_entry.get()
        power = self.power_entry.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if callsign and freq and signal and modulation and power:
            entry = f"{timestamp} - {callsign} - {freq} MHz - {signal} - {modulation} - {power} W"
            self.entries.append([timestamp, callsign, freq, signal, modulation, power])
            self.log_listbox.insert(tk.END, entry)
            
            # Alanları temizle
            self.callsign_entry.delete(0, tk.END)
            self.freq_entry.delete(0, tk.END)
            self.signal_entry.delete(0, tk.END)
            self.modulation_entry.delete(0, tk.END)
            self.power_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Giriş Hatası", "Tüm alanlar doldurulmalıdır!")
    
    def save_log(self):
        with open(self.log_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tarih-Saat", "Çağrı İşareti", "Frekans", "Sinyal Raporu", "Modülasyon Türü", "Çıkış Gücü"])
            writer.writerows(self.entries)
        messagebox.showinfo("Kaydedildi", f"Günlük başarıyla kaydedildi!\nKonum: {self.log_file}")
    
    def clear_logs(self):
        confirm = messagebox.askyesno("Onay", "Tüm günlükleri silmek istediğinize emin misiniz? Bu işlem geri alınamaz!")
        if confirm:
            self.entries = []
            self.log_listbox.delete(0, tk.END)
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            messagebox.showinfo("Silindi", "Tüm günlükler başarıyla silindi.")
    
    def load_previous_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                reader = csv.reader(file)
                next(reader, None)  # Başlık satırını atla
                self.entries = [row for row in reader]
    
    def display_previous_logs(self):
        self.log_listbox.delete(0, tk.END)
        for entry in self.entries:
            formatted_entry = f"{entry[0]} - {entry[1]} - {entry[2]} MHz - {entry[3]} - {entry[4]} - {entry[5]} W"
            self.log_listbox.insert(tk.END, formatted_entry)
    
    def filter_logs(self):
        query = self.search_entry.get().lower()
        self.log_listbox.delete(0, tk.END)
        for entry in self.entries:
            formatted_entry = f"{entry[0]} - {entry[1]} - {entry[2]} MHz - {entry[3]} - {entry[4]} - {entry[5]} W"
            if query in formatted_entry.lower():
                self.log_listbox.insert(tk.END, formatted_entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = HamRadioLogBook(root)
    root.mainloop()
