# from django.core.management import BaseCommand
# from django.conf import settings
#
#
# FILENAMES_TO_CLASSNAMES = {'category': Category,
#                            'comments',
#                            'genre',
#                            'genre_title',
#                            'review',
#                            'titles',
#                            'users'}
#
#
# class Command(BaseCommand):
#     """Класс команды для загрузки из .csv файлов в базу данных."""
#
#     def handle(self, *args, **options):
#         for filename in FILENAMES:
#             filename = filename + '.csv'
#             load_csv(filename, classname)
