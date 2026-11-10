import tkinter as tk
from qr_generator.gui import QRCodeApp


def main():
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
