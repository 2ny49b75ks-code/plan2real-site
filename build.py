#!/usr/bin/env python3
"""Génère le site Plan2Real (FR + EN) sur le modèle du site SITE DIM :
fr/ et en/ (accueil, fonctionnalités, téléchargement, contact, confidentialité),
assets/, sitemap.xml, robots.txt, netlify.toml et redirection de langue à la racine.

Images : `python3 tools/make_images.py` (logo, fonds, plan d'exemple, partage).
Captures de l'app : assets/img/{fr,en}-{intro,importer,redresser,echelle}.jpg.
Lancer `python3 build.py` après toute modification, puis commit + push : Netlify publie.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://plan2real.netlify.app"
EMAIL = "jdgeg@icloud.com"
TODAY = date.today().isoformat()
EFFECTIVE = {"fr": "15 octobre 2026", "en": "October 15, 2026"}

# Identifiant Apple de Plan2Real (App Store Connect → Informations sur l'app → Identifiant Apple).
# Tant qu'il est vide, les boutons affichent « Bientôt sur l'App Store ».
APPSTORE_ID = "6823348263"
APPSTORE = {l: f"https://apps.apple.com/ca/app/id{APPSTORE_ID}?l={l}-CA" for l in ("fr", "en")} if APPSTORE_ID else None
DEVELOPER = "https://apps.apple.com/ca/developer/id6796142518"

FILES = {
    "home": {"fr": "index.html", "en": "index.html"},
    "features": {"fr": "fonctionnalites.html", "en": "features.html"},
    "download": {"fr": "telechargement.html", "en": "download.html"},
    "contact": {"fr": "contact.html", "en": "contact.html"},
    "privacy": {"fr": "confidentialite.html", "en": "privacy.html"},
}
NAV_ORDER = ["home", "features", "download", "contact"]

T = {
    "fr": {
        "nav": {"home": "Accueil", "features": "Fonctionnalités", "download": "Téléchargement", "contact": "Contact",
                "privacy": "Confidentialité"},
        "cta": "Télécharger", "soon": "Bientôt sur l'App Store", "store": "Télécharger sur l'App Store",
        "footer": "© 2026 JDG inc. — Québec, Canada. Plan2Real est une marque de JDG inc.",
        "menu": "Menu", "locale": "fr_CA", "alt_locale": "en_CA",
    },
    "en": {
        "nav": {"home": "Home", "features": "Features", "download": "Download", "contact": "Contact", "privacy": "Privacy"},
        "cta": "Download", "soon": "Coming soon to the App Store", "store": "Download on the App Store",
        "footer": "© 2026 JDG inc. — Quebec, Canada. Plan2Real is a trademark of JDG inc.",
        "menu": "Menu", "locale": "en_CA", "alt_locale": "fr_CA",
    },
}

# Liens vers les autres apps de JDG inc. (pied de page), même bloc que les autres sites.
JDG_APPS = {
    "fr": ('<div class="jdg-apps" style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(127,127,127,.3);'
           'font-size:.88em;line-height:1.8;text-align:center"><strong>Les autres apps de JDG inc., Québec :</strong> '
           '<a href="https://sitedim.netlify.app/fr/index.html">SITE DIM</a> <span style="opacity:.75">(relevé de chantier en réalité augmentée)</span> · '
           '<a href="https://camordtu.netlify.app/">CaMordTu</a> <span style="opacity:.75">(guide de pêche au Québec)</span> · '
           '<a href="https://appmycreation.com/">MY CREATION</a> <span style="opacity:.75">(vos œuvres en relief 3D et en réalité augmentée)</span> · '
           '<a href="https://tricolab.netlify.app/fr/index.html">Tricolab</a> <span style="opacity:.75">(tricot, crochet et scrapbooking)</span> · '
           '<a href="https://apps.apple.com/ca/app/id6810440422?l=fr-CA">Acoustic Detector</a> <span style="opacity:.75">(mesure sonore et traitement acoustique)</span> · '
           '<a href="https://apps.apple.com/ca/app/id6811432420?l=fr-CA">Fort et Château</a> <span style="opacity:.75">(forts et châteaux du monde)</span></div>'),
    "en": ('<div class="jdg-apps" style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(127,127,127,.3);'
           'font-size:.88em;line-height:1.8;text-align:center"><strong>More apps by JDG inc., Quebec:</strong> '
           '<a href="https://sitedim.netlify.app/en/index.html">SITE DIM</a> <span style="opacity:.75">(AR construction measuring)</span> · '
           '<a href="https://camordtu.netlify.app/en.html">CaMordTu</a> <span style="opacity:.75">(Quebec fishing guide)</span> · '
           '<a href="https://appmycreation.com/index-en.html">MY CREATION</a> <span style="opacity:.75">(your artwork in 3D relief and AR)</span> · '
           '<a href="https://tricolab.netlify.app/en/index.html">Tricolab</a> <span style="opacity:.75">(knitting, crochet and scrapbooking)</span> · '
           '<a href="https://apps.apple.com/ca/app/id6810440422?l=en-CA">Acoustic Detector</a> <span style="opacity:.75">(sound measurement and acoustic treatment)</span> · '
           '<a href="https://apps.apple.com/ca/app/id6811432420?l=en-CA">Fort et Château</a> <span style="opacity:.75">(forts and castles of the world)</span></div>'),
}


# ----------------------------------------------------------------- contenu
HOME = {
    "fr": dict(
        title="Plan2Real — votre plan papier en grandeur réelle, au sol, en réalité augmentée",
        desc="Photographiez un plan papier, donnez son échelle et voyez-le au sol en grandeur réelle grâce à la réalité augmentée de votre iPhone. Pour entrepreneurs, clients et designers.",
        eyebrow="Plan papier · grandeur réelle · réalité augmentée",
        h1="Marchez dans votre plan avant de construire.",
        lead="Plan2Real transforme la photo d'un plan papier en plan posé au sol, en grandeur réelle, grâce à la réalité augmentée de votre iPhone. Voyez la vraie taille des pièces, des corridors et des portes en quelques minutes, sans portail web ni logiciel de dessin.",
        more="Voir les fonctionnalités",
        tagline="Votre plan en grandeur réelle",
        meta=[("iOS 17+", "requis"), ("iPhone", "LiDAR en bonus"), ("FR / EN", "bilingue"), ("Aucun", "compte")],
        callout="<strong>Un mot sur la précision.</strong> Plan2Real est un outil de visualisation, à titre indicatif : il ne remplace pas un arpenteur ni un plan d'implantation officiel. Sur de grandes surfaces, la réalité augmentée peut dériver de quelques centimètres; l'alignement sur deux repères réels (piquets, coins) sert justement à recaler le plan. Pour vérifier, l'écran affiche la cote A–B : mesurez-la au ruban.",
        h_steps="Du papier au plancher en six étapes", steps_eyebrow="Comment ça marche",
        steps=[("Photographiez le plan", "Appareil photo à pleine résolution (jusqu'à 48 Mpx), une image de Photos ou un PDF."),
               ("Redressez la feuille", "Les 4 coins sont détectés; ajustez-les avec la loupe. Les vraies proportions sont rétablies."),
               ("Donnez l'échelle", "Placez A et B sur une cote connue et entrez sa longueur, ou choisissez 1/4\" = 1', 1:50…"),
               ("Visez le sol", "La cible devient verte quand la position au sol est confirmée, comme dans SITE DIM."),
               ("Posez et ajustez", "Déplacez, tournez, montez ou baissez le plan, ajustez l'échelle au doigt, puis verrouillez."),
               ("Marchez et partagez", "Mesurez entre deux points, prenez une photo ou une vidéo, sauvegardez le projet.")],
        h_shots="L'app en images", shots_eyebrow="Captures",
        shots=[("intro", "Accueil", "Accueil de Plan2Real avec le choix de la langue"),
               ("importer", "Importer", "Écran Importer sur fond de contreplaqué, avec le plan photographié"),
               ("redresser", "Redresser", "Les quatre coins de la feuille détectés automatiquement"),
               ("echelle", "Échelle", "Repères A et B posés sur la cote de 36 pieds"),
               ("ausol", "Au sol", "Le plan posé au sol en grandeur réelle, en réalité augmentée")],
        h_who="Pour qui", who_eyebrow="Pensée pour le chantier",
        who=[("Entrepreneurs", "Montrez au client la vraie taille d'un agrandissement, vérifiez l'implantation d'un garage ou d'une terrasse avant de commander le béton."),
             ("Clients résidentiels et commerciaux", "Comprenez enfin le plan : marchez dans la future cuisine, voyez si le corridor est assez large, placez vos meubles."),
             ("Designers et architectes", "Présentez une esquisse sur le site même, en quelques minutes, sans maquette ni modèle 3D.")],
        specs=[("Plateforme", "iOS 17+"), ("Appareil", "iPhone · LiDAR en bonus"), ("Langues", "FR / EN"), ("Données", "Sur l'iPhone")],
        cta_h="Prêt à voir votre plan en vrai?", cta_p="Plan2Real arrive bientôt sur l'App Store, pour iPhone sous iOS 17 ou plus récent.",
        cta_btn="Voir la page de téléchargement",
    ),
    "en": dict(
        title="Plan2Real — your paper plan at full scale, on the floor, in augmented reality",
        desc="Photograph a paper plan, set its scale and see it on the floor at full scale with your iPhone's augmented reality. For contractors, clients and designers.",
        eyebrow="Paper plan · full scale · augmented reality",
        h1="Walk through your plan before you build.",
        lead="Plan2Real turns a photo of a paper plan into a plan laid on the floor, at full scale, with your iPhone's augmented reality. See the real size of rooms, hallways and doors in minutes, with no web portal and no drawing software.",
        more="See the features",
        tagline="Your plan at full scale",
        meta=[("iOS 17+", "required"), ("iPhone", "LiDAR a bonus"), ("FR / EN", "bilingual"), ("No", "account")],
        callout="<strong>A word on accuracy.</strong> Plan2Real is a visualization tool, for guidance only: it does not replace a land surveyor or an official layout plan. Over large areas, augmented reality can drift by a few centimetres; aligning on two real landmarks (stakes, corners) is there to correct it. To check, the screen shows the A–B dimension: measure it with a tape.",
        h_steps="From paper to floor in six steps", steps_eyebrow="How it works",
        steps=[("Photograph the plan", "Full-resolution camera (up to 48 MP), an image from Photos or a PDF."),
               ("Straighten the sheet", "The 4 corners are detected; fine-tune them with the magnifier. True proportions are restored."),
               ("Set the scale", "Place A and B on a known dimension and enter its length, or pick 1/4\" = 1', 1:50…"),
               ("Aim at the floor", "The target turns green once the floor position is confirmed, as in SITE DIM."),
               ("Place and adjust", "Move, rotate, raise or lower the plan, fine-tune the scale with your fingers, then lock it."),
               ("Walk and share", "Measure between two points, take a photo or video, save the project.")],
        h_shots="The app in pictures", shots_eyebrow="Screenshots",
        shots=[("intro", "Home", "Plan2Real home screen with the language choice"),
               ("importer", "Import", "Import screen on a plywood background, with the photographed plan"),
               ("redresser", "Straighten", "The four corners of the sheet detected automatically"),
               ("echelle", "Scale", "Landmarks A and B on the 36-foot dimension"),
               ("ausol", "On the floor", "The plan laid on the floor at full scale, in augmented reality")],
        h_who="Who it's for", who_eyebrow="Built for the job site",
        who=[("Contractors", "Show clients the real size of an addition, check a garage or deck layout before ordering concrete."),
             ("Residential and commercial clients", "Finally understand the plan: walk through the future kitchen, see if the hallway is wide enough, place your furniture."),
             ("Designers and architects", "Present a sketch right on site, in minutes, with no mock-up or 3D model.")],
        specs=[("Platform", "iOS 17+"), ("Device", "iPhone · LiDAR a bonus"), ("Languages", "FR / EN"), ("Data", "On the iPhone")],
        cta_h="Ready to see your plan for real?", cta_p="Plan2Real is coming soon to the App Store, for iPhone with iOS 17 or later.",
        cta_btn="See the download page",
    ),
}

FEATURES = {
    "fr": dict(
        title="Fonctionnalités — Plan2Real", desc="Import d'un plan à pleine résolution, redressement automatique, échelle par cote connue, pose au sol stable avec cible verte, outils au sol, sauvegarde de l'emplacement.",
        h1="Tout ce que fait Plan2Real", intro="Un parcours simple, de la photo du plan jusqu'au plan posé au sol, puis des outils pour l'ajuster et le partager.",
        rows=[
            ("importer", None, "Importer le plan",
             "Photographiez la feuille ou choisissez un fichier : l'app garde toute la netteté du plan.",
             ["Appareil photo à la résolution maximale du capteur (48 Mpx sur les iPhone Pro), priorité à la qualité, sans flash", "Image de Photos ou fichier (PDF ou image)", "PDF : le format réel de la page est lu, l'échelle s'applique directement", "Vos projets sauvegardés sont dans « Mes projets »"]),
            ("redresser", None, "Redresser la feuille",
             "Une photo prise de biais devient un plan bien droit, aux vraies proportions.",
             ["Détection automatique de la feuille, même posée sur un panneau ou une table", "4 poignées et une loupe pour viser chaque coin au pixel près", "Les vraies proportions de la feuille sont rétablies, même photographiée en angle", "« Image entière » pour un plan déjà droit (capture d'écran, numérisation)"]),
            ("echelle", None, "Donner l'échelle",
             "L'échelle se demande à l'utilisateur plutôt que de la deviner : c'est plus fiable.",
             ["Distance connue : A et B sur une cote du plan, puis sa longueur en mètres ou en pieds-pouces", "Échelles courantes : 1/16\" à 1\" = 1', 1:20 à 1:500, ou 1:N", "Formats de feuille : Lettre, Légal, Tabloïd, ARCH C à E, A4 à A0", "Les dimensions réelles du plan s'affichent avant de passer au sol"]),
            ("ausol", None, "Poser le plan au sol",
             "La même méthode de visée que SITE DIM : le plan se pose sur la vraie surface, pas dans les airs.",
             ["Cible fixe au centre : blanche, puis verte quand la position au sol est confirmée", "LiDAR en priorité, sinon plan détecté par ARKit; jamais une simple estimation", "Moyenne de plusieurs visées : un reflet ou un rebord ne fausse pas la hauteur", "Le plan est ancré à l'endroit réel et reste stable en marchant"]),
        ],
        h_rail="Les outils au sol", rail_intro="Une colonne de boutons ronds à gauche de l'écran, comme dans SITE DIM. Le nom de la fonction s'affiche 2 secondes, puis disparaît : rien ne cache le plan.",
        rail=[("✥", "Déplacer : glissez un doigt"), ("↻", "Tourner : glissez à gauche ou à droite, ou deux doigts"),
              ("↕", "Hauteur : monter ou baisser le plan, au centimètre"), ("🤏", "Échelle au doigt : pincez pour caler une cote sur un ruban au sol"),
              ("↔", "Ajuster l'échelle sur une cote réelle (ex. porte de 36 po)"), ("🔒", "Verrou : plus aucun geste ne bouge le plan"),
              ("📏", "Mesurer entre deux points au sol"), ("◐", "Opacité du plan"),
              ("📷", "Photo à partager"), ("•••", "Vidéo, alignement sur 2 repères, quart de tour, replacer")],
        h_save="Sauvegarder et revenir sur place",
        save=["Le bouton « Sauvegarder » enregistre le plan, son échelle, les repères A et B et son emplacement au sol",
              "En rouvrant le projet sur place, ARKit reconnaît les lieux et le plan se replace tout seul",
              "Tout reste sur l'iPhone : aucun compte, aucun serveur, aucune publicité"],
        h_limits="Bon à savoir", limits=[
            ("Sols difficiles", "Neige, sol mouillé ou lustré, gravier uniforme et faible lumière gênent la réalité augmentée. Visez une zone texturée et sans reflet; la lampe s'allume toute seule dans le noir."),
            ("Grandes surfaces", "Sur un terrain, la réalité augmentée peut dériver. Alignez le plan sur deux repères réels (piquets, coins) pour le recaler."),
            ("Plans photocopiés", "Une impression ou une photocopie déforme l'échelle : la méthode « distance connue » corrige ce problème.")],
    ),
    "en": dict(
        title="Features — Plan2Real", desc="Full-resolution plan import, automatic straightening, scale from a known dimension, stable floor placement with a green target, on-floor tools, saved location.",
        h1="Everything Plan2Real does", intro="A simple path, from the photo of the plan to the plan laid on the floor, then tools to adjust and share it.",
        rows=[
            ("importer", None, "Import the plan",
             "Photograph the sheet or pick a file: the app keeps all of the plan's sharpness.",
             ["Camera at the sensor's maximum resolution (48 MP on iPhone Pro), quality first, no flash", "An image from Photos or a file (PDF or image)", "PDF: the real page size is read, so a scale applies directly", "Your saved projects are in “My projects”"]),
            ("redresser", None, "Straighten the sheet",
             "A photo taken at an angle becomes a straight plan, with its true proportions.",
             ["Automatic sheet detection, even on a board or a table", "4 handles and a magnifier to aim at each corner precisely", "The sheet's true proportions are restored, even when shot at an angle", "“Whole image” for a plan that is already straight (screenshot, scan)"]),
            ("echelle", None, "Set the scale",
             "The scale is asked from the user rather than guessed: it's more reliable.",
             ["Known distance: A and B on a dimension of the plan, then its length in meters or feet-inches", "Common scales: 1/16\" to 1\" = 1', 1:20 to 1:500, or 1:N", "Sheet sizes: Letter, Legal, Tabloid, ARCH C to E, A4 to A0", "The plan's real size is shown before you go to the floor"]),
            ("ausol", None, "Lay the plan on the floor",
             "The same aiming method as SITE DIM: the plan sits on the real surface, not in mid-air.",
             ["Fixed target in the center: white, then green once the floor position is confirmed", "LiDAR first, otherwise a plane detected by ARKit; never a mere estimate", "Several aims are averaged: a reflection or a ledge can't throw off the height", "The plan is anchored to the real spot and stays put as you walk"]),
        ],
        h_rail="On-floor tools", rail_intro="A column of round buttons on the left of the screen, as in SITE DIM. The function's name shows for 2 seconds, then fades: nothing hides the plan.",
        rail=[("✥", "Move: drag one finger"), ("↻", "Rotate: drag left or right, or use two fingers"),
              ("↕", "Height: raise or lower the plan, to the centimetre"), ("🤏", "Finger scale: pinch to match a dimension with a tape on the floor"),
              ("↔", "Adjust the scale to a real dimension (e.g. a 36-inch door)"), ("🔒", "Lock: no gesture moves the plan anymore"),
              ("📏", "Measure between two points on the floor"), ("◐", "Plan opacity"),
              ("📷", "Photo to share"), ("•••", "Video, two-landmark alignment, quarter turn, place again")],
        h_save="Save and come back on site",
        save=["The “Save” button stores the plan, its scale, landmarks A and B and its location on the floor",
              "Reopen the project on site: ARKit recognizes the place and the plan puts itself back",
              "Everything stays on the iPhone: no account, no server, no ads"],
        h_limits="Good to know", limits=[
            ("Difficult floors", "Snow, wet or glossy floors, uniform gravel and low light make augmented reality harder. Aim at a textured area without reflections; the torch turns on by itself in the dark."),
            ("Large areas", "On a lot, augmented reality can drift. Align the plan on two real landmarks (stakes, corners) to correct it."),
            ("Photocopied plans", "Printing or photocopying distorts the scale: the “known distance” method corrects it.")],
    ),
}

DOWNLOAD = {
    "fr": dict(
        title="Téléchargement — Plan2Real", desc="Plan2Real arrive bientôt sur l'App Store pour iPhone (iOS 17 ou plus récent).",
        h1="Télécharger Plan2Real", intro="Plan2Real arrive bientôt sur l'App Store, pour iPhone.",
        status_h="Disponibilité", status="En préparation pour l'App Store. Cette page affichera le lien de téléchargement dès la sortie.",
        others="En attendant, découvrez les autres apps de JDG inc. sur l'App Store :", others_link="Voir les apps de JDG inc.",
        faq_h="Avant de télécharger",
        faq=[("Mon iPhone est-il compatible ?", "Plan2Real fonctionne sur les iPhone compatibles avec la réalité augmentée (ARKit), sous iOS 17 ou plus récent. Un iPhone Pro avec capteur LiDAR pose le plan plus vite et plus précisément, surtout sur un sol difficile."),
             ("Quels plans puis-je utiliser ?", "Une photo d'un plan papier, une image de Photos ou un fichier PDF. Pour un PDF, le format réel de la page est lu automatiquement."),
             ("Est-ce précis ?", "C'est un outil de visualisation, à titre indicatif. L'écran affiche la cote A–B pour la vérifier au ruban, et l'alignement sur deux repères réels recale le plan sur un grand terrain."),
             ("Ça marche dehors ?", "Oui, sur un sol avec de la texture (asphalte, béton brut, gazon court). La neige, l'eau et les sols lustrés créent des reflets qui gênent la réalité augmentée."),
             ("Faut-il un compte ?", "Non. Aucun compte, aucune publicité, aucun traceur : vos projets restent sur votre iPhone."),
             ("En quelles langues ?", "En français et en anglais, avec un bouton FR / EN sur l'écran d'accueil."),
             ("Et sur Android ?", "Pas pour l'instant : Plan2Real est seulement sur iPhone."),
             ("Comment obtenir de l'aide ?", f'Écrivez-nous à <a href="mailto:{EMAIL}">{EMAIL}</a> ou consultez la page <a href="contact.html">Contact</a>.')],
    ),
    "en": dict(
        title="Download — Plan2Real", desc="Plan2Real is coming soon to the App Store for iPhone (iOS 17 or later).",
        h1="Download Plan2Real", intro="Plan2Real is coming soon to the App Store, for iPhone.",
        status_h="Availability", status="Being prepared for the App Store. This page will show the download link as soon as it's out.",
        others="In the meantime, discover the other JDG inc. apps on the App Store:", others_link="See JDG inc. apps",
        faq_h="Before you download",
        faq=[("Is my iPhone compatible?", "Plan2Real runs on iPhones that support augmented reality (ARKit), with iOS 17 or later. An iPhone Pro with a LiDAR sensor places the plan faster and more precisely, especially on difficult floors."),
             ("Which plans can I use?", "A photo of a paper plan, an image from Photos or a PDF file. For a PDF, the real page size is read automatically."),
             ("Is it accurate?", "It's a visualization tool, for guidance only. The screen shows the A–B dimension so you can check it with a tape, and aligning on two real landmarks corrects the plan on a large lot."),
             ("Does it work outdoors?", "Yes, on a floor with texture (asphalt, raw concrete, short grass). Snow, water and glossy floors create reflections that confuse augmented reality."),
             ("Do I need an account?", "No. No account, no ads, no trackers: your projects stay on your iPhone."),
             ("Which languages?", "English and French, with an FR / EN button on the home screen."),
             ("What about Android?", "Not at the moment: Plan2Real is for iPhone only."),
             ("How do I get help?", f'Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> or visit the <a href="contact.html">Contact</a> page.')],
    ),
}

CONTACT = {
    "fr": dict(title="Contact et assistance — Plan2Real", desc="Aide, questions fréquentes et contact pour l'app Plan2Real.", h1="Contact et assistance",
               mail_h="Nous écrire", mail_p="Précisez si possible votre modèle d'iPhone, votre version d'iOS et le type de sol (intérieur, extérieur). Chaque message est lu.",
               biz_h="Entreprise", biz="JDG inc. · Québec, Canada",
               qr_h="Partager l'app", qr_p="Scannez ce code pour ouvrir le site de Plan2Real sur un autre téléphone.",
               faq_h="Questions fréquentes",
               faq=[("Le plan flotte au-dessus du sol", "Visez le plancher (pas un meuble) et attendez que la cible devienne verte avant de placer le plan. Ensuite, le bouton Hauteur permet de le monter ou de le baisser au centimètre."),
                    ("Le plan semble trop petit ou trop grand", "Vérifiez la cote A–B à l'étape Échelle. Au sol, utilisez « Ajuster l'échelle » sur une cote connue (une porte de 36 po) ou l'échelle au doigt avec un ruban posé au sol."),
                    ("Le plan bouge quand je marche", "Touchez le bouton Verrou : plus aucun geste ne le déplace. Sur un grand terrain, alignez-le sur deux repères réels."),
                    ("La photo du plan est floue", "Prenez la photo avec l'appareil de Plan2Real, bien à plat, de face et sans reflet : il utilise la pleine résolution du capteur.")]),
    "en": dict(title="Contact and support — Plan2Real", desc="Help, frequently asked questions and contact for the Plan2Real app.", h1="Contact and support",
               mail_h="Write to us", mail_p="If you can, tell us your iPhone model, your iOS version and the type of floor (indoor, outdoor). Every message is read.",
               biz_h="Company", biz="JDG inc. · Quebec, Canada",
               qr_h="Share the app", qr_p="Scan this code to open the Plan2Real website on another phone.",
               faq_h="Frequently asked questions",
               faq=[("The plan floats above the floor", "Aim at the floor (not furniture) and wait for the target to turn green before placing the plan. Then the Height button lets you raise or lower it to the centimetre."),
                    ("The plan looks too small or too big", "Check the A–B dimension at the Scale step. On the floor, use “Adjust scale” on a known dimension (a 36-inch door) or the finger scale with a tape on the floor."),
                    ("The plan moves when I walk", "Tap the Lock button: no gesture moves it anymore. On a large lot, align it on two real landmarks."),
                    ("The photo of the plan is blurry", "Take the photo with Plan2Real's camera, flat, straight on and without glare: it uses the sensor's full resolution.")]),
}

PRIVACY = {
    "fr": dict(
        title="Politique de confidentialité — Plan2Real", desc="Plan2Real ne collecte aucune donnée personnelle : tout reste sur votre iPhone.",
        h1="Politique de confidentialité",
        note="En bref : Plan2Real ne collecte, ne transmet et ne vend aucune donnée personnelle. Vos plans et vos projets restent sur votre iPhone.",
        sections=[
            ("Qui sommes-nous", f'Plan2Real est une application éditée par JDG inc., au Québec (Canada). Pour toute question sur cette politique : <a href="mailto:{EMAIL}?subject=Plan2Real%20-%20Confidentialit%C3%A9">{EMAIL}</a>.'),
            ("Les données que nous collectons", "Aucune. L'app n'a pas de compte utilisateur, pas de serveur à nous, pas de publicité, pas d'outil de mesure d'audience ni de traceur, et n'intègre aucun service tiers."),
            ("Caméra", "La caméra sert à photographier vos plans, quand vous le demandez, et à afficher le plan au sol en réalité augmentée. Les images de la réalité augmentée sont traitées sur l'appareil et ne sont ni enregistrées ni envoyées, sauf la photo ou la vidéo que vous choisissez de prendre."),
            ("Ce qui est enregistré sur votre iPhone", "Quand vous touchez « Sauvegarder », l'app enregistre dans son propre espace sur l'iPhone : l'image du plan, son échelle, les repères A et B et une carte de réalité augmentée des lieux (pour replacer le plan au même endroit). Cette carte décrit des points de repère visuels de l'environnement; elle ne contient pas de photos et ne quitte pas l'appareil. Nous n'y avons pas accès."),
            ("Photos", "Pour importer un plan, l'app utilise le sélecteur de photos du système : elle ne reçoit que l'image que vous choisissez. Pour enregistrer une photo ou une vidéo du plan au sol, elle demande seulement la permission d'ajouter des éléments à Photos."),
            ("Fichiers", "Un plan PDF ou une image choisi dans Fichiers est lu sur l'appareil, uniquement quand vous le sélectionnez."),
            ("Sauvegardes", "Si vous avez activé la sauvegarde de votre appareil (iCloud ou ordinateur), les données de l'app en font partie. Ces sauvegardes sont gérées par Apple selon sa propre politique de confidentialité."),
            ("Partage", "Quand vous partagez une photo ou une vidéo, c'est vous qui choisissez l'app ou la personne destinataire. Ce contenu est alors soumis aux règles du service choisi."),
            ("Code QR", "Le code QR affiché dans l'app mène à l'App Store. Il ne transmet aucune information sur vous."),
            ("Enfants", "Plan2Real convient à tous les âges et ne collecte aucune donnée, y compris auprès des enfants."),
            ("Supprimer vos données", "Vous pouvez supprimer un projet à tout moment dans « Mes projets ». Supprimer l'app efface toutes ses données de l'appareil."),
            ("Modifications", "Si cette politique change, la nouvelle version sera publiée sur cette page avec sa date d'entrée en vigueur."),
        ],
    ),
    "en": dict(
        title="Privacy Policy — Plan2Real", desc="Plan2Real collects no personal data: everything stays on your iPhone.",
        h1="Privacy Policy",
        note="In short: Plan2Real does not collect, transmit or sell any personal data. Your plans and projects stay on your iPhone.",
        sections=[
            ("Who we are", f'Plan2Real is an app published by JDG inc., in Québec (Canada). For any question about this policy: <a href="mailto:{EMAIL}?subject=Plan2Real%20-%20Privacy">{EMAIL}</a>.'),
            ("Data we collect", "None. The app has no user account, no server of ours, no advertising, no analytics and no trackers, and includes no third-party services."),
            ("Camera", "The camera is used to photograph your plans, when you ask for it, and to show the plan on the floor in augmented reality. Augmented-reality images are processed on the device and are neither recorded nor sent, except for the photo or video you choose to take."),
            ("What is stored on your iPhone", "When you tap “Save”, the app stores in its own space on the iPhone: the plan image, its scale, landmarks A and B and an augmented-reality map of the place (to put the plan back in the same spot). This map describes visual landmarks of the surroundings; it contains no photos and never leaves the device. We have no access to it."),
            ("Photos", "To import a plan, the app uses the system photo picker: it receives only the image you choose. To save a photo or video of the plan on the floor, it asks only for permission to add items to Photos."),
            ("Files", "A PDF or image plan chosen in Files is read on the device, only when you select it."),
            ("Backups", "If you have turned on device backups (iCloud or computer), the app's data is part of them. Those backups are handled by Apple under its own privacy policy."),
            ("Sharing", "When you share a photo or video, you choose the app or person that receives it. That content is then subject to the rules of the service you chose."),
            ("QR code", "The QR code shown in the app leads to the App Store. It transmits no information about you."),
            ("Children", "Plan2Real is suitable for all ages and collects no data, including from children."),
            ("Deleting your data", "You can delete a project at any time in “My projects”. Deleting the app erases all of its data from the device."),
            ("Changes", "If this policy changes, the new version will be published on this page with its effective date."),
        ],
    ),
}

DATE_LABEL = {"fr": "En vigueur le", "en": "Effective"}


# ----------------------------------------------------------------- gabarit
def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def page(lang, key, title, desc, body, jsonld=None):
    t = T[lang]
    other = "en" if lang == "fr" else "fr"
    nav = "".join(
        f'<li><a href="{FILES[k][lang]}"{" aria-current=\"page\"" if k == key else ""}>{t["nav"][k]}</a></li>' for k in NAV_ORDER)
    foot = "".join(f'<li><a href="{FILES[k][lang]}">{t["nav"][k]}</a></li>' for k in NAV_ORDER + ["privacy"])
    sw_fr = f'<a href="{"" if lang == "fr" else "../fr/"}{FILES[key]["fr"]}" hreflang="fr" lang="fr"{" class=\"active\"" if lang == "fr" else ""}>FR</a>'
    sw_en = f'<a href="{"" if lang == "en" else "../en/"}{FILES[key]["en"]}" hreflang="en" lang="en"{" class=\"active\"" if lang == "en" else ""}>EN</a>'
    canon = f"{SITE}/{lang}/{'' if key == 'home' else FILES[key][lang]}"
    alt = {l: f"{SITE}/{l}/{'' if key == 'home' else FILES[key][l]}" for l in ("fr", "en")}
    og = f"{SITE}/assets/img/og-image-{lang}.jpg"
    ld = f'<script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n</script>\n' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="fr" href="{alt['fr']}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="x-default" href="{alt['fr']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Plan2Real">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{t['alt_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#14213D">
{ld}<link rel="icon" href="../favicon.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

<header class="site-header">
  <div class="container site-header__row">
    <a href="index.html" class="brand"><img src="../assets/img/logo-mark.png" alt="" class="brand-mark" width="38" height="38">Plan2Real</a>
    <nav class="main-nav" id="main-nav" aria-label="{t['menu']}">
      <ul class="main-nav__links">{nav}</ul>
    </nav>
    <div class="header-actions">
      <div class="lang-switch">{sw_fr}{sw_en}</div>
      <a href="{FILES['download'][lang]}" class="btn btn--primary">{t['cta']}</a>
      <button class="nav-toggle" aria-label="{t['menu']}" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="site-footer__row">
      <a href="index.html" class="site-footer__brand"><img src="../assets/img/logo-mark.png" alt="" class="brand-mark" width="30" height="30">Plan2Real</a>
      <nav><ul>{foot}</ul></nav>
    </div>
    {JDG_APPS[lang]}
    <div class="site-footer__meta">{t['footer']}</div>
  </div>
</footer>

<script src="../assets/js/main.js"></script>
</body>
</html>
"""


