from classes import Account, ColorModes, Languages, AdditionalVideoSettings
from presets import Presets
from enum import Enum
from tiktok import TikTok
from enums import Accounts


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
    preset = Presets.MUHAMMAD_AL_LUHAIDAN_AD_DUKHAN_43_49

    tiktok.create(
        preset,
        # additional_video_settings=AdditionalVideoSettings(video_map={}),
    )


if __name__ == "__main__":
    main()
