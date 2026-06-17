import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image

# ── CONFIG ────────────────────────────────────────────────────────────────────

FABRICS = {
    "seersucker": "https://weaving-vibes.github.io/wv-eachclothqr/seersucker/",
}

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "..", "AA_Static", "logo.jpeg")
OUTPUT_DIR  = SCRIPT_DIR

BRAND_GREEN = (122, 142, 96)
WHITE       = (255, 255, 255)

# Logo occupies this fraction of the QR canvas (0.20–0.25 is safe with H correction)
LOGO_RATIO = 0.32

# Final output image size in pixels
OUTPUT_SIZE = 1200

# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_logo(path: str, target_size: int) -> Image.Image:
    
    logo = Image.open(path).convert("RGBA")

    # Fit inside a square, preserving aspect ratio
    logo.thumbnail((target_size, target_size), Image.LANCZOS)

    # White padded square — padding = 12 % of target_size on each side
    pad = int(target_size * 0.05)
    frame = target_size + pad * 2
    canvas = Image.new("RGBA", (frame, frame), (255, 255, 255, 255))
    offset = ((frame - logo.width) // 2, (frame - logo.height) // 2)
    canvas.paste(logo, offset, mask=logo)

    return canvas.resize((target_size, target_size), Image.LANCZOS)


def generate_qr(name: str, url: str) -> None:
    if not os.path.exists(LOGO_PATH):
        raise FileNotFoundError(
            f"Logo not found at: {LOGO_PATH}\n"
            "Place logo.jpeg next to this script."
        )

    # ── 1. Build QR ──────────────────────────────────────────────────────────
    qr = qrcode.QRCode(
        version=None,                              # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,   # H = 30 % recoverable
        box_size=10,
        border=4,                                  # standard quiet zone (4 modules)
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Logo size relative to QR canvas (before final resize)
    qr_canvas_px = (qr.modules_count + qr.border * 2) * qr.box_size
    logo_px      = int(qr_canvas_px * LOGO_RATIO)
    logo_img     = load_logo(LOGO_PATH, logo_px)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        embeded_image=logo_img,          # qrcode library centers this automatically
        back_color=WHITE,
        fill_color=BRAND_GREEN,
    )

    # ── 2. Convert & resize to final output size ─────────────────────────────
    img = img.convert("RGB")
    img = img.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)

    # ── 3. Save ──────────────────────────────────────────────────────────────
    out = os.path.join(OUTPUT_DIR, f"qr_{name}.png")
    img.save(out, "PNG", optimize=True)
    print(f"✓  {out}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for name, url in FABRICS.items():
        generate_qr(name, url)