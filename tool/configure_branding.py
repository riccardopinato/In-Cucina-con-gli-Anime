from __future__ import annotations

from pathlib import Path

APP_NAME = "In Cucina con gli Anime"


def replace(path: str, replacements: dict[str, str]) -> None:
    file = Path(path)
    if not file.exists():
        return
    text = file.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    file.write_text(text, encoding="utf-8")


replace("android/app/src/main/AndroidManifest.xml", {
    'android:label="animekitchen"': f'android:label="{APP_NAME}"',
})
replace("ios/Runner/Info.plist", {
    "<string>animekitchen</string>": f"<string>{APP_NAME}</string>",
})
replace("web/index.html", {
    "<title>animekitchen</title>": f"<title>{APP_NAME}</title>",
    'content="animekitchen"': f'content="{APP_NAME}"',
})
replace("web/manifest.json", {
    '"name": "animekitchen"': f'"name": "{APP_NAME}"',
    '"short_name": "animekitchen"': '"short_name": "Anime Kitchen"',
})
