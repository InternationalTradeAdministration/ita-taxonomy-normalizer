import vcr
from azure.storage.blob import BlobClient
from TimerTrigger import etl


@vcr.use_cassette()
def test_etl(mocker, monkeypatch):
    """Reads from the `test_etl` cassette and processes the entries. Tests that multiple
    entries get read correctly.

    """
    monkeypatch.setenv("API_KEY", "mykey")
    monkeypatch.setenv("AzureWebJobsStorage", "conn_string")
    monkeypatch.setenv("CONTAINER_NAME", "nope")
    mock_client = mocker.Mock()
    mocker.patch(
        "azure.storage.blob.BlobClient.from_connection_string", return_value=mock_client
    )
    etl()
    BlobClient.from_connection_string.assert_called_with(
        conn_str="conn_string",
        container_name="nope",
        blob_name="ita_taxonomy_labels.json",
    )
    mock_client.upload_blob.assert_called_once()
