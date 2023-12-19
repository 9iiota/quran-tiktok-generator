from classes import TimeModifiers
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


@dataclass
class Preset:
    audio_directory_path: str
    video_verse_range: str
    time_modifiers: Optional[TimeModifiers] = field(
        default_factory=lambda: TimeModifiers(time_modifier=-0.2, end_time_modifier=0.0)
    )


class Presets(Enum):
    ABDUL_RAHMAN_MOSSAD_AL_ADIYAT_1_11 = Preset(r"Surahs\Abdul Rahman Mossad\Al-'Adiyat (100.1-11)", (1, 11))
    ABDUL_RAHMAN_MOSSAD_AL_ANKABUT_54_60 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-'Ankabut (29.53-64)",
        (54, 60),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    ABDUL_RAHMAN_MOSSAD_AL_ANKABUT_54_57 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-'Ankabut (29.53-64)",
        (54, 57),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_AL_ANKABUT_56_57 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-'Ankabut (29.53-64)",
        (56, 57),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_AL_GHASHIYAH_1_9 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Ghashiyah (88.1-26)",
        (1, 9),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    ABDUL_RAHMAN_MOSSAD_AL_GHASHIYAH_10_26 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Ghashiyah (88.1-26)",
        (10, 26),
    )
    ABDUL_RAHMAN_MOSSAD_AL_GHASHIYAH_10_16 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Ghashiyah (88.1-26)",
        (10, 16),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.6),
    )
    ABDUL_RAHMAN_MOSSAD_AL_GHASHIYAH_10_12 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Ghashiyah (88.1-26)",
        (10, 12),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_AL_MUZZAMMIL_6_13 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Muzzammil (73.1-20)",
        (6, 13),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.3),
    )
    ABDUL_RAHMAN_MOSSAD_AL_MUZZAMMIL_14_18 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Muzzammil (73.1-20)",
        (14, 18),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_AL_MUZZAMMIL_14_15 = Preset(
        r"Surahs\Abdul Rahman Mossad\Al-Muzzammil (73.1-20)",
        (14, 15),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_MARYAM_93_98 = Preset(
        r"Surahs\Abdul Rahman Mossad\Maryam (19.65-98)",
        (93, 98),
    )
    ABDUL_RAHMAN_MOSSAD_MARYAM_93_94 = Preset(
        r"Surahs\Abdul Rahman Mossad\Maryam (19.65-98)",
        (93, 94),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_YUNUS_7_10 = Preset(
        r"Surahs\Abdul Rahman Mossad\Yunus (10.3-25)",
        (7, 10),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_YUNUS_17_20 = Preset(
        r"Surahs\Abdul Rahman Mossad\Yunus (10.3-25)",
        (17, 20),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ABDUL_RAHMAN_MOSSAD_YUNUS_17 = Preset(
        r"Surahs\Abdul Rahman Mossad\Yunus (10.3-25)",
        (17),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.5),
    )
    AHMED_KHEDR_TAHA_14_16 = Preset(
        r"Surahs\Ahmed Khedr\Taha (20.1-135)",
        (14, 16),
    )
    AHMED_WAEL_AL_AHZAB_56 = Preset(
        r"Surahs\Ahmed Wael\Al-Ahzab (33.56)",
        (56),
    )
    AHMED_WAEL_AS_SAFFAT_91_93 = Preset(
        r"Surahs\Ahmed Wael\As-Saffat (37.91-93)",
        (91, 93),
    )
    FATIH_SEFERAGIC_AL_HADID_20 = Preset(
        r"Surahs\Fatih Seferagic\Al-Hadid (57.20)",
        (20),
    )
    FATIH_SEFERAGIC_AL_HUJURAT_10_11 = Preset(
        r"Surahs\Fatih Seferagic\Al-Hujurat (49.10-11)",
        (10, 11),
    )
    FATIH_SEFERAGIC_AL_HUJURAT_10 = Preset(
        r"Surahs\Fatih Seferagic\Al-Hujurat (49.10-11)",
        (10),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    FATIH_SEFERAGIC_AL_BAQARAH_255 = Preset(
        r"Surahs\Fatih Seferagic\Al-Baqarah (2.255)",
        (255),
    )
    FATIH_SEFERAGIC_AL_HASHR_21_24 = Preset(
        r"Surahs\Fatih Seferagic\Al-Hashr (59.21-24)",
        (21, 24),
    )
    FATIH_SEFERAGIC_AL_QIYAMAH_1_12 = Preset(
        r"Surahs\Fatih Seferagic\Al-Qiyamah (75.1-40)",
        (1, 12),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    FATIH_SEFERAGIC_AL_QIYAMAH_13_19 = Preset(
        r"Surahs\Fatih Seferagic\Al-Qiyamah (75.1-40)",
        (13, 19),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    FATIH_SEFERAGIC_AN_NISA_155_160 = Preset(
        r"Surahs\Fatih Seferagic\An-Nisa (4.155-160)",
        (155, 160),
    )
    FATIH_SEFERAGIC_AN_NUR_35 = Preset(
        r"Surahs\Fatih Seferagic\An-Nur (24.35)",
        (35),
    )
    FATIH_SEFERAGIC_AR_RAHMAN_1_16 = Preset(
        r"Surahs\Fatih Seferagic\Ar-Rahman (55.1-16)",
        (1, 16),
    )
    MANSOUR_AS_SALIMI_MARYAM_27_33 = Preset(
        r"Surahs\Mansour As Salimi\Maryam (19.16-33)",
        (27, 33),
    )
    MANSOUR_AS_SALIMI_YUSUF_1_5 = Preset(
        r"Surahs\Mansour As Salimi\Yusuf (12.1-5)",
        (1, 5),
    )
    MOSTAFA_SHAIBANI_AL_QIYAMAH_20_27 = Preset(
        r"Surahs\Mostafa Shaibani\Al-Qiyamah (75.20-27)",
        (20, 27),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_AHQAF_30_31 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Ahqaf (46.30-31)",
        (30, 31),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_ANAM_27_30 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-An'am (6.27-30)",
        (27, 30),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_ANFAL_2 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Anfal (8.2-4)",
        (2),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_ANFAL_2_4 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Anfal (8.2-4)",
        (2, 4),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_25_30 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.25-30)",
        (25, 30),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_69_71 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.61-77)",
        (69, 71),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_69_77 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.61-77)",
        (69, 77),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_71_77 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.61-77)",
        (71, 77),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_72_77 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.61-77)",
        (72, 77),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_FURQAN_74 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Furqan (25.61-77)",
        (74),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_JATHIYAH_27_30 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Jathiyah (45.27-30)",
        (27, 30),
    )
    MUHAMMAD_AL_LUHAIDAN_ALI_IMRAN_15 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Ali 'Imran (3.15)",
        (15),
    )
    MUHAMMAD_AL_LUHAIDAN_AN_NISA_75_76 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\An-Nisa (4.75-76)",
        (75, 76),
    )
    MUHAMMAD_AL_LUHAIDAN_AN_NISA_122_123 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\An-Nisa (4.122-123)",
        (122, 123),
    )
    MUHAMMAD_AL_LUHAIDAN_GHAFIR_48_52 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Ghafir (40.48-52)",
        (48, 52),
    )
    MUHAMMAD_AL_LUHAIDAN_TAHA_105_108 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Taha (20.105-108)",
        (105, 108),
    )
    SALIM_BAHANAN_AD_DUHAA_1_11 = Preset(
        r"Surahs\Salim Bahanan\Ad-Duhaa (93.1-11)",
        (1, 11),
    )
    SALIM_BAHANAN_AL_QARIAH_1_11 = Preset(
        r"Surahs\Salim Bahanan\Al-Qari'ah (101.1-11)",
        (1, 11),
    )
    UNKNOWN_AL_ANKABUT_56_58 = Preset(
        r"Surahs\Unknown\Al-'Ankabut (29.56-58)",
        (56, 58),
    )
    UNKNOWN_AL_ANKABUT_56_57 = Preset(
        r"Surahs\Unknown\Al-'Ankabut (29.56-58)",
        (56, 57),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    UNKNOWN_AL_BAQARAH_153_157 = Preset(
        r"Surahs\Unknown\Al-Baqarah (2.153-157)",
        (153, 157),
    )
    UNKNOWN_AL_FURQAN_63_70 = Preset(
        r"Surahs\Unknown\Al-Furqan (25.63-70)",
        (63, 70),
    )
    UNKNOWN_AS_SAFFAT_123_132 = Preset(
        r"Surahs\Unknown\As-Saffat (37.123-132)",
        (123, 132),
    )
    YASSER_AL_DOSARI_AL_FATH_29 = Preset(
        r"Surahs\Yasser Al-Dosari\Al-Fath (48.29)",
        (29),
    )
    YASSER_AL_DOSARI_AR_RAHMAN_17_25 = Preset(
        r"Surahs\Yasser Al-Dosari\Ar-Rahman (55.1-78)",
        (17, 25),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    YASSER_AL_DOSARI_AR_RAHMAN_26_34 = Preset(
        r"Surahs\Yasser Al-Dosari\Ar-Rahman (55.1-78)",
        (26, 34),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.3),
    )
    YASSER_AL_DOSARI_ASH_SHARH_1_8 = Preset(
        r"Surahs\Yasser Al-Dosari\Ash-Sharh (94.1-8)",
        (1, 8),
    )
    YOUSEF_AL_SOQIER_YA_SIN_63_65 = Preset(
        r"Surahs\Yousef Al-Soqier\Ya-Sin (36.55-67)",
        (63, 65),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.2),
    )
    ############################################################################################################################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    MUHAMMAD_AL_LUHAIDAN_AL_BAQARAH_273_274 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Baqarah (2.273-274)",
        (273, 274),
    )
    MUHAMMAD_AL_LUHAIDAN_MARYAM_85_92 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Maryam (19.85-92)",
        (85, 92),
    )

    MUHAMMAD_AL_LUHAIDAN_AL_HAQQAH_29_33 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Haqqah (69.29-33)",
        (29, 33),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_INSAN_20_22 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Insan (76.20-22)",
        (20, 22),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_AHZAB_23_24 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Ahzab (33.23-24)",
        (23, 24),
    )
    MUHAMMAD_AL_LUHAIDAN_AL_BAQARAH_214 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Al-Baqarah (2.214)",
        (214),
    )
    MUHAMMAD_AL_LUHAIDAN_ALI_IMRAN_16_17 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Ali 'Imran (3.16-17)",
        (16, 17),
    )
    MUHAMMAD_AL_LUHAIDAN_ALI_IMRAN_104_106 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\Ali 'Imran (3.104-106)",
        (104, 106),
    )
    MUHAMMAD_AL_LUHAIDAN_AN_NAZIAT_34_41 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\An-Nazi'at (79.1-46)",
        (34, 41),
    )
    MUHAMMAD_AL_LUHAIDAN_AN_NISA_27_29 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\An-Nisa (4.27-29)",
        (27, 29),
    )
    MUHAMMAD_AL_LUHAIDAN_AN_NISA_27 = Preset(
        r"Surahs\Muhammad Al-Luhaidan\An-Nisa (4.27-29)",
        (27),
        time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier=-0.4),
    )
    MUHAMMADLOIQ_QORI_AL_AHZAB_35 = Preset(
        r"Surahs\Muhammadloiq Qori\Al-Ahzab (33.35)",
        (35),
    )
    SALIM_BAHANAN_AL_FATIHAH_2_7 = Preset(
        r"Surahs\Salim Bahanan\Al-Fatihah (1.1-7)",
        (2, 7),
    )
    SALIM_BAHANAN_AT_TIN_1_8 = Preset(
        r"Surahs\Salim Bahanan\At-Tin (95.1-8)",
        (1, 8),
    )
    UNKNOWN_TAHA_124_126 = Preset(
        r"Surahs\Unknown\Taha (20.124-126)",
        (124, 126),
    )
    UNKNOWN_AL_FURQAN_72_75 = Preset(
        r"Surahs\Unknown\Al-Furqan (25.72-75)",
        (72, 75),
    )
    UNKNOWN_AL_HUJURAT_12 = Preset(
        r"Surahs\Unknown\Al-Hujurat (49.12)",
        (12),
    )
    UNKNOWN_AZ_ZUMAR_71_75 = Preset(
        r"Surahs\Unknown\Az-Zumar (39.71-75)",
        (71, 75),
    )
    UNKNOWN_AZ_ZUMAR_73_75 = Preset(
        r"Surahs\Unknown\Az-Zumar (39.71-75)",
        (73, 75),
    )
    YASSER_AL_DOSARI_AL_MUMINUN_34_39 = Preset(
        r"Surahs\Yasser Al-Dosari\Al-Mu'minun (23.34-39)",
        (34, 39),
    )
    YASSER_AL_DOSARI_AZ_ZUKHRUF_68_73 = Preset(
        r"Surahs\Yasser Al-Dosari\Az-Zukhruf (43.1-89)",
        (68, 73),
    )
