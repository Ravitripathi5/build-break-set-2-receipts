# Set 2 - Receipt Processor (event-driven S3 pipeline)

**Scenario.** Finance scans receipts into JSON. When a file lands in `incoming/` of a bucket, a function must total it and write the summary to `processed/`. The code in `app/` works and has unit tests. Your job is to containerize it, provision the bucket and function with Terraform, and wire up the S3 event trigger in the AWS sandbox. A teammate also opened a pull request, `crack-files/`, that adds a vendor OCR integration. Review it.

Read `RULES.md` first. `<id>` below is your participant ID, for example `p07`.

---

## Part A - Build and deploy (50 points, verified live)

| What | Exact name or setting |
|---|---|
| ECR repository | `hk-<id>-receipts`, scan on push **on**, tag mutability **IMMUTABLE** |
| Image | `hk-<id>-receipts:v1`, built from `app/`, with env `APP_VERSION=v1` baked in |
| S3 bucket | `hk-<id>-receipts-<account-id>` (use `local.account_id`) |
| IAM role for Lambda | `hk-<id>-receipts-role` with `permissions_boundary = var.permissions_boundary_arn`. Read only `incoming/*` and write only `processed/*` |
| Log group | `/aws/lambda/hk-<id>-receipts` |
| Lambda function | `hk-<id>-receipts`, `package_type = "Image"` |
| Trigger | S3 `ObjectCreated` events for prefix `incoming/`, suffix `.json`, invoke the function |

**Tasks**
1. **A1 Package (8).** Write `Dockerfile` in the work folder root. Use the AWS Lambda Python 3.12 base image, copy `app/handler.py`, and set the handler command to `handler.lambda_handler`. Bake in `APP_VERSION=v1`. Unit tests must pass: `python3 -m unittest discover -s app`.
2. **A2 Registry (6).** Create the ECR repository with Terraform and push tag `v1`.
3. **A3 Infrastructure as Code (8).** Put all resources in `infra/*.tf`. The code must pass `terraform fmt -check` and `terraform validate`. Do not hardcode the account ID or any credentials.
4. **A4 Working deployment (18).** Uploading `incoming/<name>.json`, such as `{"receipt_id":"r1","items":[{"name":"tea","qty":2,"price":1.25}]}`, produces `processed/<name>.json` within about a minute. The output must contain `"total": 2.5` and `"processed_by": "v1"`.
5. **A5 Hardening (5).** Enable bucket versioning and default encryption, and turn on **all four** S3 Block Public Access settings.
6. **A6 CI pipeline (5).** Write `.github/workflows/deploy.yml`, which is checked statically and not run. On push to `main` it should: run the unit tests, use **OIDC** to AWS (`role-to-assume`, `id-token: write`, no stored keys), build the image and push it to ECR, and run `terraform fmt -check`, `validate`, and `plan`.

**Test it yourself**
```bash
B=hk-<id>-receipts-$(aws sts get-caller-identity --query Account --output text)
echo '{"receipt_id":"r1","items":[{"name":"tea","qty":2,"price":1.25}]}' > r1.json
aws s3 cp r1.json s3://$B/incoming/r1.json && sleep 20 && aws s3 cp s3://$B/processed/r1.json -
python3 tools/check_build.py --id <id>
```

**Known gotchas (not a trick)**
- The function must exist, and S3 must be allowed to invoke it (`aws_lambda_permission`), before the bucket notification can be created. Use `depends_on`.
- Lambda needs the image to exist first. `-target` the ECR repository, push the image, then run the full apply.
- Match `--platform` to `architectures`. With BuildKit, add `--provenance=false`.

---

## Part B - Break: review `crack-files/` (40 points)
`crack-files/` is a pull request, "vendor OCR integration". It has **at least 6** real security problems across secrets, network exposure, IAM, container hardening, the CI pipeline, and application code. Fix each one **in place**, keeping the file meaningful, and document it in `FINDINGS.md`.

## Part C - Operate (10 points)
Submit on time. Keep keys and state out of the zip. Keep the default tags on every resource. Answer the questions in `FINDINGS.md`.

## Submit
```bash
python3 tools/submit.py --id <id>
```
Do **not** run `terraform destroy`.
