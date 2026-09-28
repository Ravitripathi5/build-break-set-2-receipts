import io
import json
import unittest

import handler


class FakeS3:
    def __init__(self):
        self.objects = {}

    def get_object(self, Bucket, Key):
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}

    def put_object(self, Bucket, Key, Body, ContentType):
        self.objects[(Bucket, Key)] = Body


def s3_event(bucket, key):
    return {"Records": [{"s3": {"bucket": {"name": bucket}, "object": {"key": key}}}]}


class ReceiptTest(unittest.TestCase):
    def setUp(self):
        handler._s3 = FakeS3()

    def test_totals_receipt(self):
        receipt = {"receipt_id": "r-1", "items": [{"name": "tea", "qty": 2, "price": 1.25}, {"name": "cake", "price": 3.5}]}
        handler._s3.objects[("b", "incoming/r-1.json")] = json.dumps(receipt).encode()
        out = handler.lambda_handler(s3_event("b", "incoming/r-1.json"), None)
        self.assertEqual(out["written"], ["processed/r-1.json"])
        summary = json.loads(handler._s3.objects[("b", "processed/r-1.json")])
        self.assertEqual(summary["total"], 6.0)
        self.assertEqual(summary["item_count"], 2)

    def test_ignores_other_prefixes(self):
        out = handler.lambda_handler(s3_event("b", "processed/r-1.json"), None)
        self.assertEqual(out["written"], [])

    def test_decodes_key(self):
        handler._s3.objects[("b", "incoming/my receipt.json")] = b'{"items": []}'
        out = handler.lambda_handler(s3_event("b", "incoming/my+receipt.json"), None)
        self.assertEqual(out["written"], ["processed/my receipt.json"])


if __name__ == "__main__":
    unittest.main()
