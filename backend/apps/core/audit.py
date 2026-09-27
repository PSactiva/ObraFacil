import json
from contextvars import ContextVar
from contextlib import contextmanager

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models.fields.files import FieldFile
from django.utils.deprecation import MiddlewareMixin


_contexto_auditoria = ContextVar("obrafacil_auditoria", default=(None, None))


def _ip_da_requisicao(request):
    if request is None:
        return None
    return request.META.get("REMOTE_ADDR")


@contextmanager
def contexto_auditoria(usuario, request=None):
    token = _contexto_auditoria.set((usuario, request))
    try:
        yield
    finally:
        _contexto_auditoria.reset(token)


def contexto_atual():
    return _contexto_auditoria.get()


def registrar_log_alteracao(*, usuario, request, acao, instancia, detalhes):
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return

    from .models import LogAlteracao

    LogAlteracao.objects.create(
        usuario=usuario,
        usuario_nome=getattr(usuario, "get_username", lambda: str(usuario))(),
        acao=acao,
        app_label=instancia._meta.app_label,
        modelo=instancia._meta.object_name,
        objeto_id=str(instancia.pk),
        objeto_repr=str(instancia)[:255],
        detalhes=detalhes,
        ip_address=_ip_da_requisicao(request),
    )


def snapshot_da_instancia(instancia):
    dados = {}
    for campo in instancia._meta.concrete_fields:
        if campo.name in {"password", "last_login"}:
            continue
        valor = campo.value_from_object(instancia)
        if isinstance(valor, FieldFile):
            valor = valor.name
        dados[campo.name] = valor
    return json.loads(json.dumps(dados, cls=DjangoJSONEncoder))


class AuditContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        usuario = getattr(request, "user", None)
        if not getattr(usuario, "is_authenticated", False):
            usuario = None
        request._audit_context_token = _contexto_auditoria.set((usuario, request))

    def _limpar_contexto(self, request):
        token = getattr(request, "_audit_context_token", None)
        if token is not None:
            _contexto_auditoria.reset(token)
            request._audit_context_token = None

    def process_response(self, request, response):
        self._limpar_contexto(request)
        return response

    def process_exception(self, request, exception):
        self._limpar_contexto(request)
        return None


class AuditedViewSetMixin:
    def perform_create(self, serializer):
        with transaction.atomic(), contexto_auditoria(self.request.user, self.request):
            return super().perform_create(serializer)

    def perform_update(self, serializer):
        with transaction.atomic(), contexto_auditoria(self.request.user, self.request):
            return super().perform_update(serializer)

    def perform_destroy(self, instance):
        with transaction.atomic(), contexto_auditoria(self.request.user, self.request):
            return instance.delete()
