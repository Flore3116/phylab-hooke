# ============================================================
# PHYLAB V2
# VIRTUAL LABORATORY HUKUM HOOKE
# Python 3.12.9
#
# CUKUP COPY SEMUA KODE INI -> SIMPAN -> RUN
# Tidak membutuhkan HTML
# Tidak membutuhkan pip install
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import csv
import json
from datetime import datetime


# ============================================================
# WARNA
# ============================================================

BG = "#F4F7FB"
WHITE = "#FFFFFF"
NAVY = "#17324D"
BLUE = "#2878B5"
TEAL = "#168A8A"
GREEN = "#2E8B57"
ORANGE = "#E58A2B"
RED = "#C94C4C"
PURPLE = "#7654A5"
TEXT = "#263746"
MUTED = "#687887"
BORDER = "#D7E1EA"
LIGHT_BLUE = "#EAF4FC"
LIGHT_GREEN = "#EAF7EF"
LIGHT_ORANGE = "#FFF3E5"


# ============================================================
# FONT
# ============================================================

FONT = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_SUB = ("Segoe UI", 14, "bold")
FONT_TITLE = ("Segoe UI", 21, "bold")


# ============================================================
# FUNGSI FISIKA
# ============================================================

def gaya_berat(m, g):
    return m * g


def pertambahan_panjang(m, k, g):
    if k <= 0:
        return 0
    return (m * g) / k


def periode(m, k):
    if m <= 0 or k <= 0:
        return 0
    return 2 * math.pi * math.sqrt(m / k)


# ============================================================
# APLIKASI
# ============================================================

