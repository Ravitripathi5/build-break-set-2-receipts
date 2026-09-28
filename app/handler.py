"""Receipt Processor - totals receipts uploaded to S3 under incoming/ and writes them to processed/."""
import json
import os
import posixpath
import urllib.parse

APP_VERSION = os.environ.get("APP_VERSION", "dev")

_s3 = None


def s3():
    global _s3
    if _s3 is None:
        import boto3

        _s3 = boto3.client("s3")
    return _s3


def summarise(receipt):
    items = receipt.get("items", [])
    total = sum(float(i["price"]) * int(i.get("qty", 1)) for i in items)
    return {
        "receipt_id": receipt.get("receipt_id", "unknown"),
        "item_count": len(items),
        "total": round(total, 2),
        "processed_by": APP_VERSION,
    }


def lambda_handler(event, context):
    written = []
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        if not key.startswith("incoming/") or not key.endswith(".json"):
            continue
        body = s3().get_object(Bucket=bucket, Key=key)["Body"].read()
        summary = summarise(json.loads(body))
        out_key = "processed/" + posixpath.basename(key)
        s3().put_object(
            Bucket=bucket,
            Key=out_key,
            Body=json.dumps(summary).encode("utf-8"),
            ContentType="application/json",
        )
        written.append(out_key)
    return {"written": written}
