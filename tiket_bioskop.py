import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# DATA ARRAY
film = ["Janur Ireng", "KKN di Desa Ayak", "Ambacong"]

jam_tayang = [
    ["10:00", "12:00"], 
    ["11:00", "13:00"], 
    ["12:00", "15:00"]
]

kursi = [
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]], 
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]], 
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]]
]

# TEMA WARNA
BG_MAIN    = "#0a0a0a"   # Background utama : hitam
BG_CARD    = "#161616"   # Background card  : dark gray
BG_HEADER  = "#0f0f0f"   # Background header: near-black
BG_STRUK   = "#111111"   # Background struk

RED        = "#e50914"   # Merah bioskop (Netflix-style)
RED_DARK   = "#9b0610"   # Merah gelap (hover / terpilih)
RED_DIM    = "#3d0408"   # Merah sangat redup (border aktif)

GREEN      = "#1db954"   # Kursi kosong
GREEN_DARK = "#148040"   # Kursi kosong (hover)

WHITE      = "#f0f0f0"
GRAY_LIGHT = "#b0b0b0"
GRAY_MID   = "#666666"
GRAY_DARK  = "#2a2a2a"
GOLD       = "#f5c518"   # Aksen harga / total

# FONT
FONT_BRAND  = ("Georgia",    22, "bold")
FONT_TITLE  = ("Georgia",    18, "bold")
FONT_SUB    = ("Helvetica",  12, "bold")
FONT_BODY   = ("Helvetica",  11)
FONT_SMALL  = ("Helvetica",   9)
FONT_SEAT   = ("Helvetica",  10, "bold")
FONT_MONO   = ("Courier New", 10)
FONT_MONO_B = ("Courier New", 11, "bold")


# HELPER: Step Indicator (dipakai tiap window)
def build_step_indicator(parent, current: int, bg=BG_MAIN):
    steps = ["1. Film", "2. Kursi", "3. Konfirmasi", "4. Struk"]
    frame = tk.Frame(parent, bg=bg)
    frame.pack(fill="x", padx=20, pady=(10, 0))
    for i, s in enumerate(steps):
        active = (i + 1 == current)
        done   = (i + 1 < current)
        if active:
            fg, font = RED, ("Helvetica", 9, "bold")
        elif done:
            fg, font = GRAY_MID, ("Helvetica", 9)
        else:
            fg, font = GRAY_DARK, ("Helvetica", 9)
        tk.Label(frame, text=s, font=font, bg=bg, fg=fg).pack(side="left", padx=6)
        if i < len(steps) - 1:
            tk.Label(frame, text=" › ", font=("Helvetica", 9),
                    bg=bg, fg=GRAY_DARK).pack(side="left")

# HELPER: Separator garis horizontal
def separator(parent, bg=BG_MAIN, color=GRAY_DARK, pady=8):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=pady)


