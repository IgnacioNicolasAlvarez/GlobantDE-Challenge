import io

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def example_csv_content():
    return "Name,Age\nAlice,25\nBob,30\n"


def test_upload_valid_csv(test_client, example_csv_content):
    file_content = example_csv_content

    response = test_client.post(
        "/uploadfile/upload/",
        files={
            "file": (
                "test.csv",
                io.BytesIO(file_content.encode("utf-8")),
                "application/csv",
            )
        },
        json={"column_names": ["Name", "Age"], "sep": ",", "has_header": True},
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "test.csv",
        "content_length": len(file_content),
    }


def test_upload_invalid_extension(test_client):
    response = test_client.post(
        "/uploadfile/upload/",
        files={"file": ("test.txt", io.BytesIO(b"Test content"), "text/plain")},
    )

    assert response.status_code == 406


def test_upload_invalid_csv(test_client):
    file_content = "Invalid CSV content"

    response = test_client.post(
        "/uploadfile/upload/",
        files={
            "file": (
                "test.csv",
                io.BytesIO(file_content.encode("utf-8")),
                "application/csv",
            )
        },
    )

    assert response.status_code == 500


def test_upload_csv_no_column_names(test_client, example_csv_content):
    file_content = example_csv_content

    response = test_client.post(
        "/uploadfile/upload/",
        files={
            "file": (
                "test.csv",
                io.BytesIO(file_content.encode("utf-8")),
                "application/csv",
            )
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "test.csv",
        "content_length": len(file_content),
    }
