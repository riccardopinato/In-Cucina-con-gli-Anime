# F3D artwork pilot

This branch is an APK-only visual review branch.

- Card geometry is intentionally unchanged: the existing 178 px artwork area remains in place and uses `BoxFit.cover`.
- Recipe detail uses the full portrait artwork with `BoxFit.contain`.
- The existing procedural artwork remains the fallback for every recipe outside the three pilot slots.
- `recipe_000002` is semantically aligned with the ramen artwork.
- `recipe_000003` and `recipe_000009` are visual-layout stand-ins only. Their current generated images depict katsu curry and salmon donburi, not the catalog's Katsudon and Oyakodon. They MUST be replaced with exact dish artwork before this branch can be considered mergeable.

Do not merge this branch into production while either stand-in remains.
