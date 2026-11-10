import os
import pytest
from PIL import Image
from qr_generator.generator import QRCodeService, ERROR_CORRECTION_MAP


def test_generate_qr_success():
    img = QRCodeService.generate_qr("Hello World", fill_color="#000000", back_color="#FFFFFF")
    assert isinstance(img, Image.Image)
    assert img.size[0] > 0
    assert img.size[1] > 0


def test_generate_qr_empty_data_raises_error():
    with pytest.raises(ValueError, match="Data for QR code cannot be empty."):
        QRCodeService.generate_qr("")


def test_save_qr(tmp_path):
    img = QRCodeService.generate_qr("Save Test")
    output_file = os.path.join(tmp_path, "test_qr.png")
    QRCodeService.save_qr(img, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0


def test_error_corrections():
    for ec_name in ERROR_CORRECTION_MAP.keys():
        img = QRCodeService.generate_qr("Test ECC", error_correction=ec_name)
        assert isinstance(img, Image.Image)
