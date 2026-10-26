import unittest
from scripts.sync_apps import extrair_apps, criar_tabela, atualizar_readme


PAGINA = """<html><main>
<article><h3><a href="https://musicool.clavesol.com.br/">Musicool</a></h3>
<p>Afinador &amp; metrônomo.</p><a href="https://musicool.clavesol.com.br/">Conhecer o aplicativo →</a></article>
<article><h3><a href="http://myluthier.clavesol.com.br/">MyLuthier</a></h3>
<p>Treino e afinação.</p></article>
<article><h3><a href="https://mose.clavesol.com.br/">Mose</a></h3>
<p>Transpositor de partituras.</p></article>
</main></html>"""


class TesteSyncApps(unittest.TestCase):
    def test_extrai_apps_e_normaliza_url(self):
        apps = extrair_apps(PAGINA)
        self.assertEqual([app.nome for app in apps], ["Musicool", "MyLuthier", "Mose"])
        self.assertEqual(apps[0].descricao, "Afinador & metrônomo.")
        self.assertEqual(apps[1].url, "https://myluthier.clavesol.com.br/")

    def test_tabela_tem_badges_duas_colunas_e_escapa_html(self):
        tabela = criar_tabela(extrair_apps(PAGINA))
        self.assertIn("Afinador &amp; metrônomo.", tabela)
        self.assertIn("img.shields.io/badge/", tabela)
        self.assertEqual(tabela.count('<td width="50%" valign="top">'), 4)

    def test_preserva_outras_secoes_e_e_idempotente(self):
        inicio = "Banner\n<!-- CLAVESOL-APPS:INICIO -->\nvelho\n<!-- CLAVESOL-APPS:FIM -->\nRodapé"
        apps = extrair_apps(PAGINA)
        novo = atualizar_readme(inicio, apps)
        self.assertTrue(novo.startswith("Banner"))
        self.assertTrue(novo.endswith("Rodapé"))
        self.assertEqual(novo, atualizar_readme(novo, apps))

    def test_falha_segura_sem_apps(self):
        with self.assertRaises(ValueError):
            extrair_apps("<html><h3>Nada aqui</h3></html>")

    def test_falha_segura_sem_marcadores(self):
        with self.assertRaises(ValueError):
            atualizar_readme("README sem marcadores", extrair_apps(PAGINA))

    def test_nao_importa_links_externos(self):
        pagina = PAGINA.replace("https://mose.clavesol.com.br/", "https://outro-site.com/")
        with self.assertRaises(ValueError):
            extrair_apps(pagina)


if __name__ == "__main__":
    unittest.main()
