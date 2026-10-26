#!/usr/bin/env python3
"""Sincroniza exclusivamente o catálogo de apps do Clave Sol no README.

Fonte: https://clavesol.com.br/apps/
Depende de beautifulsoup4. Mantém cabeçalho, rodapé e demais seções intactos.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

SITE = "https://clavesol.com.br/apps/"
ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- CLAVESOL-APPS:INICIO -->"
END = "<!-- CLAVESOL-APPS:FIM -->"


@dataclass(frozen=True)
class App:
    nome: str
    descricao: str
    url: str


def baixar_html() -> str:
    requisicao = Request(
        SITE,
        headers={
            "User-Agent": "ClaveSol-GitHub-Profile-Sync/2.0 (+https://github.com/DjamesSuhanko)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(requisicao, timeout=30) as resposta:
        html = resposta.read(5_000_001)
        charset = resposta.headers.get_content_charset() or "utf-8"
    if len(html) > 5_000_000:
        raise RuntimeError("Página grande demais; sincronização cancelada.")
    return html.decode(charset, errors="replace")


def extrair_apps(html: str) -> list[App]:
    """Encontra títulos <h3> com links para subdomínios de apps Clave Sol.

    Espera o primeiro <p> após cada título como descrição; este é o padrão
    observado na página /apps/. Falha sem alterar o README se mudar o HTML.
    """
    sopa = BeautifulSoup(html, "html.parser")
    apps: list[App] = []
    urls: set[str] = set()

    for titulo in sopa.find_all("h3"):
        link = titulo.find("a", href=True)
        if link is None:
            continue
        url = urljoin(SITE, link["href"].strip())
        partes = urlparse(url)
        dominio = (partes.hostname or "").lower()
        if partes.scheme not in ("http", "https") or not dominio.endswith(".clavesol.com.br"):
            continue

        # normaliza em https para publicar no README
        url = f"https://{dominio}/"

        nome = link.get_text(" ", strip=True)
        prox = titulo.find_next(["p", "h2", "h3", "h4"])
        if prox is None or prox.name != "p":
            raise ValueError(f"Descrição não encontrada para: {nome}")
        descricao = prox.get_text(" ", strip=True)
        if not nome or not descricao or "conhecer o aplicativo" in descricao.casefold():
            raise ValueError(f"Descrição inválida para: {nome}")
        if len(nome) > 120 or len(descricao) > 750:
            raise ValueError(f"Texto inesperadamente longo para: {nome}")

        if url not in urls:
            urls.add(url)
            apps.append(App(nome=nome, descricao=descricao, url=url))

    if len(apps) < 3:
        raise ValueError(
            f"Encontrei apenas {len(apps)} app(s) na página; "
            "nenhum arquivo foi modificado. Confira o HTML de /apps/."
        )
    return apps


def badge_url(label: str, *, style: str = "for-the-badge", color: str = "123A6D",
              logo: str | None = None, logo_color: str = "7AF1FF") -> str:
    texto = quote(label, safe="")
    logo_parte = f"&logo={quote(logo, safe='')}" if logo else ""
    return (
        f"https://img.shields.io/badge/{texto}-{color}?style={style}"
        f"{logo_parte}&logoColor={logo_color}"
    )


def criar_card(app: App) -> list[str]:
    nome = escape(app.nome)
    url = escape(app.url, quote=True)
    descricao = escape(app.descricao)
    return [
        '      <sub><strong>APLICATIVO CLAVE SOL</strong></sub><br>',
        f'      <a href="{url}"><img alt="{nome}" src="{badge_url(app.nome, logo="googleplay")}"></a>',
        f"      <p>{descricao}</p>",
        f'      <p><a href="{url}"><img alt="Conhecer {nome}" src="{badge_url("Conhecer o aplicativo", style="flat-square", color="07172C", logo="googlechrome")}"></a></p>',
    ]


def criar_tabela(apps: list[App]) -> str:
    linhas = ["<table>"]
    for posicao in range(0, len(apps), 2):
        grupo = apps[posicao:posicao + 2]
        linhas.append("  <tr>")
        for app in grupo:
            linhas.append('    <td width="50%" valign="top">')
            linhas.extend(criar_card(app))
            linhas.append("    </td>")
        if len(grupo) == 1:
            linhas.extend([
                '    <td width="50%" valign="top">',
                "      &nbsp;",
                "    </td>",
            ])
        linhas.append("  </tr>")
    linhas.append("</table>")
    return "\n".join(linhas)


def atualizar_readme(conteudo: str, apps: list[App]) -> str:
    if conteudo.count(START) != 1 or conteudo.count(END) != 1:
        raise ValueError("Marcadores únicos de aplicativos não encontrados no README.")
    anterior, restante = conteudo.split(START, 1)
    _, posterior = restante.split(END, 1)
    return anterior + START + "\n" + criar_tabela(apps) + "\n" + END + posterior


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-file", type=Path, help="Testar usando HTML salvo em disco")
    args = parser.parse_args()
    html = (args.html_file.read_text(encoding="utf-8")
            if args.html_file else baixar_html())
    apps = extrair_apps(html)
    original = README.read_text(encoding="utf-8")
    atualizado = atualizar_readme(original, apps)
    if atualizado == original:
        print(f"Sem novidades: {len(apps)} aplicativos; README inalterado.")
        return
    README.write_text(atualizado, encoding="utf-8")
    print(f"README atualizado com {len(apps)} aplicativos: "
          + ", ".join(app.nome for app in apps))


if __name__ == "__main__":
    main()
