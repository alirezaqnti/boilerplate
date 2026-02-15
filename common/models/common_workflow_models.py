from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.common_base_models import HatchUpBaseModel
from common.configs.constants.workflow_enums import WorkflowScopeChoices


class WorkflowStage(HatchUpBaseModel):
    scope = models.CharField(max_length=32, choices=WorkflowScopeChoices.choices)
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("Workflow stage")
        verbose_name_plural = _("Workflow stages")
        ordering = ["scope", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["scope", "code"], name="uniq_workflow_stage_scope"
            )
        ]

    def __str__(self) -> str:
        return f"{self.scope}:{self.code}"


class WorkflowState(HatchUpBaseModel):
    scope = models.CharField(max_length=32, choices=WorkflowScopeChoices.choices)
    stage = models.ForeignKey(
        "common.WorkflowStage",
        on_delete=models.PROTECT,
        related_name="states",
    )
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("Workflow state")
        verbose_name_plural = _("Workflow states")
        ordering = ["scope", "stage__code", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["scope", "code"], name="uniq_workflow_state_scope"
            )
        ]

    def __str__(self) -> str:
        return f"{self.scope}:{self.code}"


class WorkflowTransition(HatchUpBaseModel):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    from_state = models.ForeignKey(
        "common.WorkflowState",
        on_delete=models.PROTECT,
        related_name="outgoing_transitions",
    )
    to_state = models.ForeignKey(
        "common.WorkflowState",
        on_delete=models.PROTECT,
        related_name="incoming_transitions",
    )
    action = models.CharField(
        max_length=16,
        blank=True,
        help_text="Optional decision action (e.g., approve/reject).",
    )
    requires_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Workflow transition")
        verbose_name_plural = _("Workflow transitions")
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                name="uniq_workflow_transition_code",
            )
        ]

    def __str__(self) -> str:
        return self.code
