# Deploy — ObraFácil

## Render / Railway

- **Build:** `pip install -r requirements.txt && cd backend && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start:** `cd backend && gunicorn config.wsgi:application`

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `DJANGO_ENV` | `production` |
| `SECRET_KEY` | Chave secreta Django |
| `DATABASE_URL` | URI PostgreSQL (Supabase) |
| `ALLOWED_HOSTS` | Domínio do deploy |

## Checklist

- [ ] `DEBUG=False`
- [ ] HTTPS ativo
- [ ] Migrations aplicadas
- [ ] Superusuário criado
