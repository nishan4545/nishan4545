# Profile maintenance

The GitHub profile README uses a white animated introduction and an original developer illustration. It has no separate portfolio website, hover effects, floating labels, or CSS shadow styling.

## Intro animations

Install Pillow, then run `python .github/scripts/render_intro.py`. This produces desktop and mobile GIFs plus static reduced-motion previews. On non-Windows systems, set `PROFILE_FONT_DIR` to a directory containing DejaVu Sans and DejaVu Sans Mono fonts. `render_profile.py` provides shared rendering helpers; its standalone entry point renders the earlier design, so use `render_intro.py` for the current banner.

## Illustration

`assets/developer.png` was generated with the built-in image-generation tool. It is a generic illustrated developer, not a portrait of Nishan.

Generation prompt:

> Use case: stylized-concept. Asset type: transparent hero illustration for a professional software developer profile on a white website. Create one polished editorial 3D illustration of a young adult male software developer with medium brown skin, short dark hair and a blue casual shirt, seated in a light ergonomic chair at a minimal white desk, typing at a slim desktop monitor displaying abstract blue code lines. This is a generic developer illustration, not a portrait of a real individual. Include a small laptop on the desk, a modest green plant, and soft subtle contact shadows. Sophisticated crafted 3D shapes, restrained proportions, elegant rounded geometry, refined materials, friendly but professional, premium technology editorial design. Three-quarter isometric view, entire desk and person fully visible, balanced compact composition centered with generous empty margin. White, light gray, cobalt blue and small mint accents. Bright high-key studio lighting, no dark background. No floating slabs, no stacked layers, no large abstract cubes, no logos, no readable text, no watermark. Transparent background; isolated illustration suitable for placement on pure white.

## Accessibility and content

- Static alternatives are provided for reduced-motion preferences.
- The animated introduction has desktop and mobile versions.
- Company project names, internal metrics, and repository links are excluded.
