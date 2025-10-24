"""Visualization utilities for SEM image metadata.

Generates an HTML page that embeds the image (converted to PNG) and a table
with selected metadata. The page is written to a temp file and opened in the
default browser (Chrome if it's the system default).
"""
import json
import re
import base64
import tempfile
import webbrowser
from pathlib import Path
from html import escape
from PIL import Image

# Preferred feature keys to show (try instrument section first, then exif, then top-level)
FEATURES_TO_EXTRACT = [
    "AP_WD",
    "AP_BEAM_TIME",
    "AP_IMAGE_PIXEL_SIZE",
    "AP_HOLDER_HEIGHT",
    "AP_BEAM_CURRENT",
    "AP_HOLDER_DIAMETER",
]


def _load_metadata(md_file):
    try:
        with open(md_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print(f"Error: File '{md_file}' not found")
        return {}


def _find_feature_value(metadata, key):
    """Look for a feature value in several possible locations."""
    if isinstance(metadata, dict):
        if key in metadata:
            return metadata[key]
        inst = metadata.get("instrument") if "instrument" in metadata else None
        if isinstance(inst, dict) and key in inst:
            return inst[key]
        exif = metadata.get("exif") if "exif" in metadata else None
        if isinstance(exif, dict) and key in exif:
            return exif[key]
        # try without AP_ prefix
        alt = key.replace("AP_", "")
        if alt in metadata:
            return metadata[alt]
        if inst and alt in inst:
            return inst[alt]
    return None


def _parse_value_unit(value):
    if value is None:
        return "", ""
    if isinstance(value, (int, float)):
        return str(value), ""
    if isinstance(value, (list, tuple)) and value:
        value = value[0]
    s = str(value).strip()
    if "=" in s:
        s = s.split("=", 1)[1].strip()
    m = re.match(r"^([+-]?\d+[\d.,]*)(?:\s*)([A-Za-zµ%°\u00b0/\-\w]*)$", s)
    if m:
        val = m.group(1).replace(",", "")
        unit = m.group(2).strip()
        return val, unit
    return s, ""


def visualize_features(image_metadata_file, image_file):
    metadata = _load_metadata(image_metadata_file)

    features = {}
    for key in FEATURES_TO_EXTRACT:
        val = _find_feature_value(metadata, key)
        if val is not None:
            features[key] = val

    # If nothing matched, pick top non-empty keys from instrument or root
    if not features and isinstance(metadata, dict):
        inst = metadata.get("instrument") if "instrument" in metadata else None
        source = inst if isinstance(inst, dict) else metadata
        count = 0
        for k, v in source.items():
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            features[k] = v
            count += 1
            if count >= 50:
                break

    # Convert image to PNG base64
    try:
        with Image.open(image_file) as im:
            im = im.convert("RGBA")
            import io
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    except FileNotFoundError:
        print(f"Error: Image file '{image_file}' not found")
        return

    rows_html = []
    for k, v in features.items():
        val, unit = _parse_value_unit(v)
        rows_html.append(f"<tr><td>{escape(str(k))}</td><td>{escape(str(val))}</td><td>{escape(str(unit))}</td></tr>")

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset='utf-8'>
        <title>SEM Image + Metadata</title>
        <style>
          body {{ font-family: sans-serif; margin: 20px; }}
          .container {{ display: flex; gap: 20px; align-items: flex-start; }}
          .image {{ max-width: 65%; }}
          img {{ max-width: 100%; height: auto; border: 1px solid #ccc; }}
          table {{ border-collapse: collapse; width: 35%; max-width: 600px; }}
          th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
          th {{ background: #f4f4f4; }}
        </style>
      </head>
      <body>
        <h2>SEM Image and Metadata</h2>
        <div class='container'>
          <div class='image'><img src='data:image/png;base64,{img_b64}' alt='SEM image'/></div>
          <div class='meta'>
            <table>
              <thead><tr><th>Variable</th><th>Value</th><th>Unit</th></tr></thead>
              <tbody>
                {''.join(rows_html)}
              </tbody>
            </table>
          </div>
        </div>
      </body>
    </html>
    """

    tmp = Path(tempfile.gettempdir()) / f"sem_view_{Path(image_file).stem}.html"
    tmp.write_text(html, encoding="utf-8")
    webbrowser.open(tmp.as_uri())

    return