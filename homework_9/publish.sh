#!/bin/bash
set -euo pipefail

# 本地已有镜像名,这就是第9课作业的镜像
LOCAL_IMAGE="mlzoomcamp-2026-serverless:latest"

AWS_REGION="ap-southeast-1"

# ECR 仓库名（可以和你本地镜像名不同，这里沿用你原来的命名习惯）
ECR_REPO_NAME="homework09_straight"

# 获取 AWS 账号 ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")

# 远程 tag：commit + 时间戳，保证唯一、方便回滚
REMOTE_TAG="$(git rev-parse --short HEAD)-$(date +"%Y%m%d-%H%M%S")"

ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${ECR_URI}/${ECR_REPO_NAME}:${REMOTE_TAG}"

echo "本地镜像: ${LOCAL_IMAGE}"
echo "远程镜像: ${IMAGE_URI}"

# 登录 ECR
aws ecr get-login-password --region ${AWS_REGION} \
| docker login --username AWS --password-stdin ${ECR_URI}

# 给本地已有镜像打远程 tag，然后推送
docker tag ${LOCAL_IMAGE} ${IMAGE_URI}
docker push ${IMAGE_URI}

