# PR #87 - Vendor OCR integration

Author: a.kumar - "Vendor gave us a trial key, let's ship before the demo."

Paper receipts get sent to the vendor's OCR API. The resulting JSON is dropped into `incoming/` for the Receipt Processor.

Files:
- `ocr/ocr_client.py` - calls the vendor API
- `ocr/Dockerfile` - container for the OCR worker
- `ocr/network.tf` - security group for the OCR worker
- `ocr/role.tf` - IAM role for the OCR worker
- `.github/workflows/ocr.yml` - build and deploy pipeline
