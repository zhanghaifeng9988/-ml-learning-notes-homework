#!/bin/bash
# 构建 Docker 镜像 → 推送到 ECR → 更新 Lambda 函数代码

IMAGE_NAME="clothing-prediction-lambda"
AWS_REGION="ap-southeast-1"

#  调用 AWS STS 获取当前身份信息，用 jq 提取出 AWS 账号 ID，存入变量。
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")

# Get latest commit SHA and current datetime
# 好处：每次构建的镜像的tag 都不同，便于区分版本，不会互相覆盖。
COMMIT_SHA=$(git rev-parse --short HEAD)
DATETIME=$(date +"%Y%m%d-%H%M%S")
IMAGE_TAG="${COMMIT_SHA}-${DATETIME}"

# ECR 仓库地址前缀,完整镜像地址
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${ECR_URI}/${IMAGE_NAME}:${IMAGE_TAG}"

# aws ecr get-login-password  →  先向 AWS 拿到临时密码
#        ↓ 管道
# docker login  →  用 AWS 作为用户名，临时密码作为密码，登录 ECR 
# 之后你本地的 Docker 就有权限向这个 ECR 仓库推送镜像了。
aws ecr get-login-password \
  --region ${AWS_REGION} \
| docker login \
  --username AWS \
  --password-stdin ${ECR_URI}

# docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
# # 构建时强制使用 amd64 架构，并禁用 provenance 证明,防止 把镜像包装成了一个包含多架构信息的索引，Lambda 不支持这种多架构镜像
docker build --platform linux/amd64 --provenance=false -t clothing-prediction-lambda:${IMAGE_TAG} .
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_URI}
docker push ${IMAGE_URI}

# 更新 Lambda 函数的代码：
#aws lambda update-function-code \
#  --function-name churn-prediction-docker \
#  --image-uri ${IMAGE_URI} \
#  --region ${AWS_REGION}