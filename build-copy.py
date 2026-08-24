# -*- coding: utf-8 -*-
"""
Rewrites the site copy in assets/js/i18n.js for the architecture practice.
Uses exact string replacement rather than regex so every change is auditable.

Run from the website/ folder:  python build-copy.py
"""
import io

P = 'assets/js/i18n.js'

PAIRS = [
    # ---------------------------------------------------------------- Dutch
    ('"meta.title": "MD-ontwerpen — Grafisch ontwerp & visuele identiteit"',
     '"meta.title": "MD-ontwerpen — Architectuur, bouwkunde en bouwbegeleiding"'),
    ('"Studio voor grafisch ontwerp, merkidentiteit en digitaal ontwerp. Werk dat helder is, standhoudt en klopt."',
     '"Bureau voor architectuur, bouwkunde en bouwbegeleiding. Van ontwerp en constructie tot vergunning, aanbesteding en oplevering."'),
    ('"hero.eyebrow": "Ontwerpstudio — beschikbaar voor opdrachten"',
     '"hero.eyebrow": "Architectuur — bouwkunde — bouwbegeleiding"'),
    ('"hero.title": "Ontwerp dat blijft staan."',
     '"hero.title": "Van eerste schets tot oplevering."'),
    ('"MD-ontwerpen is een studio voor merkidentiteit, drukwerk en digitaal ontwerp. Geen ruis, geen trucs — alleen werk dat doet wat het moet doen."',
     '"MD-ontwerpen verzorgt architectuur, bouwkundige uitwerking, constructie, installaties en bouwbegeleiding. Alle disciplines onder één dak, zodat het plan klopt vóórdat de eerste schop de grond in gaat."'),
    ('"hero.cta1": "Bekijk het werk"', '"hero.cta1": "Bekijk de diensten"'),
    ('"about.title": "Klein, scherp, betrokken."',
     '"about.title": "Eén aanspreekpunt, dertien disciplines."'),
    ('"MD-ontwerpen werkt direct met opdrachtgevers — zonder tussenlagen. Dat betekent korte lijnen, snelle beslissingen en een ontwerper die het hele traject kent."',
     '"De meeste vertraging en faalkosten ontstaan op de overgangen: tussen ontwerp en constructie, tussen bouwkunde en installaties, tussen vergunning en uitvoering. Door die disciplines in één hand te houden verdwijnen die overgangen grotendeels."'),
    ('"Elk project begint met de vraag waarom iets bestaat. Pas daarna komt de vorm. Die volgorde levert werk op dat over vijf jaar nog steeds klopt."',
     '"Dat betekent één aanspreekpunt, één informatiemodel en tekeningen die onderling kloppen. En het betekent dat een keuze in het ontwerp direct wordt getoetst op constructie, brandveiligheid en bouwfysica."'),
    ('"about.servicesTitle": "Diensten"', '"about.servicesTitle": "Werkwijze"'),
    ('"about.s1": "Merkidentiteit & logo-ontwerp"',
     '"about.s1": "Ontwerp, techniek en proces in samenhang"'),
    ('"about.s2": "Websites & digitale producten"',
     '"about.s2": "Toetsing aan Bbl, BENG en Wkb"'),
    ('"about.s3": "Drukwerk & redactioneel ontwerp"',
     '"about.s3": "Werken vanuit één informatiemodel (BIM)"'),
    ('"about.s4": "Signage & tentoonstellingsontwerp"',
     '"about.s4": "Begeleiding tot en met de oplevering"'),
    ('"contact.location": "Gevestigd in Nederland — werkzaam in heel Europa."',
     '"contact.location": "Gevestigd in Nederland — werkzaam door heel het land."'),
    ('"Vertel kort waar het over gaat en wat de planning is. Ik reageer binnen twee werkdagen."',
     '"Vertel kort waar het over gaat en wat de planning is. U krijgt binnen twee werkdagen antwoord."'),

    # -------------------------------------------------------------- English
    ('"meta.title": "MD-ontwerpen — Graphic design & visual identity"',
     '"meta.title": "MD-ontwerpen — Architecture, building engineering and construction management"'),
    ('"A studio for graphic design, brand identity and digital design. Work that is clear, durable, and right."',
     '"Practice for architecture, building engineering and construction management. From design and structure to permits, tendering and handover."'),
    ('"hero.eyebrow": "Design studio — available for commissions"',
     '"hero.eyebrow": "Architecture — building engineering — construction management"'),
    ('"hero.title": "Design that holds up."',
     '"hero.title": "From first sketch to handover."'),
    ('"MD-ontwerpen is a studio for brand identity, print and digital design. No noise, no tricks — just work that does what it needs to do."',
     '"MD-ontwerpen covers architecture, building engineering, structure, services and construction management. Every discipline under one roof, so the plan is right before the first spade goes into the ground."'),
    ('"hero.cta1": "See the work"', '"hero.cta1": "See the services"'),
    ('"about.title": "Small, sharp, involved."',
     '"about.title": "One point of contact, thirteen disciplines."'),
    ('"MD-ontwerpen works directly with clients — no layers in between. That means short lines, fast decisions, and one designer who knows the whole project."',
     '"Most delay and failure cost arises at the handovers: between design and structure, between building and services, between permit and execution. Keeping those disciplines in one place largely removes those handovers."'),
    ('"Every project starts with why the thing exists. Form comes after. That order produces work that still makes sense five years on."',
     '"That means one point of contact, one information model, and drawings that agree with each other. It also means a design choice is tested immediately against structure, fire safety and building physics."'),
    ('"about.servicesTitle": "Services"', '"about.servicesTitle": "How we work"'),
    ('"about.s1": "Brand identity & logo design"',
     '"about.s1": "Design, engineering and process developed together"'),
    ('"about.s2": "Websites & digital products"',
     '"about.s2": "Tested against Dutch building regulations"'),
    ('"about.s3": "Print & editorial design"',
     '"about.s3": "Working from a single information model (BIM)"'),
    ('"about.s4": "Signage & exhibition design"',
     '"about.s4": "Guidance through to handover"'),
    ('"contact.location": "Based in the Netherlands — working across Europe."',
     '"contact.location": "Based in the Netherlands — working nationwide."'),
]

