#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import argparse
import socket
import logging
from logging.handlers import RotatingFileHandler

# ---------- 基础路径 ----------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAIN_APP = os.path.join(BASE_DIR, "倒计时.exe")
LOG_FILE = os.path.join(BASE_DIR, "zlog.txt")

# ---------- 日志配置 ----------
logger = logging.getLogger("AutoStart")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(level, msg):
    """简易日志封装"""
    if level == 1:
        logger.error(msg)
    elif level == 2:
        logger.info(msg)
    elif level == 3:
        logger.debug(msg)
    else:
        logger.info(msg)


# ---------- 核心功能函数 ----------
def is_app_running(exe_name):
    """检测指定的 exe 是否正在运行"""
    if sys.platform == "win32":
        try:
            # 使用 tasklist 查找进程
            output = subprocess.check_output(
                f'tasklist /FI "IMAGENAME eq {exe_name}"',
                shell=True, text=True, stderr=subprocess.DEVNULL
            )
            return exe_name.lower() in output.lower()
        except Exception as e:
            log(1, f"进程检测失败: {e}")
            return False
    return False


def get_target_app():
    """智能获取主程序路径"""
    if os.path.exists(MAIN_APP):
        return MAIN_APP

    log(2, f"未找到默认主程序 {MAIN_APP}，尝试寻找其他 exe...")
    exe_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith('.exe') and f != os.path.basename(__file__)]
    if exe_files:
        # 找到体积最大的 exe，大概率是打包后的主程序
        target = os.path.join(BASE_DIR, max(exe_files, key=lambda x: os.path.getsize(os.path.join(BASE_DIR, x))))
        log(2, f"找到替代主程序: {target}")
        return target
    return None


def wait_for_system_ready(delay=30, wait_network=False, network_target="8.8.8.8", network_timeout=5):
    """等待系统环境就绪"""
    log(2, f"开始等待系统准备就绪，基础延迟 {delay} 秒，等待网络: {wait_network}")

    if delay > 0:
        log(2, f"等待 {delay} 秒基础延迟...")
        time.sleep(delay)

    if wait_network:
        log(2, f"检测网络连通性（目标: {network_target}）...")
        start = time.time()
        while time.time() - start < 60:  # 最多等待 60 秒
            try:
                socket.gethostbyname(network_target)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(network_timeout)
                result = sock.connect_ex((network_target, 80))
                sock.close()
                if result == 0:
                    log(2, "网络已连通")
                    break
            except Exception:
                pass
            log(3, "网络尚未就绪，等待 2 秒后重试...")
            time.sleep(2)
        else:
            log(1, "等待网络超时，忽略网络状态继续执行")

    if sys.platform == "win32":
        log(2, "检查桌面进程 explorer.exe...")
        for _ in range(10):  # 最多等待 20秒
            if is_app_running("explorer.exe"):
                log(2, "桌面进程已存在")
                break
            time.sleep(2)
        else:
            log(1, "未检测到 explorer.exe，可能系统尚未完全登录，忽略并继续")

    log(2, "系统就绪检测流程结束")


# ---------- 主函数 ----------
def main():
    parser = argparse.ArgumentParser(description="倒计时自启动辅助程序")
    parser.add_argument("--delay", type=int, default=30, help="启动前的基础延迟时间（秒）")
    parser.add_argument("--wait-network", action="store_true", help="等待网络连通后再启动")
    parser.add_argument("--network-target", type=str, default="8.8.8.8", help="网络连通测试目标")
    parser.add_argument("--now", action="store_true", help="立即启动，忽略所有等待条件")
    args = parser.parse_args()

    log(2, "=== 自启动程序开始运行 ===")

    target_app = get_target_app()
    if not target_app:
        log(1, "致命错误：当前目录下未找到任何可用的主程序 exe！自启动终止。")
        sys.exit(1)

    exe_name = os.path.basename(target_app)

    if args.now:
        log(2, "立即启动模式，跳过环境等待")
    else:
        wait_for_system_ready(delay=args.delay, wait_network=args.wait_network, network_target=args.network_target)

    # 核心逻辑：持续检测与拉起，直到确认主程序存活
    max_wait_time = 300  # 最长持续尝试 5 分钟 (300秒)
    start_time = time.time()

    log(2, f"开始守护启动流程，目标程序: {exe_name}")

    while time.time() - start_time < max_wait_time:
        # 1. 检查是否已经运行
        if is_app_running(exe_name):
            log(2, f"🎉 成功检测到主程序 [{exe_name}] 正在运行！自启动任务圆满完成。")
            break

        # 2. 如果没运行，尝试拉起
        log(2, f"尝试拉起主程序...")
        try:
            startupinfo = None
            creationflags = 0
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                    creationflags = subprocess.CREATE_NO_WINDOW

            subprocess.Popen([target_app], startupinfo=startupinfo, creationflags=creationflags, close_fds=True)
            log(2, "启动指令已发送，等待系统分配进程...")
        except Exception as e:
            log(1, f"发送启动指令失败: {e}")

        time.sleep(5)
    else:
        log(1, f"❌ 超过最大重试时间 ({max_wait_time}秒)，未能确认主程序启动成功，自启动程序退出。")

    log(2, "=== 自启动程序安全退出 ===")


if __name__ == "__main__":
    main()