def store_button(lang):
    t = T[lang]
    if APPSTORE:
        return f'<a href="{APPSTORE[lang]}" class="btn btn--primary" target="_blank" rel="noopener">{t["store"]}</a>'
    return f'<span class="btn btn--soon">{t["soon"]}</span>'


def shot_src(lang, key):
    return f"../assets/img/{lang}-{key}.jpg"


def jsonld(lang):
    data = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "Plan2Real",
        "operatingSystem": "iOS 17+", "applicationCategory": "BusinessApplication",
        "url": f"{SITE}/{lang}/", "description": HOME[lang]["desc"], "inLanguage": ["fr", "en"],
        "image": f"{SITE}/assets/img/logo.jpg",
        "publisher": {"@type": "Organization", "name": "JDG inc.",
                      "address": {"@type": "PostalAddress", "addressRegion": "Québec", "addressCountry": "CA"}},
    }
    if APPSTORE:
        data["installUrl"] = APPSTORE[lang]
    return data


def page_hero(eyebrow, h1, intro):
    return f"""<section class="page-hero">
  <div class="container">
    {f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}
    <h1>{h1}</h1>
    <p class="lead">{intro}</p>
  </div>
</section>
<div class="grid-band"></div>"""


# ----------------------------------------------------------------- pages
def home(lang):
    h = HOME[lang]
    meta = "".join(f"<span><strong>{a}</strong> {b}</span>" for a, b in h["meta"])
    steps = "".join(f'<div class="step card"><h3>{a}</h3><p>{b}</p></div>' for a, b in h["steps"])
    shots = "".join(
        f'<figure><div class="phone"><img src="{shot_src(lang, k)}" alt="{esc(alt)}" loading="lazy" width="600" height="1304"></div>'
        f'<figcaption>{cap}</figcaption></figure>' for k, cap, alt in h["shots"])
    who = "".join(f'<div class="card card--feature"><h3>{a}</h3><p>{b}</p></div>' for a, b in h["who"])
    specs = "".join(f'<div class="specs__item"><div class="label">{a}</div><div class="value">{b}</div></div>' for a, b in h["specs"])
    body = f"""<section class="hero">
  <div class="container hero__grid">
    <div>
      <p class="eyebrow">{h['eyebrow']}</p>
      <h1>{h['h1']}</h1>
      <p class="lead">{h['lead']}</p>
      <div class="hero__actions">{store_button(lang)}<a href="{FILES['features'][lang]}" class="btn btn--outline">{h['more']}</a></div>
      <div class="hero__meta">{meta}</div>
    </div>
    <div class="hero__visual">
      <img class="logo" src="../assets/img/logo.jpg" alt="Plan2Real" width="640" height="640">
      <p class="hero__tagline">{h['tagline']}</p>
    </div>
  </div>
</section>

<div class="grid-band"></div>

<section class="section--tight">
  <div class="container">
    <div class="callout"><p>{h['callout']}</p></div>
  </div>
</section>

<section class="section--wood">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{h['steps_eyebrow']}</p>
      <h2>{h['h_steps']}</h2>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section--alt">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{h['shots_eyebrow']}</p>
      <h2>{h['h_shots']}</h2>
    </div>
    <div class="shots">{shots}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{h['who_eyebrow']}</p>
      <h2>{h['h_who']}</h2>
    </div>
    <div class="grid-3">{who}</div>
  </div>
</section>

<section class="section--alt section--tight">
  <div class="container">
    <div class="specs">{specs}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <h2>{h['cta_h']}</h2>
      <p>{h['cta_p']}</p>
      <a href="{FILES['download'][lang]}" class="btn btn--primary">{h['cta_btn']}</a>
    </div>
  </div>
</section>"""
    return page(lang, "home", h["title"], h["desc"], body, jsonld=jsonld(lang))


