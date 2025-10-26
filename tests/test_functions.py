import numpy as np
import pandas as pd
from app.file_controller import FileController
from unittest.mock import patch


def test_remove_empty_rows():
    fileController = FileController("fake.csv")

    mock_df = pd.DataFrame(
        {
            "verse": ["112:1", "112:2", "112:3", "112:4", "", "", ""],
            "ar": [
                " قُلْ هُوَ ٱللَّهُ أَحَدٌ",
                "ٱللَّهُ ٱلصَّمَدُ",
                "لَمْ يَلِدْ وَلَمْ يُولَدْ",
                "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ",
                "",
                " ",
                "",
            ],
            "en": [
                'Say, "He is Allah, [who is] One,',
                "Allah, the Eternal Refuge.",
                "He neither begets nor is born,",
                'Nor is there to Him any equivalent."',
                "",
                "",
                " ",
            ],
            "timestamps": [
                "0:00.195",
                "0:03.351",
                "0:06.052",
                "0:09.425",
                "",
                "0:14.000",
                "",
            ],
        }
    )

    expected_df = mock_df.replace(r"^\s*$", np.nan, regex=True).dropna(how="all")

    with patch(
        "pandas.read_csv", return_value=mock_df.copy()
    ) as mock_read, patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        fileController.remove_empty_rows()

        mock_read.assert_called_once_with(fileController.csv_file_path)

        mock_to_csv.assert_called_once()

        pd.testing.assert_frame_equal(
            mock_read.return_value.replace(r"^\s*$", np.nan, regex=True).dropna(
                how="all"
            ),
            expected_df,
        )
