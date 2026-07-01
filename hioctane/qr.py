import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

FABRICS = {
    "hioctane": "https://weaving-vibes.github.io/wv-eachclothqr/hioctane/",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "..", "AA_Static", "logo.jpeg")
OUTPUT_DIR = SCRIPT_DIR

BRAND_GREEN = (122, 142, 96)
WHITE       = (255, 255, 255)

LOGO_RATIO = 0.32
OUTPUT_SIZE = 1200

def load_logo(path, target_size):
    logo = Image.open(path).convert("RGBA")
    logo.thumbnail((target_size, target_size), Image.LANCZOS)
    pad = int(target_size * 0.05)
    frame = target_size + pad * 2
    canvas = Image.new("RGBA", (frame, frame), (255, 255, 255, 255))
    offset = ((frame - logo.width) // 2, (frame - logo.height) // 2)
    canvas.paste(logo, offset, mask=logo)
    return canvas.resize((target_size, target_size), Image.LANCZOS)

def generate_qr(name, url):
    if not os.path.exists(LOGO_PATH):
        raise FileNotFoundError(f"Logo not found at: {LOGO_PATH}")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_canvas_px = (qr.modules_count + qr.border * 2) * qr.box_size
    logo_px = int(qr_canvas_px * LOGO_RATIO)
    logo_img = load_logo(LOGO_PATH, logo_px)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        embeded_image=logo_img,
        color_mask=SolidFillColorMask(back_color=WHITE, front_color=BRAND_GREEN),
    )

    img = img.convert("RGB")
    img = img.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)

    out = os.path.join(OUTPUT_DIR, f"qr_{name}.png")
    img.save(out, "PNG", optimize=True)
    print(f"DONE: {out}")

if __name__ == "__main__":
    for name, url in FABRICS.items():
        generate_qr(name, url)