def features(lang):
    f = FEATURES[lang]
    rows = []
    for i, (key, _, title, text, items) in enumerate(f["rows"]):
        flip = " feature-row--flip" if i % 2 else ""
        bullets = "".join(f"<li>{x}</li>" for x in items)
        rows.append(f"""<div class="feature-row{flip}">
      <div class="feature-row__media"><div class="phone"><img src="{shot_src(lang, key)}" alt="{esc(title)}" loading="lazy" width="600" height="1304"></div></div>
      <div><h2>{title}</h2><p class="lead">{text}</p><ul class="feature-list">{bullets}</ul></div>
    </div>""")
    rail = "".join(f'<li><span class="dot{" dot--on" if i == 0 else ""}">{icon}</span>{label}</li>' for i, (icon, label) in enumerate(f["rail"]))
    save = "".join(f"<li>{x}</li>" for x in f["save"])
    limits = "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in f["limits"])
    body = f"""{page_hero(None, f['h1'], f['intro'])}

<section>
  <div class="container">
    {''.join(rows)}
  </div>
</section>

<section class="section--alt">
  <div class="container feature-row">
    <div class="feature-row__media"><div class="phone"><img src="../assets/img/{lang}-outils.jpg" alt="{esc(f['h_rail'])}" loading="lazy" width="1080" height="1920"></div></div>
    <div>
      <h2>{f['h_rail']}</h2>
      <p class="lead">{f['rail_intro']}</p>
      <ul class="rail-legend">{rail}</ul>
    </div>
  </div>
</section>

<section class="section--wood">
  <div class="container grid-2">
    <div class="card"><h3>{f['h_save']}</h3><ul class="feature-list">{save}</ul></div>
    <div class="card"><h3>{f['h_limits']}</h3>{''.join(f'<p><strong>{a}.</strong> {b}</p>' for a, b in f['limits'])}</div>
  </div>
</section>"""
    return page(lang, "features", f["title"], f["desc"], body)


