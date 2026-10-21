#!/usr/bin/env python3
"""Génère les images du site Plan2Real (à relancer si le logo ou les fonds changent).

Sources (dépôt de l'app, dossier voisin) :
  ../Plan2Real/Plan2Real/Resources/Assets.xcassets/Logo.imageset/Logo.png
  ../Plan2Real/docs/fonds/beton-original.jpg, bois-original.jpg

Produit dans assets/img/ : logo, icônes, fonds béton/bois, plan d'exemple, photo du plan sur
contreplaqué (sert aussi aux captures de l'app), illustration « plan au sol », images de partage.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT.parent / "Plan2Real"
OUT = ROOT / "assets" / "img"
LOGO = APP / "Plan2Real/Resources/Assets.xcassets/Logo.imageset/Logo.png"
BETON = APP / "docs/fonds/beton-original.jpg"
BOIS = APP / "docs/fonds/bois-original.jpg"

NAVY = (20, 33, 61)
AMBER = (242, 169, 0)
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


# ---------------------------------------------------------------- plan d'exemple (36 pi × 24 pi)
def floor_plan():
    ft = 60                                  # 60 px par pied
    m = 170                                  # marge (cotes)
    W, H = 36 * ft + 2 * m, 24 * ft + 2 * m + 120
    im = Image.new("RGB", (W, H), (250, 250, 246))
    d = ImageDraw.Draw(im)
    x0, y0 = m, m
    wall = 16

    def X(f): return x0 + f * ft
    def Y(f): return y0 + f * ft

    def w(a, b, c, e):  # mur de (a,b) à (c,e), en pieds
        d.line([(X(a), Y(b)), (X(c), Y(e))], fill=(25, 25, 25), width=wall)

    # Contour extérieur
    for seg in [(0, 0, 36, 0), (36, 0, 36, 24), (36, 24, 0, 24), (0, 24, 0, 0)]:
        w(*seg)
    # Cloisons : salon | cuisine (x=16), chambre (y=14), salle de bain (x=24)
    w(16, 0, 16, 9); w(16, 12, 16, 24)          # ouverture salon-cuisine 9→12
    w(0, 14, 36, 14)                            # portes : chambre 9→12, s.d.b. 19→22, rangement 27→30
    w(24, 14, 24, 24)

    # Ouvertures (portes) : effacer le mur puis dessiner le battant
    def door(cx, cy, horizontal, swing):
        if horizontal:
            d.rectangle([X(cx), Y(cy) - wall, X(cx + 3), Y(cy) + wall], fill=(250, 250, 246))
            r = 3 * ft
            box = [X(cx) - r, Y(cy) - r, X(cx) + r, Y(cy) + r]
            d.arc(box, 0 if swing > 0 else 270, 90 if swing > 0 else 360, fill=(90, 90, 90), width=3)
            d.line([(X(cx), Y(cy)), (X(cx), Y(cy) + swing * r)], fill=(90, 90, 90), width=4)
        else:
            d.rectangle([X(cx) - wall, Y(cy), X(cx) + wall, Y(cy + 3)], fill=(250, 250, 246))

    door(9, 14, True, 1)
    door(19, 14, True, 1)
    door(27, 14, True, 1)
    # Entrée dans la cuisine, mur de droite de 10 à 13 pi : le battant s'ouvre vers l'intérieur.
    d.rectangle([X(36) - wall, Y(10), X(36) + wall, Y(13)], fill=(250, 250, 246))
    d.line([(X(36), Y(10)), (X(33), Y(10))], fill=(90, 90, 90), width=4)
    d.arc([X(36) - 3 * ft, Y(10) - 3 * ft, X(36) + 3 * ft, Y(10) + 3 * ft], 90, 180, fill=(90, 90, 90), width=3)
    # Fenêtres
    for (a, b, c, e) in [(4, 0, 11, 0), (22, 0, 30, 0), (36, 4, 36, 9), (0, 17, 0, 21), (28, 24, 32, 24)]:
        d.line([(X(a), Y(b)), (X(c), Y(e))], fill=(250, 250, 246), width=wall - 4)
        d.line([(X(a), Y(b)), (X(c), Y(e))], fill=(60, 110, 170), width=4)

    # Comptoir de cuisine et îlot
    d.rectangle([X(17), Y(1), X(35), Y(3)], outline=(70, 70, 70), width=4)
    d.rectangle([X(22), Y(6), X(30), Y(9)], outline=(70, 70, 70), width=4)

    # Étiquettes
    lab = font(64, bold=True)
    small = font(40)
    for text, sub, cx, cy in [("SALON", "16' × 14'", 8, 6), ("CUISINE", "20' × 14'", 26, 11.5),
                              ("CHAMBRE", "16' × 10'", 6.5, 19), ("S.D.B.", "8' × 10'", 20, 19.5),
                              ("RANGEMENT", "12' × 10'", 30, 19.5)]:
        d.text((X(cx), Y(cy)), text, fill=(30, 30, 30), font=lab, anchor="mm")
        d.text((X(cx), Y(cy) + 62), sub, fill=(80, 80, 80), font=small, anchor="mm")

    # Cotes
    dim = font(46, bold=True)
    blue = (30, 70, 140)
    d.line([(X(0), Y(0) - 90), (X(36), Y(0) - 90)], fill=blue, width=4)
    for f in (0, 36):
        d.line([(X(f), Y(0) - 120), (X(f), Y(0) - 60)], fill=blue, width=4)
    d.text((X(18), Y(0) - 100), "36'-0\"", fill=blue, font=dim, anchor="md")
    d.line([(X(0) - 90, Y(0)), (X(0) - 90, Y(24))], fill=blue, width=4)
    for f in (0, 24):
        d.line([(X(0) - 120, Y(f)), (X(0) - 60, Y(f))], fill=blue, width=4)
    t = Image.new("RGBA", (400, 80), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((200, 40), "24'-0\"", fill=blue + (255,), font=dim, anchor="mm")
    t = t.rotate(90, expand=True)
    im.paste(t, (X(0) - 150, int(Y(12) - t.height / 2)), t)
    # Cote de porte 36 po (pour la mise à l'échelle)
    d.line([(X(9), Y(14) + 70), (X(12), Y(14) + 70)], fill=blue, width=3)
    d.text((X(10.5), Y(14) + 78), "36\"", fill=blue, font=font(38, bold=True), anchor="ma")

    # Cartouche
    d.rectangle([W - 1060, H - 150, W - 60, H - 40], outline=(30, 30, 30), width=4)
    d.text((W - 1040, H - 128), "PLAN DU REZ-DE-CHAUSSÉE", fill=(30, 30, 30), font=font(40, bold=True))
    d.text((W - 1040, H - 80), "Échelle 1/4\" = 1'-0\"  ·  Exemple Plan2Real", fill=(70, 70, 70), font=font(32))
    return im


# ---------------------------------------------------------------- outils de perspective
def coeffs(src, dst):
    """Coefficients PIL pour envoyer le quadrilatère dst (sortie) vers src (entrée)."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def warp(img, quad, size):
    w, h = img.size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    rgba = img.convert("RGBA")
    return rgba.transform(size, Image.PERSPECTIVE, coeffs(src, quad), Image.BICUBIC, fillcolor=(0, 0, 0, 0))


