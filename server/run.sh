#!/bin/bash

# ---------------------------
# FastAPI 异步服务启动脚本
# ---------------------------

APP_MODULE="app.main:app"
HOST="0.0.0.0"
PORT=8000
WORKERS=4   # 生产环境可调

# 1. 判断运行模式
MODE=$1   # 可传入 "dev" 或 "prod"

if [ "$MODE" == "dev" ]; then
    echo "Starting FastAPI in development mode..."
    uvicorn $APP_MODULE --reload --host $HOST --port $PORT
else
    echo "Starting FastAPI in production mode..."
    uvicorn $APP_MODULE --host $HOST --port $PORT --workers $WORKERS
fi
