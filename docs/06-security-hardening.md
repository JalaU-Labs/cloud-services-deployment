# Security Hardening

This document consolidates the security practices applied throughout the lab.
It serves as a checklist and reference for future projects.

## 1. Principle of Least Privilege

Every component should have only the permissions required for its function.

### AWS

- Use a dedicated Security Group per workload, not the VPC `default`.
- Restrict inbound SSH to a single IP, not a subnet or `0.0.0.0/0`.
- Restrict API ports to a single IP whenever possible.
- If the instance needs to call AWS APIs, attach an IAM role with the minimum
  policy required instead of storing access keys on disk.
- Prefer SSM Session Manager over SSH when possible. It removes the need for
  inbound port 22 entirely.

### MongoDB Atlas

- Create one database user per application or developer. Never share.
- Scope the database user to the specific database it needs in production.
- Restrict Network Access to specific IPs.
- Use temporary IP entries that expire automatically.
- Enable two-factor authentication on the Atlas account itself.

### Docker

- Run containers as a non-root user (`USER app` in the Dockerfile).
- Use multi-stage builds to keep the runtime image small.
- Pin base image versions with a digest when possible.
- Do not mount the Docker socket into application containers.
- Do not run with `--privileged`.

## 2. Secrets Management

### What is a secret

Any value that grants access to a resource: database passwords, API keys, SSH
private keys, TLS certificates, connection strings with credentials.

### What is not a secret

Public identifiers, hostnames, port numbers without credentials, public keys,
version strings.

### Rules

1. Never commit a secret to Git. Ever. Even in a private repository.
2. If a secret is committed by accident, rotate it immediately. Removing it
   from a later commit is not sufficient: the history preserves it.
3. Use `.env` files for local development. They are git-ignored.
4. Use the CI/CD secret stores for pipelines (GitLab CI/CD variables, GitHub
   Actions secrets).
5. Use a secret manager for production (AWS Secrets Manager, HashiCorp Vault,
   Doppler).
6. Set strict file permissions on secret files: `chmod 600 .env`.
7. Do not echo secrets in logs. Configure your framework to redact them.

### Environment variable hygiene

- Do not use the same variable name for different purposes across environments.
- Do not mix public and secret variables in the same file if it is not
  necessary.
- Document every variable in `.env.example` with a comment.

## 3. Network Security

### EC2 Security Group rules

Inbound:

- SSH (22): `<your-ip>/32` only.
- API port (8000): `<your-ip>/32` only.

Outbound:

- DNS (53): `0.0.0.0/0` needed for resolution.
- HTTPS (443): `0.0.0.0/0` needed for package managers and Atlas.
- HTTP (80): `0.0.0.0/0` only if strictly required.

Remove any rule that is not used. Review the rules monthly.

### Local machine

- Bind published Docker ports to `127.0.0.1`, not `0.0.0.0`, unless you
  explicitly need to expose the service on the local network.
- Use a firewall (ufw, firewalld, or nftables) and only open what is needed.
- Keep the SSH client updated.

## 4. SSH Hardening

On the EC2 instance, edit
`/etc/ssh/sshd_config.d/99-hardening.conf`:

```
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

Restart:

```bash
sudo systemctl restart sshd
```

Verify that key-based authentication still works before closing the session.

## 5. Application Security

- Validate every input with Pydantic or an equivalent library.
- Reject malformed emails, empty names, and unexpected fields.
- Do not return stack traces to clients. FastAPI already hides them when
  `debug=False`.
- Log requests but never log the body of authenticated endpoints.
- Version the API (`/v1/...`) when it is consumed by external clients.
- Add rate limiting before exposing any endpoint publicly.

## 6. Container Security

- Use multi-stage builds.
- Do not run as root.
- Do not store secrets in the image.
- Scan the image for vulnerabilities with `trivy` or `docker scout`:

  ```bash
  trivy image lab-cloud-api:latest
  ```

- Keep the base image updated. Rebuild weekly.
- Sign the image if it will be distributed (cosign or Docker Content Trust).

## 7. Cost and Abuse Protection

- Set a zero-dollar AWS Budget alert.
- Monitor the Billing Dashboard weekly.
- Terminate the EC2 instance at the end of the lab.
- Remove unused Atlas clusters or downgrade to the free tier.
- Rotate database passwords every 90 days.

## 8. Incident Response Checklist

If a secret is leaked:

1. Rotate the secret immediately in the provider console.
2. Revoke access tokens and SSH keys.
3. Audit access logs for unauthorized use.
4. Remove the secret from the repository history with `git filter-repo` or
   BFG Repo-Cleaner.
5. Force-push the cleaned history and notify collaborators.
6. Document the incident and the remediation steps.

If the instance is compromised:

1. Stop the instance.
2. Take a snapshot for forensic analysis.
3. Terminate the instance and create a new one from a clean AMI.
4. Audit the Security Group rules and the IAM role.
5. Rotate every credential stored on the instance.