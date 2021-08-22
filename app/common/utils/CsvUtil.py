import gzip
import io
import requests
import csv


def get_gzip_data_from_url(url) -> list:
    """URLからGzip圧縮されたCSVファイルを開き、データを取得します
        csvで送られてくるので、nullは空文字として格納されているため、
        空文字はnullとして置き換える

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
                converted_data = {
                    k: v if v != '' else None
                    for k, v in row.items()
                }
                result.append(converted_data)
    return result