# New keys, inserted before nav.menu in each dictionary
NEW_NL = ('      "nav.services": "Diensten",\n'
          '      "services.eyebrow": "Diensten",\n'
          '      "services.title": "Het hele traject, onder één dak.",\n'
          '      "services.lead":\n'
          '        "Van eerste schets tot oplevering. Elke discipline grijpt in op de volgende, '
          'dus worden ze in samenhang uitgewerkt in plaats van na elkaar.",\n')
NEW_EN = ('      "nav.services": "Services",\n'
          '      "services.eyebrow": "Services",\n'
          '      "services.title": "The whole route, under one roof.",\n'
          '      "services.lead":\n'
          '        "From first sketch to handover. Each discipline affects the next, '
          'so they are developed together rather than in sequence.",\n')


def main():
    s = io.open(P, encoding='utf-8').read()

    applied, missing = 0, []
    for old, new in PAIRS:
        if old in s:
            s = s.replace(old, new, 1)
            applied += 1
        else:
            missing.append(old[:60])

    s = s.replace('      "nav.menu": "Menu openen",', NEW_NL + '      "nav.menu": "Menu openen",', 1)
    s = s.replace('      "nav.menu": "Open menu",', NEW_EN + '      "nav.menu": "Open menu",', 1)

    io.open(P, 'w', encoding='utf-8').write(s)
    print(f'applied {applied}/{len(PAIRS)} replacements')
    for m in missing:
        print('  NOT FOUND:', m)
    print('added services keys to both dictionaries')


if __name__ == '__main__':
    main()
