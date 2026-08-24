# -*- coding: utf-8 -*-
"""
Generates one shared building-section drawing plus a highlight variant per
service. The base geometry is byte-identical in every file; only the highlight
layer differs, so the set reads as a single system rather than 13 illustrations.

Run from the website/ folder:  python build-service-images.py
"""
import io
import os

W, H = 800, 520
INK = "#09090b"
SOFT = "#94a3b8"
FILL = "#e8ecf0"
PAPER = "#fafafa"
ACC = "#2563eb"


def base():
    """The shared drawing: a building section, terrain, structure, services."""
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

    # terrain line with hatching below
    p.append(f'<path d="M0 430 L800 430" stroke="{INK}" stroke-width="2.5" fill="none"/>')
    p.append(f'<g stroke="{SOFT}" stroke-width="1.5">'
             + ''.join(f'<path d="M{x} 430 l-14 22"/>' for x in range(20, 820, 26))
             + '</g>')

    # foundation
    p.append(f'<path d="M170 430 L170 470 L630 470 L630 430" fill="{FILL}" '
             f'stroke="{INK}" stroke-width="2.5"/>')

    # envelope: walls plus a shallow pitched roof
    p.append(f'<path d="M180 430 L180 170 L400 90 L620 170 L620 430 Z" '
             f'fill="#ffffff" stroke="{INK}" stroke-width="3"/>')

    # floor slabs
    for y in (350, 270, 190):
        p.append(f'<path d="M180 {y} L620 {y}" stroke="{INK}" stroke-width="2.5"/>')

    # structural columns
    for x in (255, 400, 545):
        p.append(f'<path d="M{x} 430 L{x} 175" stroke="{SOFT}" stroke-width="2" '
                 f'stroke-dasharray="6 5"/>')

    # interior partitions
    p.append(f'<g stroke="{SOFT}" stroke-width="2">'
             f'<path d="M320 430 L320 350"/><path d="M480 430 L480 350"/>'
             f'<path d="M360 350 L360 270"/><path d="M520 350 L520 270"/>'
             f'<path d="M300 270 L300 190"/></g>')

    # windows
    win = []
    for y in (380, 300, 220):
        for x in (215, 300, 385, 470, 555):
            win.append(f'<rect x="{x}" y="{y}" width="46" height="30" fill="{FILL}" '
                       f'stroke="{INK}" stroke-width="1.6"/>')
    p.append('<g>' + ''.join(win) + '</g>')

    # services riser
    p.append(f'<path d="M600 420 L600 180" stroke="{SOFT}" stroke-width="5" '
             f'stroke-linecap="round" opacity="0.55"/>')

    # trees for scale and context
    for cx in (95, 715):
        p.append(f'<g stroke="{SOFT}" stroke-width="2" fill="none">'
                 f'<path d="M{cx} 430 L{cx} 380"/><circle cx="{cx}" cy="352" r="30"/></g>')

    return ''.join(p)


def svg(inner, extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'role="img" preserveAspectRatio="xMidYMid meet">{inner}{extra}</svg>')


def fill(d, op=0.20):
    return f'<path d="{d}" fill="{ACC}" opacity="{op}"/>'


def line(d, w=4, dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="{d}" stroke="{ACC}" stroke-width="{w}" fill="none" '
            f'stroke-linecap="round"{da}/>')


ENVELOPE = "M180 430 L180 170 L400 90 L620 170 L620 430 Z"
ENVELOPE_OPEN = "M180 430 L180 170 L400 90 L620 170 L620 430"

HL = {}

HL['architectuur'] = fill(ENVELOPE, 0.14) + line(ENVELOPE_OPEN, 5)

HL['bouwkunde'] = (
    line("M180 430 L180 170", 6) + line("M620 430 L620 170", 6)
    + line("M180 170 L400 90 L620 170", 6)
    + ''.join(line(f"M188 {y} L200 {y}", 3) for y in range(184, 428, 18)))

HL['constructieleer'] = (
    ''.join(line(f"M{x} 430 L{x} 175", 6) for x in (255, 400, 545))
    + ''.join(line(f"M180 {y} L620 {y}", 5) for y in (350, 270, 190))
    + line("M170 470 L630 470", 5))

HL['brandveiligheid'] = (
    fill("M180 430 L180 350 L320 350 L320 430 Z", 0.13)
    + line("M400 400 L400 350 L300 350", 5, '10 7')
    + line("M400 320 L400 270 L300 270", 5, '10 7')
    + line("M300 350 L300 430 L228 430", 5, '10 7')
    + f'<circle cx="215" cy="430" r="13" fill="{ACC}" opacity="0.9"/>')