def download(lang):
    d = DOWNLOAD[lang]
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in d["faq"])
    body = f"""{page_hero(None, d['h1'], d['intro'])}

<section class="section--tight">
  <div class="container grid-2">
    <div class="card">
      <h3>{d['status_h']}</h3>
      <p>{d['status']}</p>
      <div class="hero__actions" style="margin:22px 0 0">{store_button(lang)}</div>
    </div>
    <div class="card">
      <h3>JDG inc.</h3>
      <p>{d['others']}</p>
      <a href="{DEVELOPER}" class="btn btn--outline" target="_blank" rel="noopener">{d['others_link']}</a>
    </div>
  </div>
</section>

<section class="section--alt">
  <div class="container">
    <div class="section-head"><h2>{d['faq_h']}</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>"""
    return page(lang, "download", d["title"], d["desc"], body)


def contact(lang):
    c = CONTACT[lang]
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faq"])
    body = f"""{page_hero(None, c['h1'], c['mail_p'])}

<section class="section--tight">
  <div class="container grid-3">
    <div class="card">
      <h3>{c['mail_h']}</h3>
      <p><a class="btn btn--primary" href="mailto:{EMAIL}?subject=Plan2Real">{EMAIL}</a></p>
    </div>
    <div class="card">
      <h3>{c['biz_h']}</h3>
      <p>{c['biz']}</p>
    </div>
    <div class="card qr-card">
      <img src="../assets/img/qr-site.png" alt="QR" width="132" height="132">
      <div><h3>{c['qr_h']}</h3><p>{c['qr_p']}</p></div>
    </div>
  </div>
</section>

<section class="section--alt">
  <div class="container">
    <div class="section-head"><h2>{c['faq_h']}</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>"""
    return page(lang, "contact", c["title"], c["desc"], body)


