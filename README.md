# Advance Log Detector

A small monitoring stack I built to learn how logs, metrics and alerts fit together. A Python service reads a log file, works out the share of error lines, flags a spike, and exposes it as Prometheus metrics. Prometheus fires alerts, Alertmanager routes them to a webhook, and Grafana draws it all on a dashboard. Everything runs with Docker Compose.

---

## Why I built this

I wanted to see the full alerting path work end to end: a log line goes bad, a metric moves, an alert fires, a message lands somewhere. The detection logic is deliberately simple; the goal was the DevOps plumbing around it.

---

## How it works

1. `detector.py` reads the log file and parses lines with regular expressions.
2. It tracks the share of error lines in the current window.
3. If the error rate goes above a threshold, it counts an anomaly.
4. It exposes metrics on `:8000/metrics` using `prometheus_client`.
5. Prometheus scrapes it and evaluates `alert_rules.yml`.
6. Firing alerts go to Alertmanager, which posts to a webhook receiver.
7. Grafana loads its datasource and dashboard from files.

```mermaid
flowchart TD
    A[Log file] --> B[detector.py]
    B -->|:8000/metrics| C[Prometheus]
    C --> D[Grafana]
    C -->|alert rules| E[Alertmanager]
    E --> F[Webhook receiver]
```

---

## Tech stack

| Tool | Role |
| --- | --- |
| Python 3.11, prometheus-client | Detection and metrics |
| Prometheus 2.47, Alertmanager 0.26 | Scraping, alert rules, routing |
| Grafana 10.1 | Dashboard provisioned from files |
| Docker Compose | Runs all five services |
| GitHub Actions, pytest, flake8 | CI, tests, lint |
| Terraform, AWS (EC2, VPC, IAM, SSM, S3) | Optional cloud deployment, Checkov scan in CI |

---

## Getting started

```bash
git clone git@github.com:Danishwani1999/Advance_Log_Detector.git
cd Advance_Log_Detector
cp .env.example .env      # then set your own values
docker compose up -d --build
docker compose ps
```

| Service | Port |
| --- | --- |
| detector (metrics) | 8000 |
| Prometheus | 9090 |
| Alertmanager | 9093 |
| Grafana | 3000 |

Grafana login: user and password come from `GRAFANA_ADMIN_USER` and `GRAFANA_ADMIN_PASSWORD` in your `.env`. Compose refuses to start without a password.

| Variable | Default | Meaning |
| --- | --- | --- |
| `LOG_FILE_PATH` | `/data/sample_system.log` | Log file to read |
| `ERROR_THRESHOLD` | `0.3` | Error rate that counts as a spike |
| `READ_FROM_START` | `true` | Read from the beginning |
| `WINDOW_SIZE` | `20` | Number of most recent lines per window |
| `MIN_SAMPLES` | `5` | Minimum lines before a window is judged |

---

## What it looks like when it runs

Real output from my machine, captured right after `docker compose up`.

### Containers

```text
SERVICE         IMAGE                           STATUS
alert-webhook   mendhak/http-https-echo:31      Up 31 minutes
alertmanager    prom/alertmanager:v0.26.0       Up 31 minutes
detector        advance_log_detector-detector   Up 26 seconds (healthy)
grafana         grafana/grafana:10.1.0          Up 31 minutes
prometheus      prom/prometheus:v2.47.0         Up 31 minutes
```

### Detector metrics

```text
# HELP logs_processed_total Total raw log lines processed from system file
# TYPE logs_processed_total counter
logs_processed_total 50.0
# HELP anomalies_detected_total Total error-rate anomalies flagged by the detector
# TYPE anomalies_detected_total counter
anomalies_detected_total 1.0
# HELP log_error_rate Proportion of error logs in the last processing window (0.0 - 1.0)
# TYPE log_error_rate gauge
log_error_rate 0.95
```

### Prometheus targets

```text
log_detector_service http://detector:8000/metrics up
```

### Alert rules loaded

```text
HighLogErrorRate - firing
LogDetectorDown - inactive
```

---

## Screenshots

### Grafana dashboard showing the detected anomaly

![Grafana dashboard showing the detected anomaly](docs/grafana-anomaly.png)

### Prometheus alert firing

![Prometheus alert firing](docs/prometheus-alert.png)

### Alertmanager receiving the alert

![Alertmanager receiving the alert](docs/alertmanager.png)

### Webhook receiving the alert

![Webhook receiving the alert](docs/webhook-log.png)

---

## Try it yourself

