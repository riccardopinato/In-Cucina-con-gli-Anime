from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KTS = ROOT / "android" / "app" / "build.gradle.kts"
GROOVY = ROOT / "android" / "app" / "build.gradle"
MARKER = "ANIMEKITCHEN_PERSISTENT_SIGNING"


def patch_kotlin_dsl(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False

    debug_line = '            signingConfig = signingConfigs.getByName("debug")'
    if debug_line not in text:
        raise RuntimeError(
            "Flutter Android Kotlin template changed: debug signing line not found"
        )

    if not text.startswith("plugins {"):
        raise RuntimeError(
            "Flutter Android Kotlin template changed: plugins block not found"
        )

    prelude = f"""// {MARKER}
import java.io.FileInputStream
import java.util.Properties

val animeKitchenKeystoreProperties = Properties()
val animeKitchenKeystorePropertiesFile = rootProject.file("key.properties")
if (animeKitchenKeystorePropertiesFile.exists()) {{
    FileInputStream(animeKitchenKeystorePropertiesFile).use {{
        animeKitchenKeystoreProperties.load(it)
    }}
}}

"""
    text = prelude + text

    build_types_anchor = "    buildTypes {\n"
    if build_types_anchor not in text:
        raise RuntimeError(
            "Flutter Android Kotlin template changed: buildTypes block not found"
        )

    signing_block = """    signingConfigs {
        if (animeKitchenKeystorePropertiesFile.exists()) {
            create("persistentRelease") {
                keyAlias =
                    animeKitchenKeystoreProperties["keyAlias"] as String
                keyPassword =
                    animeKitchenKeystoreProperties["keyPassword"] as String
                storeFile = file(
                    animeKitchenKeystoreProperties["storeFile"] as String
                )
                storePassword =
                    animeKitchenKeystoreProperties["storePassword"] as String
            }
        }
    }

"""
    text = text.replace(
        build_types_anchor,
        signing_block + build_types_anchor,
        1,
    )

    replacement = """            signingConfig =
                if (animeKitchenKeystorePropertiesFile.exists()) {
                    signingConfigs.getByName("persistentRelease")
                } else {
                    signingConfigs.getByName("debug")
                }"""
    text = text.replace(debug_line, replacement, 1)
    path.write_text(text, encoding="utf-8")
    return True


def patch_groovy(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False

    debug_line = "            signingConfig signingConfigs.debug"
    if debug_line not in text:
        raise RuntimeError(
            "Flutter Android Groovy template changed: debug signing line not found"
        )

    prelude = f"""// {MARKER}
def animeKitchenKeystoreProperties = new Properties()
def animeKitchenKeystorePropertiesFile = rootProject.file('key.properties')
if (animeKitchenKeystorePropertiesFile.exists()) {{
    animeKitchenKeystoreProperties.load(
        new FileInputStream(animeKitchenKeystorePropertiesFile)
    )
}}

"""
    text = prelude + text

    build_types_anchor = "    buildTypes {\n"
    if build_types_anchor not in text:
        raise RuntimeError(
            "Flutter Android Groovy template changed: buildTypes block not found"
        )

    signing_block = """    signingConfigs {
        if (animeKitchenKeystorePropertiesFile.exists()) {
            persistentRelease {
                keyAlias animeKitchenKeystoreProperties['keyAlias']
                keyPassword animeKitchenKeystoreProperties['keyPassword']
                storeFile file(animeKitchenKeystoreProperties['storeFile'])
                storePassword animeKitchenKeystoreProperties['storePassword']
            }
        }
    }

"""
    text = text.replace(
        build_types_anchor,
        signing_block + build_types_anchor,
        1,
    )

    replacement = """            signingConfig = animeKitchenKeystorePropertiesFile.exists()
                ? signingConfigs.persistentRelease
                : signingConfigs.debug"""
    text = text.replace(debug_line, replacement, 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    if KTS.is_file():
        changed = patch_kotlin_dsl(KTS)
        print(
            "Android signing patch: "
            + ("applied" if changed else "already present")
        )
        return 0

    if GROOVY.is_file():
        changed = patch_groovy(GROOVY)
        print(
            "Android signing patch: "
            + ("applied" if changed else "already present")
        )
        return 0

    raise RuntimeError("Android app Gradle file not found")


if __name__ == "__main__":
    raise SystemExit(main())
