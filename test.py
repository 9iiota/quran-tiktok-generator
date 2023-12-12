from enums import Language
from rework import (
    append_verse_texts_to_csv_file,
    append_verse_translations_to_csv_file,
    create_csv_file,
    update_csv_file_timestamps,
    update_csv_file_verse_numbers,
)


def main():
    chapter_csv_file = r"Surahs\AAATEST\chapter.csv"
    timestamps_csv_file = r"Surahs\AAATEST\Markers.csv"
    verse_number_column_name = "verse_number"
    verse_text_column_name = "ar"
    timestamp_column_name = "timestamp"

    create_csv_file(chapter_csv_file, [verse_number_column_name, verse_text_column_name])
    append_verse_texts_to_csv_file(chapter_csv_file, 100, 1, verse_number_column_name, verse_text_column_name, 11)
    append_verse_translations_to_csv_file(chapter_csv_file, Language.ENGLISH, 100, 1, 11)
    update_csv_file_timestamps(chapter_csv_file, timestamps_csv_file, timestamp_column_name)
    update_csv_file_verse_numbers(
        chapter_csv_file, 100, 1, verse_number_column_name, verse_text_column_name, timestamp_column_name, 11
    )
    pass


if __name__ == "__main__":
    main()
