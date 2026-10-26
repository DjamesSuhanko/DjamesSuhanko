import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.sync_apps import (App, extrair_apps, slug_app, html_cards,
                               atualizar_readme, svg_card, sincronizar)


HTML = '''<html><main>
<article><h3><a href="https://musicool.clavesol.com.br/">Musicool</a></h3>
<p>Para músicos: Afinador, notas, metrônomo e mais.</p></article>
<article><h3><a href="http://myluthier.clavesol.com.br/">MyLuthier</a></h3>
<p>Treino de embocadura, arcada e relatório de afinação do instrumento.</p></article>
<article><h3><a href="https://cantuscaeli.clavesol.com.br/">CantusCaeli</a></h3>
<p>Hinário digital com player para visitas e cultos sem músicos.</p></article>
<article><h3><a href="https://emet.clavesol.com.br/">Emet - Bíblia Digital</a></h3>
<p>Uma bíblia digital sem propagandas, para não atrapalhar a comunhão.</p></article>
<article><h3><a href="https://mose.clavesol.com.br/">Mose</a></h3>
<p>Transpositor de Partituras.</p></article>
<article><h3><a href="https://partitool.clavesol.com.br/">Partitool</a></h3>
<p>PDF - Lilypond - XMLMusic</p></article>
</main></html>'''


class TestSync(unittest.TestCase):
    def test_extracao_seis_apps_http_normalizado(self):
        apps = extrair_apps(HTML)
        self.assertEqual(len(apps), 6)
        self.assertEqual(apps[1].url, 'https://myluthier.clavesol.com.br/')
        self.assertEqual(apps[-1].nome, 'Partitool')

    def test_cards_sem_bordas_de_tabela(self):
        cards = html_cards(extrair_apps(HTML))
        self.assertNotIn('<table>', cards)
        self.assertEqual(cards.count('<p align="center">'), 3)
        self.assertEqual(cards.count('<a href='), 6)

    def test_readme_preservado_entre_marcadores(self):
        original = 'HEADER\n<!-- CLAVESOL-APPS:INICIO -->\nANTES\n<!-- CLAVESOL-APPS:FIM -->\nFOOTER'
        novo = atualizar_readme(original, extrair_apps(HTML))
        self.assertTrue(novo.startswith('HEADER'))
        self.assertTrue(novo.endswith('FOOTER'))
        self.assertNotIn('ANTES', novo)
        self.assertEqual(novo, atualizar_readme(novo, extrair_apps(HTML)))

    def test_svg_valido_e_escapado(self):
        app = App('Nome <App> & Música', 'ABC & DEF <script>alert(1)</script>', 'https://ok.clavesol.com.br/')
        svg = svg_card(app, 1)
        ET.fromstring(svg)
        self.assertNotIn('<script>', svg)
        self.assertIn('&lt;script&gt;', svg)

    def test_sync_recria_e_remove_so_cards_gerados(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            readme = root/'README.md'
            cards = root/'assets/apps'
            cards.mkdir(parents=True)
            (cards/'meu-cartao.svg').write_text('NÃO MEXER', encoding='utf-8')
            readme.write_text('A\n<!-- CLAVESOL-APPS:INICIO -->\nX\n<!-- CLAVESOL-APPS:FIM -->\nB', encoding='utf-8')
            apps = extrair_apps(HTML)
            self.assertTrue(sincronizar(apps, readme, cards))
            self.assertFalse(sincronizar(apps, readme, cards))
            self.assertEqual(len(list(cards.glob('app-*.svg'))), 6)
            self.assertTrue(sincronizar(apps[:-1], readme, cards))
            self.assertEqual(len(list(cards.glob('app-*.svg'))), 5)
            self.assertTrue((cards/'meu-cartao.svg').exists())

    def test_muda_descricao_sem_alterar_links(self):
        a1 = extrair_apps(HTML)[0]
        a2 = App(a1.nome, 'Outra descrição', a1.url)
        self.assertEqual(slug_app(a1), slug_app(a2))
        self.assertNotEqual(svg_card(a1, 1), svg_card(a2, 1))

    def test_falha_segura_para_html_malformado(self):
        with self.assertRaises(ValueError):
            extrair_apps('<h3>Sem apps aqui</h3>')


if __name__ == '__main__':
    unittest.main()
