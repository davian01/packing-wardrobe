# 🧳 Packing & Wardrobe

A single-file, offline HTML app to track the clothes you own, a shopping /
exchange list, and saved outfits — built for packing trips.

## Use it

Open **`index.html`** in any browser (double-click, or open from your phone via
OneDrive). No server, no account, no internet needed. Your data is saved in the
browser's local storage on that device, plus a **Backup / Restore** button
(JSON) to move it between devices.

### What it does
- **To Pack / Packed** — tick items off as you pack; the counter updates.
- **Shopping** — things to buy or exchange (with quantity + "specific vs. idea").
  Hit **Got it →** to move a bought item into your wardrobe.
- **Outfits** — bundle pieces into a named look ("Beach day") and see how many
  of its items are already packed.
- **＋** — add any item: take/attach a photo (auto-shrunk), or flag a need.

Photos are stored **inside** the file/local storage as compressed JPEGs, so it
stays portable.

## Editing the seed / rebuilding

The starter wardrobe is baked into `index.html`. To change it, edit the
`have` / `need` tables in [`build/build.py`](build/build.py) and regenerate:

```bash
cd build
pip install pillow
python build.py        # rewrites ../index.html
```

Source photos live in `build/photos/`. Items with no photo show a placeholder
emoji (👟 shoes, 🛒 to-buy, 👕 everything else).

## Notes
- The Uniqlo shorts use official product images; the rest use personal photos.
  See item notes for SKUs / links.
- Data storage key is versioned (`packing_wardrobe_v3`); bumping it in the
  template reseeds from scratch.
