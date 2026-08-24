# -*- coding: utf-8 -*-
"""
Generates one page per service in diensten/, plus the services grid markup for
the homepage. There is no build step on this site, so the shared header and
footer are inlined into each page by this script rather than fetched at runtime.

Run from the website/ folder:  python build-service-pages.py

The copy describes what each discipline involves. It deliberately makes no
claims about experience, project counts or clients - those are the owner's to
add, and inventing them would be dishonest.
"""
import io
import os

SITE = "https://md-ontwerpen.nl"

SERVICES = [
    dict(
        slug="architectuur",
        naam="Architectuur",
        titel="Architectuur",
        seo_titel="Architectuur — ontwerp en ruimtelijk concept | MD-ontwerpen",
        meta="Architectonisch ontwerp van schetsontwerp tot definitief ontwerp: ruimtelijk concept, massa, gevel en programma van eisen.",
        lead="Het architectonisch ontwerp bepaalt hoe een gebouw zich verhoudt tot zijn omgeving, hoe het gebruikt wordt en hoe het eruitziet. Het is de fase waarin uitgangspunten, wensen en regelgeving samenkomen in één samenhangend plan.",
        secties=[
            ("Van programma naar plan",
             "Een ontwerp begint bij het programma van eisen: welke ruimtes zijn nodig, hoe verhouden ze zich tot elkaar, en welke eisen stellen gebruik, budget en locatie. Vanuit die uitgangspunten volgt een schetsontwerp (SO), daarna een voorlopig ontwerp (VO) en ten slotte een definitief ontwerp (DO). Elke stap maakt het plan concreter en toetsbaarder."),
            ("Massa, licht en oriëntatie",
             "De positie van het gebouw op de kavel, de hoogte, de indeling van de gevel en de oriëntatie ten opzichte van de zon bepalen in belangrijke mate het comfort en het energiegebruik. Deze keuzes worden vroeg gemaakt en zijn later kostbaar om te wijzigen."),
            ("Samenhang met de andere disciplines",
             "Een architectonisch plan staat niet los van constructie, installaties en bouwfysica. Door die disciplines vroeg te betrekken blijven ontwerpkeuzes uitvoerbaar en voorkomt u dat het plan later ingrijpend moet worden aangepast."),
        ],
        levert=["Schetsontwerp, voorlopig ontwerp en definitief ontwerp",
                "Plattegronden, gevels en doorsneden",
                "Ruimtelijke onderbouwing en programma van eisen",
                "3D-beelden en maquettebeelden voor besluitvorming"],
        alt="Doorsnede van een gebouw met de architectonische hoofdvorm gemarkeerd",
    ),
    dict(
        slug="bouwkunde",
        naam="Bouwkunde",
        titel="Bouwkunde",
        seo_titel="Bouwkunde — technische uitwerking en details | MD-ontwerpen",
        meta="Bouwkundige uitwerking van ontwerp naar uitvoerbaar plan: details, materialisatie, bestektekeningen en werktekeningen.",
        lead="Bouwkunde vertaalt een ontwerp naar een plan dat daadwerkelijk gebouwd kan worden. Het gaat om opbouw van wanden, daken en vloeren, om aansluitingen tussen materialen, en om de tekeningen waarmee een aannemer aan de slag kan.",
        secties=[
            ("Details bepalen de kwaliteit",
             "De meeste bouwfouten ontstaan niet in het grote gebaar maar op de aansluitingen: waar de gevel de fundering raakt, waar het kozijn in de wand valt, waar het dak op de muur landt. Een goed uitgewerkt detail voorkomt lekkage, koudebruggen en geluidsoverlast."),
            ("Materialisatie en opbouw",
             "Elke laag in een constructie heeft een functie: dragen, isoleren, waterdicht houden, afwerken. De volgorde en dikte van die lagen bepalen of een gebouw droog, warm en stil blijft. Materiaalkeuze speelt daarnaast mee in onderhoud, levensduur en milieuprestatie."),
            ("Tekeningen voor uitvoering",
             "Bestektekeningen leggen vast wat er gebouwd wordt en tegen welke eisen. Werktekeningen geven de uitvoerende partij de maten en aansluitingen die nodig zijn op de bouwplaats. Beide vormen samen de basis voor prijsvorming en controle."),
        ],
        levert=["Bestektekeningen en werktekeningen",
                "Principedetails en detailboek",
                "Materialisatie- en afwerkstaten",
                "Kozijn-, deur- en ramenstaten"],
        alt="Doorsnede van een gebouw met de gevelopbouw en wandlagen gemarkeerd",
    ),
    dict(
        slug="constructieleer",
        naam="Constructieleer",
        titel="Constructieleer",
        seo_titel="Constructieleer — draagconstructie en berekeningen | MD-ontwerpen",
        meta="Constructief ontwerp en berekening: draagconstructie, krachtsafdracht, fundering en constructietekeningen volgens de Eurocode.",
        lead="De draagconstructie brengt alle belastingen in een gebouw naar de ondergrond: eigen gewicht, gebruik, sneeuw en wind. Het constructief ontwerp bepaalt welke elementen dat doen en hoe zwaar ze moeten zijn.",
        secties=[
            ("Krachtsafdracht als uitgangspunt",
             "Een heldere krachtsafdracht — van vloer naar balk, van balk naar kolom, van kolom naar fundering — levert een constructie op die eenvoudiger, lichter en goedkoper is. Onduidelijke overspanningen leiden tot zwaardere profielen en meer materiaal dan nodig."),
            ("Fundering en ondergrond",
             "De keuze tussen een staalfundering en een paalfundering hangt af van de draagkracht van de bodem en van de belasting die het gebouw afgeeft. Grondonderzoek is daarvoor het vertrekpunt; zonder die gegevens is een funderingsadvies niet meer dan een aanname."),
            ("Toetsing en berekening",
             "Constructieve berekeningen worden getoetst aan de Eurocodes en aan de eisen uit het Besluit bouwwerken leefomgeving. Bij een vergunningaanvraag horen constructieve gegevens die de gemeente of kwaliteitsborger kan controleren."),
        ],
        levert=["Constructief ontwerp en hoofdopzet",
                "Sterkte- en stabiliteitsberekeningen",
                "Funderingsadvies op basis van grondonderzoek",
                "Constructietekeningen en wapeningstekeningen"],
        alt="Doorsnede van een gebouw met kolommen, vloeren en fundering gemarkeerd",
    ),
    dict(
        slug="brandveiligheid",
        naam="Brandveiligheid",
        titel="Brandveiligheid",
        seo_titel="Brandveiligheid — compartimentering en vluchtroutes | MD-ontwerpen",
        meta="Brandveiligheidsadvies: brandcompartimentering, vluchtroutes, WBDBO en toetsing aan het Besluit bouwwerken leefomgeving.",
        lead="Brandveiligheid gaat over de tijd die mensen hebben om een gebouw veilig te verlaten en over het beperken van uitbreiding van brand. Die twee doelen bepalen de indeling in compartimenten en de opzet van de vluchtroutes.",
        secties=[
            ("Compartimentering",
             "Een gebouw wordt opgedeeld in brandcompartimenten die branduitbreiding een bepaalde tijd tegenhouden. De weerstand tegen branddoorslag en brandoverslag (WBDBO) tussen die compartimenten volgt uit de functie en de omvang van het gebouw."),
            ("Vluchtroutes",
             "Vanuit elk punt in een gebouw moet een veilige route naar buiten beschikbaar zijn, met voldoende breedte en een aanvaardbare loopafstand. Waar één route onvoldoende is, zijn twee onafhankelijke richtingen nodig."),
            ("Aantoonbaar voldoen",
             "Voldoen aan de prestatie-eisen kan langs de rechtstreekse weg of via een gelijkwaardige oplossing. In beide gevallen moet dat aantoonbaar zijn, met tekeningen en een onderbouwing die het bevoegd gezag of de kwaliteitsborger kan beoordelen."),
        ],
        levert=["Brandveiligheidsconcept en uitgangspuntendocument",
                "Compartimenterings- en vluchtroutetekeningen",
                "WBDBO-onderbouwing",
                "Onderbouwing van gelijkwaardige oplossingen"],
        alt="Doorsnede van een gebouw met vluchtroutes en een brandcompartiment gemarkeerd",
    ),
    dict(
        slug="installatietechniek",
        naam="Installatietechniek",
        titel="Installatietechniek",
        seo_titel="Installatietechniek — klimaat, ventilatie en energie | MD-ontwerpen",
        meta="Installatieconcept voor W- en E-installaties: verwarming, ventilatie, koeling, elektra en de ruimte die ze in het ontwerp nodig hebben.",
        lead="Installaties bepalen of een gebouw comfortabel en betaalbaar in gebruik is. Ze vragen ruimte, schachten en tracés, en die zijn het eenvoudigst te reserveren zolang het ontwerp nog niet vastligt.",
        secties=[
            ("Concept vóór apparatuur",
             "De vraag is eerst hoeveel warmte, koude en verse lucht een gebouw nodig heeft, en pas daarna welke installatie dat levert. Een goed geïsoleerde schil verkleint de installatie; een matige schil vraagt blijvend om zwaardere apparatuur en hogere energielasten."),
            ("Ruimte, schachten en tracés",
             "Kanalen, leidingen en technische ruimtes hebben fysieke maat. Worden ze pas laat ingetekend, dan leidt dat tot verlaagde plafonds, verspringende leidingen of ingrepen in de constructie. Vroeg reserveren voorkomt dat."),
            ("Elektra en aansluitingen",
             "Naast klimaat gaat het om verlichting, groepenverdeling, data en aansluitingen voor bijvoorbeeld laadpunten of zonnepanelen. Ook die vragen om ruimte en om een aansluitcapaciteit die tijdig bij de netbeheerder wordt aangevraagd."),
        ],
        levert=["Installatieconcept voor W- en E-installaties",
                "Ruimtereservering voor schachten en technische ruimtes",
                "Principeschema's en tracéplattegronden",
                "Uitgangspunten voor aanbesteding van de installaties"],
        alt="Doorsnede van een gebouw met de installatieschacht en leidingtracés gemarkeerd",
    ),
    dict(
        slug="bouwfysica",
        naam="Bouwfysica",
        titel="Bouwfysica",
        seo_titel="Bouwfysica — isolatie, akoestiek, vocht en daglicht | MD-ontwerpen",
        meta="Bouwfysisch advies: thermische schil, BENG, geluidwering, vochthuishouding, koudebruggen en daglichttoetreding.",
        lead="Bouwfysica gaat over hoe warmte, vocht, geluid en licht zich door een gebouw bewegen. Het bepaalt of een gebouw warm blijft in de winter, koel in de zomer, droog in de constructie en stil genoeg om in te werken of te slapen.",
        secties=[
            ("De thermische schil",
             "Isolatie werkt alleen als de schil doorlopend is. Onderbrekingen — bij een balkon, een fundering of een kozijnaansluiting — vormen koudebruggen waar warmte weglekt en waar condens en schimmel kunnen ontstaan. De schil sluitend krijgen is grotendeels een detailleringsvraagstuk."),
            ("Energieprestatie",
             "Nieuwbouw wordt beoordeeld op de BENG-indicatoren: de energiebehoefte, het primair fossiel energiegebruik en het aandeel hernieuwbare energie. Die worden bepaald door isolatie, kierdichting, oriëntatie, zonwering en installatiekeuze samen."),
            ("Geluid, vocht en daglicht",
             "Geluidwering betreft zowel geluid van buiten als geluid tussen ruimtes onderling. Vochthuishouding gaat over dampdiffusie en over ventilatie. Daglicht bepaalt de gebruikskwaliteit van een ruimte en kent een minimumeis per verblijfsgebied."),
        ],
        levert=["BENG-berekening en energieprestatie",
                "Koudebrugberekeningen en detailtoetsing",
                "Geluidweringsonderzoek",
                "Daglicht- en ventilatietoetsing"],
        alt="Doorsnede van een gebouw met de doorlopende thermische schil gemarkeerd",
    ),
    dict(
        slug="interieur",
        naam="Interieur",
        titel="Interieur",
        seo_titel="Interieur — indeling, afwerking en maatwerk | MD-ontwerpen",
        meta="Interieurontwerp: ruimtelijke indeling, materialisatie, verlichting, maatwerkmeubilair en afwerkingsstaten.",
        lead="Het interieur bepaalt hoe een gebouw dagelijks gebruikt wordt. Indeling, licht, materiaal en akoestiek maken samen het verschil tussen een ruimte die werkt en een ruimte die alleen op tekening klopt.",
        secties=[
            ("Indeling en looproutes",
             "Een goede plattegrond volgt uit hoe mensen zich door een ruimte bewegen en waar zij langer verblijven. Daglicht, uitzicht en privacy bepalen welke functies waar het beste liggen."),
            ("Materiaal, licht en akoestiek",
             "Materiaalkeuze werkt door in sfeer, onderhoud en geluid. Harde oppervlakken maken een ruimte galmend; verlichting bepaalt of kleur en textuur tot hun recht komen. Deze keuzes hangen samen en worden daarom in samenhang gemaakt."),
            ("Maatwerk",
             "Waar standaardmaten niet passen, biedt maatwerk uitkomst: inbouwkasten, balies, keukens of trappen. Maatwerk vraagt vroege maatvoering en afstemming met de constructie en de installaties."),
        ],
        levert=["Interieurplattegronden en aanzichten",
                "Materialisatie-, kleur- en afwerkstaten",
                "Verlichtingsplan",
                "Maatwerktekeningen voor meubel en inbouw"],
        alt="Doorsnede van een gebouw met de binnenruimtes en scheidingswanden gemarkeerd",
    ),
    dict(
        slug="landschap",
        naam="Landschap",
        titel="Landschap",
        seo_titel="Landschap — terreininrichting, groen en water | MD-ontwerpen",
        meta="Landschapsontwerp en terreininrichting: bestrating, groen, waterberging, hoogteverschillen en de overgang van gebouw naar buitenruimte.",
        lead="De buitenruimte is onderdeel van het plan, niet wat overblijft. Terreininrichting bepaalt hoe een gebouw benaderd wordt, hoe water wordt opgevangen en hoe de overgang tussen binnen en buiten werkt.",
        secties=[
            ("Terrein en hoogteverschillen",
             "Peilmaten, afschot en hoogteverschillen bepalen de toegankelijkheid en de afwatering. Ze worden vastgelegd in samenhang met het vloerpeil van het gebouw en met de aansluiting op de openbare weg."),
            ("Water en verharding",
             "Gemeenten stellen in toenemende mate eisen aan waterberging op eigen terrein. De verhouding tussen verharding en groen, en de wijze waarop hemelwater infiltreert of geborgen wordt, is daarmee een ontwerpopgave geworden."),
            ("Beplanting en beheer",
             "Beplanting verandert met de seizoenen en groeit door. Een beplantingsplan houdt rekening met eindmaat, standplaats en het onderhoud dat later daadwerkelijk uitgevoerd kan worden."),
        ],
        levert=["Inrichtingsplan voor het terrein",
                "Bestratings-, peil- en afwateringsplan",
                "Beplantingsplan met soortenlijst",
                "Onderbouwing waterberging op eigen terrein"],
        alt="Doorsnede van een gebouw met het maaiveld en de beplanting eromheen gemarkeerd",
    ),
    dict(
        slug="informatiemodel",
        naam="Informatiemodel",
        titel="Informatiemodel (BIM)",
        seo_titel="Informatiemodel BIM — 3D-model en clashcontrole | MD-ontwerpen",
        meta="BIM-informatiemodel: één 3D-model als bron voor tekeningen, hoeveelheden en clashcontrole tussen bouwkunde, constructie en installaties.",
        lead="Een informatiemodel is één digitaal model waarin bouwkunde, constructie en installaties samenkomen. Tekeningen, hoeveelheden en doorsneden komen uit dat model, zodat ze onderling niet uit de pas gaan lopen.",
        secties=[
            ("Eén bron voor alle uitvoer",
             "Wordt een wand in het model verplaatst, dan verandert die op elke plattegrond, doorsnede en aanzicht mee. Dat voorkomt de tegenstrijdigheden die ontstaan wanneer tekeningen afzonderlijk worden bijgehouden."),
            ("Clashcontrole",
             "Door de modellen van de verschillende disciplines te combineren, komen botsingen tussen bijvoorbeeld een kanaal en een ligger op tekening aan het licht in plaats van op de bouwplaats. Dat scheelt faalkosten en vertraging."),
            ("Data en overdracht",
             "Naast geometrie bevat een model informatie: materiaal, prestatie, hoeveelheid. Die data is bruikbaar bij aanbesteding, bij de kwaliteitsborging en later bij beheer en onderhoud. Uitwisseling verloopt via open formaten zoals IFC."),
        ],
        levert=["3D-informatiemodel volgens afgesproken LOD",
                "Tekeningen en hoeveelheden uit het model",
                "Clashcontrole tussen disciplines",
                "IFC-export voor uitwisseling en beheer"],
        alt="Doorsnede van een gebouw met een modelraster en knooppunten gemarkeerd",
    ),
    dict(
        slug="vergunnen",
        naam="Vergunnen",
        titel="Vergunnen",
        seo_titel="Vergunnen — omgevingsvergunning aanvragen | MD-ontwerpen",
        meta="Begeleiding van de omgevingsvergunning: vooroverleg, toets aan omgevingsplan en Bbl, indiening via het Omgevingsloket en de Wkb.",
        lead="Een vergunningaanvraag slaagt of strandt op volledigheid en op de aansluiting bij het omgevingsplan. Voorbereiding en vooroverleg bepalen in de praktijk hoe soepel de procedure verloopt.",
        secties=[
            ("Vooroverleg en het omgevingsplan",
             "Voordat een aanvraag wordt ingediend is het zinvol te toetsen of het plan past binnen het omgevingsplan, en bij afwijking te verkennen of de gemeente daaraan wil meewerken. Een vooroverleg legt die vraag voor voordat er kosten worden gemaakt aan een volledige uitwerking."),
            ("De aanvraag",
             "De aanvraag verloopt via het Omgevingsloket en bestaat uit tekeningen, berekeningen en onderbouwingen. Ontbrekende stukken leiden tot een verzoek om aanvulling en daarmee tot uitstel; een complete indiening voorkomt die vertraging."),
            ("Kwaliteitsborging",
             "Onder de Wet kwaliteitsborging voor het bouwen wordt de technische toets bij een deel van de bouwwerken uitgevoerd door een onafhankelijke kwaliteitsborger in plaats van door de gemeente. Dat vraagt om een borgingsplan en om dossiervorming tijdens de uitvoering."),
        ],
        levert=["Haalbaarheidstoets aan het omgevingsplan",
                "Vooroverleg met het bevoegd gezag",
                "Complete aanvraag via het Omgevingsloket",
                "Afstemming met de kwaliteitsborger (Wkb)"],
        alt="Doorsnede van een gebouw met een vergunningdocument en goedkeuringsstempel",
    ),
    dict(
        slug="aanbesteden",
        naam="Aanbesteden",
        titel="Aanbesteden",
        seo_titel="Aanbesteden — bestek, offertes en contractvorming | MD-ontwerpen",
        meta="Aanbestedingsbegeleiding: bestek en aanbestedingsstukken, offertes opvragen en vergelijken, prijsonderbouwing en contractvorming.",
        lead="Aanbesteden is het moment waarop een plan een prijs krijgt. Vergelijkbare offertes ontstaan alleen wanneer alle partijen op precies dezelfde stukken en dezelfde uitgangspunten inschrijven.",
        secties=[
            ("Vergelijkbaar uitvragen",
             "Een offerte is pas te vergelijken als vaststaat wat er wel en niet in zit. Bestek en aanbestedingsstukken leggen dat vast: omvang, kwaliteit, verantwoordelijkheden en planning. Zonder die basis vergelijkt u prijzen voor verschillende plannen."),
            ("Beoordelen op meer dan prijs",
             "De laagste inschrijving is niet automatisch de gunstigste. Stelposten, uitsluitingen, planning en ervaring met vergelijkbaar werk wegen mee. Een prijsvergelijking op onderdeelniveau maakt inzichtelijk waar verschillen vandaan komen."),
            ("Contractvorming",
             "Na gunning worden afspraken vastgelegd: contractvorm, betalingsschema, meer- en minderwerkprocedure en oplevertermijn. Heldere afspraken vooraf voorkomen discussie tijdens de uitvoering."),
        ],
        levert=["Bestek en aanbestedingsstukken",
                "Offerteaanvraag en nota van inlichtingen",
                "Prijsvergelijking op onderdeelniveau",
                "Advies bij gunning en contractvorming"],
        alt="Doorsnede van een gebouw met vergeleken offertes en een gekozen inschrijving",
    ),
    dict(
        slug="bouwen",
        naam="Bouwen",
        titel="Bouwen",
        seo_titel="Bouwen — directievoering en toezicht | MD-ontwerpen",
        meta="Uitvoeringsbegeleiding: directievoering, toezicht op de bouwplaats, bewaking van planning en budget, en beheersing van meerwerk.",
        lead="Tijdens de uitvoering wordt duidelijk of het plan klopt. Begeleiding op de bouwplaats bewaakt dat er gebouwd wordt zoals is afgesproken, en dat afwijkingen worden opgelost voordat ze duur worden.",
        secties=[
            ("Directievoering",
             "De directievoerder vertegenwoordigt de opdrachtgever richting de aannemer: bouwvergaderingen, beoordeling van termijnen, en besluiten over vragen die tijdens de uitvoering ontstaan. Eén aanspreekpunt voorkomt dat afspraken langs elkaar heen lopen."),
            ("Toezicht op het werk",
             "Toezicht controleert of het uitgevoerde werk overeenkomt met tekeningen, bestek en regelgeving. Juist bij werk dat later wordt weggewerkt — wapening, isolatie, luchtdichting — is controle op het juiste moment bepalend."),
            ("Planning, budget en meerwerk",
             "Meerwerk ontstaat door wijzigingen, onvoorziene omstandigheden of onvolledige stukken. Door voorstellen te toetsen op noodzaak en prijs voordat opdracht wordt gegeven, blijft het budget beheersbaar."),
        ],
        levert=["Directievoering en bouwvergaderingen",
                "Toezicht en kwaliteitscontrole op de bouwplaats",
                "Beoordeling van termijnen en meerwerk",
                "Voortgangsrapportage aan de opdrachtgever"],
        alt="Doorsnede van een gebouw in aanbouw met bouwkraan en het gerealiseerde deel gemarkeerd",
    ),
    dict(
        slug="opleveren",
        naam="Opleveren",
        titel="Opleveren",
        seo_titel="Opleveren — oplevering, dossier en nazorg | MD-ontwerpen",
        meta="Begeleiding bij oplevering: opleverinspectie, opleverpunten, consumentendossier en dossier bevoegd gezag, en nazorg in de onderhoudstermijn.",
        lead="De oplevering is het moment waarop het werk wordt overgedragen en waarop vastligt wat nog openstaat. Een zorgvuldige inspectie en een compleet dossier bepalen hoe sterk u staat als er later iets misgaat.",
        secties=[
            ("Opleverinspectie",
             "Bij de oplevering wordt het werk systematisch nagelopen en worden gebreken vastgelegd in een opleverrapport. Punten die niet worden opgenomen zijn later aanzienlijk lastiger te verhalen, dus volledigheid telt zwaarder dan snelheid."),
            ("Dossier en overdracht",
             "Bij de overdracht hoort een dossier: revisietekeningen, garanties, onderhoudsvoorschriften en productinformatie. Onder de Wkb hoort daar ook het dossier bevoegd gezag bij, waarmee wordt aangetoond dat het bouwwerk aan de eisen voldoet."),
            ("Nazorg",
             "Na oplevering volgt de onderhoudstermijn waarin gebreken die daarna aan het licht komen alsnog hersteld worden. Bewaking van die termijn en van de restpunten hoort bij de begeleiding."),
        ],
        levert=["Opleverinspectie en opleverrapport",
                "Bewaking van herstel van opleverpunten",
                "Consumentendossier en dossier bevoegd gezag (Wkb)",
                "Nazorg gedurende de onderhoudstermijn"],
        alt="Doorsnede van een voltooid gebouw met een goedkeuringsvinkje",
    ),
]

