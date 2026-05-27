# Week 8: On-Premise Docker vs Cloud Run Comparison

## Comparison Table

| Dimension | On-Premise Docker (Wks 3-5) | Cloud Run (Week 8) |
|-----------|----------------------------|-------------------|
| Infrastructure setup | 3 VMs created, Docker installed on each | No VMs — GCP manages all infrastructure automatically |
| Deployment command | SSH → docker build → docker run | gcloud builds submit → terraform apply |
| TLS / HTTPS | Not configured — HTTP only | Automatic HTTPS with .run.app domain |
| Scaling approach | Manual — redeploy or add VMs | Automatic — scales 0 to 3 instances based on traffic |
| Port management | Ports 5000/5001/5002 per environment | No port management needed |
| Cost when idle | VM running 24/7 regardless of traffic | Scales to zero — no cost when no requests |
| Rollback | Re-deploy previous image manually | Deploy previous SHA tag — immutable revisions |
| Secrets management | GitHub Secrets → env vars in workflow | OIDC — no long-lived credentials |

## Reflection Questions

**Q1: Which approach required more manual steps?**
The on-premise Docker approach required significantly more manual steps. Cloud Run eliminated the need to SSH into machines, manually run docker build and docker run commands, manage port assignments per environment, and restart containers after updates. A single gcloud run deploy command replaced all of those steps combined.

**Q2: How do you know which version of code is running?**
With on-premise Docker, there was no reliable way to verify which exact code version was running without SSHing into the VM and inspecting the container. With Cloud Run and commit SHA tagging, every deployed image is tagged with the exact 7-character git commit hash, making it possible to trace any running service back to a specific line of code using git log at any time.

**Q3: What is the security advantage of scale-to-zero beyond cost savings?**
When an instance is not running, it cannot be attacked. Scale-to-zero reduces the attack surface by eliminating idle processes that could be exploited through open ports, unpatched vulnerabilities, or lingering credentials. A VM running 24/7 is continuously exposed to network scanning and brute force attempts even when serving no legitimate traffic.

**Q4: What attack surface was eliminated by replacing SSH keys with OIDC?**
SSH key secrets stored in GitHub could be stolen if the repository or a developer machine were compromised. A stolen key would give an attacker persistent access to the VMs. OIDC eliminates this by issuing short-lived tokens that expire after each workflow run — there is no permanent credential to steal, store, or rotate.