class PhyLab(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("PhyLab - Virtual Laboratory Hukum Hooke")
        self.geometry("1280x800")
        self.minsize(1050, 650)
        self.configure(bg=BG)

        # ----------------------------------------------------
        # DATA IDENTITAS
        # ----------------------------------------------------

        self.nama = tk.StringVar()
        self.kelas = tk.StringVar()
        self.sekolah = tk.StringVar()

        # ----------------------------------------------------
        # DATA SIMULASI
        # ----------------------------------------------------

        self.massa = tk.DoubleVar(value=0.50)
        self.k = tk.DoubleVar(value=100.0)
        self.g = tk.DoubleVar(value=9.8)

        self.L0 = 0.20

        self.simulasi_aktif = False
        self.fase = 0

        # ----------------------------------------------------
        # DATA PERCOBAAN
        # ----------------------------------------------------

        self.data = []

        # ----------------------------------------------------
        # DATA PEMBELAJARAN
        # ----------------------------------------------------

        self.pra_prediksi = ""
        self.jawaban_analisis = []
        self.kesimpulan = ""
        self.refleksi = ""
        self.skor = None

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.halaman_sekarang = "home"
        self.halaman_dikunjungi = set()

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.setup_style()

        # ----------------------------------------------------
        # GUI
        # ----------------------------------------------------

        self.buat_header()
        self.buat_layout()
        self.buat_menu()

        self.tampilkan("home")

        self.after(50, self.animasi)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.keluar
        )


    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=30,
            font=FONT
        )

        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=FONT_BOLD
        )

        style.map(
            "Treeview",
            background=[
                ("selected", LIGHT_BLUE)
            ],
            foreground=[
                ("selected", NAVY)
            ]
        )

        style.configure(
            "TProgressbar",
            troughcolor="#DCE5ED",
            background=GREEN,
            bordercolor="#DCE5ED",
            lightcolor=GREEN,
            darkcolor=GREEN
        )


    # ========================================================
    # HEADER
    # ========================================================

    def buat_header(self):

        header = tk.Frame(
            self,
            bg=NAVY,
            height=78
        )

        header.pack(
            side="top",
            fill="x"
        )

        header.pack_propagate(False)

        kiri = tk.Frame(
            header,
            bg=NAVY
        )

        kiri.pack(
            side="left",
            padx=22,
            pady=8
        )

        tk.Label(
            kiri,
            text="PHYLAB",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 24, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            kiri,
            text="Virtual Laboratory • Konstanta Pegas & Hukum Hooke",
            bg=NAVY,
            fg="#DCEBFA",
            font=FONT_SMALL
        ).pack(
            anchor="w"
        )

        kanan = tk.Frame(
            header,
            bg=NAVY
        )

        kanan.pack(
            side="right",
            padx=25
        )

        self.progress_label = tk.Label(
            kanan,
            text="Progress Belajar: 0%",
            bg=NAVY,
            fg=WHITE,
            font=FONT_BOLD
        )

        self.progress_label.pack()

        self.progress = ttk.Progressbar(
            kanan,
            length=250,
            maximum=100
        )

        self.progress.pack(
            pady=(3, 0)
        )


    # ========================================================
    # LAYOUT UTAMA
    # ========================================================

    def buat_layout(self):

        body = tk.Frame(
            self,
            bg=BG
        )

        body.pack(
            fill="both",
            expand=True
        )

        # SIDEBAR
        self.sidebar = tk.Frame(
            body,
            bg=WHITE,
            width=235
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # AREA KONTEN
        self.content_area = tk.Frame(
            body,
            bg=BG
        )

        self.content_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        # CANVAS KONTEN
        self.content_canvas = tk.Canvas(
            self.content_area,
            bg=BG,
            highlightthickness=0
        )

        self.content_scrollbar = ttk.Scrollbar(
            self.content_area,
            orient="vertical",
            command=self.content_canvas.yview
        )

        self.content_canvas.configure(
            yscrollcommand=self.content_scrollbar.set
        )

        self.content_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.content_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.page_container = tk.Frame(
            self.content_canvas,
            bg=BG
        )

        self.page_window = self.content_canvas.create_window(
            (0, 0),
            window=self.page_container,
            anchor="nw"
        )

        self.page_container.bind(
            "<Configure>",
            self.update_scroll
        )

        self.content_canvas.bind(
            "<Configure>",
            self.resize_page
        )

        self.content_canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )


    def update_scroll(self, event=None):

        self.content_canvas.configure(
            scrollregion=self.content_canvas.bbox("all")
        )


    def resize_page(self, event):

        self.content_canvas.itemconfigure(
            self.page_window,
            width=event.width
        )


    def mouse_scroll(self, event):

        try:
            self.content_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        except:
            pass


    # ========================================================
    # MENU
    # ========================================================

    def buat_menu(self):

        tk.Label(
            self.sidebar,
            text="MENU PEMBELAJARAN",
            bg=WHITE,
            fg=MUTED,
            font=FONT_SMALL
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 8)
        )

        daftar_menu = [
            ("🏠  Beranda", "home"),
            ("🎯  Tujuan Pembelajaran", "tujuan"),
            ("📚  Materi", "materi"),
            ("📝  Pra-Praktikum", "pra"),
            ("🧰  Alat & Bahan", "alat"),
            ("🔬  Simulasi Praktikum", "simulasi"),
            ("📊  Data Percobaan", "data"),
            ("📈  Grafik", "grafik"),
            ("🧠  Analisis", "analisis"),
            ("📝  Kesimpulan", "kesimpulan"),
            ("🎮  Evaluasi", "evaluasi"),
            ("📋  Laporan Praktikum", "laporan"),
            ("📖  Glosarium", "glosarium"),
            ("📚  Referensi", "referensi"),
            ("⭐  Refleksi", "refleksi")
        ]

        self.menu_buttons = {}

        for teks, key in daftar_menu:

            button = tk.Button(
                self.sidebar,
                text=teks,
                command=lambda k=key: self.tampilkan(k),
                bg=WHITE,
                fg=TEXT,
                activebackground=LIGHT_BLUE,
                activeforeground=NAVY,
                relief="flat",
                bd=0,
                anchor="w",
                font=FONT,
                padx=14,
                pady=7,
                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=7,
                pady=1
            )

            self.menu_buttons[key] = button

        tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=18,
            pady=10
        )

        self.button(
            self.sidebar,
            "💾  Simpan Proyek",
            self.simpan_proyek,
            TEAL
        ).pack(
            fill="x",
            padx=12,
            pady=3
        )

        self.button(
            self.sidebar,
            "📂  Buka Proyek",
            self.buka_proyek,
            BLUE
        ).pack(
            fill="x",
            padx=12,
            pady=3
        )


    # ========================================================
    # BUTTON
    # ========================================================

    def button(
        self,
        parent,
        text,
        command,
        color=BLUE
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=FONT_BOLD,
            padx=10,
            pady=7,
            cursor="hand2"
        )


    # ========================================================
    # CARD
    # ========================================================

    def card(
        self,
        parent,
        title,
        subtitle=""
    ):

        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        frame.pack(
            fill="x",
            padx=22,
            pady=8
        )

        tk.Label(
            frame,
            text=title,
            bg=WHITE,
            fg=NAVY,
            font=FONT_SUB
        ).pack(
            anchor="w",
            padx=17,
            pady=(13, 3)
        )

        if subtitle:

            tk.Label(
                frame,
                text=subtitle,
                bg=WHITE,
                fg=MUTED,
                font=FONT_SMALL,
                wraplength=900,
                justify="left"
            ).pack(
                anchor="w",
                padx=17,
                pady=(0, 8)
            )

        return frame


    # ========================================================
    # NAVIGASI
    # ========================================================

    def tampilkan(self, nama):

        # Hapus isi halaman sebelumnya
        for widget in self.page_container.winfo_children():
            widget.destroy()

        self.halaman_sekarang = nama

        self.halaman_dikunjungi.add(nama)

        # Reset scroll ke atas
        self.content_canvas.yview_moveto(0)

        # Pilih builder
        fungsi = {
            "home": self.page_home,
            "tujuan": self.page_tujuan,
            "materi": self.page_materi,
            "pra": self.page_pra,
            "alat": self.page_alat,
            "simulasi": self.page_simulasi,
            "data": self.page_data,
            "grafik": self.page_grafik,
            "analisis": self.page_analisis,
            "kesimpulan": self.page_kesimpulan,
            "evaluasi": self.page_evaluasi,
            "laporan": self.page_laporan,
            "glosarium": self.page_glosarium,
            "referensi": self.page_referensi,
            "refleksi": self.page_refleksi
        }

        fungsi[nama](self.page_container)

        # Warna tombol
        for key, button in self.menu_buttons.items():

            if key == nama:
                button.configure(
                    bg=LIGHT_BLUE,
                    fg=NAVY
                )
            else:
                button.configure(
                    bg=WHITE,
                    fg=TEXT
                )

        progress = int(
            len(self.halaman_dikunjungi) /
            15 *
            100
        )

        self.progress["value"] = progress

        self.progress_label.configure(
            text=f"Progress Belajar: {progress}%"
        )

        self.after(
            50,
            self.update_scroll
        )


    # ========================================================
    # JUDUL HALAMAN
    # ========================================================

    def page_title(
        self,
        parent,
        title,
        subtitle
    ):

        tk.Label(
            parent,
            text=title,
            bg=BG,
            fg=NAVY,
            font=FONT_TITLE
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 2)
        )

        tk.Label(
            parent,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=FONT
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 12)
        )


    # ========================================================
    # BERANDA
    # ========================================================

    def page_home(self, p):

        hero = tk.Frame(
            p,
            bg=NAVY
        )

        hero.pack(
            fill="x",
            padx=22,
            pady=22
        )

        tk.Label(
            hero,
            text="PHYLAB",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 34, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 2)
        )

        tk.Label(
            hero,
            text="Virtual Laboratory Hukum Hooke",
            bg=NAVY,
            fg="#D9ECFF",
            font=("Segoe UI", 17)
        ).pack(
            anchor="w",
            padx=25
        )

        tk.Label(
            hero,
            text=(
                "Laboratorium virtual untuk memahami hubungan "
                "gaya, pertambahan panjang, dan konstanta pegas "
                "melalui eksperimen interaktif."
            ),
            bg=NAVY,
            fg=WHITE,
            font=FONT,
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=12
        )

        self.button(
            hero,
            "🚀 MULAI BELAJAR",
            lambda: self.tampilkan("tujuan"),
            TEAL
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 23)
        )

        identitas = self.card(
            p,
            "👤 Identitas Siswa",
            "Isi identitas untuk digunakan pada laporan praktikum."
        )

        identitas.grid_columnconfigure(
            0,
            weight=1
        )
        identitas.grid_columnconfigure(
            1,
            weight=1
        )
        identitas.grid_columnconfigure(
            2,
            weight=1
        )

        data_identitas = [
            ("Nama", self.nama),
            ("Kelas", self.kelas),
            ("Sekolah", self.sekolah)
        ]

        for i, (label, variable) in enumerate(data_identitas):

            box = tk.Frame(
                identitas,
                bg=WHITE
            )

            box.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=8,
                pady=10
            )

            tk.Label(
                box,
                text=label,
                bg=WHITE,
                fg=MUTED,
                font=FONT_SMALL
            ).pack(
                anchor="w"
            )

            tk.Entry(
                box,
                textvariable=variable,
                font=FONT,
                relief="solid",
                bd=1
            ).pack(
                fill="x",
                pady=4
            )

        info = self.card(
            p,
            "🔬 Apa itu PhyLab?"
        )

        tk.Label(
            info,
            text=(
                "PhyLab mensimulasikan percobaan pegas sehingga "
                "siswa dapat mengubah massa, konstanta pegas, "
                "dan gravitasi. Hasil eksperimen kemudian dapat "
                "dicatat dalam tabel, divisualisasikan melalui "
                "grafik, dianalisis, dan digunakan untuk membuat "
                "laporan praktikum."
            ),
            bg=WHITE,
            fg=TEXT,
            font=FONT,
            wraplength=950,
            justify="left"
        ).pack(
            fill="x",
            padx=17,
            pady=10
        )

        fitur = self.card(
            p,
            "✨ Fitur PhyLab"
        )

        daftar = [
            ("🔬", "Simulasi"),
            ("📊", "Data"),
            ("📈", "Grafik"),
            ("🧠", "Analisis"),
            ("🎮", "Evaluasi"),
            ("📋", "Laporan")
        ]

        baris = tk.Frame(
            fitur,
            bg=WHITE
        )

        baris.pack(
            fill="x",
            padx=12,
            pady=10
        )

        for icon, teks in daftar:

            box = tk.Frame(
                baris,
                bg=LIGHT_BLUE
            )

            box.pack(
                side="left",
                fill="x",
                expand=True,
                padx=4
            )

            tk.Label(
                box,
                text=icon,
                bg=LIGHT_BLUE,
                font=("Segoe UI", 22)
            ).pack(
                pady=(9, 3)
            )

            tk.Label(
                box,
                text=teks,
                bg=LIGHT_BLUE,
                fg=NAVY,
                font=FONT_BOLD
            ).pack(
                pady=(0, 10)
            )


    # ========================================================
    # TUJUAN
    # ========================================================

    def page_tujuan(self, p):

        self.page_title(
            p,
            "🎯 Tujuan Pembelajaran",
            "Kemampuan yang diharapkan setelah menyelesaikan PhyLab."
        )

        f = self.card(
            p,
            "Tujuan Pembelajaran"
        )

        tujuan = [
            "Menjelaskan konsep elastisitas.",
            "Menjelaskan Hukum Hooke.",
            "Menjelaskan makna konstanta pegas.",
            "Mengidentifikasi besaran F, m, g, k, dan Δx.",
            "Melakukan percobaan virtual Hukum Hooke.",
            "Mengumpulkan dan mengolah data percobaan.",
            "Membuat grafik F terhadap Δx.",
            "Menentukan nilai konstanta pegas.",
            "Menganalisis hubungan gaya dan pertambahan panjang.",
            "Menarik kesimpulan berdasarkan hasil percobaan."
        ]

        for i, teks in enumerate(tujuan, 1):

            tk.Label(
                f,
                text=f"{i}. {teks}",
                bg=WHITE,
                fg=TEXT,
                font=FONT
            ).pack(
                anchor="w",
                padx=17,
                pady=4
            )

        f2 = self.card(
            p,
            "✅ Indikator Keberhasilan"
        )

        indikator = [
            "Memahami konsep Hukum Hooke.",
            "Mampu menggunakan persamaan F = kΔx.",
            "Mampu menentukan konstanta pegas.",
            "Mampu membaca grafik F terhadap Δx.",
            "Mampu menjelaskan hasil eksperimen."
        ]

        for teks in indikator:

            tk.Label(
                f2,
                text="☐ " + teks,
                bg=WHITE,
                fg=TEXT,
                font=FONT
            ).pack(
                anchor="w",
                padx=17,
                pady=4
            )


    # ========================================================
    # MATERI
    # ========================================================

    def page_materi(self, p):

        self.page_title(
            p,
            "📚 Materi",
            "Konsep dasar elastisitas dan Hukum Hooke."
        )

        materi = [
            (
                "1. Elastisitas",
                "Elastisitas adalah kemampuan suatu benda "
                "untuk kembali ke bentuk atau ukuran semula "
                "setelah gaya yang bekerja dihilangkan, "
                "selama belum melewati batas elastis."
            ),
            (
                "2. Pegas",
                "Pegas merupakan contoh benda elastis. "
                "Ketika diberi gaya, pegas mengalami perubahan panjang."
            ),
            (
                "3. Hukum Hooke",
                "Pada daerah elastis, gaya yang diberikan "
                "kepada pegas berbanding lurus dengan "
                "pertambahan panjang pegas."
            ),
            (
                "4. Konstanta Pegas",
                "Konstanta pegas atau k menunjukkan tingkat "
                "kekakuan suatu pegas. Nilai k yang besar "
                "menunjukkan pegas yang lebih sulit diregangkan."
            )
        ]

        for judul, isi in materi:

            f = self.card(
                p,
                judul
            )

            tk.Label(
                f,
                text=isi,
                bg=WHITE,
                fg=TEXT,
                font=FONT,
                wraplength=950,
                justify="left"
            ).pack(
                fill="x",
                padx=17,
                pady=9
            )

        rumus = self.card(
            p,
            "📐 Persamaan Penting"
        )

        tk.Label(
            rumus,
            text="F = k × Δx",
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=("Cambria Math", 28, "bold")
        ).pack(
            fill="x",
            padx=17,
            pady=12
        )

        tk.Label(
            rumus,
            text=(
                "k = F / Δx\n"
                "Δx = F / k\n"
                "Δx = L − L₀\n"
                "F = mg"
            ),
            bg=WHITE,
            fg=PURPLE,
            font=("Cambria Math", 18, "bold"),
            justify="left"
        ).pack(
            anchor="w",
            padx=30,
            pady=8
        )

        periode_box = self.card(
            p,
            "⏱ Periode Getaran Pegas"
        )

        tk.Label(
            periode_box,
            text="T = 2π √(m/k)",
            bg=WHITE,
            fg=PURPLE,
            font=("Cambria Math", 25, "bold")
        ).pack(
            pady=10
        )

        contoh = self.card(
            p,
            "🧮 Contoh Perhitungan"
        )

        tk.Label(
            contoh,
            text=(
                "Diketahui:\n"
                "m = 0,5 kg\n"
                "k = 100 N/m\n"
                "g = 9,8 m/s²\n\n"
                "F = mg\n"
                "F = 0,5 × 9,8 = 4,9 N\n\n"
                "Δx = F/k\n"
                "Δx = 4,9/100\n"
                "Δx = 0,049 m = 4,9 cm"
            ),
            bg=WHITE,
            fg=TEXT,
            font=FONT,
            justify="left"
        ).pack(
            anchor="w",
            padx=17,
            pady=10
        )


    # ========================================================
    # PRA PRAKTIKUM
    # ========================================================

    def page_pra(self, p):

        self.page_title(
            p,
            "📝 Pra-Praktikum",
            "Buat prediksi sebelum melakukan eksperimen."
        )

        f = self.card(
            p,
            "Pertanyaan Prediksi"
        )

        pertanyaan = [
            "1. Apa yang terjadi jika massa beban diperbesar?",
            "2. Apa yang terjadi pada Δx jika konstanta pegas diperbesar?",
            "3. Bagaimana hubungan gaya dengan pertambahan panjang?"
        ]

        for teks in pertanyaan:

            tk.Label(
                f,
                text=teks,
                bg=WHITE,
                fg=NAVY,
                font=FONT_BOLD
            ).pack(
                anchor="w",
                padx=17,
                pady=6
            )

        tk.Label(
            f,
            text="💭 Tuliskan prediksimu:",
            bg=WHITE,
            fg=NAVY,
            font=FONT_BOLD
        ).pack(
            anchor="w",
            padx=17,
            pady=(15, 5)
        )

        self.pra_text = tk.Text(
            f,
            height=8,
            font=FONT,
            wrap="word"
        )

        self.pra_text.pack(
            fill="x",
            padx=17
        )

        if self.pra_prediksi:
            self.pra_text.insert(
                "1.0",
                self.pra_prediksi
            )

        self.button(
            f,
            "💾 Simpan Prediksi",
            self.simpan_pra,
            TEAL
        ).pack(
            anchor="w",
            padx=17,
            pady=12
        )


    def simpan_pra(self):

        self.pra_prediksi = self.pra_text.get(
            "1.0",
            "end"
        ).strip()

        messagebox.showinfo(
            "Berhasil",
            "Prediksi pra-praktikum berhasil disimpan."
        )


    # ========================================================
    # ALAT
    # ========================================================

    def page_alat(self, p):

        self.page_title(
            p,
            "🧰 Alat & Bahan Virtual",
            "Komponen yang digunakan dalam laboratorium virtual."
        )

        f = self.card(
            p,
            "Peralatan"
        )

        alat = [
            ("🌀", "Pegas", "Pegas sebagai objek elastis."),
            ("⚖", "Beban", "Beban menghasilkan gaya berat."),
            ("🧱", "Statif", "Menahan posisi pegas."),
            ("📏", "Penggaris", "Mengukur panjang pegas."),
            ("📍", "Indikator Δx", "Menunjukkan pertambahan panjang.")
        ]

        for icon, nama, deskripsi in alat:

            row = tk.Frame(
                f,
                bg=LIGHT_BLUE
            )

            row.pack(
                fill="x",
                padx=17,
                pady=4
            )

            tk.Label(
                row,
                text=icon,
                bg=LIGHT_BLUE,
                font=("Segoe UI", 24)
            ).pack(
                side="left",
                padx=15,
                pady=8
            )

            bagian = tk.Frame(
                row,
                bg=LIGHT_BLUE
            )

            bagian.pack(
                side="left",
                fill="x",
                expand=True
            )

            tk.Label(
                bagian,
                text=nama,
                bg=LIGHT_BLUE,
                fg=NAVY,
                font=FONT_BOLD
            ).pack(
                anchor="w",
                pady=(8, 2)
            )

            tk.Label(
                bagian,
                text=deskripsi,
                bg=LIGHT_BLUE,
                fg=TEXT,
                font=FONT_SMALL
            ).pack(
                anchor="w",
                pady=(0, 8)
            )


    # ========================================================
    # SIMULASI
    # ========================================================

    def page_simulasi(self, p):

        self.page_title(
            p,
            "🔬 Simulasi Praktikum",
            "Atur parameter dan amati perubahan sistem massa–pegas."
        )

        main = tk.Frame(
            p,
            bg=BG
        )

        main.pack(
            fill="x",
            padx=18
        )

        # KIRI
        visual = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        visual.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(4, 7)
        )

        tk.Label(
            visual,
            text="Visualisasi Pegas",
            bg=WHITE,
            fg=NAVY,
            font=FONT_SUB
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        self.sim_canvas = tk.Canvas(
            visual,
            bg="#F9FCFF",
            height=500,
            highlightthickness=0
        )

        self.sim_canvas.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # KANAN
        control = tk.Frame(
            main,
            bg=WHITE,
            width=350,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        control.pack(
            side="right",
            fill="y",
            padx=(7, 4)
        )

        control.pack_propagate(False)

        tk.Label(
            control,
            text="⚙ Kontrol",
            bg=WHITE,
            fg=NAVY,
            font=FONT_SUB
        ).pack(
            anchor="w",
            padx=15,
            pady=13
        )

        self.slider(
            control,
            "Massa (kg)",
            self.massa,
            0.1,
            2.0,
            0.05
        )

        self.slider(
            control,
            "Konstanta k (N/m)",
            self.k,
            20,
            200,
            5
        )

        self.slider(
            control,
            "Gravitasi (m/s²)",
            self.g,
            8,
            10,
            0.1
        )

        buttons = tk.Frame(
            control,
            bg=WHITE
        )

        buttons.pack(
            fill="x",
            padx=12,
            pady=12
        )

        self.button(
            buttons,
            "▶ Mulai",
            self.mulai,
            GREEN
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        self.button(
            buttons,
            "⏸ Pause",
            self.pause,
            ORANGE
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        self.button(
            buttons,
            "↻ Reset",
            self.reset,
            RED
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        self.status = tk.Label(
            control,
            text="Status: siap melakukan percobaan.",
            bg=WHITE,
            fg=MUTED,
            font=FONT_SMALL,
            wraplength=310,
            justify="left"
        )

        self.status.pack(
            fill="x",
            padx=15
        )

        hasil = tk.Frame(
            control,
            bg=LIGHT_BLUE
        )

        hasil.pack(
            fill="x",
            padx=15,
            pady=12
        )

        tk.Label(
            hasil,
            text="HASIL REAL-TIME",
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT_BOLD
        ).pack(
            anchor="w",
            padx=10,
            pady=7
        )

        self.hasil_F = tk.Label(
            hasil,
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT_BOLD
        )

        self.hasil_dx = tk.Label(
            hasil,
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT_BOLD
        )

        self.hasil_T = tk.Label(
            hasil,
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT_BOLD
        )

        self.hasil_L = tk.Label(
            hasil,
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT_BOLD
        )

        for label in [
            self.hasil_F,
            self.hasil_dx,
            self.hasil_T,
            self.hasil_L
        ]:
            label.pack(
                anchor="w",
                padx=10,
                pady=2
            )

        self.button(
            control,
            "📏 Ukur & Tambahkan Data",
            self.tambah_data_simulasi,
            BLUE
        ).pack(
            fill="x",
            padx=15,
            pady=8
        )

        tk.Label(
            control,
            text=(
                "Gunakan beberapa nilai massa untuk mendapatkan "
                "beberapa titik data pada grafik F terhadap Δx."
            ),
            bg=WHITE,
            fg=MUTED,
            font=FONT_SMALL,
            wraplength=310,
            justify="left"
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.gambar_simulasi()


    def slider(
        self,
        parent,
        nama,
        variable,
        minimum,
        maksimum,
        resolution
    ):

        box = tk.Frame(
            parent,
            bg=WHITE
        )

        box.pack(
            fill="x",
            padx=15,
            pady=5
        )

        atas = tk.Frame(
            box,
            bg=WHITE
        )

        atas.pack(
            fill="x"
        )

        tk.Label(
            atas,
            text=nama,
            bg=WHITE,
            fg=TEXT,
            font=FONT_SMALL
        ).pack(
            side="left"
        )

        tk.Label(
            atas,
            textvariable=variable,
            bg=WHITE,
            fg=BLUE,
            font=FONT_BOLD
        ).pack(
            side="right"
        )

        tk.Scale(
            box,
            from_=minimum,
            to=maksimum,
            resolution=resolution,
            orient="horizontal",
            variable=variable,
            showvalue=False,
            bg=WHITE,
            highlightthickness=0,
            troughcolor="#DCEAF5",
            activebackground=BLUE,
            command=lambda value: self.gambar_simulasi()
        ).pack(
            fill="x"
        )


    def mulai(self):

        self.simulasi_aktif = True

        if hasattr(self, "status"):
            self.status.configure(
                text="Status: simulasi sedang berjalan."
            )


    def pause(self):

        self.simulasi_aktif = False

        if hasattr(self, "status"):
            self.status.configure(
                text="Status: simulasi dijeda."
            )


    def reset(self):

        self.simulasi_aktif = False
        self.fase = 0

        self.massa.set(0.50)
        self.k.set(100)
        self.g.set(9.8)

        if hasattr(self, "status"):
            self.status.configure(
                text="Status: parameter dikembalikan ke nilai awal."
            )

        self.gambar_simulasi()


    def animasi(self):

        if self.simulasi_aktif:

            self.fase += (
                0.08 *
                math.sqrt(
                    self.k.get() /
                    max(self.massa.get(), 0.01)
                )
            )

        if hasattr(
            self,
            "sim_canvas"
        ):

            self.gambar_simulasi()

        self.after(
            40,
            self.animasi
        )


    def gambar_simulasi(self):

        if not hasattr(
            self,
            "sim_canvas"
        ):
            return

        canvas = self.sim_canvas

        canvas.delete("all")

        width = max(
            canvas.winfo_width(),
            650
        )

        height = max(
            canvas.winfo_height(),
            480
        )

        m = max(
            self.massa.get(),
            0.01
        )

        k = max(
            self.k.get(),
            1
        )

        g = max(
            self.g.get(),
            0.01
        )

        F = gaya_berat(
            m,
            g
        )

        dx = pertambahan_panjang(
            m,
            k,
            g
        )

        T = periode(
            m,
            k
        )

        x = width * 0.43

        posisi_awal = 155

        posisi_setimbang = (
            posisi_awal +
            min(
                dx * 750,
                height - 250
            )
        )

        getaran = 0

        if self.simulasi_aktif:

            getaran = (
                18 *
                math.sin(self.fase)
            )

        posisi_beban = (
            posisi_setimbang +
            getaran
        )

        # Judul
        canvas.create_text(
            width / 2,
            25,
            text="Sistem Massa–Pegas",
            fill=NAVY,
            font=FONT_SUB
        )

        # Statif
        canvas.create_rectangle(
            x - 22,
            65,
            x + 22,
            height - 50,
            fill="#AEBBC7",
            outline="#6F7D89"
        )

        canvas.create_polygon(
            x - 85,
            height - 50,
            x + 85,
            height - 50,
            x + 65,
            height - 22,
            x - 65,
            height - 22,
            fill="#8A98A5",
            outline="#65727D"
        )

        # Pegas
        atas = 100
        bawah = posisi_beban - 25

        if bawah < atas + 40:
            bawah = atas + 40

        titik = [
            (x, atas)
        ]

        jumlah = max(
            8,
            int((bawah - atas) / 13)
        )

        for i in range(
            1,
            jumlah + 1
        ):

            y = (
                atas +
                (bawah - atas) *
                i /
                jumlah
            )

            if i % 2:
                xx = x + 20
            else:
                xx = x - 20

            titik.append(
                (xx, y)
            )

        titik.append(
            (x, bawah)
        )

        koordinat = []

        for xx, yy in titik:
            koordinat.extend(
                [xx, yy]
            )

        canvas.create_line(
            *koordinat,
            fill=PURPLE,
            width=3,
            smooth=True
        )

        # Beban
        canvas.create_rectangle(
            x - 48,
            posisi_beban,
            x + 48,
            posisi_beban + 60,
            fill=BLUE,
            outline=NAVY,
            width=2
        )

        canvas.create_text(
            x,
            posisi_beban + 30,
            text=f"{m:.2f} kg",
            fill=WHITE,
            font=FONT_BOLD
        )

        # Garis L0
        canvas.create_line(
            x - 160,
            posisi_awal,
            x + 160,
            posisi_awal,
            fill=ORANGE,
            dash=(7, 4),
            width=2
        )

        canvas.create_text(
            x + 180,
            posisi_awal,
            text="L₀",
            fill=ORANGE,
            font=FONT_BOLD
        )

        # Garis kesetimbangan
        canvas.create_line(
            x - 160,
            posisi_setimbang,
            x + 160,
            posisi_setimbang,
            fill=TEAL,
            dash=(7, 4),
            width=2
        )

        canvas.create_text(
            x + 180,
            posisi_setimbang,
            text="Posisi setimbang",
            fill=TEAL,
            font=FONT_SMALL
        )

        # Panah Δx
        arrow_x = x - 125

        canvas.create_line(
            arrow_x,
            posisi_awal,
            arrow_x,
            posisi_setimbang,
            fill=RED,
            width=3,
            arrow=tk.LAST
        )

        canvas.create_text(
            arrow_x - 38,
            (posisi_awal + posisi_setimbang) / 2,
            text=f"Δx\n{dx:.3f} m",
            fill=RED,
            font=("Segoe UI", 9, "bold")
        )

        # Penggaris
        ruler_x = x + 235

        canvas.create_rectangle(
            ruler_x,
            90,
            ruler_x + 38,
            height - 70,
            fill="#F6D98B",
            outline="#A88437"
        )

        for i in range(10):

            yy = 90 + i * 40

            panjang = 28 if i % 5 == 0 else 15

            canvas.create_line(
                ruler_x,
                yy,
                ruler_x + panjang,
                yy,
                fill="#725A24"
            )

        # Hasil
        if hasattr(self, "hasil_F"):

            self.hasil_F.configure(
                text=f"F = {F:.3f} N"
            )

            self.hasil_dx.configure(
                text=f"Δx = {dx:.4f} m"
            )

            self.hasil_T.configure(
                text=f"T = {T:.3f} s"
            )

            self.hasil_L.configure(
                text=f"L akhir = {self.L0 + dx:.4f} m"
            )


    def tambah_data_simulasi(self):

        m = self.massa.get()
        k = self.k.get()
        g = self.g.get()

        F = gaya_berat(
            m,
            g
        )

        dx = pertambahan_panjang(
            m,
            k,
            g
        )

        L = self.L0 + dx

        nilai_k = (
            F / dx
            if dx != 0
            else 0
        )

        self.data.append({
            "massa": m,
            "gaya": F,
            "L0": self.L0,
            "L": L,
            "dx": dx,
            "k": nilai_k
        })

        if hasattr(self, "status"):

            self.status.configure(
                text=(
                    f"Data ditambahkan: "
                    f"m = {m:.2f} kg | "
                    f"F = {F:.2f} N | "
                    f"Δx = {dx:.4f} m"
                )
            )

        messagebox.showinfo(
            "Data Percobaan",
            "Data berhasil ditambahkan ke tabel."
        )


    # ========================================================
    # DATA
    # ========================================================

    def page_data(self, p):

        self.page_title(
            p,
            "📊 Data Percobaan",
            "Tabel hasil eksperimen virtual."
        )

        f = self.card(
            p,
            "Tabel Pengamatan"
        )

        self.tree = ttk.Treeview(
            f,
            columns=(
                "no",
                "m",
                "F",
                "L0",
                "L",
                "dx",
                "k"
            ),
            show="headings",
            height=14
        )

        kolom = [
            ("no", "No", 55),
            ("m", "m (kg)", 100),
            ("F", "F (N)", 100),
            ("L0", "L₀ (m)", 100),
            ("L", "L (m)", 100),
            ("dx", "Δx (m)", 110),
            ("k", "k (N/m)", 110)
        ]

        for key, judul, width in kolom:

            self.tree.heading(
                key,
                text=judul
            )

            self.tree.column(
                key,
                width=width,
                anchor="center"
            )

        self.tree.pack(
            fill="x",
            padx=17,
            pady=12
        )

        buttons = tk.Frame(
            f,
            bg=WHITE
        )

        buttons.pack(
            fill="x",
            padx=17,
            pady=5
        )

        self.button(
            buttons,
            "＋ Tambah Data",
            self.tambah_data_dari_simulasi,
            GREEN
        ).pack(
            side="left",
            padx=2
        )

        self.button(
            buttons,
            "🗑 Hapus",
            self.hapus_data,
            RED
        ).pack(
            side="left",
            padx=2
        )

        self.button(
            buttons,
            "↻ Hapus Semua",
            self.hapus_semua,
            ORANGE
        ).pack(
            side="left",
            padx=2
        )

        self.button(
            buttons,
            "💾 Ekspor CSV",
            self.ekspor_csv,
            TEAL
        ).pack(
            side="left",
            padx=2
        )

        self.label_ringkasan_data = tk.Label(
            f,
            text="",
            bg=WHITE,
            fg=NAVY,
            font=FONT_BOLD
        )

        self.label_ringkasan_data.pack(
            anchor="w",
            padx=17,
            pady=10
        )

        self.update_table()


    def tambah_data_dari_simulasi(self):

        self.tampilkan("simulasi")

        messagebox.showinfo(
            "Petunjuk",
            "Atur massa/k/gravitasi pada simulasi, kemudian "
            "tekan tombol 'Ukur & Tambahkan Data'."
        )


    def update_table(self):

        if not hasattr(
            self,
            "tree"
        ):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, d in enumerate(
            self.data,
            1
        ):

            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    f"{d['massa']:.3f}",
                    f"{d['gaya']:.3f}",
                    f"{d['L0']:.3f}",
                    f"{d['L']:.3f}",
                    f"{d['dx']:.4f}",
                    f"{d['k']:.2f}"
                )
            )

        if self.data:

            rata = sum(
                d["k"]
                for d in self.data
            ) / len(self.data)

            self.label_ringkasan_data.configure(
                text=(
                    f"Jumlah data = {len(self.data)}   |   "
                    f"Rata-rata k = {rata:.2f} N/m"
                )
            )

        else:

            self.label_ringkasan_data.configure(
                text="Belum ada data percobaan."
            )


    def hapus_data(self):

        pilihan = self.tree.selection()

        if not pilihan:

            messagebox.showwarning(
                "Data",
                "Pilih baris data terlebih dahulu."
            )

            return

        indeks = []

        for item in pilihan:

            values = self.tree.item(
                item,
                "values"
            )

            indeks.append(
                int(values[0]) - 1
            )

        for i in sorted(
            indeks,
            reverse=True
        ):

            if 0 <= i < len(self.data):
                del self.data[i]

        self.update_table()


    def hapus_semua(self):

        if not self.data:
            return

        if messagebox.askyesno(
            "Konfirmasi",
            "Hapus semua data percobaan?"
        ):

            self.data.clear()

            self.update_table()


    def ekspor_csv(self):

        if not self.data:

            messagebox.showwarning(
                "Ekspor",
                "Belum ada data."
            )

            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV", "*.csv")
            ]
        )

        if not path:
            return

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "No",
                "Massa (kg)",
                "Gaya (N)",
                "L0 (m)",
                "L (m)",
                "Delta x (m)",
                "k (N/m)"
            ])

            for i, d in enumerate(
                self.data,
                1
            ):

                writer.writerow([
                    i,
                    d["massa"],
                    d["gaya"],
                    d["L0"],
                    d["L"],
                    d["dx"],
                    d["k"]
                ])

        messagebox.showinfo(
            "Berhasil",
            "Data berhasil diekspor ke CSV."
        )


    # ========================================================
    # GRAFIK
    # ========================================================

    def page_grafik(self, p):

        self.page_title(
            p,
            "📈 Grafik",
            "Hubungan gaya (F) dengan pertambahan panjang (Δx)."
        )

        f = self.card(
            p,
            "Grafik F terhadap Δx"
        )

        self.graph_canvas = tk.Canvas(
            f,
            bg=WHITE,
            height=500,
            highlightthickness=0
        )

        self.graph_canvas.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.graph_info = tk.Label(
            f,
            text="",
            bg=WHITE,
            fg=NAVY,
            font=FONT,
            justify="left"
        )

        self.graph_info.pack(
            anchor="w",
            padx=17,
            pady=8
        )

        self.button(
            f,
            "↻ Perbarui Grafik",
            self.gambar_grafik,
            BLUE
        ).pack(
            anchor="w",
            padx=17,
            pady=8
        )

        self.gambar_grafik()


    def gambar_grafik(self):

        if not hasattr(
            self,
            "graph_canvas"
        ):
            return

        canvas = self.graph_canvas

        canvas.delete("all")

        width = max(
            canvas.winfo_width(),
            850
        )

        left = 80
        right = width - 45
        top = 55
        bottom = 420

        canvas.create_line(
            left,
            bottom,
            right,
            bottom,
            fill=TEXT,
            width=2
        )

        canvas.create_line(
            left,
            bottom,
            left,
            top,
            fill=TEXT,
            width=2
        )

        canvas.create_text(
            (left + right) / 2,
            470,
            text="Δx (m)",
            fill=TEXT,
            font=FONT_BOLD
        )

        canvas.create_text(
            20,
            (top + bottom) / 2,
            text="F (N)",
            fill=TEXT,
            font=FONT_BOLD,
            angle=90
        )

        if not self.data:

            canvas.create_text(
                width / 2,
                240,
                text=(
                    "Belum ada data.\n\n"
                    "Lakukan percobaan pada menu Simulasi Praktikum."
                ),
                fill=MUTED,
                font=FONT_BOLD,
                justify="center"
            )

            self.graph_info.configure(
                text="Belum ada data untuk ditampilkan."
            )

            return

        xs = [
            d["dx"]
            for d in self.data
        ]

        ys = [
            d["gaya"]
            for d in self.data
        ]

        xmax = max(xs) * 1.2
        ymax = max(ys) * 1.2

        if xmax <= 0:
            xmax = 1

        if ymax <= 0:
            ymax = 1

        # Grid
        for i in range(1, 6):

            x = (
                left +
                (right - left) *
                i / 6
            )

            y = (
                bottom -
                (bottom - top) *
                i / 6
            )

            canvas.create_line(
                x,
                top,
                x,
                bottom,
                fill="#E3EAF0",
                dash=(3, 4)
            )

            canvas.create_line(
                left,
                y,
                right,
                y,
                fill="#E3EAF0",
                dash=(3, 4)
            )

            canvas.create_text(
                x,
                bottom + 16,
                text=f"{xmax*i/6:.3f}",
                fill=MUTED,
                font=("Segoe UI", 8)
            )

            canvas.create_text(
                left - 30,
                y,
                text=f"{ymax*i/6:.2f}",
                fill=MUTED,
                font=("Segoe UI", 8)
            )

        # Gradien melalui titik nol
        penyebut = sum(
            x*x
            for x in xs
        )

        if penyebut != 0:

            gradien = sum(
                x*y
                for x, y in zip(xs, ys)
            ) / penyebut

        else:

            gradien = 0

        # Garis tren
        y_end = gradien * xmax

        py = (
            bottom -
            y_end / ymax *
            (bottom - top)
        )

        canvas.create_line(
            left,
            bottom,
            right,
            py,
            fill=RED,
            width=2,
            dash=(8, 4)
        )

        # Titik
        for x, y in zip(xs, ys):

            px = (
                left +
                x / xmax *
                (right - left)
            )

            py_data = (
                bottom -
                y / ymax *
                (bottom - top)
            )

            canvas.create_oval(
                px - 6,
                py_data - 6,
                px + 6,
                py_data + 6,
                fill=BLUE,
                outline=NAVY
            )

        rata = sum(
            d["k"]
            for d in self.data
        ) / len(self.data)

        self.graph_info.configure(
            text=(
                f"Jumlah data = {len(self.data)}\n"
                f"Gradien grafik = {gradien:.2f} N/m\n"
                f"Rata-rata k = {rata:.2f} N/m\n\n"
                "Pada persamaan F = kΔx, gradien grafik "
                "F terhadap Δx secara fisik merepresentasikan "
                "konstanta pegas k."
            )
        )


    # ========================================================
    # ANALISIS
    # ========================================================

    def page_analisis(self, p):

        self.page_title(
            p,
            "🧠 Analisis",
            "Gunakan data dan grafik untuk menjawab pertanyaan."
        )

        f = self.card(
            p,
            "Pertanyaan Analisis"
        )

        questions = [
            "1. Bagaimana hubungan antara gaya dengan pertambahan panjang?",
            "2. Apakah grafik F terhadap Δx cenderung linear?",
            "3. Apakah nilai k dari setiap percobaan relatif konsisten?",
            "4. Apa makna gradien grafik F terhadap Δx?",
            "5. Bagaimana pengaruh massa terhadap pertambahan panjang?",
            "6. Apakah hasil percobaan mendukung Hukum Hooke?"
        ]

        self.analysis_boxes = []

        for question in questions:

            tk.Label(
                f,
                text=question,
                bg=WHITE,
                fg=NAVY,
                font=FONT_BOLD
            ).pack(
                anchor="w",
                padx=17,
                pady=(8, 3)
            )

            box = tk.Text(
                f,
                height=3,
                font=FONT,
                wrap="word"
            )

            box.pack(
                fill="x",
                padx=17,
                pady=(0, 6)
            )

            self.analysis_boxes.append(box)

        # Masukkan jawaban lama
        for i, jawaban in enumerate(
            self.jawaban_analisis
        ):

            if i < len(self.analysis_boxes):

                self.analysis_boxes[i].insert(
                    "1.0",
                    jawaban
                )

        self.button(
            f,
            "💾 Simpan Analisis",
            self.simpan_analisis,
            TEAL
        ).pack(
            anchor="w",
            padx=17,
            pady=10
        )

        self.auto_analysis = tk.Label(
            f,
            text="",
            bg=LIGHT_BLUE,
            fg=NAVY,
            font=FONT,
            justify="left",
            wraplength=950
        )

        self.auto_analysis.pack(
            fill="x",
            padx=17,
            pady=10
        )

        self.update_auto_analysis()


    def update_auto_analysis(self):

        if not hasattr(
            self,
            "auto_analysis"
        ):
            return

        if not self.data:

            self.auto_analysis.configure(
                text=(
                    "📌 Analisis otomatis:\n"
                    "Belum ada data percobaan."
                )
            )

            return

        nilai_k = [
            d["k"]
            for d in self.data
        ]

        rata = sum(nilai_k) / len(nilai_k)

        minimum = min(nilai_k)
        maksimum = max(nilai_k)

        if rata != 0:

            variasi = (
                (maksimum - minimum) /
                rata *
                100
            )

        else:

            variasi = 0

        if variasi <= 10:
            keterangan = "relatif konsisten"
        else:
            keterangan = "memiliki variasi yang perlu dianalisis"

        self.auto_analysis.configure(
            text=(
                "📌 ANALISIS OTOMATIS\n\n"
                f"Jumlah data: {len(self.data)}\n"
                f"Nilai k terkecil: {minimum:.2f} N/m\n"
                f"Nilai k terbesar: {maksimum:.2f} N/m\n"
                f"Rata-rata k: {rata:.2f} N/m\n"
                f"Variasi relatif: {variasi:.2f}%\n"
                f"Interpretasi: nilai konstanta pegas {keterangan}."
            )
        )


    def simpan_analisis(self):

        self.jawaban_analisis = [
            box.get(
                "1.0",
                "end"
            ).strip()
            for box in self.analysis_boxes
        ]

        self.update_auto_analysis()

        messagebox.showinfo(
            "Berhasil",
            "Jawaban analisis berhasil disimpan."
        )


    # ========================================================
    # KESIMPULAN
    # ========================================================

    def page_kesimpulan(self, p):

        self.page_title(
            p,
            "📝 Kesimpulan",
            "Buat kesimpulan berdasarkan hasil percobaan."
        )

        f = self.card(
            p,
            "Kesimpulan Siswa"
        )

        self.conclusion_box = tk.Text(
            f,
            height=9,
            font=FONT,
            wrap="word"
        )

        self.conclusion_box.pack(
            fill="x",
            padx=17,
            pady=10
        )

        if self.kesimpulan:

            self.conclusion_box.insert(
                "1.0",
                self.kesimpulan
            )

        self.button(
            f,
            "💾 Simpan Kesimpulan",
            self.simpan_kesimpulan,
            TEAL
        ).pack(
            anchor="w",
            padx=17,
            pady=8
        )

        otomatis = self.card(
            p,
            "🤖 Ringkasan Otomatis"
        )

        if self.data:

            rata = sum(
                d["k"]
                for d in self.data
            ) / len(self.data)

            teks = (
                f"Berdasarkan {len(self.data)} data percobaan, "
                f"diperoleh rata-rata konstanta pegas sebesar "
                f"{rata:.2f} N/m. Secara umum, semakin besar gaya "
                f"yang diberikan pada pegas maka pertambahan panjang "
                f"juga meningkat, selama pegas masih berada pada "
                f"daerah elastis."
            )

        else:

            teks = (
                "Ringkasan otomatis akan muncul setelah "
                "data percobaan tersedia."
            )

        tk.Label(
            otomatis,
            text=teks,
            bg=WHITE,
            fg=TEXT,
            font=FONT,
            wraplength=950,
            justify="left"
        ).pack(
            fill="x",
            padx=17,
            pady=10
        )


    def simpan_kesimpulan(self):

        self.kesimpulan = self.conclusion_box.get(
            "1.0",
            "end"
        ).strip()

        messagebox.showinfo(
            "Berhasil",
            "Kesimpulan berhasil disimpan."
        )


    # ========================================================
    # EVALUASI
    # ========================================================

    def page_evaluasi(self, p):

        self.page_title(
            p,
            "🎮 Evaluasi",
            "10 soal pilihan ganda dengan penilaian otomatis."
        )

        f = self.card(
            p,
            "Tes Pemahaman"
        )

        self.quiz_vars = []

        soal = [
            (
                "Besaran yang menunjukkan kekakuan pegas adalah...",
                ["Massa", "Gaya", "Konstanta pegas", "Periode", "Panjang"],
                2,
                "Konstanta pegas k menunjukkan kekakuan pegas."
            ),
            (
                "Persamaan Hukum Hooke adalah...",
                ["F = mg", "F = kΔx", "F = k/x", "F = x/k", "F = m/k"],
                1,
                "Hukum Hooke dinyatakan F = kΔx."
            ),
            (
                "Jika k = 100 N/m dan Δx = 0,05 m, maka F = ...",
                ["2 N", "5 N", "10 N", "20 N", "50 N"],
                1,
                "F = kΔx = 100 × 0,05 = 5 N."
            ),
            (
                "Massa 0,5 kg dengan g = 10 m/s² memiliki gaya berat...",
                ["0,05 N", "0,5 N", "5 N", "10 N", "50 N"],
                2,
                "F = mg = 0,5 × 10 = 5 N."
            ),
            (
                "Jika gaya diperbesar pada pegas yang sama, Δx akan...",
                ["Berkurang", "Bertambah", "Tetap", "Nol", "Tidak berubah"],
                1,
                "Δx = F/k sehingga Δx bertambah ketika F bertambah."
            ),
            (
                "Gradien grafik F terhadap Δx menunjukkan...",
                ["Massa", "Gravitasi", "Konstanta pegas", "Periode", "Panjang awal"],
                2,
                "Pada F = kΔx, gradien grafik adalah k."
            ),
            (
                "Jika k diperbesar dan F tetap, Δx akan...",
                ["Bertambah", "Berkurang", "Tetap", "Nol", "Tidak dapat ditentukan"],
                1,
                "Δx = F/k sehingga Δx berkurang ketika k diperbesar."
            ),
            (
                "F = 8 N dan Δx = 0,04 m. Nilai k adalah...",
                ["0,32 N/m", "2 N/m", "20 N/m", "200 N/m", "320 N/m"],
                3,
                "k = F/Δx = 8/0,04 = 200 N/m."
            ),
            (
                "Hubungan F dan Δx yang linear menghasilkan grafik...",
                ["Garis lurus", "Lingkaran", "Parabola", "Acak", "Horizontal"],
                0,
                "Hubungan linear ditunjukkan oleh garis lurus."
            ),
            (
                "Periode sistem massa-pegas dipengaruhi oleh...",
                ["m dan k", "g saja", "L₀ saja", "Δx saja", "Penggaris"],
                0,
                "T = 2π√(m/k), sehingga dipengaruhi m dan k."
            )
        ]

        for nomor, (
            pertanyaan,
            pilihan,
            benar,
            pembahasan
        ) in enumerate(
            soal,
            1
        ):

            box = tk.Frame(
                f,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            box.pack(
                fill="x",
                padx=17,
                pady=5
            )

            tk.Label(
                box,
                text=f"Soal {nomor}",
                bg=WHITE,
                fg=BLUE,
                font=FONT_BOLD
            ).pack(
                anchor="w",
                padx=10,
                pady=(8, 2)
            )

            tk.Label(
                box,
                text=pertanyaan,
                bg=WHITE,
                fg=NAVY,
                font=FONT_BOLD,
                wraplength=900,
                justify="left"
            ).pack(
                anchor="w",
                padx=10
            )

            var = tk.IntVar(
                value=-1
            )

            self.quiz_vars.append(
                (
                    var,
                    benar,
                    pembahasan
                )
            )

            for i, pilihan_item in enumerate(
                pilihan
            ):

                tk.Radiobutton(
                    box,
                    text=f"{chr(65+i)}. {pilihan_item}",
                    variable=var,
                    value=i,
                    bg=WHITE,
                    activebackground=WHITE,
                    font=FONT
                ).pack(
                    anchor="w",
                    padx=25
                )

        self.button(
            f,
            "✅ CEK JAWABAN",
            self.cek_kuis,
            TEAL
        ).pack(
            anchor="w",
            padx=17,
            pady=12
        )

        self.quiz_result = tk.Label(
            f,
            text="",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 17, "bold"),
            justify="left"
        )

        self.quiz_result.pack(
            anchor="w",
            padx=17,
            pady=7
        )

        self.quiz_explanation = tk.Text(
            f,
            height=15,
            font=FONT,
            wrap="word"
        )

        self.quiz_explanation.pack(
            fill="x",
            padx=17,
            pady=10
        )

        if self.skor is not None:

            self.quiz_result.configure(
                text=f"Skor terakhir: {self.skor}/100"
            )


    def cek_kuis(self):

        benar = 0
        hasil = []

        for nomor, (
            var,
            jawaban_benar,
            pembahasan
        ) in enumerate(
            self.quiz_vars,
            1
        ):

            if var.get() == jawaban_benar:

                benar += 1
                status = "BENAR"

            else:

                status = "SALAH"

            hasil.append(
                f"Soal {nomor}: {status}\n"
                f"Pembahasan: {pembahasan}\n"
            )

        self.skor = benar * 10

        if self.skor >= 80:

            kategori = "Sangat Baik"

        elif self.skor >= 70:

            kategori = "Baik"

        elif self.skor >= 60:

            kategori = "Cukup"

        else:

            kategori = "Perlu belajar kembali"

        self.quiz_result.configure(
            text=(
                f"🏆 Skor = {self.skor}/100\n"
                f"Indikator hasil belajar = {kategori}"
            )
        )

        self.quiz_explanation.delete(
            "1.0",
            "end"
        )

        self.quiz_explanation.insert(
            "1.0",
            "\n".join(hasil)
        )


    # ========================================================
    # LAPORAN
    # ========================================================

    def page_laporan(self, p):

        self.page_title(
            p,
            "📋 Laporan Praktikum",
            "Laporan otomatis berdasarkan aktivitas PhyLab."
        )

        f = self.card(
            p,
            "Preview Laporan"
        )

        self.report_box = tk.Text(
            f,
            height=30,
            font=("Consolas", 9),
            wrap="word"
        )

        self.report_box.pack(
            fill="both",
            expand=True,
            padx=17,
            pady=10
        )

        buttons = tk.Frame(
            f,
            bg=WHITE
        )

        buttons.pack(
            fill="x",
            padx=17,
            pady=7
        )

        self.button(
            buttons,
            "↻ Perbarui",
            self.update_report,
            BLUE
        ).pack(
            side="left",
            padx=2
        )

        self.button(
            buttons,
            "💾 Simpan TXT",
            self.save_report,
            TEAL
        ).pack(
            side="left",
            padx=2
        )

        self.update_report()


    def generate_report(self):

        nama = self.nama.get() or "........................"
        kelas = self.kelas.get() or "........................"
        sekolah = self.sekolah.get() or "........................"

        teks = []

        teks.append(
            "LAPORAN PRAKTIKUM FISIKA"
        )

        teks.append(
            "PRAKTIKUM HUKUM HOOKE DAN KONSTANTA PEGAS"
        )

        teks.append(
            "=" * 70
        )

        teks.append(
            f"Nama    : {nama}"
        )

        teks.append(
            f"Kelas   : {kelas}"
        )

        teks.append(
            f"Sekolah : {sekolah}"
        )

        teks.append(
            f"Tanggal : {datetime.now().strftime('%d-%m-%Y')}"
        )

        teks.append("")

        teks.append(
            "A. TUJUAN"
        )

        teks.append(
            "Menentukan konstanta pegas dan memahami hubungan "
            "antara gaya dengan pertambahan panjang."
        )

        teks.append("")

        teks.append(
            "B. DASAR TEORI"
        )

        teks.append(
            "Hukum Hooke menyatakan bahwa dalam daerah elastis, "
            "gaya berbanding lurus dengan pertambahan panjang."
        )

        teks.append(
            "F = kΔx"
        )

        teks.append(
            "k = F/Δx"
        )

        teks.append("")

        teks.append(
            "C. ALAT DAN BAHAN"
        )

        teks.append(
            "Pegas, beban, statif, penggaris, dan indikator Δx."
        )

        teks.append("")

        teks.append(
            "D. DATA PERCOBAAN"
        )

        if self.data:

            teks.append(
                "No | m(kg) | F(N) | L0(m) | L(m) | Δx(m) | k(N/m)"
            )

            for i, d in enumerate(
                self.data,
                1
            ):

                teks.append(
                    f"{i} | "
                    f"{d['massa']:.3f} | "
                    f"{d['gaya']:.3f} | "
                    f"{d['L0']:.3f} | "
                    f"{d['L']:.3f} | "
                    f"{d['dx']:.4f} | "
                    f"{d['k']:.2f}"
                )

            rata = sum(
                d["k"]
                for d in self.data
            ) / len(self.data)

            teks.append(
                f"\nRata-rata k = {rata:.2f} N/m"
            )

        else:

            teks.append(
                "Belum ada data."
            )

        teks.append("")

        teks.append(
            "E. ANALISIS"
        )

        if self.jawaban_analisis:

            for i, jawaban in enumerate(
                self.jawaban_analisis,
                1
            ):

                teks.append(
                    f"{i}. {jawaban}"
                )

        else:

            teks.append(
                "Belum diisi."
            )

        teks.append("")

        teks.append(
            "F. KESIMPULAN"
        )

        teks.append(
            self.kesimpulan or "Belum diisi."
        )

        teks.append("")

        teks.append(
            "G. EVALUASI"
        )

        teks.append(
            f"Skor evaluasi: "
            f"{self.skor if self.skor is not None else 'Belum dikerjakan'}"
        )

        teks.append("")

        teks.append(
            "H. REFLEKSI"
        )

        teks.append(
            self.refleksi or "Belum diisi."
        )

        teks.append("")

        teks.append(
            "=" * 70
        )

        return "\n".join(teks)


    def update_report(self):

        if not hasattr(
            self,
            "report_box"
        ):
            return

        self.report_box.delete(
            "1.0",
            "end"
        )

        self.report_box.insert(
            "1.0",
            self.generate_report()
        )


    def save_report(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt")
            ]
        )

        if not path:
            return

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                self.generate_report()
            )

        messagebox.showinfo(
            "Berhasil",
            "Laporan berhasil disimpan."
        )


    # ========================================================
    # GLOSARIUM
    # ========================================================

    def page_glosarium(self, p):

        self.page_title(
            p,
            "📖 Glosarium",
            "Istilah penting dalam materi."
        )

        f = self.card(
            p,
            "Istilah Fisika"
        )

        istilah = [
            ("Elastisitas", "Kemampuan benda kembali ke bentuk semula."),
            ("Gaya", "Interaksi yang dapat mengubah gerak atau bentuk benda."),
            ("Massa", "Ukuran banyaknya materi dalam benda."),
            ("Konstanta Pegas", "Ukuran kekakuan pegas dengan satuan N/m."),
            ("Pertambahan Panjang", "Perubahan panjang pegas, Δx = L − L₀."),
            ("Gaya Berat", "Gaya akibat gravitasi, F = mg."),
            ("Gradien", "Kemiringan grafik; pada F terhadap Δx menunjukkan k."),
            ("Periode", "Waktu untuk melakukan satu getaran penuh."),
            ("Daerah Elastis", "Daerah ketika benda masih dapat kembali ke bentuk semula.")
        ]

        for nama, arti in istilah:

            row = tk.Frame(
                f,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            row.pack(
                fill="x",
                padx=17,
                pady=4
            )

            tk.Label(
                row,
                text=nama,
                bg=WHITE,
                fg=BLUE,
                font=FONT_BOLD,
                width=25,
                anchor="w"
            ).pack(
                side="left",
                padx=10,
                pady=9
            )

            tk.Label(
                row,
                text=arti,
                bg=WHITE,
                fg=TEXT,
                font=FONT,
                wraplength=700,
                justify="left"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=9
            )


    # ========================================================
    # REFERENSI
    # ========================================================

    def page_referensi(self, p):

        self.page_title(
            p,
            "📚 Referensi",
            "Bahan bacaan untuk memperdalam materi fisika."
        )

        f = self.card(
            p,
            "Referensi"
        )

        daftar = [
            "Halliday, D., Resnick, R., & Walker, J. Fundamentals of Physics.",
            "Young, H. D., & Freedman, R. A. University Physics with Modern Physics.",
            "Serway, R. A., & Jewett, J. W. Physics for Scientists and Engineers.",
            "OpenStax. College Physics.",
            "Buku teks Fisika SMA/MA pada materi Elastisitas dan Hukum Hooke."
        ]

        for i, teks in enumerate(
            daftar,
            1
        ):

            tk.Label(
                f,
                text=f"{i}. {teks}",
                bg=WHITE,
                fg=TEXT,
                font=FONT,
                wraplength=950,
                justify="left"
            ).pack(
                fill="x",
                padx=17,
                pady=7
            )


    # ========================================================
    # REFLEKSI
    # ========================================================

    def page_refleksi(self, p):

        self.page_title(
            p,
            "⭐ Refleksi",
            "Refleksikan pengalaman belajar setelah menggunakan PhyLab."
        )

        f = self.card(
            p,
            "Refleksi Belajar"
        )

        questions = [
            "1. Konsep apa yang paling kamu pahami?",
            "2. Bagian simulasi mana yang paling membantu?",
            "3. Apa yang masih membingungkan?",
            "4. Apa kelebihan laboratorium virtual menurutmu?",
            "5. Apa yang perlu diperbaiki dari PhyLab?"
        ]

        self.reflection_boxes = []

        for question in questions:

            tk.Label(
                f,
                text=question,
                bg=WHITE,
                fg=NAVY,
                font=FONT_BOLD
            ).pack(
                anchor="w",
                padx=17,
                pady=(8, 2)
            )

            box = tk.Text(
                f,
                height=3,
                font=FONT
            )

            box.pack(
                fill="x",
                padx=17,
                pady=(0, 6)
            )

            self.reflection_boxes.append(box)

        self.button(
            f,
            "💾 Simpan Refleksi",
            self.simpan_refleksi,
            TEAL
        ).pack(
            anchor="w",
            padx=17,
            pady=10
        )


    def simpan_refleksi(self):

        self.refleksi = "\n\n".join(
            box.get(
                "1.0",
                "end"
            ).strip()
            for box in self.reflection_boxes
        )

        messagebox.showinfo(
            "Berhasil",
            "Refleksi berhasil disimpan."
        )


    # ========================================================
    # SIMPAN PROYEK
    # ========================================================

    def simpan_proyek(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("PhyLab Project", "*.json")
            ]
        )

        if not path:
            return

        proyek = {
            "identitas": {
                "nama": self.nama.get(),
                "kelas": self.kelas.get(),
                "sekolah": self.sekolah.get()
            },

            "simulasi": {
                "massa": self.massa.get(),
                "k": self.k.get(),
                "g": self.g.get()
            },

            "data": self.data,

            "pra_prediksi": self.pra_prediksi,

            "analisis": self.jawaban_analisis,

            "kesimpulan": self.kesimpulan,

            "refleksi": self.refleksi,

            "skor": self.skor
        }

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                proyek,
                file,
                indent=4,
                ensure_ascii=False
            )

        messagebox.showinfo(
            "Berhasil",
            "Proyek PhyLab berhasil disimpan."
        )


    # ========================================================
    # BUKA PROYEK
    # ========================================================

    def buka_proyek(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("PhyLab Project", "*.json")
            ]
        )

        if not path:
            return

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                proyek = json.load(file)

            identitas = proyek.get(
                "identitas",
                {}
            )

            self.nama.set(
                identitas.get(
                    "nama",
                    ""
                )
            )

            self.kelas.set(
                identitas.get(
                    "kelas",
                    ""
                )
            )

            self.sekolah.set(
                identitas.get(
                    "sekolah",
                    ""
                )
            )

            simulasi = proyek.get(
                "simulasi",
                {}
            )

            self.massa.set(
                simulasi.get(
                    "massa",
                    0.5
                )
            )

            self.k.set(
                simulasi.get(
                    "k",
                    100
                )
            )

            self.g.set(
                simulasi.get(
                    "g",
                    9.8
                )
            )

            self.data = proyek.get(
                "data",
                []
            )

            self.pra_prediksi = proyek.get(
                "pra_prediksi",
                ""
            )

            self.jawaban_analisis = proyek.get(
                "analisis",
                []
            )

            self.kesimpulan = proyek.get(
                "kesimpulan",
                ""
            )

            self.refleksi = proyek.get(
                "refleksi",
                ""
            )

            self.skor = proyek.get(
                "skor"
            )

            # Refresh halaman aktif
            halaman = self.halaman_sekarang

            self.tampilkan(
                halaman
            )

            messagebox.showinfo(
                "Berhasil",
                "Proyek berhasil dibuka."
            )

        except Exception as error:

            messagebox.showerror(
                "Gagal",
                f"Proyek tidak dapat dibuka.\n\n{error}"
            )


    # ========================================================
    # KELUAR
    # ========================================================

    def keluar(self):

        if messagebox.askyesno(
            "Keluar",
            "Apakah kamu yakin ingin keluar dari PhyLab?"
        ):

            self.destroy()


# ============================================================
# JALANKAN APLIKASI
# ============================================================

if __name__ == "__main__":

    app = PhyLab()

    app.mainloop()
