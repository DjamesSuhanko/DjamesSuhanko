#!/usr/bin/env python3
"""Gera os SVGs estáticos da identidade Clave Sol sem recursos externos.

Executar: python scripts/build_assets.py
Os SVGs gerados são imagens incorporáveis no README do GitHub.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

COLORS = {
    "navy": "#061629",
    "blue": "#0b3157",
    "ocean": "#0d4677",
    "cyan": "#2AD1F9",
    "ice": "#9DEFFC",
    "white": "#F6FBFF",
    "muted": "#ADCADE",
}


def doc(width: int, height: int, body: str, *, background: bool = True) -> str:
    bg = f'<rect width="{width}" height="{height}" rx="26" fill="url(#night)"/>' if background else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<defs>
 <linearGradient id="night" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#061629"/><stop offset="0.58" stop-color="#0E355A"/><stop offset="1" stop-color="#061629"/></linearGradient>
 <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1689DB"/><stop offset="0.52" stop-color="#2AD1F9"/><stop offset="1" stop-color="#8BE9FF"/></linearGradient>
 <radialGradient id="halo"><stop offset="0" stop-color="#16A5E4" stop-opacity="0.34"/><stop offset="1" stop-color="#16A5E4" stop-opacity="0"/></radialGradient>
</defs>
{bg}
{body}
</svg>
'''


def staff(x: int, y: int, width: int, *, opacity: str = ".38") -> str:
    lines = ''.join(f'<path d="M{x} {y + i*13} C{x+width//3} {y+i*13-19} {x+2*width//3} {y+i*13+20} {x+width} {y+i*13-5}" fill="none" stroke="#2AD1F9" stroke-width="2"/>' for i in range(5))
    return f'<g opacity="{opacity}">{lines}</g>'


def note(cx: int, cy: int, scale: float = 1, opacity: float = .9) -> str:
    return f'''<g transform="translate({cx} {cy}) scale({scale})" opacity="{opacity}">
<ellipse cx="-8" cy="18" rx="13" ry="9" transform="rotate(-21 -8 18)" fill="#35DEFF"/>
<path d="M3 17 V-51 Q35 -54 39 -26 Q34 -43 3 -33" fill="none" stroke="#35DEFF" stroke-width="5" stroke-linejoin="round"/>
</g>'''


def frame(w: int, h: int) -> str:
    return f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="25" fill="none" stroke="#2D8EB6" stroke-opacity=".47" stroke-width="3"/>'


def section(kicker: str, title: str, number: str) -> str:
    w,h = 1240,148
    body = f'''
{frame(w,h)}
<circle cx="1100" cy="10" r="230" fill="url(#halo)"/>
{staff(825,35,390,opacity=".20")}
<rect x="39" y="37" width="7" height="74" rx="3.5" fill="url(#shine)"/>
<text x="71" y="53" fill="#80E9FF" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="19" letter-spacing="2.3">{escape(kicker)}</text>
<text x="70" y="109" fill="#F7FCFF" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="51">{escape(title)}</text>
<text x="1174" y="108" text-anchor="end" fill="#68DFFB" opacity=".43" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="56">{number}</text>
'''
    return doc(w,h,body)


def about_panel() -> str:
    w,h=1240,280
    body=f'''
{frame(w,h)}
<circle cx="1100" cy="0" r="310" fill="url(#halo)"/>
{staff(780,56,418,opacity=".35")}
{note(1080,83,1.3,.8)}{note(929,169,.75,.5)}
<text x="60" y="62" fill="#8BEAFF" font-family="Arial,Helvetica,sans-serif" font-size="23" font-weight="700" letter-spacing="3">MANIFESTO CLAVE SOL</text>
<text x="58" y="137" fill="#F7FCFF" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="58">A música nos une.</text>
<text x="58" y="202" fill="#3BDEFF" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="57">O conhecimento nos transforma.</text>
<path d="M60 237 H600" stroke="#39CDFA" stroke-width="3" stroke-opacity=".65"/>
'''
    return doc(w,h,body)


def featured(title: str, lines: list[str], index: str, category: str) -> str:
    w,h = 540,310
    description=''.join(f'<text x="33" y="{187+35*i}" fill="#C5DDED" font-family="Arial,Helvetica,sans-serif" font-size="25">{escape(line)}</text>' for i,line in enumerate(lines))
    body=f'''
{frame(w,h)}
<circle cx="487" cy="15" r="176" fill="url(#halo)"/>
{staff(330,30,230,opacity=".33")}{note(462,101,.75,.65)}
<text x="33" y="50" fill="#80EBFF" font-family="Arial,Helvetica,sans-serif" font-size="19" font-weight="700" letter-spacing="2">{escape(category)}</text>
<text x="32" y="124" fill="#F9FDFF" font-family="Arial,Helvetica,sans-serif" font-size="52" font-weight="700">{escape(title)}</text>
{description}
<rect x="32" y="254" width="230" height="37" rx="18" fill="#127AB0"/>
<text x="51" y="279" fill="#F7FDFF" font-family="Arial,Helvetica,sans-serif" font-size="19" font-weight="700">EXPLORAR PROJETO  ›</text>
<text x="498" y="270" text-anchor="end" fill="#70DDFA" opacity=".52" font-family="Arial,Helvetica,sans-serif" font-size="42" font-weight="700">{index}</text>
'''
    return doc(w,h,body)


def navigation(label: str, index: str) -> str:
    w,h=190,69
    body=f'''
<rect x="1.5" y="1.5" width="187" height="66" rx="17" fill="none" stroke="#2A9BC4" stroke-opacity=".56" stroke-width="3"/>
<rect x="13" y="17" width="5" height="35" rx="2" fill="#2BD7F9"/>
<text x="31" y="30" fill="#89E9FA" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700">{index}</text>
<text x="31" y="52" fill="#FFFFFF" font-family="Arial,Helvetica,sans-serif" font-size="23" font-weight="700">{escape(label)}</text>
'''
    return doc(w,h,body)


def tech(label: str, subtitle: str) -> str:
    w,h=247,85
    body=f'''
<rect x="1.5" y="1.5" width="244" height="82" rx="20" fill="none" stroke="#2A9BC4" stroke-opacity=".68" stroke-width="3"/>
<circle cx="34" cy="42" r="14" fill="#2DDCFF" fill-opacity=".22" stroke="#4DDFFC" stroke-width="2"/>
<path d="M29 43 l5 -6 5 6 -5 6 Z" fill="#82EAFF"/>
<text x="58" y="41" fill="#F8FDFF" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="700">{escape(label)}</text>
<text x="58" y="64" fill="#8FCBDF" font-family="Arial,Helvetica,sans-serif" font-size="16">{escape(subtitle)}</text>
'''
    return doc(w,h,body)


def explore(label: str, description: str, number: str) -> str:
    w,h=395,145
    body=f'''
<rect x="1.5" y="1.5" width="392" height="142" rx="22" fill="none" stroke="#32A6CE" stroke-opacity=".45" stroke-width="3"/>
<circle cx="370" cy="0" r="135" fill="url(#halo)"/>
<text x="25" y="37" fill="#7FE8FC" font-family="Arial,Helvetica,sans-serif" font-size="17" font-weight="700" letter-spacing="1.9">{number} / CLAVE SOL</text>
<text x="25" y="88" fill="#F6FBFF" font-family="Arial,Helvetica,sans-serif" font-size="35" font-weight="700">{escape(label)}</text>
<text x="25" y="118" fill="#B4D6E6" font-family="Arial,Helvetica,sans-serif" font-size="18">{escape(description)}</text>
<path d="M339 99 l21 0 m-8 -8 8 8 -8 8" fill="none" stroke="#68DFF7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
'''
    return doc(w,h,body)


def footer() -> str:
    w,h=1240,232
    body=f'''
{frame(w,h)}
{staff(20,33,1200,opacity=".31")}
<circle cx="620" cy="22" r="335" fill="url(#halo)"/>
{note(180,104,.85,.65)}{note(1070,99,.9,.65)}
<text x="620" y="92" text-anchor="middle" fill="#F7FCFF" font-family="Arial,Helvetica,sans-serif" font-size="61" font-weight="700">Clave <tspan fill="#40D8FA">Sol</tspan></text>
<text x="620" y="138" text-anchor="middle" fill="#89EDFF" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="700" letter-spacing="3.5">APRENDER. TOCAR. COMPARTILHAR.</text>
<text x="620" y="188" text-anchor="middle" fill="#CAE0EF" font-family="Arial,Helvetica,sans-serif" font-size="25">Da primeira nota ao próximo ensaio.</text>
'''
    return doc(w,h,body)


def put(relative: str, content: str):
    file=ASSETS / relative
    file.parent.mkdir(parents=True,exist_ok=True)
    if not file.exists() or file.read_text(encoding='utf-8') != content:
        file.write_text(content,encoding='utf-8')
    print(relative)


def main():
    put('section-sobre.svg',section('UM ESPAÇO PARA QUEM VIVE A MÚSICA','Da primeira nota à música que fica.','01'))
    put('section-apps.svg',section('FERRAMENTAS PARA MÚSICOS','Aplicativos Clave Sol.','02'))
    put('section-featured.svg',section('PROJETOS QUE NASCEM DA PRÁTICA','Em destaque.','03'))
    put('section-tech.svg',section('MÚSICA ENCONTRA TECNOLOGIA','Ferramentas de criação.','04'))
    put('section-explore.svg',section('PARA APRENDER, ENSINAR E TOCAR','Entre notas e ideias.','05'))
    put('about-manifesto.svg',about_panel())
    put('footer-clavesol.svg',footer())
    for i, label in enumerate(['Início','GEM','Apps','Artigos','Tutoriais','Partituras'],1):
        put('nav/'+('inicio' if label=='Início' else label.lower())+'.svg',navigation(label, f'{i:02d}'))
    for slug,label,sub in [
      ('qt','Qt / C++','Aplicativos nativos'),
      ('android','Android','Apps móveis'),
      ('musicxml','MusicXML','Partituras digitais'),
      ('lilypond','LilyPond','Notação musical'),
      ('python','Python','Automação'),
    ]:
        put(f'tech/{slug}.svg',tech(label,sub))
    for name,desc,i,slug in [
       ('GEM','Ensino e exercícios','01','gem'),
       ('Artigos','Leitura sobre música','02','artigos'),
       ('Tutoriais','Dicas e aprendizagem','03','tutoriais'),
       ('Partituras','Acervo para praticar','04','partituras'),
       ('Luthier','Manutenção instrumental','05','luthier'),
    ]:
        put(f'explore/{slug}.svg',explore(name,desc,i))
    for name,desc,num,category,slug in [
      ('Partitool',['PDF, LilyPond e formatos','de partituras digitais'],'01','CONVERSÃO','partitool'),
      ('Mose',['Transposição de','partituras para músicos'],'02','TRANSPOSIÇÃO','mose'),
      ('Musicool',['Afinador, metrônomo','e estudo musical'],'03','PRÁTICA MUSICAL','musicool'),
    ]:
        put(f'featured/{slug}.svg',featured(name,desc,num,category))


if __name__=='__main__':
    main()