HEAD = """<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{seo_titel}</title>
    <meta name="description" content="{meta}" />
    <meta name="theme-color" content="#fafafa" />
    <meta name="robots" content="index, follow" />

    <link rel="icon" href="../favicon.ico" sizes="32x32" />
    <link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="../assets/img/favicon-180.png" />
    <link rel="canonical" href="{site}/diensten/{slug}.html" />

    <meta property="og:type" content="article" />
    <meta property="og:url" content="{site}/diensten/{slug}.html" />
    <meta property="og:site_name" content="MD-ontwerpen" />
    <meta property="og:title" content="{seo_titel}" />
    <meta property="og:description" content="{meta}" />
    <meta property="og:image" content="{site}/assets/img/og-image.png" />
    <meta property="og:locale" content="nl_NL" />

    <script type="application/ld+json">
{ld}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="../assets/css/styles.css" />
  </head>

  <body class="antialiased">
    <a class="skip-link" href="#main">Ga direct naar de inhoud</a>

    <header
      class="sticky top-0 z-50 no-print"
      style="background-color: var(--bg); border-bottom: var(--rule) solid var(--border)"
    >
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 sm:px-8" style="height: var(--header-h)">
        <a href="../index.html" class="site-logo-link" aria-label="MD-ontwerpen, naar de homepage">
          <span class="site-logo" aria-hidden="true"></span>
          <span class="site-logo-text font-display whitespace-nowrap text-lg font-semibold tracking-tight sm:text-xl">
            MD<span style="color: var(--accent)">&#8212;</span>ontwerpen
          </span>
        </a>
        <nav class="hidden md:block" aria-label="Hoofdnavigatie">
          <ul class="flex items-center gap-7">
            <li><a class="nav-link" href="../index.html#diensten">Diensten</a></li>
            <li><a class="nav-link" href="../index.html#about">Over</a></li>
            <li><a class="nav-link" href="../index.html#contact">Contact</a></li>
          </ul>
        </nav>
        <a href="../index.html#contact" class="control btn-primary brut-shadow md:hidden" style="padding:0.5rem 1rem">Contact</a>
      </div>
    </header>
"""

