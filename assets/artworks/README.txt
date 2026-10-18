RETUTTA ARTWORKS
================

Place individual illustration files in this folder (JPG, PNG, or WebP).
Do not use multi-panel reference sheets here.

To add an artwork to the site:
1. Upload the image into this folder.
2. Open the root index.html and find `const ARTWORKS = [`.
3. Add an entry, for example:
   { file: "retutta-night.jpg", title: "Нічна магія", featured: true },
4. For more images, add more entries separated by commas.
5. Only one entry needs featured: true; it is used for the homepage hero.
   If none is featured, the first entry is used.
6. Commit the changes. GitHub Pages will publish automatically.

Important: GitHub Pages is static, so it cannot automatically detect new files
inside a folder. Each artwork must be added to the ARTWORKS list in index.html.
