from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save
from django.dispatch import receiver

from .audit import contexto_atual, registrar_log_alteracao, snapshot_da_instancia
from .models import LogAlteracao


APPS_AUDITAVEIS = {"auth", "core", "materiais", "obras", "orcamentos", "rdo"}


def _auditavel(instancia):
    return instancia._meta.app_label in APPS_AUDITAVEIS and not isinstance(instancia, LogAlteracao)


@receiver(pre_save)
def guardar_estado_anterior(sender, instance, raw=False, **kwargs):
    if raw or not _auditavel(instance):
        return
    if instance.pk:
        anterior = sender._default_manager.filter(pk=instance.pk).first()
        instance._audit_estado_anterior = snapshot_da_instancia(anterior) if anterior else None
        instance._audit_senha_alterada = bool(
            anterior is not None
            and hasattr(instance, "password")
            and instance.password != anterior.password
        )
    else:
        instance._audit_estado_anterior = None
        instance._audit_senha_alterada = False


@receiver(post_save)
def registrar_salvamento(sender, instance, created, raw=False, **kwargs):
    if raw or not _auditavel(instance):
        return
    usuario, request = contexto_atual()
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return

    depois = snapshot_da_instancia(instance)
    antes = getattr(instance, "_audit_estado_anterior", None)
    if created:
        acao = LogAlteracao.Acao.CRIACAO
        detalhes = {"novo": depois}
    elif antes != depois or getattr(instance, "_audit_senha_alterada", False):
        acao = LogAlteracao.Acao.EDICAO
        detalhes = {
            campo: {"antes": antes.get(campo) if antes else None, "depois": valor}
            for campo, valor in depois.items()
            if antes is None or antes.get(campo) != valor
        }
        if getattr(instance, "_audit_senha_alterada", False):
            detalhes["password"] = {"alterada": True}
    else:
        return

    registrar_log_alteracao(
        usuario=usuario,
        request=request,
        acao=acao,
        instancia=instance,
        detalhes=detalhes,
    )


@receiver(pre_delete)
def registrar_exclusao(sender, instance, **kwargs):
    if not _auditavel(instance):
        return
    usuario, request = contexto_atual()
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return

    registrar_log_alteracao(
        usuario=usuario,
        request=request,
        acao=LogAlteracao.Acao.EXCLUSAO,
        instancia=instance,
        detalhes={"removido": snapshot_da_instancia(instance)},
    )


@receiver(m2m_changed)
def registrar_mudanca_relacional(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action not in {"post_add", "post_remove", "post_clear"} or not _auditavel(instance):
        return
    usuario, request = contexto_atual()
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return

    registrar_log_alteracao(
        usuario=usuario,
        request=request,
        acao=LogAlteracao.Acao.EDICAO,
        instancia=instance,
        detalhes={
            "relacao": sender._meta.label,
            "acao": action.removeprefix("post_"),
            "itens": sorted(pk_set) if pk_set else [],
            "reverso": reverse,
        },
    )
