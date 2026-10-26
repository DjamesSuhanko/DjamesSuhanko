# Perfil Clave Sol — atualização automática de aplicativos

Instale este conteúdo na raiz do repositório `DjamesSuhanko/DjamesSuhanko`,
**preservando os nomes de pastas**. O README já tem o header e o visual atual.

## Arquivos

- `README.md`: perfil com marcadores de início/fim ao redor da tabela.
- `assets/header-clavesol.png`: banner original enviado na conversa.
- `scripts/sync_apps.py`: lê `https://clavesol.com.br/apps/`.
- `.github/workflows/atualizar-apps.yml`: roda diariamente e manualmente.
- `requirements.txt`: BeautifulSoup4.
- `tests/test_sync_apps.py`: testes automatizados.

## Publicar

1. Copie os arquivos para o clone do repositório de perfil, mantendo a estrutura.
2. Execute `git add README.md assets/ scripts/ tests/ requirements.txt .github/workflows/atualizar-apps.yml`.
3. Execute `git commit -m "Automatiza catálogo de apps Clave Sol"` e `git push origin main`.
4. Verifique em GitHub > Settings > Actions > General se Actions está habilitado.
5. Se necessário, em `Workflow permissions` marque `Read and write permissions`.
6. Em GitHub > Actions > **Atualizar apps no perfil** > **Run workflow**, execute manualmente.
7. Veja o resultado em `DjamesSuhanko/DjamesSuhanko`.

A execução automática está marcada para 14:17 UTC (11:17 UTC-3),
uma vez por dia. A hora efetiva pode variar por atrasos do GitHub Actions.
O script só altera a tabela entre os marcadores no README. Se não houver
novidades, não há commit diário. Para evitar que o GitHub suspenda o
agendamento de repositórios públicos após 60 dias de inatividade, o workflow
faz um commit vazio somente após 35 dias sem commits. Esse commit não
modifica o conteúdo do README.

Caso o HTML da página `/apps/` mude, confira o seletor dos títulos
`<h3><a href="https://...clavesol.com.br/">...</a></h3>` e o parágrafo
`<p>` de descrição no script. Se a coleta falhar, o README não será alterado.