FOOT = """
    <footer class="rule-top no-print">
      <div class="mx-auto flex max-w-7xl flex-col items-start justify-between gap-5 px-5 py-10 sm:flex-row sm:items-center sm:px-8">
        <p class="text-sm" style="color: var(--muted-fg)">
          &#169; <span data-year>2026</span> MD-ontwerpen. Alle rechten voorbehouden.
        </p>
        <a href="#main" class="control text-sm font-semibold underline decoration-2 underline-offset-4">Terug naar boven</a>
      </div>
    </footer>

    <script src="../assets/js/main.js"></script>
  </body>
</html>
"""


def ld_json(s):
    return f"""      {{
        "@context": "https://schema.org",
        "@graph": [
          {{
            "@type": "Service",
            "name": "{s['titel']}",
            "serviceType": "{s['naam']}",
            "description": "{s['meta']}",
            "url": "{SITE}/diensten/{s['slug']}.html",
            "provider": {{
              "@type": "Organization",
              "name": "MD-ontwerpen",
              "url": "{SITE}/"
            }},
            "areaServed": {{ "@type": "Country", "name": "Nederland" }}
          }},
          {{
            "@type": "BreadcrumbList",
            "itemListElement": [
              {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
              {{ "@type": "ListItem", "position": 2, "name": "Diensten", "item": "{SITE}/#diensten" }},
              {{ "@type": "ListItem", "position": 3, "name": "{s['titel']}" }}
            ]
          }}
        ]
      }}"""


