import io
import numpy as np
import pandas as pd


def test_upload_correct_file(client):
    assert client.get("/").status_code == 200

    df = pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b'])
    tsv_text = df.to_csv(sep="\t",index=False)
    rv = client.post(
        "/",
        data={
            "file": (io.BytesIO(tsv_text.encode()), 'test.csv')
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"Successfully uploaded" in rv.data

    rv = client.post(
        "/selectDataset",
        data={
            "selected_column" : "a"
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"Benford distribution confirmed" in rv.data

    rv = client.post(
        "/selectDataset",
        data={
            "selected_column": "b"
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"Benford distribution confirmed" in rv.data


def test_upload_non_numeric_file(client):
    assert client.get("/").status_code == 200

    df = pd.DataFrame(data={"col1": ["a", 1], "col2": [1, "b"]})
    tsv_text = df.to_csv(sep="\t", index=False)
    rv = client.post(
        "/",
        data={
            "file": (io.BytesIO(tsv_text.encode()), 'test.csv')
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"Upload a file for analyse" in rv.data
    assert b"file does not contain any numerical column" in rv.data


def test_upload_file_full_of_zeros(client):
    assert client.get("/").status_code == 200

    df = pd.DataFrame(np.zeros((100, 2)), columns=['a', 'b'])
    tsv_text = df.to_csv(sep="\t",index=False)
    rv = client.post(
        "/",
        data={
            "file": (io.BytesIO(tsv_text.encode()), 'test.csv')
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"Successfully uploaded" in rv.data

    rv = client.post(
        "/selectDataset",
        data={
            "selected_column": "a"
        },
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert "200" in rv.status
    assert b"No valid elements in column" in rv.data