def privacy(lang):
    p = PRIVACY[lang]
    sections = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in p["sections"])
    body = f"""{page_hero(None, p['h1'], f"{DATE_LABEL[lang]} {EFFECTIVE[lang]}")}

<section>
  <div class="container prose">
    <p class="note">{p['note']}</p>
    {sections}
  </div>
</section>"""
    return page(lang, "privacy", p["title"], p["desc"], body)


ROOT_INDEX = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=fr/index.html">
<title>Plan2Real</title>
<link rel="icon" href="favicon.png">
<script>
  (function () {
    var lang = (navigator.language || "fr").toLowerCase();
    var dest = lang.indexOf("fr") === 0 ? "fr/index.html" : "en/index.html";
    window.location.replace(dest);
  })();
</script>
</head>
<body>
  <p><a href="fr/index.html">Français</a> — <a href="en/index.html">English</a></p>
</body>
</html>
"""

NETLIFY = """[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Adresses courtes (App Store Connect : assistance et confidentialité)
[[redirects]]
  from = "/support"
  to = "/fr/contact.html"
  status = 301

[[redirects]]
  from = "/privacy"
  to = "/en/privacy.html"
  status = 301

[[redirects]]
  from = "/confidentialite"
  to = "/fr/confidentialite.html"
  status = 301

[[redirects]]
  from = "/en"
  to = "/en/index.html"
  status = 301

[[redirects]]
  from = "/fr"
  to = "/fr/index.html"
  status = 301
"""


def make_qr():
    """Code QR du site (page Contact), généré par CoreImage via un petit script Swift."""
    import subprocess
    import tempfile
    out = ROOT / "assets" / "img" / "qr-site.png"
    script = """
import CoreImage
import CoreImage.CIFilterBuiltins
import AppKit
let filter = CIFilter.qrCodeGenerator()
filter.message = Data(CommandLine.arguments[1].utf8)
filter.correctionLevel = "M"
let image = filter.outputImage!.transformed(by: CGAffineTransform(scaleX: 10, y: 10))
let rep = NSBitmapImageRep(cgImage: CIContext().createCGImage(image, from: image.extent)!)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[2]))
"""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "qr.swift"
        path.write_text(script)
        subprocess.run(["swift", str(path), SITE + "/", str(out)], check=True, capture_output=True)


def main():
    for lang in ("fr", "en"):
        folder = ROOT / lang
        folder.mkdir(exist_ok=True)
        pages = {"home": home, "features": features, "download": download, "contact": contact, "privacy": privacy}
        for key, build in pages.items():
            (folder / FILES[key][lang]).write_text(build(lang), encoding="utf-8")
    (ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    (ROOT / "netlify.toml").write_text(NETLIFY, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    urls = []
    for key in FILES:
        for lang in ("fr", "en"):
            loc = f"{SITE}/{lang}/{'' if key == 'home' else FILES[key][lang]}"
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{"" if key == "home" else FILES[key][l]}"/>' for l in ("fr", "en"))
            urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    if not (ROOT / "assets" / "img" / "qr-site.png").exists():
        make_qr()
    print("Site généré :", sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("*/*.html")))


if __name__ == "__main__":
    main()
