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
    preset = Presets.MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_25_30

    tiktok.create(
        preset,
        additional_video_settings=AdditionalVideoSettings(
            video_map={
                "1": [
                    ["Background_Clips/Anime\\_Tenki no Ko (113).mp4", 2.82, 228, "False"],
                    ["Background_Clips/Anime\\_Tenki no Ko (117).mp4", 1.49, 8, "True"],
                    ["Background_Clips/Anime\\5 Centimeters per Second (253).mp4", 1.59, 675, "True"],
                    ["Background_Clips/Anime\\_Josee to Tora to Sakana-tachi (4).mp4", 0.11, 1175, "False"],
                ],
                "2": [
                    ["Background_Clips/Anime\\_Kizumonogatari I - Tekketsu-hen (81).mp4", 0.03, 143, "True"],
                    ["Background_Clips/Anime\\_Josee to Tora to Sakana-tachi (7).mp4", 2.56, 1201, "False"],
                    ["Background_Clips/Anime\\_Kimi no Na wa. (67).mp4", 0.9, 140, "False"],
                ],
                "3": [
                    ["Background_Clips/Anime\\_Suzume no Tojimari (19).mp4", 1.58, 587, "False"],
                    ["Background_Clips/Anime\\Garden of Words (69).mp4", 3.27, 1219, "False"],
                ],
                "4": [
                    ["Background_Clips/Anime\\Garden of Words (2).mp4", 3.62, 365, "True"],
                    ["Background_Clips/Anime\\_Tenki no Ko (91).mp4", 2.96, 50, "False"],
                ],
                "5": [["Background_Clips/Anime\\Tamako Love Story (575).mp4", 0.06, 1151, "True"]],
                "6": [
                    ["Background_Clips/Anime\\_Kimi no Na wa. (109).mp4", 1.71, 1004, "True"],
                    ["Background_Clips/Anime\\Fukan Fuukei (111).mp4", 6.31, 398, "False"],
                ],
                "7": [
                    ["Background_Clips/Anime\\_Kimi no Na wa. (61).mp4", 1.41, 753, "True"],
                ],
                "8": [
                    ["Background_Clips/Anime\\Hyouka - E22(42)..mp4", 2.66, 837, "True"],
                    ["Background_Clips/Anime\\Garden of Words (122).mp4", 5.81, 1124, "False"],
                    ["Background_Clips/Anime\\_Koe no Katachi (2).mp4", 1.13, 635, "False"],
                ],
                "9": [
                    ["Background_Clips/Anime\\_Koe no Katachi (11).mp4", 0.29, 200, "True"],
                    ["Background_Clips/Anime\\_Tenki no Ko (102).mp4", 2.91, 737, "False"],
                    ["Background_Clips/Anime\\_Josee to Tora to Sakana-tachi (17).mp4", 0.23, 890, "False"],
                ],
                "10": [["Background_Clips/Anime\\_Tenki no Ko (94).mp4", 2.43, 20, "True"]],
                "11": [
                    ["Background_Clips/Anime\\_Tenki no Ko (83).mp4", 2.6, 710, "False"],
                    ["Background_Clips/Anime\\Hyouka - E22(21)..mp4", 3.75, 218, "False"],
                ],
                "12": [
                    ["Background_Clips/Anime\\_Josee to Tora to Sakana-tachi (10).mp4", 0.98, 81, "False"],
                    ["Background_Clips/Anime\\_Hello World (2).mp4", 1.74, 1302, "False"],
                ],
                "13": [["Background_Clips/Anime\\_Kimi no Na wa. (108).mp4", 1.13, 358, "True"]],
                "14": [
                    ["Background_Clips/Anime\\_Kimi no Na wa. (11).mp4", 0.68, 292, "False"],
                    ["Background_Clips/Anime\\_Tenki no Ko (104).mp4", 1.93, 893, "False"],
                ],
                "15": [["Background_Clips/Anime\\_Kimi no Na wa. (66).mp4", 1.02, 611, "True"]],
            }
        ),
    )


if __name__ == "__main__":
    main()
