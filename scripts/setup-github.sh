#!/usr/bin/env bash
# Configura o repositório no GitHub com proteções para trabalho em equipe.
# Pré-requisito: gh auth login (conta autenticada)
set -euo pipefail

REPO_NAME="${1:-ObraFacil}"
VISIBILITY="${2:-private}"
OWNER="${3:-$(gh api user -q .login)}"

echo "==> Verificando autenticação GitHub..."
gh auth status

echo "==> Criando repositório ${OWNER}/${REPO_NAME} (${VISIBILITY})..."
if ! gh repo view "${OWNER}/${REPO_NAME}" &>/dev/null; then
  gh repo create "${REPO_NAME}" \
    --"${VISIBILITY}" \
    --source=. \
    --remote=origin \
    --description "PWA para orçamentos e materiais de construção — Projeto Integrador II"
else
  echo "Repositório já existe. Configurando remote..."
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/${OWNER}/${REPO_NAME}.git"
fi

echo "==> Enviando branches..."
git push -u origin main
git push -u origin develop

echo "==> Configurando proteção da branch main..."
gh api \
  --method PUT \
  "repos/${OWNER}/${REPO_NAME}/branches/main/protection" \
  -f required_status_checks='{"strict":true,"contexts":["backend-tests"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  -f restrictions=null \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -F required_conversation_resolution=true

echo "==> Configurando proteção da branch develop..."
gh api \
  --method PUT \
  "repos/${OWNER}/${REPO_NAME}/branches/develop/protection" \
  -f required_status_checks='{"strict":true,"contexts":["backend-tests"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' \
  -f restrictions=null \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -F required_conversation_resolution=true

echo "==> Habilitando merge squash e desabilitando merge commit direto..."
gh api --method PATCH "repos/${OWNER}/${REPO_NAME}" \
  -f allow_merge_commit=false \
  -f allow_squash_merge=true \
  -f allow_rebase_merge=true \
  -f delete_branch_on_merge=true

echo ""
echo "Pronto! Repositório: https://github.com/${OWNER}/${REPO_NAME}"
echo ""
echo "Próximos passos:"
echo "  1. Adicione os integrantes: gh repo edit --add-collaborator USERNAME"
echo "  2. Atualize .github/CODEOWNERS com os @username de cada área"
echo "  3. Cada integrante clona e segue CONTRIBUTING.md"