```bash
for i in 1 2 3 4 5; do echo "2026-10-19 12:00:0$i ERROR Disk failure detected" >> data/sample_system.log; done
curl -s localhost:8000/metrics | grep -E "^(log_error_rate|anomalies_detected_total)"
docker compose logs -f alert-webhook
pip install -r requirements.txt && pytest && flake8
```

Then open `http://localhost:9090/alerts` to watch the alert fire.

---

## Deploy to AWS with Terraform

The same stack can run on a single EC2 instance, created and destroyed with Terraform (`terraform/`).

**Runtime architecture**

```mermaid
flowchart TB
    user["You (browser)<br/>allowed only from your /32"]
    admin["Admin shell via<br/>SSM Session Manager<br/>(no SSH key)"]

    subgraph aws["AWS account, ap-south-1"]
        subgraph vpc["VPC 10.20.0.0/16"]
            igw["Internet gateway"]
            subgraph ec2["EC2 t3.small in public subnet<br/>IMDSv2, encrypted disk, Elastic IP"]
                direction LR
                det["detector<br/>exporter"] -->|metrics| prom["Prometheus<br/>+ alert rules"]
                prom --> graf["Grafana :3000"]
                prom -->|alerts| am["Alertmanager"] --> wh["alert-webhook"]
            end
        end
        ssm[("SSM Parameter Store<br/>Grafana password")]
    end

    user -->|"HTTP 3000<br/>(security group)"| igw --> graf
    admin -.-> ec2
    ec2 -.->|"IAM role reads<br/>one parameter at boot"| ssm
```

**Delivery flow**

```mermaid
flowchart LR
    pr["Pull request"] --> ci["GitHub Actions"]
    ci --> v["validate job<br/>compose, promtool,<br/>flake8, pytest"]
    ci --> t["terraform job<br/>fmt, validate, Checkov"]
    t -->|merge to main| tf["terraform plan / apply<br/>(run locally)"]
    tf --> aws["AWS resources"]
    tf -.->|remote state| s3[("S3 bucket<br/>versioned, encrypted,<br/>native lock")]
```

| Piece | What it does |
|---|---|
| VPC, public subnet, internet gateway | Own network, default security group emptied |
| Security group | Grafana (3000) open to one `/32` only, outbound limited to 443 |
| EC2 (Amazon Linux 2023) | IMDSv2 only, encrypted gp3 root volume, no SSH key, access through SSM Session Manager |
| IAM role | Read access to one SSM parameter and SSM core only |
| SSM SecureString | Grafana admin password generated by Terraform, never in the repo |
| S3 backend | Remote state with versioning, encryption and native locking (`use_lockfile`) |
| `user_data` | Installs Docker, Compose and buildx, each downloaded with a pinned SHA-256, then starts the stack |

```bash
cd terraform
cp backend.hcl.example backend.hcl        # your S3 state bucket
cp terraform.tfvars.example terraform.tfvars   # allowed_cidr = <your public IP>/32
terraform init -backend-config=backend.hcl
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy                         # when finished, to stop charges
```

Applied and destroyed in my own AWS account (17 resources). Grafana showed live metrics and the `HighLogErrorRate` alert firing.

![Grafana dashboard running on EC2](docs/aws-grafana-dashboard.png)

![Prometheus alert rules shown in Grafana](docs/aws-grafana-alerts.png)

CI runs `terraform fmt`, `validate` and a Checkov scan on every push. Known limits: Grafana is served over plain HTTP (a real setup would use an HTTPS load balancer), and one instance is not highly available.

## Things that went wrong (and the fixes)

* **Target DOWN.** Prometheus must scrape the Compose service name (`detector:8000`). My README and compose file once disagreed, so the output above is captured from the running stack.
* **Grafana empty.** Provisioning needed a single datasource and a proper dashboard provider.
* **Port in use.** `sudo lsof -i :9090`, then stop whatever holds it.
* **Grafana refused connections on AWS.** The EC2 console output showed `compose build requires buildx 0.17 or later`: the buildx that ships with Amazon Linux 2023 is too old for `docker compose --build`. I added a pinned buildx plugin (SHA-256 checked) to `user_data` and `terraform apply` replaced the instance.

---

## What I learned

* Non-root containers with healthchecks
* How scrape jobs, alert rules and Alertmanager routes connect
* Provisioning Grafana as code
* Keeping secrets in `.env` and committing only `.env.example`
* Adding lint and tests to CI
* Keeping docs in sync with the code

---

## Next steps

* Multiple log files and formats
* A statistical detector instead of a fixed threshold
* Slack or email alerts
* Run it on Kubernetes (the AWS EC2 deployment with Terraform is done, see above)

---

## Author

**Danish Ahmad Wani** · https://github.com/Danishwani1999

## License

MIT. See [LICENSE](LICENSE).
