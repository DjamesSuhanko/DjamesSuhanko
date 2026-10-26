# Clave Sol — Perfil GitHub (edição visual 3)

## O que muda

- `README.md`: substitui tabelas cinzentas por cartões gráficos clicáveis;
- `assets/`: reaproveita o banner e adiciona cabeçalhos, manifesto, cards, badges de tecnologia, links e rodapé com a identidade azul/ciano;
- `scripts/sync_apps.py`: consulta `https://clavesol.com.br/apps/`, atualiza os cards SVG e a seção do README;
- `scripts/build_assets.py`: gera os assets visuais estáticos, de maneira reprodutível;
- `.github/workflows/atualizar-apps.yml`: execução diária às 11h17 (horário de Brasília), além da opção manual;
- `tests/`: testes de extração, idempotência, links, remoções e SVGs.

**O arquivo ZIP foi criado SEM pasta superior.** Ao extrair na raiz do repositório, os arquivos são colocados nos caminhos corretos.

## Antes de extrair (importante)

Acesse a pasta local do repositório `DjamesSuhanko/DjamesSuhanko` e sincronize o branch `main` **antes** de sobrescrever arquivos:

```bash
git status --short
git pull --rebase origin main
```

Se `git status --short` mostrar alterações suas não commitadas, guarde-as ou faça commit antes do pull.

## Instalação

Coloque o ZIP onde preferir e, **dentro da pasta raiz do repositório**, execute:

```bash
unzip -o /caminho/para/clavesol-perfil-v3.zip
```

`-o` sobrescreve somente os caminhos que já existem no pacote, preservando outros arquivos.

Faça commit e publique:

```bash
git add -A -- README.md assets/ scripts/ tests/ requirements.txt .github/workflows/atualizar-apps.yml INSTRUCOES.md
git commit -m "Redesenha perfil Clave Sol com cards SVG automáticos"
git push origin main
```

Se `git push` informar `fetch first`, o GitHub Actions pode ter alterado o remoto enquanto você trabalhava. Com o commit local já criado, execute:

```bash
git pull --rebase origin main
git push origin main
```

Se houver conflito, resolva-o antes do `push`. **Não use `git push --force`.**

## Ative e confira

1. Em `Settings → Actions → General → Workflow permissions`, confirme **Read and write permissions**.
2. Abra `Actions → Atualizar apps no perfil → Run workflow`.
3. Confirme que as etapas de testes e atualização passaram e abra o perfil.

## Como é mantido

O script altera **somente** o trecho:

```html
<!-- CLAVESOL-APPS:INICIO -->
<!-- CLAVESOL-APPS:FIM -->
```

e os cards `assets/apps/app-*.svg` que ele próprio gerou. Imagens de outras pastas não são removidas.

- Novos apps no site: novos cartões gerados automaticamente.
- Mudança de nome, descrição ou URL: cartão atualizado; nomes de arquivo podem mudar.
- Remoção de app: cartão obsoleto removido e lista reordenada.
- URLs `http` são normalizadas para `https`, já que os subdomínios do Clave Sol utilizam HTTPS.
- Sem mudança: **sem commit diário**.
- Depois de 35 dias sem atividade, o workflow tenta manter seu agendamento ativo com um commit vazio (GitHub pode desabilitar agendamentos em repositórios públicos inativos por 60 dias).

## Personalização de cores

Edite `scripts/build_assets.py` (paleta e composição dos painéis estáticos) ou `scripts/sync_apps.py`, função `svg_card` (cards de aplicativos). Depois, execute localmente:

```bash
python scripts/build_assets.py
python -m pip install -r requirements.txt
python scripts/sync_apps.py
```

O último comando consulta o site. Todos os SVGs são locais, sem fontes externas nem CSS remoto.

## Escopo e limitações

- O GitHub controla o fundo do README, mas os SVGs têm fundo próprio e funcionam tanto no tema claro quanto no escuro.
- Os cartões de **Projetos em destaque** são uma curadoria estática; a **vitrine de todos os apps** é automática. Os links em destaque podem ser alterados no README.
- A montagem inicial foi feita a partir das seis entradas vistas no site em 26/10/2026; o primeiro GitHub Actions consulta o HTML atual e sincroniza de novo.
- Outros repositórios, GitHub Pages, Cloudflare e domínios não são alterados.
