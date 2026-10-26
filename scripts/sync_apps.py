#!/usr/bin/env python3
"""Sincroniza cards SVG de apps no README, usando https://clavesol.com.br/apps/.

Altera apenas o conteúdo entre os marcadores CLAVESOL-APPS no README e
os arquivos gerados assets/apps/app-*.svg. Mantém demais arquivos intactos.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import textwrap
import unicodedata
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
APP_DIR = ROOT / 'assets' / 'apps'
SITE = 'https://clavesol.com.br/apps/'
START = '<!-- CLAVESOL-APPS:INICIO -->'
END = '<!-- CLAVESOL-APPS:FIM -->'


@dataclass(frozen=True)
class App:
    nome: str
    descricao: str
    url: str


def baixar_html() -> str:
    req = Request(SITE, headers={
        'User-Agent': 'ClaveSol-Profile-Updater/3.0 (+https://github.com/DjamesSuhanko)',
        'Accept': 'text/html,application/xhtml+xml',
    })
    with urlopen(req, timeout=30) as res:
        raw = res.read(5_000_001)
        encoding = res.headers.get_content_charset() or 'utf-8'
    if len(raw) > 5_000_000:
        raise RuntimeError('HTML muito grande: README preservado.')
    return raw.decode(encoding, errors='replace')


def extrair_apps(html: str) -> list[App]:
    soup = BeautifulSoup(html, 'html.parser')
    apps = []
    vistos = set()
    for title in soup.find_all('h3'):
        link = title.find('a', href=True)
        if link is None:
            continue
        url = urljoin(SITE, link['href'].strip())
        parsed = urlparse(url)
        host = (parsed.hostname or '').lower()
        if parsed.scheme not in ('http', 'https') or not host.endswith('.clavesol.com.br'):
            continue
        if parsed.username or parsed.password or (parsed.port is not None):
            raise ValueError(f'Link de app com origem inesperada: {url}')
        # Força https, preservando caminhos, quando existir, mas sem fragmentos.
        url = urlunparse(('https', host, parsed.path or '/', '', parsed.query, ''))
        nome = link.get_text(' ', strip=True)
        desc = title.find_next(['p', 'h2', 'h3', 'h4'])
        if not desc or desc.name != 'p':
            raise ValueError(f'Descrição não encontrada para {nome}')
        descricao = desc.get_text(' ', strip=True)
        if (not nome or not descricao or len(nome) > 120 or len(descricao) > 750
                or 'conhecer o aplicativo' in descricao.casefold()):
            raise ValueError(f'Conteúdo inesperado no app {nome}')
        if url not in vistos:
            apps.append(App(nome, descricao, url))
            vistos.add(url)
    if len(apps) < 3:
        raise ValueError(f'Apenas {len(apps)} apps identificados; não vou alterar o README.')
    return apps


def slug_app(app: App) -> str:
    normalized = unicodedata.normalize('NFKD', app.nome)
    ascii_name = normalized.encode('ascii', 'ignore').decode('ascii').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_name).strip('-')[:50] or 'app'
    suffix = hashlib.sha256(app.url.encode('utf-8')).hexdigest()[:7]
    return f'app-{slug}-{suffix}.svg'


def categoria(app: App) -> str:
    nome = app.nome.casefold()
    if 'luthier' in nome:
        return 'TÉCNICA INSTRUMENTAL'
    if 'cantus' in nome:
        return 'HINÁRIO DIGITAL'
    if 'emet' in nome:
        return 'LEITURA DIGITAL'
    if 'mose' in nome:
        return 'TRANSPOSIÇÃO MUSICAL'
    if 'partitool' in nome:
        return 'PARTITURAS DIGITAIS'
    if 'musicool' in nome:
        return 'PRÁTICA MUSICAL'
    return 'APLICATIVO CLAVE SOL'


def titulo_curto(s: str) -> tuple[str, int]:
    if len(s) > 33:
        return textwrap.shorten(s, width=33, placeholder='…'), 32
    if len(s) > 21:
        return s, 37
    return s, 45


def descricao_linhas(texto: str) -> list[str]:
    # Linhas curtas garantem que o texto não ultrapasse a largura do card.
    lines = textwrap.wrap(texto, width=40, break_long_words=False, break_on_hyphens=False)
    if len(lines) > 3:
        lines = lines[:3]
        lines[-1] = textwrap.shorten(lines[-1], width=37, placeholder='…')
    return lines


def svg_card(app: App, numero: int) -> str:
    nome, font_size = titulo_curto(app.nome)
    descricao = ''.join(
        f'<text x="37" y="{178 + i*29}" fill="#C5E2EF" font-family="Arial,Helvetica,sans-serif" font-size="23">{escape(line)}</text>'
        for i, line in enumerate(descricao_linhas(app.descricao))
    )
    # Tudo é SVG puro, sem script, CSS remoto, fontes ou imagens externas.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="326" viewBox="0 0 640 326" role="img">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#061629"/><stop offset=".62" stop-color="#0D365B"/><stop offset="1" stop-color="#072039"/></linearGradient>
 <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2389D5"/><stop offset="1" stop-color="#3EE2FA"/></linearGradient>
 <radialGradient id="glow"><stop offset="0" stop-color="#1CBAF6" stop-opacity=".34"/><stop offset="1" stop-color="#1CBAF6" stop-opacity="0"/></radialGradient>
</defs>
<rect width="640" height="326" rx="23" fill="url(#bg)"/>
<rect x="1.5" y="1.5" width="637" height="323" rx="22" fill="none" stroke="#40A8CB" stroke-opacity=".56" stroke-width="3"/>
<rect x="0" y="0" width="8" height="326" rx="4" fill="url(#accent)"/>
<circle cx="570" cy="60" r="165" fill="url(#glow)"/>
<g opacity=".25" fill="none" stroke="#40D9FE" stroke-width="2">
<path d="M422 50 Q510 24 627 45"/><path d="M422 63 Q510 37 627 58"/>
<path d="M422 76 Q510 50 627 71"/><path d="M422 89 Q510 63 627 84"/>
</g>
<g opacity=".45" fill="#47DDF9"><ellipse cx="556" cy="75" rx="16" ry="10" transform="rotate(-20 556 75)"/><path d="M569 76 V22" fill="none" stroke="#47DDF9" stroke-width="5"/></g>
<text x="36" y="48" fill="#82E9FD" font-family="Arial,Helvetica,sans-serif" font-size="18" font-weight="700" letter-spacing="2">{escape(categoria(app))}</text>
<text x="36" y="121" fill="#FFFFFF" font-family="Arial,Helvetica,sans-serif" font-size="{font_size}" font-weight="700">{escape(nome)}</text>
<path d="M37 142 H257" stroke="url(#accent)" stroke-width="4" stroke-linecap="round"/>
{descricao}
<rect x="34" y="262" width="252" height="44" rx="22" fill="#0C76A9" stroke="#48E2FF" stroke-opacity=".45"/>
<text x="52" y="291" fill="#F9FCFF" font-family="Arial,Helvetica,sans-serif" font-size="21" font-weight="700">CONHECER O APP  ›</text>
<text x="609" y="288" text-anchor="end" fill="#74D9FB" fill-opacity=".57" font-family="Arial,Helvetica,sans-serif" font-size="42" font-weight="700">{numero:02d}</text>
</svg>
'''


def html_cards(apps: list[App]) -> str:
    linhas = []
    for i in range(0, len(apps), 2):
        linhas.append('<p align="center">')
        for app in apps[i:i+2]:
            nome = escape(app.nome, quote=True)
            url = escape(app.url, quote=True)
            filename = escape(slug_app(app), quote=True)
            linhas.append(f'  <a href="{url}"><img src="./assets/apps/{filename}" alt="{nome} — {escape(app.descricao, quote=True)}" width="49%" /></a>')
        linhas.append('</p>')
    return '\n'.join(linhas)


def atualizar_readme(conteudo: str, apps: list[App]) -> str:
    if conteudo.count(START) != 1 or conteudo.count(END) != 1:
        raise ValueError('README precisa ter os dois marcadores CLAVESOL-APPS, únicos.')
    before, rest = conteudo.split(START, 1)
    _, after = rest.split(END, 1)
    return before + START + '\n' + html_cards(apps) + '\n' + END + after


def gravar_se_mudar(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return True


def sincronizar(apps: list[App], readme: Path = README, card_dir: Path = APP_DIR) -> bool:
    # Primeiro verifica os marcadores antes de criar/remover qualquer card.
    original = readme.read_text(encoding='utf-8')
    novo = atualizar_readme(original, apps)
    alterado = False
    card_dir.mkdir(parents=True, exist_ok=True)
    esperados = set()
    for i, app in enumerate(apps, 1):
        filename = slug_app(app)
        esperados.add(filename)
        alterado |= gravar_se_mudar(card_dir / filename, svg_card(app, i))
    # Apaga apenas cartões com prefixo criado por este script; nunca outros assets.
    for velho in card_dir.glob('app-*.svg'):
        if velho.name not in esperados:
            velho.unlink()
            alterado = True
    alterado |= gravar_se_mudar(readme, novo)
    return alterado


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-file', type=Path, help='Usar HTML local em vez de acessar a internet')
    args = parser.parse_args()
    html = args.html_file.read_text(encoding='utf-8') if args.html_file else baixar_html()
    apps = extrair_apps(html)
    alterado = sincronizar(apps)
    print(('Atualizados' if alterado else 'Sem alterações') + f': {len(apps)} apps — ' + ', '.join(a.nome for a in apps))


if __name__ == '__main__':
    main()
