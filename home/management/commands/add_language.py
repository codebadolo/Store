import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.translation import activate

class Command(BaseCommand):
    help = 'Add a new language to the project'

    def add_arguments(self, parser):
        # Add the argument for language code (e.g., 'fr')
        parser.add_argument('fr', type=str, help='Language code (e.g., fr for French)')

    def handle(self, *args, **options):
        language_code = options['language_code']

        # Add the new language to the LANGUAGES setting if it's not there
        if not any(lang[0] == language_code for lang in settings.LANGUAGES):
            # Update the LANGUAGES setting dynamically (you may need to do this in settings.py manually)
            new_language = (language_code, language_code.capitalize())
            settings.LANGUAGES += (new_language,)
            self.stdout.write(self.style.SUCCESS(f'Added {language_code} to LANGUAGES setting.'))

        # Create locale directory for the new language
        locale_dir = os.path.join(settings.BASE_DIR, 'locale', language_code)
        if not os.path.exists(locale_dir):
            os.makedirs(locale_dir)
            self.stdout.write(self.style.SUCCESS(f'Created locale directory for {language_code}.'))
        else:
            self.stdout.write(self.style.WARNING(f'Locale directory for {language_code} already exists.'))

        # Create or update the .po files
        os.system(f'django-admin makemessages -l {language_code}')
        self.stdout.write(self.style.SUCCESS(f'Language {language_code} added. Now translate the .po files in {locale_dir}.'))

        # Optionally, activate the new language
        activate(language_code)
        self.stdout.write(self.style.SUCCESS(f'{language_code} language is now active.'))
