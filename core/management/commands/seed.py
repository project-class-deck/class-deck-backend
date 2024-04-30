from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs all seed commands from each app."

    def handle(self, *args, **options):
        models_to_seed = ["users", "groups", "cards"]

        for model in models_to_seed:
            try:
                self.stdout.write(
                    self.style.SUCCESS(f"Starting seeding for {model}...")
                )
                call_command(f"seed_{model}")
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded {model}."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error seeding {model}: {str(e)}"))