def upscale(img, width):
    out = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    return out.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def pinhole_quad(aspect, size, tilt=0.45, yaw=0.12, focal_factor=0.8, fill=0.62):
    """Coins (HG, HD, BD, BG) d'une feuille de proportions `aspect` vue par une vraie caméra
    sténopé inclinée : la photo d'exemple se comporte comme une vraie photo prise de biais."""
    W, H = size
    f = focal_factor * W
    sw, sh = 1.0, 1.0 / aspect
    c, s_ = np.cos(tilt), np.sin(tilt)
    cy, sy = np.cos(yaw), np.sin(yaw)
    pts = []
    for x, y in [(-sw / 2, -sh / 2), (sw / 2, -sh / 2), (sw / 2, sh / 2), (-sw / 2, sh / 2)]:
        X, Y, Z = x, y * c, y * s_                    # inclinaison autour de X
        X, Z = X * cy + Z * sy, -X * sy + Z * cy      # lacet autour de Y
        pts.append((X, Y, Z))
    d = f * sw / (fill * W)                           # distance pour que la feuille occupe `fill` de la largeur
    quad = [(f * X / (Z + d) + W / 2, f * Y / (Z + d) + H / 2) for X, Y, Z in pts]
    return quad


# ---------------------------------------------------------------- photo du plan sur contreplaqué
def plan_photo(plan):
    """Feuille posée à plat sur un panneau de contreplaqué, photographiée de biais : toute la
    scène (panneau + feuille) passe par la même caméra sténopé, comme une vraie photo."""
    wood = upscale(Image.open(BOIS).convert("RGB"), 2600)
    W, H = wood.size
    # Scène à plat : la feuille au centre du panneau, avec une ombre douce.
    flat = wood.copy()
    sw = int(W * 0.62)
    sh = round(sw * plan.height / plan.width)
    x0, y0 = (W - sw) // 2, (H - sh) // 2
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rectangle([x0 + 10, y0 + 14, x0 + sw + 10, y0 + sh + 14], fill=140)
    flat.paste((45, 32, 20), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
    flat.paste(plan.resize((sw, sh), Image.LANCZOS), (x0, y0))
    # Plancher de béton autour, puis le panneau vu en perspective (bord proche en bas).
    floor = upscale(Image.open(BETON).convert("RGB"), W).resize((W, H))
    floor = Image.fromarray((np.asarray(floor, float) * 0.7).astype(np.uint8))
    quad = pinhole_quad(W / H, (W, H), tilt=-0.5, yaw=0.1, fill=0.98)
    board = warp(flat, quad, (W, H))
    base = floor.copy()
    base.paste(board, (0, 0), board)
    yy, xx = np.mgrid[0:H, 0:W]
    light = 1.06 - 0.12 * (((xx - W * 0.4) / W) ** 2 + ((yy - H * 0.35) / H) ** 2)
    arr = np.clip(np.asarray(base, float) * light[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


# ---------------------------------------------------------------- illustration « plan au sol »
TXT = {
    "fr": dict(confirmed="Position confirmée : le plan sera posé", confirmed2="sur la surface visée.", place="Placer le plan ici",
               pinch_tip="Échelle au doigt : pincez", pinch_help="Pincez pour faire coïncider une cote", scale="Échelle 100,0 %"),
    "en": dict(confirmed="Position confirmed: the plan will sit", confirmed2="on the surface you aim at.", place="Place the plan here",
               pinch_tip="Finger scale: pinch", pinch_help="Pinch to match a dimension", scale="Scale 100.0 %"),
}


def floor_scene(plan):
    """Plan couché sur le béton mouillé, vu en perspective, semi-transparent."""
    W, H = 1080, 1920
    beton = Image.open(BETON).convert("RGB").rotate(90, expand=True)
    beton = upscale(beton, 1400)
    base = beton.crop(((beton.width - W) // 2, 0, (beton.width - W) // 2 + W, H)) if beton.height >= H else beton.resize((W, H))
    quad = [(300, 620), (800, 600), (1260, 1720), (-120, 1760)]
    sheet = warp(plan, quad, (W, H))
    sheet.putalpha(sheet.split()[3].point(lambda a: int(a * 0.78)))
    base.paste(sheet, (0, 0), sheet)
    return base


def green_target(d, cx, cy, r=70):
    green = (51, 255, 20, 255)
    for rad, w in [(r, 7), (r * 0.66, 3), (r * 0.33, 3)]:
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=green, width=int(w))
    d.line([(cx - r, cy), (cx + r, cy)], fill=green, width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=green, width=2)


def ar_concept(plan, lang="fr"):
    """Étape de pose : cible verte au centre, consigne et bouton rouge « Placer le plan ici »."""
    W, H = 1080, 1920
    t = TXT[lang]
    base = floor_scene(plan)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    green_target(d, W // 2, H // 2, 96)
    d.rounded_rectangle([40, 1560, W - 40, 1850], radius=40, fill=(235, 236, 240, 228))
    d.text((W // 2, 1622), t["confirmed"], fill=NAVY + (255,), font=font(34), anchor="mm")
    d.text((W // 2, 1668), t["confirmed2"], fill=NAVY + (255,), font=font(34), anchor="mm")
    d.rounded_rectangle([80, 1715, W - 80, 1815], radius=26, fill=(219, 38, 38, 255))
    d.text((W // 2, 1765), t["place"], fill=(255, 255, 255, 255), font=font(42, bold=True), anchor="mm")
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


# ---------------------------------------------------------------- écran au sol avec la colonne de boutons
def rail_screen(plan, lang="fr"):
    """Écran au sol tel que dans l'app : plan au sol, boutons ronds à gauche, nom de la
    fonction affiché à côté du bouton touché (ici l'échelle au doigt)."""
    W, H = 1080, 1920
    tx = TXT[lang]
    base = floor_scene(plan)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    red = (219, 38, 38, 255)
    white = (255, 255, 255, 255)
    # Colonne de boutons
    x0, y0, size, gap = 40, 230, 92, 22
    icons = ["move", "rotate", "height", "pinch", "scale", "lock", "ruler", "opacity", "camera", "more"]

    def icon(kind, c):
        x, y = c
        k = 22
        if kind == "move":
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                d.line([(x, y), (x + dx * k, y + dy * k)], fill=white, width=5)
                d.polygon([(x + dx * (k + 8), y + dy * (k + 8)), (x + dx * k + dy * 7, y + dy * k + dx * 7),
                           (x + dx * k - dy * 7, y + dy * k - dx * 7)], fill=white)
        elif kind == "rotate":
            d.arc([x - k, y - k, x + k, y + k], 300, 220, fill=white, width=5)
            d.polygon([(x + 6, y - k - 9), (x + 6, y - k + 9), (x + 18, y - k)], fill=white)
        elif kind == "height":
            d.line([(x, y - k), (x, y + k)], fill=white, width=5)
            d.polygon([(x - 10, y - k + 4), (x + 10, y - k + 4), (x, y - k - 10)], fill=white)
            d.polygon([(x - 10, y + k - 4), (x + 10, y + k - 4), (x, y + k + 10)], fill=white)
        elif kind == "pinch":
            d.line([(x - 18, y + 18), (x - 4, y + 4)], fill=white, width=6)
            d.line([(x + 18, y - 18), (x + 4, y - 4)], fill=white, width=6)
            d.ellipse([x - 26, y + 12, x - 12, y + 26], fill=white)
            d.ellipse([x + 12, y - 26, x + 26, y - 12], fill=white)
        elif kind == "scale":
            d.line([(x - k, y), (x + k, y)], fill=white, width=5)
            d.polygon([(x - k - 10, y), (x - k + 4, y - 10), (x - k + 4, y + 10)], fill=white)
            d.polygon([(x + k + 10, y), (x + k - 4, y - 10), (x + k - 4, y + 10)], fill=white)
        elif kind == "lock":
            d.rounded_rectangle([x - 18, y - 4, x + 18, y + 22], radius=4, fill=white)
            d.arc([x - 13, y - 26, x + 13, y + 6], 180, 360, fill=white, width=5)
        elif kind == "ruler":
            d.rounded_rectangle([x - 26, y - 10, x + 26, y + 10], radius=3, outline=white, width=4)
            for t in range(-18, 20, 9):
                d.line([(x + t, y - 10), (x + t, y - 1)], fill=white, width=3)
        elif kind == "opacity":
            d.ellipse([x - k, y - k, x + k, y + k], outline=white, width=4)
            d.pieslice([x - k, y - k, x + k, y + k], 90, 270, fill=white)
        elif kind == "camera":
            d.rounded_rectangle([x - 26, y - 14, x + 26, y + 20], radius=6, outline=white, width=4)
            d.rectangle([x - 10, y - 22, x + 10, y - 14], fill=white)
            d.ellipse([x - 9, y - 6, x + 9, y + 12], outline=white, width=4)
        elif kind == "more":
            for t in (-16, 0, 16):
                d.ellipse([x + t - 5, y - 5, x + t + 5, y + 5], fill=white)

    for i, kind in enumerate(icons):
        y = y0 + i * (size + gap)
        on = kind == "pinch"
        d.ellipse([x0, y, x0 + size, y + size], fill=red if on else (0, 0, 0, 150),
                  outline=(255, 255, 255, 230 if on else 70), width=2)
        icon(kind, (x0 + size // 2, y + size // 2))
    # Nom de la fonction à côté du bouton touché
    ty = y0 + 3 * (size + gap) + size // 2
    label = tx["pinch_tip"]
    f = font(36, bold=True)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x0 + size + 20, ty - 36, x0 + size + 20 + tw + 48, ty + 36], radius=36, fill=(0, 0, 0, 170))
    d.text((x0 + size + 44, ty), label, fill=white, font=f, anchor="lm")
    # Panneau du bas (échelle)
    d.rounded_rectangle([40, 1650, W - 40, 1850], radius=40, fill=(235, 236, 240, 225))
    d.text((90, 1712), tx["pinch_help"], fill=NAVY + (255,), font=font(32), anchor="lm")
    d.text((90, 1788), tx["scale"], fill=NAVY + (255,), font=font(52, bold=True), anchor="lm")
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


# ---------------------------------------------------------------- images de partage (1200 × 630)
def og_image(lang, logo):
    W, H = 1200, 630
    beton = upscale(Image.open(BETON).convert("RGB"), 1200).resize((W, H))
    arr = (np.asarray(beton, float) * 0.55).astype(np.uint8)
    im = Image.fromarray(arr)
    im.paste(logo.resize((420, 420), Image.LANCZOS), (70, 105))
    d = ImageDraw.Draw(im)
    d.text((540, 190), "Plan2Real", fill=(255, 255, 255), font=font(96, bold=True))
    tag = {"fr": ("Votre plan en grandeur réelle,", "au sol, en réalité augmentée."),
           "en": ("Your plan at full scale,", "on the floor, in augmented reality.")}[lang]
    d.text((544, 320), tag[0], fill=(255, 255, 255), font=font(44))
    d.text((544, 376), tag[1], fill=AMBER, font=font(44, bold=True))
    d.rectangle([544, 460, 1130, 466], fill=AMBER)
    d.text((544, 486), "iPhone · iOS 17+ · FR / EN", fill=(220, 220, 220), font=font(34))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    logo = Image.open(LOGO).convert("RGB")
    logo.resize((640, 640), Image.LANCZOS).save(OUT / "logo.jpg", quality=90)
    logo.resize((128, 128), Image.LANCZOS).save(OUT / "logo-mark.png")
    logo.resize((180, 180), Image.LANCZOS).save(ROOT / "assets" / "apple-touch-icon.png")
    logo.resize((32, 32), Image.LANCZOS).save(ROOT / "favicon.png")

    upscale(Image.open(BETON).convert("RGB"), 1920).save(OUT / "fond-beton.jpg", quality=82)
    upscale(Image.open(BOIS).convert("RGB").crop((125, 30, 984, 532)), 1920).save(OUT / "fond-bois.jpg", quality=82)

    plan = floor_plan()
    plan.save(OUT / "plan-exemple.png")
    plan_photo(plan).save(OUT / "plan-photo.jpg", quality=88)
    for lang in ("fr", "en"):
        ar_concept(plan, lang).save(OUT / f"{lang}-ausol.jpg", quality=86)
        rail_screen(plan, lang).save(OUT / f"{lang}-outils.jpg", quality=86)
    for lang in ("fr", "en"):
        og_image(lang, logo).save(OUT / f"og-image-{lang}.jpg", quality=88)
    print("Images générées dans", OUT)


if __name__ == "__main__":
    main()
