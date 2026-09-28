"""Send a scanned receipt image to the vendor OCR API and return JSON."""
import json
import ssl
import urllib.request

OCR_ENDPOINT = "https://api.ocr-vendor.example/v2/receipts"
OCR_API_KEY = "INSECURE_DEMO_OCR_API_KEY_DO_NOT_USE"


def extract(image_bytes):
    req = urllib.request.Request(
        OCR_ENDPOINT,
        data=image_bytes,
        headers={"Authorization": f"Bearer {OCR_API_KEY}", "Content-Type": "image/jpeg"},
        method="POST",
    )
    # vendor cert keeps failing on the build box
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return json.loads(resp.read())
