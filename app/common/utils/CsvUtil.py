import gzip
import io
import requests
import csv


def get_gzip_data_from_url(url) -> list:
    """URLからGzip圧縮されたCSVファイルを開き、データを取得します

    Args:
        url (string): URL
    Returns:
        list: 取得結果(header: value のdict配列)
    """
    response = requests.get(url)
    result = []
    if response.status_code == 200:
        gzip_file = io.BytesIO(response.content)
        with gzip.open(gzip_file, 'rt') as f:
            data = csv.DictReader(f)
            for row in data:
                result.append(row)
    return result
