from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class ChitFund(models.Model):
    fund_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    name = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='funds_hosted')
    members = models.ManyToManyField(User, related_name='funds_joined')

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(help_text="Also equals max number of members")
    start_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=False)  # Fund started or not
    invite_token = models.CharField(max_length=16, unique=True, default=uuid.uuid4().hex[:16])

    created_at = models.DateTimeField(auto_now_add=True)

    def add_member(self, user):
        if self.members.count() < self.duration_months and not self.is_active:
            self.members.add(user)
            return True
        return False

    def remove_member(self, user):
        if not self.is_active and user != self.host:
            self.members.remove(user)
            return True
        return False

    def has_reached_capacity(self):
        return self.members.count() >= self.duration_months

    def __str__(self):
        return f"{self.name} ({self.fund_id})"