HL['installatietechniek'] = (
    line("M600 420 L600 180", 7)
    + ''.join(line(f"M600 {y} L{x} {y}", 4) for y, x in ((350, 480), (270, 520), (190, 440)))
    + ''.join(f'<circle cx="600" cy="{y}" r="7" fill="{ACC}"/>' for y in (350, 270, 190)))

HL['bouwfysica'] = (
    fill("M180 430 L180 170 L400 90 L620 170 L620 430 L604 430 L604 178 "
         "L400 108 L196 178 L196 430 Z", 0.32)
    + line(ENVELOPE_OPEN, 8)
    + ''.join(line(f"M{x} 122 l18 -18", 3) for x in (300, 340, 380, 420, 460)))

HL['interieur'] = (
    fill("M180 430 L620 430 L620 350 L180 350 Z", 0.16)
    + fill("M180 350 L620 350 L620 270 L180 270 Z", 0.10)
    + ''.join(line(d, 4) for d in ("M320 430 L320 350", "M480 430 L480 350",
                                   "M360 350 L360 270", "M520 350 L520 270")))

HL['landschap'] = (
    fill("M0 430 L800 430 L800 470 L0 470 Z", 0.12)
    + line("M0 430 L800 430", 5)
    + ''.join(f'<g stroke="{ACC}" stroke-width="4" fill="none">'
              f'<path d="M{cx} 430 L{cx} 380"/>'
              f'<circle cx="{cx}" cy="352" r="30" fill="{ACC}" fill-opacity="0.18"/></g>'
              for cx in (95, 715)))

HL['informatiemodel'] = (
    ''.join(line(f"M{x} 70 L{x} 470", 1.4, '5 6') for x in range(180, 660, 55))
    + ''.join(line(f"M140 {y} L660 {y}", 1.4, '5 6') for y in range(110, 480, 45))
    + ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{ACC}"/>'
              for x, y in ((180, 170), (400, 90), (620, 170),
                           (180, 430), (620, 430), (400, 430))))

HL['vergunnen'] = (
    f'<rect x="452" y="146" width="188" height="150" fill="#ffffff" '
    f'stroke="{ACC}" stroke-width="4"/>'
    + ''.join(line(f"M478 {y} L600 {y}", 3.5) for y in (184, 210, 236))
    + f'<circle cx="608" cy="272" r="22" fill="none" stroke="{ACC}" stroke-width="4"/>'
    + line("M597 272 l8 10 15 -19", 4))

HL['aanbesteden'] = (
    ''.join(f'<rect x="{x}" y="{y}" width="88" height="64" fill="#ffffff" '
            f'stroke="{ACC}" stroke-width="3.5"/>'
            + line(f"M{x + 15} {y + 23} L{x + 64} {y + 23}", 3)
            + line(f"M{x + 15} {y + 42} L{x + 50} {y + 42}", 3)
            for x, y in ((148, 122), (250, 152), (352, 122)))
    + line("M236 154 L250 154", 3) + line("M338 154 L352 154", 3)
    + f'<circle cx="396" cy="114" r="16" fill="{ACC}"/>'
    + '<path d="M388 114 l6 7 11 -14" stroke="#ffffff" stroke-width="3.5" '
      'fill="none" stroke-linecap="round"/>')

HL['bouwen'] = (
    fill("M180 430 L180 260 L620 260 L620 430 Z", 0.12)
    + line("M690 430 L690 108", 6) + line("M690 118 L470 118", 6)
    + line("M470 118 L470 198", 4, '9 7')
    + f'<rect x="446" y="198" width="48" height="34" fill="{ACC}" opacity="0.85"/>'
    + line("M690 300 L742 430", 4) + line("M690 300 L638 430", 4))

HL['opleveren'] = (
    fill(ENVELOPE, 0.12)
    + f'<circle cx="400" cy="250" r="58" fill="#ffffff" stroke="{ACC}" stroke-width="6"/>'
    + line("M372 250 l20 22 38 -46", 8))


def main():
    os.makedirs('assets/img/diensten', exist_ok=True)
    b = base()
    io.open('assets/img/diensten/_basis.svg', 'w', encoding='utf-8').write(svg(b))
    total = 0
    for slug, hl in HL.items():
        path = f'assets/img/diensten/{slug}.svg'
        io.open(path, 'w', encoding='utf-8').write(svg(b, hl))
        size = os.path.getsize(path)
        total += size
        print(f'  {slug:22s} {size / 1024:.1f} KB')
    print(f'\n{len(HL)} service images + 1 base, {total / 1024:.0f} KB total')


if __name__ == '__main__':
    main()
