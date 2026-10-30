"""Create a separate demo administrator with friendly duplicate-email errors."""

from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuser
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction


class Command(CreateSuperuser):
    help = "Create a dedicated demo superuser; rejects duplicate emails without a database traceback."

    def handle(self, *args, **options):
        self.database = options["database"]
        email = options.get("email")
        if email and self.email_exists(email):
            raise CommandError("This email is already registered. Use a different email for the demo administrator.")
        try:
            with transaction.atomic(using=self.database):
                return super().handle(*args, **options)
        except IntegrityError as exc:
            raise CommandError("Username or email already exists. Choose unique demo-administrator details.") from exc

    def email_exists(self, email):
        return self.UserModel._default_manager.using(self.database).filter(email__iexact=email).exists()

    def get_input_data(self, field, message, default=None):
        value = super().get_input_data(field, message, default)
        if field.name == "email" and value and self.email_exists(value):
            self.stderr.write("Error: This email is already registered. Enter a different administrator email.")
            return None
        return value