# MAIN APPLICATION CLASS
# Mengatur state global dan navigasi antar window (frame)
class BioskopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎬  CineBook – Sistem Pemesanan Tiket Bioskop")
        self.root.geometry("820x680")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)

        # SESSION STATE
        self.idx_film = -1
        self.idx_jam = -1
        self.selected_kursi = [] # Menyimpan indeks kursi yang diklik (0-8)

        # CONTAINER
        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True)

        # BUILD SEMUA FRAME
        self.frames: dict[str, tk.Frame] = {}
        for Cls in (Window1, Window2, Window3, Window4):
            frame = Cls(container, self)
            self.frames[Cls.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_frame("Window1")

    # NAVIGASI
    def show_frame(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # RESET SESSION (kembali ke awal tanpa menghapus X)
    def reset_session(self):
        self.idx_film = -1
        self.idx_jam = -1
        self.selected_kursi = []


# WINDOW 1 – PEMILIHAN FILM & JAM TAYANG
class Window1(tk.Frame):
    def __init__(self, parent, app: BioskopApp):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.card_frames: list[tk.Frame] = []
        self._build_ui()

    def _build_ui(self):
        # HEADER
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🎬  CINEBOOK", font=FONT_BRAND, bg=BG_HEADER, fg=RED).pack(side="left", padx=22, pady=14)

        build_step_indicator(self, current=1)

        # JUDUL
        tk.Label(self, text="Pilih Film", font=FONT_TITLE, bg=BG_MAIN, fg=WHITE).pack(pady=(14, 2))
        tk.Label(self, text="Klik pada film yang ingin kamu tonton hari ini", font=FONT_SMALL, bg=BG_MAIN, fg=GRAY_MID).pack()

        separator(self, pady=10)

        # DAFTAR FILM
        list_frame = tk.Frame(self, bg=BG_MAIN)
        list_frame.pack(fill="both", expand=True, padx=30)

        self.card_frames = []
        for i in range(len(film)):               
            card = self._build_film_card(list_frame, i)
            card.pack(fill="x", pady=4)
            self.card_frames.append(card)

        separator(self, pady=8)

        # BOTTOM BAR (Termasuk Pilih Jam)
        bottom = tk.Frame(self, bg=BG_MAIN)
        bottom.pack(fill="x", padx=30, pady=(0, 16))

        self.lbl_status = tk.Label(bottom, text="● Belum ada film dipilih", font=FONT_BODY, bg=BG_MAIN, fg=GRAY_MID)
        self.lbl_status.pack(side="left")

        # Container Kanan
        right_frame = tk.Frame(bottom, bg=BG_MAIN)
        right_frame.pack(side="right")

        tk.Label(right_frame, text="Jam Tayang:", bg=BG_MAIN, fg=WHITE, font=FONT_BODY).pack(side="left", padx=5)
        
        self.combo_jam = ttk.Combobox(right_frame, state="disabled", width=10, font=FONT_BODY)
        self.combo_jam.pack(side="left", padx=10)

        self.btn_lanjut = tk.Button(
            right_frame, text="Pilih Kursi  →", font=FONT_SUB,
            bg=GRAY_DARK, fg=GRAY_MID, relief="flat", padx=18, pady=6,
            cursor="arrow", state="disabled", command=self._lanjut)
        self.btn_lanjut.pack(side="left")

    def _build_film_card(self, parent, index: int) -> tk.Frame:
        outer = tk.Frame(parent, bg=BG_CARD, cursor="hand2")
        outer.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        # Nomor urut
        num = tk.Label(outer, text=f"{index + 1:02d}", font=("Georgia", 16, "bold"), bg=BG_CARD, fg=RED_DARK, width=3, anchor="center")
        num.pack(side="left", padx=(12, 0), pady=12)
        num.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        tk.Frame(outer, bg=GRAY_DARK, width=1).pack(side="left", fill="y", padx=10, pady=8)

        info = tk.Frame(outer, bg=BG_CARD)
        info.pack(side="left", fill="both", expand=True, pady=10)
        info.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        lbl_judul = tk.Label(info, text=film[index], font=FONT_SUB, bg=BG_CARD, fg=WHITE, anchor="w")
        lbl_judul.pack(anchor="w")
        lbl_judul.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        lbl_meta = tk.Label(info, text="Genre: Horror / Thriller", font=FONT_SMALL, bg=BG_CARD, fg=GRAY_MID, anchor="w")
        lbl_meta.pack(anchor="w", pady=(2, 0))
        lbl_meta.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        lbl_harga = tk.Label(outer, text="Rp 55.000", font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD)
        lbl_harga.pack(side="right", padx=16)
        lbl_harga.bind("<Button-1>", lambda e, i=index: self._pilih_film(i))

        outer._info_frame  = info
        return outer

    def _pilih_film(self, index: int):
        self.app.idx_film = index

        # Update warna tiap card
        for i, card in enumerate(self.card_frames):
            new_bg = RED_DARK if i == index else BG_CARD
            card.configure(bg=new_bg)
            for child in card.winfo_children():
                try: child.configure(bg=new_bg)
                except: pass
            for lbl in card._info_frame.winfo_children():
                try: lbl.configure(bg=new_bg)
                except: pass

        # Update Jam Tayang Options
        self.combo_jam.configure(state="readonly")
        self.combo_jam['values'] = jam_tayang[index]
        self.combo_jam.current(0)

        # Update status & aktifkan tombol
        self.lbl_status.configure(text=f"● {film[index]}", fg=GREEN)
        self.btn_lanjut.configure(state="normal", bg=RED, fg=WHITE, cursor="hand2")

    def _lanjut(self):
        if self.app.idx_film == -1:
            messagebox.showwarning("Peringatan", "Pilih film terlebih dahulu!")
            return
            
        self.app.idx_jam = self.combo_jam.current()
        if self.app.idx_jam == -1:
            messagebox.showwarning("Peringatan", "Pilih jam tayang terlebih dahulu!")
            return

        self.app.selected_kursi = [] # Bersihkan pilihan kursi saat berpindah ke W2
        self.app.show_frame("Window2")

    def on_show(self):
        self.app.idx_film = -1
        self.lbl_status.configure(text="● Belum ada film dipilih", fg=GRAY_MID)
        self.btn_lanjut.configure(state="disabled", bg=GRAY_DARK, fg=GRAY_MID, cursor="arrow")
        self.combo_jam.set('')
        self.combo_jam.configure(state="disabled")
        
        for card in self.card_frames:
            card.configure(bg=BG_CARD)
            for child in card.winfo_children():
                try: child.configure(bg=BG_CARD)
                except: pass
            for lbl in card._info_frame.winfo_children():
                try: lbl.configure(bg=BG_CARD)
                except: pass


# WINDOW 2 – PEMILIHAN KURSI (GRID DINAMIS ARRAY)
class Window2(tk.Frame):
    def __init__(self, parent, app: BioskopApp):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🎬  CINEBOOK", font=FONT_BRAND, bg=BG_HEADER, fg=RED).pack(side="left", padx=22, pady=14)

        build_step_indicator(self, current=2)

        tk.Label(self, text="Pilih Kursi", font=FONT_TITLE, bg=BG_MAIN, fg=WHITE).pack(pady=(10, 0))
        self.lbl_film_info = tk.Label(self, text="", font=FONT_SMALL, bg=BG_MAIN, fg=GRAY_MID)
        self.lbl_film_info.pack()

        # LAYAR
        screen_wrap = tk.Frame(self, bg=BG_MAIN)
        screen_wrap.pack(pady=(14, 4))
        tk.Frame(screen_wrap, bg=GRAY_MID, width=300, height=6).pack()
        tk.Label(screen_wrap, text="▲   L A Y A R   ▲", font=("Helvetica", 8), bg=BG_MAIN, fg=GRAY_MID).pack()

        # WADAH GRID KURSI
        self.grid_frame = tk.Frame(self, bg=BG_MAIN)
        self.grid_frame.pack(pady=10)

        # LEGENDA
        leg = tk.Frame(self, bg=BG_MAIN)
        leg.pack(pady=8)
        
        for color, label in [(GREEN, "Kosong"), (RED, "Dipilih"), (GRAY_DARK, "Dipesan (X)")]:
            tk.Frame(leg, bg=color, width=18, height=18).pack(side="left", padx=4)
            tk.Label(leg, text=label, font=FONT_SMALL, bg=BG_MAIN, fg=GRAY_LIGHT).pack(side="left", padx=(0, 14))

        separator(self, pady=6)

        self.lbl_tiket = tk.Label(self, text="Kursi dipilih: –    |    Jumlah tiket: 0", font=FONT_SUB, bg=BG_MAIN, fg=WHITE)
        self.lbl_tiket.pack(pady=4)

        btn_row = tk.Frame(self, bg=BG_MAIN)
        btn_row.pack(pady=(6, 16))

        tk.Button(btn_row, text="↩  Kembali", font=FONT_BODY, bg=GRAY_DARK, fg=GRAY_LIGHT, relief="flat", padx=16, pady=9, cursor="hand2", command=self._kembali).pack(side="left", padx=10)
        self.btn_lanjut = tk.Button(btn_row, text="Konfirmasi Pesanan  →", font=FONT_SUB, bg=GRAY_DARK, fg=GRAY_MID, relief="flat", padx=18, pady=9, cursor="arrow", state="disabled", command=self._lanjut)
        self.btn_lanjut.pack(side="left", padx=10)

    def on_show(self):
        f = self.app.idx_film
        j = self.app.idx_jam
        
        # Update Info Title
        self.lbl_film_info.configure(text=f"Film: {film[f]}   |   Jam: {jam_tayang[f][j]}")
        
        # Bersihkan grid lama
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Ambil referensi kursi saat ini (contoh: ["A1", "A2", "X", ...])
        kursi_saat_ini = kursi[f][j]

        # Membuat Grid 3 Baris x 3 Kolom
        for i in range(len(kursi_saat_ini)):
            status = kursi_saat_ini[i]
            r = i // 3  # Menentukan baris (0, 1, atau 2)
            c = i % 3   # Menentukan kolom (0, 1, atau 2)
            
            if status == "X":
                btn = tk.Button(self.grid_frame, text="X", font=FONT_SEAT, width=8, height=2, bg=GRAY_DARK, fg=GRAY_MID, relief="flat", bd=0, state="disabled")
            else:
                btn = tk.Button(self.grid_frame, text=status, font=FONT_SEAT, width=8, height=2, bg=GREEN, fg=WHITE, activebackground=GREEN_DARK, relief="flat", bd=0, cursor="hand2")
                btn.config(command=lambda idx=i, b=btn: self._toggle_seat(idx, b))
                
                # Jika user klik warnai merah
                if i in self.app.selected_kursi:
                    btn.config(bg=RED)
                    
            btn.grid(row=r, column=c, padx=5, pady=5)
            
        self._update_info()

    def _toggle_seat(self, idx: int, btn: tk.Button):
        if idx in self.app.selected_kursi:
            self.app.selected_kursi.remove(idx)
            btn.configure(bg=GREEN, activebackground=GREEN_DARK)
        else:
            self.app.selected_kursi.append(idx)
            btn.configure(bg=RED, activebackground=RED_DARK)
            
        self._update_info()

    def _update_info(self):
        n = len(self.app.selected_kursi)
        f, j = self.app.idx_film, self.app.idx_jam
        
        # Cari nama label aslinya untuk tampilan
        nama_kursi = []
        for idx in self.app.selected_kursi:
            nama_kursi.append(kursi[f][j][idx])
        
        seats_str = ", ".join(nama_kursi) if nama_kursi else "–"
        self.lbl_tiket.configure(text=f"Kursi dipilih: {seats_str}    |    Jumlah tiket: {n}")
        
        if n > 0:
            self.btn_lanjut.configure(state="normal", bg=RED, fg=WHITE, cursor="hand2")
        else:
            self.btn_lanjut.configure(state="disabled", bg=GRAY_DARK, fg=GRAY_MID, cursor="arrow")

    def _kembali(self):
        self.app.show_frame("Window1")

    def _lanjut(self):
        self.app.show_frame("Window3")


#  WINDOW 3 – KONFIRMASI PESANAN
class Window3(tk.Frame):
    def __init__(self, parent, app: BioskopApp):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🎬  CINEBOOK", font=FONT_BRAND, bg=BG_HEADER, fg=RED).pack(side="left", padx=22, pady=14)

        build_step_indicator(self, current=3)

        tk.Label(self, text="Konfirmasi Pesanan", font=FONT_TITLE, bg=BG_MAIN, fg=WHITE).pack(pady=(14, 2))
        tk.Label(self, text="Periksa kembali sebelum melanjutkan", font=FONT_SMALL, bg=BG_MAIN, fg=GRAY_MID).pack()

        card_wrap = tk.Frame(self, bg=RED, padx=2, pady=2)
        card_wrap.pack(padx=80, pady=18, fill="x")

        card = tk.Frame(card_wrap, bg=BG_CARD)
        card.pack(fill="both", expand=True)
        tk.Frame(card, bg=RED, height=4).pack(fill="x")

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="x", padx=30, pady=20)

        self.lbl_film   = self._baris(inner, "🎬  Film",          "–")
        self.lbl_jam    = self._baris(inner, "🕐  Jam Tayang",     "–")
        separator(inner, color=GRAY_DARK, pady=6)
        self.lbl_kursi  = self._baris(inner, "💺  Kursi Dipilih",  "–")
        self.lbl_jumlah = self._baris(inner, "🎟️  Jumlah Tiket",   "–")
        separator(inner, color=GRAY_DARK, pady=6)
        self.lbl_harga  = self._baris(inner, "💰  Harga / Tiket",  "Rp 55.000")
        self.lbl_total  = self._baris(inner, "🏦  TOTAL BAYAR",    "–", fg_val=GOLD, font_val=("Helvetica", 13, "bold"))

        btn_row = tk.Frame(self, bg=BG_MAIN)
        btn_row.pack(pady=16)

        tk.Button(btn_row, text="↩  Kembali Edit", font=FONT_BODY, bg=GRAY_DARK, fg=GRAY_LIGHT, relief="flat", padx=16, pady=10, cursor="hand2", command=self._kembali).pack(side="left", padx=10)
        tk.Button(btn_row, text="✔  Konfirmasi & Cetak Struk", font=FONT_SUB, bg=RED, fg=WHITE, activebackground=RED_DARK, relief="flat", padx=20, pady=10, cursor="hand2", command=self._konfirmasi).pack(side="left", padx=10)

    def _baris(self, parent, label: str, value: str, fg_val=WHITE, font_val=FONT_BODY) -> tk.Label:
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, font=FONT_BODY, bg=BG_CARD, fg=GRAY_MID, width=20, anchor="w").pack(side="left")
        tk.Label(row, text=" : ", font=FONT_BODY, bg=BG_CARD, fg=GRAY_MID).pack(side="left")
        lbl = tk.Label(row, text=value, font=font_val, bg=BG_CARD, fg=fg_val, anchor="w")
        lbl.pack(side="left", padx=4)
        return lbl

    def on_show(self):
        f, j = self.app.idx_film, self.app.idx_jam
        n = len(self.app.selected_kursi)          
        total = n * 55000
        
        nama_kursi = [kursi[f][j][idx] for idx in self.app.selected_kursi]
        seats_str = ", ".join(nama_kursi)

        self.lbl_film.configure(text=film[f])
        self.lbl_jam.configure(text=jam_tayang[f][j])
        self.lbl_kursi.configure(text=seats_str)
        self.lbl_jumlah.configure(text=f"{n} tiket")
        self.lbl_total.configure(text=f"Rp {total:,}".replace(",", "."))

    def _kembali(self):
        self.app.show_frame("Window2")

    def _konfirmasi(self):
        self.app.show_frame("Window4")


