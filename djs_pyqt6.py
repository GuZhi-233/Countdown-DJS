# MIT License
#
# Copyright (c) 2026 苗睿轩
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import calendar
import ctypes
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import random
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta
from enum import IntFlag, auto


import qtawesome as qta
import chinese_calendar
import getpass
import requests
from PyQt6.QtCore import (Qt, QTimer, QThread, pyqtSignal, QObject, QPoint, QRect,
                          QPropertyAnimation, QEasingCurve, QRectF, QPointF, QByteArray,
                          pyqtProperty, QSize, QEvent, QDate, qVersion, PYQT_VERSION_STR)
from PyQt6.QtGui import (QColor, QFont, QPainter, QPainterPath, QPixmap, QImage,
                         QIcon, QAction, QPen, QBrush, QPalette, QLinearGradient,
                         QFontDatabase, QMovie, QFontMetrics, QTextLayout, QTextOption, QTextCursor,
                         QCursor, QTextCharFormat)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect,
                             QSystemTrayIcon, QMenu, QMessageBox, QFileDialog,
                             QColorDialog, QInputDialog, QScrollArea,
                             QDialog, QLineEdit, QCheckBox, QComboBox, QSpinBox,
                             QSlider, QTreeWidget, QTreeWidgetItem, QTabWidget,
                             QGroupBox, QPlainTextEdit,
                             QListWidget, QListWidgetItem, QFormLayout,
                             QDoubleSpinBox, QGraphicsOpacityEffect, QSizeGrip,
                             QProgressBar, QSizePolicy, QTextEdit,
                             QFrame, QStackedWidget, QSplitter, QCalendarWidget)


PROVINCE_CITY_DATA = {
    "北京": ["北京市"],
    "天津": ["天津市"],
    "河北": ["石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市", "衡水市"],
    "山西": ["太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市", "吕梁市"],
    "内蒙古": ["呼和浩特市", "包头市", "乌海市", "赤峰市", "通辽市", "鄂尔多斯市", "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市"],
    "辽宁": ["沈阳市", "大连市", "鞍山市", "抚顺市", "本溪市", "丹东市", "锦州市", "营口市", "阜新市", "辽阳市", "盘锦市", "铁岭市", "朝阳市", "葫芦岛市"],
    "吉林": ["长春市", "吉林市", "四平市", "辽源市", "通化市", "白山市", "松原市", "白城市", "延边朝鲜族自治州"],
    "黑龙江": ["哈尔滨市", "齐齐哈尔市", "鸡西市", "鹤岗市", "双鸭山市", "大庆市", "伊春市", "佳木斯市", "七台河市", "牡丹江市", "黑河市", "绥化市"],
    "上海": ["上海市"],
    "江苏": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市", "宿迁市"],
    "浙江": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"],
    "安徽": ["合肥市", "芜湖市", "蚌埠市", "淮南市", "马鞍山市", "淮北市", "铜陵市", "安庆市", "黄山市", "滁州市", "阜阳市", "宿州市", "六安市", "亳州市", "池州市", "宣城市"],
    "福建": ["福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市", "南平市", "龙岩市", "宁德市"],
    "江西": ["南昌市", "景德镇市", "萍乡市", "九江市", "新余市", "鹰潭市", "赣州市", "吉安市", "宜春市", "抚州市", "上饶市"],
    "山东": ["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "临沂市", "德州市", "聊城市", "滨州市", "菏泽市"],
    "河南": ["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市"],
    "湖北": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市", "恩施土家族苗族自治州"],
    "湖南": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市", "娄底市", "湘西土家族苗族自治州"],
    "广东": ["广州市", "韶关市", "深圳市", "珠海市", "汕头市", "佛山市", "江门市", "湛江市", "茂名市", "肇庆市", "惠州市", "梅州市", "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市", "潮州市", "揭阳市", "云浮市"],
    "广西": ["南宁市", "柳州市", "桂林市", "梧州市", "北海市", "防城港市", "钦州市", "贵港市", "玉林市", "百色市", "贺州市", "河池市", "来宾市", "崇左市"],
    "海南": ["海口市", "三亚市", "三沙市", "儋州市"],
    "重庆": ["重庆市"],
    "四川": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市", "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市", "阿坝藏族羌族自治州", "甘孜藏族自治州", "凉山彝族自治州"],
    "贵州": ["贵阳市", "六盘水市", "遵义市", "安顺市", "毕节市", "铜仁市", "黔西南布依族苗族自治州", "黔东南苗族侗族自治州", "黔南布依族苗族自治州"],
    "云南": ["昆明市", "曲靖市", "玉溪市", "保山市", "昭通市", "丽江市", "普洱市", "临沧市", "楚雄彝族自治州", "红河哈尼族彝族自治州", "文山壮族苗族自治州", "西双版纳傣族自治州", "大理白族自治州", "德宏傣族景颇族自治州", "怒江傈僳族自治州", "迪庆藏族自治州"],
    "西藏": ["拉萨市", "日喀则市", "昌都市", "林芝市", "山南市", "那曲市", "阿里地区"],
    "陕西": ["西安市", "铜川市", "宝鸡市", "咸阳市", "渭南市", "延安市", "汉中市", "榆林市", "安康市", "商洛市"],
    "甘肃": ["兰州市", "嘉峪关市", "金昌市", "白银市", "天水市", "武威市", "张掖市", "平凉市", "酒泉市", "庆阳市", "定西市", "陇南市", "临夏回族自治州", "甘南藏族自治州"],
    "青海": ["西宁市", "海东市", "海北藏族自治州", "黄南藏族自治州", "海南藏族自治州", "果洛藏族自治州", "玉树藏族自治州", "海西蒙古族藏族自治州"],
    "宁夏": ["银川市", "石嘴山市", "吴忠市", "固原市", "中卫市"],
    "新疆": ["乌鲁木齐市", "克拉玛依市", "吐鲁番市", "哈密市", "昌吉回族自治州", "博尔塔拉蒙古自治州", "巴音郭楞蒙古自治州", "阿克苏地区", "克孜勒苏柯尔克孜自治州", "喀什地区", "和田地区", "伊犁哈萨克自治州", "塔城地区", "阿勒泰地区"],
    "香港": ["香港"],
    "澳门": ["澳门"],
    "台湾": ["台北市", "新北市", "桃园市", "台中市", "台南市", "高雄市", "基隆市", "新竹市", "嘉义市"]
}

_system_dark_cache = None
_system_dark_cache_time = 0

def is_system_dark():
    global _system_dark_cache, _system_dark_cache_time
    now = time.time()
    if _system_dark_cache is not None and now - _system_dark_cache_time < 2:
        return _system_dark_cache
    result = False
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            result = value == 0
        except Exception:
            result = False
    elif sys.platform == "darwin":
        try:
            p = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True, timeout=2
            )
            result = "Dark" in p.stdout
        except Exception:
            result = False
    else:
        try:
            p = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True, text=True, timeout=2
            )
            result = "dark" in p.stdout.lower()
        except Exception:
            result = False
    _system_dark_cache = result
    _system_dark_cache_time = now
    return result

def get_system_theme():
    dark = is_system_dark()
    if dark:
        return Theme("system_dark", is_dark=True,
                     bg_color="#1e1e2e", frame_bg="#2a2a3a",
                     accent_color="#89b4fa", text_color="#cdd6f4",
                     border_color="#45475a", font_family="Microsoft YaHei",
                     font_size=9, window_round_radius=12)
    else:
        return Theme("system_light", is_dark=False,
                     bg_color="#f5f5f5", frame_bg="#ffffff",
                     accent_color="#3498db", text_color="#2c3e50",
                     border_color="#d1d8e0", font_family="Microsoft YaHei",
                     font_size=9, window_round_radius=12)

def get_theme_qss(t):
    c = get_theme_colors(t)

    return f"""
    QDialog {{
        background-color: {c['dark_bg']}; color: {c['text_color']};
        font-family: 'Microsoft YaHei', 'Segoe UI'; font-size: 10pt;
    }}
    QWidget {{
        color: {c['text_color']}; font-family: 'Microsoft YaHei', 'Segoe UI';
    }}
    QGroupBox {{
        font-weight: bold; color: {c['accent']};
        border: 1px solid {c['border_color']}; border-radius: 6px;
        margin-top: 10px; padding-top: 10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin; left: 10px; padding: 0 5px;
        color: {c['accent']};
    }}
    QPushButton {{
        background-color: {c['accent']}; color: {c['btn_text']};
        border-radius: 4px; padding: 6px 12px; border: none; font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {c['hover_accent']}; color: {c['hover_btn_text']};
    }}
    QPushButton[primary="true"] {{
        background-color: {c['accent']}; color: {c['btn_text']};
    }}
    QPushButton[primary="true"]:hover {{
        background-color: {c['hover_accent']}; color: {c['hover_btn_text']};
    }}
    QPushButton[secondary="true"] {{
        background: transparent; color: {c['text_color']};
        border: 1px solid {c['border_color']};
    }}
    QPushButton[secondary="true"]:hover {{
        border-color: {c['accent']}; color: {c['accent']};
    }}
    QPushButton[danger="true"] {{
        background-color: {c['danger']}; color: #FFFFFF;
    }}
    QPushButton[danger="true"]:hover {{
        background-color: #c0392b; color: #FFFFFF;
    }}
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {c['input_bg']}; border: 1px solid {c['border_color']};
        border-radius: 3px; padding: 4px 6px; color: {c['text_color']};
        selection-background-color: {c['accent']};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 1px solid {c['accent']};
    }}
    QComboBox QAbstractItemView {{
        background-color: {c['panel_bg']}; color: {c['text_color']};
        selection-background-color: {c['accent']};
    }}
    QListWidget {{
        background-color: {c['panel_bg']}; color: {c['text_color']};
        border: 1px solid {c['border_color']}; border-radius: 4px; outline: none;
    }}
    QListWidget::item {{
        padding: 5px 8px; border-radius: 3px; margin: 2px 4px;
    }}
    QListWidget::item:hover {{
        background-color: {c['input_bg']}; color: {c['text_color']};
    }}
    QListWidget::item:selected {{
        background-color: {c['accent']}; color: {c['selected_text']};
    }}
    QScrollArea {{ border: none; background: transparent; }}
    QScrollBar:vertical {{
        background: {c['panel_bg']}; width: 8px; margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {c['border_color']}; border-radius: 4px; min-height: 30px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QSlider::groove:horizontal {{
        border-radius: 2px; height: 4px; background: {c['border_color']};
    }}
    QSlider::handle:horizontal {{
        background: {c['accent']}; width: 12px; height: 12px;
        margin: -4px 0; border-radius: 6px;
    }}
    QCheckBox {{ color: {c['text_color']}; spacing: 6px; }}
    QCheckBox::indicator {{
        width: 16px; height: 16px; border-radius: 3px;
        border: 2px solid {c['border_color']}; background: transparent;
    }}
    QCheckBox::indicator:checked {{
        background-color: {c['accent']}; border-color: {c['accent']};
    }}
    QLabel {{ color: {c['text_color']}; }}
    QToolTip {{
        background-color: {c['panel_bg']}; color: {c['text_color']};
        border: 1px solid {c['border_color']}; padding: 4px; border-radius: 4px;
    }}
    """
def apply_modern_window_effect(hwnd, effect_type="acrylic", is_dark=False, enable=True):
    if sys.platform != "win32":
        return False
    try:
        from ctypes import windll, c_int, byref, sizeof
        dwmapi = windll.dwmapi
        if not enable:
            backdrop_value = c_int(1)
            dwmapi.DwmSetWindowAttribute(hwnd, 38, byref(backdrop_value), sizeof(backdrop_value))
            margins = (c_int * 4)(0, 0, 0, 0)
            dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))
            return True
        dark_value = c_int(1 if is_dark else 0)
        dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(dark_value), sizeof(dark_value))
        backdrop_type = 3 if effect_type == "acrylic" else (2 if effect_type == "mica" else 4)
        backdrop_value = c_int(backdrop_type)
        dwmapi.DwmSetWindowAttribute(hwnd, 38, byref(backdrop_value), sizeof(backdrop_value))
        corner_pref = c_int(2)
        dwmapi.DwmSetWindowAttribute(hwnd, 33, byref(corner_pref), sizeof(corner_pref))
        margins = (c_int * 4)(-1, -1, -1, -1)
        dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))
        return True
    except Exception as e:
        debug_print(f"毛玻璃特效失败: {e}")
        return False

def debug_print(*args, **kwargs):
    out = sys.stderr or sys.stdout
    if out is None:
        return
    print(*args, file=out, **kwargs)
    out.flush()

def global_excepthook(exc_type, exc_value, exc_traceback):
    with open("crash.log", "w", encoding="utf-8") as f:
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    debug_print("全局异常已捕获，详情请查看 crash.log")

sys.excepthook = global_excepthook

DEBUG_MODE = 1
CONFIG_LOADED = False
LOG_FILE = ""
STATUS_MONITOR = False

LANG_CHINESE = "zh"
LANG_ENGLISH = "en"
CURRENT_LANG = LANG_CHINESE

_lang_data = {}

def tr(key):
    return _lang_data.get(CURRENT_LANG, {}).get(key, key)

_console_log_callback = None

def set_console_log_callback(callback):
    global _console_log_callback
    _console_log_callback = callback

def log_message(message, level="INFO", stack_level=1):
    global DEBUG_MODE, LOG_FILE, _console_log_callback
    level_map = {"ERROR": 1, "WARNING": 1, "INFO": 2, "DEBUG": 3}
    msg_level = level_map.get(level, 2)
    if DEBUG_MODE < msg_level:
        return
    frame = inspect.currentframe().f_back
    while stack_level > 1 and frame:
        frame = frame.f_back
        stack_level -= 1
    if frame:
        func = frame.f_code.co_name
        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        caller = f"{filename}:{lineno} {func}()"
    else:
        caller = "unknown"
    data_dir = resource_path("data")
    os.makedirs(data_dir, exist_ok=True)
    if not LOG_FILE:
        LOG_FILE = os.path.join(data_dir, "LOG.txt")
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("=== 倒计时调试日志 ===\n")
                f.write(f"日志创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"系统信息: {platform.platform()} | Python版本: {sys.version}\n")
                f.write(f"当前工作目录: {os.getcwd()}\n")
                f.write(f"数据目录: {data_dir}\n\n")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level}] [{caller}] {message}\n")
    if DEBUG_MODE >= 3:
        debug_print(f"[{timestamp}] [{level}] [{caller}] {message}")
    if _console_log_callback:
        try:
            _console_log_callback(message, level, timestamp)
        except Exception:
            pass

def hide_console():
    if sys.platform == "win32" and hasattr(sys, 'frozen'):
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        year, month, day = map(int, date_str.split('-'))
        if month < 1 or month > 12 or day < 1 or day > calendar.monthrange(year, month)[1]:
            return False
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        if not time_str:
            return True
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def calculate_days(target_date, target_time="00:00"):
    today = datetime.now()
    try:
        if not validate_date(target_date):
            return 0, 0, 0, 0, 0.0, ""
        if target_time and validate_time(target_time):
            target = datetime.strptime(f"{target_date} {target_time}", "%Y-%m-%d %H:%M")
        else:
            target = datetime.strptime(target_date, "%Y-%m-%d")
        if target < today:
            return 0, 0, 0, 0, 0.0, ""
        diff = target - today
        total_seconds = diff.total_seconds()
        days = int(total_seconds // (24 * 3600))
        hours = int((total_seconds % (24 * 3600)) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        total_days = (target.date() - today.date()).days

        work_days = 0
        work_seconds = 0.0
        holiday_name = ""

        if total_days > 0:
            for i in range(total_days):
                current_date = today.date() + timedelta(days=i + 1)
                if chinese_calendar.is_workday(current_date):
                    work_days += 1
                else:
                    on_holiday, name = chinese_calendar.get_holiday_detail(current_date)
                    if on_holiday and i == 0:
                        holiday_name = name

        if chinese_calendar.is_workday(today.date()):
            now_time = today.hour * 3600 + today.minute * 60 + today.second
            work_start = 9 * 3600
            work_end = 18 * 3600
            if now_time < work_start:
                remaining_today = work_end - work_start
            elif now_time > work_end:
                remaining_today = 0.0
            else:
                remaining_today = work_end - now_time
            work_seconds = work_days * 8 * 3600 + remaining_today
        else:
            work_seconds = work_days * 8 * 3600

        work_days_float = work_seconds / (8 * 3600)

        return days, hours, minutes, work_days, work_days_float, holiday_name
    except ValueError:
        return 0, 0, 0, 0, 0.0, ""


def format_countdown_text(days, hours, minutes, work_days, work_days_float,
                          holiday_name, show_both=True):
    parts = []

    if show_both:
        if days > 0:
            time_str = f"{days}天 {hours:02d}时 {minutes:02d}分"
        else:
            time_str = f"{hours:02d}时 {minutes:02d}分"
        parts.append(f"自然日 {time_str}")
        if work_days > 0:
            parts.append(f"工作日 {work_days}天")
    else:
        if days > 0:
            parts.append(f"剩余 {days}天 {hours:02d}时 {minutes:02d}分")
        else:
            parts.append(f"剩余 {hours:02d}时 {minutes:02d}分")
        if work_days > 0:
            parts.append(f"(工作日 {work_days}天)")

    if holiday_name:
        parts.append(f"📆 {holiday_name}")

    return "  |  ".join(parts)

# 数字滚动标签
class RollingNumberLabel(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, text="0.000 天", parent=None):
        super().__init__(parent)
        self._value = 0.0
        self._target_value = 0.0
        self._anim_progress = 1.0
        self._anim = QPropertyAnimation(self, b"anim_progress", self)
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.finished.connect(self._on_anim_finished)
        self._current_str = "0.000"
        self._target_str = "0.000"
        self._unit = " 天"
        self._expired = False
        self._expired_text = "已到期"
        self._display_format = "decimal"
        self._display_format_template = "{days}天 {hours}时 {minutes}分"
        self._raw_days = 0.0
        self.use_neon = True
        self.gradient_start = QColor("#00f2fe")
        self.gradient_end = QColor("#4facfe")
        self.glow_color = QColor(79, 172, 254, 160)
        self._pulse_phase = 0.0
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._tick_pulse)
        self._pulse_timer.start(80)
        self.setMinimumSize(200, 65)
        self.setFont(QFont("Microsoft YaHei", 28, QFont.Weight.Bold))

    def _tick_pulse(self):
        if not self.isVisible():
            return
        self._pulse_phase += 0.05
        if self._pulse_phase > 2 * math.pi:
            self._pulse_phase -= 2 * math.pi
        self.update()

    @pyqtProperty(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, val):
        self._anim_progress = val
        self.update()

    def set_display_format(self, fmt, template="{days}天 {hours}时 {minutes}分"):
        self._display_format = fmt
        self._display_format_template = template
        if not self._expired and self._raw_days > 0:
            self._apply_format_and_update()

    def _format_value(self, days_float):
        if self._display_format == "decimal":
            return f"{days_float:.3f}", " 天"
        elif self._display_format == "integer":
            return str(int(days_float)), " 天"
        elif self._display_format == "hms":
            total_seconds = days_float * 86400
            d = int(total_seconds // 86400)
            h = int((total_seconds % 86400) // 3600)
            m = int((total_seconds % 3600) // 60)
            if d > 0:
                return f"{d}天 {h}时 {m}分", ""
            else:
                return f"{h}时 {m}分", ""
        elif self._display_format == "custom":
            total_seconds = days_float * 86400
            d = int(total_seconds // 86400)
            h = int((total_seconds % 86400) // 3600)
            m = int((total_seconds % 3600) // 60)
            s = int(total_seconds % 60)
            try:
                text = self._display_format_template.format(days=d, hours=h, minutes=m, seconds=s)
            except (KeyError, ValueError):
                text = f"{d}天 {h}时 {m}分"
            return text, ""
        return f"{days_float:.3f}", " 天"

    def _apply_format_and_update(self):
        target_str, unit = self._format_value(self._raw_days)
        self._target_str = target_str
        self._current_str = target_str
        self._unit = unit
        self._anim_progress = 1.0
        self.update()

    def setValue(self, new_value: float):
        if abs(new_value - self._target_value) < 1e-6:
            return
        if self._expired and new_value <= 0:
            return
        if new_value <= 0:
            self.showExpired()
            self.value_changed.emit(new_value)
            return
        self._expired = False
        self._target_value = new_value
        self._raw_days = new_value
        target_str, unit = self._format_value(new_value)
        self._unit = unit
        if target_str == self._target_str:
            return
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
            self._current_str = self._target_str
        self._target_str = target_str
        if len(self._current_str) != len(self._target_str):
            self._current_str = self._target_str
            self._anim_progress = 1.0
            self.update()
            self.value_changed.emit(new_value)
            return
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()
        self.value_changed.emit(new_value)

    def _on_anim_finished(self):
        self._current_str = self._target_str
        self._anim_progress = 1.0
        self.update()

    def showExpired(self, text=None):
        if text is not None:
            self._expired_text = text
        display = self._expired_text if self._expired_text else "0.000"
        self._expired = True
        self._target_str = display
        self._current_str = display
        self._unit = "" if self._expired_text else " 天"
        self._target_value = 0.0
        self._anim_progress = 1.0
        self.setToolTip("此项目倒计时已到期")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(self.font())

        if self._expired:
            display_text = self._target_str
            fm = QFontMetrics(self.font())
            text_width = fm.horizontalAdvance(display_text)
            text_height = fm.height()
            x = (self.width() - text_width) // 2
            y = (self.height() - text_height) // 2 + fm.ascent()

            # 效果
            if self.use_neon:
                pulse = (math.sin(self._pulse_phase) + 1.0) / 2.0
                glow = QColor(243, 139, 168, int(40 + pulse * 30))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow)
                painter.drawRoundedRect(QRectF(self.rect().adjusted(4, 4, -4, -4)), 10, 10)

            grad = QLinearGradient(0, 0, self.width(), 0)
            grad.setColorAt(0.0, QColor("#f38ba8"))
            grad.setColorAt(1.0, QColor("#e06c75"))
            pen = QPen()
            pen.setBrush(QBrush(grad))
            painter.setPen(pen)
            painter.setFont(QFont(self.font().family(), self.font().pixelSize(), QFont.Weight.Bold))
            painter.drawText(int(x), int(y), display_text)
            return

        if self.use_neon:
            pulse = (math.sin(self._pulse_phase) + 1.0) / 2.0
            glow_alpha = int(30 + pulse * 40)
            glow_rect = self.rect().adjusted(4, 4, -4, -4)
            glow = QColor(self.glow_color)
            glow.setAlpha(glow_alpha // 3)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow)
            painter.drawRoundedRect(QRectF(glow_rect), 10, 10)

        digit_str = self._current_str
        target_str = self._target_str
        unit = self._unit
        fm = QFontMetrics(self.font())

        full_text = target_str + unit
        text_width = fm.horizontalAdvance(full_text)
        text_height = fm.height()
        x = (self.width() - text_width) // 2
        y = (self.height() - text_height) // 2 + fm.ascent()
        progress = self._anim_progress

        clip_top = int(y - fm.ascent())
        clip_h = int(fm.height())
        line_clip = QRect(0, clip_top, self.width(), clip_h)

        x_cursor = x
        for i in range(len(target_str)):
            ch_target = target_str[i]
            ch_current = digit_str[i] if i < len(digit_str) else ch_target
            char_width = fm.horizontalAdvance(ch_target)

            if ch_current != ch_target and progress < 1.0:
                painter.save()
                painter.setClipRect(line_clip)
                new_y = y + (1.0 - progress) * text_height
                painter.setPen(self._text_color())
                painter.drawText(int(x_cursor), int(new_y), ch_target)
                old_y = y - progress * text_height
                fade_alpha = max(15, int(140 * (1.0 - progress)))
                painter.setPen(self._text_color(alpha=fade_alpha))
                painter.drawText(int(x_cursor), int(old_y), ch_current)
                painter.restore()
            else:
                painter.setPen(self._text_color())
                painter.drawText(int(x_cursor), int(y), ch_target)
            x_cursor += char_width

        painter.setPen(self._text_color(alpha=220))
        painter.drawText(int(x_cursor), int(y), unit)

        if self.use_neon:
            painter.setPen(QPen(QColor(255, 255, 255, 30), 0.5))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, full_text)

    def _text_color(self, alpha=255):
        if self.use_neon:
            grad = QLinearGradient(0, 0, self.width(), 0)
            start_color = QColor(self.gradient_start)
            end_color = QColor(self.gradient_end)
            start_color.setAlpha(alpha)
            end_color.setAlpha(alpha)
            grad.setColorAt(0.0, start_color)
            grad.setColorAt(1.0, end_color)
            pen = QPen()
            pen.setBrush(QBrush(grad))
            return pen
        color = QColor("#E0E0E0")
        color.setAlpha(alpha)
        return QPen(color)

    def set_neon_config(self, use_neon, start_hex, end_hex, glow_hex, normal_hex):
        self.use_neon = use_neon
        self.gradient_start = QColor(start_hex)
        self.gradient_end = QColor(end_hex)
        self.glow_color = QColor(glow_hex)
        self.update()

    def setText(self, text):
        pass

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        text = self._target_str + self._unit
        width = fm.horizontalAdvance(text) + 40
        height = fm.height() + 20
        return QSize(max(220, width), max(60, height))

# 打字机标签 出错最多的地方危险指数 ★ ★ ★
class TypewriterLabel(QWidget):
    typing_finished = pyqtSignal()

    def __init__(self, parent=None, speed=150):
        super().__init__(parent)
        self._full_text = ""
        self._char_index = 0
        self._is_deleting = False
        self._current_display = ""
        self._speed = speed
        self._on_finished = None
        self._show_cursor = True
        self._blink_state = True
        self._alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self._word_wrap = True
        self._text_color_hex = "#E0E0E0"
        self._opacity = 1.0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate_step)

        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._toggle_blink)
        self._blink_timer.start(530)

        self._delay_timer = QTimer(self)
        self._delay_timer.setSingleShot(True)
        self._pending_text = None
        self._pending_callback = None

        self.setFont(QFont("Microsoft YaHei", 10))
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)


    def setAlignment(self, alignment):
        self._alignment = alignment
        self.update()

    def alignment(self):
        return self._alignment

    def setWordWrap(self, on):
        self._word_wrap = on
        self.update()

    def wordWrap(self):
        return self._word_wrap

    def text(self):
        return self._current_display

    def setText(self, t):
        self._current_display = t
        self._char_index = len(t)
        self._full_text = t
        self.updateGeometry()
        self.update()

    def setStyleSheet(self, style):
        super().setStyleSheet(style)
        import re
        m = re.search(r'color\s*:\s*(#[0-9a-fA-F]{3,8})', style)
        if m:
            self._text_color_hex = m.group(1)
        self.update()

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        text = self._full_text or self._current_display
        if width <= 0 or not text:
            return 40
        layout = self._build_layout(text, width)
        h = int(layout.boundingRect().height()) + 10
        return max(40, h)

    def sizeHint(self):
        w = max(self.width(), 100)
        return QSize(w, self.heightForWidth(w))

    def minimumSizeHint(self):
        fm = QFontMetrics(self.font())
        return QSize(60, fm.height() + 6)


    def _build_layout(self, text, width=None):
        if width is None:
            width = max(self.width(), 100)
        usable_width = max(width - 8, 40)

        text_option = QTextOption()
        if self._word_wrap:
            text_option.setWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        else:
            text_option.setWrapMode(QTextOption.WrapMode.NoWrap)
        text_option.setAlignment(self._alignment)

        layout = QTextLayout(text, self.font(), self)
        layout.setTextOption(text_option)
        leading = QFontMetrics(self.font()).leading()

        layout.beginLayout()
        y = 0
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(usable_width)
            y += leading
            line.setPosition(QPointF(4, y))
            y += line.height()
        layout.endLayout()
        return layout

    def _toggle_blink(self):
        self._blink_state = not self._blink_state
        if self._show_cursor:
            self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.update()

    def start_animation(self, new_text, on_finished=None, delay_ms=0):
        if not new_text:
            return
        if delay_ms > 0:
            self._pending_text = new_text
            self._pending_callback = on_finished
            try:
                self._delay_timer.timeout.disconnect()
            except Exception:
                pass
            self._delay_timer.timeout.connect(self._start_delayed)
            self._delay_timer.start(delay_ms)
            return
        self._do_start(new_text, on_finished)

    def _start_delayed(self):
        try:
            self._delay_timer.timeout.disconnect()
        except Exception:
            pass
        if self._pending_text:
            self._do_start(self._pending_text, self._pending_callback)
            self._pending_text = None
            self._pending_callback = None

    def _do_start(self, new_text, on_finished):
        self._full_text = new_text
        self._current_display = self._current_display if self._current_display else ""
        self._on_finished = on_finished
        self._is_deleting = True
        self._char_index = len(self._current_display)
        self._show_cursor = True
        if isinstance(self.graphicsEffect(), QGraphicsOpacityEffect):
            self.setGraphicsEffect(None)
        parent = self.parent()
        if parent and parent.width() > 0:
            tw = int(parent.width() * 0.9)
            th = self.heightForWidth(tw)
            th = max(th, 40)
            self.resize(tw, th)
            self.move((parent.width() - tw) // 2, self.y())
        self._timer.start(max(20, self._speed // 3))

    def stop_animation(self):
        self._timer.stop()
        self._delay_timer.stop()
        self._current_display = self._full_text
        self._char_index = len(self._full_text)
        self._show_cursor = False
        self.update()

    def _animate_step(self):
        if self._is_deleting:
            if self._char_index > 0:
                self._char_index -= 1
                self._current_display = self._current_display[:self._char_index]
            else:
                self._is_deleting = False
                self._char_index = 0
                self._timer.setInterval(self._speed)

        else:
            if self._char_index < len(self._full_text):
                self._char_index += 1
                self._current_display = self._full_text[:self._char_index]

            else:
                self._timer.stop()
                self._show_cursor = False

                if self._on_finished:
                    cb = self._on_finished
                    self._on_finished = None
                    cb()
        self.updateGeometry()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(self.font())
        painter.setOpacity(self._opacity)
        text_color = QColor(self._text_color_hex)

        if not self._current_display:
            if self._show_cursor and self._blink_state:
                fm = QFontMetrics(self.font())
                painter.setPen(QPen(text_color, 1.5))
                painter.drawLine(4, 4, 4, 4 + fm.height())
            painter.end()
            return

        w = max(self.width(), 100)
        layout = self._build_layout(self._current_display, w)

        painter.setPen(text_color)
        layout.draw(painter, QPointF(0, 0))

        if self._show_cursor and self._blink_state and self._char_index >= 0:
            cursor_drawn = False
            for i in range(layout.lineCount()):
                line = layout.lineAt(i)
                line_start = line.textStart()
                line_len = line.textLength()
                line_end = line_start + line_len

                if self._char_index <= line_end or i == layout.lineCount() - 1:
                    cursor_in_line = max(0, min(self._char_index - line_start, line_len))
                    result = line.cursorToX(cursor_in_line)
                    cursor_x = result[0] if isinstance(result, (tuple, list)) else result
                    cursor_y = line.position().y()
                    cursor_h = line.height()
                    painter.setPen(QPen(text_color, 1.5))
                    painter.drawLine(int(cursor_x), int(cursor_y + 2),
                                     int(cursor_x), int(cursor_y + cursor_h - 2))
                    cursor_drawn = True
                    break

            if not cursor_drawn and layout.lineCount() > 0:
                last_line = layout.lineAt(layout.lineCount() - 1)
                result = last_line.cursorToX(last_line.textLength())
                cursor_x = result[0] if isinstance(result, (tuple, list)) else result
                cursor_y = last_line.position().y()
                cursor_h = last_line.height()
                painter.setPen(QPen(text_color, 1.5))
                painter.drawLine(int(cursor_x), int(cursor_y + 2),
                                 int(cursor_x), int(cursor_y + cursor_h - 2))

        painter.end()

# 天气
WEATHER_CODE_MAP = {
    0: "晴", 1: "大部晴朗", 2: "多云", 3: "阴天",
    45: "雾", 48: "沉积雾凇的雾",
    51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "小阵雨", 81: "中阵雨", 82: "大阵雨",
    95: "雷暴", 96: "冰雹雷暴", 99: "大冰雹雷暴"
}

class WeatherForecastDialog(QDialog):
    def __init__(self, lat, lon, city_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"📅 {city_name} 未来天气预报")
        self.resize(500, 400)
        self.setStyleSheet(get_theme_qss(get_system_theme()))
        self.lat = lat
        self.lon = lon
        self.city = city_name
        self.forecast_data = []
        layout = QVBoxLayout(self)
        self.label_title = QLabel("正在加载...")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(self.label_title)
        self.scroll = QScrollArea()
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)
        self.load_forecast()

    def load_forecast(self):
        def fetch():
            try:
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "daily": "temperature_2m_max,temperature_2m_min,weathercode",
                    "timezone": "auto",
                    "forecast_days": 7
                }
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()
                self.forecast_data = []
                daily = data.get("daily", {})
                dates = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                codes = daily.get("weathercode", [])
                for i in range(len(dates)):
                    self.forecast_data.append({
                        "date": dates[i],
                        "max": max_temps[i],
                        "min": min_temps[i],
                        "code": codes[i]
                    })
                QTimer.singleShot(0, self.update_ui)
            except Exception as e:
                QTimer.singleShot(0, lambda: self.label_title.setText("加载失败"))
        threading.Thread(target=fetch, daemon=True).start()

    def update_ui(self):
        if not self.forecast_data:
            self.label_title.setText("无数据")
            return
        self.label_title.setText(f"{self.city} 未来天气")
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for day in self.forecast_data:
            date_str = day["date"]
            desc = WEATHER_CODE_MAP.get(day["code"], "未知")
            row = QHBoxLayout()
            lbl_date = QLabel(date_str)
            lbl_date.setStyleSheet("font-weight: bold;")
            lbl_desc = QLabel(desc)
            lbl_temp = QLabel(f"🌡 {day['min']}°C ~ {day['max']}°C")
            row.addWidget(lbl_date)
            row.addWidget(lbl_desc)
            row.addWidget(lbl_temp)
            self.content_layout.addLayout(row)

class WeatherFetcher(QObject):
    weather_updated = pyqtSignal(str)

    # 支持的API提供商：open_meteo (原版), wttr_in (国内推荐), custom (自定义)
    def __init__(self, parent=None, api_provider="wttr_in", custom_url_template=""):
        super().__init__(parent)
        self.lat = None
        self.lon = None
        self.city_name = ""
        self.api_provider = api_provider
        self.custom_url_template = custom_url_template  # 自定义URL，用{city}占位

    def fetch(self, city_name=""):
        def run():
            headers = {"User-Agent": "CountdownDesktop/1.0"}
            try:
                if self.api_provider == "wttr_in":
                    self._fetch_wttr(headers, city_name)
                elif self.api_provider == "custom" and self.custom_url_template:
                    self._fetch_custom(headers, city_name)
                else:
                    self._fetch_open_meteo(headers, city_name)
            except Exception as e:
                debug_print(f"天气获取失败: {e}")
                self.weather_updated.emit("🌤️ 天气离线")

        threading.Thread(target=run, daemon=True).start()

    def _fetch_wttr(self, headers, city_name):
        try:
            city = city_name if city_name else "Beijing"
            # format=%C+%t 表示：天气描述+温度，lang=zh 中文
            url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%C+%t&lang=zh"
            resp = requests.get(url, timeout=6, headers=headers)
            if resp.status_code == 200 and resp.text.strip():
                result = resp.text.strip().replace("+", " ")
                self.weather_updated.emit(f"{city} {result}")
            else:
                raise Exception("wttr.in 返回异常")
        except Exception as e:
            debug_print(f"wttr.in 失败，回退: {e}")
            self._fetch_open_meteo(headers, city_name)

    def _fetch_custom(self, headers, city_name):
        try:
            url = self.custom_url_template.replace("{city}", urllib.parse.quote(city_name))
            resp = requests.get(url, timeout=6, headers=headers)
            if resp.status_code == 200:
                self.weather_updated.emit(resp.text.strip())
            else:
                raise Exception(f"自定义API返回 {resp.status_code}")
        except Exception as e:
            debug_print(f"自定义天气API失败: {e}")
            self.weather_updated.emit("🌤️ 自定义API离线")

    def _fetch_open_meteo(self, headers, city_name):
        try:
            lat, lon, name = None, None, ""
            if city_name:
                try:
                    geo_params = {"name": city_name, "count": 1, "language": "zh", "format": "json"}
                    geo_resp = requests.get("https://geocoding-api.open-meteo.com/v1/search", params=geo_params, timeout=5, headers=headers)
                    geo_data = geo_resp.json()
                    if "results" in geo_data and geo_data["results"]:
                        res = geo_data["results"][0]
                        lat, lon = res["latitude"], res["longitude"]
                        name = res.get("name", city_name)
                except Exception as e:
                    debug_print(f"地理编码失败: {e}")

            if lat is None:
                try:
                    ip_resp = requests.get("http://ip-api.com/json/?lang=zh-CN", timeout=5, headers=headers)
                    ip_data = ip_resp.json()
                    if ip_data.get("status") == "success":
                        lat, lon = ip_data["lat"], ip_data["lon"]
                        name = ip_data.get("city", "本地")
                    else:
                        raise Exception("IP定位失败")
                except Exception as e:
                    debug_print(f"IP定位失败: {e}")

            if lat is None:
                self.weather_updated.emit("🌤️ 定位失败")
                return

            self.lat, self.lon, self.city_name = lat, lon, name
            weather_params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"}
            w_resp = requests.get("https://api.open-meteo.com/v1/forecast", params=weather_params, timeout=5, headers=headers)
            w_data = w_resp.json()

            if "current_weather" not in w_data:
                self.weather_updated.emit("🌤️ 数据异常")
                return

            current = w_data["current_weather"]
            temp = current["temperature"]
            desc = WEATHER_CODE_MAP.get(current["weathercode"], "未知")
            self.weather_updated.emit(f"{name} {desc} {temp}°C")

        except requests.exceptions.Timeout:
            self.weather_updated.emit("🌤️ 天气超时")
        except Exception as e:
            debug_print(f"Open-Meteo获取失败: {e}")
            self.weather_updated.emit("🌤️ 天气离线")

# 插件系统基础类
class PluginPermission(IntFlag):
    NONE = 0
    FILE_READ = auto()
    FILE_WRITE = auto()
    FILE_DELETE = auto()
    NETWORK = auto()
    NETWORK_HTTP = auto()
    NETWORK_SOCKET = auto()
    COMMAND = auto()
    COMMAND_EXEC = auto()
    CLIPBOARD = auto()
    SYSTEM_INFO = auto()
    NOTIFICATION = auto()
    UI_INJECT = auto()
    EVENT_LISTEN = auto()
    THREAD_SPAWN = auto()
    PROCESS_SPAWN = auto()
    REGISTRY = auto()
    ENV_READ = auto()
    DANGEROUS_EVAL = auto()


class PluginAPI:

    def __init__(self, plugin, app):
        self._plugin = plugin
        self._app = app  # 私有，外部不可直接访问

    def log(self, message, level="INFO"):
        self._plugin.log_plugin(message, level)

    def register_dynamic_bg(self, id_name, display_name, widget_class):
        self._app.dynamic_bg_registry[id_name] = display_name
        self._app.dynamic_bg_classes[id_name] = widget_class
        self.log(f"成功注册动态背景: {display_name}")

    def register_settings_panel(self, id_name, display_name, widget_class):
        if not hasattr(self._app, 'plugin_settings_panels'):
            self._app.plugin_settings_panels = {}
        plugin_name = self._plugin.name if self._plugin and hasattr(self._plugin, 'name') else "unknown"
        self._app.plugin_settings_panels[id_name] = {
            "name": display_name,
            "class": widget_class,
            "plugin": plugin_name
        }
        self.log(f"成功注册设置面板: {display_name}")

    def register_widget(self, id_name, display_name, widget_class):
        if not hasattr(self._app, 'custom_widget_registry'):
            self._app.custom_widget_registry = {}
        self._app.custom_widget_registry[id_name] = {
            "name": display_name,
            "class": widget_class
        }
        self.log(f"成功注册自定义控件: {display_name}")

    def register_settings_widget(self, id_name, display_name, widget_class):
        if not hasattr(self._app, 'plugin_settings_panels'):
            self._app.plugin_settings_panels = {}
        self._app.plugin_settings_panels[id_name] = {
            "name": display_name,
            "class": widget_class
        }
        self.log(f"成功注册设置面板: {display_name}")

    def get_config(self, key, default=None):
        config = self._app.plugin_manager.get_plugin_config(self._plugin.name)
        return config.get(key, default)

    def set_config(self, key, value):
        self._app.plugin_manager.set_plugin_config(self._plugin.name, key, value)

    def show_notification(self, title, message):
        try:
            tray = self._app.tray_icon.tray
            tray.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)
        except Exception as e:
            self.log(f"发送通知失败: {e}", "WARNING")

import hashlib
import threading
import sys
import os
import json

_plugin_context = threading.local()
_audit_guard = threading.local()

class PluginManager(QObject):
    def __init__(self, app, load_immediately=False):
        super().__init__()
        self.app = app
        self.plugins = []
        self.plugin_dir = os.path.join(resource_path(""), "plugins")
        os.makedirs(self.plugin_dir, exist_ok=True)
        self.plugin_security = {}
        self._plugin_risk = {}
        self.plugin_configs = {}
        self.signature_required = False
        self.public_key = None
        self._audit_hook_installed = False
        self._audit_suppress = False
        self.load_security_config()
        if load_immediately:
            self.load_plugins()

    def load_security_config(self):
        config_path = os.path.join(self.app.data_dir, "plugin_security.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.plugin_security = json.load(f)
            except:
                self.plugin_security = {}
        config_file = os.path.join(self.app.data_dir, "plugin_settings.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.plugin_configs = json.load(f)
            except:
                self.plugin_configs = {}

    def save_security_config(self):
        config_path = os.path.join(self.app.data_dir, "plugin_security.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.plugin_security, f, indent=2)
        config_file = os.path.join(self.app.data_dir, "plugin_settings.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.plugin_configs, f, indent=2)

    def get_plugin_config(self, plugin_name):
        return self.plugin_configs.get(plugin_name, {})

    def set_plugin_config(self, plugin_name, key, value):
        if plugin_name not in self.plugin_configs:
            self.plugin_configs[plugin_name] = {}
        self.plugin_configs[plugin_name][key] = value
        self.save_security_config()

    def _install_audit_hook(self):
        if self._audit_hook_installed:
            return
        manager = self
        plugin_dir_abs = os.path.normcase(os.path.abspath(self.plugin_dir))
        data_dir_abs = os.path.normcase(os.path.abspath(self.app.data_dir))

        def _find_plugin_from_stack():
            try:
                frame = sys._getframe(2)
                depth = 0
                while frame is not None and depth < 60:
                    fname = frame.f_code.co_filename
                    if fname and not fname.startswith('<'):
                        fpath = os.path.normcase(os.path.abspath(fname))
                        if fpath.startswith(plugin_dir_abs + os.sep):
                            base = os.path.basename(fpath)
                            for p in manager.plugins:
                                if p.filename == base:
                                    return p
                            return None
                    frame = frame.f_back
                    depth += 1
            except Exception:
                pass
            return None

        def _is_app_internal_file(path):
            try:
                p = os.path.normcase(os.path.abspath(str(path)))
                if not p.startswith(data_dir_abs + os.sep):
                    return False
                frame = sys._getframe(2)
                if frame:
                    fname = frame.f_code.co_filename
                    if fname and not fname.startswith('<'):
                        fpath = os.path.normcase(os.path.abspath(fname))
                        if fpath.startswith(plugin_dir_abs + os.sep):
                            return False
                return True
            except Exception:
                return False

        def audit_hook(event, args):
            if getattr(_audit_guard, 'active', False):
                return
            if manager._audit_suppress:
                return
            if event not in ('open', 'os.system', 'subprocess.Popen', 'subprocess.call',
                             'exec', 'eval', 'urllib.Request', 'socket.connect',
                             'socket.getaddrinfo', 'os.remove', 'os.unlink',
                             'os.rmdir', 'os.rename'):
                return
            if not manager.plugins:
                return
            plugin = getattr(_plugin_context, 'current_plugin', None)
            if plugin is None:
                plugin = _find_plugin_from_stack()
            if plugin is None:
                return
            disabled = manager.app.global_disable_all_plugins or not plugin.enabled

            def _record(text):
                _audit_guard.active = True
                try:
                    manager.app.append_sensitive_log(plugin.name, text,
                                                     str(args[0])[:120] if args else "")
                except Exception:
                    pass
                finally:
                    _audit_guard.active = False

            def _deny(reason):
                _audit_guard.active = True
                try:
                    manager.app.append_sensitive_log(
                        plugin.name, f"[已拦截] {event}",
                        (str(args[0])[:120] if args else "") + f" ({reason})")
                    plugin.log_plugin(f"敏感操作被拦截: {event} ({reason})", "WARNING")
                except Exception:
                    pass
                finally:
                    _audit_guard.active = False
                raise PermissionError(f"插件 '{plugin.name}' {reason}")

            if event == 'open':
                path = args[0] if len(args) > 0 else ''
                if _is_app_internal_file(path):
                    return
                mode = args[1] if len(args) > 1 else 'r'
                if isinstance(mode, int):
                    write_mode = bool(mode & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_TRUNC))
                else:
                    write_mode = any(c in str(mode) for c in ('w', 'a', '+', 'x'))
                if disabled:
                    _deny("插件处于禁用状态，禁止文件访问")
                if write_mode:
                    if not plugin.permissions & PluginPermission.FILE_WRITE:
                        _deny("无写入文件权限")
                else:
                    if not plugin.permissions & PluginPermission.FILE_READ:
                        _deny("无读取文件权限")
                _record(f"{event} mode={mode}")
                return
            if event in ('os.remove', 'os.unlink', 'os.rmdir', 'os.rename'):
                if args and _is_app_internal_file(args[0]):
                    return
                if disabled:
                    _deny("插件处于禁用状态，禁止删除/移动文件")
                if not plugin.permissions & PluginPermission.FILE_WRITE:
                    _deny("无写入文件权限")
                _record(event)
                return
            if event in ('os.system', 'subprocess.Popen', 'subprocess.call', 'exec', 'eval'):
                if disabled:
                    _deny("插件处于禁用状态，禁止执行命令")
                if not plugin.permissions & PluginPermission.COMMAND:
                    _deny("无执行系统命令权限")
                _record(event)
                return
            if event in ('urllib.Request', 'socket.connect', 'socket.getaddrinfo'):
                if disabled:
                    _deny("插件处于禁用状态，禁止网络访问")
                if not plugin.permissions & PluginPermission.NETWORK:
                    _deny("无网络权限")
                _record(event)
                return

        sys.addaudithook(audit_hook)
        self._audit_hook_installed = True

    def load_plugins(self):
        if self.app.global_disable_all_plugins:
            self.plugins.clear()
            return

        self._install_audit_hook()

        self.plugins.clear()
        self._audit_suppress = True
        sys.path.insert(0, self.plugin_dir)
        for filename in sorted(os.listdir(self.plugin_dir)):
            if filename.endswith(".py") and not filename.startswith("_"):
                filepath = os.path.join(self.plugin_dir, filename)
                module_name = filename[:-3]
                log_message(f"[插件] 正在加载: {filename}", "INFO")
                try:
                    if self.signature_required:
                        if not self._verify_signature(filepath):
                            log_message(f"[插件] {filename} 未通过签名验证，跳过", "WARNING")
                            continue
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    safe_builtins = {
                        '__import__': __import__,
                        '__build_class__': __build_class__,
                        'print': print,
                        'len': len,
                        'range': range,
                        'int': int,
                        'float': float,
                        'str': str,
                        'list': list,
                        'dict': dict,
                        'tuple': tuple,
                        'set': set,
                        'bool': bool,
                        'bytes': bytes,
                        'bytearray': bytearray,
                        'open': open,
                        'eval': eval,
                        'exec': exec,
                        'compile': compile,
                        'True': True,
                        'False': False,
                        'None': None,
                        'Exception': Exception,
                        'ValueError': ValueError,
                        'TypeError': TypeError,
                        'KeyError': KeyError,
                        'IndexError': IndexError,
                        'AttributeError': AttributeError,
                        'ImportError': ImportError,
                        'RuntimeError': RuntimeError,
                        'StopIteration': StopIteration,
                        'NotImplementedError': NotImplementedError,
                        'OSError': OSError,
                        'IOError': IOError,
                        'PermissionError': PermissionError,
                        'FileNotFoundError': FileNotFoundError,
                        'FileExistsError': FileExistsError,
                        'IsADirectoryError': IsADirectoryError,
                        'NotADirectoryError': NotADirectoryError,
                        'TimeoutError': TimeoutError,
                        'ConnectionError': ConnectionError,
                        'ZeroDivisionError': ZeroDivisionError,
                        'ArithmeticError': ArithmeticError,
                        'OverflowError': OverflowError,
                        'LookupError': LookupError,
                        'UnicodeError': UnicodeError,
                        'UnicodeDecodeError': UnicodeDecodeError,
                        'UnicodeEncodeError': UnicodeEncodeError,
                        'BlockingIOError': BlockingIOError,
                        'InterruptedError': InterruptedError,
                        'ProcessLookupError': ProcessLookupError,
                        'RecursionError': RecursionError,
                        'SystemError': SystemError,
                        'NameError': NameError,
                        'UnboundLocalError': UnboundLocalError,
                        'AssertionError': AssertionError,
                        'MemoryError': MemoryError,
                        'BufferError': BufferError,
                        'Warning': Warning,
                        'BaseException': BaseException,
                        'isinstance': isinstance,
                        'hasattr': hasattr,
                        'getattr': getattr,
                        'setattr': setattr,
                        'delattr': delattr,
                        'property': property,
                        'staticmethod': staticmethod,
                        'classmethod': classmethod,
                        'super': super,
                        'object': object,
                        'type': type,
                        'enumerate': enumerate,
                        'zip': zip,
                        'map': map,
                        'filter': filter,
                        'sorted': sorted,
                        'reversed': reversed,
                        'min': min,
                        'max': max,
                        'sum': sum,
                        'abs': abs,
                        'round': round,
                        'any': any,
                        'all': all,
                        'iter': iter,
                        'next': next,
                        'ord': ord,
                        'chr': chr,
                        'id': id,
                        'repr': repr,
                        'dir': dir,
                        'vars': vars,
                        'hex': hex,
                        'oct': oct,
                        'bin': bin,
                        'divmod': divmod,
                        'pow': pow,
                        'hash': hash,
                        'slice': slice,
                        'complex': complex,
                        'memoryview': memoryview,
                        'frozenset': frozenset,
                        'format': format,
                        'callable': callable,
                        'input': input,
                    }
                    module.__builtins__ = safe_builtins

                    module.Plugin = Plugin
                    module.PluginPermission = PluginPermission

                    spec.loader.exec_module(module)
                    if hasattr(module, 'setup'):
                        _plugin_context.current_plugin = None
                        plugin_api = PluginAPI(None, self.app)
                        plugin_instance = module.setup(self.app, plugin_api)
                        plugin_instance.filename = filename
                        plugin_instance.api = PluginAPI(plugin_instance, self.app)
                        self.plugins.append(plugin_instance)
                        log_message(
                            f"[插件] {filename} 加载成功 (name={plugin_instance.name}, ver={plugin_instance.version})",
                            "INFO")
                    else:
                        log_message(f"[插件] {filename} 缺少 setup() 函数，跳过", "WARNING")
                except Exception as e:
                    import traceback
                    tb = traceback.format_exc()
                    log_message(f"[插件] {filename} 加载失败: {e}", "ERROR")
                    log_message(f"[插件] 完整堆栈:\n{tb}", "ERROR")
        sys.path.pop(0)
        self._audit_suppress = False
        self.save_security_config()

    def _verify_signature(self, plugin_path):
        sig_path = plugin_path + ".sig"
        if not os.path.exists(sig_path):
            return False
        if not self.public_key:
            return True
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            from cryptography.exceptions import InvalidSignature
            with open(plugin_path, 'rb') as f:
                content = f.read()
            with open(sig_path, 'rb') as f:
                signature = f.read()
            public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(self.public_key))
            public_key.verify(signature, content)
            return True
        except ImportError:
            log_message("cryptography 库未安装，无法验证签名", "ERROR")
            return False
        except InvalidSignature:
            return False

    def enable_plugin(self, plugin, limited=False, force=False):
        if self.app.global_disable_all_plugins and not force:
            log_message("全局插件已禁用，无法启用", "WARNING")
            return
        if plugin.enabled and not force:
            return
        if not force and not plugin.trusted:
            perms = plugin.requested_permissions
            if perms != PluginPermission.NONE:
                msg = f"插件 '{plugin.name}' 请求以下权限：\n"
                if perms & PluginPermission.FILE_READ: msg += "  - 读取文件\n"
                if perms & PluginPermission.FILE_WRITE: msg += "  - 写入文件\n"
                if perms & PluginPermission.NETWORK: msg += "  - 网络访问\n"
                if perms & PluginPermission.COMMAND: msg += "  - 执行系统命令\n"
                msg += "\n是否授予这些权限？\n（拒绝后插件仍会启用，但无对应权限）"
                reply = QMessageBox.question(None, "权限请求", msg,
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    plugin.permissions = perms
                else:
                    plugin.permissions = PluginPermission.NONE
            else:
                plugin.permissions = PluginPermission.NONE
        elif not force and plugin.trusted:
            plugin.permissions = plugin.requested_permissions
        plugin.enabled = True
        plugin.limited = limited
        _plugin_context.current_plugin = plugin
        if hasattr(plugin, 'on_enable'):
            try:
                plugin.on_enable()
            except Exception as e:
                plugin.log_plugin(f"启用失败: {e}", "ERROR")
        _plugin_context.current_plugin = None
        self.save_security_config()
        self.app.save_config(force=True)

    def disable_plugin(self, plugin):
        if not plugin.enabled:
            return
        plugin.enabled = False
        _plugin_context.current_plugin = plugin
        if hasattr(plugin, 'on_disable'):
            try:
                plugin.on_disable()
            except Exception as e:
                plugin.log_plugin(f"禁用失败: {e}", "ERROR")
        _plugin_context.current_plugin = None
        self.save_security_config()
        self.app.save_config(force=True)

    def get_enabled_plugins(self):
        return [p for p in self.plugins if p.enabled]

    def trigger_event(self, event_name, *args, **kwargs):
        if self.app.global_disable_all_plugins:
            return
        for plugin in self.get_enabled_plugins():
            if hasattr(plugin, event_name):
                try:
                    _plugin_context.current_plugin = plugin
                    getattr(plugin, event_name)(*args, **kwargs)
                except Exception as e:
                    plugin.log_plugin(f"执行事件 {event_name} 时出错: {e}", "ERROR")
                finally:
                    _plugin_context.current_plugin = None

    def get_plugin_risk(self, plugin):
        return getattr(plugin, '_risk_level', 0)

    def set_plugin_permissions(self, plugin, perms):
        plugin.permissions = perms
        self.save_security_config()
        self.app.save_config(force=True)

class Plugin:
    def __init__(self):
        self.name = "Unnamed Plugin"
        self.version = "0.1"
        self.author = "Unknown"
        self.description = ""
        self.enabled = False
        self.log = []
        self.filename = None
        self._risk_level = 0
        self.limited = False
        self.permissions = PluginPermission.NONE
        self.requested_permissions = PluginPermission.NONE
        self.audit_log = []
        self.emergency_stop = False
        self.signature_verified = False
        self.trusted = False

    def log_plugin(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append(f"[{timestamp}][{level}] {message}")
        log_message(f"[Plugin:{self.name}] {message}", level, stack_level=2)

    def get_info_widget(self, parent=None):
        return None

    def on_enable(self):
        self.app.save_config(force=True)
        pass

    def on_disable(self):
        pass

# 主题类
class Theme:
    def __init__(self, name="默认主题", is_dark=False,
                 bg_color="#f5f7fa", frame_bg="#ffffff", accent_color="#3498db",
                 text_color="#2c3e50", border_color="#d1d8e0",
                 font_family="Microsoft YaHei", font_size=9,
                 window_round_radius=15,
                 window_brightness=1.0,
                 window_saturation=1.0):
        self.name = name
        self.is_dark = is_dark
        self.bg_color = bg_color
        self.frame_bg = frame_bg
        self.accent_color = accent_color
        self.text_color = text_color
        self.border_color = border_color
        self.font_family = font_family
        self.font_size = font_size
        self.window_round_radius = window_round_radius
        self.window_brightness = window_brightness
        self.window_saturation = window_saturation

    def to_dict(self):
        return {
            "name": self.name,
            "is_dark": self.is_dark,
            "bg_color": self.bg_color,
            "frame_bg": self.frame_bg,
            "accent_color": self.accent_color,
            "text_color": self.text_color,
            "border_color": self.border_color,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "window_round_radius": self.window_round_radius,
            "window_brightness": self.window_brightness,
            "window_saturation": self.window_saturation
        }

    @staticmethod
    def from_dict(data):
        return Theme(
            data.get("name", ""),
            data.get("is_dark", False),
            data.get("bg_color", "#f5f7fa"),
            data.get("frame_bg", "#ffffff"),
            data.get("accent_color", "#3498db"),
            data.get("text_color", "#2c3e50"),
            data.get("border_color", "#d1d8e0"),
            data.get("font_family", "Microsoft YaHei"),
            data.get("font_size", 9),
            data.get("window_round_radius", 15),
            data.get("window_brightness", 1.0),
            data.get("window_saturation", 1.0)
        )


def get_theme_colors(theme):
    if theme.is_dark:
        return {
            "accent": "#4FC3F7",
            "hover_accent": "#81D4FA",
            "panel_bg": "#252526",
            "input_bg": "#2D2D30",
            "text_color": "#E0E0E0",
            "secondary_text": "#AAAAAA",
            "border_color": "#3E3E42",
            "dark_bg": "#1E1E1E",
            "selected_text": "#1E1E1E",
            "btn_text": "#1E1E1E",
            "hover_btn_text": "#1E1E1E",
            "bg_color": "#1e1e2e",
            "alternate_bg": "#252526",
            "header_bg": "#333333",
            "header_text": "#CCCCCC",
            "tree_text": "#CCCCCC",
            "tree_bg": "#2D2D30",
            "console_bg": "#0f0f1a",
            "console_text": "#cdd6f4",
            "input_focus_border": "#89b4fa",
            "danger": "#e74c3c",
            "success": "#2ecc71",
            "purple": "#9b59b6",
            "blue": "#3498db",
            "intro_bg": "#2B2B2B",
            "intro_text": "#E0E0E0",
            "intro_title": "#FFFFFF",
        }
    else:
        return {
            "accent": "#0078D4",
            "hover_accent": "#106EBE",
            "panel_bg": "#F3F3F3",
            "input_bg": "#FFFFFF",
            "text_color": "#1D1D1F",
            "secondary_text": "#555555",
            "border_color": "#CCCCCC",
            "dark_bg": "#FFFFFF",
            "selected_text": "#FFFFFF",
            "btn_text": "#FFFFFF",
            "hover_btn_text": "#FFFFFF",
            "bg_color": "#f5f5f5",
            "alternate_bg": "#F0F0F0",
            "header_bg": "#E8E8E8",
            "header_text": "#333333",
            "tree_text": "#1E1E1E",
            "tree_bg": "#FFFFFF",
            "console_bg": "#FFFFFF",
            "console_text": "#1E1E1E",
            "input_focus_border": "#0078D4",
            "danger": "#e74c3c",
            "success": "#2ecc71",
            "purple": "#9b59b6",
            "blue": "#3498db",
            "intro_bg": "#F5F5F5",
            "intro_text": "#333333",
            "intro_title": "#1E1E1E",
        }

class SystemThemeMonitor(QObject):
    theme_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_dark = is_system_dark()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._check_theme)
        self._timer.start(2000)

    def _check_theme(self):
        new_dark = is_system_dark()
        if new_dark != self._current_dark:
            self._current_dark = new_dark
            self.theme_changed.emit(new_dark)

class CountdownProject:
    def __init__(self, name="新项目", target_date="", target_time="00:00", show_both=True,
                 font_size=28, bg_color="#0a0a1a", font_color="#c0c8f0",
                 position=None, size=None,
                 screen_width=1920, screen_height=1080, always_on_top=True, auto_font=True,
                 background_type="gradient", background_image="", window_alpha=0.88,
                 project_type="normal", pomodoro_work=25, pomodoro_break=5, pomodoro_long_break=15,
                 pomodoro_cycles=4,
                 custom_layout=None, window_round_radius=18,
                 use_neon=True, neon_start="#00f2fe", neon_end="#4facfe", neon_glow="#4facfe",
                 weather_city="",
                 gradient_start=None, gradient_end=None,
                 dynamic_bg_type="particles", dynamic_fps=30, dynamic_quality="high",
                 typewriter_interval=15, tip_interval=15, expired_text="已到期",
                 display_format="decimal", display_format_template="{days}天 {hours}时 {minutes}分"):
        self.project_type = project_type
        self.pomodoro_work = pomodoro_work
        self.pomodoro_break = pomodoro_break
        self.pomodoro_long_break = pomodoro_long_break
        self.pomodoro_cycles = pomodoro_cycles
        self.custom_layout = custom_layout or {}
        self.window_round_radius = window_round_radius
        self.use_neon = use_neon
        self.neon_start = neon_start
        self.neon_end = neon_end
        self.neon_glow = neon_glow
        self.weather_city = weather_city
        self.typewriter_interval = typewriter_interval
        self.tip_interval = tip_interval
        self.expired_text = expired_text
        self.display_format = display_format
        self.display_format_template = display_format_template
        if gradient_start is None:
            gradient_start = "#0a0a1a" if is_system_dark() else "#e0eaf5"
        if gradient_end is None:
            gradient_end = "#1a1040" if is_system_dark() else "#f5f7fa"
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end
        self.dynamic_bg_type = dynamic_bg_type
        self.dynamic_fps = dynamic_fps
        self.dynamic_quality = dynamic_quality
        self.name = name
        self.target_date = target_date or (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.target_time = target_time or "00:00"
        self.show_both = show_both
        self.font_size = font_size
        self.bg_color = bg_color
        self.font_color = font_color
        self.size = size or self.get_default_size(screen_width, screen_height)
        if position is None:
            self.position = (screen_width - self.size[0] - 80, 80)
        else:
            self.position = position
        self.always_on_top = always_on_top
        self.auto_font = auto_font
        self.background_type = background_type
        self.background_image = background_image
        self.window_alpha = window_alpha

    def get_default_size(self, screen_width, screen_height):
        width = max(360, min(460, int(screen_width * 0.24)))
        height = max(220, min(300, int(screen_height * 0.28)))
        return (int(width), int(height))

    def to_dict(self):
        return {
            "name": self.name,
            "target_date": self.target_date,
            "target_time": self.target_time,
            "show_both": self.show_both,
            "font_size": self.font_size,
            "bg_color": self.bg_color,
            "font_color": self.font_color,
            "position": self.position,
            "size": self.size,
            "always_on_top": self.always_on_top,
            "auto_font": self.auto_font,
            "background_type": self.background_type,
            "background_image": self.background_image,
            "window_alpha": self.window_alpha,
            "project_type": self.project_type,
            "pomodoro_work": self.pomodoro_work,
            "pomodoro_break": self.pomodoro_break,
            "pomodoro_long_break": self.pomodoro_long_break,
            "pomodoro_cycles": self.pomodoro_cycles,
            "custom_layout": self.custom_layout,
            "window_round_radius": self.window_round_radius,
            "use_neon": self.use_neon,
            "neon_start": self.neon_start,
            "neon_end": self.neon_end,
            "neon_glow": self.neon_glow,
            "weather_city": self.weather_city,
            "gradient_start": self.gradient_start,
            "gradient_end": self.gradient_end,
            "dynamic_bg_type": self.dynamic_bg_type,
            "dynamic_fps": self.dynamic_fps,
            "dynamic_quality": self.dynamic_quality,
            "typewriter_interval": self.typewriter_interval,
            "tip_interval": self.tip_interval,
            "expired_text": self.expired_text,
            "display_format": self.display_format,
            "display_format_template": self.display_format_template
        }

    @staticmethod
    def from_dict(data, screen_width=1920, screen_height=1080):
        return CountdownProject(
            data.get("name", "新项目"),
            data.get("target_date", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")),
            data.get("target_time", "00:00"),
            data.get("show_both", True),
            data.get("font_size", 28),
            data.get("bg_color", "#0a0a1a"),
            data.get("font_color", "#c0c8f0"),
            data.get("position", None),
            data.get("size", None),
            screen_width,
            screen_height,
            data.get("always_on_top", True),
            data.get("auto_font", True),
            data.get("background_type", "gradient"),
            data.get("background_image", ""),
            data.get("window_alpha", 0.88),
            data.get("project_type", "normal"),
            data.get("pomodoro_work", 25),
            data.get("pomodoro_break", 5),
            data.get("pomodoro_long_break", 15),
            data.get("pomodoro_cycles", 4),
            data.get("custom_layout", {}),
            data.get("window_round_radius", 18),
            data.get("use_neon", True),
            data.get("neon_start", "#00f2fe"),
            data.get("neon_end", "#4facfe"),
            data.get("neon_glow", "#4facfe"),
            data.get("weather_city", ""),
            data.get("gradient_start", None),
            data.get("gradient_end", None),
            data.get("dynamic_bg_type", "particles"),
            data.get("dynamic_fps", 30),
            data.get("dynamic_quality", "high"),
            data.get("typewriter_interval", 15),
            data.get("tip_interval", 15),
            data.get("expired_text", "已到期"),
            data.get("display_format", "decimal"),
            data.get("display_format_template", "{days}天 {hours}时 {minutes}分")
        )

TIPS_DATA = [
    "💡 保持专注，一次只做一件事",
    "🎯 设定小目标，逐步完成大任务",
    "⏰ 每小时休息5分钟，效率更高",
    "📖 学习新技能，每天进步一点点",
    "🧘 深呼吸三次，缓解压力",
    "💪 坚持就是胜利，再难也要走下去",
    "🌟 今天比昨天好，就是成功",
    "🌈 困难是暂时的，成长是永恒的",
    "🔥 热爱你的工作，热爱你的生活",
    "✨ 相信自己，你比想象中更强大",
    "🌱 种一棵树最好的时间是现在",
    "🏃 行动是打败焦虑的最好办法",
    "☕ 适当休息，不是浪费时间",
    "🎉 每一个小成就都值得庆祝",
    "🧹 整理环境，整理心情",
    "📝 写下目标，更容易实现",
    "🌊 顺境不骄，逆境不惧",
    "🔒 专注当下，不要想太多",
    "💛 对自己温柔一点",
    "🍀 好运是准备遇上了机会",
    "🚀 迈出第一步，你就已经超越了犹豫的人",
    "💎 你的时间很宝贵，别浪费在无谓的事情上",
    "🎨 创造力来源于持续的尝试",
    "🏆 成功不是终点，而是一段旅程",
    "📚 每天阅读10分钟，一年就是60小时",
    "💧 坚持微小的改变，终将汇聚成大海",
    "🌸 像花一样，即使无人欣赏也要绽放",
    "🔋 累了就充电，包括身体和心灵",
    "🤝 帮助他人，也是在成就自己",
    "🌙 夜晚的宁静，是最好的思考时刻",
    "☀️ 每一个清晨都是新的开始",
    "🎵 音乐能治愈心灵，听首歌放松一下吧",
    "🍎 健康是1，其他都是后面的0",
    "📅 规划今天，掌控未来",
    "💬 多和家人朋友聊聊天，情感需要滋养",
    "emm.. 不会真的有人会一直盯着看吧",
]

class TipHintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)
        self.tip_text = ""
        self.tip_timer = QTimer(self)
        self.tip_timer.timeout.connect(self.rotate_tip)
        self.tip_timer.start(5500)

    def rotate_tip(self):
        self.tip_text = random.choice(TIPS_DATA)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(QFont("Microsoft YaHei", 9))
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.tip_text)

    def sizeHint(self):
        return QSize(220, 32)

class PomodoroWidget(QWidget):
    def __init__(self, parent=None, work_mins=25, break_mins=5):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.is_running = False
        self.is_rest = False
        self.work_time = work_mins * 60
        self.break_time = break_mins * 60
        self.total_time = self.work_time
        self.time_left = self.total_time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def update_settings(self, work_mins, break_mins):
        self.work_time = work_mins * 60
        self.break_time = break_mins * 60
        if not self.is_running:
            self.total_time = self.break_time if self.is_rest else self.work_time
            self.time_left = self.total_time
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_running:
                self.timer.stop()
                self.is_running = False
            else:
                if self.time_left <= 0:
                    self.is_rest = not self.is_rest
                    self.total_time = self.break_time if self.is_rest else self.work_time
                    self.time_left = self.total_time
                self.timer.start(1000)
                self.is_running = True
            self.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.timer.stop()
            self.is_running = False
            self.is_rest = False
            self.total_time = self.work_time
            self.time_left = self.total_time
            self.update()

    def update_time(self):
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.timer.stop()
            self.is_running = False
            self.is_rest = not self.is_rest
            self.total_time = self.break_time if self.is_rest else self.work_time
            self.time_left = self.total_time
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(5, 5, self.width()-10, self.height()-10)
        painter.setPen(QPen(QColor(255, 255, 255, 50), 4))
        painter.drawEllipse(rect)
        progress = self.time_left / self.total_time
        span_angle = int(progress * 360 * 16)
        color = QColor("#2ecc71") if self.is_rest else QColor("#e74c3c")
        painter.setPen(QPen(color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(rect, 90 * 16, span_angle)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        mins, secs = divmod(self.time_left, 60)
        text = f"{mins:02d}:{secs:02d}"
        if not self.is_running and self.time_left == self.total_time:
            text = "☕ 休息" if self.is_rest else "🍅 专注"
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

class DynamicWallpaperWidget(QWidget):
    def __init__(self, parent=None, wallpaper_type="particles", radius=0):
        super().__init__(parent)
        self.wallpaper_type = wallpaper_type
        self.radius = radius
        self.fps = 30
        self.quality = "high"
        self.mouse_x = -1000
        self.mouse_y = -1000
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.stars = []
        self.clouds = []
        self.particles = []
        self.ripples = []
        self.init_particles()
        self.start_animation()

    def set_mouse_pos(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def trigger_click(self, x, y):
        self.ripples.append({
            "x": x, "y": y, "radius": 5, "max_radius": 150,
            "alpha": 180, "speed": 5
        })
        if self.wallpaper_type == "particles":
            for p in self.particles:
                dx = p["x"] - x
                dy = p["y"] - y
                dist = math.hypot(dx, dy)
                if dist < 250:
                    force = (250 - dist) / 8.0
                    if dist > 0:
                        p["vx"] += (dx / dist) * force
                        p["vy"] += (dy / dist) * force

    def init_particles(self):
        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()
        if self.wallpaper_type == "stars":
            count = 150 if self.quality == "high" else 80
            for _ in range(count):
                self.stars.append({
                    "x": random.randint(0, width), "y": random.randint(0, height),
                    "size": random.uniform(0.8, 2.5), "speed": random.uniform(0.1, 0.8),
                    "brightness": random.randint(80, 255), "dir": random.choice([-1, 1]),
                    "twinkle_speed": random.uniform(3, 10)
                })
        elif self.wallpaper_type == "clouds":
            count = 8 if self.quality == "high" else 4
            for _ in range(count):
                self.clouds.append({
                    "x": random.randint(0, width), "y": random.randint(0, int(height * 0.5)),
                    "size": random.randint(120, 350), "speed": random.uniform(0.3, 1.5),
                    "alpha": random.randint(30, 80)
                })
        elif self.wallpaper_type == "particles":
            count = 60 if self.quality == "high" else 30
            for _ in range(count):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.2, 0.7)
                hue = random.choice([200, 210, 220, 240, 260])
                self.particles.append({
                    "x": random.randint(0, width), "y": random.randint(0, height),
                    "vx": math.cos(angle) * speed, "vy": math.sin(angle) * speed,
                    "base_vx": math.cos(angle) * speed, "base_vy": math.sin(angle) * speed,
                    "size": random.uniform(1.5, 3.5), "hue": hue,
                    "alpha": random.randint(120, 200), "pulse": random.uniform(0, 2 * math.pi)
                })

    def start_animation(self):
        self.timer.start(1000 // self.fps)

    def set_fps(self, fps):
        self.fps = fps
        self.timer.setInterval(1000 // self.fps)

    def set_quality(self, quality):
        self.quality = quality
        self.stars.clear(); self.clouds.clear(); self.particles.clear()
        self.init_particles()

    def update_frame(self):
        width, height = self.width(), self.height()
        if width <= 0 or height <= 0:
            return
        for r in self.ripples[:]:
            r["radius"] += r["speed"]
            r["alpha"] -= 4
            if r["alpha"] <= 0 or r["radius"] >= r["max_radius"]:
                self.ripples.remove(r)
        if self.wallpaper_type == "stars":
            for star in self.stars:
                star["brightness"] += star["dir"] * star["twinkle_speed"]
                if star["brightness"] >= 255: star["brightness"] = 255; star["dir"] = -1
                elif star["brightness"] <= 40: star["brightness"] = 40; star["dir"] = 1
                star["x"] -= star["speed"]
                if star["x"] < -5: star["x"] = width + 5; star["y"] = random.randint(0, height)
        elif self.wallpaper_type == "clouds":
            for cloud in self.clouds:
                cloud["x"] -= cloud["speed"]
                if cloud["x"] + cloud["size"] < 0:
                    cloud["x"] = width + cloud["size"]
                    cloud["y"] = random.randint(0, int(height * 0.5))
        elif self.wallpaper_type == "particles":
            for p in self.particles:
                p["pulse"] += 0.04
                dx = self.mouse_x - p["x"]
                dy = self.mouse_y - p["y"]
                dist = math.hypot(dx, dy)
                if 0 < dist < 180:
                    force = (180 - dist) / 4000.0
                    p["vx"] += dx * force
                    p["vy"] += dy * force
                p["vx"] = p["vx"] * 0.96 + p["base_vx"] * 0.04
                p["vy"] = p["vy"] * 0.96 + p["base_vy"] * 0.04
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                if p["x"] < 0 or p["x"] > width: p["vx"] *= -1; p["base_vx"] *= -1; p["x"] = max(0, min(p["x"], width))
                if p["y"] < 0 or p["y"] > height: p["vy"] *= -1; p["base_vy"] *= -1; p["y"] = max(0, min(p["y"], height))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.radius > 0:
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
            painter.setClipPath(path)
        if self.wallpaper_type == "stars":
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0.0, QColor(6, 6, 24))
            gradient.setColorAt(0.5, QColor(12, 12, 40))
            gradient.setColorAt(1.0, QColor(20, 16, 50))
            painter.fillRect(self.rect(), gradient)
            for star in self.stars:
                alpha = int(star["brightness"])
                color = QColor(200, 220, 255, alpha)
                painter.setBrush(color); painter.setPen(Qt.PenStyle.NoPen)
                s = star["size"]
                if s > 1.8 and alpha > 180:
                    painter.setPen(QPen(QColor(200, 220, 255, alpha // 3), 0.5))
                    painter.drawLine(int(star["x"] - s*2), int(star["y"]), int(star["x"] + s*2), int(star["y"]))
                    painter.drawLine(int(star["x"]), int(star["y"] - s*2), int(star["x"]), int(star["y"] + s*2))
                    painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QRectF(star["x"], star["y"], s, s))
        elif self.wallpaper_type == "clouds":
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0.0, QColor(100, 160, 220))
            gradient.setColorAt(1.0, QColor(180, 210, 240))
            painter.fillRect(self.rect(), gradient)
            for cloud in self.clouds:
                painter.setBrush(QColor(255, 255, 255, cloud.get("alpha", 50)))
                painter.setPen(Qt.PenStyle.NoPen)
                cx, cy, s = cloud["x"], cloud["y"], cloud["size"]
                painter.drawEllipse(QRectF(cx, cy, s, s*0.6))
                painter.drawEllipse(QRectF(cx + s*0.2, cy - s*0.2, s*0.7, s*0.5))
                painter.drawEllipse(QRectF(cx - s*0.15, cy + s*0.1, s*0.6, s*0.4))
        elif self.wallpaper_type == "particles":
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0.0, QColor(8, 8, 28))
            gradient.setColorAt(0.3, QColor(14, 10, 36))
            gradient.setColorAt(0.7, QColor(22, 14, 48))
            gradient.setColorAt(1.0, QColor(10, 8, 30))
            painter.fillRect(self.rect(), gradient)
            connect_dist = 70
            for i, p1 in enumerate(self.particles):
                for j in range(i+1, len(self.particles)):
                    p2 = self.particles[j]
                    dist = math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])
                    if dist < connect_dist:
                        alpha = int((1 - dist/connect_dist) * 25)
                        line_color = QColor(100, 160, 255, alpha)
                        painter.setPen(QPen(line_color, 0.5))
                        painter.drawLine(int(p1["x"]), int(p1["y"]), int(p2["x"]), int(p2["y"]))
                painter.setPen(Qt.PenStyle.NoPen)
            for p in self.particles:
                pulse_size = p["size"] + math.sin(p["pulse"]) * 0.6
                core_color = QColor.fromHsv(p["hue"], 150, 255, p["alpha"])
                painter.setBrush(core_color)
                painter.drawEllipse(QRectF(p["x"] - pulse_size/2, p["y"] - pulse_size/2, pulse_size, pulse_size))
        for r in self.ripples:
            pen = QPen(QColor(100, 180, 255, int(r["alpha"])), 1.5)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(r["x"], r["y"]), r["radius"], r["radius"])

class FullscreenSettingsPanel(QWidget):
    def __init__(self, parent=None, window=None):
        super().__init__(parent)
        self.window = window
        self.setFixedWidth(300)
        self.setObjectName("FullscreenPanel")
        self.setStyleSheet("""
            #FullscreenPanel {
                background-color: rgba(25, 25, 30, 220);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 40);
            }
            QLabel { color: #E0E0E0; font-weight: bold; font-family: 'Microsoft YaHei'; }
            QSlider::groove:horizontal { border-radius: 4px; height: 8px; background: #3A3A3A; }
            QSlider::handle:horizontal { background: #3498db; width: 16px; height: 16px; margin: -4px 0; border-radius: 8px; }
            QComboBox { background-color: #3A3A3A; color: white; border-radius: 4px; padding: 4px; }
            QPushButton { background-color: #e74c3c; color: white; border-radius: 6px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #c0392b; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel(tr("window_alpha") + ":"))
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setRange(10, 100)
        self.alpha_slider.setValue(int(window.project.window_alpha * 100))
        self.alpha_slider.valueChanged.connect(self.on_alpha_changed)
        alpha_layout.addWidget(self.alpha_slider)
        layout.addLayout(alpha_layout)
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel(tr("dynamic_wallpaper") + ":"))
        self.combo_type = QComboBox()
        self.combo_type.addItem(tr("disable"), "none")
        for key, name in self.window.master.dynamic_bg_registry.items():
            self.combo_type.addItem(name, key)
        curr_bg = self.window.project.dynamic_bg_type if self.window.bg_dynamic_widget and self.window.bg_dynamic_widget.isVisible() else "none"
        idx = self.combo_type.findData(curr_bg)
        if idx >= 0:
            self.combo_type.setCurrentIndex(idx)
        self.combo_type.currentIndexChanged.connect(self.on_wallpaper_type_changed)
        type_layout.addWidget(self.combo_type)
        layout.addLayout(type_layout)
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel(tr("quality") + ":"))
        self.combo_quality = QComboBox()
        self.combo_quality.addItems([tr("high"), tr("medium"), tr("low")])
        self.combo_quality.setCurrentIndex(0 if self.window.project.dynamic_quality == "high" else (1 if self.window.project.dynamic_quality == "medium" else 2))
        self.combo_quality.currentIndexChanged.connect(self.on_quality_changed)
        quality_layout.addWidget(self.combo_quality)
        layout.addLayout(quality_layout)
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel(tr("fps") + ":"))
        self.combo_fps = QComboBox()
        self.combo_fps.addItems(["30 FPS", "60 FPS", "120 FPS"])
        self.combo_fps.setCurrentText(f"{self.window.project.dynamic_fps} FPS")
        self.combo_fps.currentIndexChanged.connect(self.on_fps_changed)
        fps_layout.addWidget(self.combo_fps)
        layout.addLayout(fps_layout)
        btn_exit = QPushButton(tr("exit_fullscreen"))
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.clicked.connect(self.window.toggle_fullscreen)
        layout.addWidget(btn_exit)
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(5000)
        self.hide_timer.timeout.connect(self.fade_out)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(600)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.hide_timer.start()

    def enterEvent(self, event):
        self.hide_timer.stop()
        self.anim.stop()
        self.opacity_effect.setOpacity(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hide_timer.start()
        super().leaveEvent(event)

    def fade_out(self):
        self.anim.setStartValue(self.opacity_effect.opacity())
        self.anim.setEndValue(0.0)
        self.anim.start()

    def on_alpha_changed(self, value):
        self.window.set_alpha(value / 100.0)

    def on_wallpaper_type_changed(self, index):
        bg_type = self.combo_type.currentData()
        self.window.temp_fullscreen_bg = bg_type
        self.window.setup_dynamic_bg()

    def on_quality_changed(self, index):
        quality_map = {0: "high", 1: "medium", 2: "low"}
        quality = quality_map[index]
        self.window.project.dynamic_quality = quality
        if self.window.bg_dynamic_widget and hasattr(self.window.bg_dynamic_widget, 'set_quality'):
            self.window.bg_dynamic_widget.set_quality(quality)

    def on_fps_changed(self, index):
        fps = int(self.combo_fps.currentText().split()[0])
        self.window.project.dynamic_fps = fps
        if self.window.bg_dynamic_widget and hasattr(self.window.bg_dynamic_widget, 'set_fps'):
            self.window.bg_dynamic_widget.set_fps(fps)

# CountdownWindow 主悬浮窗
class CountdownWindow(QWidget):
    def __init__(self, master, project, index):
        super().__init__()
        self.master = master
        self.project = project
        self.index = index
        dpi_scale = QApplication.primaryScreen().logicalDotsPerInch() / 96.0
        self.edge_margin = int(12 * dpi_scale)

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self.project.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.project.window_alpha)
        self.setMouseTracking(True)

        x, y = self.project.position
        width, height = self.project.size
        screen_geo = QApplication.primaryScreen().availableGeometry()
        x = max(screen_geo.left() - width + 50, min(x, screen_geo.right() - 50))
        y = max(screen_geo.top() - height + 50, min(y, screen_geo.bottom() - 50))
        self.setGeometry(int(x), int(y), int(width), int(height))
        self.setMinimumSize(250, 150)

        if self.project.background_type == "color" and self.project.window_alpha < 1.0:
            if self.project.window_round_radius == 0:
                apply_modern_window_effect(int(self.winId()), effect_type="acrylic", is_dark=True, enable=True)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setStyleSheet("background: transparent;")

        self.bg_image = None
        self.bg_pixmap = None
        self.bg_movie = None
        self.bg_dynamic_widget = None
        self.is_pomodoro = False
        self.pomodoro_end_time = None
        self.is_fullscreen = False
        self.old_geometry = None
        self.old_flags = None
        self.wallpaper_widget = None
        self.fullscreen_panel = None
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        self.resize_data = {"resizing": False, "edge": None, "start_pos": None, "start_geo": None}

        # 视差相关
        self.target_px = 0.0
        self.target_py = 0.0
        self.current_px = 0.0
        self.current_py = 0.0
        self.enable_parallax = True
        self.parallax_intensity = 6
        self._base_positions = {}  # elem_id -> (base_x, base_y)
        self._parallax_depth = {
            "name": 0.3, "static_text": 0.4, "countdown": 0.7,
            "weather": 0.5, "pomodoro": 0.5, "tip": 0.9, "poem": 0.8
        }

        self.parallax_timer = QTimer(self)
        self.parallax_timer.timeout.connect(self.update_parallax)
        self.parallax_timer.start(16)

        self._widget_sizes = {}
        self._last_window_size = (self.width(), self.height())

        self.init_ui()
        self.init_menu()
        self.setup_dynamic_bg()
        if not self.project.custom_layout:
            self._init_default_layout()

        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_config_now)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_countdown)
        self.update_timer.start(60000)
        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self.update_ticking_countdown)
        self.tick_timer.start(2000)
        self.typewriter_timer = QTimer(self)
        self.typewriter_timer.timeout.connect(self.start_typewriter_animation)
        self.typewriter_timer.start(self.project.typewriter_interval * 60000)
        self.tip_timer = QTimer(self)
        self.tip_timer.timeout.connect(self.start_tip_animation)
        tip_interval = self.project.tip_interval if hasattr(self.project, 'tip_interval') else self.project.typewriter_interval
        self.tip_timer.start(tip_interval * 60000)
        QTimer.singleShot(1200, self.start_typewriter_animation)
        QTimer.singleShot(1800, self.start_tip_animation)

        if self.project.background_type == "image" and self.project.background_image:
            QTimer.singleShot(100, self.load_background_image)

        self.update_countdown()
        self.apply_custom_layout(skip_style=False)
        self.master.plugin_manager.trigger_event("on_window_create", self, project)

    def _init_default_layout(self):
        is_dark = self.master.theme.is_dark if hasattr(self.master, 'theme') else is_system_dark()
        if is_dark:
            name_color = "#FFFFFF"
            name_bg = "rgba(0,0,0,0.25)"
            static_color = "#E0E0E0"
            countdown_color = "#FFFFFF"
            countdown_bg = "rgba(0,0,0,0.35)"
            stroke_color = "rgba(255,255,255,0.3)"
        else:
            name_color = "#1E1E1E"
            name_bg = "rgba(255,255,255,0.7)"
            static_color = "#333333"
            countdown_color = "#1E1E1E"
            countdown_bg = "rgba(255,255,255,0.8)"
            stroke_color = "rgba(0,0,0,0.1)"

        layout = {}
        layout["name"] = {
            "visible": True, "x": 0.5, "y": 0.10,
            "font_size": 16, "color": name_color, "opacity": 1.0,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 8,
            "bg_color": name_bg, "bg_radius": 12,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["static_text"] = {
            "visible": True, "x": 0.5, "y": 0.28,
            "font_size": 13, "color": static_color, "opacity": 0.9,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 1, "shadow_blur": 6,
            "bg_color": "transparent", "bg_radius": 0,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["countdown"] = {
            "visible": True, "x": 0.5, "y": 0.55,
            "font_size": 32, "color": countdown_color, "opacity": 1.0,
            "stroke_color": stroke_color, "stroke_width": 0.8,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 3, "shadow_blur": 12,
            "bg_color": countdown_bg, "bg_radius": 15,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        self.project.custom_layout = layout

    def init_ui(self):
        self.project_label = QLabel(self.project.name, self)
        self.project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label = RollingNumberLabel("0.000 天", self)
        self.countdown_label.set_neon_config(self.project.use_neon, self.project.neon_start,
                                             self.project.neon_end, self.project.neon_glow, self.project.font_color)
        self.static_label = QLabel("", self)
        self.static_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.static_label.setWordWrap(True)
        static_shadow = QGraphicsDropShadowEffect(self)
        static_shadow.setBlurRadius(6)
        static_shadow.setColor(QColor(0, 0, 0, 150))
        static_shadow.setOffset(1, 1)
        self.static_label.setGraphicsEffect(static_shadow)

        self.poem_label = TypewriterLabel(self, speed=60)
        self.poem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.weather_label = QLabel("⏳ 获取天气...", self)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setStyleSheet("color: white; font-weight: bold;")
        self.weather_label.setGraphicsEffect(QGraphicsDropShadowEffect(self))
        self.weather_label.mousePressEvent = self.show_weather_forecast

        self.weather_fetcher = WeatherFetcher(
            api_provider=getattr(self.master, 'weather_provider', 'wttr_in'),
            custom_url_template=getattr(self.master, 'custom_weather_url', ''))
        self.weather_fetcher.weather_updated.connect(self.weather_label.setText)
        self.weather_fetcher.weather_updated.connect(lambda _: self.apply_custom_layout(skip_style=False))
        self.weather_label.setVisible(False)

        self.pomodoro_widget = PomodoroWidget(self, self.project.pomodoro_work, self.project.pomodoro_break)
        self.pomodoro_widget.setVisible(False)
        self.tip_hint_widget = TypewriterLabel(self, speed=60)
        self.tip_hint_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_hint_widget.setVisible(False)   # 初始隐藏，由布局控制显示
        self.drag_hint_label = QLabel(tr("right_click_hint"), self)
        self.drag_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_hint_label.hide()

        self.custom_widgets = {}
        for key, cfg in self.project.custom_layout.items():
            if key.startswith("custom_text_"):
                lbl = QLabel(cfg.get("text", ""), self)
                font = QFont(cfg.get("font_family", "Microsoft YaHei"), cfg.get("font_size", 12))
                lbl.setFont(font)
                lbl.setStyleSheet(f"color: {cfg.get('color', '#FFFFFF')}; background: transparent;")
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(8)
                shadow.setColor(QColor(0, 0, 0, 180))
                shadow.setOffset(1, 1)
                lbl.setGraphicsEffect(shadow)
                lbl.setVisible(False)
                self.custom_widgets[key] = lbl
            elif key.startswith("custom_image_"):
                lbl = QLabel(self)
                lbl.setVisible(False)
                self.custom_widgets[key] = lbl

        for id_name, info in getattr(self.master, 'custom_widget_registry', {}).items():
            try:
                widget_instance = info["class"](self)
                self.custom_widgets[id_name] = widget_instance
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(8)
                shadow.setColor(QColor(0, 0, 0, 180))
                shadow.setOffset(1, 1)
                widget_instance.setGraphicsEffect(shadow)
            except Exception as e:
                log_message(f"加载自定义控件 {id_name} 失败: {e}", "ERROR")

        for label in [self.project_label, self.drag_hint_label]:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 0, 0, 180))
            shadow.setOffset(1, 1)
            label.setGraphicsEffect(shadow)

        self.refresh_styles()

    def show_weather_forecast(self, event):
        if self.weather_fetcher.lat and self.weather_fetcher.lon:
            dlg = WeatherForecastDialog(self.weather_fetcher.lat, self.weather_fetcher.lon,
                                        self.weather_fetcher.city_name, self)
            dlg.exec()

    def refresh_styles(self):
        font_family = self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei"
        def make_font(size, bold=False, italic=False):
            f = QFont(font_family, size)
            f.setBold(bold)
            f.setItalic(italic)
            f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            return f
        self.project_label.setFont(make_font(12, bold=True))
        self.project_label.setStyleSheet(f"color: {self.project.font_color};")
        self.countdown_label.setFont(make_font(self.project.font_size, bold=True))
        self.countdown_label.set_neon_config(self.project.use_neon, self.project.neon_start,
                                             self.project.neon_end, self.project.neon_glow, self.project.font_color)
        self.countdown_label.set_display_format(
            getattr(self.project, 'display_format', 'decimal'),
            getattr(self.project, 'display_format_template', '{days}天 {hours}时 {minutes}分'))
        self.poem_label.setFont(make_font(10))
        self.poem_label.setStyleSheet(f"color: {self.project.font_color};")
        self.weather_label.setFont(make_font(10, bold=True))
        self.drag_hint_label.setFont(make_font(9, italic=True))

    def init_menu(self):
        self.menu = QMenu(self)
        cm = get_theme_colors(self.master.theme)
        self.menu.setStyleSheet(f"""
            QMenu {{ background-color: {cm['panel_bg']}; color: {cm['text_color']}; border: 1px solid {cm['border_color']}; border-radius: 5px; }}
            QMenu::item:selected {{ background-color: {cm['accent']}; color: {cm['selected_text']}; }}
        """)
        act_settings = QAction(tr("settings_title"), self)
        act_settings.triggered.connect(self.master.open_settings)
        self.menu.addAction(act_settings)

        self.act_pin = QAction("取消置顶" if self.project.always_on_top else "置顶窗口", self)
        self.act_pin.triggered.connect(self.toggle_topmost)
        self.menu.addAction(self.act_pin)

        act_fs = QAction("全屏" if CURRENT_LANG == LANG_CHINESE else "Fullscreen", self)
        act_fs.triggered.connect(self.toggle_fullscreen)
        self.menu.addAction(act_fs)

        act_close = QAction(tr("close"), self)
        act_close.triggered.connect(self.close_window)
        self.menu.addAction(act_close)

        act_quit = QAction("退出应用" if CURRENT_LANG == LANG_CHINESE else "Quit", self)
        act_quit.triggered.connect(self.master.quit_app)
        self.menu.addAction(act_quit)

    def contextMenuEvent(self, event):
        if self.is_fullscreen:
            self.menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else QCursor.pos()
        self.menu.exec(pos)

    def mousePressEvent(self, event):
        if self.is_fullscreen:
            if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'trigger_click'):
                self.bg_dynamic_widget.trigger_click(event.pos().x(), event.pos().y())
            return
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            w, h = self.width(), self.height()
            edge = ""
            if pos.y() <= self.edge_margin:
                edge += "top"
            elif pos.y() >= h - self.edge_margin:
                edge += "bottom"
            if pos.x() <= self.edge_margin:
                edge += "left"
            elif pos.x() >= w - self.edge_margin:
                edge += "right"
            if edge:
                self.resize_data = {"resizing": True, "edge": edge, "start_pos": event.globalPosition().toPoint(), "start_geo": self.geometry()}
            else:
                self.drag_data = {"dragging": True, "x": event.globalPosition().x(), "y": event.globalPosition().y(), "win_x": self.x(), "win_y": self.y()}
                self.drag_hint_label.show()
                self.drag_hint_label.adjustSize()
                dw, dh = self.drag_hint_label.width(), self.drag_hint_label.height()
                self.drag_hint_label.move((self.width() - dw) // 2, self.height() - dh - 10)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'set_mouse_pos'):
            self.bg_dynamic_widget.set_mouse_pos(pos.x(), pos.y())
        if self.is_fullscreen:
            return
        w, h = self.width(), self.height()
        if not self.drag_data["dragging"] and not self.resize_data["resizing"]:
            cursor = Qt.CursorShape.ArrowCursor
            if pos.x() <= self.edge_margin and pos.y() <= self.edge_margin:
                cursor = Qt.CursorShape.SizeFDiagCursor
            elif pos.x() >= w - self.edge_margin and pos.y() >= h - self.edge_margin:
                cursor = Qt.CursorShape.SizeFDiagCursor
            elif pos.x() >= w - self.edge_margin and pos.y() <= self.edge_margin:
                cursor = Qt.CursorShape.SizeBDiagCursor
            elif pos.x() <= self.edge_margin and pos.y() >= h - self.edge_margin:
                cursor = Qt.CursorShape.SizeBDiagCursor
            elif pos.x() <= self.edge_margin or pos.x() >= w - self.edge_margin:
                cursor = Qt.CursorShape.SizeHorCursor
            elif pos.y() <= self.edge_margin or pos.y() >= h - self.edge_margin:
                cursor = Qt.CursorShape.SizeVerCursor
            self.setCursor(cursor)

            center_x, center_y = w / 2, h / 2
            dx = (pos.x() - center_x) / center_x
            dy = (pos.y() - center_y) / center_y
            self.target_px = -dx * self.parallax_intensity
            self.target_py = -dy * self.parallax_intensity
            return

        if self.resize_data["resizing"]:
            dx = int(event.globalPosition().x() - self.resize_data["start_pos"].x())
            dy = int(event.globalPosition().y() - self.resize_data["start_pos"].y())
            geo = self.resize_data["start_geo"]
            new_geo = QRect(geo)
            edge = self.resize_data["edge"]
            if "left" in edge:
                new_geo.setLeft(min(geo.left() + dx, geo.right() - 250))
            elif "right" in edge:
                new_geo.setRight(max(geo.right() + dx, geo.left() + 250))
            if "top" in edge:
                new_geo.setTop(min(geo.top() + dy, geo.bottom() - 150))
            elif "bottom" in edge:
                new_geo.setBottom(max(geo.bottom() + dy, geo.top() + 150))
            self.setGeometry(new_geo)
        elif self.drag_data["dragging"]:
            dx = event.globalPosition().x() - self.drag_data["x"]
            dy = event.globalPosition().y() - self.drag_data["y"]
            new_x = int(self.drag_data["win_x"] + dx)
            new_y = int(self.drag_data["win_y"] + dy)
            screen_geo = QApplication.primaryScreen().availableGeometry()
            if new_x < screen_geo.left() - w + 50:
                new_x = screen_geo.left() - w + 50
            elif new_x > screen_geo.right() - 50:
                new_x = screen_geo.right() - 50
            if new_y < screen_geo.top() - h + 50:
                new_y = screen_geo.top() - h + 50
            elif new_y > screen_geo.bottom() - 50:
                new_y = screen_geo.bottom() - 50
            self.move(new_x, new_y)

    def mouseReleaseEvent(self, event):
        if self.is_fullscreen:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            if self.resize_data["resizing"]:
                self.resize_data["resizing"] = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.save_config_later()
            elif self.drag_data["dragging"]:
                self.drag_data["dragging"] = False
                self.drag_hint_label.hide()
                self.save_config_later()

    def leaveEvent(self, event):
        self.target_px = 0.0
        self.target_py = 0.0
        self.drag_data["dragging"] = False
        self.resize_data["resizing"] = False
        self.drag_hint_label.hide()
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'set_mouse_pos'):
            self.bg_dynamic_widget.set_mouse_pos(-1000, -1000)
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.is_fullscreen:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.master.open_settings()

    def setup_dynamic_bg(self):
        if self.bg_dynamic_widget:
            self.bg_dynamic_widget.deleteLater()
            self.bg_dynamic_widget = None
        bg_type = "none"
        if self.is_fullscreen:
            bg_type = getattr(self, 'temp_fullscreen_bg', self.project.dynamic_bg_type)
        elif self.project.background_type == "dynamic":
            bg_type = self.project.dynamic_bg_type
        if bg_type != "none":
            if bg_type in self.master.dynamic_bg_classes:
                WidgetClass = self.master.dynamic_bg_classes[bg_type]
                self.bg_dynamic_widget = WidgetClass(self)
            else:
                radius = self.project.window_round_radius if not self.is_fullscreen else 0
                self.bg_dynamic_widget = DynamicWallpaperWidget(self, wallpaper_type=bg_type, radius=radius)
                self.bg_dynamic_widget.set_fps(self.project.dynamic_fps)
                self.bg_dynamic_widget.set_quality(self.project.dynamic_quality)
            if self.bg_dynamic_widget:
                self.bg_dynamic_widget.setGeometry(self.rect())
                self.bg_dynamic_widget.lower()
                self.bg_dynamic_widget.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        path = QPainterPath()
        radius = self.project.window_round_radius if not self.is_fullscreen else 0
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        painter.setClipPath(path)

        if self.project.background_type == "color":
            bg_color = QColor(self.project.bg_color)
            bg_color.setAlpha(int(self.project.window_alpha * 255))
            painter.fillPath(path, bg_color)
            painter.setPen(QPen(QColor(255, 255, 255, 60), 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
        elif self.project.background_type == "gradient":
            grad = QLinearGradient(0, 0, self.width(), self.height())
            grad.setColorAt(0.0, QColor(self.project.gradient_start))
            grad.setColorAt(1.0, QColor(self.project.gradient_end))
            painter.fillPath(path, grad)
            painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
        elif self.project.background_type == "image" and self.bg_movie:
            current_frame = self.bg_movie.currentPixmap()
            if not current_frame.isNull():
                painter.drawPixmap(self.rect(), current_frame.scaled(
                    self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
        elif self.project.background_type == "image" and self.bg_pixmap:
            painter.drawPixmap(self.rect(), self.bg_pixmap)

    def load_background_image(self):
        try:
            data_dir = resource_path("data")
            user_dir = os.path.join(data_dir, "user")
            image_path = os.path.join(user_dir, self.project.background_image)
            if not os.path.exists(image_path):
                image_path = os.path.join(data_dir, self.project.background_image)
            if os.path.exists(image_path):
                if image_path.lower().endswith('.gif'):
                    if self.bg_movie:
                        self.bg_movie.stop()
                    self.bg_movie = QMovie(image_path)
                    self.bg_movie.frameChanged.connect(self.update)
                    self.bg_movie.start()
                    self.bg_pixmap = None
                else:
                    if self.bg_movie:
                        self.bg_movie.stop()
                        self.bg_movie = None
                    from PIL import Image
                    self.bg_image = Image.open(image_path)
                    self.update_background_image()
            else:
                self.project.background_type = "color"
                self.update()
        except Exception as e:
            log_message(f"加载背景图片失败: {e}", "ERROR")
            self.project.background_type = "color"
            self.update()

    def update_background_image(self):
        if not self.bg_image:
            return
        try:
            width, height = self.width(), self.height()
            if width <= 1 or height <= 1:
                if not hasattr(self, 'bg_update_timer'):
                    self.bg_update_timer = QTimer(self)
                    self.bg_update_timer.setSingleShot(True)
                    self.bg_update_timer.timeout.connect(self.update_background_image)
                self.bg_update_timer.start(100)
                return
            from PIL import Image, ImageEnhance
            resized_img = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
            brightness = self.master.theme.window_brightness
            saturation = self.master.theme.window_saturation
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(resized_img)
                resized_img = enhancer.enhance(brightness)
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(resized_img)
                resized_img = enhancer.enhance(saturation)
            resized_img = resized_img.convert("RGBA")
            data = resized_img.tobytes("raw", "RGBA")
            qim = QImage(data, resized_img.width, resized_img.height, QImage.Format.Format_RGBA8888)
            self.bg_pixmap = QPixmap.fromImage(qim)
            self.update()
        except Exception as e:
            log_message(f"更新背景图片失败: {e}", "ERROR")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._last_window_size = (self.width(), self.height())
        self.apply_custom_layout(skip_style=False)
        if self.project.background_type == "image":
            if not hasattr(self, 'bg_update_timer'):
                self.bg_update_timer = QTimer(self)
                self.bg_update_timer.setSingleShot(True)
                self.bg_update_timer.timeout.connect(self.update_background_image)
            self.bg_update_timer.start(100)
        if self.bg_dynamic_widget:
            self.bg_dynamic_widget.setGeometry(self.rect())
        if self.project.auto_font:
            self.adjust_font_size()
        self.save_config_later()

    def hideEvent(self, event):
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'timer'):
            self.bg_dynamic_widget.timer.stop()
        super().hideEvent(event)

    def showEvent(self, event):
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'timer'):
            self.bg_dynamic_widget.timer.start()
        super().showEvent(event)

    def apply_custom_layout(self, skip_style=False):
        layout = self.project.custom_layout
        if not layout:
            self._init_default_layout()
            layout = self.project.custom_layout

        win_w, win_h = self.width(), self.height()
        if win_w <= 0 or win_h <= 0:
            return

        if not skip_style:
            for w in [self.weather_label, self.pomodoro_widget, self.tip_hint_widget, self.poem_label]:
                if w:
                    w.setVisible(False)

        standard = {
            "name": self.project_label,
            "static_text": self.static_label,
            "countdown": self.countdown_label,
            "weather": self.weather_label,
            "pomodoro": self.pomodoro_widget,
            "tip": self.tip_hint_widget,
            "poem": self.poem_label
        }

        days, hours, minutes, work_days, work_days_float, holiday_name = calculate_days(
            self.project.target_date, self.project.target_time
        )
        default_static = f"剩余工作日: {work_days} 天" if work_days > 0 else ""

        offset_x = 0.0
        offset_y = 0.0

        for elem_id, cfg in layout.items():
            visible = cfg.get("visible", True)
            w = standard.get(elem_id) or self.custom_widgets.get(elem_id)
            if not visible:
                if w:
                    w.setVisible(False)
                continue
            if w is None:
                if cfg.get("type") == "custom_text":
                    w = self._get_or_create_custom_text(elem_id, cfg)
                elif cfg.get("type") == "custom_image":
                    w = self._get_or_create_custom_image(elem_id, cfg)
                else:
                    w = self.custom_widgets.get(elem_id)
                if w is None:
                    continue

            w.setVisible(True)

            if not skip_style:
                if elem_id == "static_text":
                    w.setText(cfg.get("text", "") or default_static)
                elif elem_id == "name":
                    w.setText(self.project.name)

                font_family = cfg.get("font_family") or (self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei")
                font = QFont(font_family, cfg.get("font_size", 14))
                font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
                w.setFont(font)

                color = cfg.get("color", "#FFFFFF")
                bg = cfg.get("bg_color", "transparent")
                radius = cfg.get("bg_radius", 0)
                stroke_w = cfg.get("stroke_width", 0)
                stroke_color = cfg.get("stroke_color", "transparent")
                border = f"border: {stroke_w}px solid {stroke_color};" if stroke_w > 0 and stroke_color != "transparent" else "border: none;"
                stylesheet = f"color: {color}; font-size: {cfg.get('font_size', 14)}pt; background-color: {bg}; border-radius: {radius}px; {border}"
                if isinstance(w, QLabel):
                    w.setStyleSheet(stylesheet)
                elif isinstance(w, TypewriterLabel):
                    w._text_color_hex = color
                    w._opacity = cfg.get("opacity", 1.0)

                if not isinstance(w, TypewriterLabel):
                    opacity_eff = w.graphicsEffect()
                    if not isinstance(opacity_eff, QGraphicsOpacityEffect):
                        opacity_eff = QGraphicsOpacityEffect(w)
                        w.setGraphicsEffect(opacity_eff)
                    opacity_eff.setOpacity(cfg.get("opacity", 1.0))

                align_map_h = {"左": Qt.AlignmentFlag.AlignLeft, "中": Qt.AlignmentFlag.AlignCenter, "右": Qt.AlignmentFlag.AlignRight}
                align_map_v = {"上": Qt.AlignmentFlag.AlignTop, "中": Qt.AlignmentFlag.AlignCenter, "下": Qt.AlignmentFlag.AlignBottom}
                h = align_map_h.get(cfg.get("alignment_h", "中"), Qt.AlignmentFlag.AlignCenter)
                v = align_map_v.get(cfg.get("alignment_v", "中"), Qt.AlignmentFlag.AlignCenter)
                if isinstance(w, QLabel):
                    w.setAlignment(h | v)

            # 获取尺寸
            if skip_style and elem_id in self._widget_sizes:
                cw, ch = self._widget_sizes[elem_id]
            else:
                custom_w = cfg.get("custom_width")
                custom_h = cfg.get("custom_height")
                if custom_w is not None and custom_h is not None:
                    cw, ch = int(custom_w), int(custom_h)
                    if not skip_style:
                        w.resize(cw, ch)
                else:
                    if not skip_style:
                        w.adjustSize()
                    cw, ch = w.width(), w.height()
                self._widget_sizes[elem_id] = (cw, ch)

            pct_x = cfg.get("x", 0.5)
            pct_y = cfg.get("y", 0.5)

            if isinstance(w, TypewriterLabel):
                if isinstance(w.graphicsEffect(), QGraphicsOpacityEffect):
                    w.setGraphicsEffect(None)
                if not skip_style:
                    target_width = int(win_w * 0.9)
                    target_height = w.heightForWidth(target_width)
                    target_height = max(target_height, 40)
                    w.resize(target_width, target_height)
                    cw, ch = target_width, target_height
                    self._widget_sizes[elem_id] = (cw, ch)
                else:
                    if elem_id in self._widget_sizes:
                        cw, ch = self._widget_sizes[elem_id]
                    else:
                        cw, ch = int(win_w * 0.9), 40
                        self._widget_sizes[elem_id] = (cw, ch)
                x = (win_w - cw) // 2
                y = int(pct_y * win_h) - ch // 2
                w.move(x, y)
                self._base_positions[elem_id] = (x, y)
                continue

            x = int(pct_x * win_w) - cw // 2
            y = int(pct_y * win_h) - ch // 2
            w.move(x, y)
            self._base_positions[elem_id] = (x, y)

        if not skip_style and self.drag_hint_label.isVisible():
            self.drag_hint_label.adjustSize()
            dw, dh = self.drag_hint_label.width(), self.drag_hint_label.height()
            self.drag_hint_label.move((self.width() - dw) // 2, self.height() - dh - 10)

    def _get_or_create_custom_text(self, elem_id, config):
        if not hasattr(self, '_custom_widgets'):
            self._custom_widgets = {}
        if elem_id not in self._custom_widgets:
            label = QLabel(config.get("text", ""), self)
            label.setObjectName(f"custom_{elem_id}")
            label.setWordWrap(True)
            self._custom_widgets[elem_id] = label
        widget = self._custom_widgets[elem_id]
        widget.setText(config.get("text", ""))
        return widget

    def _get_or_create_custom_image(self, elem_id, config):
        if not hasattr(self, '_custom_widgets'):
            self._custom_widgets = {}
        if elem_id not in self._custom_widgets:
            label = QLabel(self)
            label.setObjectName(f"custom_{elem_id}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._custom_widgets[elem_id] = label

        widget = self._custom_widgets[elem_id]
        image_path = config.get("image_path", "")
        if not image_path:
            widget.setText("🖼️ 无图片")
            return widget

        full_path = None
        if os.path.isabs(image_path) and os.path.exists(image_path):
            full_path = image_path
        else:
            if hasattr(self.master, 'user_dir') and self.master.user_dir:
                candidate = os.path.join(self.master.user_dir, image_path)
                if os.path.exists(candidate):
                    full_path = candidate
            if not full_path:
                data_dir = resource_path("data")
                candidate = os.path.join(data_dir, image_path)
                if os.path.exists(candidate):
                    full_path = candidate

        if full_path and os.path.exists(full_path):
            if full_path.lower().endswith('.gif'):
                if not hasattr(widget, '_movie') or widget._movie is None:
                    movie = QMovie(full_path)
                    widget.setMovie(movie)
                    movie.start()
                    widget._movie = movie
                widget.setText("")
            else:
                pixmap = QPixmap(full_path)
                if not pixmap.isNull():
                    max_w = min(200, self.width() // 3)
                    max_h = min(150, self.height() // 3)
                    scaled = pixmap.scaled(max_w, max_h,
                                           Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                    widget.setPixmap(scaled)
                else:
                    widget.setText("❌ 图片损坏")
        else:
            widget.setText(f"❌ 文件不存在: {os.path.basename(image_path)}")

        return widget

    def adjust_font_size(self):
        if not self.project.auto_font:
            return
        w, h = self.width(), self.height()
        base_size = 12
        width_factor = max(0, (w - 200) / 100 * 3)
        height_factor = max(0, (h - 80) / 50 * 2)
        new_size = int(base_size + min(width_factor, height_factor))
        new_size = max(12, min(64, new_size))
        font = self.countdown_label.font()
        font.setPointSize(new_size)
        self.countdown_label.setFont(font)
        self.apply_custom_layout(skip_style=False)

    def update_parallax(self):
        old_px, old_py = self.current_px, self.current_py
        if not self.enable_parallax:
            self.current_px *= 0.85
            self.current_py *= 0.85
            if abs(self.current_px) < 0.1:
                self.current_px = 0.0
            if abs(self.current_py) < 0.1:
                self.current_py = 0.0
        else:
            self.current_px += (self.target_px - self.current_px) * 0.18
            self.current_py += (self.target_py - self.current_py) * 0.18
        diff_x = abs(self.current_px - old_px)
        diff_y = abs(self.current_py - old_py)
        if diff_x < 0.1 and diff_y < 0.1:
            return
        layout = self.project.custom_layout
        if not layout:
            return
        standard = {
            "name": self.project_label, "static_text": self.static_label,
            "countdown": self.countdown_label, "weather": self.weather_label,
            "pomodoro": self.pomodoro_widget, "tip": self.tip_hint_widget, "poem": self.poem_label
        }
        for elem_id, base_pos in self._base_positions.items():
            cfg = layout.get(elem_id)
            if not cfg or not cfg.get("visible", True):
                continue
            w = standard.get(elem_id) or self.custom_widgets.get(elem_id)
            if not w or not w.isVisible():
                continue
            depth = self._parallax_depth.get(elem_id, 0.5)
            bx, by = base_pos
            new_x = int(bx + self.current_px * depth)
            new_y = int(by + self.current_py * depth)
            if new_x != w.x() or new_y != w.y():
                w.move(new_x, new_y)

    def update_countdown(self):
        if self.is_pomodoro and self.pomodoro_end_time:
            diff = self.pomodoro_end_time - datetime.now()
            if diff.total_seconds() <= 0:
                self.static_label.setText("🎉 专注完成！")
                self.is_pomodoro = False
            else:
                mins, secs = divmod(int(diff.total_seconds()), 60)
                self.static_label.setText(f"专注倒计时 {mins:02d}:{secs:02d}")
            return

        days, hours, minutes, work_days, work_days_float, holiday_name = calculate_days(
            self.project.target_date, self.project.target_time
        )
        if days == 0 and hours == 0 and minutes == 0:
            static_text = "已到期"
        elif days == 0 and self.project.target_time != "00:00":
            static_text = "今日倒计时"
        elif self.project.show_both:
            holiday_text = f"\n🎉 {holiday_name}" if holiday_name else ""
            static_text = f"剩余工作日: {work_days}{holiday_text}"
        else:
            static_text = "倒计时"
        self.static_label.setText(static_text)
        self.static_label.setStyleSheet(f"color: {self.project.font_color};")
        self.project_label.setText(self.project.name)

    def update_ticking_countdown(self):
        if self.is_pomodoro and self.pomodoro_end_time:
            return
        try:
            target = datetime.strptime(f"{self.project.target_date} {self.project.target_time}", "%Y-%m-%d %H:%M")
            now = datetime.now()
            diff = target - now
            total_seconds = diff.total_seconds()
            if total_seconds <= 0:
                self.expired = True
                if not self.countdown_label._expired:
                    self.countdown_label.showExpired(self.project.expired_text)
                return
            natural_days = total_seconds / 86400.0
            self.expired = False
            self.countdown_label.setValue(natural_days)
        except Exception as e:
            log_message(f"update_ticking_countdown 错误: {e}", "ERROR")

    def start_typewriter_animation(self):
        layout = self.project.custom_layout
        show_poem = layout.get("poem", {}).get("visible", False)
        if show_poem:
            if not self.master.poems_data or all(len(v) == 0 for v in self.master.poems_data.values()):
                # 数据未就绪，延迟重试
                QTimer.singleShot(3000, self._retry_poem_load)
                self.poem_label._full_text = "诗语数据加载中...请稍候"
                self.poem_label._current_display = "诗语数据加载中..."
                self.poem_label.update()
                return
            text = self.master.get_random_poem_or_tip()
            if not text or text.strip() == "":
                text = "诗语轻扬 — 请检查诗词数据文件"
            self.poem_label.start_animation(text)

    def _retry_poem_load(self):
        if not self.master.poems_data or all(len(v) == 0 for v in self.master.poems_data.values()):
            self.poem_label._full_text = "诗词数据未加载\n请重启应用或在设置中检查诗词级别"
            self.poem_label._current_display = "诗词数据未加载 - 请重启应用"
            self.poem_label.update()
        else:
            text = self.master.get_random_poem_or_tip()
            self.poem_label.start_animation(text)

    def start_tip_animation(self):
        layout = self.project.custom_layout
        show_tip = layout.get("tip", {}).get("visible", False)
        if show_tip:
            if not TIPS_DATA or len(TIPS_DATA) == 0:
                QTimer.singleShot(3000, self._retry_tip_load)
                self.tip_hint_widget._full_text = "小提示数据加载中...请稍候"
                self.tip_hint_widget._current_display = "小提示数据加载中..."
                self.tip_hint_widget.update()
                return
            text = random.choice(TIPS_DATA)
            if not text or text.strip() == "":
                text = "💡 欢迎使用倒计时桌面！"
            self.tip_hint_widget.start_animation(text)

    def _retry_tip_load(self):
        if not TIPS_DATA or len(TIPS_DATA) == 0:
            self.tip_hint_widget._full_text = "小提示数据未加载\n请重启应用"
            self.tip_hint_widget._current_display = "小提示数据未加载 - 请重启应用"
            self.tip_hint_widget.update()
        else:
            text = random.choice(TIPS_DATA)
            self.tip_hint_widget.start_animation(text)

    def save_config_later(self):
        self.save_timer.start(400)

    def save_config_now(self):
        self.project.position = (self.x(), self.y())
        self.project.size = (self.width(), self.height())
        self.master.save_config(force=True)

    def toggle_topmost(self):
        self.project.always_on_top = not self.project.always_on_top
        self.act_pin.setText("取消置顶" if self.project.always_on_top else "置顶窗口")
        flags = self.windowFlags()
        if self.project.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()
        self.master.save_config(force=True)

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.old_geometry = self.geometry()
            self.old_flags = self.windowFlags()
            for win in self.master.windows:
                if win != self:
                    win.hide()
            self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.showFullScreen()
            self.is_fullscreen = True
            self.setup_dynamic_bg()
            if not self.fullscreen_panel:
                self.fullscreen_panel = FullscreenSettingsPanel(self, self)
            self.fullscreen_panel.show()
            self.fullscreen_panel.adjustSize()
            panel_width = self.fullscreen_panel.width()
            panel_height = self.fullscreen_panel.height()
            self.fullscreen_panel.move(self.width() - panel_width - 30, self.height() - panel_height - 30)
        else:
            self.is_fullscreen = False
            if self.fullscreen_panel:
                self.fullscreen_panel.hide()
            self.setWindowFlags(self.old_flags)
            self.setGeometry(self.old_geometry)
            self.showNormal()
            for win in self.master.windows:
                if win != self:
                    win.show()
            self.setup_dynamic_bg()
        self.update()

    def toggle_dynamic_wallpaper(self, enabled):
        if self.wallpaper_widget:
            self.wallpaper_widget.setVisible(enabled)

    def set_dynamic_wallpaper_type(self, w_type):
        if self.wallpaper_widget:
            self.wallpaper_widget.wallpaper_type = w_type
            self.wallpaper_widget.stars.clear()
            self.wallpaper_widget.clouds.clear()
            self.wallpaper_widget.init_particles()

    def set_alpha(self, val):
        self.project.window_alpha = val
        self.setWindowOpacity(val)
        self.master.save_config(force=True)

    def update_pomodoro_settings(self):
        if hasattr(self, 'pomodoro_widget'):
            self.pomodoro_widget.update_settings(self.project.pomodoro_work, self.project.pomodoro_break)

    def refresh(self, theme_change=False):
        self.setWindowOpacity(self.project.window_alpha)
        if self.project.background_type == "color":
            self.bg_pixmap = None
            if self.bg_movie:
                self.bg_movie.stop()
                self.bg_movie = None
            if self.project.window_alpha < 1.0 and self.project.window_round_radius == 0:
                apply_modern_window_effect(int(self.winId()), effect_type="acrylic", is_dark=True, enable=True)
            else:
                apply_modern_window_effect(int(self.winId()), enable=False)
        elif self.project.background_type == "image":
            self.load_background_image()
        elif self.project.background_type == "dynamic":
            self.setup_dynamic_bg()
        self.refresh_styles()
        self.apply_custom_layout(skip_style=False)
        self.update()

    def close_window(self):
        self.master.plugin_manager.trigger_event("on_window_closed", self, self.project)
        self.close()
        self.master.check_windows_status()
class FluentToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(46, 24)
        self._checked = checked
        self._circle_x = 22 if checked else 2

        self.anim = QPropertyAnimation(self, b"circle_x", self)
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutBack)

    @pyqtProperty(int)
    def circle_x(self):
        return self._circle_x

    @circle_x.setter
    def circle_x(self, pos):
        self._circle_x = pos
        self.update()

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked
        self.anim.setEndValue(22 if checked else 2)
        self.anim.start()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self.anim.setEndValue(22 if self._checked else 2)
            self.anim.start()
            self.toggled.emit(self._checked)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg_color = QColor("#3498db") if self._checked else QColor("#bdc3c7")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(self._circle_x, 2, 20, 20)


class CollapsibleSection(QWidget):
    def __init__(self, title="", parent=None, initially_expanded=True):
        super().__init__(parent)
        self.expanded = initially_expanded
        self.title = title

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        arrow = "▼" if initially_expanded else "▶"
        self.toggle_btn = QPushButton(f"{arrow} {title}")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(initially_expanded)
        self.toggle_btn.setFlat(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        c = get_theme_colors(get_system_theme())
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {c['secondary_text']}; font-weight: bold;
                text-align: left; padding: 6px 4px; border: none;
            }}
            QPushButton:hover {{ color: {c['accent']}; }}
        """)
        self.toggle_btn.clicked.connect(self._on_toggle)
        self.main_layout.addWidget(self.toggle_btn)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(12, 4, 4, 8)
        self.content_layout.setSpacing(6)
        self.main_layout.addWidget(self.content_widget)
        self.content_widget.setVisible(initially_expanded)

    def _on_toggle(self, checked):
        self.expanded = checked
        self.content_widget.setVisible(checked)
        arrow = "▼" if checked else "▶"
        self.toggle_btn.setText(f"{arrow} {self.title}")

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)


class PreviewCanvas(QWidget):

    def __init__(self, project, editor, parent=None):
        super().__init__(parent)
        self.project = project
        self.editor = editor
        self.highlighted_elem = None
        self.dragging_elem = None
        self.drag_offset = QPoint()
        self._resizing_elem = None
        self._resize_handle = None
        self._resize_start_rect = None
        self._resize_start_pos = None
        self._resize_start_config = None
        self.snap_enabled = True
        self.grid_spacing = 20
        self.setMinimumSize(400, 300)

        size = self.project.size
        if size and size[1] > 0:
            self._aspect_ratio = size[0] / size[1]
        else:
            self._aspect_ratio = 4.0 / 3.0

        self.setMouseTracking(True)

    def set_highlighted_element(self, elem_id):
        self.highlighted_elem = elem_id
        self.update()

    def refresh_layout(self):
        self.update()

    def _get_canvas_rect(self):
        w, h = self.width(), self.height()
        margin = 20
        available_w = w - 2 * margin
        available_h = h - 2 * margin
        if available_w / available_h > self._aspect_ratio:
            canvas_h = available_h
            canvas_w = int(canvas_h * self._aspect_ratio)
        else:
            canvas_w = available_w
            canvas_h = int(canvas_w / self._aspect_ratio)
        x = margin + (available_w - canvas_w) // 2
        y = margin + (available_h - canvas_h) // 2
        return QRect(x, y, canvas_w, canvas_h)

    def _percent_to_pixel(self, pct_x, pct_y):
        rect = self._get_canvas_rect()
        px = rect.x() + pct_x * rect.width()
        py = rect.y() + pct_y * rect.height()
        return QPoint(int(px), int(py))

    def _pixel_to_percent(self, px, py):
        rect = self._get_canvas_rect()
        pct_x = (px - rect.x()) / rect.width() if rect.width() > 0 else 0.5
        pct_y = (py - rect.y()) / rect.height() if rect.height() > 0 else 0.5
        return (max(0.0, min(1.0, pct_x)), max(0.0, min(1.0, pct_y)))

    def _snap_position(self, pct_x, pct_y):
        if not self.snap_enabled:
            return pct_x, pct_y
        layout = self.project.custom_layout or {}
        snap_threshold = 0.02
        best_dx, best_dy = snap_threshold, snap_threshold
        result_x, result_y = pct_x, pct_y
        ref_positions = [(0.5, 0.5), (1 / 3, 0.5), (2 / 3, 0.5), (0.5, 1 / 3), (0.5, 2 / 3),
                         (0.0, 0.5), (1.0, 0.5), (0.5, 0.0), (0.5, 1.0)]
        for elem_id, config in layout.items():
            if elem_id == self.dragging_elem:
                continue
            ref_positions.append((config.get("x", 0.5), config.get("y", 0.5)))
        for rx, ry in ref_positions:
            dx = abs(pct_x - rx)
            dy = abs(pct_y - ry)
            if dx < best_dx:
                best_dx = dx
                result_x = rx
            if dy < best_dy:
                best_dy = dy
                result_y = ry
        return result_x, result_y

    def _get_elem_rect(self, elem_id, config):
        pct_x = config.get("x", 0.5)
        pct_y = config.get("y", 0.5)
        center = self._percent_to_pixel(pct_x, pct_y)
        canvas_rect = self._get_canvas_rect()
        scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else canvas_rect.width() / 600.0

        custom_w = config.get("custom_width")
        custom_h = config.get("custom_height")
        if custom_w is not None and custom_h is not None:
            w = int(custom_w * scale)
            h = int(custom_h * scale)
            return QRect(center.x() - w // 2, center.y() - h // 2, w, h)

        font_size = config.get("font_size", 14)
        scaled_size = max(8, int(font_size * scale))
        elem_type = config.get("type", "")
        if elem_type == "custom_image":
            w = int(80 * scale)
            h = int(60 * scale)
        elif elem_id == "pomodoro":
            w = int(60 * scale)
            h = int(60 * scale)
        elif elem_id == "weather":
            w = int(160 * scale)
            h = scaled_size + 10
        else:
            text = self._get_elem_text(elem_id, config)
            fm_font = QFont(config.get("font_family", "Microsoft YaHei"), scaled_size)
            text_w = QFontMetrics(fm_font).horizontalAdvance(text) + 20
            w = max(40, text_w)
            h = scaled_size + 16
        bg_radius = config.get("bg_radius", 0)
        if bg_radius > 0:
            w += int(bg_radius * scale)
            h += int(bg_radius * scale)
        return QRect(center.x() - w // 2, center.y() - h // 2, w, h)

    def _get_elem_text(self, elem_id, config):
        if config.get("type") == "custom_text":
            return config.get("text", "")
        if config.get("type") == "custom_image":
            return "🖼️"
        texts = {
            "name": self.project.name,
            "static_text": f"剩余工作日",
            "countdown": "30.000 天",
            "poem": "床前明月光，疑是地上霜",
            "weather": "🌤️ 北京 晴 25°C",
            "pomodoro": "🍅 25:00",
            "tip": "💡 保持专注",
        }
        return texts.get(elem_id, elem_id)

    def _get_handle_positions(self, rect):
        return {
            "tl": QPoint(rect.left(), rect.top()),
            "tc": QPoint(rect.center().x(), rect.top()),
            "tr": QPoint(rect.right(), rect.top()),
            "ml": QPoint(rect.left(), rect.center().y()),
            "mr": QPoint(rect.right(), rect.center().y()),
            "bl": QPoint(rect.left(), rect.bottom()),
            "bc": QPoint(rect.center().x(), rect.bottom()),
            "br": QPoint(rect.right(), rect.bottom()),
        }

    def _hit_test_handle(self, pos, elem_id):
        if elem_id != self.highlighted_elem:
            return None
        config = (self.project.custom_layout or {}).get(elem_id, {})
        if not config.get("visible", True):
            return None
        rect = self._get_elem_rect(elem_id, config)
        handles = self._get_handle_positions(rect)
        for name, hpos in handles.items():
            if abs(pos.x() - hpos.x()) <= 5 and abs(pos.y() - hpos.y()) <= 5:
                return name
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        canvas_rect = self._get_canvas_rect()
        radius = self.project.window_round_radius

        painter.save()
        path = QPainterPath()
        path.addRoundedRect(QRectF(canvas_rect), radius, radius)
        painter.setClipPath(path)

        bg_type = self.project.background_type
        if bg_type == "color":
            bg_color = QColor(self.project.bg_color)
            bg_color.setAlpha(int(self.project.window_alpha * 255))
            painter.fillRect(canvas_rect, bg_color)
        elif bg_type == "gradient":
            grad = QLinearGradient(float(canvas_rect.x()), float(canvas_rect.y()),
                                   float(canvas_rect.right()), float(canvas_rect.bottom()))
            grad.setColorAt(0.0, QColor(self.project.gradient_start))
            grad.setColorAt(1.0, QColor(self.project.gradient_end))
            painter.fillRect(canvas_rect, grad)
        elif bg_type == "image":
            painter.fillRect(canvas_rect, QColor(40, 40, 50))
            painter.setPen(QPen(QColor(200, 200, 200, 100), 1))
            painter.drawText(canvas_rect, Qt.AlignmentFlag.AlignCenter, "🖼️ 图片背景预览")
        else:
            painter.fillRect(canvas_rect, QColor(20, 20, 30))

        painter.setPen(QPen(QColor(255, 255, 255, 60), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(canvas_rect, radius, radius)
        painter.restore()

        if hasattr(self.editor, 'cb_grid') and self.editor.cb_grid.isChecked():
            painter.setPen(QPen(QColor(100, 100, 130, 50), 1, Qt.PenStyle.DotLine))
            gs = self.grid_spacing
            x = canvas_rect.x()
            while x <= canvas_rect.right():
                painter.drawLine(x, canvas_rect.y(), x, canvas_rect.bottom())
                x += gs
            y = canvas_rect.y()
            while y <= canvas_rect.bottom():
                painter.drawLine(canvas_rect.x(), y, canvas_rect.right(), y)
                y += gs

        if hasattr(self.editor, 'cb_guides') and self.editor.cb_guides.isChecked():
            guide_color = QColor(79, 195, 247, 80)
            painter.setPen(QPen(guide_color, 1, Qt.PenStyle.DashLine))
            cx = canvas_rect.x() + canvas_rect.width() // 2
            cy = canvas_rect.y() + canvas_rect.height() // 2
            painter.drawLine(cx, canvas_rect.y(), cx, canvas_rect.bottom())
            painter.drawLine(canvas_rect.x(), cy, canvas_rect.right(), cy)
            for i in [1, 2]:
                tx = canvas_rect.x() + canvas_rect.width() * i // 3
                ty = canvas_rect.y() + canvas_rect.height() * i // 3
                painter.drawLine(tx, canvas_rect.y(), tx, canvas_rect.bottom())
                painter.drawLine(canvas_rect.x(), ty, canvas_rect.right(), ty)

        layout = self.project.custom_layout or {}
        for elem_id, config in layout.items():
            if not config.get("visible", True):
                continue
            rect = self._get_elem_rect(elem_id, config)
            canvas_w = canvas_rect.width()
            scale = canvas_w / self.project.size[0] if self.project.size[0] > 0 else canvas_w / 600.0
            font_size = config.get("font_size", 14)
            scaled_size = max(8, int(font_size * scale))
            color = QColor(config.get("color", "#FFFFFF"))
            opacity = config.get("opacity", 1.0)
            color.setAlpha(int(opacity * 255))

            if config.get("shadow_blur", 0) > 0:
                shadow_color = QColor(config.get("shadow_color", "#000000"))
                shadow_color.setAlpha(80)
                dx = int(config.get("shadow_offset_x", 0) * scale)
                dy = int(config.get("shadow_offset_y", 0) * scale)
                shadow_rect = rect.translated(dx, dy)
                path_shadow = QPainterPath()
                path_shadow.addRoundedRect(QRectF(shadow_rect), config.get("bg_radius", 0) * scale,
                                           config.get("bg_radius", 0) * scale)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(shadow_color)
                painter.drawPath(path_shadow)

            bg_color_str = config.get("bg_color", "transparent")
            if bg_color_str != "transparent":
                bg_color = QColor(bg_color_str)
                bg_color.setAlpha(int(opacity * bg_color.alpha()))
                painter.setBrush(bg_color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(rect, config.get("bg_radius", 0) * scale,
                                        config.get("bg_radius", 0) * scale)

            stroke_width = config.get("stroke_width", 0)
            if stroke_width > 0 and config.get("stroke_color", "transparent") != "transparent":
                stroke_pen = QPen(QColor(config["stroke_color"]), stroke_width * scale)
                painter.setPen(stroke_pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRoundedRect(rect, config.get("bg_radius", 0) * scale,
                                        config.get("bg_radius", 0) * scale)
            else:
                if elem_id == self.highlighted_elem:
                    pen = QPen(QColor(79, 195, 247, 150), 2.5, Qt.PenStyle.SolidLine)
                    painter.setPen(pen)
                    painter.setBrush(QColor(79, 195, 247, 20))
                    painter.drawRoundedRect(rect, 4, 4)
                    handles = self._get_handle_positions(rect)
                    handle_size = 5
                    handle_color = QColor(79, 195, 247, 200)
                    painter.setBrush(handle_color)
                    painter.setPen(QPen(QColor(255, 255, 255, 180), 1))
                    for hpos in handles.values():
                        painter.drawEllipse(hpos, handle_size//2, handle_size//2)

            if config.get("type") == "custom_image":
                painter.setPen(color)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "🖼️")
            else:
                text = self._get_elem_text(elem_id, config)
                align_map = {"左": Qt.AlignmentFlag.AlignLeft, "中": Qt.AlignmentFlag.AlignCenter,
                             "右": Qt.AlignmentFlag.AlignRight}
                h_align = align_map.get(config.get("alignment_h", "中"), Qt.AlignmentFlag.AlignCenter)
                v_align = {"上": Qt.AlignmentFlag.AlignTop, "中": Qt.AlignmentFlag.AlignCenter,
                           "下": Qt.AlignmentFlag.AlignBottom}.get(config.get("alignment_v", "中"),
                                                                   Qt.AlignmentFlag.AlignCenter)
                font = QFont(config.get("font_family", "Microsoft YaHei"), scaled_size)
                painter.setFont(font)
                painter.setPen(color)
                painter.drawText(rect, h_align | v_align, text)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.pos()
        layout = self.project.custom_layout or {}

        handle = self._hit_test_handle(pos, self.highlighted_elem)
        if handle:
            config = self.project.custom_layout.get(self.highlighted_elem, {})
            canvas_rect = self._get_canvas_rect()
            scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else canvas_rect.width() / 600.0
            rect = self._get_elem_rect(self.highlighted_elem, config)
            self._resizing_elem = self.highlighted_elem
            self._resize_handle = handle
            self._resize_start_pos = pos
            self._resize_start_rect = QRect(rect)
            self._resize_start_config = {
                "custom_width": config.get("custom_width", rect.width() / scale),
                "custom_height": config.get("custom_height", rect.height() / scale),
            }
            return

        self.dragging_elem = None
        for elem_id in reversed(list(layout.keys())):
            config = layout[elem_id]
            if not config.get("visible", True):
                continue
            rect = self._get_elem_rect(elem_id, config)
            if rect.contains(pos):
                self.dragging_elem = elem_id
                center = self._percent_to_pixel(config.get("x", 0.5), config.get("y", 0.5))
                self.drag_offset = pos - center
                for i in range(self.editor.element_list.count()):
                    item = self.editor.element_list.item(i)
                    if item.data(Qt.ItemDataRole.UserRole) == elem_id:
                        self.editor.element_list.setCurrentRow(i)
                        break
                break

    def mouseMoveEvent(self, event):
        if self._resizing_elem and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.pos() - self._resize_start_pos
            config = self.project.custom_layout.get(self._resizing_elem, {})
            canvas_rect = self._get_canvas_rect()
            scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else canvas_rect.width() / 600.0
            start_w = self._resize_start_config["custom_width"]
            start_h = self._resize_start_config["custom_height"]
            handle = self._resize_handle

            dx_logic = delta.x() / scale
            dy_logic = delta.y() / scale

            new_w = start_w
            new_h = start_h

            if "r" in handle:
                new_w = max(30, start_w + dx_logic)
            if "l" in handle:
                new_w = max(30, start_w - dx_logic)
            if "b" in handle:
                new_h = max(20, start_h + dy_logic)
            if "t" in handle:
                new_h = max(20, start_h - dy_logic)

            if start_w > 0 and start_h > 0:
                w_ratio = new_w / start_w
                h_ratio = new_h / start_h
                raw_scale = max(w_ratio, h_ratio)
                if raw_scale > 1.0:
                    scale_factor = 1.0 + (raw_scale - 1.0) * 0.25
                else:
                    scale_factor = max(0.5, 1.0 - (1.0 - raw_scale) * 0.5)
                old_font_size = config.get("font_size", 14)
                new_font_size = max(6, min(72, int(old_font_size * scale_factor)))
                config["font_size"] = new_font_size

            config["custom_width"] = new_w
            config["custom_height"] = new_h

            if hasattr(self.editor, 'current_elem') and self.editor.current_elem == self._resizing_elem:
                self.editor._update_ui_from_config()

            self.update()
            return

        if self.dragging_elem and event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.pos() - self.drag_offset
            pct_x, pct_y = self._pixel_to_percent(pos.x(), pos.y())
            pct_x, pct_y = self._snap_position(pct_x, pct_y)
            layout = self.project.custom_layout
            if self.dragging_elem in layout:
                layout[self.dragging_elem]["x"] = pct_x
                layout[self.dragging_elem]["y"] = pct_y
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._resizing_elem:
                self._resizing_elem = None
                self._resize_handle = None
                if self.editor.window:
                    self.editor.window.apply_custom_layout()
            self.dragging_elem = None


DEFAULT_ELEMENTS = ["name", "static_text", "countdown"]
ALL_AVAILABLE_ELEMENTS = ["name", "static_text", "countdown", "poem", "weather", "pomodoro", "tip"]
ELEMENT_DISPLAY_NAMES = {
    "name": "📌 项目名称",
    "static_text": "📝 静态文字",
    "countdown": "⏳ 倒计时",
    "poem": "📜 诗语轻扬",
    "weather": "🌤️ 天气挂件",
    "pomodoro": "🍅 番茄钟",
    "tip": "💡 小提示",
}


class PluginIntroductionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔌 帮助")
        self.resize(800, 600)
        self.setMinimumSize(700, 500)
        theme = get_system_theme()
        self.setStyleSheet(get_theme_qss(theme))

        layout = QVBoxLayout(self)

        title = QLabel("🔌 插件系统指南")
        title.setStyleSheet(f"font-size: 18pt; font-weight: bold; color: {get_theme_colors(theme)['accent']};")
        layout.addWidget(title)

        tabs = QTabWidget()

        tab_intro = QWidget()
        intro_layout = QVBoxLayout(tab_intro)
        intro_text = QTextEdit()
        intro_text.setReadOnly(True)
        intro_text.setHtml("""
        <h2>🚀 快速入门</h2>
        <p><b>什么是插件？</b><br>插件是可以扩展本应用功能的小程序，由社区或你自己编写，放置在 <code>plugins/</code> 目录下。</p>

        <h3>📥 安装插件</h3>
        <ol>
            <li>将 <code>.py</code> 插件文件放入应用目录下的 <code>plugins</code> 文件夹（若不存在请手动创建）。</li>
            <li>重新打开设置 → 插件管理，点击“刷新”或重启应用。</li>
            <li>在列表中找到新插件，右键选择“启用”。</li>
        </ol>

        <h3>⚙️ 管理插件</h3>
        <ul>
            <li><b>启用/禁用</b>：控制插件是否运行。</li>
            <li><b>权限管理</b>：限制插件能访问的文件、网络、命令等。</li>
            <li><b>插件详情</b>：选中插件可查看其说明和自定义设置。</li>
        </ul>

        <h3>⚠️ 安全提示</h3>
        <p>插件运行在沙箱环境中，但仍需谨慎使用未知来源的插件。建议仅启用你信任的插件，并严格限制其权限。</p>
        """)
        intro_layout.addWidget(intro_text)
        tabs.addTab(tab_intro, "📖 入门")

        tab_dev = QWidget()
        dev_layout = QVBoxLayout(tab_dev)
        dev_text = QTextEdit()
        dev_text.setReadOnly(True)
        dev_text.setHtml("""
        <h2>🛠️ 如何开发一个插件</h2>
        <p>插件是一个 Python 文件，必须包含一个 <code>setup(app, api)</code> 函数，返回一个继承自 <code>Plugin</code> 的实例。</p>

        <h3>最小示例</h3>
        <pre><code># my_plugin.py
from plugin_base import Plugin, PluginPermission

class MyPlugin(Plugin):
    def __init__(self, app, api):
        super().__init__()
        self.name = "我的插件"
        self.version = "1.0"
        self.author = "YourName"
        self.description = "这是一个示例插件"
        self.requested_permissions = PluginPermission.FILE_READ  # 声明所需权限

    def on_enable(self):
        self.api.log("插件已启用")
        # 在此注册你的功能，如动态背景、自定义控件等
        # self.api.register_dynamic_bg("my_bg", "我的动态背景", MyBgWidget)

def setup(app, api):
    return MyPlugin(app, api)
</code></pre>

        <h3>可用 API</h3>
        <ul>
            <li><code>api.log(message, level)</code> - 记录日志</li>
            <li><code>api.register_dynamic_bg(id, name, widget_class)</code> - 注册动态背景</li>
            <li><code>api.register_widget(id, name, widget_class)</code> - 注册桌面控件</li>
            <li><code>api.get_config(key, default)</code> - 读取插件配置</li>
            <li><code>api.set_config(key, value)</code> - 保存插件配置</li>
            <li><code>api.show_notification(title, message)</code> - 发送系统通知</li>
        </ul>

        <h3>权限声明</h3>
        <p>插件必须在 <code>requested_permissions</code> 中声明所需权限：</p>
        <ul>
            <li><code>PluginPermission.FILE_READ</code> - 读取文件</li>
            <li><code>PluginPermission.FILE_WRITE</code> - 写入文件</li>
            <li><code>PluginPermission.NETWORK</code> - 网络访问</li>
            <li><code>PluginPermission.COMMAND</code> - 执行系统命令</li>
        </ul>
        <p>用户启用插件时需确认这些权限。</p>
        """)
        dev_layout.addWidget(dev_text)
        tabs.addTab(tab_dev, "🛠️ 开发")

        tab_sec = QWidget()
        sec_layout = QVBoxLayout(tab_sec)
        sec_text = QTextEdit()
        sec_text.setReadOnly(True)
        sec_text.setHtml("""
        <h2>🔒 安全策略</h2>
        <ul>
            <li><b>沙箱执行</b>：插件运行在受限的 Python 环境中，无法直接访问危险系统函数。</li>
            <li><b>权限检查</b>：任何敏感操作都会检查插件是否拥有对应权限，否则抛出异常。</li>
            <li><b>签名验证</b>（可选）：开发者可使用 Ed25519 对插件签名，应用加载前验证。</li>
            <li><b>用户授权</b>：启用插件时必须用户确认其请求的权限。</li>
            <li><b>日志监控</b>：所有插件行为均记录在案，可在日志面板查看。</li>
        </ul>
        """)
        sec_layout.addWidget(sec_text)
        tabs.addTab(tab_sec, "🔒 安全")

        layout.addWidget(tabs)

        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

class AppearanceEditor(QDialog):
    def __init__(self, project, window, parent=None):
        super().__init__(parent)
        self.project = project
        self.window = window
        self.current_theme = get_system_theme()
        self.current_elem = None
        self._updating_ui = False

        self._layout_backup = json.loads(json.dumps(project.custom_layout or {}))

        if not project.custom_layout:
            self._init_default_layout()

        self.setWindowTitle("🎨 自定义外观编辑器")
        self.setMinimumSize(1100, 750)
        self.resize(1200, 820)
        self.init_ui()
        self.apply_theme_style()

        self._theme_monitor = SystemThemeMonitor(self)
        self._theme_monitor.theme_changed.connect(self._on_theme_changed)

    def _init_default_layout(self):
        if self.window and hasattr(self.window, 'master') and hasattr(self.window.master, 'theme'):
            is_dark = self.window.master.theme.is_dark
        else:
            is_dark = is_system_dark()

        if is_dark:
            name_color = "#FFFFFF"
            name_bg = "rgba(0,0,0,0.25)"
            static_color = "#E0E0E0"
            countdown_color = "#FFFFFF"
            countdown_bg = "rgba(0,0,0,0.35)"
            stroke_color = "rgba(255,255,255,0.3)"
        else:
            name_color = "#1E1E1E"
            name_bg = "rgba(255,255,255,0.7)"
            static_color = "#333333"
            countdown_color = "#1E1E1E"
            countdown_bg = "rgba(255,255,255,0.8)"
            stroke_color = "rgba(0,0,0,0.1)"

        layout = {}
        layout["name"] = {
            "visible": True, "x": 0.5, "y": 0.10,
            "font_size": 16, "color": name_color, "opacity": 1.0,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 8,
            "bg_color": name_bg, "bg_radius": 12,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["static_text"] = {
            "visible": True, "x": 0.5, "y": 0.28,
            "font_size": 13, "color": static_color, "opacity": 0.9,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 1, "shadow_blur": 6,
            "bg_color": "transparent", "bg_radius": 0,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["countdown"] = {
            "visible": True, "x": 0.5, "y": 0.55,
            "font_size": 32, "color": countdown_color, "opacity": 1.0,
            "stroke_color": stroke_color, "stroke_width": 0.8,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 3, "shadow_blur": 12,
            "bg_color": countdown_bg, "bg_radius": 15,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        self.project.custom_layout = layout

    def _on_theme_changed(self, is_dark):
        self.current_theme = get_system_theme()
        self.apply_theme_style()

    def apply_theme_style(self):
        self.setStyleSheet(get_theme_qss(self.current_theme))

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_panel = QWidget()
        left_panel.setFixedWidth(240)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("📐 元素列表")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 6px;")
        left_layout.addWidget(title_label)

        self.element_list = QListWidget()
        self.element_list.currentRowChanged.connect(self.on_element_select)
        left_layout.addWidget(self.element_list)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 8)
        self.btn_add = QPushButton("➕ 添加")
        self.btn_add.setProperty("primary", True)
        self.btn_add.clicked.connect(self.add_element)
        self.btn_remove = QPushButton("➖ 删除")
        self.btn_remove.setProperty("danger", True)
        self.btn_remove.clicked.connect(self.remove_element)
        self.btn_remove.setEnabled(False)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        left_layout.addLayout(btn_layout)

        order_layout = QHBoxLayout()
        order_layout.setContentsMargins(0, 0, 0, 16)
        self.btn_up = QPushButton("⬆ 上移")
        self.btn_up.setProperty("secondary", True)
        self.btn_up.clicked.connect(self.move_element_up)
        self.btn_down = QPushButton("⬇ 下移")
        self.btn_down.setProperty("secondary", True)
        self.btn_down.clicked.connect(self.move_element_down)
        order_layout.addWidget(self.btn_up)
        order_layout.addWidget(self.btn_down)
        left_layout.addLayout(order_layout)

        btn_plugin_help = QPushButton("🔌 如何添加更多元素？")
        btn_plugin_help.setStyleSheet(f"background-color: {get_theme_colors(self.current_theme)['secondary_text']}; color: white; border-radius: 4px; padding: 6px;")
        btn_plugin_help.clicked.connect(self.go_to_plugin_help)
        left_layout.addWidget(btn_plugin_help)

        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(10, 10, 10, 10)

        preview_label = QLabel("👁️ 预览（拖拽调整位置）")
        preview_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 4px;")
        center_layout.addWidget(preview_label)

        tool_layout = QHBoxLayout()
        self.cb_grid = QCheckBox("网格")
        self.cb_grid.setChecked(True)
        self.cb_snap = QCheckBox("吸附")
        self.cb_snap.setChecked(True)
        self.cb_guides = QCheckBox("参考线")
        self.cb_guides.setChecked(True)
        tool_layout.addWidget(self.cb_grid)
        tool_layout.addWidget(self.cb_snap)
        tool_layout.addWidget(self.cb_guides)
        tool_layout.addStretch()
        center_layout.addLayout(tool_layout)

        self.preview_canvas = PreviewCanvas(self.project, self)
        self.preview_canvas.setMinimumSize(400, 300)
        center_layout.addWidget(self.preview_canvas, 1)

        self.cb_grid.toggled.connect(self.preview_canvas.update)
        self.cb_snap.toggled.connect(lambda v: setattr(self.preview_canvas, 'snap_enabled', v))
        self.cb_guides.toggled.connect(self.preview_canvas.update)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(8)

        self.prop_title = QLabel("⚙️ 属性设置")
        self.prop_title.setStyleSheet(f"font-size: 12pt; font-weight: bold; color: {get_theme_colors(self.current_theme)['accent']};")
        right_layout.addWidget(self.prop_title)

        self.no_selection_label = QLabel("👈 请先选择元素")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet(f"color: {get_theme_colors(self.current_theme)['secondary_text']}; padding: 30px;")
        right_layout.addWidget(self.no_selection_label)

        self.prop_scroll = QScrollArea()
        self.prop_scroll.setWidgetResizable(True)
        self.prop_scroll.setVisible(False)

        prop_widget = QWidget()
        self.prop_layout = QVBoxLayout(prop_widget)
        self.prop_layout.setSpacing(8)
        self.prop_layout.setContentsMargins(0, 0, 0, 0)

        self.general_section = CollapsibleSection("📌 通用属性", initially_expanded=True)
        self.cb_visible = QCheckBox("可见")
        self.cb_visible.toggled.connect(self._on_property_changed)
        self.general_section.addWidget(self.cb_visible)

        size_layout = QHBoxLayout()
        lbl_font_size = QLabel("字体大小")
        lbl_font_size.setFixedWidth(80)
        lbl_font_size.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        size_layout.addWidget(lbl_font_size)
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(6, 72)
        self.spin_font_size.valueChanged.connect(self._on_property_changed)
        size_layout.addWidget(self.spin_font_size)
        self.general_section.addLayout(size_layout)

        font_family_layout = QHBoxLayout()
        lbl_font_family = QLabel("字体")
        lbl_font_family.setFixedWidth(80)
        lbl_font_family.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        font_family_layout.addWidget(lbl_font_family)
        self.combo_font_family = QComboBox()
        self.combo_font_family.addItems(QFontDatabase.families())
        self.combo_font_family.setEditable(True)
        self.combo_font_family.currentTextChanged.connect(self._on_property_changed)
        font_family_layout.addWidget(self.combo_font_family)
        self.general_section.addLayout(font_family_layout)

        self.btn_color = QPushButton("")
        self.btn_color.setFixedSize(56, 28)
        self.btn_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_color.clicked.connect(self._pick_color)
        self.btn_color.setStyleSheet(f"QPushButton {{ border-radius: 6px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']}; }}")
        color_layout = QHBoxLayout()
        lbl_color = QLabel("文字颜色")
        lbl_color.setFixedWidth(80)
        lbl_color.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        color_layout.addWidget(lbl_color)
        color_layout.addStretch()
        color_layout.addWidget(self.btn_color)
        self.general_section.addLayout(color_layout)

        opacity_layout = QHBoxLayout()
        lbl_opacity = QLabel("透明度")
        lbl_opacity.setFixedWidth(80)
        lbl_opacity.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        opacity_layout.addWidget(lbl_opacity)
        self.slider_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_opacity.setRange(0, 100)
        self.slider_opacity.setValue(100)
        self.slider_opacity.valueChanged.connect(self._on_slider_changed)
        self.label_opacity = QLabel("100%")
        self.label_opacity.setFixedWidth(35)
        opacity_layout.addWidget(self.slider_opacity)
        opacity_layout.addWidget(self.label_opacity)
        self.general_section.addLayout(opacity_layout)

        self.prop_layout.addWidget(self.general_section)
        self.prop_layout.addSpacing(12)

        self.stroke_section = CollapsibleSection("🖍️ 字体描边", initially_expanded=False)
        self.cb_stroke_enable = QCheckBox("启用描边")
        self.cb_stroke_enable.toggled.connect(self._on_property_changed)
        self.stroke_section.addWidget(self.cb_stroke_enable)

        stroke_color_layout = QHBoxLayout()
        lbl_stroke_color = QLabel("描边颜色")
        lbl_stroke_color.setFixedWidth(80)
        lbl_stroke_color.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        stroke_color_layout.addWidget(lbl_stroke_color)
        self.btn_stroke_color = QPushButton("")
        self.btn_stroke_color.setFixedSize(40, 22)
        self.btn_stroke_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stroke_color.clicked.connect(lambda: self._pick_color_attr("stroke_color"))
        self.btn_stroke_color.setStyleSheet(f"QPushButton {{ border-radius: 4px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']}; }}")
        stroke_color_layout.addStretch()
        stroke_color_layout.addWidget(self.btn_stroke_color)
        self.stroke_section.addLayout(stroke_color_layout)

        width_layout = QHBoxLayout()
        lbl_stroke_width = QLabel("宽度")
        lbl_stroke_width.setFixedWidth(80)
        lbl_stroke_width.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        width_layout.addWidget(lbl_stroke_width)
        self.spin_stroke_width = QDoubleSpinBox()
        self.spin_stroke_width.setRange(0, 10)
        self.spin_stroke_width.setSingleStep(0.5)
        self.spin_stroke_width.valueChanged.connect(self._on_property_changed)
        width_layout.addWidget(self.spin_stroke_width)
        self.stroke_section.addLayout(width_layout)

        self.prop_layout.addWidget(self.stroke_section)
        self.prop_layout.addSpacing(12)

        self.shadow_section = CollapsibleSection("🌑 文字阴影", initially_expanded=False)
        shadow_color_layout = QHBoxLayout()
        lbl_shadow_color = QLabel("阴影颜色")
        lbl_shadow_color.setFixedWidth(80)
        lbl_shadow_color.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shadow_color_layout.addWidget(lbl_shadow_color)
        self.btn_shadow_color = QPushButton("")
        self.btn_shadow_color.setFixedSize(40, 22)
        self.btn_shadow_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_shadow_color.clicked.connect(lambda: self._pick_color_attr("shadow_color"))
        self.btn_shadow_color.setStyleSheet(f"QPushButton {{ border-radius: 4px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']}; }}")
        shadow_color_layout.addStretch()
        shadow_color_layout.addWidget(self.btn_shadow_color)
        self.shadow_section.addLayout(shadow_color_layout)

        offx_layout = QHBoxLayout()
        lbl_offx = QLabel("水平偏移")
        lbl_offx.setFixedWidth(80)
        lbl_offx.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        offx_layout.addWidget(lbl_offx)
        self.spin_shadow_offx = QSpinBox()
        self.spin_shadow_offx.setRange(-20, 20)
        self.spin_shadow_offx.valueChanged.connect(self._on_property_changed)
        offx_layout.addWidget(self.spin_shadow_offx)
        self.shadow_section.addLayout(offx_layout)

        offy_layout = QHBoxLayout()
        lbl_offy = QLabel("垂直偏移")
        lbl_offy.setFixedWidth(80)
        lbl_offy.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        offy_layout.addWidget(lbl_offy)
        self.spin_shadow_offy = QSpinBox()
        self.spin_shadow_offy.setRange(-20, 20)
        self.spin_shadow_offy.valueChanged.connect(self._on_property_changed)
        offy_layout.addWidget(self.spin_shadow_offy)
        self.shadow_section.addLayout(offy_layout)

        blur_layout = QHBoxLayout()
        lbl_blur = QLabel("模糊半径")
        lbl_blur.setFixedWidth(80)
        lbl_blur.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        blur_layout.addWidget(lbl_blur)
        self.spin_shadow_blur = QDoubleSpinBox()
        self.spin_shadow_blur.setRange(0, 30)
        self.spin_shadow_blur.setSingleStep(0.5)
        self.spin_shadow_blur.valueChanged.connect(self._on_property_changed)
        blur_layout.addWidget(self.spin_shadow_blur)
        self.shadow_section.addLayout(blur_layout)

        self.prop_layout.addWidget(self.shadow_section)
        self.prop_layout.addSpacing(12)

        self.bg_section = CollapsibleSection("📦 元素背景", initially_expanded=True)
        bg_color_layout = QHBoxLayout()
        lbl_bg_color = QLabel("背景颜色")
        lbl_bg_color.setFixedWidth(80)
        lbl_bg_color.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        bg_color_layout.addWidget(lbl_bg_color)
        self.btn_bg_color = QPushButton("")
        self.btn_bg_color.setFixedSize(40, 22)
        self.btn_bg_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_bg_color.clicked.connect(lambda: self._pick_color_attr("bg_color"))
        self.btn_bg_color.setStyleSheet(f"QPushButton {{ border-radius: 4px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']}; }}")
        bg_color_layout.addStretch()
        bg_color_layout.addWidget(self.btn_bg_color)
        self.bg_section.addLayout(bg_color_layout)

        radius_layout = QHBoxLayout()
        lbl_radius = QLabel("圆角")
        lbl_radius.setFixedWidth(80)
        lbl_radius.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        radius_layout.addWidget(lbl_radius)
        self.spin_bg_radius = QDoubleSpinBox()
        self.spin_bg_radius.setRange(0, 30)
        self.spin_bg_radius.valueChanged.connect(self._on_property_changed)
        radius_layout.addWidget(self.spin_bg_radius)
        self.bg_section.addLayout(radius_layout)

        self.prop_layout.addWidget(self.bg_section)
        self.prop_layout.addSpacing(12)

        self.align_section = CollapsibleSection("↔️ 对齐方式", initially_expanded=False)
        h_layout = QHBoxLayout()
        lbl_align_h = QLabel("水平")
        lbl_align_h.setFixedWidth(80)
        lbl_align_h.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        h_layout.addWidget(lbl_align_h)
        self.combo_align_h = QComboBox()
        self.combo_align_h.addItems(["左", "中", "右"])
        self.combo_align_h.currentIndexChanged.connect(self._on_property_changed)
        h_layout.addWidget(self.combo_align_h)
        self.align_section.addLayout(h_layout)

        v_layout = QHBoxLayout()
        lbl_align_v = QLabel("垂直")
        lbl_align_v.setFixedWidth(80)
        lbl_align_v.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        v_layout.addWidget(lbl_align_v)
        self.combo_align_v = QComboBox()
        self.combo_align_v.addItems(["上", "中", "下"])
        self.combo_align_v.currentIndexChanged.connect(self._on_property_changed)
        v_layout.addWidget(self.combo_align_v)
        self.align_section.addLayout(v_layout)

        self.prop_layout.addWidget(self.align_section)
        self.prop_layout.addSpacing(12)

        self.static_text_section = CollapsibleSection("📝 文本内容")
        self.edit_static_text = QLineEdit()
        self.edit_static_text.setPlaceholderText("留空则自动显示")
        self.edit_static_text.textChanged.connect(self._on_property_changed)
        self.static_text_section.addWidget(self.edit_static_text)
        self.static_text_section.setVisible(False)
        self.prop_layout.addWidget(self.static_text_section)

        self.countdown_section = CollapsibleSection("⏳ 倒计时设置")
        cd_layout = QHBoxLayout()
        lbl_expired = QLabel("到期显示文字")
        lbl_expired.setFixedWidth(80)
        lbl_expired.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cd_layout.addWidget(lbl_expired)
        self.edit_expired_text = QLineEdit()
        self.edit_expired_text.setPlaceholderText("留空则显示 0.000 天")
        self.edit_expired_text.textChanged.connect(self._on_property_changed)
        cd_layout.addWidget(self.edit_expired_text)
        self.countdown_section.addLayout(cd_layout)

        cd_fmt_layout = QHBoxLayout()
        lbl_format = QLabel("显示格式")
        lbl_format.setFixedWidth(80)
        lbl_format.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cd_fmt_layout.addWidget(lbl_format)
        self.combo_display_format = QComboBox()
        self.combo_display_format.addItems(["小数 (天)", "整数 (天)", "时分秒", "自定义模板"])
        self.combo_display_format.currentIndexChanged.connect(self._on_display_format_changed)
        cd_fmt_layout.addWidget(self.combo_display_format)
        self.countdown_section.addLayout(cd_fmt_layout)

        self.custom_template_row = QWidget()
        ct_layout = QHBoxLayout(self.custom_template_row)
        ct_layout.setContentsMargins(0, 0, 0, 0)
        lbl_template = QLabel("模板")
        lbl_template.setFixedWidth(80)
        lbl_template.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        ct_layout.addWidget(lbl_template)
        self.edit_format_template = QLineEdit()
        self.edit_format_template.setPlaceholderText("{days}天 {hours}时 {minutes}分 {seconds}秒")
        self.edit_format_template.textChanged.connect(self._on_property_changed)
        ct_layout.addWidget(self.edit_format_template)
        self.countdown_section.addWidget(self.custom_template_row)
        self.custom_template_row.setVisible(False)

        self.countdown_section.setVisible(False)
        self.prop_layout.addWidget(self.countdown_section)
        self.prop_layout.addSpacing(12)

        self.weather_section = CollapsibleSection("🌤️ 天气设置")
        self.combo_weather_province = QComboBox()
        self.combo_weather_province.addItems(list(PROVINCE_CITY_DATA.keys()))
        self.combo_weather_city = QComboBox()
        self.combo_weather_province.currentTextChanged.connect(self._update_weather_cities)
        self.weather_section.addWidget(QLabel("省份"))
        self.weather_section.addWidget(self.combo_weather_province)
        self.weather_section.addWidget(QLabel("城市"))
        self.weather_section.addWidget(self.combo_weather_city)
        self.combo_weather_city.currentTextChanged.connect(self._on_property_changed)
        self._update_weather_cities(self.combo_weather_province.currentText())
        self.weather_section.setVisible(False)
        self.prop_layout.addWidget(self.weather_section)
        self.prop_layout.addSpacing(12)

        self.pomo_section = CollapsibleSection("🍅 番茄钟设置")
        pomo_layout = QFormLayout()
        self.spin_pomo_work = QSpinBox()
        self.spin_pomo_work.setRange(1, 120)
        self.spin_pomo_work.setSuffix(" 分钟")
        self.spin_pomo_work.valueChanged.connect(self._on_property_changed)
        pomo_layout.addRow("工作时长", self.spin_pomo_work)
        self.spin_pomo_break = QSpinBox()
        self.spin_pomo_break.setRange(1, 60)
        self.spin_pomo_break.setSuffix(" 分钟")
        self.spin_pomo_break.valueChanged.connect(self._on_property_changed)
        pomo_layout.addRow("休息时长", self.spin_pomo_break)
        self.pomo_section.addLayout(pomo_layout)
        self.pomo_section.setVisible(False)
        self.prop_layout.addWidget(self.pomo_section)
        self.prop_layout.addSpacing(12)

        self.poem_section = CollapsibleSection("📜 诗语轻扬设置")
        self.spin_typewriter = QSpinBox()
        self.spin_typewriter.setRange(1, 120)
        self.spin_typewriter.setValue(self.project.typewriter_interval)
        self.spin_typewriter.setSuffix(" 分钟")
        self.spin_typewriter.valueChanged.connect(self._on_property_changed)
        self.poem_section.addWidget(QLabel("切换间隔"))
        self.poem_section.addWidget(self.spin_typewriter)
        self.poem_section.setVisible(False)
        self.prop_layout.addWidget(self.poem_section)
        self.prop_layout.addSpacing(12)

        self.tip_section = CollapsibleSection("💡 小提示设置")
        tip_layout = QFormLayout()
        self.spin_tip_interval = QSpinBox()
        self.spin_tip_interval.setRange(1, 120)
        self.spin_tip_interval.setValue(self.project.tip_interval if hasattr(self.project, 'tip_interval') else self.project.typewriter_interval)
        self.spin_tip_interval.setSuffix(" 分钟")
        self.spin_tip_interval.valueChanged.connect(self._on_property_changed)
        tip_layout.addRow("切换间隔", self.spin_tip_interval)
        self.tip_section.addLayout(tip_layout)
        self.tip_section.setVisible(False)
        self.prop_layout.addWidget(self.tip_section)

        self.prop_layout.addStretch()
        self.prop_scroll.setWidget(prop_widget)
        right_layout.addWidget(self.prop_scroll)

        tc2 = get_theme_colors(self.current_theme)
        self.win_settings_box = QGroupBox("🪟 窗口设置")
        self.win_settings_box.setStyleSheet(f"""
            QGroupBox {{
                color: {tc2['text_color']};
                font-weight: bold; font-size: 12px;
                border: 1px solid {tc2['border_color']};
                border-radius: 7px; margin-top: 10px; padding: 12px 6px 6px 6px;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
            QLabel {{ color: {tc2['text_color']}; font-size: 11px; }}
            QComboBox {{ font-size: 11px; padding: 2px 4px; }}
            QPushButton {{ font-size: 11px; }}
        """)
        win_lay = QVBoxLayout(self.win_settings_box)
        win_lay.setSpacing(6)
        win_lay.setContentsMargins(6, 4, 6, 6)

        row_a = QHBoxLayout()
        row_a.addWidget(QLabel("窗口透明度"))
        self.win_alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.win_alpha_slider.setRange(10, 100)
        self.win_alpha_slider.setValue(int(self.project.window_alpha * 100))
        self.win_alpha_label = QLabel(f"{int(self.project.window_alpha * 100)}%")
        self.win_alpha_label.setFixedWidth(32)
        self.win_alpha_slider.valueChanged.connect(
            lambda v: self.win_alpha_label.setText(f"{v}%"))
        row_a.addWidget(self.win_alpha_slider)
        row_a.addWidget(self.win_alpha_label)
        win_lay.addLayout(row_a)

        row_b = QHBoxLayout()
        row_b.addWidget(QLabel("背景类型"))
        self.win_combo_bg = QComboBox()
        self.win_combo_bg.addItems(["🎨 纯色", "🖼️ 图片", "🌈 渐变", "🌌 动态"])
        bg_map = {"color": "🎨 纯色", "image": "🖼️ 图片", "gradient": "🌈 渐变", "dynamic": "🌌 动态"}
        self.win_combo_bg.setCurrentText(bg_map.get(self.project.background_type, "🎨 纯色"))
        self.win_combo_bg.currentTextChanged.connect(self._on_win_bg_type_changed)
        row_b.addWidget(self.win_combo_bg)
        win_lay.addLayout(row_b)

        self.win_color_row = QWidget()
        row_c = QHBoxLayout(self.win_color_row)
        row_c.setContentsMargins(0, 0, 0, 0)
        row_c.addWidget(QLabel("背景色"))
        self.win_bg_color_btn = QPushButton()
        self.win_bg_color_btn.setFixedSize(38, 24)
        self.win_bg_color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_bg_color_btn.setStyleSheet(
            f"background-color: {self.project.bg_color}; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_bg_color_btn.clicked.connect(self._pick_win_bg_color)
        row_c.addStretch()
        row_c.addWidget(self.win_bg_color_btn)
        win_lay.addWidget(self.win_color_row)

        self.win_grad_row = QWidget()
        row_g = QHBoxLayout(self.win_grad_row)
        row_g.setContentsMargins(0, 0, 0, 0)
        row_g.setSpacing(4)
        self.win_grad_start_btn = QPushButton("起点")
        self.win_grad_start_btn.setFixedSize(54, 24)
        self.win_grad_start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_grad_start_btn.setStyleSheet(
            f"background-color: {self.project.gradient_start}; color: black; font-size: 10px; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_grad_start_btn.clicked.connect(lambda: self._pick_win_color_attr(self.win_grad_start_btn, "grad_start"))
        self.win_grad_end_btn = QPushButton("终点")
        self.win_grad_end_btn.setFixedSize(54, 24)
        self.win_grad_end_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_grad_end_btn.setStyleSheet(
            f"background-color: {self.project.gradient_end}; color: black; font-size: 10px; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_grad_end_btn.clicked.connect(lambda: self._pick_win_color_attr(self.win_grad_end_btn, "grad_end"))
        row_g.addWidget(self.win_grad_start_btn)
        row_g.addWidget(self.win_grad_end_btn)
        win_lay.addWidget(self.win_grad_row)

        self.win_img_row = QWidget()
        img_r = QHBoxLayout(self.win_img_row)
        img_r.setContentsMargins(0, 0, 0, 0)
        img_r.setSpacing(4)
        self.win_combo_image = QComboBox()
        self.win_combo_image.setMinimumHeight(24)
        self._refresh_win_image_list()
        self.win_combo_image.setCurrentText(self.project.background_image)
        self.win_btn_upload_img = QPushButton("📁")
        self.win_btn_upload_img.setFixedSize(34, 24)
        self.win_btn_upload_img.setToolTip("上传图片")
        self.win_btn_upload_img.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_btn_upload_img.clicked.connect(self._upload_win_bg_image)
        img_r.addWidget(self.win_combo_image)
        img_r.addWidget(self.win_btn_upload_img)
        win_lay.addWidget(self.win_img_row)

        self.win_dyn_row = QWidget()
        dyn_r = QHBoxLayout(self.win_dyn_row)
        dyn_r.setContentsMargins(0, 0, 0, 0)
        dyn_r.setSpacing(4)
        self.win_combo_dyn = QComboBox()
        self.win_combo_dyn.setMinimumHeight(24)
        if self.window and hasattr(self.window, 'master'):
            for key, name in self.window.master.dynamic_bg_registry.items():
                self.win_combo_dyn.addItem(name, key)
        idx = self.win_combo_dyn.findData(self.project.dynamic_bg_type)
        if idx >= 0: self.win_combo_dyn.setCurrentIndex(idx)
        self.win_combo_dyn_quality = QComboBox()
        self.win_combo_dyn_quality.setMinimumHeight(24)
        self.win_combo_dyn_quality.addItems(["⚡高", "🌓中", "🐢低"])
        self.win_combo_dyn_quality.setCurrentIndex(
            0 if self.project.dynamic_quality == "high" else
            (1 if self.project.dynamic_quality == "medium" else 2))
        dyn_r.addWidget(self.win_combo_dyn)
        dyn_r.addWidget(self.win_combo_dyn_quality)
        win_lay.addWidget(self.win_dyn_row)

        row_f = QHBoxLayout()
        row_f.addWidget(QLabel("字体颜色"))
        self.win_font_color_btn = QPushButton()
        self.win_font_color_btn.setFixedSize(38, 24)
        self.win_font_color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_font_color_btn.setStyleSheet(
            f"background-color: {self.project.font_color}; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_font_color_btn.clicked.connect(self._pick_win_font_color)
        row_f.addStretch()
        row_f.addWidget(self.win_font_color_btn)
        win_lay.addLayout(row_f)

        right_layout.addWidget(self.win_settings_box)

        self._on_win_bg_type_changed(self.win_combo_bg.currentText())

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 8, 0, 16)
        self.btn_apply = QPushButton("✅ 应用并关闭")
        self.btn_apply.setProperty("primary", True)
        self.btn_apply.clicked.connect(self.apply_and_close)
        self.btn_cancel = QPushButton("❌ 取消")
        self.btn_cancel.setProperty("secondary", True)
        self.btn_cancel.clicked.connect(self.cancel_and_close)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_apply)
        bottom_layout.addWidget(self.btn_cancel)
        right_layout.addLayout(bottom_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(splitter, 1)

        self._populate_element_list()
        self.element_list.setCurrentRow(-1)
        self.no_selection_label.setVisible(True)
        self.prop_scroll.setVisible(False)

    def _update_weather_cities(self, province):
        self.combo_weather_city.blockSignals(True)
        self.combo_weather_city.clear()
        cities = PROVINCE_CITY_DATA.get(province, [])
        self.combo_weather_city.addItems(cities)
        self.combo_weather_city.blockSignals(False)

    def show_plugin_intro(self):
        dlg = PluginIntroductionDialog(self)
        dlg.exec()

    def apply_and_close(self):
        self.project.window_alpha = self.win_alpha_slider.value() / 100.0

        bg_text = self.win_combo_bg.currentText()
        if "图片" in bg_text:
            self.project.background_type = "image"
        elif "渐变" in bg_text:
            self.project.background_type = "gradient"
        elif "动态" in bg_text:
            self.project.background_type = "dynamic"
        else:
            self.project.background_type = "color"

        self.project.bg_color = self.win_bg_color_btn.property("win_bg") or self.project.bg_color
        self.project.gradient_start = self.win_grad_start_btn.property("win_grad_start") or self.project.gradient_start
        self.project.gradient_end = self.win_grad_end_btn.property("win_grad_end") or self.project.gradient_end
        self.project.background_image = self.win_combo_image.currentText() if self.project.background_type == "image" else ""
        self.project.font_color = self.win_font_color_btn.property("win_font") or self.project.font_color

        self.project.dynamic_bg_type = self.win_combo_dyn.currentData()
        qmap = {0: "high", 1: "medium", 2: "low"}
        self.project.dynamic_quality = qmap.get(self.win_combo_dyn_quality.currentIndex(), "high")

        if self.window:
            self.window.apply_custom_layout()
            self.window.setup_dynamic_bg()
            self.window.update()
        self.accept()

    def cancel_and_close(self):
        self.project.custom_layout = self._layout_backup
        if self.window:
            self.window.apply_custom_layout()
        self.reject()

    def _populate_element_list(self):
        self.element_list.blockSignals(True)
        self.element_list.clear()
        layout = self.project.custom_layout or {}
        for elem_id in layout:
            display = ELEMENT_DISPLAY_NAMES.get(elem_id, elem_id)
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, elem_id)
            if not layout[elem_id].get("visible", True):
                item.setText(f"{display} (隐藏)")
            self.element_list.addItem(item)
        self.element_list.blockSignals(False)
        self.element_list.setCurrentRow(-1)
        self.current_elem = None
        self.no_selection_label.setVisible(True)
        self.prop_scroll.setVisible(False)

    def on_element_select(self, row):
        if row < 0:
            self.current_elem = None
            self.no_selection_label.setVisible(True)
            self.prop_scroll.setVisible(False)
            self.btn_remove.setEnabled(False)
            return
        item = self.element_list.item(row)
        if not item: return
        elem_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_elem = elem_id
        self.btn_remove.setEnabled(True)
        self.no_selection_label.setVisible(False)
        self.prop_scroll.setVisible(True)
        self._load_element_properties(elem_id)

        self.weather_section.setVisible(elem_id == "weather")
        self.pomo_section.setVisible(elem_id == "pomodoro")
        self.poem_section.setVisible(elem_id == "poem")
        self.tip_section.setVisible(elem_id == "tip")
        self.static_text_section.setVisible(elem_id == "static_text")
        self.countdown_section.setVisible(elem_id == "countdown")
        self.preview_canvas.set_highlighted_element(elem_id)

    def _update_ui_from_config(self):
        if not self.current_elem:
            return
        self._load_element_properties(self.current_elem)

    def go_to_plugin_help(self):
        if self.window and self.window.master:
            self.window.master.open_settings(tab="help", section="🛠️ 开发插件")

    def _load_element_properties(self, elem_id):
        self._updating_ui = True
        layout = self.project.custom_layout
        elem = layout.get(elem_id, {})

        self.cb_visible.setChecked(elem.get("visible", True))
        self.spin_font_size.setValue(elem.get("font_size", 14))
        font_family = elem.get("font_family", "")
        self.combo_font_family.setCurrentText(font_family if font_family else "Microsoft YaHei")

        color = elem.get("color", "#FFFFFF")
        self.btn_color.setStyleSheet(f"background-color: {{color}}; border-radius: 6px; border: 1px solid {{border_color}};".format(color=color, border_color=get_theme_colors(self.current_theme)['border_color']))
        self.btn_color.setProperty("color_value", color)

        opacity = int(elem.get("opacity", 1.0) * 100)
        self.slider_opacity.setValue(opacity)
        self.label_opacity.setText(f"{opacity}%")

        self.cb_stroke_enable.setChecked(elem.get("stroke_color", "transparent") != "transparent")
        sc = elem.get("stroke_color", "transparent")
        self.btn_stroke_color.setStyleSheet(f"background-color: {{sc}}; border-radius: 4px; border: 1px solid {{border_color}};".format(sc=sc, border_color=get_theme_colors(self.current_theme)['border_color']))
        self.btn_stroke_color.setProperty("color_value", sc)
        self.spin_stroke_width.setValue(elem.get("stroke_width", 0))

        sh_color = elem.get("shadow_color", "#000000")
        self.btn_shadow_color.setStyleSheet(f"background-color: {{sh_color}}; border-radius: 4px; border: 1px solid {{border_color}};".format(sh_color=sh_color, border_color=get_theme_colors(self.current_theme)['border_color']))
        self.btn_shadow_color.setProperty("color_value", sh_color)
        self.spin_shadow_offx.setValue(elem.get("shadow_offset_x", 0))
        self.spin_shadow_offy.setValue(elem.get("shadow_offset_y", 0))
        self.spin_shadow_blur.setValue(elem.get("shadow_blur", 0))

        bg = elem.get("bg_color", "transparent")
        self.btn_bg_color.setStyleSheet(f"background-color: {{bg}}; border-radius: 4px; border: 1px solid {{border_color}};".format(bg=bg, border_color=get_theme_colors(self.current_theme)['border_color']))
        self.btn_bg_color.setProperty("color_value", bg)
        self.spin_bg_radius.setValue(elem.get("bg_radius", 0))

        align_h = elem.get("alignment_h", "center")
        self.combo_align_h.setCurrentIndex(["左", "中", "右"].index(align_h) if align_h in ["左","中","右"] else 1)
        align_v = elem.get("alignment_v", "center")
        self.combo_align_v.setCurrentIndex(["上", "中", "下"].index(align_v) if align_v in ["上","中","下"] else 1)

        if elem_id == "weather":
            city = elem.get("city", "")
            if "-" in city:
                parts = city.split("-")
                province = parts[0]
                real_city = parts[1]
            else:
                province = list(PROVINCE_CITY_DATA.keys())[0]
                real_city = city
            idx = self.combo_weather_province.findText(province)
            if idx >= 0:
                self.combo_weather_province.setCurrentIndex(idx)
                self._update_weather_cities(province)
                cdx = self.combo_weather_city.findText(real_city)
                if cdx >= 0:
                    self.combo_weather_city.setCurrentIndex(cdx)
        if elem_id == "pomodoro":
            self.spin_pomo_work.setValue(elem.get("work_mins", 25))
            self.spin_pomo_break.setValue(elem.get("break_mins", 5))
        if elem_id == "poem":
            self.spin_typewriter.setValue(elem.get("interval", self.project.typewriter_interval))
        if elem_id == "tip":
            tip_interval = elem.get("interval", self.project.tip_interval if hasattr(self.project, 'tip_interval') else self.project.typewriter_interval)
            self.spin_tip_interval.setValue(tip_interval)
        if elem_id == "static_text":
            self.edit_static_text.setText(elem.get("text", ""))
        if elem_id == "countdown":
            self.edit_expired_text.setText(self.project.expired_text)
            fmt_map = {"decimal": 0, "integer": 1, "hms": 2, "custom": 3}
            fmt_idx = fmt_map.get(getattr(self.project, 'display_format', 'decimal'), 0)
            self.combo_display_format.blockSignals(True)
            self.combo_display_format.setCurrentIndex(fmt_idx)
            self.combo_display_format.blockSignals(False)
            self.edit_format_template.setText(getattr(self.project, 'display_format_template', '{days}天 {hours}时 {minutes}分'))
            self.custom_template_row.setVisible(fmt_idx == 3)

        self._updating_ui = False

    def _on_property_changed(self, *args):
        if self._updating_ui or not self.current_elem:
            return
        layout = self.project.custom_layout
        if self.current_elem not in layout:
            layout[self.current_elem] = {}
        elem = layout[self.current_elem]

        elem["visible"] = self.cb_visible.isChecked()
        elem["font_size"] = self.spin_font_size.value()
        elem["font_family"] = self.combo_font_family.currentText()
        elem["color"] = self.btn_color.property("color_value") or "#FFFFFF"
        elem["opacity"] = self.slider_opacity.value() / 100.0
        self.label_opacity.setText(f"{self.slider_opacity.value()}%")

        elem["stroke_color"] = self.btn_stroke_color.property("color_value") if self.cb_stroke_enable.isChecked() else "transparent"
        elem["stroke_width"] = self.spin_stroke_width.value()

        elem["shadow_color"] = self.btn_shadow_color.property("color_value") or "#000000"
        elem["shadow_offset_x"] = self.spin_shadow_offx.value()
        elem["shadow_offset_y"] = self.spin_shadow_offy.value()
        elem["shadow_blur"] = self.spin_shadow_blur.value()

        elem["bg_color"] = self.btn_bg_color.property("color_value") or "transparent"
        elem["bg_radius"] = self.spin_bg_radius.value()

        elem["alignment_h"] = ["左", "中", "右"][self.combo_align_h.currentIndex()]
        elem["alignment_v"] = ["上", "中", "下"][self.combo_align_v.currentIndex()]

        if self.current_elem == "weather":
            province = self.combo_weather_province.currentText()
            city = self.combo_weather_city.currentText()
            elem["city"] = f"{province}-{city}"
            self.project.weather_city = elem["city"]
        if self.current_elem == "pomodoro":
            elem["work_mins"] = self.spin_pomo_work.value()
            elem["break_mins"] = self.spin_pomo_break.value()
            self.project.pomodoro_work = elem["work_mins"]
            self.project.pomodoro_break = elem["break_mins"]
        if self.current_elem == "poem":
            self.project.typewriter_interval = self.spin_typewriter.value()
            elem["interval"] = self.project.typewriter_interval
        if self.current_elem == "tip":
            self.project.tip_interval = self.spin_tip_interval.value()
            elem["interval"] = self.project.tip_interval
        if self.current_elem == "static_text":
            elem["text"] = self.edit_static_text.text()
        if self.current_elem == "countdown":
            self.project.expired_text = self.edit_expired_text.text()
            fmt_map = {0: "decimal", 1: "integer", 2: "hms", 3: "custom"}
            self.project.display_format = fmt_map.get(self.combo_display_format.currentIndex(), "decimal")
            self.project.display_format_template = self.edit_format_template.text()
            if self.window and hasattr(self.window, 'countdown_label'):
                self.window.countdown_label.set_display_format(
                    self.project.display_format, self.project.display_format_template)
                self.window.update_ticking_countdown()

        self.preview_canvas.refresh_layout()
        self._update_list_item_text()
        if self.window:
            self.window.apply_custom_layout()

    def _update_list_item_text(self):
        if not self.current_elem: return
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == self.current_elem:
                display = ELEMENT_DISPLAY_NAMES.get(self.current_elem, self.current_elem)
                if not self.project.custom_layout.get(self.current_elem, {}).get("visible", True):
                    item.setText(f"{display} (隐藏)")
                else:
                    item.setText(display)
                break

    def _pick_color(self):
        current = self.btn_color.property("color_value") or "#FFFFFF"
        color = QColorDialog.getColor(QColor(current), self, "选择颜色")
        if color.isValid():
            self.btn_color.setStyleSheet(f"background-color: {{c}}; border-radius: 6px; border: 1px solid {{bc}};".format(c=color.name(), bc=get_theme_colors(self.current_theme)['border_color']))
            self.btn_color.setProperty("color_value", color.name())
            self._on_property_changed()

    def _pick_color_attr(self, attr_name):
        btn_map = {
            "stroke_color": self.btn_stroke_color,
            "shadow_color": self.btn_shadow_color,
            "bg_color": self.btn_bg_color
        }
        btn = btn_map[attr_name]
        current = btn.property("color_value") or "#000000"
        color = QColorDialog.getColor(QColor(current), self, "选择颜色")
        if color.isValid():
            btn.setStyleSheet(f"background-color: {{c}}; border-radius: 4px; border: 1px solid {{bc}};".format(c=color.name(), bc=get_theme_colors(self.current_theme)['border_color']))
            btn.setProperty("color_value", color.name())
            self._on_property_changed()

    def _on_slider_changed(self, val):
        self.label_opacity.setText(f"{val}%")
        self._on_property_changed()

    def _on_display_format_changed(self, index):
        self.custom_template_row.setVisible(index == 3)
        self._on_property_changed()

    def add_element(self):
        layout = self.project.custom_layout or {}
        existing = set(layout.keys())
        available = [e for e in ALL_AVAILABLE_ELEMENTS if e not in existing]
        available.append("custom_text")
        available.append("custom_image")
        display_items = []
        for e in available:
            if e == "custom_text": display_items.append("📝 自定义文字")
            elif e == "custom_image": display_items.append("🖼️ 自定义图片")
            else: display_items.append(ELEMENT_DISPLAY_NAMES.get(e, e))
        if not display_items:
            QMessageBox.information(self, "提示", "所有可用元素已添加")
            return
        choice, ok = QInputDialog.getItem(self, "添加元素", "选择要添加的元素：", display_items, 0, False)
        if not ok: return
        idx = display_items.index(choice)
        elem_id = available[idx]

        if elem_id == "custom_text":
            text, ok = QInputDialog.getText(self, "自定义文字", "请输入文字内容：")
            if not ok or not text: return
            unique_id = f"custom_text_{int(time.time())}"
            layout[unique_id] = {
                "visible": True, "x": 0.5, "y": 0.5, "font_size": 12, "color": "#FFFFFF", "opacity": 1.0,
                "stroke_color": "transparent", "stroke_width": 0,
                "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 0, "shadow_blur": 0,
                "bg_color": "transparent", "bg_radius": 0,
                "alignment_h": "center", "alignment_v": "center",
                "type": "custom_text", "text": text
            }
            ELEMENT_DISPLAY_NAMES[unique_id] = f"📝 {text[:10]}"
        elif elem_id == "custom_image":
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.gif *.bmp *.webp)")
            if not file_path: return
            import shutil
            filename = os.path.basename(file_path)
            dest_dir = os.path.join(resource_path("data"), "user")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            if not os.path.exists(dest_path):
                shutil.copy(file_path, dest_path)
            unique_id = f"custom_image_{int(time.time())}"
            layout[unique_id] = {
                "visible": True, "x": 0.5, "y": 0.5, "font_size": 12, "color": "#FFFFFF", "opacity": 1.0,
                "stroke_color": "transparent", "stroke_width": 0,
                "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 0, "shadow_blur": 0,
                "bg_color": "transparent", "bg_radius": 0,
                "alignment_h": "center", "alignment_v": "center",
                "type": "custom_image", "image_path": filename
            }
            ELEMENT_DISPLAY_NAMES[unique_id] = f"🖼️ {os.path.basename(file_path)[:10]}"
        else:
            default_positions = {
                "name": (0.5, 0.10), "static_text": (0.5, 0.28),
                "countdown": (0.5, 0.55), "poem": (0.5, 0.80),
                "weather": (0.88, 0.06), "pomodoro": (0.12, 0.06), "tip": (0.5, 0.92)
            }
            pos = default_positions.get(elem_id, (0.5, 0.5))
            layout[elem_id] = {
                "visible": True, "x": pos[0], "y": pos[1], "font_size": 14, "color": "#FFFFFF", "opacity": 1.0,
                "stroke_color": "transparent", "stroke_width": 0,
                "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 0, "shadow_blur": 0,
                "bg_color": "transparent", "bg_radius": 0,
                "alignment_h": "center", "alignment_v": "center",
                "text": ""
            }
        self.project.custom_layout = layout
        self._populate_element_list()

    def remove_element(self):
        if not self.current_elem: return
        if self.current_elem in ("name", "countdown"):
            QMessageBox.warning(self, "提示", "项目名称和倒计时不能删除")
            return
        del self.project.custom_layout[self.current_elem]
        self.current_elem = None
        self._populate_element_list()
        self.preview_canvas.refresh_layout()

    def move_element_up(self):
        row = self.element_list.currentRow()
        if row <= 0: return
        layout = self.project.custom_layout
        keys = list(layout.keys())
        keys[row], keys[row - 1] = keys[row - 1], keys[row]
        self.project.custom_layout = {k: layout[k] for k in keys}
        self._populate_element_list()
        self.element_list.setCurrentRow(row - 1)

    def move_element_down(self):
        row = self.element_list.currentRow()
        if row < 0 or row >= self.element_list.count() - 1: return
        layout = self.project.custom_layout
        keys = list(layout.keys())
        keys[row], keys[row + 1] = keys[row + 1], keys[row]
        self.project.custom_layout = {k: layout[k] for k in keys}
        self._populate_element_list()
        self.element_list.setCurrentRow(row + 1)

    # ---------- 窗口级外观设置方法 ----------
    def _on_win_bg_type_changed(self, text):
        is_color = "纯色" in text
        is_image = "图片" in text
        is_grad = "渐变" in text
        is_dyn = "动态" in text
        self.win_color_row.setVisible(is_color)
        self.win_grad_row.setVisible(is_grad)
        self.win_img_row.setVisible(is_image)
        self.win_dyn_row.setVisible(is_dyn)

    def _pick_win_bg_color(self):
        color = QColorDialog.getColor(QColor(self.project.bg_color), self, "选择窗口背景色")
        if color.isValid():
            self.win_bg_color_btn.setProperty("win_bg", color.name())
            self.win_bg_color_btn.setStyleSheet(
                f"background-color: {color.name()}; border-radius: 4px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']};")

    def _pick_win_color_attr(self, btn, attr_name):
        cur = btn.property(f"win_{attr_name}") or (
            self.project.gradient_start if attr_name == "grad_start" else self.project.gradient_end)
        color = QColorDialog.getColor(QColor(cur), self, "选择颜色")
        if color.isValid():
            btn.setProperty(f"win_{attr_name}", color.name())
            btn.setStyleSheet(
                f"background-color: {color.name()}; color: black; font-size: 10px; border-radius: 4px; "
                f"border: 1px solid {get_theme_colors(self.current_theme)['border_color']};")

    def _pick_win_font_color(self):
        color = QColorDialog.getColor(QColor(self.project.font_color), self, "选择窗口字体颜色")
        if color.isValid():
            self.win_font_color_btn.setProperty("win_font", color.name())
            self.win_font_color_btn.setStyleSheet(
                f"background-color: {color.name()}; border-radius: 4px; border: 1px solid {get_theme_colors(self.current_theme)['border_color']};")

    def _refresh_win_image_list(self):
        self.win_combo_image.clear()
        if not hasattr(self, 'window') or not self.window:
            return
        user_dir = getattr(self.window.master, 'user_dir', '') if hasattr(self.window, 'master') else ''
        if user_dir and os.path.exists(user_dir):
            images = [f for f in os.listdir(user_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            self.win_combo_image.addItems(images)

    def _upload_win_bg_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "上传背景图片", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            import shutil
            filename = os.path.basename(file_path)
            user_dir = getattr(self.window.master, 'user_dir', '') if hasattr(self.window, 'master') else ''
            if user_dir:
                dest_path = os.path.join(user_dir, filename)
                if not os.path.exists(dest_path):
                    shutil.copy(file_path, dest_path)
                self._refresh_win_image_list()
                self.win_combo_image.setCurrentText(filename)

class ProjectEditorDialog(QDialog):
    def __init__(self, app, project, parent=None):
        super().__init__(parent)
        self.app = app
        self.project = project
        self.setStyleSheet(get_theme_qss(self.app.theme))
        self.setWindowTitle(tr("edit_project") + f" - {project.name}")
        self.setMinimumSize(420, 280)
        self.resize(460, 340)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        tc = get_theme_colors(self.app.theme)

        # ---- 项目信息 ----
        grp = QGroupBox("📋 项目信息")
        grp.setStyleSheet(f"""
            QGroupBox {{
                color: {tc['text_color']};
                font-weight: bold; font-size: 13px;
                border: 1px solid {tc['border_color']};
                border-radius: 8px; margin-top: 10px; padding: 14px 10px 10px 10px;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
        """)
        form = QFormLayout(grp)
        form.setSpacing(10)

        self.edit_name = QLineEdit(self.project.name)
        self.edit_name.setMinimumHeight(32)
        self.edit_name.setStyleSheet(f"border-radius: 5px; padding: 4px 8px;")
        form.addRow(tr("project_name") + ":", self.edit_name)

        date_layout = QHBoxLayout()
        date_layout.setSpacing(4)
        self.edit_date = QLineEdit(self.project.target_date)
        self.edit_date.setPlaceholderText("YYYY-MM-DD")
        self.edit_date.setMinimumHeight(32)
        self.edit_date.setStyleSheet(f"border-radius: 5px; padding: 4px 8px;")
        date_layout.addWidget(self.edit_date)

        btn_cal = QPushButton("📅")
        btn_cal.setFixedWidth(36)
        btn_cal.setMinimumHeight(32)
        btn_cal.setToolTip("点击选择日期")
        btn_cal.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cal.setStyleSheet(f"""
            QPushButton {{
                background-color: {tc['input_bg']};
                border: 1px solid {tc['border_color']};
                border-radius: 5px; font-size: 16px;
            }}
            QPushButton:hover {{ background-color: {tc['accent']}; }}
        """)
        btn_cal.clicked.connect(self._show_calendar)
        date_layout.addWidget(btn_cal)
        form.addRow(tr("target_date") + ":", date_layout)

        time_layout = QHBoxLayout()
        time_layout.setSpacing(8)
        self.chk_exact_time = QCheckBox(tr("set_exact_time"))
        self.chk_exact_time.setChecked(self.project.target_time != "00:00")
        self.edit_time = QLineEdit(self.project.target_time if self.project.target_time != "00:00" else "08:00")
        self.edit_time.setEnabled(self.chk_exact_time.isChecked())
        self.edit_time.setMinimumHeight(32)
        self.edit_time.setPlaceholderText("HH:MM")
        self.edit_time.setStyleSheet(f"border-radius: 5px; padding: 4px 8px;")
        self.chk_exact_time.toggled.connect(self.edit_time.setEnabled)
        time_layout.addWidget(self.chk_exact_time)
        time_layout.addWidget(self.edit_time)
        form.addRow(tr("target_time") + ":", time_layout)

        self.chk_show_both = QCheckBox(tr("show_both"))
        self.chk_show_both.setChecked(self.project.show_both)
        self.chk_show_both.setToolTip("同时显示已过天数和剩余天数")
        form.addRow("", self.chk_show_both)

        main_layout.addWidget(grp)

        hint = QLabel("💡 字体、颜色、背景等外观设置请使用「自定义外观编辑器」")
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color: {tc['secondary_text']}; font-size: 11px; padding: 2px 4px;")
        main_layout.addWidget(hint)

        main_layout.addStretch()

        btn_save = QPushButton(tr("save"))
        btn_save.setMinimumHeight(40)
        btn_save.setStyleSheet(
            "background-color: #2ecc71; color: #FFFFFF; padding: 10px 18px; "
            "border-radius: 8px; font-weight: bold; font-size: 14px;")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.save_project)
        main_layout.addWidget(btn_save)

    def _show_calendar(self):
        cal_dlg = QDialog(self)
        cal_dlg.setWindowTitle("选择日期")
        cal_dlg.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        cal_dlg.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        cal_layout = QVBoxLayout(cal_dlg)
        cal_layout.setContentsMargins(4, 4, 4, 4)
        cal = QCalendarWidget()
        cal.setGridVisible(True)
        cal.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        cal.setStyleSheet("""
            QCalendarWidget QToolButton { height: 28px; font-weight: bold; }
            QCalendarWidget QMenu { width: 150px; }
            QCalendarWidget QTableView { selection-background-color: #3498db; }
        """)
        try:
            d = QDate.fromString(self.edit_date.text().strip(), "yyyy-MM-dd")
            if d.isValid():
                cal.setSelectedDate(d)
        except:
            pass
        cal.clicked.connect(lambda qdate: (
            self.edit_date.setText(qdate.toString("yyyy-MM-dd")),
            cal_dlg.accept()
        ))
        cal_layout.addWidget(cal)
        cal_dlg.resize(310, 260)
        pos = self.edit_date.mapToGlobal(self.edit_date.rect().bottomLeft())
        cal_dlg.move(pos + QPoint(0, 4))
        cal_dlg.exec()

    def save_project(self):
        date_str = self.edit_date.text().strip()
        if not validate_date(date_str):
            QMessageBox.critical(self, "错误", "日期格式无效！请使用 YYYY-MM-DD")
            return
        time_str = self.edit_time.text().strip() if self.chk_exact_time.isChecked() else "00:00"
        if self.chk_exact_time.isChecked() and not validate_time(time_str):
            QMessageBox.critical(self, "错误", "时间格式无效！请使用 HH:MM")
            return

        self.project.name = self.edit_name.text().strip()
        self.project.target_date = date_str
        self.project.target_time = time_str
        self.project.show_both = self.chk_show_both.isChecked()

        self.app.save_config(force=True)
        for win in self.app.windows:
            if win.project == self.project:
                win.refresh()
        self.accept()


class DebugConsole(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("控制台")
        self.setMinimumSize(800, 550)
        self.resize(900, 600)

        self.is_root = False
        self.root_eligible = self._check_root_eligible()

        self.log_forward_enabled = False

        self.allowed_dirs = [
            os.path.abspath(self.app.data_dir),
            os.path.abspath(os.path.dirname(self.app.config_path)),
            os.path.abspath(os.getcwd())
        ]
        self.current_work_dir = os.path.abspath(os.getcwd())

        self.history = []
        self.history_pos = -1

        self._setup_ui()
        self._register_commands()
        self._update_log_callback()
        self._show_welcome()

        self.input_line.setFocus()

    def _check_root_eligible(self):
        if sys.platform == "win32":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            return os.geteuid() == 0 if hasattr(os, 'geteuid') else False

    def _is_path_allowed(self, path):
        if self.is_root:
            return True
        abs_path = os.path.abspath(path)
        for allowed in self.allowed_dirs:
            if abs_path.startswith(allowed):
                return True
        return False

    def _setup_ui(self):
        theme = get_system_theme()
        c = get_theme_colors(theme)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme.bg_color};
                color: {c['console_text']};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11pt;
            }}
            QTextEdit {{
                background-color: {c['console_bg']};
                color: {c['console_text']};
                border: none;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11pt;
                selection-background-color: {c['border_color']};
            }}
            QLineEdit {{
                background-color: {c['input_bg']};
                color: {c['console_text']};
                border: 1px solid {c['border_color']};
                border-radius: 4px;
                padding: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11pt;
            }}
            QLineEdit:focus {{
                border: 1px solid {c['input_focus_border']};
            }}
            QCheckBox {{
                color: {c['console_text']};
                font-family: 'Microsoft YaHei', sans-serif;
                font-size: 10pt;
                spacing: 4px;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {c['border_color']};
                border-radius: 2px;
                background: {c['input_bg']};
            }}
            QCheckBox::indicator:checked {{
                background: {c['input_focus_border']};
                border-color: {c['input_focus_border']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 6, 8, 8)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(8)

        self.log_toggle = QCheckBox("📋 日志转发（开启后日志实时显示在控制台）")
        self.log_toggle.setChecked(False)
        self.log_toggle.stateChanged.connect(self._on_log_toggle_changed)
        self.log_toggle.setToolTip("默认关闭：防止日志刷屏覆盖调试信息\n开启后所有 log_message 输出将实时显示在控制台中")
        toolbar_layout.addWidget(self.log_toggle)

        toolbar_layout.addStretch()

        btn_clear = QPushButton("清屏")
        btn_clear.setFixedSize(60, 24)
        btn_clear.setStyleSheet(f"""
            QPushButton {{
                background: {c['input_bg']};
                color: {c['console_text']};
                border: 1px solid {c['border_color']};
                border-radius: 3px;
                font-size: 10pt;
                padding: 2px 6px;
            }}
            QPushButton:hover {{ border-color: {c['input_focus_border']}; }}
        """)
        btn_clear.clicked.connect(lambda: self.output.clear())
        toolbar_layout.addWidget(btn_clear)

        btn_help = QPushButton("帮助")
        btn_help.setFixedSize(60, 24)
        btn_help.setStyleSheet(f"""
            QPushButton {{
                background: {c['input_bg']};
                color: {c['console_text']};
                border: 1px solid {c['border_color']};
                border-radius: 3px;
                font-size: 10pt;
                padding: 2px 6px;
            }}
            QPushButton:hover {{ border-color: {c['input_focus_border']}; }}
        """)
        btn_help.clicked.connect(self.show_help)
        toolbar_layout.addWidget(btn_help)

        layout.addLayout(toolbar_layout)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.output, 1)

        input_layout = QHBoxLayout()
        self.prompt_label = QLabel(">>> ")
        self.prompt_label.setStyleSheet(f"color: {get_theme_colors(get_system_theme())['input_focus_border']}; font-weight: bold;")
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("输入 help 查看命令 | ↑↓ 历史 | Tab 补全")
        self.input_line.returnPressed.connect(self.execute_command)
        self.input_line.installEventFilter(self)
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.input_line)
        layout.addLayout(input_layout)

    def _update_input_style(self):
        c = get_theme_colors(get_system_theme())
        if self.is_root:
            style = f"""
                QLineEdit {{
                    background-color: #ffcccc;
                    color: {c['bg_color']};
                    border: 1px solid #f38ba8;
                    border-radius: 4px;
                    padding: 6px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 11pt;
                    font-weight: bold;
                }}
                QLineEdit:focus {{
                    border: 1px solid {c['input_focus_border']};
                }}
            """
        else:
            style = f"""
                QLineEdit {{
                    background-color: {c['input_bg']};
                    color: {c['console_text']};
                    border: 1px solid {c['border_color']};
                    border-radius: 4px;
                    padding: 6px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 11pt;
                }}
                QLineEdit:focus {{
                    border: 1px solid {c['input_focus_border']};
                }}
            """
        self.input_line.setStyleSheet(style)

    # ---- 日志转发控制 ----

    def _on_log_toggle_changed(self, state):
        self.log_forward_enabled = (state == Qt.CheckState.Checked.value)
        self._update_log_callback()
        status = "已开启" if self.log_forward_enabled else "已关闭"
        self.write_info(f"日志转发 {status}（{'实时显示' if self.log_forward_enabled else '仅写入文件'}）")

    def _update_log_callback(self):
        if self.log_forward_enabled:
            set_console_log_callback(self._on_log_forward)
        else:
            set_console_log_callback(None)

    def _on_log_forward(self, message, level, timestamp):
        short_msg = message[:200] + ("..." if len(message) > 200 else "")
        QTimer.singleShot(0, lambda: self._write_log_entry(short_msg, level, timestamp))

    def _write_log_entry(self, message, level, timestamp):
        color_map = {
            "ERROR": "red",
            "WARNING": "yellow",
            "INFO": "green",
            "DEBUG": "cyan",
        }
        c = color_map.get(level, "white")
        short_msg = message[:200] + ("..." if len(message) > 200 else "")
        self.write(f"[{timestamp}] [{level}] {short_msg}", color=c)


    def eventFilter(self, obj, event):
        if obj == self.input_line and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Up:
                if self.history_pos > 0:
                    self.history_pos -= 1
                    self.input_line.setText(self.history[self.history_pos])
                return True
            elif event.key() == Qt.Key.Key_Down:
                if self.history_pos < len(self.history) - 1:
                    self.history_pos += 1
                    self.input_line.setText(self.history[self.history_pos])
                elif self.history_pos == len(self.history) - 1:
                    self.history_pos = len(self.history)
                    self.input_line.clear()
                return True
            elif event.key() == Qt.Key.Key_Tab:
                self._tab_complete()
                return True
        return super().eventFilter(obj, event)

    def _tab_complete(self):
        """Tab 键补全命令"""
        text = self.input_line.text().strip()
        if not text:
            return
        builtin_cmds = ["help", "root", "exit", "quit", "exit()", "quit()",
                        "read_file", "write_file", "ls", "pwd", "cd", "classes",
                        "restart", "clear_cache", "perf_info", "close_window",
                        "open_settings", "backup_config", "theme_info",
                        "app_info", "list_threads", "gc_collect", "clear"]
        registered_funcs = [k for k in self.locals.keys() if callable(self.locals.get(k)) and not k.startswith("_")]
        all_cmds = builtin_cmds + registered_funcs
        matches = [c for c in all_cmds if c.startswith(text)]
        if len(matches) == 1:
            self.input_line.setText(matches[0] + " ")
        elif len(matches) > 1:
            self.write("可能的补全:", color="cyan")
            for m in sorted(matches)[:15]:
                self.write(f"  {m}", color="white")

    def closeEvent(self, event):
        set_console_log_callback(None)
        super().closeEvent(event)

    def write(self, text, color="white", newline=True):
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        color_map = {
            "white": "#cdd6f4",
            "red": "#f38ba8",
            "green": "#a6e3a1",
            "cyan": "#89dceb",
            "yellow": "#f9e2af",
            "magenta": "#cba6f7",
        }
        hex_color = color_map.get(color, "#cdd6f4")
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(hex_color))
        cursor.insertText(str(text), fmt)
        if newline:
            cursor.insertText("\n", fmt)

        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    def write_error(self, text):   self.write(text, "red")
    def write_success(self, text): self.write(text, "green")
    def write_info(self, text):    self.write(text, "cyan")
    def write_warning(self, text): self.write(text, "yellow")

    def execute_command(self):
        cmd = self.input_line.text().strip()
        if not cmd:
            self.write(">>> ", newline=False)
            return

        self.input_line.clear()
        self.write(f">>> {cmd}")

        self.history.append(cmd)
        self.history_pos = len(self.history)

        cmd_lower = cmd.lower()

        if cmd_lower == "mrx":
            self.write("苗睿轩牛逼 ✨", color="magenta")
        elif cmd_lower == "help":
            self.show_help()
        elif cmd_lower == "root":
            self._cmd_root()
        elif cmd_lower in ("exit", "exit()", "quit", "quit()"):
            self.close()
        elif cmd_lower == "clear":
            self.output.clear()
        elif cmd_lower == "restart":
            self._cmd_restart()
        elif cmd_lower == "clear_cache":
            self._cmd_clear_cache()
        elif cmd_lower == "perf_info":
            self._cmd_perf_info()
        elif cmd_lower == "theme_info":
            self._cmd_theme_info()
        elif cmd_lower == "app_info":
            self._cmd_app_info()
        elif cmd_lower == "list_threads":
            self._cmd_list_threads()
        elif cmd_lower == "backup_config":
            self._cmd_backup_config()
        elif cmd_lower == "open_settings":
            self._cmd_open_settings()
        elif cmd_lower == "toggle_log":
            self._cmd_toggle_log()
        elif cmd_lower.startswith("close_window"):
            arg = cmd[13:].strip()
            self._cmd_close_window(arg if arg else None)
        elif cmd_lower.startswith("read_file "):
            self._cmd_read_file(cmd[10:].strip())
        elif cmd_lower.startswith("write_file "):
            parts = cmd[11:].strip().split(maxsplit=1)
            if len(parts) == 2:
                self._cmd_write_file(parts[0], parts[1])
            else:
                self.write_error("用法: write_file <路径> <内容>")
        elif cmd_lower.startswith("ls "):
            self._cmd_ls(cmd[3:].strip() or ".")
        elif cmd_lower == "pwd":
            self._cmd_pwd()
        elif cmd_lower.startswith("cd "):
            self._cmd_cd(cmd[3:].strip())
        elif cmd_lower.startswith("classes"):
            arg = cmd[7:].strip()
            self._cmd_classes(arg if arg else None)
        else:
            self._exec_python(cmd)

        self.write(">>> ", newline=False)

    def _cmd_root(self):
        if self.is_root:
            self.write_warning("已经处于 ROOT 模式。")
            return
        if self.root_eligible:
            self.is_root = True
            self._update_input_style()
            self.write_success("权限已提升")
        else:
            self.write_error("权限不足")

    def _cmd_read_file(self, path):
        if not path:
            self.write_error("请指定文件路径。")
            return
        try:
            abs_path = os.path.abspath(os.path.join(self.current_work_dir, path))
            if not self._is_path_allowed(abs_path):
                self.write_error("权限不足：无法读取该文件")
                return
            if not os.path.exists(abs_path):
                self.write_error(f"文件不存在: {abs_path}")
                return
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.write(f"文件内容 ({abs_path}):", color="cyan")
            if len(content) > 5000:
                content = content[:5000] + "\n... (内容过长，仅显示前5000字符)"
            self.write(content, color="white")
        except Exception as e:
            self.write_error(f"读取文件失败: {e}")

    def _cmd_write_file(self, path, content):
        if not path:
            self.write_error("请指定文件路径。")
            return
        try:
            abs_path = os.path.abspath(os.path.join(self.current_work_dir, path))
            if not self._is_path_allowed(abs_path):
                self.write_error("权限不足：无法写入该文件")
                return
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.write_success(f"已写入文件: {abs_path}")
        except Exception as e:
            self.write_error(f"写入文件失败: {e}")

    def _cmd_ls(self, path):
        try:
            target = os.path.abspath(os.path.join(self.current_work_dir, path))
            if not self._is_path_allowed(target):
                self.write_error("权限不足：无法列出目录内容")
                return
            if not os.path.isdir(target):
                self.write_error(f"路径不是目录: {target}")
                return
            items = os.listdir(target)
            self.write(f"目录 {target} 的内容:", color="cyan")
            for item in sorted(items):
                full = os.path.join(target, item)
                if os.path.isdir(full):
                    self.write(f"  📁 {item}/", color="yellow")
                else:
                    size = os.path.getsize(full)
                    self.write(f"  📄 {item} ({size} bytes)", color="white")
        except Exception as e:
            self.write_error(f"列出目录失败: {e}")

    def _cmd_pwd(self):
        self.write(f"当前工作目录: {self.current_work_dir}", color="green")

    def _cmd_cd(self, path):
        if not path:
            self.write_error("请指定目录。")
            return
        try:
            new_dir = os.path.abspath(os.path.join(self.current_work_dir, path))
            if not self._is_path_allowed(new_dir):
                self.write_error("权限不足：无法切换到该目录")
                return
            if not os.path.isdir(new_dir):
                self.write_error(f"目录不存在: {new_dir}")
                return
            self.current_work_dir = new_dir
            self.write_success(f"工作目录已切换至: {self.current_work_dir}")
        except Exception as e:
            self.write_error(f"切换目录失败: {e}")

    def _cmd_classes(self, obj_name):
        if obj_name is None:
            classes = []
            for name, obj in globals().items():
                if isinstance(obj, type):
                    classes.append(name)
            for name, obj in self.locals.items():
                if isinstance(obj, type) and name not in classes:
                    classes.append(name)
            classes.sort()
            self.write(f"当前环境中定义的类（共 {len(classes)} 个）:", color="cyan")
            for cls_name in classes:
                self.write(f"  {cls_name}", color="white")
        else:
            try:
                obj = None
                if obj_name in self.locals:
                    obj = self.locals[obj_name]
                elif obj_name in globals():
                    obj = globals()[obj_name]
                else:
                    obj = eval(obj_name, globals(), self.locals)
                if obj is None:
                    self.write_error(f"找不到对象: {obj_name}")
                    return
                self.write(f"对象: {obj_name}", color="cyan")
                self.write(f"类型: {type(obj).__name__}", color="green")
                self.write("继承链:", color="cyan")
                for cls in type(obj).__mro__:
                    self.write(f"  ↳ {cls.__name__}", color="white")
                methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
                if methods:
                    self.write(f"公共方法 ({len(methods)}):", color="cyan")
                    for m in methods[:30]:
                        self.write(f"  {m}()", color="white")
                    if len(methods) > 30:
                        self.write(f"  ... 还有 {len(methods)-30} 个方法未显示", color="yellow")
            except Exception as e:
                self.write_error(f"获取类信息失败: {e}")

    def _exec_python(self, code):
        try:
            if "=" in code and not code.strip().startswith(("if","for","while","def","import")):
                exec(code, globals(), self.locals)
            else:
                result = eval(code, globals(), self.locals)
                if result is not None:
                    self.write(repr(result), color="magenta")
        except Exception as e:
            self.write_error(f"{type(e).__name__}: {e}")


    def _cmd_restart(self):
        reply = QMessageBox.question(
            self, "确认重启", "确定要重启应用程序吗？\n所有未保存的更改将先保存。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.write_warning("正在重启应用...")
            self.close()
            self.app.restart_application()

    def _cmd_clear_cache(self):
        """清理缓存"""
        cache_dirs = []
        data_dir = self.app.data_dir
        import shutil
        cleared = 0
        cleared_size = 0

        pycache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__")
        if os.path.isdir(pycache):
            size = sum(os.path.getsize(os.path.join(pycache, f)) for f in os.listdir(pycache) if os.path.isfile(os.path.join(pycache, f)))
            shutil.rmtree(pycache, ignore_errors=True)
            cleared += 1
            cleared_size += size

        for fname in os.listdir(data_dir):
            if fname.endswith(('.tmp', '.cache', '.bak')):
                fpath = os.path.join(data_dir, fname)
                try:
                    cleared_size += os.path.getsize(fpath)
                    os.remove(fpath)
                    cleared += 1
                except:
                    pass

        if cleared > 0:
            self.write_success(f"缓存清理完成：移除了 {cleared} 个项目，释放 {cleared_size / 1024:.1f} KB")
        else:
            self.write_info("没有需要清理的缓存")

        # 垃圾回收
        import gc
        gc.collect()
        self.write_info("已执行垃圾回收 (gc.collect)")

    def _cmd_perf_info(self):
        import threading, gc
        import time

        self.write("═══ 性能信息 ═══", color="cyan")

        try:
            import psutil
            process = psutil.Process()
            mem = process.memory_info()
            self.write(f"物理内存: {mem.rss / 1024 / 1024:.1f} MB", color="green")
            self.write(f"虚拟内存: {mem.vms / 1024 / 1024:.1f} MB", color="green")
            cpu_percent = process.cpu_percent(interval=0.1)
            self.write(f"CPU 使用率: {cpu_percent:.1f}%", color="green")
            self.write(f"线程数: {process.num_threads()}", color="green")
            self.write(f"打开文件数: {len(process.open_files())}", color="green")
        except ImportError:
            self.write_warning("psutil 未安装，无法获取详细性能信息")
            self.write("提示: pip install psutil 安装后可查看详细性能", color="yellow")


        self.write(f"活跃线程数: {threading.active_count()}", color="green")
        self.write(f"GC 对象计数: {len(gc.get_objects())}", color="green")
        self.write(f"引用计数阈值: {gc.get_threshold()}", color="green")

        wins = self.app.windows
        visible = sum(1 for w in wins if w.isVisible())
        self.write(f"悬浮窗: {visible}/{len(wins)} 可见", color="green")

        try:
            has_settings = hasattr(self.app, 'settings_dlg') and self.app.settings_dlg and self.app.settings_dlg.isVisible()
            self.write(f"设置窗口: {'已打开' if has_settings else '已关闭'}", color="green")
        except RuntimeError:
            self.write("设置窗口: 已关闭", color="green")

    def _cmd_theme_info(self):
        """显示当前主题信息"""
        theme = get_system_theme()
        c = get_theme_colors(theme)
        self.write("═══ 主题信息 ═══", color="cyan")
        self.write(f"系统深色模式: {'是' if is_system_dark() else '否'}", color="green")
        self.write(f"当前主题名: {theme.name if hasattr(theme, 'name') else '默认'}", color="green")
        self.write(f"背景色: {theme.bg_color}", color="white")
        self.write(f"前景色: {theme.fg_color if hasattr(theme, 'fg_color') else 'N/A'}", color="white")
        self.write(f"强调色: {c.get('accent', 'N/A')}", color="white")
        self.write(f"控制台背景: {c.get('console_bg', 'N/A')}", color="white")
        self.write(f"控制台文字: {c.get('console_text', 'N/A')}", color="white")
        self.write(f"边框色: {c.get('border_color', 'N/A')}", color="white")
        self.write(f"输入框背景: {c.get('input_bg', 'N/A')}", color="white")

    def _cmd_app_info(self):
        self.write("═══ 应用信息 ═══", color="cyan")
        self.write(f"应用版本: {self.app.current_version}", color="green")
        self.write(f"Python: {sys.version}", color="green")
        self.write(f"平台: {platform.platform()}", color="green")
        self.write(f"处理器: {platform.processor()}", color="green")
        self.write(f"架构: {platform.architecture()[0]}", color="green")
        self.write(f"数据目录: {self.app.data_dir}", color="green")
        self.write(f"配置文件: {self.app.config_path}", color="green")
        self.write(f"工作目录: {os.getcwd()}", color="green")
        self.write(f"是否打包: {'是' if getattr(sys, 'frozen', False) else '否（开发模式）'}", color="green")
        self.write(f"DEBUG_MODE: {DEBUG_MODE}", color="green")

        projects = self.app.projects
        self.write(f"项目数: {len(projects)}", color="green")

        pm = self.app.plugin_manager
        enabled = sum(1 for p in pm.plugins if p.enabled)
        self.write(f"插件: {enabled}/{len(pm.plugins)} 已启用", color="green")

        self.write(f"Qt 版本: {qVersion()}", color="green")
        self.write(f"PyQt 版本: {PYQT_VERSION_STR}", color="green")

    def _cmd_list_threads(self):
        import threading
        self.write("═══ 活跃线程 ═══", color="cyan")
        for t in threading.enumerate():
            daemon = "守护" if t.daemon else "普通"
            alive = "运行中" if t.is_alive() else "已停止"
            self.write(f"  [{daemon}] {t.name} ({alive})", color="white")
        self.write(f"共 {threading.active_count()} 个线程", color="green")

    def _cmd_backup_config(self):
        config_path = self.app.config_path
        if not os.path.exists(config_path):
            self.write_error(f"配置文件不存在: {config_path}")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.app.data_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"config_backup_{timestamp}.json")
        try:
            import shutil
            shutil.copy2(config_path, backup_path)
            self.write_success(f"配置已备份到: {backup_path}")
            # 列出所有备份
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("config_backup_")], reverse=True)
            if len(backups) > 1:
                self.write(f"历史备份 ({len(backups)} 个):", color="cyan")
                for b in backups[:5]:
                    self.write(f"  {b}", color="white")
        except Exception as e:
            self.write_error(f"备份失败: {e}")

    def _cmd_open_settings(self):
        self.write_info("正在打开设置窗口...")
        self.app.open_settings()

    def _cmd_toggle_log(self):
        new_state = not self.log_forward_enabled
        self.log_toggle.setChecked(new_state)
        self._on_log_toggle_changed(
            Qt.CheckState.Checked.value if new_state else Qt.CheckState.Unchecked.value
        )

    def _cmd_close_window(self, index_str):
        wins = self.app.windows
        if not index_str:
            self.write("当前悬浮窗:", color="cyan")
            for i, w in enumerate(wins):
                status = "可见" if w.isVisible() else "隐藏"
                self.write(f"  [{i}] {w.project.name} ({status})", color="white")
            self.write_info("用法: close_window <索引>")
            return
        try:
            idx = int(index_str)
            if 0 <= idx < len(wins):
                w = wins[idx]
                name = w.project.name
                w.close()
                self.write_success(f"已关闭悬浮窗 [{idx}] {name}")
            else:
                self.write_error(f"索引超出范围 (0-{len(wins)-1})")
        except ValueError:
            self.write_error(f"无效索引: {index_str}")

    def _register_commands(self):
        self.locals = {
            "app": self.app,
            "console": self,
            "QApplication": QApplication,
            "Qt": Qt,
            "os": os,
            "sys": sys,
            "json": json,
            "platform": platform,
            "getpass": getpass,
        }
        try:
            import psutil
            self.locals["psutil"] = psutil
        except ImportError:
            pass

        def list_windows():
            wins = self.app.windows
            self.write(f"共有 {len(wins)} 个悬浮窗:")
            for i, w in enumerate(wins):
                self.write(f"  [{i}] {w.project.name} | pos=({w.x()},{w.y()}) size={w.width()}x{w.height()} visible={w.isVisible()}")
        self.locals["list_windows"] = list_windows

        def show_windows():
            for w in self.app.windows:
                w.show()
            self.write_success("所有悬浮窗已显示")
        self.locals["show_windows"] = show_windows

        def hide_windows():
            for w in self.app.windows:
                w.hide()
            self.write_success("所有悬浮窗已隐藏")
        self.locals["hide_windows"] = hide_windows

        def refresh_windows():
            for w in self.app.windows:
                w.refresh()
            self.write_success("所有悬浮窗已刷新")
        self.locals["refresh_windows"] = refresh_windows

        def set_window_alpha(alpha):
            try:
                a = float(alpha)
                a = max(0.1, min(1.0, a))
                for w in self.app.windows:
                    w.set_alpha(a)
                self.write_success(f"所有悬浮窗透明度已设置为 {a}")
            except:
                self.write_error("用法: set_window_alpha(0.8)")
        self.locals["set_window_alpha"] = set_window_alpha

        def get_focused_window():
            focused = QApplication.focusWidget()
            self.write(f"当前焦点控件: {focused}")
        self.locals["get_focused_window"] = get_focused_window

        def list_projects():
            projects = self.app.projects
            self.write(f"共有 {len(projects)} 个项目:")
            for i, p in enumerate(projects):
                self.write(f"  [{i}] {p.name} | 目标: {p.target_date} {p.target_time}")
        self.locals["list_projects"] = list_projects

        def current_project(index=None):
            if index is None:
                self.write_warning("当前项目索引? 请调用 list_projects() 查看")
            else:
                try:
                    idx = int(index)
                    if 0 <= idx < len(self.app.projects):
                        proj = self.app.projects[idx]
                        self.write(f"当前选定项目: {proj.name}")
                        return proj
                    else:
                        self.write_error("索引超出范围")
                except:
                    self.write_error("用法: current_project(索引)")
        self.locals["current_project"] = current_project

        def dump_project(index):
            try:
                proj = self.app.projects[int(index)]
                self.write(json.dumps(proj.to_dict(), indent=2, ensure_ascii=False))
            except:
                self.write_error("用法: dump_project(索引)")
        self.locals["dump_project"] = dump_project

        def save_config():
            self.app.save_config(force=True)
            self.write_success("配置已保存")
        self.locals["save_config"] = save_config

        def reload_theme():
            self.app.theme = get_system_theme()
            self.app.setStyleSheet(get_theme_qss(self.app.theme))
            for w in self.app.windows:
                w.refresh(theme_change=True)
            self.write_success("主题已重新加载")
        self.locals["reload_theme"] = reload_theme

        def set_debug_level(level):
            global DEBUG_MODE
            DEBUG_MODE = int(level)
            self.app.save_config()
            self.write_success(f"调试等级设置为 {DEBUG_MODE}")
        self.locals["set_debug_level"] = set_debug_level

        def plugins():
            pm = self.app.plugin_manager
            self.write(f"插件数量: {len(pm.plugins)}")
            for p in pm.plugins:
                status = "启用" if p.enabled else "禁用"
                perms = []
                if p.permissions & PluginPermission.FILE_READ: perms.append("📖")
                if p.permissions & PluginPermission.FILE_WRITE: perms.append("📝")
                if p.permissions & PluginPermission.NETWORK: perms.append("🌐")
                if p.permissions & PluginPermission.COMMAND: perms.append("⚡")
                self.write(f"  {p.name} v{p.version} [{status}] 权限: {' '.join(perms) or '无'}")
        self.locals["plugins"] = plugins

        def enable_plugin(name):
            for p in self.app.plugin_manager.plugins:
                if p.name == name:
                    self.app.plugin_manager.enable_plugin(p)
                    self.write_success(f"已启用插件: {name}")
                    return
            self.write_error(f"未找到插件: {name}")
        self.locals["enable_plugin"] = enable_plugin

        def disable_plugin(name):
            for p in self.app.plugin_manager.plugins:
                if p.name == name:
                    self.app.plugin_manager.disable_plugin(p)
                    self.write_success(f"已禁用插件: {name}")
                    return
            self.write_error(f"未找到插件: {name}")
        self.locals["disable_plugin"] = disable_plugin

        def reload_plugins():
            self.app.plugin_manager.load_plugins()
            self.write_success("插件已重新加载")
        self.locals["reload_plugins"] = reload_plugins

        def plugin_mgr():
            try:
                sys.path.insert(0, self.app.plugin_manager.plugin_dir)
                from extra_plugin import PluginManager as EPM, PluginManagerDialog
                mgr = EPM(self.app)
                mgr.plugin_dir = self.app.plugin_manager.plugin_dir
                mgr.data_dir = self.app.data_dir
                dlg = PluginManagerDialog(mgr, self.settings_dlg if hasattr(self, 'settings_dlg') and self.settings_dlg else None)
                dlg.setWindowTitle("Enhanced Plugin Manager")
                dlg.show()
                self.write_success("Plugin Manager opened")
            except Exception as e:
                import traceback
                self.write_error(f"Failed: {e}\n{traceback.format_exc()}")
        self.locals["plugin_mgr"] = plugin_mgr

        def sys_info():
            import platform
            self.write(f"系统: {platform.platform()}")
            self.write(f"Python: {sys.version}")
            self.write(f"应用版本: {self.app.current_version}")
            self.write(f"数据目录: {self.app.data_dir}")
        self.locals["sys_info"] = sys_info

        def get_username():
            import getpass
            self.write(f"当前用户名: {getpass.getuser()}")
        self.locals["get_username"] = get_username

        def check_admin():
            is_admin = False
            if sys.platform == "win32":
                try:
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    is_admin = False
            else:
                is_admin = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
            self.write(f"管理员权限: {'是' if is_admin else '否'}")
        self.locals["check_admin"] = check_admin

        def get_screen_info():
            screen = QApplication.primaryScreen()
            geom = screen.geometry()
            avail = screen.availableGeometry()
            dpi = screen.logicalDotsPerInch()
            self.write(f"屏幕分辨率: {geom.width()}x{geom.height()}")
            self.write(f"可用区域: {avail.width()}x{avail.height()}")
            self.write(f"DPI: {dpi:.1f}")
        self.locals["get_screen_info"] = get_screen_info

        def check_disk_space(path=None):
            if path is None:
                path = self.app.data_dir
            import shutil
            usage = shutil.disk_usage(path)
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            self.write(f"路径: {path}")
            self.write(f"剩余空间: {free_gb:.2f} GB / 总计: {total_gb:.2f} GB")
        self.locals["check_disk_space"] = check_disk_space

        def get_env(var_name):
            val = os.environ.get(var_name, "未设置")
            self.write(f"{var_name} = {val}")
        self.locals["get_env"] = get_env

        def log(message, level="INFO"):
            log_message(message, level)
            self.write(f"[LOG][{level}] {message}")
        self.locals["log"] = log

        def show_log(limit=50):
            log_file = os.path.join(self.app.data_dir, "LOG.txt")
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines[-int(limit):]:
                    self.write(line.rstrip())
            else:
                self.write_error("日志文件不存在")
        self.locals["show_log"] = show_log

        def clear_log():
            log_file = os.path.join(self.app.data_dir, "LOG.txt")
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("")
            self.write_success("日志已清空")
        self.locals["clear_log"] = clear_log

        def exec_code(code):
            try:
                exec(code, globals(), self.locals)
            except Exception as e:
                self.write_error(f"执行错误: {e}")
        self.locals["exec_code"] = exec_code

        def restart():
            self.write_warning("正在重启...")
            self.app.restart_application()
        self.locals["restart"] = restart

        def exit_app():
            self.write_warning("正在退出...")
            self.app.quit_app()
        self.locals["exit"] = exit_app

        def refresh_weather():
            for w in self.app.windows:
                if hasattr(w, 'weather_fetcher') and w.weather_fetcher:
                    w.weather_fetcher.fetch(w.project.weather_city)
            self.write_success("天气已强制刷新")
        self.locals["refresh_weather"] = refresh_weather

        def test_notification():
            tray = QSystemTrayIcon(self.app)
            tray.setIcon(QIcon())
            tray.showMessage("调试通知", "这是一条测试通知", QSystemTrayIcon.MessageIcon.Information, 3000)
            self.write_info("已发送测试通知（可能需要托盘图标支持）")
        self.locals["test_notification"] = test_notification

        def clear_screen():
            self.output.clear()
        self.locals["clear_screen"] = clear_screen

        def list_all_shortcuts():
            self.show_help()
        self.locals["list_all_shortcuts"] = list_all_shortcuts

        self.locals["list_all_shortcuts"] = list_all_shortcuts

    def show_help(self):
        help_text = """
  ╔══════════════════════════ 控制台命令列表 ═══════════════════════════╗
  ║  版本: V1.0.4
  ╚══════════════════════════════════════════════════════════════════╝

  ┌──【内建命令】（直接输入，无需括号）────────────────────────────┐
  │  help             显示此帮助文档                      
  │  clear            清空控制台输出                      
  │  root             提升权限（需管理员）                   
  │  exit / quit      关闭控制台                        
  │  restart          重启应用程序（会先保存配置）               
  │  clear_cache      清理缓存 + 垃圾回收                  
  │  perf_info        显示性能信息（内存/CPU/线程/窗口）         
  │  app_info         显示应用详细信息（版本/路径/Qt/Python）    
  │  theme_info       显示当前主题配色详情                   
  │  list_threads     列出所有活跃线程                     
  │  backup_config    备份当前配置文件到 backups/ 目录        
  │  open_settings    打开设置窗口                       
  │  close_window [N] 关闭指定悬浮窗（不传参数列出所有窗口）        
  │  toggle_log       切换日志转发开关（同顶部复选框）             
  │  read_file <路径> 读取文件内容（最多显示 5000 字符）           
  │  write_file <路径> <内容>  写入文件                    
  │  ls [路径]        列出目录内容                         
  │  pwd              显示当前工作目录                     
  │  cd <目录>        切换工作目录                         
  │  classes [类名]   列出所有类 / 查看类的继承链和方法             
  └───────────────────────────────────────────────────────────┘

  ┌──【窗口操作】──────────────────────────────────────────────────┐
  │  list_windows()        列出所有悬浮窗                       
  │  show_windows()        显示所有悬浮窗                       
  │  hide_windows()        隐藏所有悬浮窗                       
  │  refresh_windows()     刷新所有悬浮窗                       
  │  set_window_alpha(0.8) 设置悬浮窗透明度 (0.1~1.0)            
  │  get_focused_window()  获取当前焦点控件                      
  └───────────────────────────────────────────────────────────────┘

  ┌──【项目管理】──────────────────────────────────────────────────┐
  │  list_projects()       列出所有项目                          
  │  current_project(N)    查看/设置当前项目                       
  │  dump_project(N)       打印项目完整配置 (JSON)                 
  └──────────────────────────────────────────────────────────────┘

  ┌──【配置与主题】────────────────────────────────────────────────┐
  │  save_config()         保存配置                               
  │  reload_theme()        重新加载主题                             
  │  set_debug_level(N)    设置调试等级 (0=关闭 1=错误 2=信息 3=详细)
  │  backup_config         备份当前配置                             
  └─────────────────────────────────────────────────────────────┘

  ┌──【插件管理】──────────────────────────────────────────────────┐
  │  plugins()             列出所有插件（含权限状态）               
  │  enable_plugin("名")   启用指定插件                            
  │  disable_plugin("名")  禁用指定插件                            
  │  reload_plugins()      重新加载所有插件                         
  │  plugin_mgr()          打开增强插件管理器                       
  └─────────────────────────────────────────────────────────────┘

  ┌──【系统与性能】────────────────────────────────────────────────┐
  │  sys_info()            系统基本信息                           
  │  get_username()        当前用户名                            
  │  check_admin()         检查管理员权限                          
  │  get_screen_info()     屏幕分辨率/DPI                        
  │  check_disk_space()    磁盘剩余空间                           
  │  get_env("PATH")       查看环境变量                           
  │  perf_info             性能概览（需 psutil）                   
  │  list_threads          活跃线程列表                           
  └──────────────────────────────────────────────────────────────┘

  ┌──【日志操作】──────────────────────────────────────────────────┐
  │  log("msg","INFO")     手动写入日志            
  │  show_log(50)          显示最近 N 行日志        
  │  clear_log()           清空日志文件            
  │  clear_screen()        清空控制台显示           
  │  clear                 清屏（内建命令）          
  │  toggle_log            切换日志实时转发到控制台      
  │  📋 顶部复选框         开启/关闭日志转发（默认关闭防刷屏）      
  └──────────────────────────────────────────────────────────────┘

  ┌──【其他工具】──────────────────────────────────────────────────┐
  │  refresh_weather()     强制刷新天气                           
  │  test_notification()   发送测试系统通知                       
  │  exec_code("代码")     执行任意 Python 代码                   
  │  restart               重启应用                               
  │  exit / quit           退出应用                               
  └─────────────────────────────────────────────────────────────┘

  ┌──【快捷操作提示】──────────────────────────────────────────────┐
  │  ↑↓  浏览命令历史                                         
  │  Tab 命令自动补全                                         
  │  任意 Python 表达式均可执行: 1+2, len(app.windows), dir(app) 
  │  app.windows[0].project.name  获取第一个窗口的项目名           
  └─────────────────────────────────────────────────────────────┘
  ══════════════════════════════════════════════════════════════════
    """
        for line in help_text.splitlines():
            self.write(line, color="white")

    def _show_welcome(self):
        username = getpass.getuser()
        self.write(f"Python {sys.version.split()[0]}  Countdown 调试控制台 V1.0.4", color="cyan")
        self.write(f"用户: {username}", color="yellow")

        if username.lower() == "guzhi":
            self.write("你好，开发者：GuZhi，欢迎您", color="magenta")

        if self.root_eligible:
            self.write_success("保留所有权限")
        else:
            self.write_warning("保留有限权限")

        self.write(f"日志转发: {'开启（日志会实时显示）' if self.log_forward_enabled else '关闭（推荐：防止刷屏）'}", color="green")
        self.write("输入 'help' 查看命令列表 | ↑↓ 历史 | Tab 补全 | 版本: V2.0.0", color="green")
        self.write(">>> ", newline=False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.history_pos > 0:
                self.history_pos -= 1
                self.input_line.setText(self.history[self.history_pos])
        elif event.key() == Qt.Key.Key_Down:
            if self.history_pos < len(self.history) - 1:
                self.history_pos += 1
                self.input_line.setText(self.history[self.history_pos])
            else:
                self.history_pos = len(self.history)
                self.input_line.clear()
        else:
            super().keyPressEvent(event)

class HelpTab(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setFixedWidth(280)
        self.nav_tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {get_theme_colors(self.app.theme)['tree_bg']};
                color: {get_theme_colors(self.app.theme)['tree_text']};
                border-right: 1px solid {get_theme_colors(self.app.theme)['border_color']};
                font-size: 13px;
            }}
            QTreeWidget::item {{
                padding: 6px 4px;
            }}
            QTreeWidget::item:selected {{
                background-color: {get_theme_colors(self.app.theme)['accent']};
                color: white;
            }}
            QTreeWidget::item:hover {{
                background-color: {get_theme_colors(self.app.theme)['border_color']};
            }}
        """)
        layout.addWidget(self.nav_tree)

        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setStyleSheet(f"QScrollArea {{ border: none; background: {get_theme_colors(self.app.theme)['dark_bg']}; }}")
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_label.setStyleSheet(f"color: {get_theme_colors(self.app.theme)['text_color']}; font-size: 14px; padding: 20px;")
        self.content_label.setOpenExternalLinks(False)
        self.content_label.linkActivated.connect(self.on_link_clicked)
        self.content_area.setWidget(self.content_label)
        layout.addWidget(self.content_area, 1)

        self.build_help_data()
        self.nav_tree.currentItemChanged.connect(self.on_nav_selected)

        if self.nav_tree.topLevelItemCount() > 0:
            self.nav_tree.setCurrentItem(self.nav_tree.topLevelItem(0))

    def build_help_data(self):
        quick = QTreeWidgetItem(["🚀 快速入门"])
        QTreeWidgetItem(quick, ["📌 欢迎与概览"])
        QTreeWidgetItem(quick, ["🖱️ 悬浮窗操作指南"])
        QTreeWidgetItem(quick, ["⚙️ 第一次使用设置"])
        self.nav_tree.addTopLevelItem(quick)

        proj = QTreeWidgetItem(["📁 项目管理"])
        QTreeWidgetItem(proj, ["➕ 创建项目"])
        QTreeWidgetItem(proj, ["✏️ 编辑项目"])
        QTreeWidgetItem(proj, ["🎨 自定义外观入门"])
        QTreeWidgetItem(proj, ["🗑️ 删除项目"])
        self.nav_tree.addTopLevelItem(proj)

        appearance = QTreeWidgetItem(["🎨 深度定制"])
        QTreeWidgetItem(appearance, ["🖼️ 背景类型详解"])
        QTreeWidgetItem(appearance, ["📝 文字元素样式"])
        QTreeWidgetItem(appearance, ["🌐 布局编辑器详解"])
        QTreeWidgetItem(appearance, ["✨ 动态壁纸机制"])
        QTreeWidgetItem(appearance, ["🍅 番茄钟使用"])
        QTreeWidgetItem(appearance, ["🌤️ 天气挂件配置"])
        QTreeWidgetItem(appearance, ["📜 诗词格言轮播"])
        QTreeWidgetItem(appearance, ["➕ 自定义文字/图片"])
        self.nav_tree.addTopLevelItem(appearance)

        plugin = QTreeWidgetItem(["🔌 CAC插件系统"])
        QTreeWidgetItem(plugin, ["📥 安装插件"])
        QTreeWidgetItem(plugin, ["⚙️ 管理插件与权限"])
        QTreeWidgetItem(plugin, ["🔒 权限模型详解"])
        QTreeWidgetItem(plugin, ["🛠️ 开发插件 - 快速开始"])
        QTreeWidgetItem(plugin, ["📘 插件API完整参考"])
        QTreeWidgetItem(plugin, ["💡 插件开发完整示例"])
        QTreeWidgetItem(plugin, ["🔑 签名与安全"])
        QTreeWidgetItem(plugin, ["🛡️ 沙箱与审计"])
        self.nav_tree.addTopLevelItem(plugin)

        security = QTreeWidgetItem(["🔒 安全与调试"])
        QTreeWidgetItem(security, ["📜 权限最佳实践"])
        QTreeWidgetItem(security, ["📝 敏感操作审计"])
        QTreeWidgetItem(security, ["🐞 调试控制台完全指南"])
        QTreeWidgetItem(security, ["📄 日志等级与查看"])
        self.nav_tree.addTopLevelItem(security)

        faq = QTreeWidgetItem(["❓ 常见问题"])
        QTreeWidgetItem(faq, ["❔ 窗口/倒计时问题"])
        QTreeWidgetItem(faq, ["❔ 天气/网络问题"])
        QTreeWidgetItem(faq, ["❔ 插件相关故障"])
        QTreeWidgetItem(faq, ["❔ 动态壁纸优化"])
        self.nav_tree.addTopLevelItem(faq)

        shortcuts = QTreeWidgetItem(["⌨️ 快捷键与技巧"])
        QTreeWidgetItem(shortcuts, ["🖱️ 鼠标操作速查"])
        QTreeWidgetItem(shortcuts, ["⌨️ 键盘快捷键"])
        QTreeWidgetItem(shortcuts, ["💡 效率小技巧"])
        self.nav_tree.addTopLevelItem(shortcuts)

        about = QTreeWidgetItem(["ℹ️ 关于"])
        QTreeWidgetItem(about, ["📦 版本信息"])
        QTreeWidgetItem(about, ["👨‍💻 致谢与贡献"])
        self.nav_tree.addTopLevelItem(about)

    def on_link_clicked(self, link):
        if link.startswith("nav:"):
            self.navigate_to(link[4:])

    def on_nav_selected(self, current, previous):
        if not current:
            return
        if current.childCount() > 0:
            self.show_category_index(current)
            return
        item_text = current.text(0)
        content = self.get_content_for(item_text)
        self.content_label.setText(content)

    def show_category_index(self, category_item):
        title = category_item.text(0)
        children = []
        for i in range(category_item.childCount()):
            children.append(category_item.child(i).text(0))

        html = f"<h1>{title}</h1><ul>"
        accent = get_theme_colors(self.app.theme)['accent']
        for child in children:
            html += f'<li><a href="nav:{child}" style="color:{accent}; text-decoration:none;">📄 {child}</a></li>'
        html += "</ul><p>点击上方链接查看详细内容。</p>"
        self.content_label.setText(html)

    def navigate_to(self, section_text):
        def search_item(parent):
            for i in range(parent.childCount()):
                child = parent.child(i)
                if child.childCount() == 0 and child.text(0) == section_text:
                    return child
                if child.childCount() > 0:
                    found = search_item(child)
                    if found:
                        return found
            return None

        for i in range(self.nav_tree.topLevelItemCount()):
            top = self.nav_tree.topLevelItem(i)
            found = search_item(top)
            if found:
                self.nav_tree.setCurrentItem(found)
                return

    def get_content_for(self, topic):
        db = {
            "📌 欢迎与概览": """
            <h1>🎉 欢迎使用倒计时桌面</h1>
            <p>这是一款功能强大的桌面倒计时工具，支持：</p>
            <ul>
            <li><b>多项目独立倒计时</b> – 可同时创建多个悬浮窗，分别设置目标日期和时间</li>
            <li><b>自然日/工作日双模式</b> – 自动识别中国法定节假日和调休，显示剩余工作日</li>
            <li><b>所见即所得的布局编辑器</b> – 拖拽调整文字、图片、天气、番茄钟等元素位置</li>
            <li><b>动态壁纸引擎</b> – 星空、白云、鼠标粒子效果，可调节帧率和画质</li>
            <li><b>插件系统</b> – 支持第三方扩展，可自定义动态背景、桌面控件、设置面板等</li>
            </ul>
            <p>本帮助文档将引导您从零开始掌握所有功能。</p>
            """,
            "🖱️ 悬浮窗操作指南": """
            <h2>🖱️ 悬浮窗基本操作</h2>
            <ul>
            <li><b>移动窗口</b>：在窗口<b>中心区域</b>按住鼠标左键拖拽即可移动。窗口会自动吸附到屏幕边缘，方便对齐。</li>
            <li><b>调整大小</b>：将鼠标移动到窗口的<b>四个边缘或角落</b>，光标变为双向箭头时拖拽即可缩放。最小尺寸为 250×150 像素。</li>
            <li><b>右键菜单</b>：右键点击悬浮窗弹出菜单，包含：设置、置顶/取消置顶、全屏模式、关闭窗口、退出应用。</li>
            <li><b>双击动作</b>：双击悬浮窗任意位置，快速打开<b>全局设置面板</b>。</li>
            <li><b>全屏模式</b>：全屏后会自动隐藏其他窗口，鼠标移动到右下角会出现悬浮控制面板，可调节透明度、切换动态壁纸等。</li>
            </ul>
            """,
            "⚙️ 第一次使用设置": """
            <h2>⚙️ 第一次使用指南</h2>
            <ol>
            <li><b>创建你的第一个项目</b>：右键悬浮窗 → 设置 → 项目管理 → 添加项目。默认名称为“新项目”，目标日期为30天后。</li>
            <li><b>编辑项目细节</b>：选中项目，点击“编辑项目”。您可以修改项目名称、目标日期（格式 YYYY-MM-DD），如果需要精确到时分，请勾选“设置精确时间”。</li>
            <li><b>调整外观</b>：在项目列表中选中项目后，点击“自定义外观”进入布局编辑器。您可以拖拽各个元素（名称、倒计时数字、静态文字等）到合适位置，也可以在右侧属性面板修改颜色、字体、阴影等。</li>
            <li><b>全局设置</b>：在“全局设置”标签页，可以选择全局字体、诗词级别（初级/中级/高级/关闭）、开机自启动等。</li>
            <li><b>插件系统</b>：如果您需要扩展功能，请进入“插件管理”标签页，首先开启插件系统（默认关闭），然后放入插件文件到 plugins 文件夹，刷新并启用。</li>
            </ol>
            """,
            "➕ 创建项目": "<h2>➕ 创建项目</h2><p>在设置面板 → 项目管理 → 点击“添加项目”，新项目将使用默认配置（目标日期30天后，纯色背景）。您可以后续编辑修改。一个项目对应一个独立的悬浮窗。</p>",
            "✏️ 编辑项目": "<h2>✏️ 编辑项目</h2><p>选中项目后点击“编辑项目”，弹出对话框可修改：<br>• 项目名称<br>• 目标日期与精确时间<br>• 是否同时显示自然日和工作日<br>• 字体大小及自动调整<br>• 窗口透明度（0.1~1.0）<br>• 背景类型：纯色、图片、渐变、动态壁纸<br>• 字体颜色<br>• 诗词切换间隔（分钟）</p>",
            "🎨 自定义外观入门": "<h2>🎨 自定义外观编辑器</h2><p>这是本软件最强大的功能之一。您可以在左侧元素列表中增删元素，在中间预览区<b>直接拖拽元素位置</b>（支持吸附和参考线），在右侧属性面板精细调整每个元素的样式。所有修改实时生效。</p>",
            "🗑️ 删除项目": "<h2>🗑️ 删除项目</h2><p>选中项目后点击“删除项目”。注意：至少需要保留一个项目，无法删除最后一个项目。</p>",
            "🖼️ 背景类型详解": """
            <h2>🖼️ 背景类型详解</h2>
            <ul>
            <li><b>纯色</b>：单一颜色背景，可调节透明度。当透明度 < 1.0 且圆角为0时，会自动启用 Windows 亚克力模糊效果（仅Win10/11）。</li>
            <li><b>图片</b>：支持 JPG/PNG/BMP/GIF 格式。GIF 会自动播放动画。图片会拉伸铺满整个窗口，您可以在编辑项目时上传图片到 data/user 目录。</li>
            <li><b>渐变</b>：线性渐变，可自定义起点色和终点色。渐变方向为左上到右下。</li>
            <li><b>动态</b>：包含星空、白云、鼠标粒子三种内置动态壁纸，可调节帧率（30/60/120 FPS）和画质（高/中/低）。</li>
            </ul>
            """,
            "📝 文字元素样式": """
            <h2>📝 文字元素样式设置</h2>
            <p>在布局编辑器右侧，选中任意文字元素（如名称、倒计时、静态文字等），可以设置：</p>
            <ul>
            <li><b>字体大小</b>：6~72 像素</li>
            <li><b>文字颜色</b>：任意颜色，支持透明度</li>
            <li><b>透明度</b>：0% 完全透明，100% 完全不透明</li>
            <li><b>描边</b>：可启用描边并设置颜色和宽度，使文字更清晰</li>
            <li><b>阴影</b>：设置阴影颜色、水平/垂直偏移、模糊半径，营造立体感</li>
            <li><b>背景</b>：可为文字元素添加背景色和圆角矩形</li>
            <li><b>对齐方式</b>：水平（左/中/右）和垂直（上/中/下）对齐</li>
            </ul>
            """,
            "🌐 布局编辑器详解": """
            <h2>🌐 布局编辑器使用技巧</h2>
            <ul>
            <li><b>拖拽定位</b>：在预览画布上直接按住元素拖拽，元素的位置会以百分比形式保存（相对于窗口宽高）。</li>
            <li><b>网格与吸附</b>：开启“网格”显示辅助格子，开启“吸附”后拖拽时会自动对齐其他元素的位置或参考线（三分线、中心线）。</li>
            <li><b>参考线</b>：显示水平/垂直的居中线以及三等分线，帮助精确对齐。</li>
            <li><b>元素层级</b>：通过“上移”“下移”按钮可以调整元素的渲染顺序，后添加的元素默认在上层。</li>
            <li><b>添加自定义元素</b>：点击“添加”按钮，可以添加自定义文字或自定义图片。文字内容可任意编辑，图片可从本地选择（自动复制到用户目录）。</li>
            <li><b>删除元素</b>：选中元素后点击“删除”（项目名称和倒计时不可删除）。</li>
            </ul>
            """,
            "✨ 动态壁纸机制": """
            <h2>✨ 动态壁纸工作原理</h2>
            <ul>
            <li><b>星空模式</b>：生成数百个随机亮度的星星，缓慢向左飘移，并且星星的亮度会周期性变化（闪烁），模拟夜空效果。</li>
            <li><b>白云模式</b>：绘制半透明的椭圆云朵，从左向右缓慢移动，营造天空云彩飘动的感觉。</li>
            <li><b>鼠标粒子模式</b>：创建许多带有颜色的小圆点，它们具有初始速度。当鼠标移动时，粒子会受到鼠标的“引力”或“斥力”影响，粒子之间距离小于阈值时会绘制连线。点击窗口时产生涟漪扩散效果。</li>
            </ul>
            <p>您可以在全屏模式下的控制面板或项目编辑器中调整动态壁纸的帧率和画质，高画质会使用更多粒子/星星，低画质则减少数量以提升性能。</p>
            """,
            "🍅 番茄钟使用": """
            <h2>🍅 番茄钟使用说明</h2>
            <p>在布局编辑器中添加“番茄钟”元素后，该元素会显示一个圆形计时器。</p>
            <ul>
            <li><b>单击</b>：开始/暂停当前计时（专注或休息）。</li>
            <li><b>双击</b>：重置计时器，恢复到专注状态。</li>
            <li>您可以在项目编辑器中分别设置专注时长（默认25分钟）和休息时长（默认5分钟）。</li>
            <li>番茄钟计时结束后会自动切换到休息/专注，并发出提示（当前无声音，仅视觉更新）。</li>
            </ul>
            """,
            "🌤️ 天气挂件配置": """
            <h2>🌤️ 天气挂件配置</h2>
            <p>首先在布局编辑器中添加“天气挂件”元素，然后在右侧属性面板选择省份和城市。目前使用 <b>wttr.in</b> 作为天气数据源（国内可用，无需代理）。</p>
            <ul>
            <li><b>刷新策略</b>：每15分钟自动刷新一次，您也可以点击天气文字手动刷新（会弹出未来7天预报窗口）。</li>
            <li><b>显示内容</b>：城市名称、天气状况（如晴、多云）、温度（摄氏度）。</li>
            <li><b>故障处理</b>：如果长时间显示“获取天气...”或“天气离线”，请检查网络连接，或尝试重启应用。国内大部分地区 wttr.in 工作正常。</li>
            </ul>
            """,
            "📜 诗词格言轮播": """
            <h2>📜 诗词格言轮播</h2>
            <p>在全局设置中选择诗词级别：</p>
            <ul>
            <li><b>无</b>：不显示诗词，改为显示小提示（如“保持专注”）。</li>
            <li><b>初级</b>：简单易懂的短句或诗句。</li>
            <li><b>中级</b>：经典诗词名句。</li>
            <li><b>高级</b>：更长或更深刻的诗句。</li>
            </ul>
            <p>诗词每隔一段时间（默认15分钟，可在项目编辑器中修改）会以打字机效果逐字显示在悬浮窗上。诗词数据存放在 <code>data/poems.json</code> 中，您可以自行增删。</p>
            """,
            "➕ 自定义文字/图片": """
            <h2>➕ 添加自定义文字/图片</h2>
            <p>在布局编辑器中点击“添加”按钮，选择“自定义文字”或“自定义图片”。</p>
            <ul>
            <li><b>自定义文字</b>：输入任意文本，之后可以像其他文字元素一样调整位置、颜色、字体等。</li>
            <li><b>自定义图片</b>：选择本地图片文件（支持PNG/JPG/GIF等），图片会被复制到 <code>data/user/</code> 目录并显示在悬浮窗上。您还可以在属性面板中调整图片的尺寸（目前为固定缩放，后续版本支持自定义大小）。</li>
            </ul>
            """,
            "📥 安装插件": """
            <h2>📥 如何安装第三方插件</h2>
            <ol>
            <li><b>获取插件文件</b>：插件是一个单独的 <code>.py</code> 文件，通常由社区或开发者提供。</li>
            <li><b>放置插件</b>：将 <code>.py</code> 文件复制到应用所在目录下的 <code>plugins</code> 文件夹（如果不存在请手动创建）。</li>
            <li><b>启用插件系统</b>：打开设置 → 插件管理，确保顶部的“启用插件系统”开关已打开（默认关闭）。</li>
            <li><b>刷新列表</b>：插件会自动加载，出现在列表中。</li>
            <li><b>启用插件</b>：选中插件，点击“启用”，根据插件请求的权限弹出确认窗口，点击“是”后插件即开始运行。</li>
            </ol>
            <p>注意：插件系统默认全局关闭，以保障安全。仅从可信来源安装插件。</p>
            """,
            "⚙️ 管理插件与权限": """
            <h2>⚙️ 管理插件</h2>
            <p>在插件管理标签页中，每个插件会显示名称、版本、作者、状态、所需权限、风险等级。</p>
            <ul>
            <li><b>启用/禁用</b>：控制插件是否运行。禁用后插件不会执行任何代码。</li>
            <li><b>权限管理</b>：点击“权限”按钮，可以单独授予或撤销插件的文件读取、文件写入、网络访问、执行命令权限。修改后即时生效。</li>
            <li><b>插件详情</b>：选中插件后右侧会显示详细信息，如果插件提供了自定义设置面板，也会显示在此处。</li>
            <li><b>日志查看</b>：下方“常规日志”显示插件的运行日志，“敏感操作”记录插件对文件、网络、命令的每次调用（需要审计钩子支持）。</li>
            </ul>
            """,
            "🔒 权限模型详解": """
            <h2>🔒 插件权限模型</h2>
            <p>插件在代码中必须声明其需要的权限（通过 <code>requested_permissions</code> 属性），用户启用插件时会弹出确认窗口。</p>
            <p>权限分为四种：</p>
            <ul>
            <li><b>FILE_READ</b>：允许读取文件。插件可以打开、读取任意文件（但受沙箱限制，无法读取系统关键目录）。</li>
            <li><b>FILE_WRITE</b>：允许写入、创建、删除文件。具有此权限的插件可能修改用户数据。</li>
            <li><b>NETWORK</b>：允许进行网络连接。用于获取网络资源、API调用等。</li>
            <li><b>COMMAND</b>：允许执行系统命令（如 <code>os.system</code>、<code>subprocess.Popen</code>）。此权限风险极高，请谨慎授予。</li>
            </ul>
            <p>插件运行时，Python 审计钩子会拦截所有敏感操作，如果插件未获得对应权限，会抛出 <code>PermissionError</code>，操作被阻止并记录到日志。</p>
            """,
            "🛠️ 开发插件 - 快速开始": """
            <h2>🛠️ 开发自己的插件 - 5分钟入门</h2>
            <p>插件是一个标准的 Python 文件，必须包含一个 <code>setup(app, api)</code> 函数，并返回一个继承自 <code>Plugin</code> 类的实例。</p>
            <pre><code># my_first_plugin.py
from plugin_base import Plugin, PluginPermission

class HelloWorldPlugin(Plugin):
    def __init__(self, app, api):
        super().__init__()
        self.name = "Hello World"
        self.version = "1.0"
        self.author = "YourName"
        self.description = "一个简单的示例插件"
        # 声明需要的权限（本例不需要任何权限）
        self.requested_permissions = PluginPermission.NONE

    def on_enable(self):
        self.api.log("插件已启用")
        self.api.show_notification("Hello", "插件开始运行！")

def setup(app, api):
    return HelloWorldPlugin(app, api)
</code></pre>
            <p>将上述代码保存为 <code>.py</code> 文件，放入 <code>plugins</code> 文件夹，然后在应用中启用插件即可看到通知。</p>
            """,
            "📘 插件API完整参考": """
            <h2>📘 插件API参考</h2>
            <p>在插件代码中，通过 <code>self.api</code> 可以调用以下方法：</p>
            <ul>
            <li><code>api.log(message, level="INFO")</code> – 记录日志，日志会显示在插件管理界面的“常规日志”中。</li>
            <li><code>api.register_dynamic_bg(id_name, display_name, widget_class)</code> – 注册一个动态背景。<br>
                <b>参数</b>：<code>id_name</code>（唯一标识符），<code>display_name</code>（显示名称，如“极光效果”），<code>widget_class</code>（一个继承自 <code>QWidget</code> 的类，实现动态绘制）。<br>
                <b>示例</b>：<code>api.register_dynamic_bg("aurora", "极光", AuroraWidget)</code>，之后用户可以在动态壁纸下拉框中选择“极光”。</li>
            <li><code>api.register_widget(id_name, display_name, widget_class)</code> – 注册一个桌面控件，目前保留用于未来扩展。</li>
            <li><code>api.register_settings_widget(id_name, display_name, widget_class)</code> – 为插件添加一个自定义设置面板，会显示在插件管理详情区域。</li>
            <li><code>api.get_config(key, default=None)</code> – 读取插件保存的配置（JSON存储）。</li>
            <li><code>api.set_config(key, value)</code> – 保存插件配置。</li>
            <li><code>api.show_notification(title, message)</code> – 显示系统通知（需要系统托盘图标支持）。</li>
            </ul>
            """,
            "💡 插件开发完整示例": """
            <h2>💡 完整插件示例：实时股票行情控件</h2>
            <p>这个示例展示了如何注册一个动态背景，并显示股票价格。</p>
            <pre><code># stock_widget.py
import threading, requests, json
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer
from plugin_base import Plugin, PluginPermission

class StockWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 50)
        self.setStyleSheet("color: white; background: rgba(0,0,0,0.5); border-radius: 8px;")
        self.setText("加载中...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch)
        self.timer.start(10000)  # 每10秒刷新
        self.fetch()

    def fetch(self):
        def run():
            try:
                resp = requests.get("https://api.example.com/stock/000001", timeout=5)
                data = resp.json()
                price = data["price"]
                self.setText(f"📈 平安银行: {price} 元")
            except:
                self.setText("📉 获取失败")
        threading.Thread(target=run, daemon=True).start()

class StockPlugin(Plugin):
    def __init__(self, app, api):
        super().__init__()
        self.name = "股票行情"
        self.version = "1.0"
        self.author = "Demo"
        self.description = "显示实时股价"
        self.requested_permissions = PluginPermission.NETWORK

    def on_enable(self):
        # 注册动态背景类型（其实这里注册了一个控件，但动态背景也可以）
        self.api.register_dynamic_bg("stock_widget", "股票面板", StockWidget)
        self.api.log("股票插件已启动")

def setup(app, api):
    return StockPlugin(app, api)
</code></pre>
            <p>用户启用后，在动态壁纸下拉框中会出现“股票面板”，选择后即可在悬浮窗上显示股票价格。</p>
            """,
            "🔑 签名与安全": """
            <h2>🔑 插件签名验证（高级安全）</h2>
            <p>为确保插件来源可信，应用支持 Ed25519 签名验证。开发者可以对插件文件（.py）生成签名文件（.py.sig），用户在应用中开启签名验证后，只有签名验证通过的插件才能加载。</p>
            <p>签名验证默认关闭，普通用户无需关心。如果您是开发者并希望使用此功能，请参考源码中的 <code>_verify_signature</code> 方法实现。</p>
            """,
            "🛡️ 沙箱与审计": """
            <h2>🛡️ 插件沙箱与审计</h2>
            <ul>
            <li><b>沙箱</b>：插件运行在受限的 Python 环境中，<code>__builtins__</code> 被替换为安全子集，<code>open</code>、<code>eval</code>、<code>exec</code> 等危险函数被审计钩子拦截。</li>
            <li><b>审计钩子</b>：通过 <code>sys.addaudithook</code> 监控所有敏感操作（文件、网络、命令）。未授权的操作会抛出 <code>PermissionError</code> 并记录到“敏感操作”日志。</li>
            <li><b>日志记录</b>：所有插件的操作都会记录到日志文件 <code>data/LOG.txt</code> 以及界面的日志区域，方便排查问题。</li>
            </ul>
            """,
            "📜 权限最佳实践": """
            <h2>📜 插件权限最佳实践</h2>
            <ul>
            <li><b>最小权限原则</b>：插件只应申请它确实需要的权限。例如，一个天气插件只需要网络权限，不应申请文件写入权限。</li>
            <li><b>用户确认</b>：启用插件时用户会看到权限请求弹窗，请清晰说明为什么需要这些权限。</li>
            <li><b>定期审计</b>：建议用户定期查看插件列表和敏感操作记录，发现异常及时禁用插件。</li>
            </ul>
            """,
            "📝 敏感操作审计": """
            <h2>📝 敏感操作审计功能</h2>
            <p>在插件管理界面的“敏感操作”标签页中，记录了每个插件对文件、网络、命令的调用详情。例如：</p>
            <pre>[2025-01-15 10:30:22] [StockPlugin] 网络访问 | GET https://api.example.com/stock</pre>
            <p>这有助于用户了解插件的行为，发现潜在的恶意操作。如果某个插件频繁尝试访问非必要资源，建议禁用或调整其权限。</p>
            """,
            "🐞 调试控制台完全指南": """
            <h2>🐞 调试控制台完全指南</h2>
            <p>在设置界面按下键盘上的 <code>~</code> 或 <code>`</code> 键即可打开内置的调试控制台（V2.0）。这是一个强大的交互式 Python 环境，支持命令行历史、Tab 自动补全和 20+ 内置调试命令。</p>
            <h3>界面说明</h3>
            <ul>
              <li><b>日志转发开关</b>：工具栏上的复选框，默认<b>关闭</b>，避免日志刷屏。开启后系统日志将实时显示在控制台中</li>
              <li><b>↑↓ 方向键</b>：浏览历史命令，方便重复执行</li>
              <li><b>Tab 键</b>：自动补全命令名，输入前几个字母按 Tab 即可</li>
              <li><b>清空/帮助按钮</b>：一键清屏或查看所有命令</li>
            </ul>
            <h3>内置命令一览</h3>
            <table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse; width:100%;'>
              <tr style='background:#3498db; color:white;'><th>命令</th><th>参数</th><th>功能说明</th></tr>
              <tr><td><code>help</code></td><td>-</td><td>显示完整的命令帮助列表</td></tr>
              <tr><td><code>clear</code></td><td>-</td><td>清空控制台输出内容</td></tr>
              <tr><td><code>restart</code></td><td>-</td><td>重新启动整个应用程序</td></tr>
              <tr><td><code>clear_cache</code></td><td>-</td><td>清理应用缓存（天气、背景等临时数据）</td></tr>
              <tr><td><code>perf_info</code></td><td>-</td><td>显示性能统计：窗口数、线程数、内存占用</td></tr>
              <tr><td><code>theme_info</code></td><td>-</td><td>显示当前主题详细信息（名称、色值、模式）</td></tr>
              <tr><td><code>app_info</code></td><td>-</td><td>显示应用版本、Python版本、系统环境信息</td></tr>
              <tr><td><code>list_threads</code></td><td>-</td><td>列出所有活跃线程及其状态</td></tr>
              <tr><td><code>backup_config</code></td><td>-</td><td>备份当前配置文件到 backups/ 目录</td></tr>
              <tr><td><code>open_settings</code></td><td>-</td><td>快速打开全局设置窗口</td></tr>
              <tr><td><code>toggle_log</code></td><td>-</td><td>切换日志转发开关（开/关）</td></tr>
              <tr><td><code>close_window</code></td><td>&lt;N&gt;</td><td>关闭第 N 个悬浮窗（从0开始编号）</td></tr>
              <tr><td><code>list_windows</code></td><td>-</td><td>列出所有悬浮窗的索引和名称</td></tr>
              <tr><td><code>show_windows</code></td><td>-</td><td>显示所有悬浮窗</td></tr>
              <tr><td><code>hide_windows</code></td><td>-</td><td>隐藏所有悬浮窗</td></tr>
              <tr><td><code>set_window_alpha</code></td><td>&lt;0.1-1.0&gt;</td><td>设置所有窗口的全局透明度</td></tr>
              <tr><td><code>list_projects</code></td><td>-</td><td>列出所有项目名称和目标日期</td></tr>
              <tr><td><code>dump_project</code></td><td>&lt;N&gt;</td><td>打印第 N 个项目的完整配置（JSON）</td></tr>
              <tr><td><code>reload_theme</code></td><td>-</td><td>重新加载主题样式表</td></tr>
              <tr><td><code>plugins</code></td><td>-</td><td>列出所有已装载的插件</td></tr>
              <tr><td><code>enable_plugin</code></td><td>&lt;名称&gt;</td><td>启用指定名称的插件</td></tr>
              <tr><td><code>disable_plugin</code></td><td>&lt;名称&gt;</td><td>禁用指定名称的插件</td></tr>
              <tr><td><code>set_debug_level</code></td><td>&lt;0-3&gt;</td><td>设置全局调试等级（0=关闭, 1=错误, 2=信息, 3=详细）</td></tr>
              <tr><td><code>refresh_weather</code></td><td>-</td><td>强制刷新所有窗口的天气信息</td></tr>
              <tr><td><code>exit</code></td><td>-</td><td>关闭调试控制台窗口</td></tr>
            </table>
            <h3>高级用法</h3>
            <p>控制台支持任意 Python 表达式求值，输入后按回车即可执行。例如：</p>
            <pre><code>len(app.windows)          # 查看当前悬浮窗数量
app.theme.is_dark          # 检查是否为暗色主题
app.projects[0].name       # 查看第一个项目的名称
[x.project.name for x in app.windows]  # 列表推导式</code></pre>
            <p>如果命令不是内置的，控制台会尝试用 <code>eval()</code> 求值，因此你可以访问所有以 <code>app</code> 开头的对象属性和方法。</p>
            <h3>注意事项</h3>
            <ul>
              <li>日志转发默认关闭——执行命令的输出不会被日志冲刷掉</li>
              <li>修改应用状态的命令会立即生效（如 set_window_alpha、set_debug_level）</li>
              <li><code>restart</code> 会关闭所有窗口并重新加载，请确认已保存</li>
              <li><code>close_window N</code> 会彻底删除对应的悬浮窗，操作不可撤销</li>
            </ul>
            """,
            "📄 日志等级与查看": """
            <h2>📄 日志等级与查看方法</h2>
            <p>在全局设置中可以调整日志等级：</p>
            <ul>
            <li><b>0 - 关闭</b>：不记录任何日志</li>
            <li><b>1 - 错误/警告</b>：只记录错误和警告</li>
            <li><b>2 - 普通信息</b>：记录一般信息（默认）</li>
            <li><b>3 - 详细调试</b>：记录所有调试信息，包括插件调用的细节</li>
            </ul>
            <p>日志文件保存在 <code>data/LOG.txt</code>，您可以使用“查看日志文件”按钮快速打开。日志会记录时间、级别、调用位置和内容，有助于排查问题。</p>
            """,
            "❔ 窗口/倒计时问题": """
            <h2>❔ 窗口或倒计时相关问题</h2>
            <ul>
            <li><b>窗口无法移动</b>：确保在中心区域拖拽，而非边缘。如果窗口移出屏幕，可通过托盘菜单“重置窗口位置”恢复。</li>
            <li><b>倒计时不更新</b>：检查目标日期是否已过，已到期会显示“已到期”。如果工作日为0，静态文字可能为空，但数字倒计时应该仍会更新。检查日志文件是否有错误。</li>
            <li><b>数字滚动不流畅</b>：数字滚动使用 QPropertyAnimation，通常很流畅。如果出现卡顿，可能是动态壁纸占用过高，请降低帧率或画质。</li>
            </ul>
            """,
            "❔ 天气/网络问题": """
            <h2>❔ 天气挂件或网络相关问题</h2>
            <ul>
            <li><b>天气不显示</b>：确认已添加天气元素并选择了城市。默认使用 wttr.in，国内大部分地区可用，但如果网络特殊，可能超时。请检查系统网络连接，或重启应用。</li>
            <li><b>点击天气标签没有反应</b>：需要先成功获取一次天气数据，获得经纬度后才能弹出预报窗口。如果一直失败，请查看日志。</li>
            <li><b>更新检查失败</b>：更新服务器地址可能变更，具体以发布页面为准。</li>
            </ul>
            """,
            "❔ 插件相关故障": """
            <h2>❔ 插件加载或运行故障</h2>
            <ul>
            <li><b>插件列表为空</b>：确认 plugins 文件夹存在且包含 .py 文件，并且全局插件系统已启用（插件管理页面的开关）。</li>
            <li><b>启用插件时提示“权限不足”</b>：插件请求的权限未被用户授予，可以在权限管理中手动添加权限。</li>
            <li><b>插件加载失败（语法错误）</b>：查看插件日志或控制台输出，修正插件代码后重启应用。</li>
            <li><b>插件导致应用崩溃</b>：如果某个插件导致崩溃，可以在安全模式下启动：删除或移出该插件文件，再重启应用。或者通过命令行参数 <code>--no-plugins</code> 启动（需要自行实现）。</li>
            </ul>
            """,
            "❔ 动态壁纸优化": """
            <h2>❔ 动态壁纸卡顿或性能问题</h2>
            <ul>
            <li><b>降低帧率</b>：将帧率从60 FPS降低到30 FPS，CPU/GPU占用会明显下降。</li>
            <li><b>降低画质</b>：选择“低画质”会减少粒子/星星数量。</li>
            <li><b>关闭动态壁纸</b>：如果硬件配置较低，建议使用静态图片或纯色背景。</li>
            <li><b>鼠标粒子模式</b>：该模式下粒子数量较多且连线计算密集，对性能要求较高。</li>
            </ul>
            """,
            "🖱️ 鼠标操作速查": "<h2>🖱️ 鼠标操作速查表</h2><ul><li>左键拖拽中心 → 移动窗口</li><li>左键拖拽边缘/角 → 调整大小</li><li>右键 → 上下文菜单</li><li>双击 → 打开设置</li><li>全屏模式下鼠标移动到右下角 → 显示控制面板</li></ul>",
            "⌨️ 键盘快捷键": "<h2>⌨️ 键盘快捷键</h2><ul><li>在设置界面按 <code>~</code> 或 <code>`</code> → 打开调试控制台</li><li>在全屏模式下，目前没有预设键盘快捷键，可通过鼠标控制面板操作。</li></ul>",
            "💡 效率小技巧": """
            <h2>💡 效率小技巧</h2>
            <ul>
            <li><b>快速复制项目</b>：目前没有“复制项目”按钮，但您可以手动编辑一个项目后，在配置文件中复制项目块（谨慎操作）。</li>
            <li><b>备份配置</b>：定期备份 <code>data/countdown_config.json</code> 文件，可以保存所有项目和布局设置。</li>
            <li><b>自定义诗词</b>：编辑 <code>data/poems.json</code>，按照已有格式添加您喜欢的诗句。</li>
            <li><b>窗口置顶技巧</b>：右键菜单中切换“置顶窗口”，可使窗口始终浮在其他应用之上。</li>
            </ul>
            """,
            "📦 版本信息": f"<h2>📦 版本信息</h2><p><b>当前版本</b>：{self.app.current_version}<br><b>构建号</b>：{self.app.build_version}<br><b>Python版本</b>：{self.app.python_version}<br><b>操作系统</b>：{platform.system()} {platform.release()}<br><b>数据目录</b>：{self.app.data_dir}</p>",
            "👨‍💻 致谢与贡献": """
            <h2>👨‍💻 致谢与贡献</h2>
            <p>本软件由 <b>苗睿轩</b> 开发维护。感谢所有测试人员、插件开发者以及提出宝贵建议的用户。</p>
            <p>如果您想报告问题或贡献代码，请发送意见和建议到guzhiawa@qq.com</p>
            """
        }
        return db.get(topic, "<h2>暂无详细内容，请选择其他主题</h2>")

class SystemTrayIcon(QObject):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.tray = QSystemTrayIcon(self.master)

        icon_path = os.path.join(self.master.data_dir, "djstp.ico")
        if os.path.exists(icon_path):
            self.tray.setIcon(QIcon(icon_path))
        else:
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor("#3498db"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
            painter.setPen(QColor("white"))
            font = QFont("Arial", 24, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "⏳")
            painter.end()
            self.tray.setIcon(QIcon(pixmap))

        self.tray.setToolTip(tr("app_title"))

        self.menu = QMenu()

        act_settings = QAction(tr("settings_title"), self)
        act_settings.triggered.connect(self.master.open_settings)
        self.menu.addAction(act_settings)

        act_show = QAction("👁️ 显示所有窗口", self)
        act_show.triggered.connect(self.master.create_windows)
        self.menu.addAction(act_show)

        act_hide = QAction("🙈 隐藏所有窗口", self)
        act_hide.triggered.connect(self.hide_all_windows)
        self.menu.addAction(act_hide)

        act_reset = QAction("🔄 重置窗口位置", self)
        act_reset.triggered.connect(self.reset_windows_position)
        self.menu.addAction(act_reset)

        self.menu.addSeparator()

        act_quit = QAction("🚪 退出", self)
        act_quit.triggered.connect(self.master.quit_app)
        self.menu.addAction(act_quit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_activated)
        self.tray.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.master.open_settings()

    def hide_all_windows(self):
        for window in getattr(self.master, 'windows', []):
            window.close()
        self.master.windows = []

    def reset_windows_position(self):
        screen_geo = QApplication.primaryScreen().geometry()
        for i, window in enumerate(self.master.windows):
            x = 100 + i * 30
            y = 100 + i * 30
            if x + window.width() > screen_geo.width():
                x = screen_geo.width() - window.width()
            if y + window.height() > screen_geo.height():
                y = screen_geo.height() - window.height()
            window.move(x, y)
            window.project.position = (x, y)
        self.master.save_config(force=True)

class UpdateCheckerThread(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def run(self):
        api_url = "http://127.0.0.1:5000/api/check"
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.result_ready.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

class CountdownApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName(tr("app_title"))
        self.setQuitOnLastWindowClosed(False)

        self.current_version = "2.8.2"
        self.build_version = 101
        self.python_version = sys.version.split()[0]
        self.global_font = "Microsoft YaHei"
        self.current_theme = "system"
        self.theme = get_system_theme()
        self.custom_themes = []
        self.projects = []
        self.windows = []
        self.plugin_settings_tabs = {}

        self.auto_start = False
        self.last_save_time = 0
        self.poem_level = "junior"
        self.daily_poem = ""
        self.plugin_monitor = False
        self.plugin_prompt_on_deny = True
        self.global_disable_all_plugins = False

        self.weather_provider = "wttr_in"
        self.custom_weather_url = ""

        self.dynamic_bg_registry = {"stars": "✨ 星空", "clouds": "☁️ 白云", "particles": "🌌 鼠标粒子"}
        self.dynamic_bg_classes = {}

        self.settings_geometry = None
        self.editor_geometry = None
        self.help_geometry = None
        self.tools_geometry = None

        self.current_dir = os.getcwd()
        self.data_dir = resource_path("data")
        self.user_dir = os.path.join(self.data_dir, "user")
        os.makedirs(self.user_dir, exist_ok=True)

        self.config_path = os.path.join(self.data_dir, "countdown_config.json")

        self.show_splash()

        self.load_languages()
        self.load_poems()
        self.load_config()
        self.update_daily_poem()

        self.plugin_manager = PluginManager(self, load_immediately=False)
        QTimer.singleShot(1000, self._load_plugins_and_restore)

        self.tray_icon = SystemTrayIcon(self)

        self.create_windows()

        self.cmd_timer = QTimer(self)
        self.cmd_timer.timeout.connect(self.check_debug_command)
        self.cmd_timer.start(1000)

        self._last_system_dark = is_system_dark()
        self.theme_check_timer = QTimer(self)
        self.theme_check_timer.timeout.connect(self.check_system_theme)
        self.theme_check_timer.start(2000)

        self.theme_monitor = SystemThemeMonitor(self)
        self.theme_monitor.theme_changed.connect(self._on_system_theme_changed)

        if not getattr(sys, 'frozen', False):
            self.start_console_debugger()

        log_message("应用程序初始化完成", "INFO")

    def _on_system_theme_changed(self, is_dark):
        log_message(f"系统主题变化: {'深色' if is_dark else '浅色'}", "INFO")
        self.current_theme = "system"
        self.theme = get_system_theme()
        self._refresh_all_windows()

    def open_log_file(self):
        log_path = os.path.join(self.data_dir, "LOG.txt")
        if os.path.exists(log_path):
            try:
                if sys.platform == "win32":
                    os.startfile(log_path)
                else:
                    subprocess.run(["xdg-open", log_path])
            except Exception as e:
                QMessageBox.warning(self.settings_dlg, "错误", f"无法打开日志文件:\n{e}")
        else:
            QMessageBox.information(self.settings_dlg, "提示", "日志文件尚未生成")

    def _refresh_all_windows(self):
        qss = get_theme_qss(self.theme)
        for widget in QApplication.topLevelWidgets():
            widget.setStyleSheet(qss)
            widget.update()
        for window in self.windows:
            window.refresh(theme_change=True)

    def create_windows(self):
        for win in self.windows:
            win.close()
        self.windows.clear()
        for i, proj in enumerate(self.projects):
            win = CountdownWindow(self, proj, i)
            self.windows.append(win)
            win.show()

    def close_splash(self):
        if hasattr(self, 'splash') and self.splash:
            opacity_effect = QGraphicsOpacityEffect(self.splash)
            self.splash.setGraphicsEffect(opacity_effect)
            anim = QPropertyAnimation(opacity_effect, b"opacity")
            anim.setDuration(300)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.finished.connect(self.splash.deleteLater)
            anim.start()
            self.splash = None

    def show_splash(self):
        self.splash = QWidget()
        self.splash.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.splash.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.splash.setFixedSize(220, 120)

        layout = QVBoxLayout(self.splash)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        lbl_title = QLabel("⏳ 倒计时")
        lbl_title.setStyleSheet(f"color: {get_theme_colors(get_system_theme())['console_text']}; font-size: 18px; font-weight: bold; font-family: 'Microsoft YaHei';")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_loading = QLabel("正在启动...")
        lbl_loading.setStyleSheet(f"color: {get_theme_colors(get_system_theme())['input_focus_border']}; font-size: 10px; font-family: 'Microsoft YaHei';")
        lbl_loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_loading)

        layout.addStretch()

        screen_geo = self.primaryScreen().geometry()
        self.splash.move(int((screen_geo.width() - 220) / 2), int((screen_geo.height() - 120) / 2))
        self.splash.show()

        self.splash_close_timer = QTimer(self)
        self.splash_close_timer.setSingleShot(True)
        self.splash_close_timer.timeout.connect(self.close_splash)
        self.splash_close_timer.start(1800)

    def load_languages(self):
        global _lang_data
        lang_file = os.path.join(self.data_dir, "languages.json")
        if os.path.exists(lang_file):
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    _lang_data = json.load(f)
            except Exception as e:
                log_message(f"加载语言文件失败: {e}", "ERROR")

    def load_poems(self):
        poem_file = os.path.join(self.data_dir, "poems.json")
        if os.path.exists(poem_file):
            try:
                with open(poem_file, "r", encoding="utf-8") as f:
                    self.poems_data = json.load(f)
            except:
                self.poems_data = {"primary": [], "junior": [], "senior": []}
        else:
            self.poems_data = {"primary": [], "junior": [], "senior": []}

    def update_daily_poem(self):
        if self.poem_level != "none" and self.poems_data.get(self.poem_level):
            self.daily_poem = random.choice(self.poems_data[self.poem_level])
        else:
            self.daily_poem = ""

    def get_random_poem_or_tip(self):
        if self.poems_data.get(self.poem_level):
            return random.choice(self.poems_data[self.poem_level])
        return random.choice(TIPS_DATA)

    def get_optimal_window_size(self, base_width, base_height, dialog_type="settings"):
        screen_geo = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geo.width()
        screen_height = screen_geo.height()

        if dialog_type == "settings":
            target_w, target_h = int(screen_width * 0.5), int(screen_height * 0.6)
        elif dialog_type == "editor":
            target_w, target_h = int(screen_width * 0.6), int(screen_height * 0.7)
        elif dialog_type == "help":
            target_w, target_h = int(screen_width * 0.4), int(screen_height * 0.5)
        else:
            target_w, target_h = base_width, base_height

        optimal_width = max(800, min(target_w, screen_width - 100))
        optimal_height = max(600, min(target_h, screen_height - 100))
        return optimal_width, optimal_height

    def load_config(self):
        global DEBUG_MODE, STATUS_MONITOR, CURRENT_LANG
        screen_geo = self.primaryScreen().geometry()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.projects = [CountdownProject.from_dict(p, screen_geo.width(), screen_geo.height()) for p in
                                 config.get("projects", [])]
                self.auto_start = config.get("auto_start", False)
                self.poem_level = config.get("poem_level", "junior")
                DEBUG_MODE = config.get("debug_mode", 3)
                STATUS_MONITOR = config.get("status_monitor", False)
                self.global_font = config.get("global_font", "Microsoft YaHei")
                CURRENT_LANG = config.get("language", LANG_CHINESE)
                self.current_theme = config.get("current_theme", "system")
                self.plugin_monitor = config.get("plugin_monitor", False)
                self.plugin_prompt_on_deny = config.get("plugin_prompt_on_deny", True)
                self.global_disable_all_plugins = config.get("global_disable_all_plugins", False)
                self.weather_provider = config.get("weather_provider", "wttr_in")
                self.custom_weather_url = config.get("custom_weather_url", "")

                def _decode_geom(hex_str):
                    return QByteArray.fromHex(hex_str.encode('utf-8')) if hex_str else None

                self.settings_geometry = _decode_geom(config.get("settings_geometry"))
                self.editor_geometry = _decode_geom(config.get("editor_geometry"))
                self.help_geometry = _decode_geom(config.get("help_geometry"))
                self.tools_geometry = _decode_geom(config.get("tools_geometry"))

                self.custom_themes = [Theme.from_dict(t) for t in config.get("custom_themes", [])]

                if self.current_theme == "system":
                    self.theme = get_system_theme()
                else:
                    matched = False
                    for t in self.custom_themes:
                        if t.name == self.current_theme:
                            self.theme = t
                            matched = True
                            break
                    if not matched:
                        self.theme = get_system_theme()
                        self.current_theme = "system"
            except Exception as e:
                log_message(f"加载配置错误: {e}", "ERROR")

        if not self.projects:
            self.projects = [
                CountdownProject("示例项目", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"), "00:00")]
            self.save_config(force=True)

    def save_config(self, force=False):
        current_time = time.time()
        if not force and current_time - self.last_save_time < 1.0:
            return
        for win in self.windows:
            if hasattr(win, 'is_fullscreen') and win.is_fullscreen and win.old_geometry:
                win.project.position = (win.old_geometry.x(), win.old_geometry.y())
                win.project.size = (win.old_geometry.width(), win.old_geometry.height())
            else:
                win.project.position = (win.x(), win.y())
                win.project.size = (win.width(), win.height())

        plugin_states = {}
        if hasattr(self, 'plugin_manager'):
            for plugin in self.plugin_manager.plugins:
                plugin_states[plugin.filename] = {
                    "enabled": plugin.enabled,
                    "limited": plugin.limited,
                    "permissions": int(plugin.permissions)
                }

        def _encode_geom(geom):
            return geom.toHex().data().decode('utf-8') if geom else None

        data = {
            "projects": [p.to_dict() for p in self.projects],
            "auto_start": self.auto_start,
            "poem_level": self.poem_level,
            "debug_mode": DEBUG_MODE,
            "status_monitor": STATUS_MONITOR,
            "global_font": self.global_font,
            "language": CURRENT_LANG,
            "current_theme": self.current_theme,
            "custom_themes": [t.to_dict() for t in self.custom_themes],
            "plugin_monitor": self.plugin_monitor,
            "plugin_prompt_on_deny": self.plugin_prompt_on_deny,
            "global_disable_all_plugins": self.global_disable_all_plugins,
            "weather_provider": self.weather_provider,
            "custom_weather_url": self.custom_weather_url,
            "plugin_states": plugin_states,
            "settings_geometry": _encode_geom(self.settings_geometry),
            "editor_geometry": _encode_geom(self.editor_geometry),
            "help_geometry": _encode_geom(self.help_geometry),
            "tools_geometry": _encode_geom(self.tools_geometry)
        }
        try:
            temp_path = self.config_path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, self.config_path)
            self.last_save_time = current_time
        except Exception as e:
            log_message(f"保存配置错误: {e}", "ERROR")

    def _load_plugins_and_restore(self):
        if self.global_disable_all_plugins:
            return
        self.plugin_manager.load_plugins()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                states = config.get("plugin_states", {})
                for plugin in self.plugin_manager.plugins:
                    state = states.get(plugin.filename, {})
                    if "permissions" in state:
                        try:
                            plugin.permissions = PluginPermission(int(state["permissions"]))
                        except Exception:
                            plugin.permissions = plugin.requested_permissions
                    elif state.get("enabled", False):
                        plugin.permissions = plugin.requested_permissions
                    if state.get("enabled", False):
                        self.plugin_manager.enable_plugin(plugin, limited=state.get("limited", False), force=True)
            except Exception as e:
                import traceback
                log_message(f"[插件] 恢复状态失败: {e}\n{traceback.format_exc()}", "ERROR")

    def check_system_theme(self):
        current_dark = is_system_dark()
        if current_dark != self._last_system_dark:
            self._last_system_dark = current_dark
            QTimer.singleShot(200, self.reload_system_theme)

    def reload_system_theme(self):
        self.theme = get_system_theme()
        self.setStyleSheet(get_theme_qss(self.theme))
        for win in self.windows:
            win.refresh(theme_change=True)
        if hasattr(self, 'settings_dlg') and self.settings_dlg and not self.settings_dlg.isHidden():
            self.settings_dlg.setStyleSheet(get_theme_qss(self.theme))

    def check_windows_status(self):
        active = sum(1 for w in self.windows if w.isVisible())
        if active == 0:
            log_message("所有悬浮窗已关闭，应用仍在后台运行", "INFO")

    def quit_app(self):
        self.save_config(force=True)
        self.quit()

    def start_console_debugger(self):
        def console_loop():
            print("=" * 60)
            print("  倒计时 (Countdown) - 开发调试控制台 V2.0.0")
            print("  输入 'help' 查看可用命令")
            print("=" * 60)
            while True:
                try:
                    cmd = input("dj>>> ").strip()
                    if not cmd:
                        continue
                    if cmd == "help":
                        print("""
  可用命令:
    help           - 显示此帮助
    p              - 打印所有项目信息
    w              - 打印所有窗口信息
    reload         - 重新加载配置并刷新窗口
    restart        - 重启应用
    info           - 显示应用基本信息
    screen         - 显示屏幕信息
    theme          - 显示主题信息
    threads        - 列出活跃线程
    perf           - 性能概览（需 psutil）
    backup         - 备份当前配置文件
    log [N]        - 显示最近 N 行日志（默认 30）
    clearlog       - 清空日志文件
    plugins        - 列出所有插件
    exit / quit    - 退出调试控制台
    也支持任意 Python 表达式: self.projects, len(self.windows)
  """)
                        continue
                    if cmd in ("exit", "quit"):
                        print("调试控制台已关闭")
                        break
                    if cmd == "p":
                        for i, proj in enumerate(self.projects):
                            print(f"  [{i}] {proj.name}  目标: {proj.target_date} {proj.target_time}")
                        continue
                    if cmd == "w":
                        for i, w in enumerate(self.windows):
                            vis = "可见" if w.isVisible() else "隐藏"
                            print(f"  [{i}] {w.project.name} pos=({w.x()},{w.y()}) size={w.width()}x{w.height()} [{vis}]")
                        continue
                    if cmd == "reload":
                        self.save_config(force=True)
                        self.load_config()
                        self.create_windows()
                        print("配置已重载，窗口已刷新")
                        continue
                    if cmd == "restart":
                        print("正在重启应用...")
                        self.restart_application()
                        break
                    if cmd == "info":
                        print(f"  版本: {self.current_version}")
                        print(f"  Python: {sys.version}")
                        print(f"  平台: {platform.platform()}")
                        print(f"  数据目录: {self.data_dir}")
                        print(f"  项目数: {len(self.projects)}")
                        print(f"  悬浮窗: {len(self.windows)}")
                        continue
                    if cmd == "screen":
                        screen = QApplication.primaryScreen()
                        geom = screen.geometry()
                        avail = screen.availableGeometry()
                        dpi = screen.logicalDotsPerInch()
                        print(f"  分辨率: {geom.width()}x{geom.height()}")
                        print(f"  可用区域: {avail.width()}x{avail.height()}")
                        print(f"  DPI: {dpi:.1f}")
                        continue
                    if cmd == "theme":
                        theme = get_system_theme()
                        dark = is_system_dark()
                        print(f"  系统深色模式: {'是' if dark else '否'}")
                        print(f"  背景色: {theme.bg_color}")
                        print(f"  DEBUG_MODE: {DEBUG_MODE}")
                        continue
                    if cmd == "threads":
                        import threading
                        for t in threading.enumerate():
                            d = "守护" if t.daemon else "普通"
                            a = "运行中" if t.is_alive() else "已停止"
                            print(f"  [{d}] {t.name} ({a})")
                        print(f"  共 {threading.active_count()} 个线程")
                        continue
                    if cmd == "perf":
                        try:
                            import psutil
                            proc = psutil.Process()
                            mem = proc.memory_info()
                            print(f"  物理内存: {mem.rss / 1024 / 1024:.1f} MB")
                            print(f"  虚拟内存: {mem.vms / 1024 / 1024:.1f} MB")
                            print(f"  CPU: {proc.cpu_percent(interval=0.1):.1f}%")
                            print(f"  线程数: {proc.num_threads()}")
                        except ImportError:
                            print("  psutil 未安装，无法获取性能信息")
                        import gc
                        print(f"  活跃线程: {threading.active_count()}")
                        print(f"  GC对象数: {len(gc.get_objects())}")
                        continue
                    if cmd == "backup":
                        config_path = self.config_path
                        if os.path.exists(config_path):
                            import shutil
                            backup_dir = os.path.join(self.data_dir, "backups")
                            os.makedirs(backup_dir, exist_ok=True)
                            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                            bp = os.path.join(backup_dir, f"config_backup_{ts}.json")
                            shutil.copy2(config_path, bp)
                            print(f"  配置已备份到: {bp}")
                        else:
                            print("  配置文件不存在")
                        continue
                    if cmd.startswith("log"):
                        parts = cmd.split()
                        n = int(parts[1]) if len(parts) > 1 else 30
                        log_file = os.path.join(self.data_dir, "LOG.txt")
                        if os.path.exists(log_file):
                            with open(log_file, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                            for line in lines[-n:]:
                                print(line.rstrip())
                        else:
                            print("  日志文件不存在")
                        continue
                    if cmd == "clearlog":
                        log_file = os.path.join(self.data_dir, "LOG.txt")
                        with open(log_file, "w", encoding="utf-8") as f:
                            f.write("")
                        print("  日志已清空")
                        continue
                    if cmd == "plugins":
                        pm = self.plugin_manager
                        for p in pm.plugins:
                            status = "启用" if p.enabled else "禁用"
                            print(f"  {p.name} v{p.version} [{status}]")
                        continue
                    try:
                        result = eval(cmd, {"self": self, "app": self, "os": os, "sys": sys, "json": json})
                        if result is not None:
                            print(result)
                    except Exception as e:
                        print(f"  错误: {e}")
                except EOFError:
                    break
                except Exception as e:
                    print(f"  输入异常: {e}")

        t = threading.Thread(target=console_loop, daemon=True)
        t.start()

    def check_debug_command(self):
        cmd_file = os.path.join(self.data_dir, "debug_command.txt")
        if not os.path.exists(cmd_file):
            return

        if os.path.getsize(cmd_file) == 0:
            os.remove(cmd_file)
            return

        try:
            with open(cmd_file, "r", encoding="utf-8") as f:
                cmd_data = json.load(f)
            os.remove(cmd_file)
            self.execute_debug_command(cmd_data)
        except Exception as e:
            log_message(f"处理调试命令失败: {e}", "ERROR")
            try:
                os.remove(cmd_file)
            except:
                pass

    def append_sensitive_log(self, plugin_name, operation, detail=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{timestamp}] [{plugin_name}] {operation}"
        if detail:
            msg += f" | {detail}"
        if not hasattr(self, '_sensitive_log_entries'):
            self._sensitive_log_entries = []
        self._sensitive_log_entries.append(msg)
        if len(self._sensitive_log_entries) > 500:
            del self._sensitive_log_entries[:-500]
        if threading.current_thread() is not threading.main_thread():
            return
        def _append():
            try:
                w = getattr(self, 'sensitive_log_text', None)
                if w is not None:
                    w.appendPlainText(msg)
            except RuntimeError:
                pass
        QTimer.singleShot(0, _append)

    def _clear_sensitive_log(self):
        if hasattr(self, '_sensitive_log_entries'):
            self._sensitive_log_entries.clear()
        try:
            w = getattr(self, 'sensitive_log_text', None)
            if w is not None:
                w.clear()
        except RuntimeError:
            pass



    def execute_debug_command(self, cmd_data):
        command = cmd_data.get("command")
        log_message(f"收到监控器命令: {command}", "INFO")
        if command == "set_debug_level":
            global DEBUG_MODE
            DEBUG_MODE = cmd_data.get("level", 2)
            self.save_config(force=True)
        elif command == "restart":
            self.restart_application()
        elif command == "terminate":
            self.quit_app()
        elif command == "disable_all_plugins":
            self.global_disable_all_plugins = True
            for p in self.plugin_manager.get_enabled_plugins():
                self.plugin_manager.disable_plugin(p)
            self.save_config()
        elif command == "disable_all_plugins_and_restart":
            self.global_disable_all_plugins = True
            self.save_config(force=True)
            self.restart_application()
        elif command == "hide_all_windows":
            for w in self.windows:
                w.hide()
        elif command == "simulate_error":
            raise Exception("这是监控器模拟的错误")
        elif command == "reset_and_restart":
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            self.restart_application()

    def restart_application(self):
        self.save_config(force=True)
        subprocess.Popen([sys.executable] + sys.argv)
        self.quit()

    def register_settings_tab(self, name: str, widget_factory, enabled=True):
        self.plugin_settings_tabs[name] = (widget_factory, enabled)

    def register_settings_tab(self, name: str, widget_factory, enabled=True):
        """注册一个新的设置选项卡（在主设置对话框的Tab栏中）
        name: 选项卡显示名称
        widget_factory: 可调用对象，接受 parent 参数，返回 QWidget
        enabled: 是否启用
        """
        if not hasattr(self, 'plugin_settings_tabs'):
            self.plugin_settings_tabs = {}
        self.plugin_settings_tabs[name] = (widget_factory, enabled)

    def open_settings(self, tab="project", section=None):
        global tabs
        try:
            if hasattr(self, 'settings_dlg') and self.settings_dlg and self.settings_dlg.isVisible():
                self.settings_dlg.raise_()
                self.settings_dlg.activateWindow()
                return
        except RuntimeError:
            self.settings_dlg = None

        self.settings_dlg = QDialog()
        self.settings_dlg.setStyleSheet(get_theme_qss(self.theme))
        self.settings_dlg.setWindowTitle(tr("settings_title"))
        self.settings_dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        if self.settings_geometry:
            try:
                self.settings_dlg.restoreGeometry(self.settings_geometry)
            except:
                w, h = self.get_optimal_window_size(900, 650, "settings")
                self.settings_dlg.resize(w, h)
        else:
            w, h = self.get_optimal_window_size(900, 650, "settings")
            self.settings_dlg.resize(w, h)

        main_layout = QVBoxLayout(self.settings_dlg)

        lbl_title = QLabel(tr("settings_title"))
        lbl_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {get_theme_colors(self.theme)['accent']};")
        main_layout.addWidget(lbl_title)

        if hasattr(self, 'plugin_settings_tabs'):
            for tab_name, (widget_factory, enabled) in self.plugin_settings_tabs.items():
                if enabled:
                    try:
                        tab_widget = widget_factory(self.settings_dlg)
                        tabs.addTab(tab_widget, tab_name)
                    except Exception as e:
                        log_message(f"加载插件选项卡 {tab_name} 失败: {e}", "ERROR")

        tabs = QTabWidget()

        for tab_name, (widget_factory, enabled) in self.plugin_settings_tabs.items():
            if enabled:
                try:
                    tab_widget = widget_factory(self.settings_dlg)
                    tabs.addTab(tab_widget, tab_name)
                except Exception as e:
                    log_message(f"加载插件选项卡 {tab_name} 失败: {e}", "ERROR")

        def wrap_in_scroll(widget):
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(widget)
            scroll.setFrameShape(QFrame.Shape.NoFrame)
            scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
            return scroll

        tab_proj = QWidget()
        layout_proj = QVBoxLayout(tab_proj)

        self.list_proj = QListWidget()
        self.list_proj.setStyleSheet(
            f"background-color: {self.theme.frame_bg}; color: {self.theme.text_color}; border-radius: 5px;")
        for p in self.projects:
            self.list_proj.addItem(f"{p.name} ({p.target_date})")
        layout_proj.addWidget(self.list_proj)

        btn_layout_proj = QHBoxLayout()
        btn_add = QPushButton("➕ " + tr("add_project"))
        btn_add.clicked.connect(self.add_project_ui)
        btn_edit = QPushButton("✏️ " + tr("edit_project"))
        btn_edit.clicked.connect(self.edit_project_ui)
        btn_del = QPushButton("🗑️ " + tr("delete_project"))
        btn_del.setStyleSheet("background-color: #e74c3c; color: #FFFFFF; border-radius: 5px; padding: 6px;")
        btn_del.clicked.connect(self.del_project_ui)

        btn_custom = QPushButton("🎨 " + tr("customize_appearance"))
        btn_custom.setStyleSheet("background-color: #9b59b6; color: #FFFFFF; border-radius: 5px; padding: 6px;")
        btn_custom.clicked.connect(self.open_custom_appearance)
        btn_custom.setEnabled(False)

        btn_layout_proj.addWidget(btn_add)
        btn_layout_proj.addWidget(btn_edit)
        btn_layout_proj.addWidget(btn_del)
        btn_layout_proj.addWidget(btn_custom)
        layout_proj.addLayout(btn_layout_proj)

        self.list_proj.itemSelectionChanged.connect(
            lambda: btn_custom.setEnabled(len(self.list_proj.selectedItems()) > 0)
        )

        tabs.addTab(wrap_in_scroll(tab_proj), tr("project_management"))

        tab_global = QWidget()
        layout_global = QVBoxLayout(tab_global)

        grp_info = QGroupBox(tr("version_info"))
        lay_info = QVBoxLayout(grp_info)
        lay_info.addWidget(QLabel(f"{tr('current_version')}: {self.current_version} (Build {self.build_version})"))
        lay_info.addWidget(QLabel(f"{tr('python_env')}: Python {self.python_version} | {platform.system()}"))
        lay_info.addWidget(QLabel(f"{tr('data_dir')}: {self.data_dir}"))

        self.btn_check_update = QPushButton("🚀 检查更新")
        self.btn_check_update.setStyleSheet(
            "background-color: #3498db; color: white; border-radius: 4px; padding: 6px; font-weight: bold;")
        lay_info.addWidget(self.btn_check_update)

        def on_check_update_clicked():
            self.btn_check_update.setText("⏳ 正在请求服务器...")
            self.btn_check_update.setEnabled(False)

            self.update_thread = UpdateCheckerThread()

            def handle_result(data):
                self.btn_check_update.setText("🚀 更新")
                self.btn_check_update.setEnabled(True)

                server_build = data.get("build_version", 0)
                server_ver_str = data.get("version_str", "")
                download_url = data.get("download_url", "")

                if server_build > self.build_version:
                    reply = QMessageBox.question(
                        self.settings_dlg,
                        "✨ 发现新版本",
                        f"当前版本: {self.current_version}\n"
                        f"最新版本: {server_ver_str}\n\n"
                        f"是否立即前往下载？",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes and download_url:
                        webbrowser.open(download_url)
                else:
                    QMessageBox.information(self.settings_dlg, "提示", "当前已是最新版本！")

            def handle_error(err):
                self.btn_check_update.setText("🚀 检查更新")
                self.btn_check_update.setEnabled(True)
                QMessageBox.warning(self.settings_dlg, "网络错误", f"无法连接到更新服务器:\n{err}")

            self.update_thread.result_ready.connect(handle_result)
            self.update_thread.error_occurred.connect(handle_error)
            self.update_thread.start()

        self.btn_check_update.clicked.connect(on_check_update_clicked)

        btn_vote = QPushButton(tr("feature_vote"))
        btn_vote.setProperty("primary", True)
        btn_vote.clicked.connect(lambda: webbrowser.open("https://gitcode.com/2401_86556713/djs/discussions"))
        lay_info.addWidget(btn_vote)

        layout_global.addWidget(grp_info)

        grp_basic = QGroupBox(tr("global_settings"))
        lay_basic = QVBoxLayout(grp_basic)

        grp_debug = QGroupBox("🐛 调试与日志")
        lay_debug = QVBoxLayout(grp_debug)

        debug_layout = QHBoxLayout()
        debug_layout.addWidget(QLabel("日志等级:"))
        self.combo_debug = QComboBox()
        self.combo_debug.addItems(["❌ 关闭 (0)", "⚠️ 错误/警告 (1)", "ℹ️ 普通信息 (2)", "🔍 详细调试 (3)"])
        self.combo_debug.setCurrentIndex(DEBUG_MODE)
        self.combo_debug.currentIndexChanged.connect(self.auto_save_global_settings)
        debug_layout.addWidget(self.combo_debug)
        lay_debug.addLayout(debug_layout)

        btn_view_log = QPushButton("📄 查看日志文件")
        btn_view_log.clicked.connect(self.open_log_file)
        lay_debug.addWidget(btn_view_log)

        layout_global.addWidget(grp_debug)

        auto_start_lay = QHBoxLayout()
        auto_start_lay.addWidget(QLabel(tr("autostart") + ":"))
        self.chk_auto_start = QCheckBox("")
        self.chk_auto_start.setChecked(self.auto_start)
        self.chk_auto_start.toggled.connect(lambda v: setattr(self, 'auto_start', v) or self.auto_save_global_settings())
        auto_start_lay.addWidget(self.chk_auto_start)
        auto_start_lay.addStretch()
        lay_basic.addLayout(auto_start_lay)

        poem_lay = QHBoxLayout()
        poem_lay.addWidget(QLabel(tr("poem_level") + ":"))
        self.combo_poem = QComboBox()
        self.combo_poem.addItems([tr("poem_none"), tr("poem_primary"), tr("poem_junior"), tr("poem_senior")])
        self.combo_poem.setCurrentIndex(["none", "primary", "junior", "senior"].index(self.poem_level))
        self.combo_poem.currentIndexChanged.connect(self.auto_save_global_settings)
        poem_lay.addWidget(self.combo_poem)
        lay_basic.addLayout(poem_lay)

        lang_lay = QHBoxLayout()
        lang_lay.addWidget(QLabel(tr("language_label") + ":"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["🇨🇳 中文", "🇬🇧 English"])
        self.combo_lang.setCurrentIndex(0 if CURRENT_LANG == LANG_CHINESE else 1)
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        lang_lay.addWidget(self.combo_lang)
        lay_basic.addLayout(lang_lay)

        layout_global.addWidget(grp_basic)

        # 天气API配置
        grp_weather = QGroupBox(tr("weather_source"))
        lay_weather = QVBoxLayout(grp_weather)

        weather_src_lay = QHBoxLayout()
        weather_src_lay.addWidget(QLabel(tr("weather_source") + ":"))
        self.combo_weather_source = QComboBox()
        self.combo_weather_source.addItems(["wttr.in (" + tr("default") + ")", "Open-Meteo", tr("custom")])
        provider_map = {"wttr_in": 0, "open_meteo": 1, "custom": 2}
        self.combo_weather_source.setCurrentIndex(provider_map.get(self.weather_provider, 0))
        self.combo_weather_source.currentIndexChanged.connect(self._on_weather_source_changed)
        weather_src_lay.addWidget(self.combo_weather_source)
        lay_weather.addLayout(weather_src_lay)

        self.weather_custom_url_row = QWidget()
        custom_url_lay = QHBoxLayout(self.weather_custom_url_row)
        custom_url_lay.setContentsMargins(0, 0, 0, 0)
        custom_url_lay.addWidget(QLabel(tr("custom_url") + ":"))
        self.edit_custom_weather_url = QLineEdit()
        self.edit_custom_weather_url.setPlaceholderText("https://api.example.com/weather?city={city}")
        self.edit_custom_weather_url.setText(self.custom_weather_url)
        self.edit_custom_weather_url.textChanged.connect(self._on_weather_url_changed)
        custom_url_lay.addWidget(self.edit_custom_weather_url)
        lay_weather.addWidget(self.weather_custom_url_row)
        self.weather_custom_url_row.setVisible(self.weather_provider == "custom")

        layout_global.addWidget(grp_weather)

        layout_global.addStretch()
        tabs.addTab(wrap_in_scroll(tab_global), tr("global_settings"))

        tab_plugin = QWidget()
        plugin_main_layout = QVBoxLayout(tab_plugin)
        plugin_main_layout.setContentsMargins(10, 10, 10, 10)
        plugin_main_layout.setSpacing(10)

        self.plugin_header_widget = QWidget()
        top_row = QHBoxLayout(self.plugin_header_widget)
        top_row.setContentsMargins(0, 0, 0, 0)
        self.plugin_toggle = FluentToggleSwitch(checked=not self.global_disable_all_plugins)
        self.plugin_toggle.toggled.connect(self.toggle_global_disable_plugins)
        top_row.addWidget(QLabel("启用插件系统"))
        top_row.addWidget(self.plugin_toggle)
        top_row.addStretch()
        plugin_main_layout.addWidget(self.plugin_header_widget)

        self.plugin_intro_widget = QWidget()
        intro_card = QFrame()
        intro_card.setStyleSheet(f"""
            QFrame {{
                background-color: {get_theme_colors(self.theme)['intro_bg']};
                border-radius: 20px;
            }}
            QLabel {{
                color: {get_theme_colors(self.theme)['intro_text']};
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
                font-size: 14px;
            }}
            QLabel#CardTitle {{
                font-size: 26px;
                font-weight: bold;
                color: {get_theme_colors(self.theme)['intro_title']};
            }}
            QPushButton#EnableBtn {{
                background-color: {get_theme_colors(self.theme)['accent']};
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 14px 24px;
            }}
            QPushButton#EnableBtn:hover {{
                background-color: {get_theme_colors(self.theme)['hover_accent']};
            }}
            QPushButton#EnableBtn:pressed {{
                background-color: #005A9E;
            }}
        """)
        card_layout = QVBoxLayout(intro_card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.plug', color='#F0F0F0').pixmap(60, 60))
        card_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("欢迎使用CAC插件系统")
        title_label.setObjectName("CardTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel(
            "插件可以扩展倒计时桌面的功能，添加动态背景、桌面小工具、天气源等。\n"
            "为了安全，插件系统默认处于关闭状态。\n\n"
            "请从可信来源安装插件，并仔细审查其请求的权限。  制作:苗睿轩"
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc_label, alignment=Qt.AlignmentFlag.AlignCenter)

        enable_btn = QPushButton(" 开启插件系统")
        enable_btn.setObjectName("EnableBtn")
        enable_btn.setIcon(qta.icon('fa5s.power-off', color='white'))
        enable_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        enable_btn.clicked.connect(self.enable_plugin_system)
        card_layout.addWidget(enable_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        intro_inner = QVBoxLayout(self.plugin_intro_widget)
        intro_inner.addStretch()
        intro_inner.addWidget(intro_card)
        intro_inner.addStretch()
        plugin_main_layout.addWidget(self.plugin_intro_widget)

        self.plugin_management_widget = QWidget()
        mgmt_layout = QVBoxLayout(self.plugin_management_widget)
        mgmt_layout.setContentsMargins(0, 0, 0, 0)
        mgmt_layout.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(4)
        self.btn_plug_en = QPushButton(" 启用")
        self.btn_plug_en.setIcon(qta.icon('fa5s.play', color='white'))
        self.btn_plug_en.clicked.connect(self.enable_selected_plugin)
        self.btn_plug_dis = QPushButton(" 禁用")
        self.btn_plug_dis.setIcon(qta.icon('fa5s.stop', color='white'))
        self.btn_plug_dis.clicked.connect(self.disable_selected_plugin)
        self.btn_perm = QPushButton(" 权限")
        self.btn_perm.setIcon(qta.icon('fa5s.lock', color='white'))
        self.btn_perm.clicked.connect(self.manage_plugin_permissions)
        toolbar.addWidget(self.btn_plug_en)
        toolbar.addWidget(self.btn_plug_dis)
        toolbar.addWidget(self.btn_perm)
        toolbar.addStretch()
        left_layout.addLayout(toolbar)

        self.tree_plugins = QTreeWidget()
        self.tree_plugins.setHeaderLabels(["插件名称", "版本", "作者", "状态", "权限", "风险等级"])
        self.tree_plugins.setAlternatingRowColors(True)
        self.tree_plugins.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {get_theme_colors(self.theme)['tree_bg']};
                alternate-background-color: {get_theme_colors(self.theme)['alternate_bg']};
                color: {get_theme_colors(self.theme)['tree_text']};
                border: 1px solid {get_theme_colors(self.theme)['border_color']};
                border-radius: 6px;
                padding: 4px;
            }}
            QTreeWidget::item:selected {{
                background-color: {get_theme_colors(self.theme)['accent']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {get_theme_colors(self.theme)['header_bg']};
                color: {get_theme_colors(self.theme)['header_text']};
                border: none;
                padding: 6px;
            }}
        """)
        self.refresh_plugin_list()
        left_layout.addWidget(self.tree_plugins)

        self.empty_table_label = QLabel("暂无已安装插件\n请将插件文件放入 plugins 文件夹后刷新")
        self.empty_table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_table_label.setStyleSheet(f"color: {get_theme_colors(self.theme)['secondary_text']}; font-size: 14px; padding: 40px;")
        left_layout.addWidget(self.empty_table_label)
        self.empty_table_label.setVisible(len(self.plugin_manager.plugins) == 0)

        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        self.plugin_detail_group = QGroupBox("📋 插件详情")
        self.plugin_detail_group.setStyleSheet(f"""
            QGroupBox {{
                color: {get_theme_colors(self.theme)['text_color']};
                font-weight: bold;
                border: 1px solid {get_theme_colors(self.theme)['border_color']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        detail_layout_inner = QVBoxLayout(self.plugin_detail_group)
        self.detail_label = QLabel("请选择插件")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet(f"color: {get_theme_colors(self.theme)['secondary_text']};")
        detail_layout_inner.addWidget(self.detail_label)
        self.plugin_custom_widget = QStackedWidget()
        detail_layout_inner.addWidget(self.plugin_custom_widget)
        right_layout.addWidget(self.plugin_detail_group)

        self.log_combined_frame = QGroupBox("📜 日志与敏感操作记录")
        self.log_combined_frame.setStyleSheet(f"""
            QGroupBox {{
                color: {get_theme_colors(self.theme)['text_color']};
                font-weight: bold;
                border: 1px solid {get_theme_colors(self.theme)['border_color']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        log_combined_layout = QVBoxLayout(self.log_combined_frame)
        log_tabs = QTabWidget()
        log_page1 = QWidget()
        log_page1_layout = QVBoxLayout(log_page1)
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumBlockCount(500)
        log_page1_layout.addWidget(self.log_text)
        btn_refresh_log = QPushButton("刷新日志")
        btn_refresh_log.clicked.connect(self.update_plugin_log)
        log_page1_layout.addWidget(btn_refresh_log)
        log_tabs.addTab(log_page1, "常规日志")

        log_page2 = QWidget()
        log_page2_layout = QVBoxLayout(log_page2)
        self.sensitive_log_text = QPlainTextEdit()
        self.sensitive_log_text.setReadOnly(True)
        self.sensitive_log_text.setMaximumBlockCount(200)
        self.sensitive_log_text.setPlainText("\n".join(getattr(self, '_sensitive_log_entries', [])))
        log_page2_layout.addWidget(self.sensitive_log_text)
        btn_clear_sensitive = QPushButton("清空记录")
        btn_clear_sensitive.clicked.connect(self._clear_sensitive_log)
        log_page2_layout.addWidget(btn_clear_sensitive)
        log_tabs.addTab(log_page2, "敏感操作")

        log_combined_layout.addWidget(log_tabs)
        right_layout.addWidget(self.log_combined_frame)

        tc = get_theme_colors(self.theme)
        self.plugin_panels_group = QGroupBox("Plugin Settings")
        self.plugin_panels_group.setStyleSheet(
            "QGroupBox {"
            "  color: " + tc["text_color"] + ";"
            "  font-weight: bold;"
            "  border: 1px solid " + tc["border_color"] + ";"
            "  border-radius: 8px;"
            "  margin-top: 10px;"
            "  padding-top: 12px;"
            "}"
            "QGroupBox::title {"
            "  subcontrol-origin: margin;"
            "  left: 10px;"
            "  padding: 0 5px;"
            "}"
        )
        panels_layout = QVBoxLayout(self.plugin_panels_group)
        self.plugin_panels_list = QListWidget()
        self.plugin_panels_list.setMaximumHeight(120)
        self.plugin_panels_list.setStyleSheet(
            "QListWidget {"
            "  background-color: " + tc["panel_bg"] + ";"
            "  color: " + tc["text_color"] + ";"
            "  border: 1px solid " + tc["border_color"] + ";"
            "  border-radius: 4px;"
            "}"
            "QListWidget::item {"
            "  padding: 6px 10px; border-radius: 3px; margin: 1px 2px;"
            "}"
            "QListWidget::item:hover {"
            "  background-color: " + tc["input_bg"] + ";"
            "}"
            "QListWidget::item:selected {"
            "  background-color: " + tc["accent"] + ";"
            "  color: " + tc["selected_text"] + ";"
            "}"
        )
        self.plugin_panels_list.itemDoubleClicked.connect(self._open_plugin_panel)
        panels_layout.addWidget(self.plugin_panels_list)
        right_layout.addWidget(self.plugin_panels_group)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        mgmt_layout.addWidget(splitter)
        plugin_main_layout.addWidget(self.plugin_management_widget)

        self._update_plugin_ui_state()
        self.tree_plugins.itemSelectionChanged.connect(self.on_plugin_selected)
        self.tree_plugins.model().rowsInserted.connect(lambda: self.empty_table_label.setVisible(self.tree_plugins.topLevelItemCount() == 0))
        self.tree_plugins.model().rowsRemoved.connect(lambda: self.empty_table_label.setVisible(self.tree_plugins.topLevelItemCount() == 0))

        tabs.addTab(wrap_in_scroll(tab_plugin), "插件管理")

        self.tab_help = HelpTab(self)
        tabs.addTab(wrap_in_scroll(self.tab_help), tr("help"))

        main_layout.addWidget(tabs)

        grip_layout = QHBoxLayout()
        grip_layout.addStretch()
        grip_layout.addWidget(QSizeGrip(self.settings_dlg))
        main_layout.addLayout(grip_layout)

        self.settings_dlg.closeEvent = lambda event: self.on_settings_close(event)

        if tab == "help":
            tabs.setCurrentWidget(self.tab_help)
            if section:
                QTimer.singleShot(100, lambda: self.tab_help.navigate_to(section))

        self.settings_dlg.show()

        def on_settings_key_press(event):
            if event.key() == Qt.Key.Key_AsciiTilde or event.key() == Qt.Key.Key_QuoteLeft:
                console = DebugConsole(self, self.settings_dlg)
                console.show()

        self.settings_dlg.keyPressEvent = on_settings_key_press
        self.settings_dlg.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    
    def _refresh_plugin_panels(self):
        self.plugin_panels_list.clear()
        panels = getattr(self, "plugin_settings_panels", {})
        if self.global_disable_all_plugins:
            panels = {}
        else:
            enabled_names = {p.name for p in self.plugin_manager.plugins if p.enabled}
            panels = {pid: info for pid, info in panels.items()
                      if not info.get("plugin") or info.get("plugin") in enabled_names}
        if not panels:
            self.plugin_panels_list.addItem("(No registered panels)")
            self.plugin_panels_group.setVisible(False)
        else:
            self.plugin_panels_group.setVisible(True)
            for pid, panel_info in panels.items():
                item = QListWidgetItem(panel_info.get("name", pid))
                item.setData(Qt.ItemDataRole.UserRole, pid)
                self.plugin_panels_list.addItem(item)

    def _open_plugin_panel(self, item):
        panel_id = item.data(Qt.ItemDataRole.UserRole)
        if not panel_id:
            return
        panels = getattr(self, "plugin_settings_panels", {})
        panel_info = panels.get(panel_id)
        if not panel_info:
            return
        panel_plugin = panel_info.get("plugin")
        if panel_plugin:
            plugin_obj = next((p for p in self.plugin_manager.plugins if p.name == panel_plugin), None)
            if self.global_disable_all_plugins or not plugin_obj or not plugin_obj.enabled:
                QMessageBox.warning(self.settings_dlg, "Error", "该面板所属插件已禁用，无法打开")
                return
        panel_class = panel_info.get("class")
        if not panel_class:
            QMessageBox.warning(self.settings_dlg, "Error", "Panel class not found")
            return
        try:
            dialog = panel_class(self.plugin_manager, self.settings_dlg)
            dialog.setWindowTitle(panel_info.get("name", panel_id))
            dialog.show()
        except Exception as e:
            import traceback
            QMessageBox.critical(self.settings_dlg, "Error",
                f"Failed to open panel:\n{e}\n\n{{traceback.format_exc()}}")
    def on_settings_close(self, event):
        if hasattr(self, 'log_timer') and self.log_timer.isActive():
            self.log_timer.stop()
        self.settings_geometry = self.settings_dlg.saveGeometry()
        self.save_config(force=True)
        self.plugin_manager.trigger_event("on_settings_closed")
        self.settings_dlg = None
        event.accept()

    def _update_plugin_ui_state(self):
        if not hasattr(self, 'plugin_intro_widget') or not hasattr(self, 'plugin_management_widget'):
            return
        enabled = not self.global_disable_all_plugins
        self.plugin_intro_widget.setVisible(not enabled)
        self.plugin_management_widget.setVisible(enabled)
        if hasattr(self, 'plugin_header_widget'):
            self.plugin_header_widget.setVisible(enabled)
        if hasattr(self, 'plugin_toggle'):
            self.plugin_toggle.blockSignals(True)
            self.plugin_toggle.setChecked(enabled)
            self.plugin_toggle.blockSignals(False)
        if hasattr(self, 'log_combined_frame'):
            self.log_combined_frame.setVisible(enabled)
        if not enabled:
            try:
                if hasattr(self, 'log_text'):
                    self.log_text.clear()
                if hasattr(self, 'sensitive_log_text'):
                    self.sensitive_log_text.clear()
            except RuntimeError:
                pass
        self._refresh_plugin_panels()

    def toggle_global_disable_plugins(self, checked):
        self.global_disable_all_plugins = not checked
        self.save_config(force=True)
        self._update_plugin_ui_state()

    def enable_plugin_system(self):
        self.global_disable_all_plugins = False
        self.save_config(force=True)
        self._load_plugins_and_restore()
        self._update_plugin_ui_state()
        try:
            self.refresh_plugin_list()
        except (RuntimeError, AttributeError):
            pass

    def on_plugin_selected(self):
        item = self.tree_plugins.currentItem()
        if not item:
            self.detail_label.setText("请选择插件")
            while self.plugin_custom_widget.count():
                self.plugin_custom_widget.removeWidget(self.plugin_custom_widget.widget(0))
            return

        plugin_name = item.text(0)
        plugin = next((p for p in self.plugin_manager.plugins if p.name == plugin_name), None)
        if not plugin:
            return

        info = f"<b>名称:</b> {plugin.name}<br>"
        info += f"<b>版本:</b> {plugin.version}<br>"
        info += f"<b>作者:</b> {plugin.author}<br>"
        info += f"<b>描述:</b> {plugin.description or '无'}<br>"
        perms = []
        if plugin.permissions & PluginPermission.FILE_READ: perms.append("读取文件")
        if plugin.permissions & PluginPermission.FILE_WRITE: perms.append("写入文件")
        if plugin.permissions & PluginPermission.NETWORK: perms.append("网络")
        if plugin.permissions & PluginPermission.COMMAND: perms.append("系统命令")
        info += f"<b>当前权限:</b> {', '.join(perms) if perms else '无'}<br>"
        info += f"<b>状态:</b> {'启用' if plugin.enabled else '禁用'}<br>"
        self.detail_label.setText(info)

        while self.plugin_custom_widget.count():
            self.plugin_custom_widget.removeWidget(self.plugin_custom_widget.widget(0))

        if self.global_disable_all_plugins or not plugin.enabled:
            disabled_lbl = QLabel("🔒 该插件当前处于禁用状态，其功能与设置面板不可用。")
            disabled_lbl.setWordWrap(True)
            disabled_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            disabled_lbl.setStyleSheet(
                f"color: {get_theme_colors(self.theme)['secondary_text']}; padding: 20px;")
            self.plugin_custom_widget.addWidget(disabled_lbl)
            return

        if hasattr(plugin, 'get_info_widget'):
            _plugin_context.current_plugin = plugin
            try:
                custom_w = plugin.get_info_widget(self.settings_dlg)
            except Exception as e:
                plugin.log_plugin(f"构建设置面板失败: {e}", "ERROR")
                custom_w = None
            finally:
                _plugin_context.current_plugin = None
            if custom_w:
                self.plugin_custom_widget.addWidget(custom_w)

    def refresh_plugin_list(self):
        self.tree_plugins.clear()
        for p in self.plugin_manager.plugins:
            risk = self.plugin_manager.get_plugin_risk(p)
            status = "启用" if p.enabled else "禁用"
            if risk >= 2:
                status += " [危险]"
            perms = []
            if p.permissions & PluginPermission.FILE_READ: perms.append("R")
            if p.permissions & PluginPermission.FILE_WRITE: perms.append("W")
            if p.permissions & PluginPermission.NETWORK: perms.append("N")
            if p.permissions & PluginPermission.COMMAND: perms.append("C")
            if risk == 0:
                risk_text = "🟢 安全"
            elif risk == 1:
                risk_text = "🟡 低风险"
            elif risk == 2:
                risk_text = "🟠 中风险"
            else:
                risk_text = "🔴 高风险"
            item = QTreeWidgetItem([p.name, p.version, p.author, status, ",".join(perms) or "无", risk_text])
            self.tree_plugins.addTopLevelItem(item)

    def enable_selected_plugin(self):
        curr = self.tree_plugins.currentItem()
        if curr:
            name = curr.text(0)
            for p in self.plugin_manager.plugins:
                if p.name == name:
                    self.plugin_manager.enable_plugin(p)
                    self.refresh_plugin_list()
                    break

    def disable_selected_plugin(self):
        curr = self.tree_plugins.currentItem()
        if curr:
            name = curr.text(0)
            for p in self.plugin_manager.plugins:
                if p.name == name:
                    self.plugin_manager.disable_plugin(p)
                    self.refresh_plugin_list()
                    break

    def manage_plugin_permissions(self):
        curr = self.tree_plugins.currentItem()
        if not curr:
            return
        name = curr.text(0)
        plugin = next((p for p in self.plugin_manager.plugins if p.name == name), None)
        if not plugin:
            return

        dlg = QDialog(self.settings_dlg)
        dlg.setWindowTitle(f"权限管理 - {plugin.name}")
        layout = QVBoxLayout(dlg)

        perms = plugin.permissions
        cb_read = QCheckBox("📖 读取文件")
        cb_read.setChecked(bool(perms & PluginPermission.FILE_READ))
        cb_write = QCheckBox("📝 写入文件")
        cb_write.setChecked(bool(perms & PluginPermission.FILE_WRITE))
        cb_net = QCheckBox("🌐 网络连接")
        cb_net.setChecked(bool(perms & PluginPermission.NETWORK))
        cb_cmd = QCheckBox("⚡ 执行系统命令")
        cb_cmd.setChecked(bool(perms & PluginPermission.COMMAND))

        layout.addWidget(cb_read)
        layout.addWidget(cb_write)
        layout.addWidget(cb_net)
        layout.addWidget(cb_cmd)

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(lambda: self.save_plugin_permissions(plugin, cb_read, cb_write, cb_net, cb_cmd, dlg))
        layout.addWidget(btn_save)

        dlg.exec()

    def save_plugin_permissions(self, plugin, cb_read, cb_write, cb_net, cb_cmd, dlg):
        new_perms = PluginPermission.NONE
        if cb_read.isChecked(): new_perms |= PluginPermission.FILE_READ
        if cb_write.isChecked(): new_perms |= PluginPermission.FILE_WRITE
        if cb_net.isChecked(): new_perms |= PluginPermission.NETWORK
        if cb_cmd.isChecked(): new_perms |= PluginPermission.COMMAND
        self.plugin_manager.set_plugin_permissions(plugin, new_perms)
        self.refresh_plugin_list()
        dlg.accept()

    def update_plugin_log(self):
        try:
            logs = []
            for p in self.plugin_manager.plugins:
                for entry in p.log[-50:]:
                    logs.append(f"[{p.name}] {entry}")
            logs.sort(reverse=True)
            self.log_text.setPlainText("\n".join(logs[-200:]))
        except RuntimeError:
            if hasattr(self, 'log_timer'):
                self.log_timer.stop()

    def open_custom_appearance(self):
        selected = self.list_proj.selectedItems()
        if not selected:
            return
        index = self.list_proj.row(selected[0])
        project = self.projects[index]
        target_window = None
        for w in self.windows:
            if w.project == project:
                target_window = w
                break
        editor = AppearanceEditor(project, target_window, self.settings_dlg)
        editor.finished.connect(lambda: self.save_config(force=True))
        editor.show()

    def add_project_ui(self):
        new_proj = CountdownProject(screen_width=self.primaryScreen().size().width(),
                                     screen_height=self.primaryScreen().size().height())
        self.projects.append(new_proj)
        self.list_proj.addItem(f"{new_proj.name} ({new_proj.target_date})")
        self.create_windows()
        self.save_config(force=True)

    def edit_project_ui(self):
        row = self.list_proj.currentRow()
        if row >= 0:
            proj = self.projects[row]
            editor = ProjectEditorDialog(self, proj, self.settings_dlg)
            if editor.exec():
                self.list_proj.item(row).setText(f"{proj.name} ({proj.target_date})")
                self.create_windows()
                self.save_config(force=True)

    def del_project_ui(self):
        row = self.list_proj.currentRow()
        if row >= 0:
            if len(self.projects) <= 1:
                QMessageBox.warning(self.settings_dlg, "警告", "至少需要保留一个项目！")
                return
            del self.projects[row]
            self.list_proj.takeItem(row)
            self.create_windows()
            self.save_config(force=True)

    def _on_weather_source_changed(self, index):
        provider_map = {0: "wttr_in", 1: "open_meteo", 2: "custom"}
        self.weather_provider = provider_map.get(index, "wttr_in")
        self.weather_custom_url_row.setVisible(self.weather_provider == "custom")
        self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _on_weather_url_changed(self, text):
        self.custom_weather_url = text.strip()
        if self.weather_provider == "custom":
            self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _apply_weather_config_to_windows(self):
        """将天气配置应用到所有窗口并刷新"""
        for w in self.windows:
            if hasattr(w, 'weather_fetcher') and w.weather_fetcher:
                w.weather_fetcher.api_provider = self.weather_provider
                w.weather_fetcher.custom_url_template = self.custom_weather_url
                w.weather_fetcher.fetch(w.project.weather_city)

    def auto_save_global_settings(self, _=None):
        index = self.combo_poem.currentIndex()
        if index == 0:
            self.poem_level = "none"
        elif index == 1:
            self.poem_level = "primary"
        elif index == 2:
            self.poem_level = "junior"
        elif index == 3:
            self.poem_level = "senior"
        self.set_auto_start_registry(self.auto_start)

        global DEBUG_MODE
        DEBUG_MODE = self.combo_debug.currentIndex()

        self.save_config(force=True)
        self.update_daily_poem()
        for win in self.windows:
            poem_text = self.daily_poem if self.poem_level != "none" else ""
            win.poem_label.stop_animation()
            win.poem_label.start_animation(poem_text)
            win.refresh(theme_change=True)

    def set_auto_start_registry(self, enabled):
        try:
            if sys.platform == "win32":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_SET_VALUE)
                if enabled:
                    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
                    autostart_path = os.path.join(base_dir, "autostart.exe")
                    if os.path.exists(autostart_path):
                        executable = f'"{autostart_path}"'
                    else:
                        executable = f'"{sys.executable}"' if getattr(sys, 'frozen', False) else f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
                    winreg.SetValueEx(key, "CountdownApp", 0, winreg.REG_SZ, executable)
                else:
                    try:
                        winreg.DeleteValue(key, "CountdownApp")
                    except FileNotFoundError:
                        pass
                winreg.CloseKey(key)
        except Exception as e:
            log_message(f"设置开机自启动失败: {e}", "ERROR")

    def _on_language_changed(self, index):
        global CURRENT_LANG
        new_lang = LANG_CHINESE if index == 0 else LANG_ENGLISH
        if new_lang == CURRENT_LANG:
            return
        CURRENT_LANG = new_lang
        self.save_config(force=True)
        for win in self.windows:
            win.init_menu()
            win.update_countdown()
        QMessageBox.information(
            self.settings_dlg if hasattr(self, 'settings_dlg') and self.settings_dlg else None,
            tr("language_label"),
            "语言已切换，部分界面将在重启后完全生效。\nLanguage changed. Some UI will update after restart."
        )

if __name__ == "__main__":
    import sys
    app = CountdownApp(sys.argv)
    sys.exit(app.exec())