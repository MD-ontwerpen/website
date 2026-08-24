# -*- coding: utf-8 -*-
"""
Inserts the layered 3D viewer section into index.html, above the services grid.

Run from the website/ folder:  python build-viewer-section.py
"""
import io

from build_service_data import SERVICES


def buttons():
    return ''.join(
        f'''
              <li>
                <button type="button" class="control filter-btn w-full" data-layer="{s['slug']}" aria-pressed="false">{s['titel'].replace(' (BIM)', '')}</button>
              </li>''' for s in SERVICES)


SECTION = '''      <!-- ================= 3D MODEL ================= -->
      <section id="model" class="rule-top" style="background-color: var(--muted)">
        <div class="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28">
          <div class="reveal max-w-2xl">
            <p class="eyebrow mb-4">Het model</p>
            <h2 class="headline text-[clamp(2rem,5vw,3.5rem)]">Eén gebouw, dertien lagen.</h2>
            <p class="mt-5 text-lg" style="color: var(--muted-fg)">
              Elke discipline is een laag in hetzelfde model. Kies een laag om te zien
              welk deel van het gebouw erbij hoort — en hoe de lagen op elkaar ingrijpen.
            </p>
          </div>

          <div class="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-[1fr_260px]" data-viewer>
            <div class="brut-box relative overflow-hidden" style="aspect-ratio: 16 / 10">
              <!-- Static drawing shows first; the model only loads on request -->
              <img
                src="assets/img/diensten/_basis.svg"
                alt="Doorsnede van een gebouw met terrein, constructie en installaties"
                width="800" height="520"
                class="h-full w-full object-cover"
                data-viewer-fallback
              />
              <div class="absolute inset-0" data-viewer-canvas></div>

              <button
                type="button"
                class="control btn-primary brut-shadow absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
                data-viewer-start
              >
                Laad het 3D-model
              </button>

              <p
                class="eyebrow absolute bottom-0 left-0 right-0 px-4 py-3"
                style="background-color: var(--bg); border-top: var(--rule) solid var(--border)"
                data-viewer-status
                role="status"
                aria-live="polite"
                hidden
              ></p>
            </div>

            <div>
              <p class="eyebrow mb-3">Toon laag</p>
              <ul class="grid grid-cols-2 gap-2 lg:grid-cols-1">%s
              </ul>
              <p class="mt-4 text-[0.85rem] leading-relaxed" style="color: var(--muted-fg)">
                Sleep om te draaien, scroll om te zoomen. Klik een actieve laag nogmaals
                om alles weer te tonen.
              </p>
            </div>
          </div>

          <p class="eyebrow mt-8" style="color: var(--muted-fg)">
            Het getoonde model is een voorbeeldmassa, geen uitgevoerd project.
          </p>
        </div>
      </section>

'''


def main():
    p = 'index.html'
    s = io.open(p, encoding='utf-8').read()

    if 'data-viewer' in s:
        print('viewer section already present - nothing to do')
        return

    anchor = '      <!-- ================= DIENSTEN ================= -->'
    assert anchor in s, 'services section not found'
    s = s.replace(anchor, (SECTION % buttons()) + anchor, 1)

    # Module script, after the existing ones
    old = '    <script src="assets/js/main.js"></script>'
    new = ('    <script src="assets/js/main.js"></script>\n'
           '    <script type="module" src="assets/js/viewer.js"></script>')
    assert old in s
    s = s.replace(old, new, 1)

    io.open(p, 'w', encoding='utf-8').write(s)
    print('index.html: 3D viewer section inserted above the services grid')
    print('  layer buttons:', s.count('data-layer='))


if __name__ == '__main__':
    main()
