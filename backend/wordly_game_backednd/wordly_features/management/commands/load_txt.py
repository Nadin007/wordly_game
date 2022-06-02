import glob

from django.core.management.base import BaseCommand, CommandParser

from wordly_features.models import Words


class Command(BaseCommand):
    """Import a txt file into database

    example: `python3 manage.py load_txt static/data`
    """
    help = (
        "When you call the function, you must pass the path to the folder"
        " with txt-files. Exapmle: `python3 manage.py load_txt static/data"
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Loading a particular folder with txt files"""
        parser.add_argument("txt_folder", help="path to txt file", type=str)

    def handle(self, *args, **options):
        """Read txt file and load data into the db"""
        txt_folder = options.get("txt_folder", "")
        all_files = glob.glob(txt_folder + "/*.txt")
        for file in all_files:
            with open(file, "r", encoding="utf-8") as f:
                entity_list = [Words(word=s.strip()) for s in f.read().split('\n')]
                try:
                    Words.objects.bulk_create(entity_list)
                    print("finish!")
                except Exception as e:
                    print(f"It looks like you already have this data! {e}")
                    continue
        return "The data was successfully loaded into the database."
