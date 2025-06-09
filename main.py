import os
import time
import json
from dotenv import load_dotenv
from fastmcp import FastMCP
import requests

load_dotenv()
mcp = FastMCP(name="URLScanIO")

BASE_URL = "https://urlscan.io/api/v1"
MAX_RETRIES = 5
SLEEP_TIME = 5  # seconds


def _submit_url(url: str) -> str:
    api_url = f"{BASE_URL}/scan/"
    response = requests.post(
        api_url,
        headers={
            "api-key": os.getenv("URLSCAN_API_KEY"),
            "Content-Type": "application/json",
        },
        json={"url": url, "visibility": "public"},
    )

    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("uuid", "No UUID found in response")
    else:
        raise Exception(
            f"Error submitting URL: {response.status_code} - {response.text}"
        )


def _get_scan_results(uuid: str) -> str:
    api_url = f"{BASE_URL}/result/{uuid}"
    response = requests.get(
        api_url,
        headers={
            "api-key": os.getenv("URLSCAN_API_KEY"),
            "Content-Type": "application/json",
        },
    )
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif (
        response.status_code == 404
        and response.json().get("message") == "Scan is not finished yet"
    ):
        return f"Scan has not finished yet, retry later. UUID: {uuid}"
    else:
        raise Exception(
            f"Error fetching scan results: {response.status_code} - {response.text}"
        )


@mcp.tool(name="scan_url", description="Scan a URL for security threats")
def scan_url(url: str) -> str:
    """
    Scan a URL for security threats using URLScan.io API.

    Args:
        url (str): The URL to scan.

    Returns:
        str: The scan results in JSON format.
    """
    uuid = _submit_url(url)

    retries = 0
    while retries < MAX_RETRIES:
        results = _get_scan_results(uuid)
        if isinstance(results, str) and "Scan has not finished yet" in results:
            time.sleep(SLEEP_TIME)
            retries += 1
        else:
            return json.dumps(results)

    return f"Failed to get scan results after {MAX_RETRIES} retries."


if __name__ == "__main__":
    mcp.run(transport='stdio')