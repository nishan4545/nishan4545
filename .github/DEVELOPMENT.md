# Profile maintenance

The GitHub profile README uses a white animated introduction, a greeting-to-work character loop, and an Engineering Focus section organized around six core engineering areas. It has no separate portfolio website, hover effects, floating labels, or CSS shadow styling.

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

## Greeting-to-work animation

The current `assets/developer-hello-work.gif` is a silent frame-based animation, not generated speech or a continuous 3D video. It waves hello, returns to typing, and repeats. The built-in image-generation tool created the artwork; FFmpeg separates and assembles its frames.

Source: `.github/artwork/greeting-work-sheet.png`. To rebuild, run `.github/scripts/assemble_greeting.ps1 -Sheet .github/artwork/greeting-work-sheet.png`, with FFmpeg on PATH or supplied through `-Ffmpeg`. The script also writes the reduced-motion preview.

Final generation prompt (the reference was a six-pose greeting sheet based on the original developer illustration):

> Edit this animation sprite sheet into an 8-FRAME greeting-to-work loop. Output exactly FOUR columns by TWO rows of equal SQUARE tiles, 2:1 total aspect ratio, no gutters, no borders. Each tile repeats the identical developer, white desk, white monitor with blue code, chair, laptop, plant from the reference. Preserve the reference character identity and the entire scene composition in EVERY tile; locked camera and position, constant scene scale, white background. Read frames row-major from left to right. FRAME 1: character smiles at viewer with raised hand tilted left and speech bubble 'Hi!'. FRAME 2: same smile, hand tilted right, 'Hi!'. FRAME 3: hand half lowered toward keyboard, head turning a little toward monitor, no bubble. FRAME 4: both hands on keyboard, head facing monitor, no bubble. FRAME 5: same typing pose, tiny hand/finger shift, eyes on monitor. FRAME 6: still typing, tiny finger shift. FRAME 7: head turning toward viewer, greeting arm half raised, no bubble. FRAME 8: smiling at viewer, hand raised upright, speech bubble 'Hi!'. Critical: identical face, torso scale, desk position, plant, monitor geometry and contents across all frames. Only head, greeting arm and fingers change. Full character, chair and entire desk visible within every square, with 8% safe margins. PURE WHITE background and light monitor screen. No floor shadow, no dark background, no numbered captions, no skill cards, no other text. Premium clean 3D illustration. This sheet will be cut into equal square frames to make a looping GIF, so tile alignment is essential.
