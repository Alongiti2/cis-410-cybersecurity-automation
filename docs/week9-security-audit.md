# Week 9 Security Audit

## Before/After IAM Table

| Role | Before | After |
|------|--------|-------|
| roles/run.admin | ✅ Present | ❌ Removed |
| roles/run.developer | ❌ Absent | ✅ Added |
| roles/storage.admin (project) | ✅ Present | ❌ Removed |
| roles/storage.admin (bucket) | ❌ Absent | ✅ Added to tfstate only |

## Reflection Questions

**1. Why is roles/run.admin excessive for a deployment service account?**
roles/run.admin grants full administrative control over all Cloud Run services including the ability to delete services and modify IAM policies. A deployment service account only needs to deploy new revisions, so roles/run.developer is sufficient and follows the principle of least privilege.

**2. Why should storage.admin be scoped to the tfstate bucket only?**
Project-level storage.admin grants read and write access to every storage bucket in the project including any sensitive data buckets. Scoping it to only the tfstate bucket limits the blast radius if the service account is compromised.

**3. Why is Secret Manager better than GitHub Secrets for runtime credentials?**
GitHub Secrets are injected as environment variables during CI/CD pipeline execution and can be exposed in logs or by malicious workflow steps. Secret Manager stores credentials encrypted at rest and grants access only at runtime to authorized service accounts using IAM, reducing the risk of credential exposure.
