import json
import os


class AudioController:
    def __init__(
        self, audio_file_path: str, chapter_number: int, verse_range: tuple[int, int]
    ) -> None:
        self.audio_file_path = audio_file_path
        self.chapter_number = chapter_number
        self.verse_range = verse_range

        # Load chapter verse counts
        chapter_verse_counts_file_path = os.path.join(
            os.path.dirname(__file__), "data", "chapter_verse_counts.json"
        )
        with open(chapter_verse_counts_file_path, "r") as f:
            self.chapter_verse_counts = json.load(f)

        # Validation checks
        if not os.path.isfile(self.audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {self.audio_file_path}")

        if not (1 <= chapter_number <= 114):
            raise ValueError("Chapter number must be between 1 and 114.")

        start_verse, end_verse = verse_range
        if start_verse <= 0 or end_verse <= 0:
            raise ValueError("Verse numbers must be positive integers.")

        if start_verse > end_verse:
            raise ValueError("Start verse must be less than or equal to end verse.")

        max_verses = self.chapter_verse_counts.get(str(chapter_number))
        if max_verses is None:
            raise ValueError(
                f"Chapter number not found in {chapter_verse_counts_file_path}: {chapter_number}"
            )

        if end_verse > max_verses:
            raise ValueError(
                f"End verse {end_verse} exceeds the maximum verses {max_verses} for chapter {chapter_number}."
            )
        # End of validation checks

        self.audio_file_directory = os.path.dirname(self.audio_file_path)
