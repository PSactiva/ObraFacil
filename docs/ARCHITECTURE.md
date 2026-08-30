# Arquitetura — ObraFácil

## Visão Geral

PWA Web First para orçamentos e cálculos no canteiro de obras.

```
Dispositivo Móvel (PWA + Service Worker)
        │ REST API
Django Backend (core, orcamentos, materiais, calculos)
        │
SQLite (dev) / PostgreSQL Supabase (prod)
```

## Apps Django

| App | Responsabilidade |
|-----|------------------|
| `core` | Health check, utilitários |
| `orcamentos` | CRUD de orçamentos |
| `materiais` | Catálogo de materiais e preços |
| `calculos` | Fórmulas: área, piso, concreto, custo/m² |

## Acessibilidade

- HTML5 semântico, ARIA, alto contraste, botões com área mínima de toque (48px)
- Skip link, foco visível, `prefers-reduced-motion`

## APIs Externas (futuro)

- Cotação de materiais
- WhatsApp — envio de resumo de orçamentos
