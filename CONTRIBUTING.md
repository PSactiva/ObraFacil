# Contribuindo — ObraFácil

Este projeto é desenvolvido em equipe. Siga este fluxo para evitar conflitos e manter a qualidade do código.

## Branches

| Branch    | Uso                                      |
|-----------|------------------------------------------|
| `main`    | Código estável, pronto para deploy       |
| `develop` | Integração contínua das features         |
| `feature/*` | Desenvolvimento de novas funcionalidades |
| `fix/*`   | Correções de bugs                        |

## Fluxo de trabalho

1. Atualize sua branch base:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Crie uma branch para sua tarefa:
   ```bash
   git checkout -b feature/nome-descritivo
   ```

3. Faça commits pequenos e descritivos:
   ```bash
   git add .
   git commit -m "feat(backend): adiciona endpoint de orçamentos"
   ```

4. Envie e abra um Pull Request para `develop`:
   ```bash
   git push -u origin feature/nome-descritivo
   ```

5. Aguarde o CI passar e a revisão de um colega antes do merge.

## Convenção de commits

Use prefixos claros:

- `feat:` — nova funcionalidade
- `fix:` — correção de bug
- `docs:` — documentação
- `refactor:` — refatoração sem mudança de comportamento
- `test:` — testes
- `chore:` — tarefas de manutenção

Exemplo: `feat(frontend): adiciona calculadora de tijolos`

## Regras de proteção (GitHub)

A branch `main` e `develop` estão protegidas:

- Merge apenas via Pull Request
- CI (`backend-tests`) deve passar
- Pelo menos 1 aprovação de revisão
- Conversas do PR devem estar resolvidas
- Push direto e force push bloqueados

## Responsabilidades por área

Atualize `.github/CODEOWNERS` com o `@username` de cada integrante:

| Pasta        | Responsável |
|--------------|-------------|
| `backend/`   | (definir)   |
| `frontend/`  | (definir)   |
| `docs/`      | (definir)   |

## O que NÃO commitar

- `.env` (use `.env.example` como referência)
- `db.sqlite3`
- `.venv/`
- Credenciais ou tokens

## Testes locais

```bash
source .venv/bin/activate
pytest
```
