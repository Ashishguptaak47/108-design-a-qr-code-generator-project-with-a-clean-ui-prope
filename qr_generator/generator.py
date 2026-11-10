import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)
from PIL import Image

ERROR_CORRECTION_MAP = {
    "L (7%)": ERROR_CORRECT_L,
    "M (15%)": ERROR_CORRECT_M,
    "Q (25%)": ERROR_CORRECT_Q,
    "H (30%)": ERROR_CORRECT_H,
}


class QRCodeService:
    """Service class for rendering and saving QR codes."""

    @staticmethod
    def generate_qr(
        data: str,
        fill_color: str = "#000000",
        back_color: str = "#FFFFFF",
        box_size: int = 10,
        border: int = 4,
        error_correction: str = "M (15%)",
    ) -> Image.Image:
        if not data:
            raise ValueError("Data for QR code cannot be empty.")

        ec_level = ERROR_CORRECTION_MAP.get(error_correction, ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec_level,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
        return img

    @staticmethod
    def save_qr(img: Image.Image, file_path: str) -> None:
        """Save Pillow image to specified file path."""
        img.save(file_path)
