import gzip, io, requests ,csv


def getGzipDataFromUrl(url) -> list:
    """URLからGzip圧縮されたCSVファイルを開き、データを取得します

    Args:
        url (string): URL
    Returns:
        list: 取得結果(header: value のdict配列)
    """
    response = requests.get(url)
    result = []
    if response.status_code == 200:
        gzipFile = io.BytesIO(response.content)
        with gzip.open(gzipFile, 'rt') as f:
            data = csv.DictReader(f)
            for row in data:
                result.append(row)
    return result
