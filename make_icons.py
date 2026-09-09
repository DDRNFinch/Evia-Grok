from PIL import Image, ImageDraw, ImageFont

TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SUB_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ORB_A = (255, 225, 77)   # --orb-a
ORB_B = (255, 179, 0)    # --orb-b
WHITE = (255, 255, 255, 255)

def make_icon(size, corner_radius_ratio, filename, maskable=False):
    scale = 4  # supersample for smooth text/corners, then downscale
    S = size * scale

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # background: soft yellow gradient (radial-ish via vertical blend) + rounded corners
    bg = Image.new("RGBA", (S, S), ORB_B)
    top = Image.new("RGBA", (S, S), ORB_A)
    mask = Image.new("L", (S, S), 0)
    mdraw = ImageDraw.Draw(mask)
    for y in range(S):
        mdraw.line([(0, y), (S, y)], fill=int(255 * (1 - y / S) * 0.55))
    bg = Image.composite(top, bg, mask)

    if maskable:
        # maskable icons should fill edge-to-edge (safe zone handled by OS), no rounding
        corner_radius = 0
    else:
        corner_radius = int(S * corner_radius_ratio)

    rounded_mask = Image.new("L", (S, S), 0)
    rmdraw = ImageDraw.Draw(rounded_mask)
    rmdraw.rounded_rectangle([0, 0, S, S], radius=corner_radius, fill=255)

    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(bg, (0, 0), rounded_mask)
    draw = ImageDraw.Draw(out)

    # subtle inner glow highlight top-left
    highlight = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    hd.ellipse(
        [S * 0.05, S * 0.02, S * 0.75, S * 0.55],
        fill=(255, 255, 255, 40),
    )
    out = Image.alpha_composite(out, highlight)
    draw = ImageDraw.Draw(out)

    # text: "Evia" large, "Apprentice" smaller below
    title_size = int(S * 0.30)
    sub_size = int(S * 0.105)

    title_font = ImageFont.truetype(TITLE_FONT, title_size)
    sub_font = ImageFont.truetype(SUB_FONT, sub_size)

    title_text = "Evia"
    sub_text = "Apprentice"

    tb = draw.textbbox((0, 0), title_text, font=title_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    sb = draw.textbbox((0, 0), sub_text, font=sub_font)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]

    gap = int(S * 0.045)
    block_h = th + gap + sh
    start_y = (S - block_h) / 2 - S * 0.015

    title_x = (S - tw) / 2 - tb[0]
    title_y = start_y - tb[1]
    draw.text((title_x, title_y), title_text, font=title_font, fill=WHITE)

    sub_y = start_y + th + gap - sb[1]
    sub_x = (S - sw) / 2 - sb[0]
    # slightly translucent white for hierarchy
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(255, 255, 255, 225))

    out = out.resize((size, size), Image.LANCZOS)
    out.save(filename)
    print("wrote", filename, size)


make_icon(192, 0.22, "/home/claude/loading-orb/icons/icon-192.png")
make_icon(512, 0.22, "/home/claude/loading-orb/icons/icon-512.png")
make_icon(512, 0, "/home/claude/loading-orb/icons/icon-512-maskable.png", maskable=True)
make_icon(180, 0.22, "/home/claude/loading-orb/icons/apple-touch-icon.png")
make_icon(32, 0.22, "/home/claude/loading-orb/icons/favicon-32.png")
