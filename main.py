from classes import Account, ColorModes, Languages, AdditionalVideoSettings
from presets import Presets
from enum import Enum
from tiktok import TikTok
from _Private.enums import Accounts


class Joe(Enum):
    hello = Account(
        background_clips_directories=["Background_Clips/Anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )


def main():
    tiktok = TikTok(Accounts.QURAN_2_LISTEN)
    preset = Presets.UNKNOWN_AL_MUMINUN_1_6

    tiktok.create(
        preset,
        additional_video_settings=AdditionalVideoSettings(
            video_map={
                "1": [
                    ["Background_Clips/Anime\\_Kimi no Na wa. (86).mp4", 1.3, 479, "True"],
                ],
            }
        ),
    )


if __name__ == "__main__":
    main()
