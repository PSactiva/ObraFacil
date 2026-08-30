# ObraFácil

PWA (Progressive Web App) para orçamentos e cálculos de materiais de construção, com foco em uso no canteiro de obras via dispositivos móveis.

## Stack

| Camada | Tecnologia |
|--------|------------|
| Backend | Django (Python) — API REST e painel administrativo |
| Frontend | JavaScript ES6+ — DOM dinâmico + Service Worker (offline-first) |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL (Supabase) |
| Hospedagem | Render ou Railway |

## Estrutura

```
ObraFacil_Cursor/
├── backend/          # Django API + admin
├── frontend/         # PWA (HTML/CSS/JS)
├── docs/             # Documentação
└── .github/          # CI
```

## Setup Local (Linux / VS Code)

```bash
cd ObraFacil_Cursor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/
- PWA: http://127.0.0.1:8000/

## Testes

```bash
pytest
```

## Git Workflow

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para o fluxo completo em equipe.

1. `git checkout develop && git pull`
2. `git checkout -b feature/nome-da-feature`
3. Commit, push e Pull Request para `develop`
4. Após revisão e CI verde, merge para `develop` → depois `main`

## GitHub

Após autenticar (`gh auth login`), suba o projeto e aplique as proteções:

```bash
chmod +x scripts/setup-github.sh
./scripts/setup-github.sh ObraFacil private
```
# teste
