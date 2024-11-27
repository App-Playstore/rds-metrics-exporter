# RDS Metrics Exporter

## Overview

This Python-based exporter collects and exposes metrics related to AWS RDS instances. It's designed for seamless integration with Prometheus.

## Metrics Exported

| Metric Name         | Description                           |
|---------------------|---------------------------------------|
| `rds_engine_version` | Engine version of the RDS instance   |

## Docker Image

The exporter is packaged as a Docker image:  
**`ogechibogu/rds-metrics-exporter`**

## Usage

### Set Environment Variables:
```bash
export AWS_ACCESS_KEY_ID=<your_access_key_id>
export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>   
export REGION=<your_region> 