#  WINDOW 4 – STRUK & UPDATE ARRAY KURSI GLOBAL
class Window4(tk.Frame):
    def __init__(self, parent, app: BioskopApp):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🎬  CINEBOOK", font=FONT_BRAND, bg=BG_HEADER, fg=RED).pack(side="left", padx=22, pady=14)

        build_step_indicator(self, current=4)

        tk.Label(self, text="✅  Pemesanan Berhasil!", font=FONT_TITLE, bg=BG_MAIN, fg=GREEN).pack(pady=(12, 2))
        tk.Label(self, text="Simpan struk ini sebagai bukti pemesanan tiketmu", font=FONT_SMALL, bg=BG_MAIN, fg=GRAY_MID).pack()

        struk_border = tk.Frame(self, bg=GRAY_DARK, padx=2, pady=2)
        struk_border.pack(padx=100, pady=14, fill="x")

        struk = tk.Frame(struk_border, bg=BG_STRUK)
        struk.pack(fill="both", expand=True)
        tk.Frame(struk, bg=RED, height=6).pack(fill="x")

        tk.Label(struk, text="CINEBOOK CINEMA", font=("Courier New", 14, "bold"), bg=BG_STRUK, fg=WHITE).pack(pady=(14, 0))
        tk.Label(struk, text="Jl. Sudirman No.1, Jakarta Pusat", font=FONT_MONO, bg=BG_STRUK, fg=GRAY_MID).pack()
        tk.Label(struk, text="─" * 42, font=FONT_MONO, bg=BG_STRUK, fg=GRAY_DARK).pack(pady=(6, 0))

        isi = tk.Frame(struk, bg=BG_STRUK)
        isi.pack(padx=24, pady=6, fill="x")

        self.lbl_booking = self._baris_struk(isi, "No. Booking",  "–")
        self.lbl_tgl     = self._baris_struk(isi, "Tanggal",      "–")
        tk.Label(isi, text="─" * 38, font=FONT_MONO, bg=BG_STRUK, fg=GRAY_DARK).pack(pady=2)
        self.lbl_film    = self._baris_struk(isi, "Film",         "–")
        self.lbl_jam     = self._baris_struk(isi, "Jam Tayang",   "–")
        tk.Label(isi, text="─" * 38, font=FONT_MONO, bg=BG_STRUK, fg=GRAY_DARK).pack(pady=2)
        self.lbl_kursi   = self._baris_struk(isi, "Kursi",        "–")
        self.lbl_jumlah  = self._baris_struk(isi, "Jml Tiket",    "–")
        tk.Label(isi, text="─" * 38, font=FONT_MONO, bg=BG_STRUK, fg=GRAY_DARK).pack(pady=2)
        self.lbl_total   = self._baris_struk(isi, "TOTAL",        "–", fg_val=GOLD, bold=True)

        tk.Label(struk, text="─" * 42, font=FONT_MONO, bg=BG_STRUK, fg=GRAY_DARK).pack(pady=(4, 0))
        tk.Label(struk, text="Terima kasih telah memilih CineBook!", font=FONT_MONO, bg=BG_STRUK, fg=GRAY_MID).pack(pady=(4, 0))
        tk.Frame(struk, bg=RED, height=6).pack(fill="x", pady=(10, 0))

        tk.Button(self, text="✔  Selesai – Kembali ke Beranda", font=FONT_SUB, bg=RED, fg=WHITE, activebackground=RED_DARK, relief="flat", padx=24, pady=12, cursor="hand2", command=self._selesai).pack(pady=14)

    def _baris_struk(self, parent, label: str, value: str, fg_val=WHITE, bold=False) -> tk.Label:
        row = tk.Frame(parent, bg=BG_STRUK)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{label:<14}", font=FONT_MONO, bg=BG_STRUK, fg=GRAY_MID, anchor="w").pack(side="left")
        tk.Label(row, text=": ", font=FONT_MONO, bg=BG_STRUK, fg=GRAY_MID).pack(side="left")
        font = FONT_MONO_B if bold else FONT_MONO
        lbl = tk.Label(row, text=value, font=font, bg=BG_STRUK, fg=fg_val, anchor="w")
        lbl.pack(side="left")
        return lbl

    def on_show(self):
        f, j = self.app.idx_film, self.app.idx_jam
        n = len(self.app.selected_kursi)         
        total = n * 55000
        
        # Ambil nama kursi sebelum diubah jadi X
        nama_kursi = [kursi[f][j][idx] for idx in self.app.selected_kursi]
        seats_str  = ", ".join(nama_kursi)   

        # UPDATE ARRAY GLOBAL MENJADI "X"
        for idx in self.app.selected_kursi:
            kursi[f][j][idx] = "X"

        no_booking = f"CB-{random.randint(100000, 999999)}"
        tanggal    = datetime.now().strftime("%d/%m/%Y  %H:%M WIB")

        self.lbl_booking.configure(text=no_booking)
        self.lbl_tgl.configure(text=tanggal)
        self.lbl_film.configure(text=film[f])
        self.lbl_jam.configure(text=jam_tayang[f][j])
        self.lbl_kursi.configure(text=seats_str)
        self.lbl_jumlah.configure(text=f"{n} tiket")
        self.lbl_total.configure(text=f"Rp {total:,}".replace(",", "."))

    def _selesai(self):
        self.app.reset_session()
        self.app.show_frame("Window1")


if __name__ == "__main__":
    root = tk.Tk()
    app  = BioskopApp(root)
    root.mainloop()