# -*- coding: utf-8 -*-
"""
Rewrites index.html for the architecture / bouwkunde practice:
  - swaps the invented graphic-design project grid for the 13 services
  - repoints the nav and the metadata

Run from the website/ folder:  python build-home.py
"""
import io
import re

from build_service_data import SERVICES  # noqa: E402

SITE = "https://md-ontwerpen.nl"


def cards():
    out = []
    for s in SERVICES:
        out.append(f'''
            <li class="dienst-card brut-box brut-shadow reveal">
              <a href="diensten/{s['slug']}.html" class="flex h-full flex-col">
                <img
                  src="assets/img/diensten/{s['slug']}.svg"
                  alt="{s['alt']}"
                  width="800" height="520" loading="lazy"
                  class="dienst-thumb"
                />
                <span class="flex flex-1 flex-col p-5">
                  <span class="font-display text-lg font-bold">{s['titel']}</span>
                  <span class="mt-2 flex-1 text-[0.9rem] leading-relaxed" style="color: var(--muted-fg)">{s['kort']}</span>
                  <span class="eyebrow mt-4 inline-flex items-center gap-2" style="color: var(--accent-strong)">
                    Lees meer
                    <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
                  </span>
                </span>
              </a>
            </li>''')
    return ''.join(out)


def main():
    p = 'index.html'
    s = io.open(p, encoding='utf-8').read()

    # ---- metadata -------------------------------------------------------
    s = s.replace(
        '<title>MD-ontwerpen — Grafisch ontwerp &amp; visuele identiteit</title>',
        '<title>MD-ontwerpen — Architectuur, bouwkunde en bouwbegeleiding</title>')
    s = s.replace(
        'content="Studio voor grafisch ontwerp, merkidentiteit en digitaal ontwerp. Werk dat helder is, standhoudt en klopt."',
        'content="Bureau voor architectuur, bouwkunde en bouwbegeleiding. Van ontwerp en constructie tot vergunning, aanbesteding en oplevering."')
    s = s.replace(
        '<meta property="og:title" content="MD-ontwerpen — Grafisch ontwerp &amp; visuele identiteit" />',
        '<meta property="og:title" content="MD-ontwerpen — Architectuur, bouwkunde en bouwbegeleiding" />')
    s = s.replace(
        '<meta name="twitter:title" content="MD-ontwerpen — Grafisch ontwerp &amp; visuele identiteit" />',
        '<meta name="twitter:title" content="MD-ontwerpen — Architectuur, bouwkunde en bouwbegeleiding" />')
    s = s.replace(
        'content="Studio voor merkidentiteit, drukwerk en digitaal ontwerp."',
        'content="Architectuur, bouwkunde en bouwbegeleiding — van eerste schets tot oplevering."')
    s = s.replace(
        '"description": "Studio voor grafisch ontwerp, merkidentiteit en digitaal ontwerp.",',
        '"description": "Bureau voor architectuur, bouwkunde en bouwbegeleiding in Nederland.",')

    # ---- nav: Werk -> Diensten -----------------------------------------
    s = s.replace('href="#work" data-i18n="nav.work">Werk</a>',
                  'href="#diensten" data-i18n="nav.services">Diensten</a>')

    # ---- hero CTA points at the services -------------------------------
    s = s.replace('<a href="#work" class="control btn-primary brut-shadow" data-i18n="hero.cta1">',
                  '<a href="#diensten" class="control btn-primary brut-shadow" data-i18n="hero.cta1">')

    # ---- swap the whole WORK section for the services grid -------------
    start = s.index('      <!-- ================= WORK ================= -->')
    end = s.index('      <!-- ================= ABOUT ================= -->')
    services_section = f'''      <!-- ================= DIENSTEN ================= -->
      <section id="diensten" class="rule-top">
        <div class="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28">
          <div class="reveal max-w-2xl">
            <p class="eyebrow mb-4" data-i18n="services.eyebrow">Diensten</p>
            <h2 class="headline text-[clamp(2rem,5vw,3.5rem)]" data-i18n="services.title">
              Het hele traject, onder één dak.
            </h2>
            <p class="mt-5 text-lg" style="color: var(--muted-fg)" data-i18n="services.lead">
              Van eerste schets tot oplevering. Elke discipline grijpt in op de volgende, dus
              worden ze in samenhang uitgewerkt in plaats van na elkaar.
            </p>
          </div>

          <ul class="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">{cards()}
          </ul>
        </div>
      </section>

'''
    s = s[:start] + services_section + s[end:]

    io.open(p, 'w', encoding='utf-8').write(s)
    print('index.html rewritten: metadata, nav, hero CTA, services grid')
    print('  services section contains', s.count('dienst-card'), 'cards')
    print('  references to the old project grid remaining:', s.count('data-category'))


if __name__ == '__main__':
    main()
