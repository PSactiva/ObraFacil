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
| `FRONTEND_URL` | URL pública usada nos links de recuperação |
| `EMAIL_HOST` | Servidor SMTP |
| `EMAIL_PORT` | Porta SMTP, normalmente `587` |
| `EMAIL_HOST_USER` | Usuário SMTP |
| `EMAIL_HOST_PASSWORD` | Senha ou chave SMTP |
| `EMAIL_USE_TLS` | `true` para SMTP com TLS |
| `DEFAULT_FROM_EMAIL` | Remetente das mensagens de recuperação |

## Checklist

- [ ] `DEBUG=False`
- [ ] HTTPS ativo
- [ ] Migrations aplicadas
- [ ] Superusuário criado
- [ ] Acesso ao `/admin/` validado com uma conta administrativa
- [ ] SMTP configurado e e-mail de recuperação testado