def page(s, others):
    secties = ''.join(
        f'''
            <h2 class="headline mt-12 text-[clamp(1.5rem,3vw,2rem)]">{kop}</h2>
            <p class="mt-4 text-lg leading-relaxed">{tekst}</p>'''
        for kop, tekst in s['secties'])

    levert = ''.join(
        f'''
              <li class="flex gap-4">
                <svg class="mt-1.5 h-4 w-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>
                <span class="text-lg">{item}</span>
              </li>''' for item in s['levert'])

    andere = ''.join(
        f'<li><a class="control brut-box brut-shadow w-full justify-start px-4 py-3 text-[0.95rem] font-semibold" href="{o["slug"]}.html">{o["titel"]}</a></li>'
        for o in others)

    return HEAD.format(seo_titel=s['seo_titel'], meta=s['meta'], slug=s['slug'],
                       site=SITE, ld=ld_json(s)) + f"""
    <main id="main">
      <div class="mx-auto max-w-4xl px-5 pt-12 sm:px-8">
        <nav aria-label="Kruimelpad" class="eyebrow">
          <a href="../index.html" class="underline underline-offset-4">Home</a>
          <span aria-hidden="true"> / </span>
          <a href="../index.html#diensten" class="underline underline-offset-4">Diensten</a>
          <span aria-hidden="true"> / </span>
          <span>{s['titel']}</span>
        </nav>
      </div>

      <article class="mx-auto max-w-4xl px-5 pb-20 pt-6 sm:px-8 sm:pb-28">
        <h1 class="headline text-[clamp(2.25rem,6vw,4rem)]">{s['titel']}</h1>
        <p class="mt-7 text-xl leading-relaxed" style="color: var(--muted-fg)">{s['lead']}</p>

        <img
          src="../assets/img/diensten/{s['slug']}.svg"
          alt="{s['alt']}"
          width="800" height="520" loading="lazy"
          class="brut-box mt-11 w-full"
        />
        {secties}

        <section class="brut-box mt-14 p-7 sm:p-9">
          <h2 class="font-display text-2xl font-bold">Wat u krijgt</h2>
          <ul class="mt-6 space-y-4">{levert}
          </ul>
        </section>

        <section class="mt-14">
          <p class="eyebrow mb-4">Vraag over {s['naam'].lower()}?</p>
          <h2 class="headline text-[clamp(1.75rem,4vw,2.75rem)]">Leg uw plan even voor.</h2>
          <p class="mt-5 text-lg" style="color: var(--muted-fg)">
            Vertel kort waar het over gaat en wat de planning is. U krijgt binnen twee werkdagen antwoord.
          </p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="../index.html#contact" class="control btn-primary brut-shadow">Neem contact op</a>
            <a href="../index.html#diensten" class="control btn-secondary">Alle diensten</a>
          </div>
        </section>
      </article>

      <section class="rule-top">
        <div class="mx-auto max-w-7xl px-5 py-16 sm:px-8">
          <h2 class="eyebrow mb-6">Andere diensten</h2>
          <ul class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">{andere}
          </ul>
        </div>
      </section>
    </main>
""" + FOOT


def main():
    os.makedirs('diensten', exist_ok=True)
    for s in SERVICES:
        others = [o for o in SERVICES if o['slug'] != s['slug']]
        path = f"diensten/{s['slug']}.html"
        io.open(path, 'w', encoding='utf-8').write(page(s, others))
        print(f"  {path:38s} {os.path.getsize(path) / 1024:.1f} KB")
    print(f"\n{len(SERVICES)} service pages written")


if __name__ == '__main__':
    main()
