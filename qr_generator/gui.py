import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import ImageTk, Image

from .generator import QRCodeService, ERROR_CORRECTION_MAP


class QRCodeApp:
    """Tkinter UI Application for QR Code Studio."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Studio")
        self.root.geometry("650x500")
        self.root.minsize(600, 460)

        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.current_image = None
        self.tk_image = None

        self._configure_styles()
        self._build_ui()
        self._generate_preview()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8fafc")
        style.configure("TLabel", background="#f8fafc", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#0f172a")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])

    def _build_ui(self):
        self.root.configure(bg="#f8fafc")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(main_frame, text="QR Code Studio", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Left Panel (Controls)
        controls = ttk.Frame(main_frame)
        controls.grid(row=1, column=0, sticky="nsew", padx=(0, 20))

        ttk.Label(controls, text="Content / URL:").grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.data_entry = ttk.Entry(controls, width=30)
        self.data_entry.insert(0, "https://github.com")
        self.data_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.data_entry.bind("<KeyRelease>", lambda e: self._generate_preview())

        ttk.Label(controls, text="Foreground Color:").grid(row=2, column=0, sticky="w", pady=(5, 2))
        self.fg_btn = tk.Button(
            controls, text=self.fill_color, bg=self.fill_color, fg="#ffffff",
            command=self._choose_fg_color, width=15, relief="flat", cursor="hand2"
        )
        self.fg_btn.grid(row=3, column=0, sticky="w", pady=(0, 10))

        ttk.Label(controls, text="Background Color:").grid(row=4, column=0, sticky="w", pady=(5, 2))
        self.bg_btn = tk.Button(
            controls, text=self.back_color, bg=self.back_color, fg="#000000",
            command=self._choose_bg_color, width=15, relief="flat", cursor="hand2"
        )
        self.bg_btn.grid(row=5, column=0, sticky="w", pady=(0, 10))

        ttk.Label(controls, text="Error Correction:").grid(row=6, column=0, sticky="w", pady=(5, 2))
        self.ec_combo = ttk.Combobox(
            controls, values=list(ERROR_CORRECTION_MAP.keys()), state="readonly", width=18
        )
        self.ec_combo.set("M (15%)")
        self.ec_combo.grid(row=7, column=0, sticky="w", pady=(0, 10))
        self.ec_combo.bind("<<ComboboxSelected>>", lambda e: self._generate_preview())

        ttk.Label(controls, text="Box Size:").grid(row=8, column=0, sticky="w", pady=(5, 2))
        self.size_scale = ttk.Scale(controls, from_=5, to=20, value=10, command=lambda v: self._generate_preview())
        self.size_scale.grid(row=9, column=0, sticky="ew", pady=(0, 15))

        save_btn = ttk.Button(controls, text="Export QR Code", style="Accent.TButton", command=self._save_qr)
        save_btn.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Right Panel (Preview)
        preview_frame = ttk.LabelFrame(main_frame, text=" Preview ", padding="10")
        preview_frame.grid(row=1, column=1, sticky="nsew")

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def _choose_fg_color(self):
        color = colorchooser.askcolor(color=self.fill_color, title="Choose Foreground Color")[1]
        if color:
            self.fill_color = color
            self.fg_btn.configure(bg=color, text=color)
            self._generate_preview()

    def _choose_bg_color(self):
        color = colorchooser.askcolor(color=self.back_color, title="Choose Background Color")[1]
        if color:
            self.back_color = color
            self.bg_btn.configure(bg=color, text=color)
            self._generate_preview()

    def _generate_preview(self):
        text = self.data_entry.get().strip()
        if not text:
            text = " "

        try:
            box_sz = int(self.size_scale.get())
            ec = self.ec_combo.get()
            self.current_image = QRCodeService.generate_qr(
                data=text,
                fill_color=self.fill_color,
                back_color=self.back_color,
                box_size=box_sz,
                border=2,
                error_correction=ec,
            )
            preview_img = self.current_image.resize((240, 240), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(preview_img)
            self.preview_label.config(image=self.tk_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")

    def _save_qr(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "No QR Code available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")],
            title="Save QR Code"
        )
        if file_path:
            try:
                QRCodeService.save_qr(self.current_image, file_path)
                messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")
