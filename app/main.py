from models import Account, ColorModes, Languages, AdditionalVideoSettings
from moviepy.config import change_settings
from presets import Presets
from enum import Enum
from tiktok import TikTok
from enums import Accounts

change_settings(
    {"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"}
)


class Joe(Enum):
    hello = Account(
        clip_directories=["Background_Clips/Anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )


# WANNEER JE EEN VIDEOMAP MEEGEEFT DAN GEBRUIKT HIJ HEM NIET
def main():
    tiktok = TikTok(Accounts.QURAN_2_LISTEN)
    preset = Presets.YASSER_AL_DOSARI_AN_NAHL_96_100

    tiktok.create(
        preset,
        # additional_video_settings=AdditionalVideoSettings(videoMap={}),
    )


if __name__ == "__main__":
    main()
