# Site Plan2Real

Site public de l'app Plan2Real (JDG inc.), bilingue FR/EN, sur le modèle du site SITE DIM.
Publié sur Netlify : https://plan2real.netlify.app

- `python3 tools/make_images.py` — régénère les images (logo, fonds, plan d'exemple, illustrations, partage)
  à partir du dépôt de l'app placé à côté (`../Plan2Real`).
- `python3 build.py` — régénère toutes les pages (`fr/`, `en/`), `sitemap.xml`, `robots.txt`, `netlify.toml`.
- Captures de l'app : `assets/img/{fr,en}-{intro,importer,redresser,echelle}.jpg` (simulateur iPhone 17 Pro).
- À la publication sur l'App Store : renseigner `APPSTORE_ID` dans `build.py`, relancer, commit + push.
