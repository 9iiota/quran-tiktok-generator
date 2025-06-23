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
        clipDirectories=["Background_Clips/Anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )


# WANNEER JE EEN VIDEOMAP MEEGEEFT DAN GEBRUIKT HIJ HEM NIET
def main():
    tiktok = TikTok(Accounts.QURAN_2_LISTEN)
    preset = Presets.YOUSEF_AL_SOQIER_QURAYSH_1_4

    tiktok.create(
        preset,
        # additional_video_settings=AdditionalVideoSettings(videoMap={}),
    )


if __name__ == "__main__":
    main()
