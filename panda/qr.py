"""
Weaving Vibes — Fabric QR Code Generator
------------------------------------------
Generates a styled QR code (with WV logo embedded in the center)
for each fabric's GitHub Pages link.

Usage:
    python3 generate_qr.py

To add more fabrics later, just add entries to the FABRICS dict below
and re-run. Each one outputs a PNG named after the fabric.
"""

import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

# ---- CONFIG ----------------------------------------------------

# Add one entry per fabric. Key = output filename, Value = full URL.
FABRICS = {
    "panda": "https://weaving-vibes.github.io/wv-eachclothqr/panda/",
}

# Resolve paths relative to THIS script's location, not the terminal's
# current folder — so it works no matter which directory you run it from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "..", "AA_Static", "logo.jpeg")
OUTPUT_DIR = SCRIPT_DIR

# Weaving Vibes brand green (sampled from your logo/site)
BRAND_GREEN = (122, 142, 96)   # muted sage green
BACKGROUND = (255, 255, 255)   # white background for scan reliability

# ---- LOGO PREP ----------------------------------------------------

def prep_logo(logo_path, size=200):
    """
    Loads the logo and pastes it onto a clean white square.
    This gives the QR code a solid 'quiet zone' around the logo,
    which keeps the QR scannable even with a busy logo in the center.
    """
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((size, size), Image.LANCZOS)

    # white padded square slightly bigger than the logo
    pad = 24
    canvas_size = max(logo.size) + pad * 2
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))

    offset = (
        (canvas_size - logo.width) // 2,
        (canvas_size - logo.height) // 2,
    )
    canvas.paste(logo, offset, mask=logo)
    return canvas


# ---- QR GENERATION ----------------------------------------------------

def generate_qr(url: str, output_path: str, logo_path: str = LOGO_PATH):
    if not os.path.exists(logo_path):
        raise FileNotFoundError(
            f"\n\nCouldn't find the logo file at:\n  {logo_path}\n"
            f"Check that AA_Static/width_436.webp exists at the project root,\n"
            f"one level above the folder this script is sitting in.\n"
        )

    qr = qrcode.QRCode(
        version=None,                # auto-size based on data
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # high — needed since we're covering center with logo
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    logo_img = prep_logo(logo_path)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=BACKGROUND,
            front_color=BRAND_GREEN,
        ),
        embeded_image=logo_img,
    )

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    for name, url in FABRICS.items():
        generate_qr(url, f"{OUTPUT_DIR}/qr_{name}.png")