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
import re
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
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
from PyQt6.QtCore import (Qt, QTimer, QThread, pyqtSignal, QObject, QPoint, QRect,
                          QPropertyAnimation, QEasingCurve, QRectF, QPointF, QByteArray,
                          pyqtProperty, QSize, QEvent, QDate, qVersion, PYQT_VERSION_STR, QUrl)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import (QColor, QFont, QPainter, QPainterPath, QPixmap, QImage,
                         QIcon, QAction, QPen, QBrush, QPalette, QLinearGradient, QRadialGradient,
                         QFontDatabase, QMovie, QFontMetrics, QTextLayout, QTextOption, QTextCursor,
                         QCursor, QTextCharFormat, QTransform)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect,
                             QSystemTrayIcon, QMenu, QMessageBox, QFileDialog,
                             QColorDialog, QInputDialog, QScrollArea,
                             QDialog, QLineEdit, QCheckBox, QComboBox, QSpinBox,
                             QSlider, QTreeWidget, QTreeWidgetItem, QTabWidget,
                             QGroupBox, QPlainTextEdit,
                             QListWidget, QListWidgetItem, QFormLayout,
                             QDoubleSpinBox, QGraphicsOpacityEffect, QSizeGrip,
                             QProgressBar, QSizePolicy, QTextEdit,
                             QFrame, QStackedWidget, QSplitter, QCalendarWidget,
                             QAbstractSpinBox, QRadioButton, QButtonGroup)
try:
    from PyQt6.QtOpenGL import (QOpenGLWindow, QOpenGLShaderProgram, QOpenGLShader,
                                 QOpenGLBuffer, QOpenGLVertexArrayObject,
                                 QOpenGLFunctions_4_1_Core, QOpenGLFunctions_2_1,
                                 QOpenGLVersionFunctionsFactory, QOpenGLVersionProfile)
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
    from PyQt6.QtGui import QSurfaceFormat, QOpenGLContext, QOffscreenSurface
    HAS_OPENGL = True
    HAS_OPENGL_41 = True
    HAS_OPENGL_21 = True
except ImportError:
    HAS_OPENGL = False
    HAS_OPENGL_41 = False
    HAS_OPENGL_21 = False


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

def get_system_theme(force_dark=None):
    dark = is_system_dark() if force_dark is None else force_dark
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
    _ac = QColor(c['accent'])
    _ac_light = _ac.lighter(118).name()
    _ac_dark = _ac.darker(118).name()
    _dg = QColor(c['danger'])
    _dg_light = _dg.lighter(115).name()
    _dg_dark = _dg.darker(125).name()

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
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {_ac_light}, stop:1 {_ac_dark});
        color: {c['btn_text']};
        border: 1px solid {_ac_dark};
    }}
    QPushButton[primary="true"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {_ac.lighter(130).name()}, stop:1 {c['accent']});
        color: {c['hover_btn_text']};
        border: 1px solid {_ac_dark};
    }}
    QPushButton[secondary="true"] {{
        background: transparent; color: {c['text_color']};
        border: 1px solid {c['border_color']};
    }}
    QPushButton[secondary="true"]:hover {{
        border-color: {c['accent']}; color: {c['accent']};
    }}
    QPushButton[danger="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {_dg_light}, stop:1 {_dg_dark});
        color: #FFFFFF;
        border: 1px solid {_dg_dark};
    }}
    QPushButton[danger="true"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {_dg.lighter(130).name()}, stop:1 {c['danger']});
        color: #FFFFFF;
        border: 1px solid {_dg_dark};
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
    try:
        print(*args, file=out, **kwargs)
        out.flush()
    except (OSError, ValueError):
        try:
            out.flush()
        except Exception:
            pass

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
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 1024 * 1024:
            for i in (2, 1):
                src = os.path.join(data_dir, f"LOG.{i}.txt")
                dst = os.path.join(data_dir, f"LOG.{i + 1}.txt")
                if os.path.exists(src):
                    os.replace(src, dst)
            os.replace(LOG_FILE, os.path.join(data_dir, "LOG.1.txt"))
    except Exception:
        pass
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

HOLIDAY_API_BASE = "https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{}.json"

_holiday_cache_loaded = False


def _get_holiday_cache_path(data_dir):
    return os.path.join(data_dir, "holidays.json")


def _atomic_replace_file(src, dst, retries=4, delay=0.05):
    for attempt in range(retries):
        try:
            os.replace(src, dst)
            return
        except OSError:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                import shutil
                shutil.copy2(src, dst)
                os.remove(src)


def _inject_holidays(year_data):
    injected = 0
    for entry in year_data.get("days", []):
        try:
            d = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            name = entry.get("name", "")
            if entry.get("isOffDay"):
                chinese_calendar.constants.holidays[d] = name
            else:
                chinese_calendar.constants.workdays[d] = name
            injected += 1
        except (ValueError, KeyError) as e:
            log_message(f"跳过无效假期条目 {entry}: {e}", "WARNING")
            continue
    return injected


def load_holiday_cache(data_dir):
    global _holiday_cache_loaded
    cache_path = _get_holiday_cache_path(data_dir)
    if not os.path.exists(cache_path):
        log_message("未找到本地假期数据缓存，将使用库内置数据", "INFO")
        return
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
        total = 0
        for year_str, year_data in cache.items():
            total += _inject_holidays(year_data)
        _holiday_cache_loaded = True
        log_message(f"已加载本地假期数据缓存: {len(cache)} 个年份, {total} 条记录", "INFO")
    except Exception as e:
        log_message(f"加载假期缓存失败: {e}", "WARNING")


def fetch_holidays_for_year(year):
    url = HOLIDAY_API_BASE.format(year)
    log_message(f"正在获取假期数据: {url}", "INFO")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def update_holidays_online(data_dir, years=None, callback=None):
    if years is None:
        cur_year = datetime.now().year
        years = list(range(cur_year, cur_year + 3))
    log_message(f"开始更新假期数据，目标年份: {years}", "INFO")
    cache_path = _get_holiday_cache_path(data_dir)
    cache = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception as e:
            log_message(f"读取旧缓存失败，将重建: {e}", "WARNING")
            cache = {}
    updated_years = []
    failed_years = []
    for year in years:
        try:
            year_data = fetch_holidays_for_year(year)
            if year_data.get("days"):
                cache[str(year)] = year_data
                updated_years.append(year)
                log_message(f"获取 {year} 年假期数据成功: {len(year_data['days'])} 条", "INFO")
            else:
                log_message(f"{year} 年假期数据为空", "WARNING")
                failed_years.append((year, "数据为空"))
        except Exception as e:
            log_message(f"获取 {year} 年假期数据失败: {e}", "WARNING")
            failed_years.append((year, str(e)))
    if updated_years:
        try:
            tmp_path = cache_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            _atomic_replace_file(tmp_path, cache_path)
            injected_total = 0
            for year in updated_years:
                injected_total += _inject_holidays(cache[str(year)])
            global _holiday_cache_loaded
            _holiday_cache_loaded = True
            log_message(f"假期数据已更新并注入: {updated_years}, 共 {injected_total} 条", "INFO")
        except Exception as e:
            log_message(f"保存假期缓存失败: {e}", "WARNING")
    else:
        log_message("本次无任何年份更新成功", "WARNING")
    if callback:
        callback(updated_years, failed_years)
    return updated_years, failed_years


class HolidayUpdateThread(QThread):
    finished_signal = pyqtSignal(list, list)

    def __init__(self, data_dir, years=None):
        super().__init__()
        self.data_dir = data_dir
        self.years = years

    def run(self):
        try:
            updated, failed = update_holidays_online(self.data_dir, self.years)
            self.finished_signal.emit(updated, failed)
        except Exception as e:
            log_message(f"假期更新线程异常: {e}", "ERROR")
            self.finished_signal.emit([], [(0, str(e))])


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

        _fallback_logged = False

        def _safe_is_workday(d):
            nonlocal _fallback_logged
            try:
                return chinese_calendar.is_workday(d)
            except NotImplementedError:
                if not _fallback_logged:
                    log_message(f"年份 {d.year} 超出 chinese_calendar 支持范围，回退到标准工作日", "WARNING")
                    _fallback_logged = True
                return d.weekday() < 5

        def _safe_get_holiday_detail(d):
            nonlocal _fallback_logged
            try:
                return chinese_calendar.get_holiday_detail(d)
            except NotImplementedError:
                if not _fallback_logged:
                    log_message(f"年份 {d.year} 超出 chinese_calendar 支持范围，回退到标准工作日", "WARNING")
                    _fallback_logged = True
                return (d.weekday() >= 5, "")

        if total_days > 0:
            for i in range(total_days):
                current_date = today.date() + timedelta(days=i + 1)
                if _safe_is_workday(current_date):
                    work_days += 1
                else:
                    on_holiday, name = _safe_get_holiday_detail(current_date)
                    if on_holiday and i == 0:
                        holiday_name = name

        if _safe_is_workday(today.date()):
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


FORMAT_PRESET_DHM = "{days}天 {hours}时 {minutes}分"
FORMAT_PRESET_HMS = "{hours}时 {minutes}分 {seconds}秒"


def sanitize_format_template(template):
    if template is None:
        return FORMAT_PRESET_DHM
    cleaned = str(template).replace("{{", "").replace("}}", "")
    return cleaned


def validate_format_template(template):
    if not template or not template.strip():
        return False, "模板不能为空"
    try:
        template.format(days=1, hours=2, minutes=3, seconds=4)
    except KeyError as e:
        return False, f"未知占位符: {e}（可用 days/hours/minutes/seconds）"
    except (ValueError, IndexError) as e:
        return False, f"模板语法错误: {e}"
    return True, ""


def render_format_template(template, days_float):
    total_seconds = max(0.0, days_float * 86400)
    d = int(total_seconds // 86400)
    h = int((total_seconds % 86400) // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    try:
        escaped = template.replace("{", "\x00").replace("}", "\x01")
        escaped = escaped.replace("\x00days\x01", str(d))
        escaped = escaped.replace("\x00hours\x01", str(h))
        escaped = escaped.replace("\x00minutes\x01", str(m))
        escaped = escaped.replace("\x00seconds\x01", str(s))
        escaped = escaped.replace("\x00", "{").replace("\x01", "}")
        return escaped
    except Exception:
        return f"{d}天 {h}时 {m}分"


WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def get_next_recurrence(project, now=None):
    if now is None:
        now = datetime.now()
    weekdays = getattr(project, 'recur_weekdays', None) or []
    if not weekdays:
        return None
    try:
        hh, mm = map(int, (project.target_time or "00:00").split(":")[:2])
    except (ValueError, AttributeError):
        hh, mm = 0, 0
    end_date = None
    end_str = getattr(project, 'recur_end_date', "") or ""
    if end_str:
        try:
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        except ValueError:
            end_date = None
    for i in range(0, 370):
        d = now.date() + timedelta(days=i)
        if d.weekday() not in weekdays:
            continue
        cand = datetime(d.year, d.month, d.day, hh, mm)
        if cand <= now:
            continue
        if end_date and d > end_date:
            return None
        return cand
    return None


def get_effective_target(project):
    if getattr(project, 'project_type', 'normal') != 'recurring':
        return project.target_date, project.target_time
    nxt = get_next_recurrence(project)
    if nxt is None:
        return None, None
    return nxt.strftime("%Y-%m-%d"), nxt.strftime("%H:%M")


def describe_next_recurrence(project):
    nxt = get_next_recurrence(project)
    if nxt is None:
        return "已结束"
    now = datetime.now()
    days_until = (nxt.date() - now.date()).days
    time_str = nxt.strftime("%H:%M")
    if days_until == 0:
        return f"今天 {time_str}"
    if days_until == 1:
        return f"明天 {time_str}"
    end_of_week = now.date() + timedelta(days=(6 - now.weekday()))
    if nxt.date() <= end_of_week:
        return f"{WEEKDAY_NAMES[nxt.weekday()]} {time_str}"
    if nxt.date() <= end_of_week + timedelta(days=7):
        return f"下{WEEKDAY_NAMES[nxt.weekday()]} {time_str}"
    return f"{nxt.strftime('%Y-%m-%d')} {time_str}"

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
        self.enable_flip_animation = True
        self.gradient_start = QColor("#00f2fe")
        self.gradient_end = QColor("#4facfe")
        self.glow_color = QColor(79, 172, 254, 160)
        self._pulse_phase = 0.0
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._tick_pulse)
        self._pulse_timer.start(80)
        self._blink_enabled = True
        self._blink_visible = True
        self._blink_interval = 500
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._tick_blink)
        self.setMinimumSize(200, 65)
        self.setFont(QFont("Microsoft YaHei", 28, QFont.Weight.Bold))

    def _tick_pulse(self):
        if not self.isVisible():
            return
        if not self.use_neon:
            return
        self._pulse_phase += 0.05
        if self._pulse_phase > 2 * math.pi:
            self._pulse_phase -= 2 * math.pi
        self.update()

    def _tick_blink(self):
        if not self._expired or not self._blink_enabled:
            return
        self._blink_visible = not self._blink_visible
        self.update()

    def startBlink(self, interval=None):
        if interval is not None and interval > 0:
            self._blink_interval = interval
        self._blink_enabled = True
        self._blink_visible = True
        self._blink_timer.start(self._blink_interval)

    def stopBlink(self):
        self._blink_timer.stop()
        self._blink_visible = True
        if self._expired:
            self.update()

    def setBlinkSpeed(self, ms):
        if ms > 0:
            self._blink_interval = ms
            if self._blink_timer.isActive():
                self._blink_timer.setInterval(ms)

    def setBlinkEnabled(self, enabled):
        self._blink_enabled = enabled
        if not enabled:
            self.stopBlink()
        elif self._expired:
            self.startBlink()

    def blinkInfo(self):
        return {
            "enabled": self._blink_enabled,
            "active": self._blink_timer.isActive(),
            "visible": self._blink_visible,
            "interval_ms": self._blink_interval,
            "expired": self._expired,
        }

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
            return render_format_template(self._display_format_template, days_float), ""
        return f"{days_float:.3f}", " 天"

    def uses_seconds(self):
        if self._display_format == "custom":
            return "{seconds}" in (self._display_format_template or "")
        return False

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
        self.stopBlink()
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
        if not getattr(self, 'enable_flip_animation', True) or len(self._current_str) != len(self._target_str):
            self._current_str = self._target_str
            self._anim_progress = 1.0
            self.update()
            self.value_changed.emit(new_value)
            return
        self._anim.setDuration(400 if self.uses_seconds() else 800)
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
        # 启动到期闪烁动画
        if self._blink_enabled:
            self.startBlink()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(self.font())

        if self._expired:
            if self._blink_enabled and not self._blink_visible:
                if self.use_neon:
                    pulse = (math.sin(self._pulse_phase) + 1.0) / 2.0
                    glow = QColor(243, 139, 168, int(10 + pulse * 15))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(glow)
                    painter.drawRoundedRect(QRectF(self.rect().adjusted(4, 4, -4, -4)), 10, 10)
                return

            display_text = self._target_str
            base_font = self.font()
            fm = QFontMetrics(base_font)
            text_width = fm.horizontalAdvance(display_text)
            avail = self.width() - 16
            if avail > 0 and text_width > avail:
                scale = avail / text_width
                scaled = QFont(base_font)
                ps = base_font.pixelSize()
                if ps > 0:
                    scaled.setPixelSize(max(8, int(ps * scale)))
                else:
                    scaled.setPointSize(max(6, int(base_font.pointSize() * scale)))
                base_font = scaled
                fm = QFontMetrics(scaled)
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
            painter.setFont(base_font)
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
        base_font = self.font()
        fm = QFontMetrics(base_font)

        full_text = target_str + unit
        text_width = fm.horizontalAdvance(full_text)
        avail = self.width() - 16
        if avail > 0 and text_width > avail:
            scale = avail / text_width
            scaled = QFont(base_font)
            ps = base_font.pixelSize()
            if ps > 0:
                scaled.setPixelSize(max(8, int(ps * scale)))
            else:
                scaled.setPointSize(max(6, int(base_font.pointSize() * scale)))
            base_font = scaled
            fm = QFontMetrics(scaled)
            text_width = fm.horizontalAdvance(full_text)
        painter.setFont(base_font)
        text_height = fm.height()
        x = (self.width() - text_width) // 2
        y = (self.height() - text_height) // 2 + fm.ascent()
        progress = self._anim_progress
        clip_top = int(y - fm.ascent())
        clip_h = int(fm.height())

        if digit_str != target_str and progress < 1.0:
            char_x = x
            min_len = min(len(digit_str), len(target_str))
            for ci in range(max(len(digit_str), len(target_str))):
                old_ch = digit_str[ci] if ci < len(digit_str) else ""
                new_ch = target_str[ci] if ci < len(target_str) else ""
                ch_w = fm.horizontalAdvance(new_ch if new_ch else old_ch)

                if ci < min_len and old_ch == new_ch:
                    painter.setPen(self._text_color())
                    painter.drawText(int(char_x), int(y), new_ch)
                    char_x += ch_w
                    continue

                if old_ch and new_ch and not (old_ch.isdigit() and new_ch.isdigit()):
                    painter.setPen(self._text_color())
                    painter.drawText(int(char_x), int(y), new_ch)
                    char_x += ch_w
                    continue

                painter.save()
                painter.setClipRect(QRect(int(char_x), clip_top, int(ch_w) + 1, clip_h))
                new_y = y + (1.0 - progress) * text_height
                painter.setPen(self._text_color())
                if new_ch:
                    painter.drawText(int(char_x), int(new_y), new_ch)
                old_y = y - progress * text_height
                fade_alpha = max(15, int(140 * (1.0 - progress)))
                painter.setPen(self._text_color(alpha=fade_alpha))
                if old_ch:
                    painter.drawText(int(char_x), int(old_y), old_ch)
                painter.restore()
                char_x += ch_w
        else:
            painter.setPen(self._text_color())
            painter.drawText(int(x), int(y), target_str)

        painter.setPen(self._text_color(alpha=220))
        unit_x = x + fm.horizontalAdvance(target_str)
        painter.drawText(int(unit_x), int(y), unit)

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
        if self._raw_days <= 0 and self._display_format not in ("decimal", "integer"):
            sample_str, sample_unit = self._format_value(123 + 86399 / 86400)
            sample_text = sample_str + sample_unit
            if fm.horizontalAdvance(sample_text) > fm.horizontalAdvance(text):
                text = sample_text
        width = fm.horizontalAdvance(text) + 40
        height = fm.height() + 20
        return QSize(max(220, width), max(60, height))

# 打字机标签
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
        self._text_color_hex = "#E0E0E0" if is_system_dark() else "#2c3e50"
        self._opacity = 1.0
        self._line_spacing = 1.2
        self._marquee = False
        self._scroll_x = 0
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._scroll_step)

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

    def set_line_spacing(self, factor):
        try:
            factor = float(factor)
        except (TypeError, ValueError):
            factor = 1.2
        self._line_spacing = max(0.8, min(3.0, factor))
        self.updateGeometry()
        self.update()

    def set_marquee(self, on):
        on = bool(on)
        if on == self._marquee:
            return
        self._marquee = on
        if on:
            self._timer.stop()
            self._delay_timer.stop()
            self._current_display = self._full_text or self._current_display
            self._show_cursor = False
            self._scroll_x = 0
            self._scroll_timer.start(40)
        else:
            self._scroll_timer.stop()
            self._scroll_x = 0
        self.updateGeometry()
        self.update()

    def _scroll_step(self):
        if not self._marquee or not self.isVisible():
            return
        fm = QFontMetrics(self.font())
        text_w = fm.horizontalAdvance(self._current_display)
        if text_w <= self.width():
            self._scroll_x = 0
        else:
            self._scroll_x += 2
            if self._scroll_x > text_w + 40:
                self._scroll_x = -self.width()
        self.update()

    def _needs_marquee(self):
        if not self._current_display:
            return False
        fm = QFontMetrics(self.font())
        return fm.horizontalAdvance(self._current_display) > self.width()

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
        if self._marquee:
            return int(QFontMetrics(self.font()).height() * self._line_spacing) + 14
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
        leading = QFontMetrics(self.font()).leading() * self._line_spacing

        layout.beginLayout()
        y = 0
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(usable_width)
            y += leading
            line.setPosition(QPointF(4, y))
            y += line.height() * self._line_spacing
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
        if self._marquee:
            self._current_display = new_text
            self._char_index = len(new_text)
            self._show_cursor = False
            self._on_finished = None
            self._scroll_x = 0
            self.updateGeometry()
            self.update()
            if on_finished:
                on_finished()
            return
        if self._current_display == new_text:
            self._char_index = len(new_text)
            self._show_cursor = False
            self.update()
            if on_finished:
                on_finished()
            return
        self._on_finished = on_finished
        if self._current_display:
            self._is_deleting = True
            self._char_index = len(self._current_display)
            self._show_cursor = True
            self._timer.start(max(30, self._speed // 2))
        else:
            self._is_deleting = False
            self._char_index = 0
            self._show_cursor = True
            self._timer.start(self._speed)
        if isinstance(self.graphicsEffect(), QGraphicsOpacityEffect):
            self.setGraphicsEffect(None)

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

        if self._marquee:
            fm = QFontMetrics(self.font())
            text_w = fm.horizontalAdvance(self._current_display)
            if text_w <= self.width():
                x = (self.width() - text_w) // 2
            else:
                x = self.width() - self._scroll_x
            y = (self.height() - fm.height()) // 2 + fm.ascent()
            painter.setPen(text_color)
            painter.drawText(int(x), int(y), self._current_display)
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


def _weather_ring_color(text):
    """根据天气文字返回圆形挂件的主色"""
    if not text:
        return QColor(120, 180, 240, 220)
    t = text
    if "雷" in t:
        return QColor(155, 89, 182, 220)
    if "雪" in t:
        return QColor(236, 240, 241, 230)
    if "大雨" in t or "大阵雨" in t or "暴雨" in t:
        return QColor(41, 128, 185, 230)
    if "雨" in t or "阵雨" in t or "毛毛雨" in t:
        return QColor(52, 152, 219, 220)
    if "雾" in t or "霾" in t:
        return QColor(149, 165, 166, 220)
    if "阴" in t:
        return QColor(120, 130, 145, 220)
    if "晴" in t:
        return QColor(241, 196, 15, 230)
    if "多云" in t:
        return QColor(174, 196, 225, 220)
    return QColor(120, 180, 240, 220)


class CircularWeatherWidget(QWidget):
    """圆形天气挂件：外圈颜色随天气变化，圈内显示图标+温度，下方显示城市"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._temp = ""
        self._emoji = "🌤️"
        self._icon_path = None
        self._city = ""
        self._raw_text = ""
        self._ring_color = QColor(120, 180, 240, 220)
        self._font_size = 18
        self._fg_color = QColor(240, 244, 248) if is_system_dark() else QColor(45, 55, 75)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setMinimumSize(72, 88)

    def sizeHint(self):
        return QSize(140, 160)

    def setText(self, text):
        self._raw_text = text or ""
        self._parse(text)
        self.update()

    def setFont(self, font):
        super().setFont(font)
        try:
            self._font_size = font.pointSize()
        except Exception:
            pass
        self.update()

    def setStyleSheet(self, qss):
        col_match = re.search(r"color:\s*(#[0-9A-Fa-f]{6,8}|rgba?\([^)]+\))", qss or "")
        if col_match:
            c = col_match.group(1)
            if c.startswith("#"):
                self._fg_color = QColor(c)
            else:
                self._fg_color = QColor(c)
        self.update()

    def _parse(self, text):
        if not text:
            return
        m = re.search(r'(-?\d+)\s*°', text)
        if m:
            self._temp = m.group(1) + "°"
        else:
            m2 = re.search(r'(-?\d+)\s*(?:°?C|℃)', text)
            if m2:
                self._temp = m2.group(1) + "°"
        img_match = re.search(r'src="file:///([^"]+)"', text)
        if img_match:
            self._icon_path = img_match.group(1).replace("/", os.sep)
        else:
            self._icon_path = None
        plain = re.sub(r'<[^>]+>', '', text).strip()
        emoji_match = re.match(r'^([\U0001F300-\U0001FAFF\u2600-\u27BF])', plain)
        if emoji_match:
            self._emoji = emoji_match.group(1)
            plain = plain[1:].strip()
        parts = re.split(r'[·\s]+', plain)
        parts = [p.strip() for p in parts if p.strip()]
        if parts:
            self._city = parts[0]
        weather_text = plain
        self._ring_color = _weather_ring_color(weather_text)

    def _set_city_from_fetcher(self, fetcher):
        try:
            if fetcher and fetcher.city_name:
                self._city = fetcher.city_name
                self.update()
        except Exception:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        w, h = self.width(), self.height()
        if w < 10 or h < 10:
            return
        city_h = max(10, int(h * 0.13)) if self._city else 0
        avail_h = h - city_h - 6
        circle_d = min(w, avail_h) - 4
        circle_d = max(circle_d, 32)
        cx = w / 2
        cy = circle_d / 2 + 3
        ring_w = max(1, circle_d // 28)
        painter.setPen(QPen(self._ring_color, ring_w))
        painter.setBrush(QColor(15, 22, 38, 180) if is_system_dark() else QColor(255, 255, 255, 210))
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2, circle_d / 2)
        painter.setPen(QPen(QColor(self._ring_color.red(), self._ring_color.green(), self._ring_color.blue(), 60), ring_w + 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2 + 2, circle_d / 2 + 2)
        icon_size = int(circle_d * 0.42)
        if self._icon_path and os.path.exists(self._icon_path):
            img = QImage(self._icon_path)
            if not img.isNull():
                pix = QPixmap.fromImage(img).scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                painter.drawPixmap(QPointF(cx - pix.width() / 2, cy - circle_d / 2 + 6), pix)
        else:
            emoji_font = QFont("Segoe UI Emoji")
            emoji_font.setPointSizeF(max(6, circle_d / 5.5))
            painter.setFont(emoji_font)
            painter.setPen(self._fg_color)
            painter.drawText(QRectF(cx - circle_d / 2, cy - circle_d / 2 + 4, circle_d, icon_size + 4), Qt.AlignmentFlag.AlignCenter, self._emoji)
        temp_font = QFont("Microsoft YaHei")
        temp_font.setBold(True)
        temp_font.setPointSizeF(max(7, circle_d / 6.5))
        painter.setFont(temp_font)
        painter.setPen(self._fg_color)
        painter.drawText(QRectF(cx - circle_d / 2, cy - 2, circle_d, circle_d / 2 + 2), Qt.AlignmentFlag.AlignCenter, self._temp or "--")
        if self._city:
            city_font = QFont("Microsoft YaHei")
            city_font.setPointSizeF(max(6, circle_d / 12))
            painter.setFont(city_font)
            painter.setPen(QColor(200, 210, 220, 220) if is_system_dark() else QColor(90, 100, 120, 220))
            painter.drawText(QRectF(0, cy + circle_d / 2 + 4, w, city_h), Qt.AlignmentFlag.AlignCenter, self._city)

    def mousePressEvent(self, event):
        parent = self.parent()
        if parent and hasattr(parent, 'show_weather_forecast'):
            parent.show_weather_forecast(event)


class HourlyForecastChart(QWidget):
    """24小时温度曲线图 - 贝塞尔平滑 + 温度梯度面积 + 当前时刻锚点 + 悬停 Tooltip"""
    def __init__(self, hourly_data, provider="qweather", current_index=0, parent=None):
        super().__init__(parent)
        self.hourly_data = hourly_data or []
        self.provider = provider
        self.current_index = max(0, min(current_index, len(self.hourly_data) - 1)) if self.hourly_data else 0
        self.setMinimumHeight(210)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self._hover_idx = -1
        self._pulse_phase = 0.0
        self._pts = []
        self._plot_geom = (0, 0, 0, 0)
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_tick)
        self._pulse_timer.start(60)

    def _pulse_tick(self):
        self._pulse_phase = (self._pulse_phase + 0.10) % (2 * math.pi)
        self.update()

    def _parse_temp(self, h):
        try:
            return float(h.get("temp", 0))
        except (TypeError, ValueError):
            return 0.0

    def _parse_time(self, h):
        t_str = h.get("time", "")
        if "T" in t_str:
            t_str = t_str.split("T")[-1]
        try:
            return t_str[:5]
        except Exception:
            return t_str

    def mouseMoveEvent(self, event):
        x = event.position().x()
        if not self._pts:
            return
        best_i, best_d = -1, 1e9
        for i, (px, py) in enumerate(self._pts):
            d = abs(px - x)
            if d < best_d:
                best_d = d
                best_i = i
        if best_i != self._hover_idx:
            self._hover_idx = best_i
            self.update()

    def leaveEvent(self, event):
        if self._hover_idx >= 0:
            self._hover_idx = -1
            self.update()

    def _temp_color(self, t, t_min, t_max):
        span = max(t_max - t_min, 1)
        r = (t - t_min) / span
        if r < 0.5:
            k = r / 0.5
            return QColor(int(79 + (255 - 79) * k * 0.4), int(195 - 195 * k * 0.5), int(247 - 247 * k * 0.4))
        else:
            k = (r - 0.5) / 0.5
            return QColor(int(180 + 75 * k), int(120 - 60 * k), int(150 - 120 * k))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        if w <= 10 or h <= 10 or len(self.hourly_data) < 2:
            painter.setPen(QColor(150, 150, 150))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "暂无足够数据绘制曲线图")
            return
        temps = [self._parse_temp(hd) for hd in self.hourly_data]
        t_min, t_max = min(temps), max(temps)
        if t_max - t_min < 1:
            t_max = t_min + 1
        pad_l, pad_r, pad_t, pad_b = 36, 36, 36, 42
        plot_w = w - pad_l - pad_r
        plot_h = h - pad_t - pad_b
        n = len(temps)
        step_x = plot_w / (n - 1) if n > 1 else plot_w
        pts = []
        for i, t in enumerate(temps):
            x = pad_l + i * step_x
            y = pad_t + plot_h - (t - t_min) / (t_max - t_min) * plot_h
            pts.append((x, y))
        self._pts = pts
        self._plot_geom = (pad_l, pad_t, plot_w, plot_h)

        line_path = QPainterPath()
        line_path.moveTo(pts[0][0], pts[0][1])
        for i in range(1, len(pts)):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            cx = (x0 + x1) / 2
            line_path.cubicTo(cx, y0, cx, y1, x1, y1)

        fill_path = QPainterPath()
        fill_path.moveTo(pts[0][0], pad_t + plot_h)
        fill_path.lineTo(pts[0][0], pts[0][1])
        for i in range(1, len(pts)):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            cx = (x0 + x1) / 2
            fill_path.cubicTo(cx, y0, cx, y1, x1, y1)
        fill_path.lineTo(pts[-1][0], pad_t + plot_h)
        fill_path.closeSubpath()

        grad = QLinearGradient(0, pad_t, 0, pad_t + plot_h)
        grad.setColorAt(0.0, QColor(255, 167, 38, 130))
        grad.setColorAt(0.5, QColor(126, 87, 194, 90))
        grad.setColorAt(1.0, QColor(79, 195, 247, 0))
        painter.fillPath(fill_path, QBrush(grad))

        pen = QPen(QColor(180, 220, 255), 2.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(line_path)

        label_step = max(1, n // 8)
        mono_font = QFont("Consolas")
        mono_font.setPointSize(8)
        label_font = QFont("Microsoft YaHei")
        label_font.setPointSize(8)
        for i, (x, y) in enumerate(pts):
            is_cur = (i == self.current_index)
            is_hover = (i == self._hover_idx)
            if is_cur:
                pulse = 0.5 + 0.5 * math.sin(self._pulse_phase)
                halo_r = 7 + 4 * pulse
                for ring in range(3):
                    a = int(120 * (1 - ring / 3.0) * (0.6 + 0.4 * pulse))
                    painter.setBrush(QColor(255, 235, 120, a))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(QPointF(x, y), halo_r + ring * 3, halo_r + ring * 3)
                painter.setBrush(QColor(255, 245, 180))
                painter.setPen(QPen(QColor(255, 200, 80), 1.5))
                painter.drawEllipse(QPointF(x, y), 5, 5)
            elif is_hover:
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(180, 220, 255), 1.5))
                painter.drawEllipse(QPointF(x, y), 5, 5)
            else:
                painter.setBrush(self._temp_color(temps[i], t_min, t_max))
                painter.setPen(QPen(QColor(255, 255, 255, 180), 1))
                painter.drawEllipse(QPointF(x, y), 3, 3)
            if i % label_step == 0 or i == n - 1 or is_cur:
                painter.setPen(QColor(255, 255, 255) if is_cur else QColor(220, 230, 240))
                label_font.setBold(is_cur)
                painter.setFont(label_font)
                temp_str = f"{int(round(temps[i]))}°"
                painter.drawText(QRectF(x - 22, y - 24, 44, 16), Qt.AlignmentFlag.AlignCenter, temp_str)
                label_font.setBold(False)
                painter.setPen(QColor(150, 165, 185) if is_cur else QColor(130, 145, 165))
                painter.setFont(mono_font)
                t_label = self._parse_time(self.hourly_data[i])
                painter.drawText(QRectF(x - 28, pad_t + plot_h + 8, 56, 14), Qt.AlignmentFlag.AlignCenter, t_label)

        if 0 <= self.current_index < len(pts):
            cx, _ = pts[self.current_index]
            dash_pen = QPen(QColor(255, 235, 120, 140), 1.2, Qt.PenStyle.DashLine)
            painter.setPen(dash_pen)
            painter.drawLine(QPointF(cx, pad_t - 4), QPointF(cx, pad_t + plot_h + 4))
            cur_tag = "此刻"
            painter.setPen(QColor(255, 235, 120))
            tag_font = QFont("Microsoft YaHei")
            tag_font.setPointSize(7)
            tag_font.setBold(True)
            painter.setFont(tag_font)
            painter.drawText(QRectF(cx - 20, pad_t - 18, 40, 14), Qt.AlignmentFlag.AlignCenter, cur_tag)

        if 0 <= self._hover_idx < len(self.hourly_data):
            hi = self._hover_idx
            hx, hy = pts[hi]
            tip_w, tip_h = 130, 56
            tip_x = max(4, min(hx - tip_w / 2, w - tip_w - 4))
            tip_y = max(4, hy - tip_h - 14)
            tip_rect = QRectF(tip_x, tip_y, tip_w, tip_h)
            painter.setBrush(QColor(20, 28, 42, 230))
            painter.setPen(QPen(QColor(120, 180, 240), 1))
            painter.drawRoundedRect(tip_rect, 8, 8)
            hd = self.hourly_data[hi]
            t_label = self._parse_time(hd)
            temp_v = hd.get("temp", "?")
            text_v = hd.get("text", "") or WEATHER_CODE_MAP.get(hd.get("code", 0), "")
            pop_v = hd.get("pop", "")
            tip_font = QFont("Microsoft YaHei")
            tip_font.setPointSize(9)
            painter.setFont(tip_font)
            painter.setPen(QColor(180, 200, 220))
            painter.drawText(QRectF(tip_x + 8, tip_y + 5, tip_w - 16, 14), Qt.AlignmentFlag.AlignLeft, f"🕐 {t_label}")
            painter.setPen(QColor(255, 255, 255))
            tip_font.setBold(True)
            painter.setFont(tip_font)
            painter.drawText(QRectF(tip_x + 8, tip_y + 20, tip_w - 16, 14), Qt.AlignmentFlag.AlignLeft, f"{text_v}  {temp_v}°C")
            tip_font.setBold(False)
            painter.setFont(tip_font)
            painter.setPen(QColor(140, 200, 240) if pop_v else QColor(150, 165, 185))
            pop_str = f"🌧️ 降水 {pop_v}%" if pop_v else "无降水数据"
            painter.drawText(QRectF(tip_x + 8, tip_y + 35, tip_w - 16, 14), Qt.AlignmentFlag.AlignLeft, pop_str)
            painter.setPen(QPen(QColor(180, 220, 255, 180), 1, Qt.PenStyle.DashLine))
            painter.drawLine(QPointF(hx, tip_y + tip_h), QPointF(hx, hy))


class WeatherForecastDialog(QDialog):
    def __init__(self, lat, lon, city_name, parent=None, provider="qweather", qw_key="", qw_host="", detailed_address=""):
        super().__init__(parent)
        self.setWindowTitle(f"📅 {city_name} 天气预报")
        self.resize(620, 740)
        self.lat = lat
        self.lon = lon
        self.city = city_name
        self.detailed_address = detailed_address or city_name
        self.provider = provider
        self.qw_key = qw_key
        self.qw_host = qw_host
        self.hourly_data = []
        self.daily_data = []
        self.current_data = {}
        self.sunrise = ""
        self.sunset = ""
        self._current_hour_idx = 0
        self._weather_text = ""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.label_title = QLabel("正在加载...")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: rgba(255,255,255,230); padding: 10px; background: transparent;")
        layout.addWidget(self.label_title)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background: transparent; border: none; } QScrollBar:vertical { background: rgba(255,255,255,20); width: 8px; border-radius: 4px; } QScrollBar::handle:vertical { background: rgba(255,255,255,90); border-radius: 4px; min-height: 30px; } QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }")
        self.content = QWidget()
        self.content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(14, 6, 14, 14)
        self.content_layout.setSpacing(10)
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)
        self.load_forecast()

    def _weather_palette(self):
        """根据天气文字返回背景渐变颜色三元组 (top, mid, bottom)"""
        t = self._weather_text or ""
        is_day, _ = self._day_phase()
        if "雷" in t:
            return (QColor(28, 18, 48), QColor(45, 28, 70), QColor(60, 35, 90))
        if "雪" in t:
            return (QColor(70, 90, 120) if is_day else QColor(40, 50, 80), QColor(120, 140, 170), QColor(180, 195, 215))
        if "大雨" in t or "暴雨" in t or "大阵雨" in t:
            return (QColor(25, 35, 55), QColor(40, 55, 80), QColor(55, 70, 95))
        if "雨" in t or "阵雨" in t or "毛毛雨" in t:
            return (QColor(40, 55, 80) if is_day else QColor(20, 30, 55), QColor(60, 80, 110), QColor(85, 105, 135))
        if "雾" in t or "霾" in t:
            return (QColor(85, 90, 100), QColor(120, 125, 135), QColor(155, 160, 170))
        if "阴" in t:
            return (QColor(55, 65, 80) if is_day else QColor(25, 30, 45), QColor(80, 90, 105), QColor(110, 120, 135))
        if "晴" in t:
            if is_day:
                return (QColor(48, 102, 168), QColor(82, 134, 184), QColor(214, 142, 88))
            return (QColor(8, 12, 36), QColor(20, 18, 52), QColor(40, 24, 70))
        if "多云" in t:
            if is_day:
                return (QColor(60, 95, 145), QColor(110, 140, 175), QColor(180, 165, 140))
            return (QColor(15, 20, 42), QColor(30, 30, 60), QColor(50, 35, 75))
        if is_day:
            return (QColor(48, 102, 168), QColor(82, 134, 184), QColor(214, 142, 88))
        return (QColor(8, 12, 36), QColor(20, 18, 52), QColor(40, 24, 70))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_day, day_progress = self._day_phase()
        w, h = self.width(), self.height()
        c_top, c_mid, c_bot = self._weather_palette()
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, c_top)
        grad.setColorAt(0.55, c_mid)
        grad.setColorAt(1.0, c_bot)
        painter.fillRect(self.rect(), grad)
        if not is_day:
            painter.setPen(Qt.PenStyle.NoPen)
            rng = random.Random(42)
            star_count = 90
            t = self._weather_text or ""
            if any(k in t for k in ["雨", "雪", "雾", "霾", "阴"]):
                star_count = 20
            for _ in range(star_count):
                sx = rng.random() * w
                sy = rng.random() * h * 0.6
                sa = rng.randint(60, 200)
                painter.setBrush(QColor(230, 240, 255, sa))
                painter.drawEllipse(QPointF(sx, sy), 1.2, 1.2)

    def _day_phase(self):
        now = datetime.now()
        sr = self._parse_hm(self.sunrise)
        ss = self._parse_hm(self.sunset)
        if sr is None or ss is None:
            sr, ss = (6, 0), (18, 0)
        now_min = now.hour * 60 + now.minute
        sr_min = sr[0] * 60 + sr[1]
        ss_min = ss[0] * 60 + ss[1]
        if sr_min <= now_min < ss_min:
            return True, (now_min - sr_min) / max(ss_min - sr_min, 1)
        return False, 0.0

    def _parse_hm(self, s):
        if not s:
            return None
        try:
            if "T" in s:
                s = s.split("T")[1]
            s = s.split("+")[0]
            parts = s.split(":")
            return (int(parts[0]), int(parts[1]))
        except Exception:
            return None

    def _qw_icon(self, code):
        if not code:
            return None
        icons_dir = os.path.join(resource_path("data"), "qweather_icons")
        try:
            os.makedirs(icons_dir, exist_ok=True)
        except Exception:
            return None
        local_path = os.path.join(icons_dir, f"{code}.svg")
        if not os.path.exists(local_path):
            try:
                resp = requests.get(f"https://cdn.jsdelivr.net/npm/qweather-icons@1.8.0/icons/{code}.svg", timeout=6)
                if resp.status_code == 200 and resp.content:
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                else:
                    return None
            except Exception:
                return None
        return local_path

    def _icon_label(self, code, size=28):
        lbl = QLabel()
        path = self._qw_icon(code)
        if path:
            lbl.setText(f'<img src="file:///{path.replace(chr(92), "/")}" width="{size}" height="{size}">')
            lbl.setTextFormat(Qt.TextFormat.RichText)
        return lbl

    def _hour_icon_code(self, h, idx):
        if self.provider == "qweather":
            now = datetime.now()
            t_str = h.get("time", "")
            try:
                if "T" in t_str:
                    th = int(t_str.split("T")[1][:2])
                else:
                    th = int(t_str[:2])
            except Exception:
                th = now.hour
            sr = self._parse_hm(self.sunrise)
            ss = self._parse_hm(self.sunset)
            sr_h = sr[0] if sr else 6
            ss_h = ss[0] if ss else 18
            is_day = sr_h <= th < ss_h
            return h.get("icon", "") if is_day else (h.get("icon", "") or h.get("iconNight", ""))
        return None

    def _glass_panel(self, bg_alpha=120, border_alpha=60):
        w = QWidget()
        w.setStyleSheet(f"background: rgba(20, 28, 48, {bg_alpha}); border-radius: 14px; border: 1px solid rgba(255,255,255,{border_alpha});")
        return w

    def load_forecast(self):
        def fetch():
            try:
                self._fetch_qweather_forecast()
                QTimer.singleShot(0, self.update_ui)
            except Exception as e:
                debug_print(f"预报加载失败: {e}")
                QTimer.singleShot(0, lambda: self.label_title.setText("加载失败"))
        threading.Thread(target=fetch, daemon=True).start()

    def _fetch_qweather_forecast(self):
        key = self.qw_key
        host = (self.qw_host or "").strip().rstrip("/")
        if host and not host.startswith("http"):
            host = "https://" + host
        elif not host:
            host = "https://" + WeatherFetcher.QWEATHER_DEFAULT_HOST
        coord = f"{self.lon:.2f},{self.lat:.2f}"
        headers = {"User-Agent": "CountdownDesktop/1.0"}
        now_resp = requests.get(f"{host}/v7/weather/now", params={"location": coord, "key": key, "lang": "zh"}, timeout=10, headers=headers)
        now_data = now_resp.json()
        if str(now_data.get("code", "")) == "200" and now_data.get("now"):
            n = now_data["now"]
            self.current_data = {
                "temp": n.get("temp", "?"),
                "feelsLike": n.get("feelsLike", ""),
                "text": n.get("text", ""),
                "icon": n.get("icon", ""),
                "wind": f"{n.get('windDir', '')} {n.get('windScale', '')}级",
                "humidity": n.get("humidity", ""),
                "obsTime": n.get("obsTime", ""),
            }
        h_resp = requests.get(f"{host}/v7/weather/24h", params={"location": coord, "key": key, "lang": "zh"}, timeout=10, headers=headers)
        h_data = h_resp.json()
        if str(h_data.get("code", "")) == "200" and h_data.get("hourly"):
            self.hourly_data = []
            for h in h_data["hourly"][:24]:
                self.hourly_data.append({
                    "time": h.get("fxTime", "")[:16],
                    "temp": h.get("temp", "?"),
                    "text": h.get("text", ""),
                    "icon": h.get("icon", ""),
                    "wind": f"{h.get('windDir', '')} {h.get('windScale', '')}级",
                    "pop": h.get("pop", ""),
                    "humidity": h.get("humidity", ""),
                    "precip": h.get("precip", ""),
                })
        d_resp = requests.get(f"{host}/v7/weather/7d", params={"location": coord, "key": key, "lang": "zh"}, timeout=10, headers=headers)
        d_data = d_resp.json()
        if str(d_data.get("code", "")) == "200" and d_data.get("daily"):
            self.daily_data = []
            for d in d_data["daily"]:
                self.daily_data.append({
                    "date": d.get("fxDate", ""),
                    "max": d.get("tempMax", "?"),
                    "min": d.get("tempMin", "?"),
                    "text_day": d.get("textDay", ""),
                    "icon_day": d.get("iconDay", ""),
                    "text_night": d.get("textNight", ""),
                    "icon_night": d.get("iconNight", ""),
                    "sr": d.get("sunrise", ""),
                    "ss": d.get("sunset", ""),
                })
            if self.daily_data:
                self.sunrise = self.daily_data[0].get("sr", "")
                self.sunset = self.daily_data[0].get("ss", "")
        self._current_hour_idx = self._calc_current_hour_idx()

    def _calc_current_hour_idx(self):
        if not self.hourly_data:
            return 0
        now = datetime.now()
        best_i, best_d = 0, 1e18
        for i, h in enumerate(self.hourly_data):
            t_str = h.get("time", "")
            try:
                if "T" in t_str:
                    dt = datetime.fromisoformat(t_str.split("+")[0])
                else:
                    continue
            except Exception:
                continue
            d = abs((dt - now).total_seconds())
            if d < best_d:
                best_d = d
                best_i = i
        return best_i

    def update_ui(self):
        if not self.daily_data and not self.hourly_data and not self.current_data:
            self.label_title.setText("无数据")
            return
        self.label_title.setText(f"{self.city} 天气预报")
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._weather_text = self.current_data.get("text", "") or ""
        is_day, _ = self._day_phase()
        self._build_current_card(is_day)
        if self.hourly_data:
            self._build_hourly_section(is_day)
        if self.daily_data:
            self._build_daily_section(is_day)
        self.content_layout.addStretch()
        self.update()

    def _build_current_card(self, is_day):
        if not self.current_data:
            return
        card = self._glass_panel(150 if is_day else 110, 80)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(18, 14, 18, 14)
        cl.setSpacing(4)
        loc_row = QHBoxLayout()
        addr_text = self.detailed_address or self.city
        loc_lbl = QLabel(f"📍 {addr_text}")
        loc_lbl.setStyleSheet("color: rgba(255,255,255,210); font-size: 10pt; background: transparent; border: none;")
        loc_lbl.setWordWrap(True)
        loc_row.addWidget(loc_lbl, 1)
        loc_row.addStretch()
        obs = self.current_data.get("obsTime", "")
        obs_short = ""
        if obs and "T" in obs:
            try:
                obs_short = obs.split("T")[1][:5]
            except Exception:
                obs_short = ""
        if obs_short:
            time_lbl = QLabel(f"🕐 {obs_short} 更新")
            time_lbl.setStyleSheet("color: rgba(255,255,255,160); font-size: 9pt; background: transparent; border: none;")
            loc_row.addWidget(time_lbl)
        cl.addLayout(loc_row)
        main_row = QHBoxLayout()
        main_row.setSpacing(14)
        if self.provider == "qweather" and self.current_data.get("icon"):
            icon_lbl = self._icon_label(self.current_data["icon"], 64)
            icon_lbl.setStyleSheet("background: transparent; border: none;")
            main_row.addWidget(icon_lbl)
        temp_v = self.current_data.get("temp", "?")
        try:
            temp_int = int(round(float(temp_v)))
        except Exception:
            temp_int = temp_v
        temp_lbl = QLabel(f"{temp_int}°")
        temp_lbl.setStyleSheet("color: white; font-size: 42pt; font-weight: bold; background: transparent; border: none;")
        main_row.addWidget(temp_lbl)
        info_col = QVBoxLayout()
        info_col.setSpacing(2)
        text_lbl = QLabel(self.current_data.get("text", ""))
        text_lbl.setStyleSheet("color: white; font-size: 13pt; font-weight: bold; background: transparent; border: none;")
        info_col.addWidget(text_lbl)
        fl = self.current_data.get("feelsLike", "")
        hum = self.current_data.get("humidity", "")
        wind = self.current_data.get("wind", "")
        detail_parts = []
        if fl:
            detail_parts.append(f"体感 {fl}°")
        if hum:
            detail_parts.append(f"湿度 {hum}%")
        if wind:
            detail_parts.append(wind)
        if detail_parts:
            det_lbl = QLabel(" · ".join(detail_parts))
            det_lbl.setStyleSheet("color: rgba(255,255,255,180); font-size: 9pt; background: transparent; border: none;")
            info_col.addWidget(det_lbl)
        info_col.addStretch()
        main_row.addLayout(info_col)
        main_row.addStretch()
        cl.addLayout(main_row)
        sr = self._parse_hm(self.sunrise)
        ss = self._parse_hm(self.sunset)
        if sr and ss:
            sr_str = f"{sr[0]:02d}:{sr[1]:02d}"
            ss_str = f"{ss[0]:02d}:{ss[1]:02d}"
            sun_row = QHBoxLayout()
            sun_lbl = QLabel(f"🌅 日出 {sr_str}    🌇 日落 {ss_str}")
            sun_lbl.setStyleSheet("color: rgba(255,235,150,200); font-size: 9pt; background: transparent; border: none;")
            sun_row.addWidget(sun_lbl)
            sun_row.addStretch()
            cl.addLayout(sun_row)
        self.content_layout.addWidget(card)

    def _build_hourly_section(self, is_day):
        h_title = QLabel("🕐 未来24小时温度趋势")
        h_title.setStyleSheet(f"font-size: 11pt; font-weight: bold; color: {'rgba(255,255,255,230)' if is_day else '#4FC3F7'}; padding: 6px 2px; background: transparent;")
        self.content_layout.addWidget(h_title)
        chart_card = self._glass_panel(100, 50)
        cl = QVBoxLayout(chart_card)
        cl.setContentsMargins(8, 8, 8, 8)
        chart = HourlyForecastChart(self.hourly_data, self.provider, self._current_hour_idx, chart_card)
        cl.addWidget(chart)
        self.content_layout.addWidget(chart_card)
        hint = QLabel("💡 鼠标悬停曲线查看详情，黄色光点为当前时刻")
        hint.setStyleSheet("color: rgba(255,255,255,140); font-size: 8pt; padding: 2px 6px; background: transparent;")
        self.content_layout.addWidget(hint)
        list_card = self._glass_panel(90, 40)
        ll = QVBoxLayout(list_card)
        ll.setContentsMargins(10, 8, 10, 8)
        ll.setSpacing(2)
        header_row = self._make_grid_row("时间", "天气", "温度", "体感", "降水", is_header=True)
        ll.addLayout(header_row)
        for i, h in enumerate(self.hourly_data):
            is_cur = (i == self._current_hour_idx)
            t_str = h.get("time", "")
            t_short = t_str.split("T")[-1][:5] if "T" in t_str else t_str[-5:]
            if self.provider == "qweather":
                text_v = h.get("text", "")
            else:
                text_v = WEATHER_CODE_MAP.get(h.get("code", 0), "")
            temp_v = h.get("temp", "?")
            try:
                temp_int = int(round(float(temp_v)))
                temp_disp = f"{temp_int}°C"
            except Exception:
                temp_disp = f"{temp_v}°C"
            fl_v = h.get("feelsLike", "")
            try:
                fl_disp = f"{int(round(float(fl_v)))}°" if fl_v != "" else "—"
            except Exception:
                fl_disp = str(fl_v) if fl_v != "" else "—"
            pop_v = h.get("pop", "")
            pop_disp = f"🌧️ {pop_v}%" if pop_v else "—"
            row = self._make_grid_row(t_short, text_v, temp_disp, fl_disp, pop_disp, is_current=is_cur, idx=i, h=h)
            ll.addLayout(row)
        self.content_layout.addWidget(list_card)

    def _make_grid_row(self, t, text, temp, feel, pop, is_header=False, is_current=False, idx=-1, h=None):
        row = QHBoxLayout()
        row.setSpacing(6)
        if is_header:
            lbl_color = "rgba(255,255,255,150)"
            lbl_font = "font-size: 9pt; font-weight: bold;"
            bg = "transparent"
        elif is_current:
            lbl_color = "rgba(255,235,120,255)"
            lbl_font = "font-size: 10pt; font-weight: bold;"
            bg = "rgba(255,235,120,40)"
        else:
            lbl_color = "rgba(255,255,255,220)"
            lbl_font = "font-size: 9pt;"
            bg = "transparent"

        def cell(text, w, mono=False, color=None, bold=False):
            l = QLabel(text)
            family = "Consolas" if mono else "Microsoft YaHei"
            l.setStyleSheet(f"color: {color or lbl_color}; {lbl_font} background: {bg}; border: none; font-family: '{family}';")
            l.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            l.setMinimumWidth(w)
            l.setMaximumWidth(w)
            return l

        def icon_cell(code, size=20):
            l = QLabel()
            l.setFixedSize(28, 28)
            if code:
                path = self._qw_icon(code)
                if path:
                    l.setText(f'<img src="file:///{path.replace(chr(92), "/")}" width="{size}" height="{size}">')
                    l.setTextFormat(Qt.TextFormat.RichText)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.setStyleSheet(f"background: {bg}; border: none;")
            return l

        row.addStretch(1)
        row.addWidget(cell(t, 60, mono=True))
        row.addStretch(1)
        if is_header:
            row.addWidget(cell(text, 128))
        else:
            if h is not None and self.provider == "qweather":
                icon_code = self._hour_icon_code(h, idx)
                row.addWidget(icon_cell(icon_code, 22 if is_current else 20))
            text_lbl = QLabel(text)
            text_lbl.setStyleSheet(f"color: {lbl_color}; {lbl_font} background: {bg}; border: none; font-family: 'Microsoft YaHei';")
            text_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            text_lbl.setMinimumWidth(100)
            text_lbl.setMaximumWidth(100)
            row.addWidget(text_lbl)
        row.addStretch(1)
        row.addWidget(cell(temp, 60, bold=is_current))
        row.addStretch(1)
        feel_color = "rgba(255,200,140,220)" if (not is_header and feel != "—" and feel != "") else lbl_color
        row.addWidget(cell(feel, 60, color=feel_color))
        row.addStretch(1)
        pop_color = "rgba(140,200,240,255)" if (not is_header and pop != "—") else lbl_color
        row.addWidget(cell(pop, 70, color=pop_color))
        row.addStretch(1)
        return row

    def _build_daily_section(self, is_day):
        d_title = QLabel("📅 未来7天")
        d_title.setStyleSheet(f"font-size: 11pt; font-weight: bold; color: {'rgba(255,255,255,230)' if is_day else '#81C784'}; padding: 8px 2px 4px; background: transparent;")
        self.content_layout.addWidget(d_title)
        list_card = self._glass_panel(90, 40)
        ll = QVBoxLayout(list_card)
        ll.setContentsMargins(10, 8, 10, 8)
        ll.setSpacing(2)
        for i, d in enumerate(self.daily_data):
            row = QHBoxLayout()
            row.setSpacing(8)
            date_str = d.get("date", "")
            try:
                dt = datetime.fromisoformat(date_str)
                date_disp = dt.strftime("%m-%d")
                weekday = ["一", "二", "三", "四", "五", "六", "日"][dt.weekday()]
                date_disp = f"{date_disp} 周{weekday}"
            except Exception:
                date_disp = date_str
            if i == 0:
                date_disp = "今天 " + date_disp
                date_color = "rgba(255,235,120,255)"
            else:
                date_color = "rgba(255,255,255,220)"
            date_lbl = QLabel(date_disp)
            date_lbl.setStyleSheet(f"color: {date_color}; font-size: 9pt; font-weight: {'bold' if i == 0 else 'normal'}; background: transparent; border: none; font-family: 'Microsoft YaHei';")
            date_lbl.setMinimumWidth(110)
            date_lbl.setMaximumWidth(110)
            row.addWidget(date_lbl)
            if self.provider == "qweather":
                row.addWidget(self._icon_label(d.get("icon_day", ""), 26))
                text_lbl = QLabel(d.get("text_day", ""))
            else:
                text_lbl = QLabel(WEATHER_CODE_MAP.get(d.get("code", 0), "未知"))
            text_lbl.setStyleSheet("color: rgba(255,255,255,220); font-size: 9pt; background: transparent; border: none; font-family: 'Microsoft YaHei';")
            text_lbl.setMinimumWidth(80)
            row.addWidget(text_lbl)
            row.addStretch()
            temp_lbl = QLabel(f"🌡 {d.get('min', '?')}° ~ {d.get('max', '?')}°")
            temp_lbl.setStyleSheet("color: rgba(255,200,140,220); font-size: 9pt; background: transparent; border: none; font-family: 'Consolas';")
            row.addWidget(temp_lbl)
            ll.addLayout(row)
        self.content_layout.addWidget(list_card)

class WeatherFetcher(QObject):
    weather_updated = pyqtSignal(str)
    QWEATHER_DEFAULT_KEY = "09c8e836cf904b5dbcf716f1f769de04"
    QWEATHER_DEFAULT_HOST = "k969396drm.re.qweatherapi.com"

    def __init__(self, parent=None, api_provider="qweather", custom_url_template="", qweather_api_key="", qweather_api_host=""):
        super().__init__(parent)
        self.lat = None
        self.lon = None
        self.city_name = ""
        self.detailed_address = ""
        self.api_provider = api_provider
        self.custom_url_template = custom_url_template
        self.qweather_api_key = qweather_api_key
        self.qweather_api_host = qweather_api_host

    def fetch(self, city_name=""):
        def run():
            headers = {"User-Agent": "CountdownDesktop/1.0"}
            try:
                if self.api_provider == "custom" and self.custom_url_template:
                    self._fetch_custom(headers, city_name)
                else:
                    self._fetch_qweather(headers, city_name)
            except Exception as e:
                debug_print(f"天气获取失败: {e}")
                self.weather_updated.emit("🌤️ 天气离线")

        threading.Thread(target=run, daemon=True).start()

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

    def _pick_cn_name(self, loc, fallback=""):
        """从和风 GeoAPI 的 location 对象中提取中文名称和详细地址。
        name 字段在某些城市会返回拼音（如 Anning），优先用 adm2/adm1 等中文字段。"""
        name = loc.get("name", "") or fallback
        adm1 = loc.get("adm1", "") or ""
        adm2 = loc.get("adm2", "") or ""
        country = loc.get("country", "") or ""
        def is_ascii(s):
            try:
                return all(ord(c) < 128 for c in s if c.strip())
            except Exception:
                return False
        if is_ascii(name):
            for candidate in [adm2, adm1]:
                if candidate and not is_ascii(candidate):
                    name = candidate
                    break
        parts = [p for p in [country, adm1, adm2, name] if p]
        detail = " ".join(parts) if parts else name
        return name, detail

    def _weather_emoji(self, text):
        if not text:
            return "🌤️"
        t = text
        if "雷" in t:
            return "⛈️"
        if "雪" in t:
            return "❄️"
        if "雨" in t or "阵雨" in t or "毛毛雨" in t:
            return "🌧️"
        if "雾" in t or "霾" in t:
            return "🌫️"
        if "阴" in t:
            return "☁️"
        if "晴" in t:
            return "☀️"
        if "多云" in t:
            return "⛅"
        return "🌤️"

    def _qweather_icon_path(self, code):
        if not code:
            return None
        icons_dir = os.path.join(resource_path("data"), "qweather_icons")
        try:
            os.makedirs(icons_dir, exist_ok=True)
        except Exception:
            return None
        local_path = os.path.join(icons_dir, f"{code}.svg")
        if not os.path.exists(local_path):
            try:
                url = f"https://cdn.jsdelivr.net/npm/qweather-icons@1.8.0/icons/{code}.svg"
                resp = requests.get(url, timeout=6)
                if resp.status_code == 200 and resp.content:
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                else:
                    return None
            except Exception as e:
                debug_print(f"和风天气图标下载失败({code}): {e}")
                return None
        return local_path

    def _fetch_qweather(self, headers, city_name):
        try:
            key = (self.qweather_api_key or "").strip() or self.QWEATHER_DEFAULT_KEY
            host = ((self.qweather_api_host or "").strip() or self.QWEATHER_DEFAULT_HOST).rstrip("/")
            if host:
                if not host.startswith("http"):
                    host = "https://" + host
                wx_base = f"{host}/v7"
                aq_base = f"{host}/airquality/v1"
                geo_base = f"{host}/geo/v2/city/lookup"
            else:
                wx_base = "https://devapi.qweather.com/v7"
                aq_base = "https://devapi.qweather.com/airquality/v1"
                geo_base = "https://geoapi.qweather.com/v2/city/lookup"

            lat, lon, name = None, None, ""
            detail_addr = ""
            city = city_name if city_name else ""
            if city:
                try:
                    geo_params = {"location": city, "key": key, "lang": "zh"}
                    geo_resp = requests.get(geo_base, params=geo_params, timeout=6, headers=headers)
                    geo_data = geo_resp.json()
                    if str(geo_data.get("code", "")) == "200" and geo_data.get("location"):
                        loc = geo_data["location"][0]
                        lat, lon = float(loc["lat"]), float(loc["lon"])
                        name, detail_addr = self._pick_cn_name(loc, city)
                except Exception as e:
                    debug_print(f"和风地理编码失败: {e}")
            if lat is None:
                try:
                    geo_params = {"location": "ip", "key": key, "lang": "zh"}
                    geo_resp = requests.get(geo_base, params=geo_params, timeout=6, headers=headers)
                    geo_data = geo_resp.json()
                    if str(geo_data.get("code", "")) == "200" and geo_data.get("location"):
                        loc = geo_data["location"][0]
                        lat, lon = float(loc["lat"]), float(loc["lon"])
                        name, detail_addr = self._pick_cn_name(loc, "本地")
                        debug_print(f"和风 GeoAPI IP 定位: {name} / {detail_addr}")
                except Exception as e:
                    debug_print(f"和风 GeoAPI IP 定位失败: {e}")
            if lat is None:
                try:
                    ip_resp = requests.get("http://ip-api.com/json/?lang=zh-CN", timeout=5, headers=headers)
                    ip_data = ip_resp.json()
                    if ip_data.get("status") == "success":
                        lat, lon = ip_data["lat"], ip_data["lon"]
                        name = ip_data.get("city", "本地")
                        region = ip_data.get("regionName", "")
                        country = ip_data.get("country", "")
                        parts = [p for p in [country, region, name] if p]
                        detail_addr = " ".join(parts)
                    else:
                        raise Exception("IP定位失败")
                except Exception as e:
                    debug_print(f"IP定位失败: {e}")
            if lat is None:
                self.weather_updated.emit("🌤️ 定位失败")
                return
            self.lat, self.lon, self.city_name = lat, lon, name
            self.detailed_address = detail_addr or name
            coord = f"{lon:.2f},{lat:.2f}"

            now_url = f"{wx_base}/weather/now"
            now_resp = requests.get(now_url, params={"location": coord, "key": key, "lang": "zh"}, timeout=6, headers=headers)
            now_data = now_resp.json()
            if str(now_data.get("code", "")) != "200" or not now_data.get("now"):
                raise Exception(f"天气API返回 {now_data.get('code')}")
            now = now_data["now"]
            temp = now.get("temp", "?")
            text = now.get("text", "未知")
            icon_code = now.get("icon", "")
            icon_path = self._qweather_icon_path(icon_code)
            obs_time = now.get("obsTime", "")
            time_label = ""
            if obs_time and "T" in obs_time:
                try:
                    time_label = obs_time.split("T")[1][:5]
                except Exception:
                    time_label = ""

            main_text = f"{name} {time_label} {text} {temp}°C" if time_label else f"{name} {text} {temp}°C"
            parts = [main_text]

            try:
                aq_url = f"{aq_base}/{lat:.2f}/{lon:.2f}"
                aq_resp = requests.get(aq_url, params={"key": key}, timeout=6, headers=headers)
                if aq_resp.status_code == 200:
                    aq_data = aq_resp.json()
                    aq_now = aq_data.get("now") or {}
                    aqi_val = (aq_now.get("aqi") or {}).get("value") or aq_now.get("aqi")
                    cat = (aq_now.get("aqi") or {}).get("category") or aq_now.get("category")
                    if aqi_val:
                        parts.append(f"AQI {aqi_val} {cat or ''}".strip())
            except Exception as e:
                debug_print(f"和风空气质量获取失败: {e}")

            try:
                idx_url = f"{wx_base}/indices/1d"
                idx_resp = requests.get(idx_url, params={"location": coord, "key": key, "type": "0"}, timeout=6, headers=headers)
                idx_data = idx_resp.json()
                if str(idx_data.get("code", "")) == "200" and idx_data.get("daily"):
                    di = idx_data["daily"][0]
                    parts.append(f"穿衣 {di.get('category', '')}")
            except Exception as e:
                debug_print(f"和风生活指数获取失败: {e}")

            text_str = " · ".join(parts)
            if icon_path:
                display = f'<img src="file:///{icon_path.replace(chr(92), "/")}" width="24" height="24" style="vertical-align:middle;"> {text_str}'
                self.weather_updated.emit(display)
            else:
                emoji = self._weather_emoji(text)
                self.weather_updated.emit(f"{emoji} {text_str}")

        except requests.exceptions.Timeout:
            self.weather_updated.emit("🌤️ 天气超时")
        except Exception as e:
            debug_print(f"和风天气获取失败: {e}")
            self.weather_updated.emit("🌤️ 天气离线")

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
        self._app = app 

    def log(self, message, level="INFO"):
        self._plugin.log_plugin(message, level)

    def _plugin_name(self):
        return self._plugin.name if self._plugin and hasattr(self._plugin, 'name') else "unknown"

    def _validate_widget_class(self, id_name, widget_class, kind):
        if not (isinstance(widget_class, type) and issubclass(widget_class, QWidget)):
            msg = f"{kind}注册失败: 类未继承 QWidget (ID={id_name})"
            self._app.plugin_manager.report_register_error(self._plugin_name(), msg)
            raise TypeError(msg)

    def _check_duplicate_id(self, id_name, registry, kind):
        if id_name in registry:
            msg = f"{kind}注册失败: ID 重复 (ID={id_name})"
            self._app.plugin_manager.report_register_error(self._plugin_name(), msg)
            raise ValueError(msg)

    def register_dynamic_bg(self, id_name, display_name, widget_class, border_radius=None):
        self._validate_widget_class(id_name, widget_class, "动态背景")
        self._check_duplicate_id(id_name, self._app.dynamic_bg_registry, "动态背景")
        self._app.dynamic_bg_registry[id_name] = display_name
        self._app.dynamic_bg_classes[id_name] = {
            "class": widget_class,
            "border_radius": border_radius
        }
        self.log(f"成功注册动态背景: {display_name}")

    def update_dynamic_bg_radius(self, id_name, border_radius):
        entry = self._app.dynamic_bg_classes.get(id_name)
        if not entry:
            self.log(f"未找到动态背景: {id_name}", "WARNING")
            return False
        entry["border_radius"] = border_radius
        for win in getattr(self._app, 'windows', []):
            w = getattr(win, 'bg_dynamic_widget', None)
            if w is not None and getattr(w, '_bg_id', None) == id_name:
                if hasattr(w, 'set_radius'):
                    w.set_radius(border_radius if border_radius is not None else 0)
                elif hasattr(w, 'radius'):
                    w.radius = border_radius if border_radius is not None else 0
                    w.update()
        return True

    def register_settings_panel(self, id_name, display_name, widget_class):
        self._validate_widget_class(id_name, widget_class, "设置面板")
        if not hasattr(self._app, 'plugin_settings_panels'):
            self._app.plugin_settings_panels = {}
        self._check_duplicate_id(id_name, self._app.plugin_settings_panels, "设置面板")
        self._app.plugin_settings_panels[id_name] = {
            "name": display_name,
            "class": widget_class,
            "plugin": self._plugin_name()
        }
        self.log(f"成功注册设置面板: {display_name}")

    def register_widget(self, id_name, display_name, widget_class):
        self._validate_widget_class(id_name, widget_class, "自定义控件")
        if not hasattr(self._app, 'custom_widget_registry'):
            self._app.custom_widget_registry = {}
        self._check_duplicate_id(id_name, self._app.custom_widget_registry, "自定义控件")
        self._app.custom_widget_registry[id_name] = {
            "name": display_name,
            "class": widget_class
        }
        self.log(f"成功注册自定义控件: {display_name}")

    def register_settings_widget(self, id_name, display_name, widget_class):
        self._validate_widget_class(id_name, widget_class, "设置面板")
        if not hasattr(self._app, 'plugin_settings_panels'):
            self._app.plugin_settings_panels = {}
        self._check_duplicate_id(id_name, self._app.plugin_settings_panels, "设置面板")
        self._app.plugin_settings_panels[id_name] = {
            "name": display_name,
            "class": widget_class,
            "plugin": self._plugin_name()
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
        self.load_errors = []
        self.register_errors = []
        self._resource_strikes = {}
        self.load_security_config()
        if load_immediately:
            self.load_plugins()

    def report_register_error(self, plugin_name, message):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] [{plugin_name}] {message}"
        self.register_errors.append(entry)
        if len(self.register_errors) > 200:
            del self.register_errors[:-200]
        log_message(f"[插件] {entry}", "ERROR")
        try:
            self.app.update_plugin_log()
        except (RuntimeError, AttributeError):
            pass

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
        self.load_errors = []
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
                        if not isinstance(plugin_instance, Plugin):
                            msg = "setup() 未返回 Plugin 实例"
                            self.load_errors.append(f"{filename}: {msg}")
                            log_message(f"[插件] {filename} {msg}，跳过", "ERROR")
                            continue
                        plugin_instance.filename = filename
                        plugin_instance.api = PluginAPI(plugin_instance, self.app)
                        self.plugins.append(plugin_instance)
                        log_message(
                            f"[插件] {filename} 加载成功 (name={plugin_instance.name}, ver={plugin_instance.version})",
                            "INFO")
                    else:
                        msg = "缺少 setup() 函数"
                        self.load_errors.append(f"{filename}: {msg}")
                        log_message(f"[插件] {filename} {msg}，跳过", "WARNING")
                except Exception as e:
                    import traceback
                    tb = traceback.format_exc()
                    self.load_errors.append(f"{filename}: {type(e).__name__}: {e}")
                    log_message(f"[插件] {filename} 加载失败: {e}", "ERROR")
                    log_message(f"[插件] 完整堆栈:\n{tb}", "ERROR")
        sys.path.pop(0)
        self._audit_suppress = False
        self.save_security_config()

    def reload_plugins(self):
        states = {}
        if os.path.exists(self.app.config_path):
            try:
                with open(self.app.config_path, "r", encoding="utf-8") as f:
                    states = json.load(f).get("plugin_states", {})
            except Exception:
                states = {}
        for plugin in list(self.plugins):
            if plugin.enabled:
                try:
                    self.disable_plugin(plugin)
                except Exception:
                    pass
        self.load_plugins()
        for plugin in self.plugins:
            state = states.get(plugin.filename, {})
            if "permissions" in state:
                try:
                    plugin.permissions = PluginPermission(int(state["permissions"]))
                except Exception:
                    plugin.permissions = plugin.requested_permissions
            plugin.autostart = bool(state.get("autostart", state.get("enabled", False)))
            if plugin.autostart:
                self.enable_plugin(plugin, limited=state.get("limited", False), force=True)
        return self.load_errors

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
        limit_enabled = getattr(self.app, 'plugin_resource_limit', False)
        for plugin in self.get_enabled_plugins():
            if hasattr(plugin, event_name):
                start = time.perf_counter()
                try:
                    _plugin_context.current_plugin = plugin
                    getattr(plugin, event_name)(*args, **kwargs)
                except Exception as e:
                    plugin.log_plugin(f"执行事件 {event_name} 时出错: {e}", "ERROR")
                finally:
                    _plugin_context.current_plugin = None
                if limit_enabled:
                    elapsed = time.perf_counter() - start
                    if elapsed > 2.0:
                        strikes = self._resource_strikes.get(plugin.filename, 0) + 1
                        self._resource_strikes[plugin.filename] = strikes
                        plugin.log_plugin(
                            f"事件 {event_name} 耗时 {elapsed:.2f}s，超出资源限制 ({strikes}/3)", "WARNING")
                        if strikes >= 3:
                            plugin.limited = True
                            self.disable_plugin(plugin)
                            self._resource_strikes[plugin.filename] = 0
                            plugin.log_plugin("因多次超出资源限制，插件已被自动禁用", "ERROR")

    def get_plugin_risk(self, plugin):
        return getattr(plugin, '_risk_level', 0)

    def set_plugin_permissions(self, plugin, perms):
        plugin.permissions = perms
        self.save_security_config()
        self.app.save_config(force=True)

class Plugin:
    PLUGIN_SYSTEM_VERSION = "0.11"

    def __init__(self):
        self.name = "Unnamed Plugin"
        self.version = "0.1"
        self.author = "Unknown"
        self.description = ""
        self.enabled = False
        self.autostart = False
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
                 font_size=28, bg_color=None, font_color=None,
                 position=None, size=None,
                 screen_width=1920, screen_height=1080, always_on_top=True, auto_font=True,
                 background_type="gradient", background_image="", window_alpha=0.88,
                 project_type="normal", pomodoro_work=25, pomodoro_break=5, pomodoro_long_break=15,
                 pomodoro_cycles=4,
                 custom_layout=None, fullscreen_layout=None, window_round_radius=18,
                 use_neon=True, neon_start="#00f2fe", neon_end="#4facfe", neon_glow="#4facfe",
                 weather_city="",
                 gradient_start=None, gradient_end=None,
                 dynamic_bg_type="particles", dynamic_fps=30, dynamic_quality="high", graphics_preset="high",
                 typewriter_interval=15, tip_interval=15, expired_text="已到期",
                 display_format="decimal", display_format_template="{days}天 {hours}时 {minutes}分",
                 click_through=False, recur_weekdays=None, recur_end_date="",
                 enable_end_sound=True, end_sound_mode="windchime", custom_sound_path="",
                 fullscreen_layouts=None):
        self.project_type = project_type
        self.click_through = click_through
        self.recur_weekdays = recur_weekdays or []
        self.recur_end_date = recur_end_date
        self.enable_end_sound = enable_end_sound
        self.end_sound_mode = end_sound_mode
        self.custom_sound_path = custom_sound_path
        self.pomodoro_work = pomodoro_work
        self.pomodoro_break = pomodoro_break
        self.pomodoro_long_break = pomodoro_long_break
        self.pomodoro_cycles = pomodoro_cycles
        self.custom_layout = custom_layout or {}
        self.fullscreen_layout = fullscreen_layout or {}
        self.fullscreen_layouts = fullscreen_layouts or {}
        if not self.fullscreen_layouts and self.fullscreen_layout:
            self.fullscreen_layouts["default"] = self.fullscreen_layout
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
            gradient_start = "#0a0a1a" if is_system_dark() else "#f5f0e8"
        if gradient_end is None:
            gradient_end = "#1a1040" if is_system_dark() else "#e2ecf5"
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end
        self.dynamic_bg_type = dynamic_bg_type
        self.dynamic_fps = dynamic_fps
        self.dynamic_quality = dynamic_quality
        self.graphics_preset = graphics_preset
        self.name = name
        self.target_date = target_date or (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.target_time = target_time or "00:00"
        self.show_both = show_both
        self.font_size = font_size
        if bg_color is None:
            bg_color = "#0a0a1a" if is_system_dark() else "#f5f7fa"
        if font_color is None:
            font_color = "#c0c8f0" if is_system_dark() else "#2c3e50"
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
            "fullscreen_layout": self.fullscreen_layout,
            "fullscreen_layouts": self.fullscreen_layouts,
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
            "graphics_preset": self.graphics_preset,
            "typewriter_interval": self.typewriter_interval,
            "tip_interval": self.tip_interval,
            "expired_text": self.expired_text,
            "display_format": self.display_format,
            "display_format_template": self.display_format_template,
            "click_through": self.click_through,
            "recur_weekdays": self.recur_weekdays,
            "recur_end_date": self.recur_end_date,
            "enable_end_sound": self.enable_end_sound,
            "end_sound_mode": self.end_sound_mode,
            "custom_sound_path": self.custom_sound_path
        }

    @staticmethod
    def from_dict(data, screen_width=1920, screen_height=1080):
        return CountdownProject(
            data.get("name", "新项目"),
            data.get("target_date", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")),
            data.get("target_time", "00:00"),
            data.get("show_both", True),
            data.get("font_size", 28),
            data.get("bg_color", None),
            data.get("font_color", None),
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
            data.get("fullscreen_layout", {}),
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
            data.get("graphics_preset", "high"),
            data.get("typewriter_interval", 15),
            data.get("tip_interval", 15),
            data.get("expired_text", "已到期"),
            data.get("display_format", "decimal"),
            data.get("display_format_template", "{days}天 {hours}时 {minutes}分"),
            data.get("click_through", False),
            data.get("recur_weekdays", None),
            data.get("recur_end_date", ""),
            data.get("enable_end_sound", True),
            data.get("end_sound_mode", "windchime"),
            data.get("custom_sound_path", ""),
            data.get("fullscreen_layouts", None)
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
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self.update_frame)
        self.stars = []
        self.clouds = []
        self.particles = []
        self.ripples = []
        self._frame_costs = []
        self._auto_degrade = True
        self.init_particles()
        self.start_animation()

    def set_radius(self, radius):
        self.radius = max(0, int(radius))
        self.update()

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
            count = {'ultra': 200, 'high': 150, 'medium': 90, 'low': 50}.get(self.quality, 90)
            for _ in range(count):
                self.stars.append({
                    "x": random.randint(0, width), "y": random.randint(0, height),
                    "size": random.uniform(0.8, 2.5), "speed": random.uniform(0.1, 0.8),
                    "brightness": random.randint(80, 255), "dir": random.choice([-1, 1]),
                    "twinkle_speed": random.uniform(3, 10)
                })
        elif self.wallpaper_type == "clouds":
            count = {'ultra': 12, 'high': 8, 'medium': 5, 'low': 3}.get(self.quality, 5)
            for _ in range(count):
                self.clouds.append({
                    "x": random.randint(0, width), "y": random.randint(0, int(height * 0.5)),
                    "size": random.randint(120, 350), "speed": random.uniform(0.3, 1.5),
                    "alpha": random.randint(30, 80)
                })
        elif self.wallpaper_type == "particles":
            count = {'ultra': 90, 'high': 60, 'medium': 35, 'low': 20}.get(self.quality, 35)
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
        frame_start = time.perf_counter()
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
        if self._auto_degrade:
            cost = time.perf_counter() - frame_start
            self._frame_costs.append(cost)
            if len(self._frame_costs) >= 60:
                avg = sum(self._frame_costs) / len(self._frame_costs)
                self._frame_costs.clear()
                budget = 1.0 / max(self.fps, 1)
                if avg > budget * 0.8:
                    if self.quality == "high":
                        self.set_quality("medium")
                        log_message("动态壁纸检测到性能压力，画质已自动降为中", "INFO")
                    elif self.quality == "medium":
                        self.set_quality("low")
                        log_message("动态壁纸检测到性能压力，画质已自动降为低", "INFO")
                    elif self.fps > 30:
                        self.set_fps(30)
                        log_message("动态壁纸检测到性能压力，帧率已自动降为 30", "INFO")

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


class AuroraBackgroundWidget(QWidget):
    """3D透视极光背景 - 多层体积光幕 + 透视投影 + 远山剪影"""
    def __init__(self, parent=None, radius=0):
        super().__init__(parent)
        self.radius = radius
        self.fps = 30
        self.quality = "high"
        self._t = 0.0
        self._stars = []
        self._mountains = []
        self._cache = None
        self._frame_costs = []
        self._auto_degrade = True
        self._target_fps = 30
        self._degraded = False
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self._tick)
        self._init_stars()
        self._init_mountains()
        self.set_fps(30)

    def set_radius(self, radius):
        self.radius = max(0, int(radius))
        self.update()

    def set_fps(self, fps):
        self._target_fps = max(15, int(fps))
        if not self._degraded:
            self.fps = self._target_fps
        self.timer.start(1000 // max(self.fps, 15))

    def set_quality(self, quality):
        self.quality = quality
        self._cache = None
        self._init_stars()
        self._frame_costs.clear()
        self._degraded = False

    def _scale_factor(self):
        if self.quality == "high":
            return 3
        if self.quality == "medium":
            return 4
        return 6

    def _init_stars(self):
        count = 160 if self.quality == "high" else (90 if self.quality == "medium" else 50)
        self._stars = [{
            "x": random.random(), "y": random.random() * 0.5,
            "size": random.uniform(0.4, 2.0),
            "twinkle": random.uniform(0, 6.2832),
            "speed": random.uniform(1.5, 5.5)
        } for _ in range(count)]

    def _init_mountains(self):
        layers = []
        for layer in range(3):
            pts = []
            n = 24 + layer * 8
            base_h = 0.76 + layer * 0.06
            amp = 0.06 - layer * 0.014
            for i in range(n + 1):
                x = i / n
                h = base_h - amp * (0.5 + 0.5 * math.sin(x * (6 + layer * 3) + layer * 1.7) * math.sin(x * (13 + layer * 5) + layer))
                pts.append((x, h))
            layers.append(pts)
        self._mountains = layers

    def _ensure_cache(self, w, h):
        scale = self._scale_factor()
        rw = max(2, w // scale)
        rh = max(2, h // scale)
        if self._cache and self._cache[0] == rw and self._cache[1] == rh:
            return self._cache
        xs = np.linspace(0.0, 1.0, rw, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, rh, dtype=np.float32)
        X, Y = np.meshgrid(xs, ys)
        self._cache = (rw, rh, scale, X, Y)
        return self._cache

    def _render_aurora_3d(self, X, Y, t):
        """3D透视极光：地平线起源的体积光幕，向上延伸，远处汇聚到灭点"""
        horizon = 0.66
        height_above = np.clip(horizon - Y, 0, horizon) / horizon
        breath = 0.78 + 0.22 * math.sin(t * 0.4)

        intensity = np.zeros_like(X)
        r_acc = np.zeros_like(X)
        g_acc = np.zeros_like(X)
        b_acc = np.zeros_like(X)
        band_sum = np.zeros_like(X)

        bands = [
            {"cx": 0.50, "speed": 0.060, "warp": 5.2, "amp": 0.075, "w": 0.14, "rgb": (51, 255, 140), "i": 1.00, "phase": 0.0},
            {"cx": 0.36, "speed": 0.045, "warp": 6.8, "amp": 0.065, "w": 0.12, "rgb": (77, 217, 255), "i": 0.85, "phase": 1.6},
            {"cx": 0.64, "speed": 0.075, "warp": 4.5, "amp": 0.085, "w": 0.13, "rgb": (77, 230, 204), "i": 0.75, "phase": 3.1},
            {"cx": 0.44, "speed": 0.050, "warp": 7.5, "amp": 0.055, "w": 0.10, "rgb": (140, 89, 217), "i": 0.55, "phase": 4.7},
            {"cx": 0.56, "speed": 0.055, "warp": 6.0, "amp": 0.060, "w": 0.11, "rgb": (242, 115, 191), "i": 0.40, "phase": 6.2},
        ]

        n_bands = max(len(bands), 1)
        for k, b in enumerate(bands):
            phase = t * b["speed"] + b["phase"]
            s_mod = math.sin(t * 0.3 + b["phase"])
            spread = 0.08 + height_above * 0.22
            curve_x = b["cx"] + b["amp"] * np.sin(X * b["warp"] + phase) * (0.7 + 0.3 * s_mod) + 0.035 * np.sin(X * (b["warp"] * 2.3) + phase * 1.6) + 0.025 * np.sin(X * (b["warp"] * 1.7) + phase * 2.2)
            curve_x += (X - b["cx"]) * height_above * 0.3
            dx = X - curve_x
            band_w = b["w"] * (0.6 + 0.4 * np.sin(X * 9.0 + phase * 0.7)) + spread
            horiz_falloff = np.exp(-(dx ** 2) / (2.0 * band_w ** 2))

            edge_noise = 0.7 + 0.3 * self._fbm_approx(X, Y, t)
            horiz_falloff = horiz_falloff * edge_noise

            curtain_top = horizon - 0.02 * np.sin(X * 8.0 + phase)
            curtain_h = 0.42 + 0.18 * np.sin(X * 7.0 + phase * 0.9) + 0.08 * np.sin(X * 18.0 + phase * 1.8)
            curtain_h = np.clip(curtain_h, 0.15, 0.62)

            y_in_curtain = (curtain_top - Y) / (curtain_h + 1e-6)
            vert = np.exp(-(y_in_curtain ** 2) * 2.2)
            vert = vert * (Y < curtain_top + 0.02) * (Y > curtain_top - curtain_h - 0.05)

            streak = 0.35 + 0.65 * np.sin(X * (26 + k * 6) + phase * 2.0 + y_in_curtain * 14)
            streak = np.where(streak > 0, streak, 0)

            bottom_fade = np.clip(1.0 - y_in_curtain * 0.4, 0.3, 1.0)
            band_breath = 0.7 + 0.3 * math.sin(t * 0.4 + b["phase"])
            band_i = horiz_falloff * vert * streak * bottom_fade * b["i"] * band_breath * breath
            band_sum += band_i
            intensity += band_i
            persp = k / max(n_bands - 1, 1)
            lum = 0.33 * b["rgb"][0] + 0.33 * b["rgb"][1] + 0.33 * b["rgb"][2]
            cr = b["rgb"][0] * (1 - persp * 0.22) + lum * persp * 0.22
            cg = b["rgb"][1] * (1 - persp * 0.22) + lum * persp * 0.22
            cb = b["rgb"][2] * (1 - persp * 0.22) + lum * persp * 0.22
            cr = cr * (1 - persp * 0.12) + 63.75 * persp * 0.12
            cg = cg * (1 - persp * 0.12) + 89.25 * persp * 0.12
            cb = cb * (1 - persp * 0.12) + 153.0 * persp * 0.12
            r_acc += band_i * cr
            g_acc += band_i * cg
            b_acc += band_i * cb

            if k < 2:
                edge = np.clip(np.abs(dx) / band_w, 0, 1)
                edge = np.where(edge < 0.3, 0, (edge - 0.3) / 0.7)
                edge = edge * horiz_falloff * vert * streak
                r_acc += edge * (153 * 0.15 + 230 * 0.10) * b["i"]
                g_acc += edge * (51 * 0.15 + 77 * 0.10) * b["i"]
                b_acc += edge * (204 * 0.15 + 179 * 0.10) * b["i"]
                intensity += edge * 0.25 * b["i"]

        intensity += band_sum * 0.15
        r_acc += band_sum * 0.15 * 200
        g_acc += band_sum * 0.15 * 200
        b_acc += band_sum * 0.15 * 200

        intensity_norm = np.clip(intensity, 0, 1.8)
        r_col = np.clip(r_acc / (intensity + 1e-6), 0, 255) * intensity_norm
        g_col = np.clip(g_acc / (intensity + 1e-6), 0, 255) * intensity_norm
        b_col = np.clip(b_acc / (intensity + 1e-6), 0, 255) * intensity_norm
        return r_col, g_col, b_col, intensity_norm

    def _fbm_approx(self, X, Y, t):
        """轻量 fbm 近似，用于边缘晕染"""
        v = 0.5 * np.sin(X * 6.0 + t * 0.1) * np.cos(Y * 6.0)
        v += 0.25 * np.sin(X * 12.0 + t * 0.15) * np.cos(Y * 12.0)
        v += 0.125 * np.sin(X * 24.0 + t * 0.2) * np.cos(Y * 24.0)
        return np.clip(v * 0.5 + 0.5, 0, 1)

    def _tick(self):
        self._t += 1.0 / self.fps
        self.update()

    def _record_frame_cost(self, cost):
        if not (self._auto_degrade and HAS_NUMPY):
            return
        self._frame_costs.append(cost)
        if len(self._frame_costs) >= 40:
            avg = sum(self._frame_costs) / len(self._frame_costs)
            self._frame_costs.clear()
            budget = 1.0 / max(self._target_fps, 1)
            if avg > budget * 0.85:
                if self.quality == "high":
                    self.set_quality("medium")
                    self._degraded = True
                    log_message("极光背景检测到性能压力，画质已自动降为中", "INFO")
                elif self.quality == "medium":
                    self.set_quality("low")
                    self._degraded = True
                    log_message("极光背景检测到性能压力，画质已自动降为低", "INFO")
                elif self.fps > max(20, int(self._target_fps * 0.6)):
                    self.fps = max(20, int(self._target_fps * 0.6))
                    self._degraded = True
                    self.timer.start(1000 // max(self.fps, 15))
                    log_message(f"极光背景检测到性能压力，帧率已自动降为 {self.fps}", "INFO")
            elif self._degraded and avg < budget * 0.5:
                if self.fps < self._target_fps:
                    self.fps = self._target_fps
                    self._degraded = False
                    self.timer.start(1000 // max(self.fps, 15))
                    log_message("极光背景性能恢复，帧率已还原", "INFO")
                elif self.quality == "low":
                    self.set_quality("medium")
                    log_message("极光背景性能恢复，画质已升为中", "INFO")
                elif self.quality == "medium":
                    self.set_quality("high")
                    self._degraded = False
                    log_message("极光背景性能恢复，画质已升为高", "INFO")

    def paintEvent(self, event):
        frame_start = time.perf_counter() if self._auto_degrade else 0
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        if self.radius > 0:
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
            painter.setClipPath(path)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return
        if HAS_NUMPY:
            self._paint_numpy(painter, w, h)
        else:
            self._paint_fallback(painter, w, h)
        if self._auto_degrade:
            self._record_frame_cost(time.perf_counter() - frame_start)

    def _paint_numpy(self, painter, w, h):
        rw, rh, scale, X, Y = self._ensure_cache(w, h)
        t = self._t
        r_au, g_au, b_au, intensity = self._render_aurora_3d(X, Y, t)

        sky_r = np.where(Y < 0.5, 1.3 + Y * 4.0, 2.5 + (Y - 0.5) * 3.0)
        sky_g = np.where(Y < 0.5, 2.0 + Y * 5.0, 4.0 + (Y - 0.5) * 4.0)
        sky_b = np.where(Y < 0.5, 5.0 + Y * 8.0, 9.0 + (Y - 0.5) * 7.0)

        horizon = 0.68
        horizon_glow = np.clip(1.0 - np.abs(Y - horizon) * 5.0, 0.0, 1.0) * 14.0

        glow_intensity = intensity / 1.8
        bloom = glow_intensity * 0.5
        final_r = sky_r + r_au * 0.9 + bloom * 24 + horizon_glow * 0.4
        final_g = sky_g + g_au * 0.9 + bloom * 30 + horizon_glow
        final_b = sky_b + b_au * 0.9 + bloom * 18 + horizon_glow * 0.5

        height_above = np.clip(horizon - Y, 0, horizon) / horizon
        fog = np.clip(height_above * 2.5, 0, 1)
        final_r = final_r * (0.6 + 0.4 * fog)
        final_g = final_g * (0.6 + 0.4 * fog)
        final_b = final_b * (0.6 + 0.4 * fog)
        final_r = np.where(Y < 0.5, final_r * 0.7, final_r)
        final_g = np.where(Y < 0.5, final_g * 0.7, final_g)
        final_b = np.where(Y < 0.5, final_b * 0.7, final_b)

        arr = np.dstack([final_r, final_g, final_b])
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        arr = np.ascontiguousarray(arr)
        img = QImage(arr.data, rw, rh, 3 * rw, QImage.Format.Format_RGB888).copy()
        painter.drawImage(self.rect(), img)

        self._paint_stars(painter, w, h)
        self._paint_mountains(painter, w, h)

    def _paint_stars(self, painter, w, h):
        painter.setPen(Qt.PenStyle.NoPen)
        horizon_y = 0.66 * h
        for s in self._stars:
            sx = s["x"] * w
            sy = s["y"] * h
            if sy > horizon_y:
                continue
            bright = 0.5 + 0.5 * math.sin(self._t * s["speed"] + s["twinkle"])
            alpha = int(90 + 165 * bright)
            painter.setBrush(QColor(230, 240, 255, alpha))
            painter.drawEllipse(QRectF(sx - s["size"]/2, sy - s["size"]/2, s["size"], s["size"]))
            if bright > 0.85 and s["size"] > 1.3:
                painter.setBrush(QColor(200, 220, 255, int(alpha * 0.25)))
                painter.drawEllipse(QRectF(sx - s["size"]*1.8, sy - s["size"]*1.8, s["size"]*3.6, s["size"]*3.6))

    def _paint_mountains(self, painter, w, h):
        painter.setPen(Qt.PenStyle.NoPen)
        colors = [QColor(2, 4, 14, 235), QColor(4, 6, 18, 215), QColor(6, 8, 24, 195)]
        for li, pts in enumerate(self._mountains):
            painter.setBrush(colors[li])
            path = QPainterPath()
            path.moveTo(0, h)
            for x, y in pts:
                path.lineTo(x * w, y * h)
            path.lineTo(w, h)
            path.closeSubpath()
            painter.drawPath(path)

    def _paint_fallback(self, painter, w, h):
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor(1, 2, 5))
        grad.setColorAt(0.5, QColor(3, 4, 12))
        grad.setColorAt(0.66, QColor(5, 7, 20))
        grad.setColorAt(1.0, QColor(1, 1, 3))
        painter.fillRect(self.rect(), grad)
        horizon_y = h * 0.66
        bands = [(0.5, 51, 255, 140), (0.36, 77, 217, 255), (0.64, 89, 242, 191), (0.44, 140, 89, 217)]
        breath = 0.7 + 0.3 * math.sin(self._t * 0.4)
        for i, (cx, r, g, b) in enumerate(bands):
            phase = self._t * 0.07 + i * 1.6
            for j in range(20):
                t_ratio = j / 20
                px = (cx + 0.06 * math.sin(phase + t_ratio * 6)) * w
                py = horizon_y - t_ratio * h * 0.45
                alpha = int(120 * (1 - t_ratio) * (0.6 + 0.4 * math.sin(phase * 2 + t_ratio * 10)) * breath)
                painter.setBrush(QColor(r, g, b, max(0, alpha)))
                painter.drawEllipse(QRectF(px - 25, py - 8, 50, 16))
        self._paint_stars(painter, w, h)
        self._paint_mountains(painter, w, h)


class SkyBackgroundWidget(QWidget):
    """清晨天空背景 - 钴蓝渐变月白 + 薄卷云 + 丁达尔光痕 + 蜂蜜色微光"""
    def __init__(self, parent=None, radius=0):
        super().__init__(parent)
        self.radius = radius
        self.fps = 30
        self.quality = "high"
        self._t = 0.0
        self._clouds = []
        self._god_rays = []
        self._cache = None
        self._frame_costs = []
        self._auto_degrade = True
        self._target_fps = 30
        self._degraded = False
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self._tick)
        self._init_clouds()
        self._init_god_rays()
        self.set_fps(30)

    def set_radius(self, radius):
        self.radius = max(0, int(radius))
        self.update()

    def set_fps(self, fps):
        self._target_fps = max(15, int(fps))
        if not self._degraded:
            self.fps = self._target_fps
        self.timer.start(1000 // max(self.fps, 15))

    def set_quality(self, quality):
        self.quality = quality
        self._cache = None
        self._init_clouds()
        self._frame_costs.clear()
        self._degraded = False

    def _scale_factor(self):
        if self.quality == "high":
            return 3
        if self.quality == "medium":
            return 4
        return 6

    def _init_clouds(self):
        count = 4 if self.quality == "high" else (3 if self.quality == "medium" else 2)
        self._clouds = []
        layers = [(0.68, 0.42, 0.018), (0.52, 0.50, 0.014), (0.38, 0.58, 0.010), (0.26, 0.70, 0.006)]
        for i in range(min(count, len(layers))):
            alpha, base_y, speed = layers[i]
            self._clouds.append({
                "alpha": alpha, "base_y": base_y, "speed": speed,
                "seed": random.random() * 100,
                "scale": 3.0 + i * 1.5,
                "y_offset": random.uniform(-0.05, 0.05)
            })

    def _init_god_rays(self):
        sun_x = 0.72
        self._god_rays = []
        n_rays = 11
        spread = 0.62
        half = (n_rays - 1) / 2.0
        for i in range(n_rays):
            fi = float(i) - half
            angle = -1.5708 + fi * (spread / half)
            self._god_rays.append({
                "x": sun_x, "angle": angle, "phase": i * 1.7,
                "width": 0.010,
            })

    def _ensure_cache(self, w, h):
        scale = self._scale_factor()
        rw = max(2, w // scale)
        rh = max(2, h // scale)
        if self._cache and self._cache[0] == rw and self._cache[1] == rh:
            return self._cache
        xs = np.linspace(0.0, 1.0, rw, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, rh, dtype=np.float32)
        X, Y = np.meshgrid(xs, ys)
        self._cache = (rw, rh, scale, X, Y)
        return self._cache

    def _fbm_cloud(self, X, Y, t, seed, scale):
        v = 0.5 * np.sin(X * scale + seed + t * 0.05) * np.cos(Y * scale * 0.7 + seed)
        v += 0.25 * np.sin(X * scale * 2.1 + seed * 1.3 + t * 0.04) * np.cos(Y * scale * 1.5 + seed)
        v += 0.125 * np.sin(X * scale * 4.3 + seed * 2.1 + t * 0.03) * np.cos(Y * scale * 3.0 + seed)
        v += 0.06 * np.sin(X * scale * 8.5 + seed * 3.7 + t * 0.02) * np.cos(Y * scale * 6.0 + seed)
        return np.clip(v * 0.5 + 0.5, 0, 1)

    def _cloud_density_at(self, X, Y, t):
        n0 = self._fbm_cloud((X - (t * 0.012) % 1.0) % 1.0, Y, t, 0.0, 3.0)
        d0 = np.clip((n0 - 0.58) * 4.5, 0, 1) * 0.55
        n1 = self._fbm_cloud((X - (t * 0.009) % 1.0) % 1.0, Y, t, 13.7, 4.5)
        d1 = np.clip((n1 - 0.58) * 4.5, 0, 1) * 0.38
        return np.clip(d0 + d1, 0, 1)

    def _render_sky(self, X, Y, t):
        seg = np.clip(Y / 0.5, 0, 1)
        seg = seg * seg * (3 - 2 * seg)
        seg2 = np.clip((Y - 0.5) / 0.5, 0, 1)
        seg2 = seg2 * seg2 * (3 - 2 * seg2)
        top_r = 56 + seg * (148 - 56)
        top_r = top_r + seg2 * (235 - top_r)
        top_g = 92 + seg * (189 - 92)
        top_g = top_g + seg2 * (224 - top_g)
        top_b = 158 + seg * (235 - 158)
        top_b = top_b + seg2 * (209 - top_b)
        dream_haze = np.exp(-(np.maximum(0, Y - 0.55)) ** 1.5 * 3.0) * 0.15
        top_r = top_r + 242 * dream_haze
        top_g = top_g + 204 * dream_haze
        top_b = top_b + 217 * dream_haze
        low_haze = np.exp(-(np.maximum(0, 0.45 - Y)) ** 1.5 * 4.0) * 0.10
        top_r = top_r + 204 * low_haze
        top_g = top_g + 217 * low_haze
        top_b = top_b + 255 * low_haze
        sun_glow_r = np.exp(-((X - 0.72) ** 2 + (Y - 0.82) ** 2) * 180.0) * 0.35
        sun_glow_far = np.exp(-((X - 0.72) ** 2 + (Y - 0.82) ** 2) * 40.0) * 0.12
        top_r = top_r + 255 * sun_glow_r + 255 * sun_glow_far
        top_g = top_g + 235 * sun_glow_r + 217 * sun_glow_far
        top_b = top_b + 199 * sun_glow_r + 179 * sun_glow_far
        final_r = top_r.copy()
        final_g = top_g.copy()
        final_b = top_b.copy()

        n_clouds = max(len(self._clouds), 1)
        sun_x = 0.72
        sun_y = 0.82
        sun_dx = sun_x - X
        sun_dy = sun_y - Y
        sun_dnorm = np.sqrt(sun_dx ** 2 + sun_dy ** 2 + 0.16) + 1e-6
        light_dx = sun_dx / sun_dnorm
        light_dy = sun_dy / sun_dnorm
        light_dz = 0.4 / sun_dnorm
        sun_dist2 = (X - sun_x) ** 2 + (Y - sun_y) ** 2
        sun_factor = np.exp(-sun_dist2 * 8.0)
        cloud_cover = np.zeros_like(X)
        for idx, c in enumerate(self._clouds):
            drift = (t * c["speed"]) % 1.0
            base_y = c["base_y"]
            y_fade = np.clip(1.0 - np.abs(Y - base_y) / 0.18, 0, 1)
            def _dens_at(xxs, yys):
                cn = self._fbm_cloud((xxs - drift) % 1.0, yys + c["y_offset"], t, c["seed"], c["scale"])
                return np.clip((cn - 0.62) * 5.5, 0, 1) * y_fade
            dissolve = 0.7 + 0.3 * np.sin(t * 0.08 + c["seed"])
            dens = _dens_at(X, Y) * dissolve
            if dens.max() < 0.02:
                continue
            dL = _dens_at(X + 0.012, Y) * dissolve
            dR = _dens_at(X - 0.012, Y) * dissolve
            dU = _dens_at(X, Y + 0.012) * dissolve
            dD = _dens_at(X, Y - 0.012) * dissolve
            grad_x = (dR - dL) * 40.0
            grad_y = (dD - dU) * 40.0
            nlen = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.0) + 1e-6
            nx = -grad_x / nlen
            ny = -grad_y / nlen
            nz = 1.0 / nlen
            diff = np.maximum(0, nx * light_dx + ny * light_dy + nz * light_dz)
            diff = diff * 0.7 + 0.3
            rim = (1.0 - np.clip(nz, 0, 1)) ** 2
            lit_r = 275.0 * diff + 255.0 * rim * sun_factor * 0.5
            lit_g = 265.0 * diff + 242.0 * rim * sun_factor * 0.5
            lit_b = 245.0 * diff + 217.0 * rim * sun_factor * 0.5
            thickness = dens * 1.6
            self_shadow = np.exp(-thickness * 0.9)
            amb_r, amb_g, amb_b = 148.0, 158.0, 179.0
            cloud_r = amb_r + (lit_r - amb_r) * (0.60 + 0.40 * self_shadow)
            cloud_g = amb_g + (lit_g - amb_g) * (0.60 + 0.40 * self_shadow)
            cloud_b = amb_b + (lit_b - amb_b) * (0.60 + 0.40 * self_shadow)
            h = np.clip((Y - (base_y - 0.09)) / 0.18, 0, 1)
            cloud_r = cloud_r * (0.90 + 0.14 * h)
            cloud_g = cloud_g * (0.90 + 0.14 * h)
            cloud_b = cloud_b * (0.90 + 0.14 * h)
            persp = idx / max(n_clouds - 1, 1)
            cloud_r = cloud_r * (1 - persp * 0.25) + 235 * persp * 0.25
            cloud_g = cloud_g * (1 - persp * 0.25) + 237 * persp * 0.25
            cloud_b = cloud_b * (1 - persp * 0.25) + 242 * persp * 0.25
            alpha = np.clip(c["alpha"] * dens, 0, 1)
            final_r = final_r * (1 - alpha) + cloud_r * alpha
            final_g = final_g * (1 - alpha) + cloud_g * alpha
            final_b = final_b * (1 - alpha) + cloud_b * alpha
            cloud_cover = np.clip(cloud_cover + alpha, 0, 1)

        for ray in self._god_rays:
            ray_phase = t * 0.2 + ray["phase"]
            flicker = 0.55 + 0.45 * np.sin(ray_phase * 0.4)
            if flicker < 0.18:
                continue
            ca = np.cos(ray["angle"])
            sa = np.sin(ray["angle"])
            dx = X - sun_x
            dy = Y - sun_y
            along = dx * ca + dy * sa
            perp = np.abs(dx * sa - dy * ca)
            ray_width = 0.006 + np.maximum(along, 0.0) * 0.028
            ray_mask = np.exp(-(perp ** 2) / (2 * ray_width ** 2))
            ray_occ = np.zeros_like(X)
            for s in range(1, 6):
                ft = s / 6.0
                sp_x = sun_x + ca * (along * ft)
                sp_y = sun_y + sa * (along * ft)
                ray_occ = ray_occ + self._cloud_density_at(sp_x, sp_y, t)
            ray_occ = np.clip(1.0 - ray_occ / 5.0 * 1.3, 0.0, 1.0)
            along_pos = np.maximum(along, 0.0)
            len_fade = np.clip(along_pos * 4.5, 0.0, 1.0) * np.clip(1.0 - along_pos * 0.95, 0.0, 1.0)
            ray_mask = ray_mask * len_fade * flicker * ray_occ * 0.42
            atten = (1.0 - cloud_cover * 0.4)
            final_r = final_r + (255 - final_r) * ray_mask * 0.50 * atten
            final_g = final_g + (247 - final_g) * ray_mask * 0.50 * atten
            final_b = final_b + (230 - final_b) * ray_mask * 0.50 * atten

        bottom_mask = np.clip((Y - 0.75) * 4.0, 0, 1)
        horizon_glow = np.exp(-(Y - 0.85)**2 / 0.005) * 30.0
        final_r = final_r + horizon_glow * 0.7
        final_g = final_g + horizon_glow * 0.55
        final_b = final_b + horizon_glow * 0.35

        honey_phase = t * 0.15
        honey_pulse = 0.5 + 0.5 * np.sin(honey_phase)
        honey_intensity = honey_pulse * bottom_mask * 0.25
        final_r = final_r + (255 - final_r) * honey_intensity
        final_g = final_g + (237 - final_g) * honey_intensity
        final_b = final_b + (209 - final_b) * honey_intensity

        fog_noise = self._fbm_cloud(X, Y, t, 7.7, 1.5)
        fog_mask = bottom_mask * np.clip((fog_noise - 0.4) * 1.5, 0, 1) * 0.2
        final_r = final_r * (1 - fog_mask) + 235 * fog_mask
        final_g = final_g * (1 - fog_mask) + 230 * fog_mask
        final_b = final_b * (1 - fog_mask) + 224 * fog_mask

        shimmer = 0.5 + 0.5 * np.sin(Y * 30 + t * 0.5)
        final_r = final_r + shimmer * bottom_mask * 1.3
        final_g = final_g + shimmer * bottom_mask * 1.0
        final_b = final_b + shimmer * bottom_mask * 0.8

        return final_r, final_g, final_b

    def _tick(self):
        self._t += 1.0 / self.fps
        self.update()

    def _record_frame_cost(self, cost):
        if not (self._auto_degrade and HAS_NUMPY):
            return
        self._frame_costs.append(cost)
        if len(self._frame_costs) >= 40:
            avg = sum(self._frame_costs) / len(self._frame_costs)
            self._frame_costs.clear()
            budget = 1.0 / max(self._target_fps, 1)
            if avg > budget * 0.85:
                if self.quality == "high":
                    self.set_quality("medium")
                    self._degraded = True
                    log_message("天空背景检测到性能压力，画质已自动降为中", "INFO")
                elif self.quality == "medium":
                    self.set_quality("low")
                    self._degraded = True
                    log_message("天空背景检测到性能压力，画质已自动降为低", "INFO")
                elif self.fps > max(20, int(self._target_fps * 0.6)):
                    self.fps = max(20, int(self._target_fps * 0.6))
                    self._degraded = True
                    self.timer.start(1000 // max(self.fps, 15))
                    log_message(f"天空背景检测到性能压力，帧率已自动降为 {self.fps}", "INFO")
            elif self._degraded and avg < budget * 0.5:
                if self.fps < self._target_fps:
                    self.fps = self._target_fps
                    self._degraded = False
                    self.timer.start(1000 // max(self.fps, 15))
                    log_message("天空背景性能恢复，帧率已还原", "INFO")
                elif self.quality == "low":
                    self.set_quality("medium")
                    log_message("天空背景性能恢复，画质已升为中", "INFO")
                elif self.quality == "medium":
                    self.set_quality("high")
                    self._degraded = False
                    log_message("天空背景性能恢复，画质已升为高", "INFO")

    def paintEvent(self, event):
        frame_start = time.perf_counter() if self._auto_degrade else 0
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        if self.radius > 0:
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
            painter.setClipPath(path)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return
        if HAS_NUMPY:
            self._paint_numpy(painter, w, h)
        else:
            self._paint_fallback(painter, w, h)
        if self._auto_degrade:
            self._record_frame_cost(time.perf_counter() - frame_start)

    def _paint_numpy(self, painter, w, h):
        rw, rh, scale, X, Y = self._ensure_cache(w, h)
        t = self._t
        r_s, g_s, b_s = self._render_sky(X, Y, t)
        arr = np.dstack([r_s, g_s, b_s])
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        arr = np.ascontiguousarray(arr)
        img = QImage(arr.data, rw, rh, 3 * rw, QImage.Format.Format_RGB888).copy()
        painter.drawImage(self.rect(), img)

    def _paint_fallback(self, painter, w, h):
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor(60, 110, 180))
        grad.setColorAt(0.5, QColor(120, 170, 210))
        grad.setColorAt(1.0, QColor(220, 230, 240))
        painter.fillRect(self.rect(), grad)
        for c in self._clouds:
            drift = (self._t * c["speed"] * w) % w
            cx = (w * 0.5 + drift) % w
            cy = c["base_y"] * h + c["y_offset"] * h
            alpha = int(c["alpha"] * 180)
            painter.setBrush(QColor(250, 245, 240, alpha))
            painter.setPen(Qt.PenStyle.NoPen)
            for i in range(5):
                px = cx + (i - 2) * 30
                painter.drawEllipse(QRectF(px % w - 40, cy - 8, 80, 16))
        for ray in self._god_rays:
            flicker = 0.5 + 0.5 * math.sin(self._t * 0.2 + ray["phase"])
            if flicker < 0.3:
                continue
            alpha = int(flicker * 40)
            painter.setBrush(QColor(255, 250, 240, alpha))
            ca = math.cos(ray["angle"])
            sa = math.sin(ray["angle"])
            step = max(w, h) * 0.045
            for i in range(18):
                dist = i * step
                px = ray["x"] * w + ca * dist
                py = 0.82 * h + sa * dist
                painter.drawEllipse(QRectF(px - 3, py - 3, 6, 6))


if HAS_OPENGL:
    _GPU_CAP_CACHE = None

    def _detect_gpu_capability():
        global _GPU_CAP_CACHE
        if _GPU_CAP_CACHE is not None:
            return _GPU_CAP_CACHE
        vendor, renderer, gl_ver, capable, reason = "未知", "未知", "", True, "未检测（视为兼容）"
        try:
            fmt = QSurfaceFormat()
            fmt.setVersion(3, 3)
            fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
            off = QOffscreenSurface()
            off.setFormat(fmt)
            off.create()
            ctx = QOpenGLContext()
            ctx.setFormat(fmt)
            if ctx.create() and ctx.makeCurrent(off):
                f = None
                try:
                    f = QOpenGLVersionFunctionsFactory.get(QOpenGLVersionProfile(fmt), ctx)
                    if f is not None:
                        f.initializeOpenGLFunctions()
                except Exception:
                    f = None
                if f is None and HAS_OPENGL_41:
                    try:
                        f = QOpenGLFunctions_4_1_Core()
                        f.initializeOpenGLFunctions()
                    except Exception:
                        f = None
                if f is None:
                    try:
                        f = ctx.functions()
                        f.initializeOpenGLFunctions()
                    except Exception:
                        f = None
                if f is not None:
                    try:
                        v = f.glGetString(0x1F00)
                        vendor = v if isinstance(v, str) else str(v, encoding='utf-8', errors='ignore') if v else "未知"
                    except Exception:
                        pass
                    try:
                        r = f.glGetString(0x1F01)
                        renderer = r if isinstance(r, str) else str(r, encoding='utf-8', errors='ignore') if r else "未知"
                    except Exception:
                        pass
                    try:
                        g = f.glGetString(0x1F02)
                        gl_ver = g if isinstance(g, str) else str(g, encoding='utf-8', errors='ignore') if g else ""
                    except Exception:
                        pass
                ctx.doneCurrent()
                low = renderer.lower()
                sw_kw = ["microsoft", "llvmpipe", "softpipe", "swiftshader", "software", "gdi", "d3d11"]
                if any(k in low for k in sw_kw):
                    capable, reason = False, f"检测到软件渲染器 ({renderer})"
                elif "nvidia" in low or "geforce" in low or "quadro" in low or "rtx" in low or "gtx" in low:
                    capable, reason = True, "NVIDIA 显卡，OpenGL 兼容性优秀"
                elif "amd" in low or "radeon" in low or "ati " in low or "r9" in low or "rx " in low:
                    capable, reason = True, "AMD Radeon 显卡，OpenGL 兼容性良好"
                elif "intel" in low:
                    capable, reason = True, "Intel 核显，已启用但复杂着色器可能性能受限"
                elif renderer != "未知":
                    capable, reason = True, f"未知显卡 ({renderer})，尝试启用"
                else:
                    capable, reason = True, "无法获取显卡信息，视为兼容"
            else:
                capable, reason = True, "无法创建 OpenGL 上下文，视为兼容（实际渲染时再判断）"
        except Exception as e:
            capable, reason = True, f"GPU 检测异常: {e}（视为兼容，实际渲染时再判断）"
        _GPU_CAP_CACHE = (vendor, renderer, gl_ver, capable, reason)
        log_message(f"GPU 能力检测: vendor={vendor}, renderer={renderer}, gl={gl_ver}, capable={capable}, reason={reason}", "INFO")
        return _GPU_CAP_CACHE

    def _get_gl_version_funcs(ctx):
        versions = [
            (3, 3, QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile, "3.3 Compatibility"),
            (4, 1, QSurfaceFormat.OpenGLContextProfile.CoreProfile, "4.1 Core"),
            (2, 0, QSurfaceFormat.OpenGLContextProfile.NoProfile, "2.0"),
        ]
        tried = []
        for major, minor, profile, label in versions:
            tried.append(label)
            fmt = QSurfaceFormat()
            fmt.setVersion(major, minor)
            fmt.setProfile(profile)
            vp = QOpenGLVersionProfile(fmt)
            try:
                funcs = QOpenGLVersionFunctionsFactory.get(vp, ctx)
            except Exception:
                continue
            if funcs is not None:
                try:
                    funcs.initializeOpenGLFunctions()
                    return funcs, label
                except Exception as e:
                    debug_print(f"_get_gl_version_funcs: {label} initializeOpenGLFunctions 失败: {e}")
                    continue
        raise RuntimeError(f"无法获取 OpenGL 函数 (尝试过: {', '.join(tried)})")

    class AuroraShaderWindow(QOpenGLWidget):
        _VS_SRC = """
        #version 330
        in vec2 aPos;
        out vec2 vUv;
        void main() {
            vUv = aPos * 0.5 + 0.5;
            gl_Position = vec4(aPos, 0.0, 1.0);
        }
        """
        _FS_SRC = """
        #version 330
        in vec2 vUv;
        uniform float uTime;
        uniform vec2 uResolution;
        uniform float uQuality;
        out vec4 fragColor;

        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        float vnoise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
                       mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        float fbm(vec2 p) {
            float v = 0.0;
            float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * vnoise(p);
                p *= 2.0;
                a *= 0.5;
            }
            return v;
        }

        void main() {
            vec2 uv = vUv;
            vec2 p = uv;
            p.x *= uResolution.x / max(uResolution.y, 1.0);

            float breath = 0.88 + 0.12 * sin(uTime * 0.4);

            vec3 col = vec3(0.0);
            float skyR = mix(0.005, 0.02, smoothstep(0.0, 0.5, uv.y));
            float skyG = mix(0.008, 0.03, smoothstep(0.0, 0.5, uv.y));
            float skyB = mix(0.02, 0.08, smoothstep(0.0, 0.5, uv.y));
            col = vec3(skyR, skyG, skyB);

            float neb = fbm(uv * 2.5 + vec2(uTime * 0.02, 1.3));
            col += vec3(0.06, 0.04, 0.12) * smoothstep(0.45, 0.85, neb) * smoothstep(0.0, 1.0, uv.y) * 0.7;
            col += vec3(0.10, 0.06, 0.18) * smoothstep(0.5, 0.95, neb) * smoothstep(0.3, 0.95, uv.y) * 0.5;

            vec3 aurora = vec3(0.0);
            float bandSum = 0.0;

            vec3 bcol0 = vec3(0.15, 0.95, 0.45);
            vec3 bcol1 = vec3(0.25, 0.80, 1.00);
            vec3 bcol2 = vec3(0.30, 0.90, 0.80);
            vec3 bcol3 = vec3(0.60, 0.30, 0.90);
            vec3 bcol4 = vec3(0.95, 0.40, 0.70);

            for (int k = 0; k < 5; k++) {
                float bk = float(k);
                float phase = uTime * (0.04 + bk * 0.008) + bk * 1.8;
                float n1 = fbm(vec2(p.x * 4.5 + bk * 1.3, uTime * 0.12 + bk * 0.7)) - 0.5;
                float n2 = fbm(vec2(p.x * 2.0 + bk * 2.1, uTime * 0.07 + bk * 1.2)) - 0.5;
                float n3 = fbm(vec2(p.x * 8.0 + bk * 0.8, uTime * 0.18 + bk * 0.5)) - 0.5;
                float cx = 0.5 + n1 * 0.28 + n2 * 0.18 + n3 * 0.10 + sin(p.x * 3.0 + phase) * 0.06;

                float bandW = 0.18 + bk * 0.04 + n1 * 0.08;
                float dx = p.x - cx;
                float horizFall = exp(-(dx * dx) / (2.0 * bandW * bandW));

                float curtainTop = 0.92 - bk * 0.06 + n2 * 0.08;
                float curtainH = 0.55 + bk * 0.08 + n1 * 0.12;
                curtainH = clamp(curtainH, 0.30, 0.80);
                float yInCurtain = (curtainTop - uv.y) / (curtainH + 1e-6);
                float vert = exp(-yInCurtain * yInCurtain * 1.2);
                vert *= smoothstep(curtainH + 0.05, curtainH - 0.02, curtainTop - uv.y);
                vert *= smoothstep(0.0, 0.12, curtainTop - uv.y);

                float streak = 0.5 + 0.5 * sin(p.x * (20.0 + bk * 7.0) + phase * 2.0 + yInCurtain * 10.0);
                streak = max(streak, 0.0);
                float bottomFade = clamp(1.0 - yInCurtain * 0.35, 0.25, 1.0);
                float bandBreath = 0.7 + 0.3 * sin(uTime * 0.4 + bk * 1.8);
                float bi = 1.2 - bk * 0.14;
                float bandI = horizFall * vert * streak * bottomFade * bi * bandBreath * breath;
                bandSum += bandI;

                vec3 c = (k == 0) ? bcol0 : (k == 1) ? bcol1 : (k == 2) ? bcol2 : (k == 3) ? bcol3 : bcol4;
                float persp = bk / 4.0;
                c = mix(c, vec3(dot(c, vec3(0.33))), persp * 0.15);
                aurora += c * bandI;

                vec3 edgeCol = vec3(0.7, 0.3, 0.9) * (1.0 - persp);
                float edge = smoothstep(0.0, 0.35, abs(dx) / bandW) * horizFall * vert * streak * 0.18;
                aurora += edgeCol * edge;
            }

            aurora += bandSum * 0.12;

            float intensity = clamp(max(max(aurora.r, aurora.g), aurora.b), 0.0, 1.8);
            float glow = intensity / 1.8;
            float bloom = glow * 0.65;
            col += aurora * 1.2;
            col += vec3(0.06, 0.16, 0.12) * bloom * 15.0;

            col = clamp(col, 0.0, 1.0);
            col = pow(col, vec3(0.92));
            fragColor = vec4(col, 1.0);
        }
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._shader_id = id(self)
            self._t = 0.0
            self.fps = 60
            self._target_fps = 60
            self._degraded = False
            self.quality = "high"
            self._prog = None
            self._vao = None
            self._vbo = None
            self._funcs = None
            self._loc_time = -1
            self._loc_res = -1
            self._loc_quality = -1
            self._timer = QTimer(self)
            self._timer.setTimerType(Qt.TimerType.PreciseTimer)
            self._timer.timeout.connect(self._tick)
            self._init_ok = False
            self._frame_costs = []
            self._auto_degrade = True

        def _tick(self):
            self._t += 1.0 / max(self.fps, 15)
            self.update()

        def set_fps(self, fps):
            self._target_fps = max(15, int(fps))
            if not self._degraded:
                self.fps = self._target_fps
            self._timer.start(1000 // max(self.fps, 15))

        def set_quality(self, quality):
            self.quality = quality
            self._degraded = False

        def _record_frame_cost(self, cost):
            if not self._auto_degrade:
                return
            self._frame_costs.append(cost)
            if len(self._frame_costs) >= 40:
                avg = sum(self._frame_costs) / len(self._frame_costs)
                self._frame_costs.clear()
                budget = 1.0 / max(self._target_fps, 1)
                if avg > budget * 0.85:
                    if self.quality == "high":
                        self.set_quality("medium")
                        self._degraded = True
                        log_message("极光GPU着色器检测到性能压力，画质已自动降为中", "INFO")
                    elif self.quality == "medium":
                        self.set_quality("low")
                        self._degraded = True
                        log_message("极光GPU着色器检测到性能压力，画质已自动降为低", "INFO")
                    elif self.fps > max(20, int(self._target_fps * 0.6)):
                        self.fps = max(20, int(self._target_fps * 0.6))
                        self._degraded = True
                        self._timer.start(1000 // max(self.fps, 15))
                        log_message(f"极光GPU着色器检测到性能压力，帧率已自动降为 {self.fps}", "INFO")
                elif self._degraded and avg < budget * 0.5:
                    if self.fps < self._target_fps:
                        self.fps = self._target_fps
                        self._degraded = False
                        self._timer.start(1000 // max(self.fps, 15))
                        log_message("极光GPU着色器性能恢复，帧率已还原", "INFO")
                    elif self.quality == "low":
                        self.set_quality("medium")
                        log_message("极光GPU着色器性能恢复，画质已升为中", "INFO")
                    elif self.quality == "medium":
                        self.set_quality("high")
                        self._degraded = False
                        log_message("极光GPU着色器性能恢复，画质已升为高", "INFO")

        def initializeGL(self):
            try:
                ctx = self.context()
                self._funcs, gl_ver = _get_gl_version_funcs(ctx)
                cfmt = ctx.format()
                renderer_str = "未知"
                vendor_str = "未知"
                try:
                    renderer = self._funcs.glGetString(0x1F01)
                    if renderer:
                        renderer_str = renderer if isinstance(renderer, str) else str(renderer, encoding='utf-8', errors='ignore')
                except Exception:
                    pass
                try:
                    vendor = self._funcs.glGetString(0x1F00)
                    if vendor:
                        vendor_str = vendor if isinstance(vendor, str) else str(vendor, encoding='utf-8', errors='ignore')
                except Exception:
                    pass
                self._renderer_name = renderer_str
                low = renderer_str.lower()
                if "nvidia" in low or "geforce" in low:
                    compat_note = "NVIDIA: 完全兼容"
                elif "amd" in low or "radeon" in low or "ati " in low:
                    compat_note = "AMD: 兼容（如遇问题可降低画质）"
                elif "intel" in low:
                    compat_note = "Intel 核显: 兼容但性能有限"
                else:
                    compat_note = "未知厂商: 尝试兼容"
                log_message(f"AuroraShader GL 初始化成功: {gl_ver}, 版本={cfmt.majorVersion()}.{cfmt.minorVersion()}, Profile={cfmt.profile()}, 厂商={vendor_str}, 渲染器={renderer_str}, 兼容={compat_note}", "INFO")
                sw_keywords = ["microsoft", "llvmpipe", "softpipe", "swiftshader", "software", "gdi"]
                if any(kw in low for kw in sw_keywords):
                    raise RuntimeError(f"检测到软件渲染 ({renderer_str})，将回退到 CPU 版本以获得更好性能")
                self._prog = QOpenGLShaderProgram(self)
                if not self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, self._VS_SRC):
                    raise RuntimeError("vs compile: " + self._prog.log())
                if not self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, self._FS_SRC):
                    raise RuntimeError("fs compile: " + self._prog.log())
                self._prog.bindAttributeLocation("aPos", 0)
                if not self._prog.link():
                    raise RuntimeError("link: " + self._prog.log())
                self._loc_time = self._prog.uniformLocation("uTime")
                self._loc_res = self._prog.uniformLocation("uResolution")
                self._loc_quality = self._prog.uniformLocation("uQuality")
                import struct
                verts = struct.pack('6f', -1.0, -1.0, 3.0, -1.0, -1.0, 3.0)
                self._vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
                self._vbo.create()
                self._vbo.bind()
                self._vbo.allocate(verts, len(verts))
                self._vbo.release()
                self._vao = QOpenGLVertexArrayObject(self)
                self._vao.create()
                self._vao.bind()
                self._vbo.bind()
                self._prog.enableAttributeArray(0)
                self._prog.setAttributeBuffer(0, 0x1406, 0, 2)
                self._vbo.release()
                self._vao.release()
                self._init_ok = True
                self._timer.start(1000 // max(self.fps, 15))
                debug_print(f"AuroraShaderWindow 初始化成功, FPS={self.fps}, quality={self.quality}")
            except Exception as e:
                self._init_error = str(e)
                log_message(f"AuroraShaderWindow 初始化失败: {e}", "ERROR")
                self._init_ok = False
                self._timer.stop()

        def paintGL(self):
            if not self._init_ok or self._funcs is None or self._prog is None:
                return
            if not getattr(self, '_first_frame_logged', False):
                self._first_frame_logged = True
                log_message(f"AuroraShader paintGL 首帧: w={self.width()}, h={self.height()}, ctx={self.context() is not None}", "INFO")
            frame_start = time.perf_counter() if self._auto_degrade else 0
            f = self._funcs
            dpr = self.devicePixelRatio() if hasattr(self, 'devicePixelRatio') else 1.0
            vw = max(1, int(self.width() * dpr))
            vh = max(1, int(self.height() * dpr))
            f.glViewport(0, 0, vw, vh)
            f.glClearColor(0.012, 0.018, 0.06, 1.0)
            f.glClear(0x4000)
            f.glDisable(0x0B71)
            self._prog.bind()
            self._prog.setUniformValue(self._loc_time, float(self._t))
            self._prog.setUniformValue(self._loc_res, float(vw), float(vh))
            qmap = {"ultra": 1.2, "high": 1.0, "medium": 0.7, "low": 0.45}
            self._prog.setUniformValue(self._loc_quality, float(qmap.get(self.quality, 1.0)))
            self._vao.bind()
            f.glDrawArrays(4, 0, 3)
            self._vao.release()
            self._prog.release()
            if self._auto_degrade:
                self._record_frame_cost(time.perf_counter() - frame_start)

        def cleanup(self):
            try:
                if self._vbo is not None:
                    self._vbo.destroy()
                if self._vao is not None:
                    self._vao.destroy()
                if self._prog is not None:
                    self._prog.removeAllShaders()
            except Exception:
                pass

        def closeEvent(self, event):
            self.cleanup()
            super().closeEvent(event)


    class AuroraShaderWidget(AuroraShaderWindow):
        def __init__(self, parent=None, radius=0):
            super().__init__(parent)
            self.radius = max(0, int(radius))
            self._fallback_check_done = False
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            QTimer.singleShot(500, self._check_init_and_fallback)

        def _check_init_and_fallback(self):
            if self._fallback_check_done:
                return
            self._fallback_check_done = True
            if not self._init_ok:
                err = getattr(self, '_init_error', '未知错误')
                log_message(f"AuroraShader GL 初始化失败，触发回退 (原因: {err})", "ERROR")
                parent = self.parent()
                if parent is not None:
                    QTimer.singleShot(0, lambda: parent._fallback_to_cpu_dynamic_bg("aurora"))
            else:
                log_message(f"AuroraShaderWidget 回退检查通过: init_ok={self._init_ok}", "INFO")

        def set_radius(self, radius):
            self.radius = max(0, int(radius))
            self._apply_mask()

        def _apply_mask(self):
            if self.radius > 0:
                from PyQt6.QtGui import QRegion
                path = QPainterPath()
                path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), self.radius, self.radius)
                region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
                self.setMask(region)
            else:
                self.clearMask()

        def trigger_click(self, x, y):
            pass

        def is_init_ok(self):
            return self._init_ok

        def resizeEvent(self, event):
            super().resizeEvent(event)
            self._apply_mask()


    class SkyShaderWindow(QOpenGLWidget):
        """GPU 着色器渲染的天空背景"""
        _VS_SRC = """
        #version 330
        in vec2 aPos;
        out vec2 vUv;
        void main() {
            vUv = aPos * 0.5 + 0.5;
            gl_Position = vec4(aPos, 0.0, 1.0);
        }
        """
        _FS_SRC = """
        #version 330
        in vec2 vUv;
        uniform float uTime;
        uniform vec2 uResolution;
        uniform float uQuality;
        out vec4 fragColor;

        float hash3(vec3 p) {
            p = fract(p * vec3(443.8975, 441.4235, 437.1955));
            p += dot(p, p.yzx + 19.19);
            return fract((p.x + p.y) * p.z);
        }
        float vnoise3(vec3 p) {
            vec3 i = floor(p);
            vec3 f = fract(p);
            vec3 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
            return mix(
                mix(mix(hash3(i + vec3(0.0, 0.0, 0.0)), hash3(i + vec3(1.0, 0.0, 0.0)), u.x),
                    mix(hash3(i + vec3(0.0, 1.0, 0.0)), hash3(i + vec3(1.0, 1.0, 0.0)), u.x), u.y),
                mix(mix(hash3(i + vec3(0.0, 0.0, 1.0)), hash3(i + vec3(1.0, 0.0, 1.0)), u.x),
                    mix(hash3(i + vec3(0.0, 1.0, 1.0)), hash3(i + vec3(1.0, 1.0, 1.0)), u.x), u.y), u.z);
        }
        float fbm3(vec3 p) {
            float v = 0.0;
            float a = 0.5;
            int oct = int(mix(3.0, 5.0, uQuality));
            for (int i = 0; i < 5; i++) {
                if (i >= oct) break;
                v += a * vnoise3(p);
                p = p * 2.03 + vec3(1.7, 9.2, 2.3);
                a *= 0.5;
            }
            return v;
        }
        float cloudDensity(vec3 p) {
            float h = clamp(p.y, 0.0, 3.0);
            float heightFade = smoothstep(0.25, 0.6, h) * (1.0 - smoothstep(1.0, 1.9, h));
            if (heightFade < 0.002) return 0.0;
            vec3 q = p * 0.9 + vec3(uTime * 0.015, 0.0, uTime * 0.008);
            vec3 warp = vec3(
                fbm3(q + vec3(0.0)),
                fbm3(q + vec3(5.2, 1.3, 3.7)),
                fbm3(q + vec3(2.1, 7.8, 4.5))
            );
            vec3 qq = q + warp * 0.45;
            float n = fbm3(qq * 1.3);
            float detail = fbm3(qq * 4.0 + vec3(3.3, 1.1, 6.7));
            float coverage = 0.55;
            float d = smoothstep(coverage, coverage + 0.20, n) * heightFade;
            d *= (0.6 + 0.4 * detail);
            d = clamp(d - detail * 0.10, 0.0, 1.0);
            return d * 0.95;
        }
        float hgPhase(float costh, float g) {
            float g2 = g * g;
            return (1.0 - g2) / pow(1.0 + g2 - 2.0 * g * costh, 1.5);
        }
        float lightMarch(vec3 p, vec3 sunDir) {
            float transmittance = 1.0;
            float stepSz = 0.08;
            for (int i = 1; i <= 5; i++) {
                p += sunDir * stepSz;
                float d = cloudDensity(p);
                transmittance *= exp(-d * stepSz * 3.5);
                if (transmittance < 0.02) break;
            }
            return transmittance;
        }

        void main() {
            vec2 uv = vUv;
            float aspect = uResolution.x / max(uResolution.y, 1.0);
            bool isLow = uQuality < 0.6;
            bool isUltra = uQuality > 1.05;

            vec3 skyTop = vec3(0.18, 0.32, 0.58);
            vec3 skyMid = vec3(0.30, 0.52, 0.82);
            vec3 skyHorizon = vec3(0.58, 0.70, 0.88);
            vec3 col = mix(skyHorizon, skyMid, smoothstep(0.0, 0.45, uv.y));
            col = mix(col, skyTop, smoothstep(0.45, 1.0, uv.y));
            float warmHaze = exp(-pow(max(0.0, uv.y - 0.55), 1.5) * 3.5) * 0.14;
            col += vec3(1.0, 0.78, 0.62) * warmHaze;
            if (!isLow) {
                float coolHaze = exp(-pow(max(0.0, 0.42 - uv.y), 1.5) * 3.0) * 0.10;
                col += vec3(0.65, 0.75, 1.0) * coolHaze;
            }

            vec2 sunPos = vec2(0.72, 0.82);
            float sunD = length((uv - sunPos) * vec2(aspect, 1.0));
            float sunGlow = exp(-sunD * sunD * 50.0);
            float sunDisc = smoothstep(0.028, 0.014, sunD);
            col += vec3(1.3, 1.08, 0.82) * sunGlow * 0.55;
            if (!isLow) {
                col += vec3(1.1, 0.90, 0.68) * exp(-sunD * sunD * 15.0) * 0.25;
            }
            col = mix(col, vec3(1.25, 1.08, 0.85), sunDisc * 0.92);

            vec3 sunDir3D = normalize(vec3(0.45, 0.75, 0.55));
            vec3 rd = normalize(vec3((uv.x - 0.5) * aspect * 1.2, uv.y * 1.8 + 0.15, 0.8));
            vec3 ro = vec3(0.0, 0.0, 0.0);
            float cloudBottom = 0.2;
            float cloudTop = 2.2;
            float tEnter = (cloudBottom - ro.y) / max(rd.y, 0.001);
            float tExit = (cloudTop - ro.y) / max(rd.y, 0.001);
            if (tEnter < 0.0) tEnter = 0.0;
            float transmittance = 1.0;
            vec3 scatteredLight = vec3(0.0);
            if (rd.y > 0.001 && tExit > tEnter) {
                int maxSteps = 24;
                if (uQuality > 0.9) maxSteps = 72;
                else if (uQuality > 0.6) maxSteps = 48;
                else if (uQuality > 0.4) maxSteps = 32;
                else maxSteps = 24;
                int steps = maxSteps;
                float range = tExit - tEnter;
                float stepSize = range / float(steps);
                int lightSteps = 5;
                if (isUltra) lightSteps = 7;
                else if (uQuality > 0.9) lightSteps = 5;
                else if (uQuality > 0.6) lightSteps = 4;
                else lightSteps = 3;
                for (int i = 0; i < 72; i++) {
                    if (i >= steps) break;
                    float t = tEnter + (float(i) + 0.5) * stepSize;
                    vec3 pos = ro + rd * t;
                    float dens = cloudDensity(pos);
                    if (dens < 0.005) continue;
                    float lt = 1.0;
                    {
                        vec3 lp = pos + sunDir3D * 0.08;
                        for (int li = 0; li < 7; li++) {
                            if (li >= lightSteps) break;
                            float ld = cloudDensity(lp);
                            lt *= exp(-ld * 0.08 * 3.5);
                            if (lt < 0.02) break;
                            lp += sunDir3D * 0.08;
                        }
                    }
                    float lightT = lt;
                    float extinction = exp(-dens * stepSize * 2.0);
                    transmittance *= extinction;
                    float costh = dot(rd, sunDir3D);
                    float phase = hgPhase(costh, 0.6) * 0.7 + hgPhase(costh, -0.3) * 0.25;
                    phase = clamp(phase, 0.0, 2.5);
                    vec3 litCol = mix(
                        vec3(1.05, 0.88, 0.72),
                        vec3(1.12, 0.66, 0.52),
                        pow(1.0 - lightT, 1.5)
                    );
                    litCol += vec3(1.0, 0.88, 0.70) * pow(lightT, 2.5) * 0.30;
                    if (isUltra) {
                        litCol += vec3(1.15, 0.92, 0.78) * pow(lightT, 5.0) * 0.22;
                    }
                    vec3 shadowCol = mix(
                        vec3(0.16, 0.13, 0.38),
                        vec3(0.36, 0.14, 0.42),
                        dens * 0.7
                    );
                    shadowCol += vec3(0.12, 0.10, 0.30) * (1.0 - lightT) * 0.4;
                    vec3 cloudCol = mix(shadowCol, litCol, lightT);
                    cloudCol += vec3(0.28, 0.40, 0.65) * 0.12 * (1.0 - lightT);
                    scatteredLight += transmittance * dens * cloudCol * phase * stepSize * 2.0;
                    if (transmittance < 0.005) break;
                }
            }
            col = col * transmittance + scatteredLight;

            if (uQuality > 0.9) {
                vec2 toSun = sunPos - uv;
                float distToSun = length(toSun * vec2(aspect, 1.0));
                if (distToSun > 0.005 && distToSun < 1.5) {
                    vec2 dir = normalize(toSun);
                    int raySteps = 12;
                    float occ = 0.0;
                    for (int s = 1; s <= 12; s++) {
                        if (s > raySteps) break;
                        float fi = float(s) / float(raySteps);
                        vec2 sp = uv + dir * fi * 0.25;
                        vec3 rd_sp = normalize(vec3((sp.x - 0.5) * aspect * 1.2, sp.y * 1.8 + 0.15, 0.8));
                        float t_sp = 0.8 / max(rd_sp.y, 0.001);
                        vec3 pos_sp = rd_sp * t_sp;
                        occ += cloudDensity(pos_sp);
                    }
                    occ = clamp(1.0 - occ / float(raySteps) * 0.4, 0.0, 1.0);
                    float rayMask = exp(-distToSun * 2.2) * occ;
                    col += vec3(1.15, 0.98, 0.72) * rayMask * 0.12 * transmittance;
                }
            }

            float lum = dot(col, vec3(0.299, 0.587, 0.114));
            float bloomThresh = 1.3;
            float bloomStr = 0.0;
            if (isUltra) { bloomThresh = 0.72; bloomStr = 0.22; }
            else if (uQuality > 0.9) { bloomThresh = 0.75; bloomStr = 0.18; }
            else if (uQuality > 0.6) { bloomThresh = 0.82; bloomStr = 0.10; }
            else { bloomThresh = 1.3; bloomStr = 0.0; }
            if (bloomStr > 0.0) {
                float bloomMask = smoothstep(bloomThresh, 1.3, lum);
                col += col * bloomMask * bloomStr;
                col += vec3(1.0, 0.82, 0.55) * sunGlow * 0.10;
            }

            if (uQuality > 0.6) {
                float dreamFog = exp(-pow(max(0.0, abs(uv.y - 0.5) - 0.15), 1.5) * 4.0) * 0.08;
                col += vec3(0.85, 0.72, 0.95) * dreamFog * (1.0 - transmittance * 0.5);
                col += vec3(0.95, 0.80, 0.65) * dreamFog * 0.5;
            }

            float sat = 1.18;
            if (isUltra) sat = 1.22;
            else if (uQuality > 0.9) sat = 1.18;
            else if (uQuality > 0.6) sat = 1.12;
            else sat = 1.06;
            float lum2 = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(vec3(lum2), col, sat);

            float horizonMask = smoothstep(0.18, 0.0, uv.y);
            col += vec3(0.85, 0.50, 0.28) * horizonMask * 0.14;

            col = col / (col + vec3(0.24));
            col = pow(col, vec3(0.90));
            fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
        }
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._shader_id = id(self)
            self._t = 0.0
            self.fps = 60
            self._target_fps = 60
            self._degraded = False
            self.quality = "high"
            self._prog = None
            self._vao = None
            self._vbo = None
            self._funcs = None
            self._loc_time = -1
            self._loc_res = -1
            self._loc_quality = -1
            self._timer = QTimer(self)
            self._timer.setTimerType(Qt.TimerType.PreciseTimer)
            self._timer.timeout.connect(self._tick)
            self._init_ok = False
            self._frame_costs = []
            self._auto_degrade = True

        def _tick(self):
            self._t += 1.0 / max(self.fps, 15)
            self.update()

        def set_fps(self, fps):
            self._target_fps = max(15, int(fps))
            if not self._degraded:
                self.fps = self._target_fps
            self._timer.start(1000 // max(self.fps, 15))

        def set_quality(self, quality):
            self.quality = quality
            self._degraded = False

        def _record_frame_cost(self, cost):
            if not self._auto_degrade:
                return
            self._frame_costs.append(cost)
            if len(self._frame_costs) >= 40:
                avg = sum(self._frame_costs) / len(self._frame_costs)
                self._frame_costs.clear()
                budget = 1.0 / max(self._target_fps, 1)
                if avg > budget * 0.85:
                    if self.quality == "high":
                        self.set_quality("medium")
                        self._degraded = True
                        log_message("天空GPU着色器检测到性能压力，画质已自动降为中", "INFO")
                    elif self.quality == "medium":
                        self.set_quality("low")
                        self._degraded = True
                        log_message("天空GPU着色器检测到性能压力，画质已自动降为低", "INFO")
                    elif self.fps > max(20, int(self._target_fps * 0.6)):
                        self.fps = max(20, int(self._target_fps * 0.6))
                        self._degraded = True
                        self._timer.start(1000 // max(self.fps, 15))
                        log_message(f"天空GPU着色器检测到性能压力，帧率已自动降为 {self.fps}", "INFO")
                elif self._degraded and avg < budget * 0.5:
                    if self.fps < self._target_fps:
                        self.fps = self._target_fps
                        self._degraded = False
                        self._timer.start(1000 // max(self.fps, 15))
                        log_message("天空GPU着色器性能恢复，帧率已还原", "INFO")
                    elif self.quality == "low":
                        self.set_quality("medium")
                        log_message("天空GPU着色器性能恢复，画质已升为中", "INFO")
                    elif self.quality == "medium":
                        self.set_quality("high")
                        self._degraded = False
                        log_message("天空GPU着色器性能恢复，画质已升为高", "INFO")

        def initializeGL(self):
            try:
                ctx = self.context()
                self._funcs, gl_ver = _get_gl_version_funcs(ctx)
                cfmt = ctx.format()
                renderer_str = "未知"
                vendor_str = "未知"
                try:
                    renderer = self._funcs.glGetString(0x1F01)
                    if renderer:
                        renderer_str = renderer if isinstance(renderer, str) else str(renderer, encoding='utf-8', errors='ignore')
                except Exception:
                    pass
                try:
                    vendor = self._funcs.glGetString(0x1F00)
                    if vendor:
                        vendor_str = vendor if isinstance(vendor, str) else str(vendor, encoding='utf-8', errors='ignore')
                except Exception:
                    pass
                self._renderer_name = renderer_str
                low = renderer_str.lower()
                if "nvidia" in low or "geforce" in low:
                    compat_note = "NVIDIA: 完全兼容"
                elif "amd" in low or "radeon" in low or "ati " in low:
                    compat_note = "AMD: 兼容（如遇问题可降低画质）"
                elif "intel" in low:
                    compat_note = "Intel 核显: 兼容但性能有限"
                else:
                    compat_note = "未知厂商: 尝试兼容"
                log_message(f"SkyShader GL 初始化成功: {gl_ver}, 版本={cfmt.majorVersion()}.{cfmt.minorVersion()}, Profile={cfmt.profile()}, 厂商={vendor_str}, 渲染器={renderer_str}, 兼容={compat_note}", "INFO")
                sw_keywords = ["microsoft", "llvmpipe", "softpipe", "swiftshader", "software", "gdi"]
                if any(kw in low for kw in sw_keywords):
                    raise RuntimeError(f"检测到软件渲染 ({renderer_str})，将回退到 CPU 版本以获得更好性能")
                self._prog = QOpenGLShaderProgram(self)
                if not self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, self._VS_SRC):
                    raise RuntimeError("vs compile: " + self._prog.log())
                if not self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, self._FS_SRC):
                    raise RuntimeError("fs compile: " + self._prog.log())
                self._prog.bindAttributeLocation("aPos", 0)
                if not self._prog.link():
                    raise RuntimeError("link: " + self._prog.log())
                self._loc_time = self._prog.uniformLocation("uTime")
                self._loc_res = self._prog.uniformLocation("uResolution")
                self._loc_quality = self._prog.uniformLocation("uQuality")
                import struct
                verts = struct.pack('6f', -1.0, -1.0, 3.0, -1.0, -1.0, 3.0)
                self._vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
                self._vbo.create()
                self._vbo.bind()
                self._vbo.allocate(verts, len(verts))
                self._vbo.release()
                self._vao = QOpenGLVertexArrayObject(self)
                self._vao.create()
                self._vao.bind()
                self._vbo.bind()
                self._prog.enableAttributeArray(0)
                self._prog.setAttributeBuffer(0, 0x1406, 0, 2)
                self._vbo.release()
                self._vao.release()
                self._init_ok = True
                self._timer.start(1000 // max(self.fps, 15))
                debug_print(f"SkyShaderWindow 初始化成功, FPS={self.fps}, quality={self.quality}")
            except Exception as e:
                self._init_error = str(e)
                log_message(f"SkyShaderWindow 初始化失败: {e}", "ERROR")
                self._init_ok = False
                self._timer.stop()

        def paintGL(self):
            if not self._init_ok or self._funcs is None or self._prog is None:
                return
            if not getattr(self, '_first_frame_logged', False):
                self._first_frame_logged = True
                log_message(f"SkyShader paintGL 首帧: id={self._shader_id}, w={self.width()}, h={self.height()}, ctx={self.context() is not None}", "INFO")
            frame_start = time.perf_counter() if self._auto_degrade else 0
            f = self._funcs
            dpr = self.devicePixelRatio() if hasattr(self, 'devicePixelRatio') else 1.0
            vw = max(1, int(self.width() * dpr))
            vh = max(1, int(self.height() * dpr))
            f.glViewport(0, 0, vw, vh)
            f.glClearColor(0.42, 0.62, 0.82, 1.0)
            f.glClear(0x4000)
            f.glDisable(0x0B71)
            self._prog.bind()
            self._prog.setUniformValue(self._loc_time, float(self._t))
            self._prog.setUniformValue(self._loc_res, float(vw), float(vh))
            qmap = {"ultra": 1.2, "high": 1.0, "medium": 0.7, "low": 0.45}
            self._prog.setUniformValue(self._loc_quality, float(qmap.get(self.quality, 1.0)))
            self._vao.bind()
            f.glDrawArrays(4, 0, 3)
            self._vao.release()
            self._prog.release()
            self._auto_degrade and self._record_frame_cost(time.perf_counter() - frame_start)

        def cleanup(self):
            try:
                if self._vbo is not None:
                    self._vbo.destroy()
                if self._vao is not None:
                    self._vao.destroy()
                if self._prog is not None:
                    self._prog.removeAllShaders()
            except Exception:
                pass

        def closeEvent(self, event):
            self.cleanup()
            super().closeEvent(event)


    class SkyShaderWidget(SkyShaderWindow):
        def __init__(self, parent=None, radius=0):
            super().__init__(parent)
            self.radius = max(0, int(radius))
            self._fallback_check_done = False
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            QTimer.singleShot(300, self._check_init_and_fallback)

        def _check_init_and_fallback(self):
            if self._fallback_check_done:
                return
            self._fallback_check_done = True
            if not self._init_ok:
                err = getattr(self, '_init_error', '未知错误')
                log_message(f"SkyShader GL 初始化失败，触发回退 (原因: {err})", "ERROR")
                parent = self.parent()
                if parent is not None:
                    QTimer.singleShot(0, lambda: parent._fallback_to_cpu_dynamic_bg("sky"))
            else:
                log_message(f"SkyShaderWidget 回退检查通过: init_ok={self._init_ok}", "INFO")

        def set_radius(self, radius):
            self.radius = max(0, int(radius))
            self._apply_mask()

        def _apply_mask(self):
            if self.radius > 0:
                from PyQt6.QtGui import QRegion
                path = QPainterPath()
                path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), self.radius, self.radius)
                region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
                self.setMask(region)
            else:
                self.clearMask()

        def trigger_click(self, x, y):
            pass

        def is_init_ok(self):
            return self._init_ok

        def resizeEvent(self, event):
            super().resizeEvent(event)
            self._apply_mask()


class _StaysOnTopComboBox(QComboBox):
    def showPopup(self):
        win = self.window()
        if hasattr(win, 'bg_dynamic_widget') and win.bg_dynamic_widget:
            gl_w = win.bg_dynamic_widget
            if hasattr(gl_w, '_timer') and gl_w._timer.isActive():
                gl_w._timer.stop()
                self._gl_timer_was_active = True
            else:
                self._gl_timer_was_active = False
        super().showPopup()

    def hidePopup(self):
        super().hidePopup()
        if getattr(self, '_gl_timer_was_active', False):
            win = self.window()
            if hasattr(win, 'bg_dynamic_widget') and win.bg_dynamic_widget:
                gl_w = win.bg_dynamic_widget
                if hasattr(gl_w, '_timer') and gl_w.isVisible():
                    gl_w._timer.start(1000 // max(getattr(gl_w, 'fps', 60), 15))

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            if not self.view().isVisible():
                self.showPopup()
            else:
                if key == Qt.Key.Key_Up:
                    self.setCurrentIndex(max(0, self.currentIndex() - 1))
                else:
                    self.setCurrentIndex(min(self.count() - 1, self.currentIndex() + 1))
        else:
            super().keyPressEvent(event)


class SkyPresetDialog(QDialog):
    SKY_PRESETS = [
        ('ultra', '最高画质', '云层光线步进 72 步 + 7 步光阴影 + god rays 丁达尔光 + 强 bloom 泛光 + 梦幻雾气', '推荐 RTX 3060 / RX 6600 及以上显卡'),
        ('high', '高画质', '云层光线步进 48 步 + 5 步光阴影 + god rays + 中等 bloom + 梦幻雾气', '推荐 GTX 1060 / RX 580 及以上'),
        ('medium', '中等画质', '云层光线步进 32 步 + 4 步光阴影 + 弱 bloom，无 god rays', '推荐 Intel 核显 / MX 系列低端独显'),
        ('low', '低画质', '云层光线步进 24 步 + 3 步光阴影，关闭 god rays / bloom / 雾气', '适合老旧集成显卡'),
    ]
    AURORA_PRESETS = [
        ('ultra', '最高画质', '5 层极光 + 满屏帘幕 + fbm 噪声边缘 + 强 bloom 泛光 + 星云纹理', '推荐 RTX 3060 / RX 6600 及以上显卡'),
        ('high', '高画质', '5 层极光 + 满屏帘幕 + fbm 噪声边缘 + 中等 bloom', '推荐 GTX 1060 / RX 580 及以上'),
        ('medium', '中等画质', '5 层极光 + 简化帘幕 + 弱 bloom，无星云纹理', '推荐 Intel 核显 / MX 系列低端独显'),
        ('low', '低画质', '3 层极光 + 简化帘幕，关闭 bloom / 星云', '适合老旧集成显卡'),
    ]

    def __init__(self, parent=None, current='high', bg_label='天空'):
        super().__init__(parent)
        self._bg_label = bg_label
        self.setWindowTitle(f'{bg_label}背景 · 画质选择')
        self.setModal(True)
        self.result_preset = current
        dark = is_system_dark()
        tc = {
            'bg': '#1E1E24' if dark else '#F5F5F5',
            'text': '#E8E8E8' if dark else '#1D1D1F',
            'hint': '#9AA0A6' if dark else '#666666',
            'sub': '#6B7280' if dark else '#888888',
            'cancel_bg': '#3A3A3A' if dark else '#D0D0D0',
            'cancel_text': 'white' if dark else '#333333',
        }
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)
        title = QLabel(f'选择{bg_label}背景渲染画质')
        title.setStyleSheet(f'font-size:15px;font-weight:bold;color:{tc["text"]};')
        layout.addWidget(title)
        is_aurora = bg_label == '极光'
        hint_text = ('不同画质影响极光帘幕层数、fbm 噪声、bloom 泛光等特效。\n若运行卡顿请降档；随时可在右下角设置区切换。'
                     if is_aurora else
                     '不同画质影响云层光线步进、光阴影、god rays 与 bloom 泛光等特效。\n若运行卡顿请降档；随时可在右下角设置区切换。')
        hint = QLabel(hint_text)
        hint.setWordWrap(True)
        hint.setStyleSheet(f'color:{tc["hint"]};font-size:11px;')
        layout.addWidget(hint)
        presets = self.AURORA_PRESETS if is_aurora else self.SKY_PRESETS
        self._buttons = []
        for key, name, desc, hw in presets:
            btn = QRadioButton(f'{name}　—　{desc}')
            btn.setStyleSheet(f'color:{tc["text"]};font-size:12px;padding:4px;')
            btn.toggled.connect(lambda checked, k=key: self._on_toggled(checked, k))
            hw_lbl = QLabel(f'　　{hw}')
            hw_lbl.setStyleSheet(f'color:{tc["sub"]};font-size:10px;padding-left:20px;')
            layout.addWidget(btn)
            layout.addWidget(hw_lbl)
            self._buttons.append((btn, key))
        for btn, key in self._buttons:
            if key == current:
                btn.setChecked(True)
                break
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        ok_btn = QPushButton('确定')
        ok_btn.setStyleSheet('background:#3498db;color:white;border-radius:4px;padding:6px 18px;')
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton('取消')
        cancel_btn.setStyleSheet(f'background:{tc["cancel_bg"]};color:{tc["cancel_text"]};border-radius:4px;padding:6px 18px;')
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)
        self.setStyleSheet(f'background-color:{tc["bg"]};')

    def _on_toggled(self, checked, key):
        if checked:
            self.result_preset = key


class FullscreenSettingsPanel(QWidget):
    def __init__(self, parent=None, window=None):
        super().__init__(parent)
        self.window = window
        self.setFixedWidth(300)
        self.setObjectName("FullscreenPanel")
        _dark = is_system_dark()
        _panel_bg = "rgba(25, 25, 30, 220)" if _dark else "rgba(255, 255, 255, 235)"
        _panel_border = "rgba(255, 255, 255, 40)" if _dark else "rgba(0, 0, 0, 35)"
        _label_color = "#E0E0E0" if _dark else "#1D1D1F"
        _groove_bg = "#3A3A3A" if _dark else "#D0D0D0"
        _combo_bg = "#3A3A3A" if _dark else "#F3F3F3"
        _combo_text = "white" if _dark else "#1D1D1F"
        self.setStyleSheet(f"""
            #FullscreenPanel {{
                background-color: {_panel_bg};
                border-radius: 12px;
                border: 1px solid {_panel_border};
            }}
            QLabel {{ color: {_label_color}; font-weight: bold; font-family: 'Microsoft YaHei'; }}
            QSlider::groove:horizontal {{ border-radius: 4px; height: 8px; background: {_groove_bg}; }}
            QSlider::handle:horizontal {{ background: #3498db; width: 16px; height: 16px; margin: -4px 0; border-radius: 8px; }}
            QComboBox {{ background-color: {_combo_bg}; color: {_combo_text}; border-radius: 4px; padding: 4px; }}
            QComboBox QAbstractItemView {{ background-color: {_combo_bg}; color: {_combo_text}; selection-background-color: #3498db; selection-color: white; }}
            QPushButton {{ background-color: #e74c3c; color: white; border-radius: 6px; padding: 8px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #c0392b; }}
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
        self.combo_type = _StaysOnTopComboBox()
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
        hint_lbl = QLabel("↑ ↓ 键切换背景选项")
        hint_lbl.setStyleSheet("color: #6B7280; font-size: 9pt; font-weight: normal;")
        layout.addWidget(hint_lbl)
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel(tr("fps") + ":"))
        self.combo_fps = _StaysOnTopComboBox()
        self.combo_fps.addItems(["30 FPS", "60 FPS", "120 FPS"])
        self.combo_fps.setCurrentText(f"{self.window.project.dynamic_fps} FPS")
        self.combo_fps.currentIndexChanged.connect(self.on_fps_changed)
        fps_layout.addWidget(self.combo_fps)
        layout.addLayout(fps_layout)
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("画面设置:"))
        self.combo_preset = _StaysOnTopComboBox()
        self.combo_preset.addItems(["最高", "高", "中", "低"])
        curr_preset = getattr(self.window.project, 'graphics_preset', 'high')
        pmap = {'ultra': 0, 'high': 1, 'medium': 2, 'low': 3}
        self.combo_preset.setCurrentIndex(pmap.get(curr_preset, 1))
        self.combo_preset.currentIndexChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.combo_preset)
        layout.addLayout(preset_layout)
        engine_lay = QHBoxLayout()
        engine_lay.addWidget(QLabel("渲染器:"))
        self.lbl_render = QLabel("检测中…")
        self.lbl_render.setStyleSheet("color: #f39c12; font-size: 10pt; font-weight: normal;")
        self.lab_engine_icon = QLabel("🔧")
        self.lab_engine_icon.setStyleSheet("font-size: 12pt;")
        engine_lay.addWidget(self.lbl_render)
        engine_lay.addStretch()
        engine_lay.addWidget(self.lab_engine_icon)
        layout.addLayout(engine_lay)
        self._refresh_render_label()
        QTimer.singleShot(700, self._refresh_render_label)
        QTimer.singleShot(1500, self._refresh_render_label)
        QTimer.singleShot(3000, self._refresh_render_label)
        btn_layout_editor = QPushButton("全屏布局编辑器")
        btn_layout_editor.setCursor(Qt.CursorShape.PointingHandCursor)
        _le_bg = "#2c3e50" if is_system_dark() else "#3498db"
        _le_hover = "#34495e" if is_system_dark() else "#2980b9"
        btn_layout_editor.setStyleSheet(f"""
            QPushButton {{ background-color: {_le_bg}; color: white; border-radius: 6px; padding: 8px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {_le_hover}; }}
        """)
        btn_layout_editor.clicked.connect(self.open_fullscreen_layout_editor)
        layout.addWidget(btn_layout_editor)
        btn_exit = QPushButton(tr("exit_fullscreen"))
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.clicked.connect(self.window.toggle_fullscreen)
        layout.addWidget(btn_exit)
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(7000)
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
        self._refresh_render_label()
        super().enterEvent(event)

    def _refresh_render_label(self):
        if not hasattr(self, 'lab_engine_icon') or not hasattr(self, 'lbl_render'):
            return
        renderer_name = "CPU 渲染"
        is_gpu = False
        is_pending = False
        try:
            bg_widget = getattr(self.window, 'bg_dynamic_widget', None)
            if bg_widget is not None:
                has_init_flag = hasattr(bg_widget, '_init_ok')
                if has_init_flag:
                    init_ok = getattr(bg_widget, '_init_ok', False)
                    if init_ok:
                        rn = getattr(bg_widget, '_renderer_name', None)
                        if rn:
                            renderer_name = rn
                            for suffix in ('/PCIe/SSE2', '/PCIe', '/SSE2'):
                                if renderer_name.endswith(suffix):
                                    renderer_name = renderer_name[:-len(suffix)]
                                    break
                            is_gpu = True
                        else:
                            renderer_name = "GPU 着色器"
                            is_gpu = True
                    elif getattr(bg_widget, '_init_error', None):
                        renderer_name = "GPU 初始化失败 → CPU"
                    else:
                        renderer_name = "检测中…"
                        is_pending = True
                else:
                    renderer_name = "CPU 渲染"
                    is_gpu = False
        except Exception:
            pass
        self.lbl_render.setText(renderer_name)
        self.lbl_render.setToolTip(renderer_name)
        if is_gpu:
            color = '#2ecc71'
        elif is_pending:
            color = '#95a5a6'
        else:
            color = '#f39c12'
        self.lbl_render.setStyleSheet(f"color: {color}; font-size: 10pt; font-weight: normal;")
        self.lab_engine_icon.setText("⚡" if is_gpu else ("⏳" if is_pending else "🔧"))

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
        prev_bg = getattr(self.window, 'temp_fullscreen_bg', None) or getattr(self.window.project, 'dynamic_bg_type', 'particles')
        if bg_type in ("aurora", "sky"):
            gpu_on = getattr(getattr(self.window, 'master', None), 'enable_gpu_acceleration', False)
            if not gpu_on:
                ret = QMessageBox.warning(self, "需要 GPU 加速",
                    f"「{'极光' if bg_type == 'aurora' else '天空'}」为高渲染动态背景，未开启 GPU 着色器加速时将使用 CPU 渲染，CPU 占用高且可能卡顿。\n\n是否现在开启 GPU 加速？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
                if ret == QMessageBox.StandardButton.Yes:
                    self.window.master.enable_gpu_acceleration = True
                    self.window.master.save_config(force=True)
                    if hasattr(self.window.master, 'chk_gpu_accel'):
                        self.window.master.chk_gpu_accel.setChecked(True)
                else:
                    log_message(f"用户在未开启 GPU 加速下选择 {bg_type}，将使用 CPU 渲染", "INFO")
            label = '极光' if bg_type == 'aurora' else '天空'
            curr = getattr(self.window.project, 'graphics_preset', 'high')
            dlg = SkyPresetDialog(self, current=curr, bg_label=label)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                preset = dlg.result_preset
                self.window.project.graphics_preset = preset
                self.window.project.dynamic_quality = preset
                try:
                    self.window.master.save_config(force=True)
                except Exception:
                    pass
                idx_map = {'ultra': 0, 'high': 1, 'medium': 2, 'low': 3}
                if hasattr(self, 'combo_preset'):
                    self.combo_preset.blockSignals(True)
                    self.combo_preset.setCurrentIndex(idx_map.get(preset, 1))
                    self.combo_preset.blockSignals(False)
            else:
                for i in range(self.combo_type.count()):
                    if self.combo_type.itemData(i) == prev_bg:
                        self.combo_type.blockSignals(True)
                        self.combo_type.setCurrentIndex(i)
                        self.combo_type.blockSignals(False)
                        break
                return
        self.window.temp_fullscreen_bg = bg_type
        try:
            self.window.setup_dynamic_bg()
        except Exception as e:
            log_message(f"on_wallpaper_type_changed setup_dynamic_bg 异常: {e}", "ERROR")
        if self.window.is_fullscreen:
            try:
                self.window._apply_fullscreen_layout()
            except Exception as e:
                log_message(f"on_wallpaper_type_changed _apply_fullscreen_layout 异常: {e}", "ERROR")
        QTimer.singleShot(1000, self._refresh_render_label)

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

    def on_preset_changed(self, index):
        preset_map = {0: 'ultra', 1: 'high', 2: 'medium', 3: 'low'}
        preset = preset_map.get(index, 'high')
        self.window.project.graphics_preset = preset
        self.window.project.dynamic_quality = preset
        if self.window.bg_dynamic_widget and hasattr(self.window.bg_dynamic_widget, 'set_quality'):
            self.window.bg_dynamic_widget.set_quality(preset)
        try:
            self.window.master.save_config(force=True)
        except Exception:
            pass

    def _render_name(self, backend):
        names = {"auto": "自动", "software": "软件渲染", "opengl": "OpenGL",
                 "vulkan": "Vulkan", "d3d11": "DirectX 11", "d3d12": "DirectX 12", "metal": "Metal"}
        return names.get(backend, backend if backend else "未知")

    def open_fullscreen_layout_editor(self):
        try:
            self.window._pause_dynamic_bg()
            dlg = FullscreenLayoutEditor(self.window.project, self.window, self.window)
            result = dlg.exec()
            self.window._resume_dynamic_bg()
            if result == QDialog.DialogCode.Accepted:
                self.window._apply_fullscreen_layout()
                self.window._update_fullscreen_flip_clock()
                self.window.master.save_config(force=True)
        except Exception as e:
            self.window._resume_dynamic_bg()
            log_message(f"打开全屏布局编辑器失败: {e}", "ERROR")


class WallpaperPreloadThread(QThread):
    pixmap_ready = pyqtSignal(str, QImage)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self._path = path

    def run(self):
        try:
            img = QImage(self._path)
            if not img.isNull():
                self.pixmap_ready.emit(self._path, img)
        except Exception:
            pass


class WallpaperManager(QObject):
    wallpaper_changed = pyqtSignal()

    def __init__(self, app=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.wallpapers = []
        self.enabled = False
        self.mode = "loop"
        self.interval = 60
        self.fill_mode = "fit"
        self.fade = False
        self.dual_screen = False
        self.screen_target = "main"
        self.current_index = 0
        self._preloaded_pixmap = None
        self._preloaded_path = None
        self._preload_thread = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_wallpaper)

    def add_wallpaper(self, path):
        if path and os.path.exists(path) and path not in self.wallpapers:
            self.wallpapers.append(path)
            self._preload_next()
            self.wallpaper_changed.emit()

    def remove_wallpaper(self, index):
        if 0 <= index < len(self.wallpapers):
            self.wallpapers.pop(index)
            if self.current_index >= len(self.wallpapers):
                self.current_index = max(0, len(self.wallpapers) - 1)
            self._preload_next()
            self.wallpaper_changed.emit()

    def move_up(self, index):
        if 0 < index < len(self.wallpapers):
            self.wallpapers[index], self.wallpapers[index - 1] = self.wallpapers[index - 1], self.wallpapers[index]
            if self.current_index == index:
                self.current_index = index - 1
            elif self.current_index == index - 1:
                self.current_index = index
            self._preload_next()
            self.wallpaper_changed.emit()

    def move_down(self, index):
        if 0 <= index < len(self.wallpapers) - 1:
            self.wallpapers[index], self.wallpapers[index + 1] = self.wallpapers[index + 1], self.wallpapers[index]
            if self.current_index == index:
                self.current_index = index + 1
            elif self.current_index == index + 1:
                self.current_index = index
            self._preload_next()
            self.wallpaper_changed.emit()

    def get_current_wallpaper(self):
        if not self.wallpapers:
            return None
        if self.current_index >= len(self.wallpapers):
            self.current_index = 0
        return self.wallpapers[self.current_index]

    def get_current_pixmap(self):
        path = self.get_current_wallpaper()
        if not path:
            return None
        if self._preloaded_pixmap is not None and not self._preloaded_pixmap.isNull() \
                and path == self._preloaded_path:
            return self._preloaded_pixmap
        pm = QPixmap(path)
        if pm.isNull():
            return None
        return pm

    def next_wallpaper(self):
        if not self.wallpapers:
            return
        if len(self.wallpapers) == 1:
            self.current_index = 0
            self.wallpaper_changed.emit()
            if self.enabled:
                self.apply_to_desktop()
            return
        if self.mode == "random":
            new_index = self.current_index
            while new_index == self.current_index:
                new_index = random.randint(0, len(self.wallpapers) - 1)
            self.current_index = new_index
        else:
            self.current_index = (self.current_index + 1) % len(self.wallpapers)
        self._preload_next()
        self.wallpaper_changed.emit()
        if self.enabled:
            self.apply_to_desktop()

    def _preload_next(self):
        if not self.wallpapers:
            self._preloaded_pixmap = None
            self._preloaded_path = None
            return
        next_idx = (self.current_index + 1) % len(self.wallpapers)
        path = self.wallpapers[next_idx]
        if self._preload_thread is not None:
            try:
                self._preload_thread.pixmap_ready.disconnect()
            except Exception:
                pass
        self._preload_thread = WallpaperPreloadThread(path, self)
        self._preload_thread.pixmap_ready.connect(self._on_pixmap_ready)
        self._preload_thread.start()

    def _on_pixmap_ready(self, path, image):
        if image is None or image.isNull():
            self._preloaded_pixmap = None
            self._preloaded_path = None
            return
        pm = QPixmap.fromImage(image)
        if pm.isNull():
            self._preloaded_pixmap = None
            self._preloaded_path = None
            return
        self._preloaded_pixmap = pm
        self._preloaded_path = path

    def start_slideshow(self):
        if self.enabled and self.wallpapers and self.interval > 0:
            self.timer.start(self.interval * 1000)
        else:
            self.timer.stop()

    def stop_slideshow(self):
        self.timer.stop()

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)
        if self.enabled:
            self.start_slideshow()
        else:
            self.stop_slideshow()

    def apply_to_desktop(self):
        path = self.get_current_wallpaper()
        if not path:
            return False
        try:
            if sys.platform == "win32":
                SPI_SETDESKWALLPAPER = 20
                SPIF_UPDATEINIFILE = 0x01
                SPIF_SENDWININICHANGE = 0x02
                result = ctypes.windll.user32.SystemParametersInfoW(
                    SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
                return bool(result)
            elif sys.platform == "darwin":
                script = f'tell application "System Events" to set picture of every desktop to "{path}"'
                subprocess.run(["osascript", "-e", script], check=False)
                return True
            else:
                try:
                    subprocess.run(["feh", "--bg-fill", path], check=False)
                except FileNotFoundError:
                    subprocess.run([
                        "gsettings", "set", "org.gnome.desktop.background",
                        "picture-uri", f"file://{path}"
                    ], check=False)
                return True
        except Exception as e:
            log_message(f"应用桌面壁纸失败: {e}", "ERROR")
            return False

    def load_config(self, config_dict):
        if not config_dict:
            return
        self.wallpapers = list(config_dict.get("wallpapers", []))
        self.enabled = bool(config_dict.get("enabled", False))
        self.mode = config_dict.get("mode", "loop")
        self.interval = int(config_dict.get("interval", 60))
        self.fill_mode = config_dict.get("fill_mode", "fit")
        self.fade = bool(config_dict.get("fade", False))
        self.dual_screen = bool(config_dict.get("dual_screen", False))
        self.screen_target = config_dict.get("screen_target", "main")
        self.current_index = int(config_dict.get("current_index", 0))
        if self.current_index >= len(self.wallpapers):
            self.current_index = 0
        self._preload_next()
        if self.enabled:
            self.start_slideshow()

    def save_config(self):
        return {
            "wallpapers": list(self.wallpapers),
            "enabled": self.enabled,
            "mode": self.mode,
            "interval": self.interval,
            "fill_mode": self.fill_mode,
            "fade": self.fade,
            "dual_screen": self.dual_screen,
            "screen_target": self.screen_target,
            "current_index": self.current_index,
        }


class SlideshowWallpaperWidget(QWidget):
    def __init__(self, parent=None, manager=None, radius=0):
        super().__init__(parent)
        self.manager = manager
        self.radius = max(0, int(radius))
        self.current_pixmap = None
        self._prev_pixmap = None
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._load_current()
        if self.manager is not None:
            try:
                self.manager.wallpaper_changed.connect(self._on_wallpaper_changed)
            except Exception:
                pass
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(500)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def set_radius(self, radius):
        self.radius = max(0, int(radius))
        self.update()

    def _load_current(self):
        if self.manager is None:
            return
        path = self.manager.get_current_wallpaper()
        if path:
            pm = self.manager.get_current_pixmap()
            if pm is not None and not pm.isNull():
                self.current_pixmap = pm
                self.update()
                return
        self.current_pixmap = None

    def _on_wallpaper_changed(self):
        if self.manager is not None and self.manager.fade and self.current_pixmap is not None:
            self._prev_pixmap = self.current_pixmap
            try:
                self._fade_anim.stop()
                self._fade_anim.setStartValue(1.0)
                self._fade_anim.setEndValue(0.0)
                self._fade_anim.finished.connect(self._on_fade_out_done, Qt.ConnectionType.UniqueConnection)
                self._fade_anim.start()
                return
            except Exception:
                self._prev_pixmap = None
        self._load_current()

    def _on_fade_out_done(self):
        try:
            self._fade_anim.finished.disconnect(self._on_fade_out_done)
        except Exception:
            pass
        self._load_current()
        try:
            self._fade_anim.setStartValue(0.0)
            self._fade_anim.setEndValue(1.0)
            self._fade_anim.start()
        except Exception:
            pass

    def paintEvent(self, event):
        if self.current_pixmap is None or self.current_pixmap.isNull():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
        painter.setClipPath(path)
        pm = self.current_pixmap
        fill = self.manager.fill_mode if self.manager is not None else "fit"
        if fill == "stretch":
            painter.drawPixmap(self.rect(), pm.scaled(
                self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        elif fill == "fit":
            scaled = pm.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        elif fill == "center":
            x = (self.width() - pm.width()) // 2
            y = (self.height() - pm.height()) // 2
            painter.drawPixmap(x, y, pm)
        elif fill == "tile":
            painter.drawTiledPixmap(self.rect(), pm)
        else:
            painter.drawPixmap(self.rect(), pm)


def ensure_ding_sound(data_dir):
    path = os.path.join(data_dir, "ding.wav")
    if os.path.exists(path):
        return path
    try:
        import wave
        import struct
        sample_rate = 44100
        duration = 0.6
        n = int(sample_rate * duration)
        frames = []
        for i in range(n):
            t = i / sample_rate
            env = math.exp(-3.5 * t)
            s = env * (math.sin(2 * math.pi * 880 * t)
                       + 0.5 * math.sin(2 * math.pi * 1320 * t)
                       + 0.25 * math.sin(2 * math.pi * 1760 * t))
            frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        return path
    except Exception as e:
        log_message(f"生成提示音失败: {e}", "ERROR")
        return None


def play_ding_sound(data_dir):
    if sys.platform != "win32":
        return
    try:
        path = ensure_ding_sound(data_dir)
        if path and os.path.exists(path):
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception as e:
        log_message(f"播放提示音失败: {e}", "ERROR")


def _generate_piano_sound(path):
    import wave
    import struct
    sample_rate = 44100
    duration = 1.2
    n = int(sample_rate * duration)
    fundamental = 523.25
    frames = []
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-2.8 * t)
        s = env * (
            math.sin(2 * math.pi * fundamental * t)
            + 0.6 * math.sin(2 * math.pi * 2 * fundamental * t)
            + 0.4 * math.sin(2 * math.pi * 3 * fundamental * t)
            + 0.2 * math.sin(2 * math.pi * 4 * fundamental * t)
        )
        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_double_ding_sound(path):
    import wave
    import struct
    sample_rate = 44100
    ding_dur = 0.20
    gap_dur = 0.18
    total_dur = ding_dur * 2 + gap_dur
    n = int(sample_rate * total_dur)
    freq1 = 1175.0
    freq2 = 1480.0
    frames = []
    for i in range(n):
        t = i / sample_rate
        if t < ding_dur:
            local_t = t
            env = math.exp(-10.0 * local_t) * (1.0 + 0.15 * math.sin(2 * math.pi * 18 * local_t))
            s = env * (0.7 * math.sin(2 * math.pi * freq1 * local_t)
                       + 0.35 * math.sin(2 * math.pi * 2 * freq1 * local_t)
                       + 0.15 * math.sin(2 * math.pi * 3 * freq1 * local_t))
        elif t < ding_dur + gap_dur:
            s = 0.0
        else:
            local_t = t - ding_dur - gap_dur
            env = math.exp(-10.0 * local_t) * (1.0 + 0.15 * math.sin(2 * math.pi * 18 * local_t))
            s = env * (0.7 * math.sin(2 * math.pi * freq2 * local_t)
                       + 0.35 * math.sin(2 * math.pi * 2 * freq2 * local_t)
                       + 0.15 * math.sin(2 * math.pi * 3 * freq2 * local_t))
        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_urgent_beep_sound(path):
    import wave
    import struct
    sample_rate = 44100
    beep_dur = 0.06
    gap_dur = 0.04
    n_beeps = 6
    total_dur = beep_dur * n_beeps + gap_dur * (n_beeps - 1)
    n = int(sample_rate * total_dur)
    freqs = [1200.0, 1400.0, 1600.0, 1400.0, 1600.0, 1800.0]
    cycle = beep_dur + gap_dur
    frames = []
    for i in range(n):
        t = i / sample_rate
        cycle_pos = t % cycle
        beep_idx = int(t / cycle)
        if beep_idx >= n_beeps or cycle_pos >= beep_dur:
            s = 0.0
        else:
            local_t = cycle_pos
            freq = freqs[beep_idx] if beep_idx < len(freqs) else 1400.0
            if local_t < 0.003:
                env = local_t / 0.003
            elif local_t > beep_dur - 0.003:
                env = (beep_dur - local_t) / 0.003
            else:
                env = 1.0
            pulse = 0.65 * math.copysign(1.0, math.sin(2 * math.pi * freq * local_t))
            s = env * pulse
        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_windchime_sound(path):
    import wave
    import struct
    import random
    sample_rate = 44100
    duration = 4.2
    n = int(sample_rate * duration)

    base_freqs = [1046.5, 1174.7, 1318.5, 1396.9, 1568.0, 1760.0, 1975.5, 2093.0, 2349.3, 2637.0]

    chimes = []
    rng = random.Random(42)
    for idx, freq in enumerate(base_freqs):
        base_delay = 0.0
        if idx == 0:
            base_delay = 0.0
        elif idx <= 3:
            base_delay = rng.uniform(0.08, 0.22) * (idx)
        elif idx <= 6:
            base_delay = 0.4 + rng.uniform(0.2, 0.45) * (idx - 3)
        else:
            base_delay = 1.5 + rng.uniform(0.3, 0.6) * (idx - 6)
        freq_offset = rng.uniform(-8.0, 8.0)
        freq_actual = freq + freq_offset

        base_decay = 1.8 if freq > 2000 else 2.5 if freq > 1500 else 3.2
        decay = base_decay + rng.uniform(-0.3, 0.3)

        amp = (0.22 - idx * 0.016) * (0.8 if freq > 2000 else 1.0)
        amp = max(0.06, amp)

        chimes.append({
            'freq': freq_actual,
            'delay': base_delay,
            'decay': decay,
            'amp': amp,
            'overtones': [
                (1.0, 1.0),
                (2.76, 0.40),
                (5.40, 0.18),
                (8.93, 0.08),
            ],
            'detune': [rng.uniform(-3.0, 3.0) for _ in range(4)],
        })

    frames = []
    for i in range(n):
        t = i / sample_rate
        s = 0.0
        for ch in chimes:
            local_t = t - ch['delay']
            if local_t < 0:
                continue
            if local_t < 0.008:
                attack_env = local_t / 0.008
            else:
                attack_env = 1.0

            chime_s = 0.0
            for k, (ratio, coeff) in enumerate(ch['overtones']):
                overtone_freq = ch['freq'] * ratio + ch['detune'][k]
                overtone_decay = ch['decay'] * (1.0 + 0.7 * ratio)
                decays_per_sample = math.exp(-overtone_decay * local_t)
                drift = 1.0 - 0.0003 * local_t * overtone_freq / 1000.0
                sine = math.sin(2 * math.pi * overtone_freq * local_t * drift)
                chime_s += coeff * decays_per_sample * sine

            s += ch['amp'] * attack_env * chime_s

        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_long_buzz_sound(path):
    import wave
    import struct
    sample_rate = 44100
    duration = 1.8
    n = int(sample_rate * duration)
    freq = 260.0
    attack = 0.04
    release = 0.25
    frames = []
    for i in range(n):
        t = i / sample_rate
        if t < attack:
            env = t / attack
        elif t > duration - release:
            env = max(0.0, (duration - t) / release)
        else:
            env = 1.0
        square = math.copysign(1.0, math.sin(2 * math.pi * freq * t))
        tremolo = 1.0 + 0.08 * math.sin(2 * math.pi * 4.5 * t)
        s = env * tremolo * (0.6 * square + 0.2 * math.sin(2 * math.pi * freq * 2 * t))
        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_alarm_sound(path):
    import wave
    import struct
    sample_rate = 44100
    duration = 2.6
    n = int(sample_rate * duration)

    base_notes = [
        (523.25, 0.28),   # C5
        (659.25, 0.22),   # E5
        (783.99, 0.20),   # G5
        (1046.5, 0.18),   # C6
        (783.99, 0.18),   # G5
        (659.25, 0.16),   # E5
        (523.25, 0.16),   # C5
        (1046.5, 0.14),   # C6
        (783.99, 0.14),   # G5
        (1046.5, 0.12),   # C6
    ]
    cum_times = [0.0]
    for _, w in base_notes[:-1]:
        cum_times.append(cum_times[-1] + w)

    frames = []
    for i in range(n):
        t = i / sample_rate

        global_env = min(1.0, (t / duration) ** 0.5)

        s = 0.0
        for idx, (freq, _) in enumerate(base_notes):
            start_t = cum_times[idx]
            local_t = t - start_t
            if local_t < 0 or local_t > 0.45:
                continue

            attack = 0.012
            if local_t < attack:
                note_env = local_t / attack
            else:
                decay = 5.0 + 1.5 * idx
                note_env = math.exp(-decay * (local_t - attack))

            harmonics = (
                1.0 * math.sin(2 * math.pi * freq * local_t)
                + 0.45 * math.sin(2 * math.pi * freq * 2.0 * local_t)
                + 0.22 * math.sin(2 * math.pi * freq * 3.0 * local_t)
                + 0.10 * math.sin(2 * math.pi * freq * 4.0 * local_t)
                + 0.05 * math.sin(2 * math.pi * freq * 6.0 * local_t)
            )

            weight = base_notes[idx][1] / 0.28
            s += weight * note_env * harmonics

        s *= global_env * 0.55

        s *= 1.0 + 0.025 * math.sin(2 * math.pi * 4.8 * t)

        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_wave_sound(path):
    import wave
    import struct
    import random
    sample_rate = 44100
    duration = 3.5
    n = int(sample_rate * duration)

    rng = random.Random(98765)

    noise1 = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    noise2 = [rng.uniform(-0.6, 0.6) for _ in range(n)]
    noise3 = [rng.uniform(-0.5, 0.5) for _ in range(n)]

    frames = []
    lp1 = lp2 = lp3 = 0.0

    for i in range(n):
        t = i / sample_rate

        tide1 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.28 * t)
        tide2 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.45 * t + 0.8)
        breaker_env = 0.5 + 0.5 * math.sin(2 * math.pi * 1.3 * t)
        breaker_env *= 0.3 + 0.2 * math.sin(2 * math.pi * 0.55 * t)

        main_env = 0.55 * tide1 + 0.25 * tide2 + 0.12 * breaker_env

        alpha1 = 0.025
        lp1 = lp1 + alpha1 * (noise1[i] * 0.9 - lp1)

        alpha2 = 0.08
        lp2 = lp2 + alpha2 * (noise2[i] * 0.7 - lp2)
        wash_env = 0.3 + 0.7 * max(0, tide1 - 0.3)

        alpha3 = 0.25
        lp3 = lp3 + alpha3 * (noise3[i] * 0.4 - lp3)
        foam_env = max(0, tide1 - 0.7) * 1.5
        foam_env = min(1.0, foam_env)

        sub_bass = 0.12 * math.sin(2 * math.pi * 0.42 * t) * tide1

        s = (main_env * (lp1 * 0.7 + lp2 * wash_env * 0.35 + sub_bass)
             + foam_env * lp3 * 0.25)

        s *= 1.4

        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def _generate_synth_arp_sound(path):
    import wave
    import struct
    sample_rate = 44100
    duration = 2.2
    n = int(sample_rate * duration)

    # C小调琶音上行
    arp_notes = [261.63, 311.13, 392.0, 523.25, 622.25, 783.99, 1046.5,
                 784.0, 622.25, 523.25, 392.0, 311.13, 261.63]
    note_dur = duration / len(arp_notes)

    frames = []
    for i in range(n):
        t = i / sample_rate
        note_idx = int(t / note_dur)
        if note_idx >= len(arp_notes):
            note_idx = len(arp_notes) - 1
        local_t = t - note_idx * note_dur

        freq = arp_notes[note_idx]

        attack = 0.015
        if local_t < attack:
            env = local_t / attack
        else:
            env = math.exp(-6.0 * (local_t - attack))

        phase = (freq * local_t) % 1.0
        saw = 2.0 * phase - 1.0  # 锯齿波
        square = math.copysign(1.0, math.sin(2 * math.pi * freq * local_t))

        filter_env = min(1.0, t / 0.3)
        brightness = 0.3 + 0.7 * filter_env

        s = env * (0.5 * saw * brightness + 0.3 * square * (1.0 - brightness)
                   + 0.15 * math.sin(2 * math.pi * freq * 1.5 * local_t) * brightness)

        global_env = math.exp(-0.6 * t)
        s *= global_env

        frames.append(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 28000)))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def ensure_sound_assets(data_dir):
    sounds_dir = os.path.join(data_dir, "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    version_file = os.path.join(sounds_dir, "sound_version.txt")
    current_sound_version = 2
    need_regenerate = False
    try:
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                saved_ver = int(f.read().strip())
            if saved_ver < current_sound_version:
                need_regenerate = True
                for fname in ("alarm_rise.wav", "ocean_wave.wav"):
                    fp = os.path.join(sounds_dir, fname)
                    if os.path.exists(fp):
                        os.remove(fp)
        else:
            need_regenerate = True
    except Exception:
        need_regenerate = True

    assets = [
        ("piano_ding.wav", _generate_piano_sound),
        ("double_ding.wav", _generate_double_ding_sound),
        ("urgent_beep.wav", _generate_urgent_beep_sound),
        ("windchime.wav", _generate_windchime_sound),
        ("long_buzz.wav", _generate_long_buzz_sound),
        ("alarm_rise.wav", _generate_alarm_sound),
        ("ocean_wave.wav", _generate_wave_sound),
        ("synth_arp.wav", _generate_synth_arp_sound),
    ]
    for name, gen in assets:
        path = os.path.join(sounds_dir, name)
        if not os.path.exists(path):
            try:
                gen(path)
            except Exception as e:
                log_message(f"生成提示音失败 [{name}]: {e}", "ERROR")

    # 写入声效版本号
    try:
        with open(version_file, "w") as f:
            f.write(str(current_sound_version))
    except Exception:
        pass

    if need_regenerate:
        log_message("声效文件已更新到最新版本", "INFO")
    return sounds_dir


_active_sound_players = []


def play_sound_file(file_path):
    if not file_path or not os.path.exists(file_path):
        log_message(f"提示音文件不存在: {file_path}", "WARNING")
        return
    try:
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        player.setSource(QUrl.fromLocalFile(file_path))
        audio_output.setVolume(0.9)
        player.play()
        _active_sound_players.append(player)

        def _cleanup(*_args):
            try:
                player.stop()
                audio_output.deleteLater()
                player.deleteLater()
            except Exception:
                pass
            try:
                _active_sound_players.remove(player)
            except ValueError:
                pass

        player.mediaStatusChanged.connect(
            lambda st: _cleanup() if st == QMediaPlayer.MediaStatus.EndOfMedia else None
        )
        QTimer.singleShot(5000, _cleanup)
    except Exception as e:
        log_message(f"播放提示音失败: {e}", "ERROR")


class FlipDigit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = "0"
        self._old_value = "0"
        self._flip = 1.0
        self._color = "#F5F5F5"
        self._card_color = QColor(45, 45, 55)
        self._card_highlight = QColor(65, 65, 80)
        self._card_shadow = QColor(25, 25, 35)
        self._anim = QPropertyAnimation(self, b"flip", self)
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.setMinimumSize(50, 90)

    def get_flip(self):
        return self._flip

    def set_flip(self, v):
        self._flip = v
        self.update()

    flip = pyqtProperty(float, get_flip, set_flip)

    def setColor(self, color):
        self._color = color
        self.update()

    def setCardColor(self, color):
        if isinstance(color, str):
            self._card_color = QColor(color)
        else:
            self._card_color = QColor(color)
        self._card_highlight = QColor(
            min(255, self._card_color.red() + 20),
            min(255, self._card_color.green() + 20),
            min(255, self._card_color.blue() + 25))
        self._card_shadow = QColor(
            max(0, self._card_color.red() - 20),
            max(0, self._card_color.green() - 20),
            max(0, self._card_color.blue() - 20))
        self.update()

    def setValue(self, new_val):
        new_val = str(new_val)
        if new_val == self._value:
            return
        self._old_value = self._value
        self._value = new_val
        self._flip = 0.0
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def _draw_text(self, painter, val, w, h):
        font = QFont("Microsoft YaHei")
        font.setPixelSize(int(h * 0.68))
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(self._color))
        painter.drawText(QRectF(0, 0, w, h), Qt.AlignmentFlag.AlignCenter, val)

    def _draw_card_bg(self, painter, w, h):
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(self._card_color)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 8, 8)

        grad = QLinearGradient(0, 0, 0, h * 0.3)
        grad.setColorAt(0.0, QColor(255, 255, 255, 25))
        grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(grad)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 8, 8)

        grad2 = QLinearGradient(0, h * 0.7, 0, h - 1)
        grad2.setColorAt(0.0, QColor(0, 0, 0, 0))
        grad2.setColorAt(1.0, QColor(0, 0, 0, 40))
        painter.setBrush(grad2)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 8, 8)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(0, 0, 0, 60), 1))
        painter.drawRoundedRect(QRectF(1.5, 1.5, w - 3, h - 3), 8, 8)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        w = self.width()
        h = self.height()
        mid = h / 2.0

        self._draw_card_bg(painter, w, h)

        line_grad = QLinearGradient(0, mid, w, mid)
        line_grad.setColorAt(0.0, QColor(0, 0, 0, 0))
        line_grad.setColorAt(0.15, QColor(0, 0, 0, 80))
        line_grad.setColorAt(0.5, QColor(0, 0, 0, 120))
        line_grad.setColorAt(0.85, QColor(0, 0, 0, 80))
        line_grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(QPen(QBrush(line_grad), 1))
        painter.drawLine(QPointF(0, mid), QPointF(w, mid))
        painter.setPen(QPen(QColor(255, 255, 255, 15), 0.5))
        painter.drawLine(QPointF(0, mid + 1), QPointF(w, mid + 1))

        if self._flip >= 1.0:
            self._draw_text(painter, self._value, w, h)
            return

        # ═══════════════════════════════════════════════
        # 第一段
        # ═══════════════════════════════════════════════
        if self._flip < 0.5:
            t = self._flip * 2.0  # 0.0 → 1.0

            painter.save()
            painter.setClipRect(QRectF(0, mid, w, h - mid))
            self._draw_text(painter, self._old_value, w, h)
            painter.restore()

            scale_y = math.cos(t * math.pi / 2.0)
            offset_y = mid * (1.0 - scale_y)

            painter.save()
            painter.setClipRect(QRectF(0, 0, w, mid))
            transform = QTransform()
            transform.translate(w / 2.0, mid)
            transform.scale(1.0, max(0.01, scale_y))
            transform.translate(-w / 2.0, -mid)
            transform.translate(0, -offset_y)
            painter.setTransform(transform)
            self._draw_text(painter, self._old_value, w, h)
            painter.restore()

            if scale_y < 0.98:
                shadow_a = int((1.0 - scale_y) * 160)
                painter.setPen(Qt.PenStyle.NoPen)
                shade = QLinearGradient(0, 0, 0, mid)
                shade.setColorAt(0.0, QColor(0, 0, 0, shadow_a))
                shade.setColorAt(0.6, QColor(0, 0, 0, shadow_a // 2))
                shade.setColorAt(1.0, QColor(0, 0, 0, 0))
                painter.setBrush(shade)
                painter.drawRect(QRectF(0, 0, w, mid))

            if scale_y < 0.15:
                edge_a = int((0.15 - scale_y) / 0.15 * 100)
                painter.setPen(QPen(QColor(0, 0, 0, edge_a), 3))
                painter.drawLine(QPointF(0, mid), QPointF(w, mid))

        # ═══════════════════════════════════════════════
        # 第二段
        # ═══════════════════════════════════════════════
        else:
            t = (self._flip - 0.5) * 2.0  # 0.0 → 1.0

            painter.save()
            painter.setClipRect(QRectF(0, 0, w, mid))
            self._draw_text(painter, self._value, w, h)
            painter.restore()

            scale_y = math.sin(t * math.pi / 2.0)
            offset_y = mid * (1.0 - scale_y)

            painter.save()
            painter.setClipRect(QRectF(0, mid, w, h - mid))
            transform = QTransform()
            transform.translate(w / 2.0, mid)
            transform.scale(1.0, max(0.01, scale_y))
            transform.translate(-w / 2.0, -mid)
            transform.translate(0, offset_y)
            painter.setTransform(transform)
            self._draw_text(painter, self._value, w, h)
            painter.restore()

            if scale_y < 0.98:
                shadow_a = int((1.0 - scale_y) * 160)
                painter.setPen(Qt.PenStyle.NoPen)
                shade = QLinearGradient(0, mid, 0, h)
                shade.setColorAt(0.0, QColor(0, 0, 0, 0))
                shade.setColorAt(0.4, QColor(0, 0, 0, shadow_a // 2))
                shade.setColorAt(1.0, QColor(0, 0, 0, shadow_a))
                painter.setBrush(shade)
                painter.drawRect(QRectF(0, mid, w, h - mid))

            if scale_y < 0.15:
                edge_a = int((0.15 - scale_y) / 0.15 * 100)
                painter.setPen(QPen(QColor(0, 0, 0, edge_a), 3))
                painter.drawLine(QPointF(0, mid), QPointF(w, mid))


class FlipClockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._enable_flip = True
        self._color = "#F5F5F5"
        self._card_color = "#2D2D37"
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self.digits = []
        self.colons = []
        for i in range(6):
            d = FlipDigit(self)
            d.setColor(self._color)
            d.setCardColor(self._card_color)
            self.digits.append(d)
            layout.addWidget(d)
            if i % 2 == 1 and i < 5:
                c = QLabel(":")
                c.setAlignment(Qt.AlignmentFlag.AlignCenter)
                c.setStyleSheet(f"color: {self._color}; font-weight: bold;")
                c.setMinimumWidth(20)
                self.colons.append(c)
                layout.addWidget(c)

    def setEnableFlip(self, enabled):
        self._enable_flip = bool(enabled)

    def setColor(self, color):
        self._color = color
        for d in self.digits:
            d.setColor(color)
        for c in self.colons:
            c.setStyleSheet(f"color: {color}; font-weight: bold;")

    def setCardColor(self, color):
        self._card_color = color
        for d in self.digits:
            d.setCardColor(color)

    def setDigitSize(self, w, h):
        for d in self.digits:
            d.setMinimumSize(w, h)
            d.setMaximumSize(w, h)

    def setTime(self, total_seconds):
        if total_seconds < 0:
            total_seconds = 0
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        text = f"{hours:02d}{minutes:02d}{seconds:02d}"
        for i, ch in enumerate(text):
            if self._enable_flip:
                self.digits[i].setValue(ch)
            else:
                if self.digits[i]._value != ch:
                    self.digits[i]._old_value = self.digits[i]._value
                    self.digits[i]._value = ch
                    self.digits[i]._flip = 1.0
                    self.digits[i].update()


def _pick_condensed_font():
    try:
        families = set(QFontDatabase.families())
    except Exception:
        families = set()
    for name in ["Orbitron", "DIN Condensed", "Bahnschrift Condensed", "Bahnschrift",
                 "Arial Narrow", "Oswald", "Calibri Light"]:
        if name in families:
            return name
    return "Microsoft YaHei"


class BoardingPassWidget(QWidget):
    _bg_pixmap = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = ""
        self._sub_text = ""
        self._total_seconds = 0
        self._expired = False
        self._expired_text = "已到期"
        self._text_color = QColor(40, 50, 70)
        self._sub_color = QColor(90, 120, 160, 220)
        self._accent_color = QColor(120, 180, 240)
        self._poem = ""
        self._load_bg_pixmap()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    @classmethod
    def _load_bg_pixmap(cls):
        if cls._bg_pixmap is not None:
            return
        for ext in (".jpg", ".png"):
            path = resource_path(os.path.join("data", "backgrounds", "boarding_pass" + ext))
            if os.path.exists(path):
                pm = QPixmap(path)
                if not pm.isNull():
                    cls._bg_pixmap = pm
                    return

    def setPoem(self, poem):
        self._poem = poem or ""
        self.update()

    def setContent(self, name, sub_text, total_seconds, expired=False, expired_text="已到期"):
        self._name = name or ""
        self._sub_text = sub_text or ""
        self._total_seconds = max(0, int(total_seconds or 0))
        self._expired = bool(expired)
        self._expired_text = expired_text or "已到期"
        self.update()

    def setColors(self, text_color, sub_color, accent_color):
        if text_color:
            self._text_color = QColor(text_color) if isinstance(text_color, str) else text_color
        if sub_color:
            self._sub_color = QColor(sub_color) if isinstance(sub_color, str) else sub_color
        if accent_color:
            self._accent_color = QColor(accent_color) if isinstance(accent_color, str) else accent_color
        self.update()

    def _format_time(self):
        d = self._total_seconds // 86400
        r = self._total_seconds % 86400
        h = r // 3600
        r %= 3600
        m = r // 60
        s = r % 60
        return (d, h, m, s)

    def _draw_plane_icon(self, painter, cx, cy, size, color):
        painter.save()
        painter.translate(cx, cy)
        sc = size / 24.0
        painter.scale(sc, sc)
        pen = QPen(color, 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.moveTo(0, -10)
        path.cubicTo(2.2, -8, 2.2, -2, 1.2, 0)
        path.lineTo(10, 4)
        path.lineTo(10, 6.2)
        path.lineTo(1.2, 4.2)
        path.lineTo(0.4, 8)
        path.lineTo(3.2, 10)
        path.lineTo(3.2, 11)
        path.lineTo(-3.2, 11)
        path.lineTo(-3.2, 10)
        path.lineTo(-0.4, 8)
        path.lineTo(-1.2, 4.2)
        path.lineTo(-10, 6.2)
        path.lineTo(-10, 4)
        path.lineTo(-1.2, 0)
        path.cubicTo(-2.2, -2, -2.2, -8, 0, -10)
        painter.drawPath(path)
        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        w, h = self.width(), self.height()
        if w < 20 or h < 20:
            return
        radius = 14
        rect = QRectF(1, 1, w - 2, h - 2)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, radius, radius)
        painter.save()
        painter.setClipPath(clip_path)
        if self._bg_pixmap and not self._bg_pixmap.isNull():
            painter.drawPixmap(rect, self._bg_pixmap, QRectF(0, 0, self._bg_pixmap.width(), self._bg_pixmap.height()))
        else:
            grad = QLinearGradient(0, 0, w, h)
            grad.setColorAt(0, QColor(245, 248, 252))
            grad.setColorAt(1, QColor(220, 232, 245))
            painter.fillRect(rect, grad)
        glassGrad = QLinearGradient(0, 0, w, h)
        glassGrad.setColorAt(0, QColor(248, 250, 255, 210))
        glassGrad.setColorAt(0.5, QColor(238, 244, 252, 200))
        glassGrad.setColorAt(1, QColor(228, 238, 250, 205))
        painter.fillRect(rect, glassGrad)
        grad_top = QLinearGradient(0, 0, 0, h * 0.5)
        grad_top.setColorAt(0, QColor(255, 255, 255, 120))
        grad_top.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(rect, grad_top)
        sideGrad = QLinearGradient(0, 0, w, 0)
        sideGrad.setColorAt(0, QColor(255, 228, 195, 28))
        sideGrad.setColorAt(1, QColor(195, 218, 255, 28))
        painter.fillRect(rect, sideGrad)
        painter.restore()

        painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
        painter.setPen(QPen(QColor(120, 150, 190, 80), 1))
        painter.drawRoundedRect(rect.adjusted(1.5, 1.5, -1.5, -1.5), radius - 1, radius - 1)

        tear_x = int(w * 0.44)
        pen = QPen(QColor(120, 140, 170, 140), 1, Qt.PenStyle.DashLine)
        pen.setDashPattern([3, 4])
        painter.setPen(pen)
        painter.drawLine(tear_x, 10, tear_x, h - 10)
        self._draw_plane_icon(painter, tear_x, h / 2, min(20, h * 0.34), QColor(80, 120, 170, 210))

        left_rect = QRectF(14, 6, tear_x - 22, h - 12)
        name_size = max(11, int(h * 0.34))
        sub_size = max(9, int(h * 0.20))
        name_font = QFont("Microsoft YaHei", name_size)
        name_font.setBold(True)
        name_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        painter.setFont(name_font)
        if self._sub_text:
            name_rect = QRectF(left_rect.x(), left_rect.y(), left_rect.width(), left_rect.height() * 0.62)
        else:
            name_rect = QRectF(left_rect.x(), left_rect.y(), left_rect.width(), left_rect.height())
        painter.setPen(QColor(0, 0, 0, 60))
        painter.drawText(QRectF(name_rect.x() + 1, name_rect.y() + 1, name_rect.width(), name_rect.height()),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._name)
        painter.setPen(self._text_color)
        painter.drawText(name_rect,
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._name)

        if self._sub_text:
            sub_font = QFont("Microsoft YaHei", sub_size)
            sub_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            painter.setFont(sub_font)
            painter.setPen(self._sub_color)
            painter.drawText(QRectF(left_rect.x(), left_rect.y() + left_rect.height() * 0.58, left_rect.width(), left_rect.height() * 0.42),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._sub_text)

        right_rect = QRectF(tear_x + 14, 6, w - tear_x - 26, h - 12)
        if self._expired:
            exp_font = QFont("Microsoft YaHei", max(13, int(h * 0.34)))
            exp_font.setBold(True)
            painter.setFont(exp_font)
            painter.setPen(QColor(0, 0, 0, 90))
            painter.drawText(QRectF(right_rect.x() + 1, right_rect.y() + 1, right_rect.width(), right_rect.height()),
                             Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._expired_text)
            painter.setPen(QColor("#e06c75"))
            painter.drawText(right_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._expired_text)
            return

        d_val, h_val, m_val, s_val = self._format_time()
        units = [("天", d_val), ("时", h_val), ("分", m_val), ("秒", s_val)]
        n_blocks = 4
        gap = 3
        avail_w = right_rect.width()
        block_w = (avail_w - gap * (n_blocks - 1)) / n_blocks
        num_size = max(10, int(h * 0.34))
        unit_size = max(6, int(h * 0.13))
        num_font = QFont("Consolas", num_size)
        num_font.setBold(True)
        num_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        unit_font = QFont("Microsoft YaHei", unit_size)
        card_h = right_rect.height() * 0.72
        for idx, (unit, val) in enumerate(units):
            bx = right_rect.x() + idx * (block_w + gap)
            by = right_rect.y()
            card_rect = QRectF(bx, by, block_w, card_h)
            painter.setPen(QPen(QColor(255, 255, 255, 95), 0.8))
            painter.setBrush(QColor(255, 255, 255, 55))
            painter.drawRoundedRect(card_rect, 4, 4)
            painter.setPen(QPen(QColor(120, 150, 200, 40), 0.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(card_rect.adjusted(0.5, 0.5, -0.5, -0.5), 3.5, 3.5)
            painter.setFont(num_font)
            painter.setPen(QColor(0, 0, 0, 70))
            painter.drawText(card_rect.adjusted(0, 1, 1, 1),
                             Qt.AlignmentFlag.AlignCenter, f"{val:02d}")
            painter.setPen(self._text_color)
            painter.drawText(card_rect,
                             Qt.AlignmentFlag.AlignCenter, f"{val:02d}")
            unit_rect = QRectF(bx, card_rect.bottom() + 2, block_w, right_rect.height() - card_h - 2)
            painter.setFont(unit_font)
            painter.setPen(self._sub_color)
            painter.drawText(unit_rect, Qt.AlignmentFlag.AlignCenter, unit)

        if self._poem:
            poem_font = QFont("Microsoft YaHei", max(5, int(h * 0.09)))
            poem_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            painter.setFont(poem_font)
            painter.setPen(QColor(120, 130, 150, 200))
            poem_rect = QRectF(left_rect.x(), h - max(8, int(h * 0.10)) - 4, left_rect.width() * 0.92, max(8, int(h * 0.10)))
            painter.drawText(poem_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._poem)


class FullscreenCountdownWidget(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._total_seconds = 0
        self._expired = False
        self._expired_text = "已到期"
        self._enable_flip = True
        self._color = "#F5F5F5"
        self._card_color = "#2D2D37"
        self._label_color = "#b0b0b0"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)

        clock_widget = QWidget()
        clock_layout = QHBoxLayout(clock_widget)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(8)

        self._digit_groups = []
        self._all_digits = []

        d_group = []
        for _ in range(2):
            d = FlipDigit(self)
            d.setColor(self._color)
            d.setCardColor(self._card_color)
            clock_layout.addWidget(d)
            d_group.append(d)
            self._all_digits.append(d)
        self._digit_groups.append((d_group, None))

        lbl_day = QLabel("天")
        lbl_day.setStyleSheet(f"color: {self._label_color}; font-size: 18pt; font-weight: bold;")
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_layout.addWidget(lbl_day)

        h_group = []
        for _ in range(2):
            d = FlipDigit(self)
            d.setColor(self._color)
            d.setCardColor(self._card_color)
            clock_layout.addWidget(d)
            h_group.append(d)
            self._all_digits.append(d)
        self._digit_groups.append((h_group, None))

        lbl_hour = QLabel("时")
        lbl_hour.setStyleSheet(f"color: {self._label_color}; font-size: 18pt; font-weight: bold;")
        lbl_hour.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_layout.addWidget(lbl_hour)

        m_group = []
        for _ in range(2):
            d = FlipDigit(self)
            d.setColor(self._color)
            d.setCardColor(self._card_color)
            clock_layout.addWidget(d)
            m_group.append(d)
            self._all_digits.append(d)
        self._digit_groups.append((m_group, None))

        lbl_min = QLabel("分")
        lbl_min.setStyleSheet(f"color: {self._label_color}; font-size: 18pt; font-weight: bold;")
        lbl_min.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_layout.addWidget(lbl_min)

        s_group = []
        for _ in range(2):
            d = FlipDigit(self)
            d.setColor(self._color)
            d.setCardColor(self._card_color)
            clock_layout.addWidget(d)
            s_group.append(d)
            self._all_digits.append(d)
        self._digit_groups.append((s_group, None))

        lbl_sec = QLabel("秒")
        lbl_sec.setStyleSheet(f"color: {self._label_color}; font-size: 18pt; font-weight: bold;")
        lbl_sec.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_layout.addWidget(lbl_sec)

        clock_layout.addStretch()
        outer.addStretch()
        outer.addWidget(clock_widget, 0, Qt.AlignmentFlag.AlignCenter)
        outer.addStretch()

        self._blink_enabled = True
        self._blink_visible = True
        self._blink_interval = 500
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._tick_blink)

        self._expired_label = QLabel("", self)
        self._expired_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._expired_label.setStyleSheet("color: #e06c75; font-size: 36pt; font-weight: bold;")
        self._expired_label.hide()

    def setEnableFlip(self, enabled):
        self._enable_flip = bool(enabled)

    def setColor(self, color):
        self._color = color
        for d in self._all_digits:
            d.setColor(color)

    def setCardColor(self, color):
        self._card_color = color
        for d in self._all_digits:
            d.setCardColor(color)

    def setDigitSize(self, w, h):
        for d in self._all_digits:
            d.setMinimumSize(w, h)
            d.setMaximumSize(w, h)

    def showExpired(self, text="已到期"):
        self._expired = True
        self._expired_text = text
        self._expired_label.setText(text)
        self._expired_label.show()
        for d in self._all_digits:
            d.hide()
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item and item.widget() and item.widget() is not self._expired_label:
                for child in item.widget().findChildren(QWidget):
                    if isinstance(child, QLabel) and child not in [self._expired_label]:
                        child.hide()
        if self._blink_enabled:
            self._blink_timer.start(self._blink_interval)

    def _tick_blink(self):
        if not self._expired or not self._blink_enabled:
            return
        self._blink_visible = not self._blink_visible
        self._expired_label.setVisible(self._blink_visible)

    def setTime(self, total_seconds):
        if total_seconds is None:
            self._total_seconds = 0
            return
        if total_seconds <= 0:
            if not self._expired:
                self.showExpired()
            return

        self._expired = False
        self._blink_timer.stop()
        self._expired_label.hide()
        for d in self._all_digits:
            d.show()
        self._total_seconds = int(total_seconds)

        days = self._total_seconds // 86400
        remaining = self._total_seconds % 86400
        hours = remaining // 3600
        remaining %= 3600
        minutes = remaining // 60
        seconds = remaining % 60

        text = f"{days:02d}{hours:02d}{minutes:02d}{seconds:02d}"
        for i, ch in enumerate(text):
            if i < len(self._all_digits):
                if self._enable_flip:
                    self._all_digits[i].setValue(ch)
                else:
                    if self._all_digits[i]._value != ch:
                        self._all_digits[i]._old_value = self._all_digits[i]._value
                        self._all_digits[i]._value = ch
                        self._all_digits[i]._flip = 1.0
                        self._all_digits[i].update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        digit_w = min(int(w / 14), int(h * 0.55))
        digit_h = int(digit_w * 1.6)
        for d in self._all_digits:
            d.setMinimumSize(digit_w, digit_h)
            d.setMaximumSize(digit_w, digit_h)


class ExamModeConfigDialog(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("📝 倒计时·DJS - 考试模式")
        self.setMinimumSize(420, 380)
        cfg = getattr(app, 'exam_mode_config', {}) or {}
        tc = get_theme_colors(app.theme)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("📝 考试模式")
        title.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {tc['accent']};")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        self.edit_name = QLineEdit(cfg.get("name", "考试"))
        form.addRow("考试名称", self.edit_name)

        dur_row = QHBoxLayout()
        self.spin_dur = QDoubleSpinBox()
        self.spin_dur.setRange(0.1, 999.0)
        self.spin_dur.setSingleStep(0.5)
        self.spin_dur.setDecimals(1)
        self.combo_unit = QComboBox()
        self.combo_unit.addItem("分钟", "minute")
        self.combo_unit.addItem("小时", "hour")
        unit = cfg.get("unit", "hour")
        idx = self.combo_unit.findData(unit)
        if idx >= 0:
            self.combo_unit.setCurrentIndex(idx)
        default_dur = cfg.get("duration", 2.0) if unit == "hour" else cfg.get("duration", 120.0)
        self.spin_dur.setValue(default_dur)
        dur_row.addWidget(self.spin_dur)
        dur_row.addWidget(self.combo_unit)
        form.addRow("总时长", dur_row)

        self.edit_tip = QLineEdit(cfg.get("tip", "沉着冷静，认真应答"))
        form.addRow("提示文字", self.edit_tip)

        self.chk_flip = QCheckBox("启用翻页动画")
        self.chk_flip.setChecked(cfg.get("flip", True))
        form.addRow(self.chk_flip)

        color_row = QHBoxLayout()
        self.btn_color = QPushButton()
        self.btn_color.setFixedSize(40, 24)
        self.btn_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bg_color = cfg.get("bg_color", "#000000")
        self.btn_color.setStyleSheet(
            f"background-color: {self._bg_color}; border-radius: 4px; border: 1px solid {tc['border_color']};")
        self.btn_color.clicked.connect(self._pick_color)
        color_row.addWidget(self.btn_color)
        color_row.addStretch()
        form.addRow("背景颜色", color_row)

        layout.addLayout(form)

        self.lbl_preview_tip = QLabel(cfg.get("tip", "沉着冷静，认真应答"))
        self.lbl_preview_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_preview_tip.setStyleSheet(f"color: {tc['secondary_text']}; font-size: 9pt;")
        self.edit_tip.textChanged.connect(self.lbl_preview_tip.setText)
        layout.addWidget(self.lbl_preview_tip)

        layout.addStretch()

        btn_row = QHBoxLayout()
        self.btn_start = QPushButton("开始考试")
        self.btn_start.setProperty("primary", True)
        self.btn_start.setMinimumHeight(38)
        self.btn_start.setAutoDefault(False)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self._start)
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setProperty("secondary", True)
        self.btn_cancel.setMinimumHeight(38)
        self.btn_cancel.setAutoDefault(False)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_cancel)
        layout.addLayout(btn_row)

    def _pick_color(self):
        color = QColorDialog.getColor(QColor(self._bg_color), self, "选择背景颜色")
        if color.isValid():
            self._bg_color = color.name()
            tc = get_theme_colors(self.app.theme)
            self.btn_color.setStyleSheet(
                f"background-color: {self._bg_color}; border-radius: 4px; border: 1px solid {tc['border_color']};")

    def _build_config(self):
        unit = self.combo_unit.currentData()
        return {
            "name": self.edit_name.text().strip() or "考试",
            "duration": self.spin_dur.value(),
            "unit": unit,
            "tip": self.edit_tip.text().strip() or "沉着冷静，认真应答",
            "flip": self.chk_flip.isChecked(),
            "bg_color": self._bg_color,
        }

    def _start(self):
        cfg = self._build_config()
        self.app.exam_mode_config = cfg
        self.app.save_config(force=True)
        self.accept()
        self.app.enter_exam_mode(cfg)


class ExamModeWindow(QWidget):
    def __init__(self, app, config):
        super().__init__()
        self.app = app
        self.config = config
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.bg_color = QColor(config.get("bg_color", "#000000"))
        self.tip_text = config.get("tip", "沉着冷静，认真应答")
        self.exam_name = config.get("name", "考试")

        unit = config.get("unit", "hour")
        dur = config.get("duration", 2.0)
        total = dur * 3600 if unit == "hour" else dur * 60
        self.total_seconds = int(total)
        self.remaining = self.total_seconds

        self.state = "idle"
        self._ended = False
        self._hidden_windows = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 30)
        layout.setSpacing(0)

        self.lbl_name = QLabel(self.exam_name)
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 16pt;")
        layout.addWidget(self.lbl_name)

        self.lbl_tip = QLabel(self.tip_text)
        self.lbl_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_tip.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 20pt; padding: 18px;")
        layout.addWidget(self.lbl_tip)

        layout.addStretch()

        self.clock = FlipClockWidget(self)
        self.clock.setEnableFlip(config.get("flip", True))
        self.clock.setColor("#F5F5F5")
        self.clock.setCardColor("#2D2D37")
        clock_row = QHBoxLayout()
        clock_row.addStretch()
        clock_row.addWidget(self.clock)
        clock_row.addStretch()
        layout.addLayout(clock_row)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        self.btn_start = QPushButton("开始")
        self.btn_start.setProperty("primary", True)
        self.btn_start.setFixedSize(110, 42)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self.toggle_start)
        self.btn_pause = QPushButton("暂停")
        self.btn_pause.setFixedSize(110, 42)
        self.btn_pause.setEnabled(False)
        self.btn_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_exit = QPushButton("退出")
        self.btn_exit.setFixedSize(110, 42)
        self.btn_exit.setProperty("danger", True)
        self.btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exit.clicked.connect(self.confirm_exit)
        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_exit)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color)

    def showEvent(self, event):
        super().showEvent(event)
        self.showFullScreen()
        self._fit_clock()
        self.clock.setTime(self.remaining)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._fit_clock()

    def _fit_clock(self):
        sw = self.width()
        sh = self.height()
        digit_w = max(50, int(min(sw * 0.09, sh * 0.16)))
        digit_h = int(digit_w * 1.7)
        self.clock.setDigitSize(digit_w, digit_h)

    def _hide_countdown_windows(self):
        self._hidden_windows = []
        for w in getattr(self.app, 'windows', []):
            if w.isVisible():
                self._hidden_windows.append(w)
                w.hide()

    def _restore_countdown_windows(self):
        for w in self._hidden_windows:
            try:
                w.show()
            except Exception:
                pass
        self._hidden_windows = []

    def toggle_start(self):
        if self.state == "idle":
            self._hide_countdown_windows()
            self.state = "running"
            self.btn_start.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_pause.setText("暂停")
            self.timer.start()

    def toggle_pause(self):
        if self.state == "running":
            self.state = "paused"
            self.timer.stop()
            self.btn_pause.setText("继续")
        elif self.state == "paused":
            self.state = "running"
            self.timer.start()
            self.btn_pause.setText("暂停")

    def _tick(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.clock.setTime(self.remaining)
            if self.remaining <= 0:
                self._on_finished()

    def _on_finished(self):
        self._ended = True
        self.timer.stop()
        self.state = "ended"
        self.clock.setColor("#FF3B3B")
        self.clock.setTime(0)
        play_ding_sound(self.app.data_dir)
        self.btn_pause.setEnabled(False)
        self.btn_start.setEnabled(False)

    def confirm_exit(self):
        reply = QMessageBox.question(
            self, "退出考试模式", "确定要退出考试模式吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close_exam()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.confirm_exit()
        else:
            super().keyPressEvent(event)

    def close_exam(self):
        self.timer.stop()
        self._restore_countdown_windows()
        self.app.exam_mode_window = None
        self.close()


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

        if self.project.background_type == "transparent":
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setStyleSheet("background: transparent;")
        elif self.project.background_type == "color" and self.project.window_alpha < 1.0:
            if self.project.window_round_radius == 0:
                apply_modern_window_effect(int(self.winId()), effect_type="acrylic", is_dark=is_system_dark(), enable=True)
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
        self.fullscreen_flip_clock = None
        self._fullscreen_widgets = {}
        self._fs_widget_sizes = {}
        self._render_info_action = None
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        self.resize_data = {"resizing": False, "edge": None, "start_pos": None, "start_geo": None}

        # 视差相关
        self.target_px = 0.0
        self.target_py = 0.0
        self.current_px = 0.0
        self.current_py = 0.0
        self.enable_parallax = True
        self.parallax_intensity = 6
        self._base_positions = {}
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
        if not self.project.fullscreen_layout or not self.project.fullscreen_layouts:
            self._init_default_fullscreen_layout()

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
        QTimer.singleShot(200, self.start_typewriter_animation)
        QTimer.singleShot(400, self.start_tip_animation)

        if self.project.background_type == "image" and self.project.background_image:
            QTimer.singleShot(100, self.load_background_image)

        self.update_countdown()
        self.apply_custom_layout(skip_style=False)
        if getattr(self.project, 'click_through', False):
            self.set_click_through(True, save=False)
        self._update_tick_interval()

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self._refresh_weather)
        QTimer.singleShot(3000, self._refresh_weather)

        self.master.plugin_manager.trigger_event("on_window_create", self, project)

    def _refresh_weather(self, initial=False):
        if hasattr(self, 'weather_fetcher') and self.weather_fetcher:
            if initial or self.weather_label.isVisible():
                self.weather_fetcher.fetch(self.project.weather_city)

    def _update_tick_interval(self):
        interval = 1000 if self.countdown_label.uses_seconds() else 2000
        self.tick_timer.setInterval(interval)

    def _apply_click_through_state(self, enabled):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, bool(enabled))
        if sys.platform == 'win32':
            try:
                import ctypes
                hwnd = int(self.winId())
                if hwnd:
                    GWL_EXSTYLE = -20
                    WS_EX_TRANSPARENT = 0x20
                    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                    if enabled:
                        style |= WS_EX_TRANSPARENT
                    else:
                        style &= ~WS_EX_TRANSPARENT
                    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            except Exception:
                pass

    def set_click_through(self, enabled, save=True):
        self.project.click_through = bool(enabled)
        self._apply_click_through_state(enabled)
        if enabled:
            self.unsetCursor()
            self.drag_data["dragging"] = False
            self.resize_data["resizing"] = False
        if hasattr(self, 'act_click_through'):
            self.act_click_through.blockSignals(True)
            self.act_click_through.setChecked(bool(enabled))
            self.act_click_through.blockSignals(False)
        if save:
            self.master.save_config(force=True)

    def _switch_to_fullscreen_layout(self):
        self.countdown_label.hide()
        self.drag_hint_label.hide()
        if self.fullscreen_flip_clock:
            self.fullscreen_flip_clock.hide()
        if self.boarding_pass_widget:
            self.boarding_pass_widget.hide()
        self.tick_timer.setInterval(1000)
        self._apply_fullscreen_layout()

    def _switch_to_normal_layout(self):
        self.countdown_label.show()
        if self.fullscreen_flip_clock:
            self.fullscreen_flip_clock.hide()
        if self.boarding_pass_widget:
            self.boarding_pass_widget.hide()
        self._update_tick_interval()
        self.apply_custom_layout(skip_style=False)

    def _apply_fullscreen_layout(self):
        self.countdown_label.hide()
        self.drag_hint_label.hide()
        current_bg = getattr(self, 'temp_fullscreen_bg', self.project.dynamic_bg_type) if self.is_fullscreen else "default"
        layouts = self.project.fullscreen_layouts
        layout = layouts.get(current_bg) or layouts.get("default", {})
        if not layout:
            self._init_default_fullscreen_layout()
            layouts = self.project.fullscreen_layouts
            layout = layouts.get(current_bg) or layouts.get("default", {})

        win_w, win_h = self.width(), self.height()
        if win_w <= 0 or win_h <= 0:
            return

        is_sky = (current_bg == "sky")

        name_cfg = layout.get("name", {})
        if is_sky:
            self.project_label.hide()
            self.static_label.hide()
            boarding_cfg = layout.get("boarding_pass", {})
            if boarding_cfg.get("visible", True) and self.boarding_pass_widget:
                total_sec = getattr(self, '_last_total_seconds', 0) or 0
                self.boarding_pass_widget.setContent(
                    self.project.name, "", total_sec,
                    getattr(self, 'expired', False), self.project.expired_text)
                bw = int(boarding_cfg.get("width", 0.42) * win_w)
                bh = int(boarding_cfg.get("height", 0.15) * win_h)
                bx = int(boarding_cfg.get("x", 0.24) * win_w) - bw // 2
                by = int(boarding_cfg.get("y", 0.88) * win_h) - bh // 2
                self.boarding_pass_widget.setGeometry(bx, by, bw, bh)
                self.boarding_pass_widget.setColors(
                    boarding_cfg.get("text_color"),
                    boarding_cfg.get("sub_color"),
                    boarding_cfg.get("accent_color"))
                self.boarding_pass_widget.show()
                self.boarding_pass_widget.raise_()
                if not self._boarding_poem_timer.isActive():
                    self._update_boarding_poem()
                    self._boarding_poem_timer.start()
            else:
                self.boarding_pass_widget.hide()
                self._boarding_poem_timer.stop()
        else:
            if self.boarding_pass_widget:
                self.boarding_pass_widget.hide()
            self._boarding_poem_timer.stop()
            if name_cfg.get("visible", True):
                self.project_label.show()
                font = QFont(self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei",
                             max(12, name_cfg.get("font_size", 28)))
                font.setBold(True)
                font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
                self.project_label.setFont(font)
                self.project_label.setStyleSheet(
                    f"color: {name_cfg.get('color', '#FFFFFF')};"
                    f"background-color: {name_cfg.get('bg_color', 'rgba(0,0,0,0.25)')};"
                    f"border-radius: {name_cfg.get('bg_radius', 16)}px; border: none;"
                    f"font-size: {name_cfg.get('font_size', 28)}pt;")
                self.project_label.adjustSize()
                nw = max(self.project_label.width(), int(name_cfg.get("width", 0.30) * win_w))
                nh = max(self.project_label.height(), int(name_cfg.get("height", 0.08) * win_h))
                nx = int(name_cfg.get("x", 0.5) * win_w) - nw // 2
                ny = int(name_cfg.get("y", 0.06) * win_h) - nh // 2
                self.project_label.setGeometry(nx, ny, nw, nh)
                self.project_label.raise_()
            else:
                self.project_label.hide()

            static_cfg = layout.get("static_text", {})
            if static_cfg.get("visible", True):
                self.static_label.show()
                font = QFont(self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei",
                             max(10, static_cfg.get("font_size", 18)))
                font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
                self.static_label.setFont(font)
                self.static_label.setStyleSheet(
                    f"color: {static_cfg.get('color', '#E0E0E0')};"
                    f"background-color: {static_cfg.get('bg_color', 'transparent')};"
                    f"border-radius: {static_cfg.get('bg_radius', 0)}px; border: none;"
                    f"font-size: {static_cfg.get('font_size', 18)}pt;")
                self.static_label.adjustSize()
                sw = max(self.static_label.width(), int(static_cfg.get("width", 0.40) * win_w))
                sh = max(self.static_label.height(), int(static_cfg.get("height", 0.06) * win_h))
                sx = int(static_cfg.get("x", 0.5) * win_w) - sw // 2
                sy = int(static_cfg.get("y", 0.14) * win_h) - sh // 2
                self.static_label.setGeometry(sx, sy, sw, sh)
                self.static_label.raise_()
            else:
                self.static_label.hide()

        countdown_cfg = layout.get("countdown", {})
        if is_sky:
            if self.fullscreen_flip_clock:
                self.fullscreen_flip_clock.hide()
        else:
            if countdown_cfg.get("visible", True) and self.fullscreen_flip_clock:
                self.fullscreen_flip_clock.show()
                card_color = countdown_cfg.get("card_color", "#2D2D37")
                label_color = countdown_cfg.get("label_color", "#b0b0b0")
                self.fullscreen_flip_clock.setCardColor(card_color)
                self.fullscreen_flip_clock.setColor(countdown_cfg.get("color", "#FFFFFF"))
                self.fullscreen_flip_clock.setEnableFlip(
                    getattr(getattr(self, 'master', None), 'enable_flip_animation', True))
                cdx = countdown_cfg.get("x", 0.5)
                cdy = countdown_cfg.get("y", 0.48)
                clock_w = int(countdown_cfg.get("width", 0.75) * win_w)
                clock_h = int(countdown_cfg.get("height", 0.30) * win_h)
                cx = int(cdx * win_w) - clock_w // 2
                cy = int(cdy * win_h) - clock_h // 2
                self.fullscreen_flip_clock.setGeometry(cx, cy, clock_w, clock_h)
                self.fullscreen_flip_clock.raise_()
            else:
                if self.fullscreen_flip_clock:
                    self.fullscreen_flip_clock.hide()

        # 天气
        weather_cfg = layout.get("weather", {})
        has_weather = weather_cfg.get("visible", False)
        if has_weather:
            was_hidden = not self.weather_label.isVisible()
            self.weather_label.show()
            if was_hidden and hasattr(self, 'weather_fetcher') and self.weather_fetcher:
                if not self.weather_timer.isActive():
                    self.weather_timer.start(30 * 60 * 1000)
                QTimer.singleShot(500, self._refresh_weather)
            font = QFont(self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei",
                         max(10, weather_cfg.get("font_size", 18)))
            font.setBold(True)
            font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            self.weather_label.setFont(font)
            self.weather_label.setStyleSheet(
                f"color: {weather_cfg.get('color', '#E0E0E0')};"
                f"background-color: transparent; border: none;")
            cw = weather_cfg.get("custom_width")
            ch = weather_cfg.get("custom_height")
            if cw is not None and ch is not None:
                we_w = max(72, int(cw))
                we_h = max(88, int(ch))
            else:
                we_w = max(72, int(weather_cfg.get("width", 0.10) * win_w))
                we_h = max(88, int(weather_cfg.get("height", 0.16) * win_h))
            wex = int(weather_cfg.get("x", 0.85) * win_w) - we_w // 2
            wey = int(weather_cfg.get("y", 0.06) * win_h) - we_h // 2
            self.weather_label.setGeometry(wex, wey, we_w, we_h)
            self.weather_label.raise_()
        else:
            self.weather_label.hide()
            if self.weather_timer.isActive():
                self.weather_timer.stop()

        # 番茄钟
        pomo_cfg = layout.get("pomodoro", {})
        if pomo_cfg.get("visible", False):
            self.pomodoro_widget.show()
            pm_w = max(self.pomodoro_widget.sizeHint().width(), int(pomo_cfg.get("width", 0.18) * win_w))
            pm_h = max(self.pomodoro_widget.sizeHint().height(), int(pomo_cfg.get("height", 0.08) * win_h))
            self.pomodoro_widget.resize(pm_w, pm_h)
            pm_x, pm_y = pomo_cfg.get("x", 0.15), pomo_cfg.get("y", 0.06)
            self.pomodoro_widget.move(
                int(pm_x * win_w) - pm_w // 2,
                int(pm_y * win_h) - pm_h // 2)
            self.pomodoro_widget.raise_()
        else:
            self.pomodoro_widget.hide()

        # 诗词
        poem_cfg = layout.get("poem", {})
        show_poem = poem_cfg.get("visible", False) and poem_cfg.get("show_poem", True)
        if show_poem:
            self.poem_label.show()
            font = QFont(self.master.global_font if self.master.current_theme != "system_native" else "Microsoft YaHei",
                         max(10, poem_cfg.get("font_size", 22)))
            font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            self.poem_label.setFont(font)
            self.poem_label._text_color_hex = poem_cfg.get("color", "#D0D0D0" if is_system_dark() else "#333333")
            self.poem_label._opacity = poem_cfg.get("opacity", 0.9)
            self.poem_label.set_line_spacing(poem_cfg.get("line_spacing", 1.5))
            self.poem_label.set_marquee(poem_cfg.get("marquee", True))
            pw = int(poem_cfg.get("width", 0.80) * win_w)
            ph = self.poem_label.heightForWidth(pw)
            ph = max(ph, int(poem_cfg.get("height", 0.10) * win_h))
            self.poem_label.resize(pw, ph)
            pox = int(poem_cfg.get("x", 0.5) * win_w) - pw // 2
            poy = int(poem_cfg.get("y", 0.88) * win_h) - ph // 2
            self.poem_label.move(pox, poy)
            self.poem_label.raise_()
        else:
            self.poem_label.hide()

    def _update_fullscreen_flip_clock(self):
        flip_visible = self.fullscreen_flip_clock and self.fullscreen_flip_clock.isVisible()
        if not flip_visible:
            return
        try:
            eff_date, eff_time = get_effective_target(self.project)
            if eff_date is None:
                self.fullscreen_flip_clock.showExpired("循环已结束")
                return
            target = datetime.strptime(f"{eff_date} {eff_time}", "%Y-%m-%d %H:%M")
            now = datetime.now()
            diff = target - now
            total_seconds = diff.total_seconds()
            if total_seconds <= 0:
                self.fullscreen_flip_clock.showExpired(self.project.expired_text)
            else:
                self.fullscreen_flip_clock.setTime(total_seconds)
        except Exception as e:
            log_message(f"全屏翻页钟更新错误: {e}", "ERROR")

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

    def _init_default_fullscreen_layout(self):
        default_layout = self._build_default_fullscreen_layout()
        if not self.project.fullscreen_layout:
            self.project.fullscreen_layout = default_layout
        self.project.fullscreen_layouts.setdefault("default", default_layout)
        self.project.fullscreen_layouts.setdefault("aurora", json.loads(json.dumps(default_layout)))
        self.project.fullscreen_layouts.setdefault("sky", self._build_sky_fullscreen_layout())

    def _build_default_fullscreen_layout(self):
        is_dark = self.master.theme.is_dark if hasattr(self.master, 'theme') else is_system_dark()
        if is_dark:
            name_color = "#FFFFFF"
            name_bg = "rgba(0,0,0,0.25)"
            static_color = "#E0E0E0"
            weather_color = "#E0E0E0"
            poem_color = "#D0D0D0"
            countdown_color = "#FFFFFF"
            countdown_bg = "rgba(0,0,0,0.35)"
            card_color = "#2D2D37"
            label_color = "#b0b0b0"
            pomodoro_color = "#E0E0E0"
            pomodoro_bg = "rgba(0,0,0,0.2)"
        else:
            name_color = "#1E1E1E"
            name_bg = "rgba(255,255,255,0.7)"
            static_color = "#333333"
            weather_color = "#333333"
            poem_color = "#333333"
            countdown_color = "#1E1E1E"
            countdown_bg = "rgba(255,255,255,0.55)"
            card_color = "#F5F7FA"
            label_color = "#666666"
            pomodoro_color = "#333333"
            pomodoro_bg = "rgba(255,255,255,0.6)"

        layout = {}
        layout["name"] = {
            "visible": True, "x": 0.5, "y": 0.06, "width": 0.30, "height": 0.08,
            "font_size": 28, "color": name_color, "opacity": 1.0,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 3, "shadow_blur": 12,
            "bg_color": name_bg, "bg_radius": 16,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["static_text"] = {
            "visible": True, "x": 0.5, "y": 0.14, "width": 0.40, "height": 0.06,
            "font_size": 18, "color": static_color, "opacity": 0.95,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 8,
            "bg_color": "transparent", "bg_radius": 0,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["countdown"] = {
            "visible": True, "x": 0.5, "y": 0.48, "width": 0.75, "height": 0.30,
            "font_size": 36, "color": countdown_color, "opacity": 1.0,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 4, "shadow_blur": 16,
            "bg_color": countdown_bg, "bg_radius": 15,
            "alignment_h": "center", "alignment_v": "center", "text": "",
            "card_color": card_color,
            "label_color": label_color
        }
        layout["pomodoro"] = {
            "visible": False, "x": 0.15, "y": 0.06, "width": 0.18, "height": 0.08,
            "font_size": 16, "color": pomodoro_color, "opacity": 0.95,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 8,
            "bg_color": pomodoro_bg, "bg_radius": 12,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["weather"] = {
            "visible": False, "x": 0.85, "y": 0.06, "width": 0.10, "height": 0.16,
            "font_size": 14, "color": weather_color, "opacity": 0.95,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 8,
            "bg_color": "rgba(0,0,0,0.2)", "bg_radius": 12,
            "alignment_h": "center", "alignment_v": "center", "text": ""
        }
        layout["poem"] = {
            "visible": False, "x": 0.5, "y": 0.88, "width": 0.80, "height": 0.10,
            "font_size": 22, "color": poem_color, "opacity": 0.9,
            "stroke_color": "transparent", "stroke_width": 0,
            "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 2, "shadow_blur": 10,
            "bg_color": "rgba(0,0,0,0.2)", "bg_radius": 14,
            "alignment_h": "center", "alignment_v": "center", "text": "",
            "show_poem": True, "marquee": True, "line_spacing": 1.5
        }
        return layout

    def _build_sky_fullscreen_layout(self):
        layout = self._build_default_fullscreen_layout()
        layout["name"]["visible"] = False
        layout["static_text"]["visible"] = False
        layout["countdown"]["visible"] = False
        layout["boarding_pass"] = {
            "visible": True, "x": 0.24, "y": 0.88,
            "width": 0.42, "height": 0.15,
            "text_color": "#28344A",
            "sub_color": "rgba(90,120,160,0.88)",
            "accent_color": "#78B4F0",
        }
        layout["pomodoro"]["visible"] = False
        layout["poem"]["visible"] = False
        layout["weather"]["visible"] = False
        return layout

    def init_ui(self):
        self.project_label = QLabel(self.project.name, self)
        self.project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label = RollingNumberLabel("0.000 天", self)
        self.countdown_label.set_neon_config(self.project.use_neon, self.project.neon_start,
                                             self.project.neon_end, self.project.neon_glow, self.project.font_color)
        self.countdown_label.enable_flip_animation = getattr(getattr(self, 'master', None), 'enable_flip_animation', True)
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

        self.weather_label = CircularWeatherWidget(self)
        self.weather_label.setText("⏳ 获取天气...")
        self.weather_label.setGraphicsEffect(QGraphicsDropShadowEffect(self))

        self.weather_fetcher = WeatherFetcher(
            api_provider=getattr(self.master, 'weather_provider', 'qweather'),
            custom_url_template=getattr(self.master, 'custom_weather_url', ''),
            qweather_api_key=getattr(self.master, 'qweather_api_key', ''),
            qweather_api_host=getattr(self.master, 'qweather_api_host', ''))
        self.weather_fetcher.weather_updated.connect(self.weather_label.setText)
        self.weather_fetcher.weather_updated.connect(lambda _: self.apply_custom_layout(skip_style=False))
        self.weather_fetcher.weather_updated.connect(lambda _: self.weather_label._set_city_from_fetcher(self.weather_fetcher))
        self.weather_label.setVisible(False)

        self.pomodoro_widget = PomodoroWidget(self, self.project.pomodoro_work, self.project.pomodoro_break)
        self.pomodoro_widget.setVisible(False)
        self.tip_hint_widget = TypewriterLabel(self, speed=60)
        self.tip_hint_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_hint_widget.setVisible(False)
        self.drag_hint_label = QLabel(tr("right_click_hint"), self)
        self.drag_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_hint_label.hide()

        self.fullscreen_flip_clock = FullscreenCountdownWidget(self)
        self.fullscreen_flip_clock.setEnableFlip(
            getattr(getattr(self, 'master', None), 'enable_flip_animation', True))
        self.fullscreen_flip_clock.hide()

        self.boarding_pass_widget = BoardingPassWidget(self)
        self.boarding_pass_widget.hide()

        self._boarding_poem_timer = QTimer(self)
        self._boarding_poem_timer.setInterval(10000)
        self._boarding_poem_timer.timeout.connect(self._update_boarding_poem)

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
            qw_key = (self.weather_fetcher.qweather_api_key or "").strip() or WeatherFetcher.QWEATHER_DEFAULT_KEY
            qw_host = (self.weather_fetcher.qweather_api_host or "").strip() or WeatherFetcher.QWEATHER_DEFAULT_HOST
            dlg = WeatherForecastDialog(self.weather_fetcher.lat, self.weather_fetcher.lon,
                                        self.weather_fetcher.city_name, self,
                                        provider=self.weather_fetcher.api_provider,
                                        qw_key=qw_key, qw_host=qw_host,
                                        detailed_address=getattr(self.weather_fetcher, 'detailed_address', ''))
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
        self.countdown_label.enable_flip_animation = getattr(getattr(self, 'master', None), 'enable_flip_animation', True)
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

        self.act_click_through = QAction(tr("click_through"), self)
        self.act_click_through.setCheckable(True)
        self.act_click_through.setChecked(getattr(self.project, 'click_through', False))
        self.act_click_through.toggled.connect(self.set_click_through)
        self.menu.addAction(self.act_click_through)

        act_fs = QAction("全屏" if CURRENT_LANG == LANG_CHINESE else "Fullscreen", self)
        act_fs.triggered.connect(self.toggle_fullscreen)
        self.menu.addAction(act_fs)

        act_exam = QAction("考试模式", self)
        act_exam.triggered.connect(self.master.open_exam_mode)
        self.menu.addAction(act_exam)

        act_close = QAction(tr("close"), self)
        act_close.triggered.connect(self.close_window)
        self.menu.addAction(act_close)

        act_quit = QAction("退出应用" if CURRENT_LANG == LANG_CHINESE else "Quit", self)
        act_quit.triggered.connect(self.master.quit_app)
        self.menu.addAction(act_quit)

    def contextMenuEvent(self, event):
        if self.is_fullscreen:
            self.menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            if not hasattr(self, '_render_info_action') or self._render_info_action is None:
                self._render_info_action = QAction("", self)
                self._render_info_action.setEnabled(False)
                self.menu.addAction(self._render_info_action)
            rbe = getattr(self.master, 'render_backend', 'auto') if hasattr(self, 'master') else 'auto'
            rn = {"auto": "自动", "software": "软件渲染", "opengl": "OpenGL",
                  "vulkan": "Vulkan", "d3d11": "DirectX 11", "d3d12": "DirectX 12", "metal": "Metal"}.get(rbe, rbe)
            is_hw = rbe in ("d3d11", "d3d12", "metal", "vulkan")
            self._render_info_action.setText(f"渲染引擎: {rn}")
        pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else QCursor.pos()
        self.menu.popup(pos)

    def _pause_dynamic_bg(self):
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, '_timer'):
            try:
                self.bg_dynamic_widget._timer.stop()
            except Exception:
                pass
        elif self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'timer'):
            try:
                self.bg_dynamic_widget.timer.stop()
            except Exception:
                pass

    def _resume_dynamic_bg(self):
        if self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, '_timer'):
            try:
                w = self.bg_dynamic_widget
                w._timer.start(1000 // max(w.fps, 15))
            except Exception:
                pass
        elif self.bg_dynamic_widget and hasattr(self.bg_dynamic_widget, 'timer'):
            try:
                fps = getattr(self.bg_dynamic_widget, 'fps', 30)
                self.bg_dynamic_widget.timer.start(1000 // max(fps, 15))
            except Exception:
                pass

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

    def _fallback_to_cpu_dynamic_bg(self, bg_type):
        old_widget = self.bg_dynamic_widget
        self.bg_dynamic_widget = None
        radius = 0 if self.is_fullscreen else self.project.window_round_radius
        if bg_type == "aurora":
            self.bg_dynamic_widget = AuroraBackgroundWidget(self, radius=radius)
        elif bg_type == "sky":
            self.bg_dynamic_widget = SkyBackgroundWidget(self, radius=radius)
        else:
            return
        self.bg_dynamic_widget.set_fps(self.project.dynamic_fps)
        self.bg_dynamic_widget.set_quality(self.project.dynamic_quality)
        self.bg_dynamic_widget.setGeometry(self.rect())
        self.bg_dynamic_widget.lower()
        self.bg_dynamic_widget.show()
        if old_widget and old_widget is not self.bg_dynamic_widget:
            old_widget.hide()
            old_widget.deleteLater()
        if self.is_fullscreen and self.fullscreen_panel:
            self.fullscreen_panel.raise_()
        log_message(f"GPU 着色器初始化失败，已回退到 CPU 版 ({bg_type})", "ERROR")

    def setup_dynamic_bg(self):
        old_widget = self.bg_dynamic_widget
        self.bg_dynamic_widget = None
        bg_type = "none"
        if self.is_fullscreen:
            bg_type = getattr(self, 'temp_fullscreen_bg', self.project.dynamic_bg_type)
        elif self.project.background_type == "dynamic":
            bg_type = self.project.dynamic_bg_type
            if bg_type not in ("stars", "particles"):
                bg_type = "stars"
        log_message(f"setup_dynamic_bg: 目标类型={bg_type}, fullscreen={self.is_fullscreen}, gpu_enabled={getattr(getattr(self, 'master', None), 'enable_gpu_acceleration', False)}, HAS_OPENGL={HAS_OPENGL}, fps={self.project.dynamic_fps}, quality={self.project.dynamic_quality}", "INFO")
        if bg_type != "none":
            radius = 0 if self.is_fullscreen else self.project.window_round_radius
            gpu_enabled = getattr(getattr(self, 'master', None), 'enable_gpu_acceleration', False)
            debug_print(f"setup_dynamic_bg: type={bg_type}, fullscreen={self.is_fullscreen}, gpu_enabled={gpu_enabled}, HAS_OPENGL={HAS_OPENGL}, fps={self.project.dynamic_fps}, quality={self.project.dynamic_quality}")
            if bg_type == "slideshow":
                mgr = getattr(self.master, 'wallpaper_manager', None)
                self.bg_dynamic_widget = SlideshowWallpaperWidget(self, manager=mgr, radius=radius)
            elif bg_type in self.master.dynamic_bg_classes:
                entry = self.master.dynamic_bg_classes[bg_type]
                if isinstance(entry, dict):
                    WidgetClass = entry.get("class")
                    plugin_radius = entry.get("border_radius")
                else:
                    WidgetClass = entry
                    plugin_radius = None
                if plugin_radius is None:
                    plugin_radius = radius
                try:
                    self.bg_dynamic_widget = WidgetClass(self)
                except Exception as e:
                    log_message(f"创建插件动态背景 {bg_type} 失败: {e}", "ERROR")
                    self.bg_dynamic_widget = None
                if self.bg_dynamic_widget is not None:
                    self.bg_dynamic_widget._bg_id = bg_type
                    if hasattr(self.bg_dynamic_widget, 'set_radius'):
                        self.bg_dynamic_widget.set_radius(plugin_radius)
                    elif hasattr(self.bg_dynamic_widget, 'radius'):
                        self.bg_dynamic_widget.radius = plugin_radius
            else:
                if bg_type == "aurora":
                    shader_ok = False
                    if gpu_enabled and HAS_OPENGL:
                        try:
                            self.bg_dynamic_widget = AuroraShaderWidget(self, radius=radius)
                            shader_ok = True
                            debug_print("setup_dynamic_bg: 使用 AuroraShaderWidget (GPU)")
                        except Exception as e:
                            debug_print(f"AuroraShaderWidget 创建失败，回退 CPU 版: {e}")
                            self.bg_dynamic_widget = None
                    if not shader_ok or self.bg_dynamic_widget is None:
                        self.bg_dynamic_widget = AuroraBackgroundWidget(self, radius=radius)
                        debug_print("setup_dynamic_bg: 使用 AuroraBackgroundWidget (CPU)")
                elif bg_type == "sky":
                    shader_ok = False
                    if gpu_enabled and HAS_OPENGL:
                        try:
                            self.bg_dynamic_widget = SkyShaderWidget(self, radius=radius)
                            shader_ok = True
                            debug_print("setup_dynamic_bg: 使用 SkyShaderWidget (GPU)")
                        except Exception as e:
                            debug_print(f"SkyShaderWidget 创建失败，回退 CPU 版: {e}")
                            self.bg_dynamic_widget = None
                    if not shader_ok or self.bg_dynamic_widget is None:
                        self.bg_dynamic_widget = SkyBackgroundWidget(self, radius=radius)
                        debug_print("setup_dynamic_bg: 使用 SkyBackgroundWidget (CPU)")
                else:
                    self.bg_dynamic_widget = DynamicWallpaperWidget(self, wallpaper_type=bg_type, radius=radius)
                if not self.is_fullscreen:
                    self.bg_dynamic_widget.set_fps(min(self.project.dynamic_fps, 30))
                    self.bg_dynamic_widget.set_quality("medium" if self.project.dynamic_quality == "high" else self.project.dynamic_quality)
                else:
                    self.bg_dynamic_widget.set_fps(self.project.dynamic_fps)
                    self.bg_dynamic_widget.set_quality(self.project.dynamic_quality)
            if self.bg_dynamic_widget:
                self.bg_dynamic_widget._bg_id = bg_type
                self.bg_dynamic_widget.setGeometry(self.rect())
                self.bg_dynamic_widget.lower()
                self.bg_dynamic_widget.show()
                log_message(f"setup_dynamic_bg: 显示背景 widget={type(self.bg_dynamic_widget).__name__}, bg_id={bg_type}, geo={self.bg_dynamic_widget.geometry().width()}x{self.bg_dynamic_widget.geometry().height()}, visible={self.bg_dynamic_widget.isVisible()}", "INFO")
            if self.is_fullscreen and self.fullscreen_panel:
                self.fullscreen_panel.raise_()
            if old_widget and old_widget is not self.bg_dynamic_widget:
                old_widget.hide()
                old_widget.deleteLater()

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
        if getattr(self, 'is_fullscreen', False):
            self._apply_fullscreen_layout()
            return
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

        is_recurring = getattr(self.project, 'project_type', 'normal') == 'recurring'
        if is_recurring:
            nxt_desc = describe_next_recurrence(self.project)
            default_static = f"🔁 下次: {nxt_desc}" if nxt_desc != "已结束" else "🔁 循环已结束"
        else:
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
                elif cfg.get("type") == "deco_shape":
                    w = self._get_or_create_deco_shape(elem_id, cfg)
                elif cfg.get("type") == "divider":
                    w = self._get_or_create_divider(elem_id, cfg)
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
                    if elem_id == "poem":
                        w.set_line_spacing(cfg.get("line_spacing", 1.2))
                        w.set_marquee(cfg.get("marquee", False))
                        if not cfg.get("show_poem", True):
                            w.setVisible(False)
                            continue

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
                    if elem_id == "weather":
                        rel_w = cfg.get("width", 0.10)
                        rel_h = cfg.get("height", 0.16)
                        cw = max(72, int(rel_w * win_w))
                        ch = max(88, int(rel_h * win_h))
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
                x = int(pct_x * win_w) - cw // 2
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

    def _get_or_create_deco_shape(self, elem_id, config):
        if not hasattr(self, '_custom_widgets'):
            self._custom_widgets = {}
        if elem_id not in self._custom_widgets:
            shape_widget = QWidget(self)
            shape_widget.setObjectName(f"shape_{elem_id}")
            self._custom_widgets[elem_id] = shape_widget
        widget = self._custom_widgets[elem_id]
        shape_type = config.get("shape_type", "rectangle")
        bg_color = QColor(config.get("color", "#4facfe"))
        opacity = config.get("opacity", 1.0)
        stroke_color = QColor(config.get("stroke_color", "#3498db"))
        stroke_w = config.get("stroke_width", 2)
        radius = config.get("bg_radius", 8)
        style = f"""
            QWidget#shape_{elem_id} {{
                background-color: {bg_color.name() if shape_type == 'rectangle' else 'transparent'};
                border: {stroke_w}px solid {stroke_color.name() if stroke_color.name() != 'transparent' else 'transparent'};
                border-radius: {radius if shape_type == 'rectangle' else 9999}px;
                opacity: {opacity};
            }}
        """
        widget.setStyleSheet(style)
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        return widget

    def _get_or_create_divider(self, elem_id, config):
        if not hasattr(self, '_custom_widgets'):
            self._custom_widgets = {}
        if elem_id not in self._custom_widgets:
            divider_widget = QWidget(self)
            divider_widget.setObjectName(f"divider_{elem_id}")
            self._custom_widgets[elem_id] = divider_widget
        widget = self._custom_widgets[elem_id]
        color = QColor(config.get("color", "#666666"))
        opacity = config.get("opacity", 0.6)
        radius = config.get("bg_radius", 2)
        style = f"""
            QWidget#divider_{elem_id} {{
                background-color: {color.name()};
                border: none;
                border-radius: {radius}px;
                opacity: {opacity};
            }}
        """
        widget.setStyleSheet(style)
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
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

        eff_date, eff_time = get_effective_target(self.project)
        is_recurring = getattr(self.project, 'project_type', 'normal') == 'recurring'
        if is_recurring and eff_date is None:
            self.static_label.setText("🔁 循环已结束")
            self.static_label.setStyleSheet(f"color: {self.project.font_color};")
            self.project_label.setText(self.project.name)
            return
        days, hours, minutes, work_days, work_days_float, holiday_name = calculate_days(
            eff_date, eff_time
        )
        if is_recurring:
            static_text = f"🔁 下次: {describe_next_recurrence(self.project)}"
        elif days == 0 and hours == 0 and minutes == 0:
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
        self._update_boarding_pass()

    def update_ticking_countdown(self):
        if self.is_pomodoro and self.pomodoro_end_time:
            return
        try:
            eff_date, eff_time = get_effective_target(self.project)
            if eff_date is None:
                self._last_total_seconds = 0
                self._update_boarding_pass()
                if not self.countdown_label._expired:
                    self._maybe_play_end_sound()
                    self.countdown_label.showExpired("已结束")
                return
            target = datetime.strptime(f"{eff_date} {eff_time}", "%Y-%m-%d %H:%M")
            now = datetime.now()
            diff = target - now
            total_seconds = diff.total_seconds()
            if total_seconds <= 0:
                self.expired = True
                self._last_total_seconds = 0
                self._update_boarding_pass()
                if not self.countdown_label._expired:
                    self._maybe_play_end_sound()
                    self.countdown_label.showExpired(self.project.expired_text)
                return
            natural_days = total_seconds / 86400.0
            self.expired = False
            self._last_total_seconds = total_seconds
            self.countdown_label.setValue(natural_days)
            if self.is_fullscreen and self.fullscreen_flip_clock and self.fullscreen_flip_clock.isVisible():
                self.fullscreen_flip_clock.setTime(total_seconds)
            self._update_boarding_pass()
        except Exception as e:
            log_message(f"update_ticking_countdown 错误: {e}", "ERROR")

    def _update_boarding_pass(self):
        if not getattr(self, 'boarding_pass_widget', None):
            return
        if not self.boarding_pass_widget.isVisible():
            return
        self.boarding_pass_widget.setContent(
            self.project.name, "",
            getattr(self, '_last_total_seconds', 0),
            getattr(self, 'expired', False), self.project.expired_text)

    def _update_boarding_poem(self):
        poem = self.master.get_random_poem_or_tip()
        self.boarding_pass_widget.setPoem(poem if poem else "保持专注 · 享受当下")

    def _maybe_play_end_sound(self):
        if not getattr(self.project, 'enable_end_sound', True):
            return
        target_idx = self.master.get_highest_priority_expired_sound_index()
        if target_idx is None or target_idx != self.index:
            return
        if self.master._sound_playing_flag:
            return
        self.master.play_highest_priority_end_sound()

    def start_typewriter_animation(self):
        layout = self.project.custom_layout
        poem_cfg = layout.get("poem", {})
        show_poem = poem_cfg.get("visible", False) and poem_cfg.get("show_poem", True)
        if show_poem:
            if not self.master.poems_data or all(len(v) == 0 for v in self.master.poems_data.values()):
                QTimer.singleShot(3000, self._retry_poem_load)
                self.poem_label._full_text = "诗语数据加载中...请稍候"
                self.poem_label._current_display = "诗语数据加载中..."
                self.poem_label.update()
                return
            text = self.master.get_random_poem_or_tip(poem_cfg.get("levels"))
            if not text or text.strip() == "":
                text = "诗语轻扬 — 请在编辑器中勾选诗词来源"
            self.poem_label.start_animation(text)

    def _retry_poem_load(self):
        if not self.master.poems_data or all(len(v) == 0 for v in self.master.poems_data.values()):
            self.poem_label._full_text = "诗词数据未加载\n请重启应用或在设置中检查诗词级别"
            self.poem_label._current_display = "诗词数据未加载 - 请重启应用"
            self.poem_label.update()
        else:
            poem_cfg = self.project.custom_layout.get("poem", {})
            text = self.master.get_random_poem_or_tip(poem_cfg.get("levels"))
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
                text = "💡 欢迎使用倒计时·DJS！"
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

    def _hide_normal_widgets(self):
        for w in (self.countdown_label, self.drag_hint_label,
                  getattr(self, 'project_label', None),
                  getattr(self, 'static_label', None)):
            if w is not None:
                w.hide()
        if self.weather_label:
            self.weather_label.hide()
        if self.pomodoro_widget:
            self.pomodoro_widget.hide()
        if self.tip_hint_widget:
            self.tip_hint_widget.hide()
        if self.poem_label:
            self.poem_label.hide()

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.temp_fullscreen_bg = "stars"
            log_message(f"toggle_fullscreen: 进入全屏, bg_type=stars (默认)", "INFO")
            self.old_geometry = self.geometry()
            self.old_flags = self.windowFlags()
            for win in self.master.windows:
                if win != self:
                    win.hide()
            self.setUpdatesEnabled(False)
            self._hide_normal_widgets()
            if self.fullscreen_flip_clock:
                self.fullscreen_flip_clock.hide()
            self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self._hide_normal_widgets()
            self.show()
            self.showFullScreen()
            self.setWindowState(Qt.WindowState.WindowFullScreen)
            QApplication.processEvents()
            QApplication.processEvents()
            self._hide_normal_widgets()
            self._apply_click_through_state(False)
            self.is_fullscreen = True
            self.setup_dynamic_bg()
            if not self.project.fullscreen_layout or not self.project.fullscreen_layouts:
                self._init_default_fullscreen_layout()
            self._switch_to_fullscreen_layout()
            self.setUpdatesEnabled(True)
            if self.bg_dynamic_widget:
                self.bg_dynamic_widget.update()
            if not self.fullscreen_panel:
                self.fullscreen_panel = FullscreenSettingsPanel(self, self)
            self.fullscreen_panel.show()
            self.fullscreen_panel.adjustSize()
            panel_width = self.fullscreen_panel.width()
            panel_height = self.fullscreen_panel.height()
            self.fullscreen_panel.move(self.width() - panel_width - 30, self.height() - panel_height - 30)
            self.fullscreen_panel.raise_()
            self._update_fullscreen_flip_clock()
            log_message(f"toggle_fullscreen: 全屏完成, window_geo={self.width()}x{self.height()}", "INFO")
        else:
            log_message("toggle_fullscreen: 退出全屏", "INFO")
            self.is_fullscreen = False
            if hasattr(self, 'temp_fullscreen_bg'):
                delattr(self, 'temp_fullscreen_bg')
            if self.fullscreen_panel:
                self.fullscreen_panel.hide()
            saved_geo = self.old_geometry if self.old_geometry and self.old_geometry.width() > 0 and self.old_geometry.height() > 0 else self.geometry()
            try:
                self.setUpdatesEnabled(False)
                self.showNormal()
                self.setWindowState(Qt.WindowState.WindowNoState)
                QApplication.processEvents()
                self.setWindowFlags(self.old_flags)
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
                if self.project.background_type in ("transparent", "color"):
                    self.setStyleSheet("background: transparent;")
                self.setWindowOpacity(self.project.window_alpha)
                self.setGeometry(saved_geo)
                self.show()
                self.raise_()
                self.activateWindow()
                QApplication.processEvents()
                self._apply_click_through_state(getattr(self.project, 'click_through', False))
                for win in self.master.windows:
                    if win != self:
                        win.show()
                try:
                    self.setup_dynamic_bg()
                except Exception as e:
                    log_message(f"退出全屏时 setup_dynamic_bg 异常: {e}", "ERROR")
                try:
                    self._switch_to_normal_layout()
                except Exception as e:
                    log_message(f"退出全屏时 _switch_to_normal_layout 异常: {e}", "ERROR")
            finally:
                self.setUpdatesEnabled(True)
                self.show()
                self.raise_()
                self.activateWindow()
                self.update()
            log_message(f"toggle_fullscreen: 退出全屏完成, window_geo={self.width()}x{self.height()}", "INFO")

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

    def _update_default_colors_for_theme(self):
        layout = self.project.custom_layout
        if not layout:
            return
        is_dark = self.master.theme.is_dark if hasattr(self.master, 'theme') else is_system_dark()
        cur_key = "dark" if is_dark else "light"
        other_key = "light" if is_dark else "dark"
        defaults = {
            ("name", "color"): {"dark": "#FFFFFF", "light": "#1E1E1E"},
            ("name", "bg_color"): {"dark": "rgba(0,0,0,0.25)", "light": "rgba(255,255,255,0.7)"},
            ("static_text", "color"): {"dark": "#E0E0E0", "light": "#333333"},
            ("countdown", "color"): {"dark": "#FFFFFF", "light": "#1E1E1E"},
            ("countdown", "bg_color"): {"dark": "rgba(0,0,0,0.35)", "light": "rgba(255,255,255,0.8)"},
            ("countdown", "stroke_color"): {"dark": "rgba(255,255,255,0.3)", "light": "rgba(0,0,0,0.1)"},
        }
        for elem_id, cfg in layout.items():
            for (eid, field), colors in defaults.items():
                if eid != elem_id:
                    continue
                cur_val = cfg.get(field)
                if cur_val and cur_val == colors.get(other_key):
                    cfg[field] = colors.get(cur_key, cur_val)

    def refresh(self, theme_change=False):
        if theme_change:
            self._update_default_colors_for_theme()
        self.setWindowOpacity(self.project.window_alpha)
        if self.project.background_type == "transparent":
            self.bg_pixmap = None
            if self.bg_movie:
                self.bg_movie.stop()
                self.bg_movie = None
            if self.bg_dynamic_widget:
                self.bg_dynamic_widget.deleteLater()
                self.bg_dynamic_widget = None
            apply_modern_window_effect(int(self.winId()), enable=False)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setStyleSheet("background: transparent;")
        elif self.project.background_type == "color":
            self.bg_pixmap = None
            if self.bg_movie:
                self.bg_movie.stop()
                self.bg_movie = None
            if self.project.window_alpha < 1.0 and self.project.window_round_radius == 0:
                apply_modern_window_effect(int(self.winId()), effect_type="acrylic", is_dark=is_system_dark(), enable=True)
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

    HANDLE_SIZE = 8
    HANDLE_HOVER_SIZE = 12

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
        self._hover_handle = None
        self.snap_enabled = True
        self.grid_spacing = 20
        self.setMinimumSize(400, 300)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

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
        elif elem_type == "deco_shape":
            w = config.get("custom_width", 120)
            h = config.get("custom_height", 80)
        elif elem_type == "divider":
            w = config.get("custom_width", 200)
            h = config.get("custom_height", 3)
        elif elem_id == "pomodoro":
            w = int(60 * scale)
            h = int(60 * scale)
        elif elem_id == "weather":
            rel_w = config.get("width", 0.10)
            rel_h = config.get("height", 0.16)
            pw = self.project.size[0] if self.project.size and self.project.size[0] > 0 else 600
            ph = self.project.size[1] if self.project.size and len(self.project.size) > 1 and self.project.size[1] > 0 else 400
            w = int(max(72, int(rel_w * pw)) * scale)
            h = int(max(88, int(rel_h * ph)) * scale)
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
        if config.get("type") == "deco_shape":
            return ""
        if config.get("type") == "divider":
            return ""
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

    def _draw_weather_preview(self, painter, rect, scale):
        """在预览画布中绘制圆形天气挂件预览"""
        w, h = rect.width(), rect.height()
        city_h = int(14 * scale)
        avail_h = h - city_h - 6
        circle_d = min(w, avail_h) - 4
        circle_d = max(circle_d, int(36 * scale))
        cx = rect.center().x()
        cy = rect.top() + circle_d / 2 + 3
        ring_w = max(2, circle_d // 28)
        ring_color = QColor(120, 180, 240, 220)
        painter.setPen(QPen(ring_color, ring_w))
        painter.setBrush(QColor(15, 22, 38, 180))
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2, circle_d / 2)
        painter.setPen(QPen(QColor(ring_color.red(), ring_color.green(), ring_color.blue(), 60), ring_w + 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2 + 2, circle_d / 2 + 2)
        icon_size = int(circle_d * 0.42)
        emoji_font = QFont("Segoe UI Emoji")
        emoji_font.setPointSizeF(max(7, circle_d / 5.5))
        painter.setFont(emoji_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - circle_d / 2, cy - circle_d / 2 + 3, circle_d, icon_size + 3), Qt.AlignmentFlag.AlignCenter, "⛅")
        temp_font = QFont("Microsoft YaHei")
        temp_font.setBold(True)
        temp_font.setPointSizeF(max(8, circle_d / 6.5))
        painter.setFont(temp_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - circle_d / 2, cy - 2, circle_d, circle_d / 2 + 2), Qt.AlignmentFlag.AlignCenter, "25°")
        city_font = QFont("Microsoft YaHei")
        city_font.setPointSizeF(max(7, circle_d / 12))
        painter.setFont(city_font)
        painter.setPen(QColor(200, 210, 220, 220))
        painter.drawText(QRectF(rect.left(), cy + circle_d / 2 + 3, w, city_h), Qt.AlignmentFlag.AlignCenter, "北京")

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

    def _elem_manual_size(self, elem_id):
        config = (self.project.custom_layout or {}).get(elem_id, {})
        return not config.get("auto_width", True)

    def _hit_test_handle(self, pos, elem_id):
        if elem_id != self.highlighted_elem:
            return None
        if not self._elem_manual_size(elem_id):
            return None
        config = (self.project.custom_layout or {}).get(elem_id, {})
        if not config.get("visible", True):
            return None
        rect = self._get_elem_rect(elem_id, config)
        handles = self._get_handle_positions(rect)
        half = self.HANDLE_HOVER_SIZE // 2 + 2
        for name, hpos in handles.items():
            if abs(pos.x() - hpos.x()) <= half and abs(pos.y() - hpos.y()) <= half:
                return name
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        _tc = get_theme_colors(get_system_theme())
        painter.fillRect(self.rect(), QColor(_tc["alternate_bg"]))

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

        painter.setPen(QPen(QColor(_tc["border_color"]), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(canvas_rect, radius, radius)
        painter.restore()

        if hasattr(self.editor, 'cb_grid') and self.editor.cb_grid.isChecked():
            painter.setPen(Qt.PenStyle.NoPen)
            dot_color = QColor(100, 100, 130, 60)
            painter.setBrush(dot_color)
            gs = self.grid_spacing
            x = canvas_rect.x()
            while x <= canvas_rect.right():
                y = canvas_rect.y()
                while y <= canvas_rect.bottom():
                    painter.drawEllipse(QPointF(float(x), float(y)), 1.0, 1.0)
                    y += gs
                x += gs

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
            if elem_id == self.highlighted_elem:
                pen = QPen(QColor("#3498db"), 2.0, Qt.PenStyle.SolidLine)
                painter.setPen(pen)
                painter.setBrush(QColor(52, 152, 219, 25))
                painter.drawRoundedRect(rect, 4, 4)
                if self._elem_manual_size(elem_id):
                    handles = self._get_handle_positions(rect)
                    for hname, hpos in handles.items():
                        hs = self.HANDLE_HOVER_SIZE if hname == self._hover_handle else self.HANDLE_SIZE
                        painter.setBrush(QColor("#3498db"))
                        painter.setPen(QPen(QColor(255, 255, 255, 220), 1.2))
                        painter.drawRect(int(hpos.x() - hs // 2), int(hpos.y() - hs // 2), hs, hs)

            if config.get("type") == "custom_image":
                painter.setPen(color)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "🖼️")
            elif config.get("type") == "deco_shape":
                shape_type = config.get("shape_type", "rectangle")
                fill_color = QColor(config.get("color", "#4facfe"))
                fill_color.setAlpha(int(config.get("opacity", 1.0) * 255))
                stroke_color = QColor(config.get("stroke_color", "#3498db"))
                stroke_w = config.get("stroke_width", 2)
                radius = config.get("bg_radius", 8)
                painter.setPen(QPen(stroke_color, stroke_w) if stroke_w > 0 and stroke_color.name() != "transparent" else Qt.PenStyle.NoPen)
                painter.setBrush(fill_color)
                r = QRectF(rect)
                if shape_type == "circle":
                    painter.drawEllipse(r)
                else:
                    painter.drawRoundedRect(r, radius, radius)
            elif config.get("type") == "divider":
                line_color = QColor(config.get("color", "#666666"))
                line_color.setAlpha(int(config.get("opacity", 0.6) * 255))
                line_w = config.get("custom_height", 3)
                radius = config.get("bg_radius", 2)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(line_color)
                painter.drawRoundedRect(QRectF(rect), radius, radius)
            elif elem_id == "weather":
                self._draw_weather_preview(painter, rect, scale)
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
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            hover = self._hit_test_handle(event.pos(), self.highlighted_elem)
            if hover != self._hover_handle:
                self._hover_handle = hover
                self.setToolTip(tr("arrow_keys_resize") if hover else "")
                self.update()
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
            if self.dragging_elem and self.editor.window:
                self.editor.window.apply_custom_layout()
                self.editor.persist_layout()
            self.dragging_elem = None

    def keyPressEvent(self, event):
        elem_id = self.highlighted_elem
        if not elem_id or not self._elem_manual_size(elem_id):
            super().keyPressEvent(event)
            return
        key = event.key()
        if key not in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
            super().keyPressEvent(event)
            return
        step = 10 if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else 2
        config = (self.project.custom_layout or {}).get(elem_id)
        if config is None:
            return
        rect = self._get_elem_rect(elem_id, config)
        canvas_rect = self._get_canvas_rect()
        scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else 1.0
        cw = config.get("custom_width", rect.width() / scale)
        ch = config.get("custom_height", rect.height() / scale)
        if key == Qt.Key.Key_Right:
            cw += step
        elif key == Qt.Key.Key_Left:
            cw = max(30, cw - step)
        elif key == Qt.Key.Key_Down:
            ch += step
        elif key == Qt.Key.Key_Up:
            ch = max(20, ch - step)
        if config.get("type") == "custom_image":
            aspect = config.get("img_aspect")
            if aspect and aspect > 0:
                if key in (Qt.Key.Key_Left, Qt.Key.Key_Right):
                    ch = cw / aspect
                else:
                    cw = ch * aspect
        config["custom_width"] = cw
        config["custom_height"] = ch
        self.editor._update_ui_from_config()
        self.update()
        if self.editor.window:
            self.editor.window.apply_custom_layout()
        self.editor.persist_layout()
        event.accept()


DEFAULT_ELEMENTS = ["name", "static_text", "countdown"]
ALL_AVAILABLE_ELEMENTS = ["name", "static_text", "countdown", "poem", "weather", "pomodoro", "tip"]
EXTRA_ELEMENTS = ["deco_shape", "divider"]
ELEMENT_DISPLAY_NAMES = {
    "name": "📌 项目名称",
    "static_text": "📝 静态文字",
    "countdown": "⏳ 倒计时",
    "poem": "📜 诗语轻扬",
    "weather": "🌤️ 天气挂件",
    "pomodoro": "🍅 番茄钟",
    "tip": "💡 小提示",
    "deco_shape": "🎨 装饰图形",
    "divider": "➖ 分割线",
}


class PluginIntroductionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔌 倒计时·DJS - 帮助")
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
        tabs.addTab(tab_intro, "入门")

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
        tabs.addTab(tab_dev, "开发")

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
        tabs.addTab(tab_sec, "安全")

        layout.addWidget(tabs)

        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


def _fs_default_size(elem_id):
    defaults = {
        "name": (0.30, 0.08),
        "static_text": (0.40, 0.06),
        "countdown": (0.75, 0.30),
        "weather": (0.10, 0.16),
        "pomodoro": (0.18, 0.08),
        "poem": (0.80, 0.10),
    }
    return defaults.get(elem_id, (0.30, 0.10))


class FullscreenLayoutEditor(QDialog):
    def __init__(self, project, window, parent=None):
        super().__init__(parent)
        self.project = project
        self.window = window
        self.current_theme = get_system_theme()
        self.current_bg_type = "default"

        self._layout_backup = json.loads(json.dumps(project.fullscreen_layouts or {}))
        self._fl_backup = json.loads(json.dumps(project.fullscreen_layout or {}))

        if not project.fullscreen_layouts:
            window._init_default_fullscreen_layout()
        if "default" not in (project.fullscreen_layouts or {}):
            project.fullscreen_layouts["default"] = project.fullscreen_layout or {}

        self.setWindowTitle("倒计时·DJS - 全屏布局编辑器")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        self.init_ui()
        self.apply_theme_style()

    def _current_layout(self):
        layouts = self.project.fullscreen_layouts
        if self.current_bg_type not in layouts:
            layouts[self.current_bg_type] = json.loads(json.dumps(layouts.get("default", {})))
        return layouts[self.current_bg_type]

    def init_ui(self):
        _tc = get_theme_colors(self.current_theme)
        self.setStyleSheet(get_theme_qss(self.current_theme))

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        #元素列表
        left_panel = QWidget()
        left_panel.setObjectName("fsleLeft")
        left_panel.setFixedWidth(220)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)

        lbl_title = QLabel("全屏控件")
        lbl_title.setStyleSheet(f"font-size: 13pt; font-weight: bold; color: {_tc['accent']};")
        left_layout.addWidget(lbl_title)

        bg_lay = QHBoxLayout()
        bg_lay.addWidget(QLabel("背景:"))
        self.combo_bg_type = QComboBox()
        self.combo_bg_type.addItem("默认", "default")
        self.combo_bg_type.addItem("极光", "aurora")
        self.combo_bg_type.addItem("天空", "sky")
        self.combo_bg_type.currentIndexChanged.connect(self._on_bg_type_changed)
        bg_lay.addWidget(self.combo_bg_type)
        left_layout.addLayout(bg_lay)

        self.element_list = QListWidget()
        self.element_list.setStyleSheet(
            f"QListWidget {{ background-color: {_tc['input_bg']}; border: 1px solid {_tc['border_color']}; border-radius: 6px; }}"
            f"QListWidget::item {{ padding: 6px 10px; border-radius: 4px; }}"
            f"QListWidget::item:hover {{ background-color: {_tc['alternate_bg']}; }}"
            f"QListWidget::item:selected {{ background-color: {_tc['accent']}; color: {_tc['selected_text']}; }}")
        self.element_list.currentItemChanged.connect(self._on_element_selected)
        left_layout.addWidget(self.element_list)

        self.lbl_bg_hint = QLabel("")
        self.lbl_bg_hint.setWordWrap(True)
        self.lbl_bg_hint.setStyleSheet("color: #f39c12; font-size: 9pt; padding: 4px; border: none;")
        left_layout.addWidget(self.lbl_bg_hint)
        self._rebuild_element_list()

        # 可见性开关
        vis_lay = QHBoxLayout()
        vis_lay.addWidget(QLabel("可见:"))
        self.chk_visible = QCheckBox()
        self.chk_visible.setChecked(True)
        self.chk_visible.toggled.connect(self._on_visibility_changed)
        vis_lay.addWidget(self.chk_visible)
        vis_lay.addStretch()
        left_layout.addLayout(vis_lay)

        left_layout.addWidget(QHLine())

        # 属性编辑
        self.prop_form = QFormLayout()
        self.edit_x = self._make_spin("x", 0.0, 1.0, 0.01)
        self.edit_y = self._make_spin("y", 0.0, 1.0, 0.01)
        self.edit_width = self._make_spin("宽度", 0.05, 1.0, 0.01)
        self.edit_height = self._make_spin("高度", 0.05, 1.0, 0.01)
        self.edit_font_size = self._make_spin("字号", 8, 200, 1)
        self.edit_color = QLineEdit()
        self.edit_color.setPlaceholderText("#FFFFFF")
        self.edit_color.textChanged.connect(self._on_property_changed)
        self.edit_bg = QLineEdit()
        self.edit_bg.setPlaceholderText("transparent")
        self.edit_bg.textChanged.connect(self._on_property_changed)
        self.edit_opacity = self._make_spin("透明度", 0.0, 1.0, 0.05)

        self.prop_form.addRow("水平位置:", self.edit_x)
        self.prop_form.addRow("垂直位置:", self.edit_y)
        self.prop_form.addRow("宽度 (%):", self.edit_width)
        self.prop_form.addRow("高度 (%):", self.edit_height)
        self.prop_form.addRow("字体大小:", self.edit_font_size)
        self.prop_form.addRow("文字颜色:", self.edit_color)
        self.prop_form.addRow("背景颜色:", self.edit_bg)
        self.prop_form.addRow("透明度:", self.edit_opacity)
        left_layout.addLayout(self.prop_form)

        left_layout.addStretch()

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.accept)
        btn_save.setStyleSheet(f"background-color: {_tc['accent']}; color: {_tc['selected_text']}; padding: 8px; border-radius: 6px; font-weight: bold;")
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        btn_reset = QPushButton("恢复默认")
        btn_reset.clicked.connect(self._reset_to_default)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        left_layout.addLayout(btn_layout)
        left_layout.addWidget(btn_reset)

        main_layout.addWidget(left_panel)

        # 预览画布
        self.canvas = FullscreenPreviewCanvas(self.project, self)
        main_layout.addWidget(self.canvas, 1)

        if self.element_list.count() > 0:
            self.element_list.setCurrentRow(0)

    def _make_spin(self, label, min_v, max_v, step):
        spin = QDoubleSpinBox()
        spin.setRange(min_v, max_v)
        spin.setSingleStep(step)
        spin.setDecimals(3 if step < 1 else 0)
        spin.valueChanged.connect(self._on_property_changed)
        return spin

    def _on_element_selected(self, current, previous):
        if not current:
            return
        elem_id = current.data(Qt.ItemDataRole.UserRole)
        if not elem_id:
            return
        self.canvas.set_highlighted_element(elem_id)
        cfg = self._current_layout().get(elem_id, {})
        default_w, default_h = _fs_default_size(elem_id)
        self._updating_ui = True
        self.edit_x.setValue(cfg.get("x", 0.5))
        self.edit_y.setValue(cfg.get("y", 0.5))
        self.edit_width.setValue(cfg.get("width", default_w))
        self.edit_height.setValue(cfg.get("height", default_h))
        self.edit_font_size.setValue(cfg.get("font_size", 28))
        self.edit_color.setText(cfg.get("color", "#FFFFFF"))
        self.edit_bg.setText(cfg.get("bg_color", "transparent"))
        self.edit_opacity.setValue(cfg.get("opacity", 1.0))
        self.chk_visible.setChecked(cfg.get("visible", True))
        self._updating_ui = False

    def _on_property_changed(self, *args):
        if getattr(self, '_updating_ui', False):
            return
        item = self.element_list.currentItem()
        if not item:
            return
        elem_id = item.data(Qt.ItemDataRole.UserRole)
        if not elem_id:
            return
        default_w, default_h = _fs_default_size(elem_id)
        cfg = self._current_layout().setdefault(elem_id, {
            "visible": True, "x": 0.5, "y": 0.5, "width": default_w, "height": default_h,
            "font_size": 28, "color": "#FFFFFF", "opacity": 1.0, "bg_color": "transparent"})
        cfg["x"] = self.edit_x.value()
        cfg["y"] = self.edit_y.value()
        cfg["width"] = self.edit_width.value()
        cfg["height"] = self.edit_height.value()
        cfg["font_size"] = int(self.edit_font_size.value())
        cfg["color"] = self.edit_color.text() or "#FFFFFF"
        cfg["bg_color"] = self.edit_bg.text() or "transparent"
        cfg["opacity"] = self.edit_opacity.value()
        self.canvas.update()

    def _on_visibility_changed(self, checked):
        item = self.element_list.currentItem()
        if not item:
            return
        elem_id = item.data(Qt.ItemDataRole.UserRole)
        if not elem_id:
            return
        default_w, default_h = _fs_default_size(elem_id)
        self._current_layout().setdefault(elem_id, {
            "visible": True, "x": 0.5, "y": 0.5, "width": default_w, "height": default_h,
            "font_size": 28, "color": "#FFFFFF", "opacity": 1.0, "bg_color": "transparent"})
        self._current_layout()[elem_id]["visible"] = checked
        self.canvas.update()

    def _reset_to_default(self):
        reply = QMessageBox.question(self, "恢复默认", "确认恢复当前背景的全屏控件为默认布局吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.window._init_default_fullscreen_layout()
            if self.current_bg_type == "default":
                self.project.fullscreen_layouts["default"] = self.window._build_default_fullscreen_layout()
            elif self.current_bg_type == "aurora":
                self.project.fullscreen_layouts["aurora"] = self.window._build_default_fullscreen_layout()
            elif self.current_bg_type == "sky":
                self.project.fullscreen_layouts["sky"] = self.window._build_sky_fullscreen_layout()
            self.canvas.update()
            if self.element_list.currentItem():
                self._on_element_selected(self.element_list.currentItem(), None)

    def _rebuild_element_list(self):
        self.element_list.blockSignals(True)
        self.element_list.clear()
        all_items = [("name", "📛 项目名称"), ("static_text", "📝 静态文字"),
                     ("countdown", "⏱️ 翻页倒计时"), ("weather", "🌤️ 天气"),
                     ("pomodoro", "🍅 番茄钟"), ("poem", "📜 诗词")]
        restricted = self.current_bg_type in ("sky", "aurora")
        if restricted:
            all_items = [it for it in all_items if it[0] in ("name", "static_text", "countdown")]
        for eid, elabel in all_items:
            item = QListWidgetItem(elabel)
            item.setData(Qt.ItemDataRole.UserRole, eid)
            self.element_list.addItem(item)
        self.element_list.blockSignals(False)
        if restricted:
            self.lbl_bg_hint.setText("⛅ 高渲染动态背景：仅保留核心控件，可调整位置与大小；挂件（天气/番茄钟/诗词）已禁用")
            self.chk_visible.setEnabled(False)
        else:
            self.lbl_bg_hint.setText("")
            self.chk_visible.setEnabled(True)
        if self.element_list.count() > 0:
            self.element_list.setCurrentRow(0)

    def _on_bg_type_changed(self, index):
        self.current_bg_type = self.combo_bg_type.currentData()
        self._rebuild_element_list()
        self.canvas.update()
        if self.element_list.currentItem():
            self._on_element_selected(self.element_list.currentItem(), None)

    def accept(self):
        if self.project.fullscreen_layouts.get("default"):
            self.project.fullscreen_layout = self.project.fullscreen_layouts["default"]
        super().accept()

    def apply_theme_style(self):
        _tc = get_theme_colors(self.current_theme)
        self.setStyleSheet(get_theme_qss(self.current_theme))

    def reject(self):
        self.project.fullscreen_layouts = self._layout_backup
        self.project.fullscreen_layout = self._fl_backup
        super().reject()


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class FullscreenPreviewCanvas(QWidget):
    HANDLE_SIZE = 10

    def __init__(self, project, editor, parent=None):
        super().__init__(parent)
        self.project = project
        self.editor = editor
        self.highlighted_elem = None
        self.dragging_elem = None
        self.drag_offset = QPoint()
        self.resizing_elem = None
        self.resize_handle = None  # "tl", "tr", "bl", "br"
        self.resize_start_pct = None
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)

        self._aspect_ratio = 16.0 / 9.0

    def set_highlighted_element(self, elem_id):
        self.highlighted_elem = elem_id
        self.update()

    def _get_canvas_rect(self):
        w, h = self.width(), self.height()
        margin = 16
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

    def _pct_to_px(self, pct_x, pct_y):
        rect = self._get_canvas_rect()
        return QPoint(int(rect.x() + pct_x * rect.width()), int(rect.y() + pct_y * rect.height()))

    def _px_to_pct(self, px, py):
        rect = self._get_canvas_rect()
        return (max(0.0, min(1.0, (px - rect.x()) / max(1, rect.width()))),
                max(0.0, min(1.0, (py - rect.y()) / max(1, rect.height()))))

    def _get_elem_rect(self, elem_id, cfg):
        """根据 x, y, width, height 百分比计算控件矩形"""
        default_w, default_h = _fs_default_size(elem_id)
        pct_x = cfg.get("x", 0.5)
        pct_y = cfg.get("y", 0.5)
        pct_w = cfg.get("width", default_w)
        pct_h = cfg.get("height", default_h)
        rect = self._get_canvas_rect()
        ew = max(40, int(pct_w * rect.width()))
        eh = max(28, int(pct_h * rect.height()))
        center = self._pct_to_px(pct_x, pct_y)
        ex = center.x() - ew // 2
        ey = center.y() - eh // 2
        return QRect(ex, ey, ew, eh)

    def _get_handle_rect(self, elem_rect, handle):
        hh = self.HANDLE_SIZE
        if handle == "tl":
            return QRect(elem_rect.x() - hh // 2, elem_rect.y() - hh // 2, hh, hh)
        if handle == "tr":
            return QRect(elem_rect.right() - hh // 2, elem_rect.y() - hh // 2, hh, hh)
        if handle == "bl":
            return QRect(elem_rect.x() - hh // 2, elem_rect.bottom() - hh // 2, hh, hh)
        if handle == "br":
            return QRect(elem_rect.right() - hh // 2, elem_rect.bottom() - hh // 2, hh, hh)
        return QRect()

    def _handle_at(self, elem_rect, pos):
        for h in ["tl", "tr", "bl", "br"]:
            if self._get_handle_rect(elem_rect, h).contains(pos):
                return h
        return None

    def _draw_weather_preview(self, painter, rect):
        w, h = rect.width(), rect.height()
        city_h = max(10, int(h * 0.13))
        avail_h = h - city_h - 6
        circle_d = min(w, avail_h) - 4
        circle_d = max(circle_d, 36)
        cx = rect.center().x()
        cy = rect.top() + circle_d / 2 + 3
        ring_w = max(2, circle_d // 28)
        ring_color = QColor(120, 180, 240, 220)
        painter.setPen(QPen(ring_color, ring_w))
        painter.setBrush(QColor(15, 22, 38, 180))
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2, circle_d / 2)
        painter.setPen(QPen(QColor(ring_color.red(), ring_color.green(), ring_color.blue(), 60), ring_w + 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), circle_d / 2 + 2, circle_d / 2 + 2)
        emoji_font = QFont("Segoe UI Emoji")
        emoji_font.setPointSizeF(max(7, circle_d / 5.5))
        painter.setFont(emoji_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - circle_d / 2, cy - circle_d / 2 + 3, circle_d, circle_d * 0.45), Qt.AlignmentFlag.AlignCenter, "⛅")
        temp_font = QFont("Microsoft YaHei")
        temp_font.setBold(True)
        temp_font.setPointSizeF(max(8, circle_d / 6.5))
        painter.setFont(temp_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - circle_d / 2, cy - 2, circle_d, circle_d / 2 + 2), Qt.AlignmentFlag.AlignCenter, "25°")
        city_font = QFont("Microsoft YaHei")
        city_font.setPointSizeF(max(7, circle_d / 12))
        painter.setFont(city_font)
        painter.setPen(QColor(200, 210, 220, 220))
        painter.drawText(QRectF(rect.left(), cy + circle_d / 2 + 3, w, city_h), Qt.AlignmentFlag.AlignCenter, "北京")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        painter.fillRect(self.rect(), QColor(30, 30, 35))

        rect = self._get_canvas_rect()
        # 画布区域
        painter.setPen(QPen(QColor(60, 60, 70), 1))
        painter.setBrush(QColor(20, 20, 25))
        painter.drawRoundedRect(QRectF(rect), 8, 8)

        # 参考线
        painter.setPen(QPen(QColor(50, 50, 60, 80), 1, Qt.PenStyle.DashLine))
        for pct in [0.25, 0.5, 0.75]:
            px = rect.x() + int(pct * rect.width())
            py = rect.y() + int(pct * rect.height())
            painter.drawLine(px, rect.y(), px, rect.bottom())
            painter.drawLine(rect.x(), py, rect.right(), py)

        layout = self.editor._current_layout() or {}
        elem_labels = {"name": "名称", "static_text": "静态文字", "countdown": "翻页倒计时",
                       "weather": "天气", "pomodoro": "番茄钟", "poem": "诗词"}

        for highlight_pass in (False, True):
            for elem_id, cfg in layout.items():
                if not cfg.get("visible", True):
                    continue
                is_highlighted = (elem_id == self.highlighted_elem)
                if is_highlighted != highlight_pass:
                    continue

                elem_rect = self._get_elem_rect(elem_id, cfg)

                if is_highlighted:
                    painter.setPen(QPen(QColor("#4FC3F7"), 2, Qt.PenStyle.DashLine))
                    painter.setBrush(QColor(79, 195, 247, 30))
                else:
                    painter.setPen(QPen(QColor(100, 100, 120), 1))
                    painter.setBrush(QColor(40, 40, 50, 180))

                painter.drawRoundedRect(QRectF(elem_rect), 6, 6)

                if elem_id == "weather":
                    self._draw_weather_preview(painter, elem_rect)
                else:
                    label = elem_labels.get(elem_id, elem_id)
                    painter.setPen(QPen(QColor("#E0E0E0")))
                    font = QFont("Microsoft YaHei", 9)
                    painter.setFont(font)
                    painter.drawText(QRectF(elem_rect), Qt.AlignmentFlag.AlignCenter, label)

                if is_highlighted:
                    painter.setBrush(QColor("#4FC3F7"))
                    painter.setPen(Qt.PenStyle.NoPen)
                    for h in ["tl", "tr", "bl", "br"]:
                        hr = self._get_handle_rect(elem_rect, h)
                        painter.drawRect(hr)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        layout = self.editor._current_layout() or {}
        if self.highlighted_elem:
            cfg = layout.get(self.highlighted_elem, {})
            if cfg.get("visible", True):
                elem_rect = self._get_elem_rect(self.highlighted_elem, cfg)
                handle = self._handle_at(elem_rect, event.pos())
                if handle:
                    self.resizing_elem = self.highlighted_elem
                    self.resize_handle = handle
                    self.resize_start_pct = (
                        cfg.get("x", 0.5), cfg.get("y", 0.5),
                        cfg.get("width", _fs_default_size(self.highlighted_elem)[0]),
                        cfg.get("height", _fs_default_size(self.highlighted_elem)[1]))
                    return

        for elem_id, cfg in layout.items():
            if not cfg.get("visible", True):
                continue
            elem_rect = self._get_elem_rect(elem_id, cfg)
            if elem_rect.contains(event.pos()):
                self.dragging_elem = elem_id
                self.drag_offset = event.pos() - elem_rect.center()
                self.editor.element_list.setCurrentRow(
                    [self.editor.element_list.item(i).data(Qt.ItemDataRole.UserRole)
                     for i in range(self.editor.element_list.count())].index(elem_id))
                break

    def mouseMoveEvent(self, event):
        if self.dragging_elem:
            new_center = event.pos() - self.drag_offset
            pctx, pcty = self._px_to_pct(new_center.x(), new_center.y())
            cfg = self.editor._current_layout().setdefault(self.dragging_elem, {})
            cfg["x"] = pctx
            cfg["y"] = pcty
            if hasattr(self.editor, '_updating_ui'):
                self.editor._updating_ui = True
                self.editor.edit_x.setValue(pctx)
                self.editor.edit_y.setValue(pcty)
                self.editor._updating_ui = False
            self.update()
        elif self.resizing_elem:
            cfg = self.editor._current_layout().setdefault(self.resizing_elem, {})
            sx, sy, sw, sh = self.resize_start_pct
            rect = self._get_canvas_rect()
            cx_px = sx * rect.width() + rect.x()
            cy_px = sy * rect.height() + rect.y()
            dx_px = event.pos().x() - cx_px
            dy_px = event.pos().y() - cy_px
            new_w_pct = max(0.05, min(1.0, abs(dx_px) * 2 / max(1, rect.width())))
            new_h_pct = max(0.05, min(1.0, abs(dy_px) * 2 / max(1, rect.height())))
            cfg["width"] = new_w_pct
            cfg["height"] = new_h_pct
            if hasattr(self.editor, '_updating_ui'):
                self.editor._updating_ui = True
                self.editor.edit_width.setValue(new_w_pct)
                self.editor.edit_height.setValue(new_h_pct)
                self.editor._updating_ui = False
            self.update()
        else:
            cursor = Qt.CursorShape.ArrowCursor
            if self.highlighted_elem:
                cfg = (self.editor._current_layout() or {}).get(self.highlighted_elem, {})
                if cfg.get("visible", True):
                    elem_rect = self._get_elem_rect(self.highlighted_elem, cfg)
                    h = self._handle_at(elem_rect, event.pos())
                    if h in ("tl", "br"):
                        cursor = Qt.CursorShape.SizeFDiagCursor
                    elif h in ("tr", "bl"):
                        cursor = Qt.CursorShape.SizeBDiagCursor
                    elif elem_rect.contains(event.pos()):
                        cursor = Qt.CursorShape.SizeAllCursor
            self.setCursor(cursor)

    def mouseReleaseEvent(self, event):
        self.dragging_elem = None
        self.resizing_elem = None
        self.resize_handle = None
        self.resize_start_pct = None
        self.update()


class AppearanceEditor(QDialog):
    def __init__(self, project, window, parent=None):
        super().__init__(parent)
        self.project = project
        self.window = window
        self.current_theme = get_system_theme()
        self.current_elem = None
        self._updating_ui = False
        self._dirty = False

        self._layout_backup = json.loads(json.dumps(project.custom_layout or {}))
        self._alpha_backup = project.window_alpha

        if not project.custom_layout:
            self._init_default_layout()

        self.setWindowTitle("倒计时·DJS - 自定义外观编辑器")
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
        _tc = get_theme_colors(self.current_theme)
        _panel_qss = f"QWidget#aePanel {{ background-color: {_tc['panel_bg']}; border: 1px solid {_tc['border_color']}; border-radius: 8px; }}"
        if hasattr(self, 'left_panel'):
            self.left_panel.setStyleSheet(_panel_qss)
            self.center_panel.setStyleSheet(_panel_qss)
            self.right_panel.setStyleSheet(_panel_qss)
        if hasattr(self, 'element_list'):
            self._apply_element_list_style(_tc)

    def _apply_element_list_style(self, _tc):
        self.element_list.setStyleSheet(
            "QListWidget { background-color: " + _tc["input_bg"] + "; border: 1px solid " + _tc["border_color"] + "; border-radius: 6px; padding: 4px; }"
            "QListWidget::item { padding: 8px 10px 8px 14px; border-radius: 4px; margin: 1px 2px; }"
            "QListWidget::item:hover { background-color: " + _tc["alternate_bg"] + "; color: " + _tc["text_color"] + "; }"
            "QListWidget::item:selected { background-color: " + _tc["accent"] + "; color: " + _tc["selected_text"] + "; }"
        )

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        _tc = get_theme_colors(self.current_theme)
        _panel_qss = f"QWidget#aePanel {{ background-color: {_tc['panel_bg']}; border: 1px solid {_tc['border_color']}; border-radius: 8px; }}"

        left_panel = QWidget()
        left_panel.setObjectName("aePanel")
        left_panel.setFixedWidth(240)
        left_panel.setStyleSheet(_panel_qss)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("📐 元素列表")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 6px;")
        left_layout.addWidget(title_label)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 8)
        toolbar.setSpacing(4)
        self.btn_add = QPushButton("➕")
        self.btn_add.setToolTip("添加元素")
        self.btn_add.setFixedSize(34, 30)
        self.btn_add.setProperty("primary", True)
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.clicked.connect(self.add_element)
        toolbar.addWidget(self.btn_add)
        self.btn_remove = QPushButton("🗑️")
        self.btn_remove.setToolTip("删除选中元素")
        self.btn_remove.setFixedSize(34, 30)
        self.btn_remove.setProperty("danger", True)
        self.btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_remove.clicked.connect(self.remove_element)
        self.btn_remove.setEnabled(False)
        toolbar.addWidget(self.btn_remove)
        toolbar.addStretch()
        self.btn_up = QPushButton("⬆")
        self.btn_up.setToolTip("上移")
        self.btn_up.setFixedSize(34, 30)
        self.btn_up.setProperty("secondary", True)
        self.btn_up.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_up.clicked.connect(self.move_element_up)
        toolbar.addWidget(self.btn_up)
        self.btn_down = QPushButton("⬇")
        self.btn_down.setToolTip("下移")
        self.btn_down.setFixedSize(34, 30)
        self.btn_down.setProperty("secondary", True)
        self.btn_down.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_down.clicked.connect(self.move_element_down)
        toolbar.addWidget(self.btn_down)
        self.btn_plugin_help = QPushButton("❓")
        self.btn_plugin_help.setToolTip("如何添加更多元素？")
        self.btn_plugin_help.setFixedSize(34, 30)
        self.btn_plugin_help.setProperty("secondary", True)
        self.btn_plugin_help.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_plugin_help.clicked.connect(self.go_to_plugin_help)
        toolbar.addWidget(self.btn_plugin_help)
        left_layout.addLayout(toolbar)

        self.element_list = QListWidget()
        self.element_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.element_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.element_list.model().rowsMoved.connect(self._on_element_rows_moved)
        self.element_list.currentRowChanged.connect(self.on_element_select)
        _tc = get_theme_colors(self.current_theme)
        self._apply_element_list_style(_tc)
        left_layout.addWidget(self.element_list)

        grid_options_box = QFrame()
        grid_options_box.setStyleSheet(
            "QFrame { background-color: " + _tc["panel_bg"] + "; border: 1px solid " + _tc["border_color"] + "; border-radius: 6px; }"
        )
        grid_options_lay = QHBoxLayout(grid_options_box)
        grid_options_lay.setContentsMargins(8, 6, 8, 6)
        grid_options_lay.setSpacing(10)
        self.cb_grid = QCheckBox("网格")
        self.cb_grid.setChecked(True)
        self.cb_snap = QCheckBox("吸附")
        self.cb_snap.setChecked(True)
        self.cb_guides = QCheckBox("参考线")
        self.cb_guides.setChecked(True)
        grid_options_lay.addWidget(self.cb_grid)
        grid_options_lay.addWidget(self.cb_snap)
        grid_options_lay.addWidget(self.cb_guides)
        grid_options_lay.addStretch()
        left_layout.addWidget(grid_options_box)

        center_panel = QWidget()
        center_panel.setObjectName("aePanel")
        center_panel.setStyleSheet(_panel_qss)
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(10, 10, 10, 10)

        preview_label = QLabel("👁️ 预览（拖拽调整位置）")
        preview_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 4px;")
        center_layout.addWidget(preview_label)

        self.preview_canvas = PreviewCanvas(self.project, self)
        self.preview_canvas.setMinimumSize(400, 300)
        center_layout.addWidget(self.preview_canvas, 1)

        self.cb_grid.toggled.connect(self.preview_canvas.update)
        self.cb_snap.toggled.connect(lambda v: setattr(self.preview_canvas, 'snap_enabled', v))
        self.cb_guides.toggled.connect(self.preview_canvas.update)

        right_panel = QWidget()
        right_panel.setObjectName("aePanel")
        right_panel.setStyleSheet(_panel_qss)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(8)

        self.prop_title = QLabel("属性设置")
        self.prop_title.setStyleSheet(f"font-size: 12pt; font-weight: bold; color: {get_theme_colors(self.current_theme)['accent']};")
        right_layout.addWidget(self.prop_title)

        self.no_selection_label = QLabel("← 请选择元素")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        _nstc = get_theme_colors(self.current_theme)
        self.no_selection_label.setStyleSheet(
            f"color: {_nstc['secondary_text']}; font-size: 9pt; padding: 12px; "
            f"border: 1px dashed {_nstc['border_color']}; border-radius: 6px; margin: 4px;")
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
        self.slider_font_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_font_size.setRange(6, 72)
        self.slider_font_size.valueChanged.connect(self._on_font_size_slider)
        size_layout.addWidget(self.slider_font_size, 1)
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(6, 72)
        self.spin_font_size.setFixedWidth(56)
        self.spin_font_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_font_size.valueChanged.connect(self._on_font_size_spin)
        size_layout.addWidget(self.spin_font_size)
        self.general_section.addLayout(size_layout)

        self.cb_auto_width = QCheckBox("自动宽度（尺寸随字号与内容自适应）")
        self.cb_auto_width.setChecked(True)
        self.cb_auto_width.toggled.connect(self._on_auto_width_toggled)
        self.general_section.addWidget(self.cb_auto_width)

        self.manual_size_widget = QWidget()
        ms_layout = QVBoxLayout(self.manual_size_widget)
        ms_layout.setContentsMargins(0, 0, 0, 0)
        ms_layout.setSpacing(4)
        width_row = QHBoxLayout()
        lbl_w = QLabel("宽度")
        lbl_w.setFixedWidth(80)
        lbl_w.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        width_row.addWidget(lbl_w)
        self.slider_width = QSlider(Qt.Orientation.Horizontal)
        self.slider_width.setRange(30, 800)
        self.slider_width.valueChanged.connect(self._on_manual_size_changed)
        width_row.addWidget(self.slider_width, 1)
        self.spin_width = QSpinBox()
        self.spin_width.setRange(30, 800)
        self.spin_width.setFixedWidth(64)
        self.spin_width.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_width.valueChanged.connect(self._on_manual_size_spin)
        width_row.addWidget(self.spin_width)
        ms_layout.addLayout(width_row)
        height_row = QHBoxLayout()
        lbl_h = QLabel("高度")
        lbl_h.setFixedWidth(80)
        lbl_h.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        height_row.addWidget(lbl_h)
        self.slider_height = QSlider(Qt.Orientation.Horizontal)
        self.slider_height.setRange(20, 600)
        self.slider_height.valueChanged.connect(self._on_manual_size_changed)
        height_row.addWidget(self.slider_height, 1)
        self.spin_height = QSpinBox()
        self.spin_height.setRange(20, 600)
        self.spin_height.setFixedWidth(64)
        self.spin_height.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_height.valueChanged.connect(self._on_manual_size_spin)
        height_row.addWidget(self.spin_height)
        ms_layout.addLayout(height_row)
        self.manual_size_widget.setVisible(False)
        self.general_section.addWidget(self.manual_size_widget)

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
        self.spin_opacity = QSpinBox()
        self.spin_opacity.setRange(0, 100)
        self.spin_opacity.setFixedWidth(64)
        self.spin_opacity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_opacity.setSuffix("%")
        self.spin_opacity.valueChanged.connect(self._on_opacity_spin)
        opacity_layout.addWidget(self.slider_opacity, 1)
        opacity_layout.addWidget(self.spin_opacity)
        self.general_section.addLayout(opacity_layout)

        self.prop_layout.addWidget(self.general_section)
        self.prop_layout.addSpacing(12)

        self.effects_section = CollapsibleSection("✨ 特效（描边/阴影）", initially_expanded=True)

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

        self.effects_section.addWidget(self.stroke_section)

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

        self.effects_section.addWidget(self.shadow_section)
        self.prop_layout.addWidget(self.effects_section)
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

        self.layout_section = CollapsibleSection("📐 位置与布局", initially_expanded=True)

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
        self.layout_section.addWidget(self.align_section)

        pos_section = CollapsibleSection("🎯 窗口位置（相对坐标）", initially_expanded=False)
        x_row = QHBoxLayout()
        lbl_pos_x = QLabel("水平 X")
        lbl_pos_x.setFixedWidth(80)
        lbl_pos_x.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        x_row.addWidget(lbl_pos_x)
        self.slider_pos_x = QSlider(Qt.Orientation.Horizontal)
        self.slider_pos_x.setRange(0, 100)
        self.slider_pos_x.valueChanged.connect(self._on_pos_changed)
        x_row.addWidget(self.slider_pos_x, 1)
        self.spin_pos_x = QSpinBox()
        self.spin_pos_x.setRange(0, 100)
        self.spin_pos_x.setSuffix("%")
        self.spin_pos_x.setFixedWidth(64)
        self.spin_pos_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_pos_x.valueChanged.connect(self._on_pos_x_spin)
        x_row.addWidget(self.spin_pos_x)
        pos_section.addLayout(x_row)

        y_row = QHBoxLayout()
        lbl_pos_y = QLabel("垂直 Y")
        lbl_pos_y.setFixedWidth(80)
        lbl_pos_y.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        y_row.addWidget(lbl_pos_y)
        self.slider_pos_y = QSlider(Qt.Orientation.Horizontal)
        self.slider_pos_y.setRange(0, 100)
        self.slider_pos_y.valueChanged.connect(self._on_pos_changed)
        y_row.addWidget(self.slider_pos_y, 1)
        self.spin_pos_y = QSpinBox()
        self.spin_pos_y.setRange(0, 100)
        self.spin_pos_y.setSuffix("%")
        self.spin_pos_y.setFixedWidth(64)
        self.spin_pos_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_pos_y.valueChanged.connect(self._on_pos_y_spin)
        y_row.addWidget(self.spin_pos_y)
        pos_section.addLayout(y_row)
        self._pos_section = pos_section
        self.layout_section.addWidget(pos_section)

        self.prop_layout.addWidget(self.layout_section)
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
        self.combo_display_format.addItems([
            "小数 (天)", "整数 (天)", "天时分", "时分秒", "自定义模板"
        ])
        self.combo_display_format.currentIndexChanged.connect(self._on_display_format_changed)
        cd_fmt_layout.addWidget(self.combo_display_format)
        self.countdown_section.addLayout(cd_fmt_layout)

        self.custom_template_row = QWidget()
        ct_outer = QVBoxLayout(self.custom_template_row)
        ct_outer.setContentsMargins(0, 0, 0, 0)
        ct_outer.setSpacing(4)
        ct_layout = QHBoxLayout()
        ct_layout.setContentsMargins(0, 0, 0, 0)
        lbl_template = QLabel("模板")
        lbl_template.setFixedWidth(80)
        lbl_template.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        ct_layout.addWidget(lbl_template)
        self.edit_format_template = QLineEdit()
        self.edit_format_template.setPlaceholderText("{days}天 {hours}时 {minutes}分 {seconds}秒")
        self.edit_format_template.textChanged.connect(self._on_property_changed)
        ct_layout.addWidget(self.edit_format_template)
        ct_outer.addLayout(ct_layout)

        ct_btn_row = QHBoxLayout()
        ct_btn_row.setContentsMargins(80, 0, 0, 0)
        ct_btn_row.setSpacing(4)
        lbl_hint = QLabel("插入:")
        lbl_hint.setStyleSheet("font-size: 10px; color: gray;")
        ct_btn_row.addWidget(lbl_hint)
        for label, token in [("天 {days}", "{days}"), ("时 {hours}", "{hours}"),
                             ("分 {minutes}", "{minutes}"), ("秒 {seconds}", "{seconds}")]:
            btn = QPushButton(label)
            btn.setFixedHeight(22)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("font-size: 10px; padding: 1px 6px;")
            btn.clicked.connect(lambda _checked=False, t=token: self._insert_template_token(t))
            ct_btn_row.addWidget(btn)
        ct_btn_row.addStretch()
        ct_outer.addLayout(ct_btn_row)

        self.countdown_section.addWidget(self.custom_template_row)
        self.custom_template_row.setVisible(False)

        self.countdown_section.setVisible(False)
        self.prop_layout.addWidget(self.countdown_section)
        self.prop_layout.addSpacing(12)

        self.weather_section = CollapsibleSection("🌤️ 天气设置")
        self.combo_weather_province = QComboBox()
        self.combo_weather_province.addItems(list(PROVINCE_CITY_DATA.keys()))
        self.combo_weather_province.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.combo_weather_city = QComboBox()
        self.combo_weather_city.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.combo_weather_province.currentTextChanged.connect(self._update_weather_cities)
        province_row = QHBoxLayout()
        lbl_prov = QLabel("省份")
        lbl_prov.setFixedWidth(80)
        lbl_prov.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        province_row.addWidget(lbl_prov)
        province_row.addWidget(self.combo_weather_province, 1)
        self.weather_section.addLayout(province_row)
        city_row = QHBoxLayout()
        lbl_city = QLabel("城市")
        lbl_city.setFixedWidth(80)
        lbl_city.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        city_row.addWidget(lbl_city)
        city_row.addWidget(self.combo_weather_city, 1)
        self.weather_section.addLayout(city_row)
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
        poem_form = QFormLayout()
        poem_form.setSpacing(6)
        self.chk_show_poem = QCheckBox(tr("show_poem"))
        self.chk_show_poem.setChecked(True)
        self.chk_show_poem.toggled.connect(self._on_property_changed)
        poem_form.addRow(self.chk_show_poem)

        level_box = QGroupBox(tr("poem_levels"))
        level_lay = QVBoxLayout(level_box)
        level_lay.setSpacing(4)
        self.chk_lv_primary = QCheckBox(tr("poem_primary"))
        self.chk_lv_junior = QCheckBox(tr("poem_junior"))
        self.chk_lv_senior = QCheckBox(tr("poem_senior"))
        self.chk_lv_extra = QCheckBox(tr("poem_extra"))
        self.chk_lv_extra.setChecked(True)
        for chk in (self.chk_lv_primary, self.chk_lv_junior,
                    self.chk_lv_senior, self.chk_lv_extra):
            chk.toggled.connect(self._on_property_changed)
            level_lay.addWidget(chk)
        poem_form.addRow(level_box)

        self.spin_typewriter = QSpinBox()
        self.spin_typewriter.setRange(1, 120)
        self.spin_typewriter.setValue(self.project.typewriter_interval)
        self.spin_typewriter.setSuffix(" 分钟")
        self.spin_typewriter.valueChanged.connect(self._on_property_changed)
        poem_form.addRow(tr("switch_interval"), self.spin_typewriter)

        row_poem_ls = QHBoxLayout()
        row_poem_ls.addWidget(QLabel(tr("line_spacing")))
        self.slider_poem_line_spacing = QSlider(Qt.Orientation.Horizontal)
        self.slider_poem_line_spacing.setRange(8, 30)
        self.slider_poem_line_spacing.setValue(12)
        self.label_poem_ls = QLabel("1.2")
        self.label_poem_ls.setFixedWidth(32)
        self.slider_poem_line_spacing.valueChanged.connect(
            lambda v: self.label_poem_ls.setText(f"{v / 10:.1f}"))
        self.slider_poem_line_spacing.valueChanged.connect(self._on_property_changed)
        row_poem_ls.addWidget(self.slider_poem_line_spacing)
        row_poem_ls.addWidget(self.label_poem_ls)
        poem_form.addRow(row_poem_ls)

        self.chk_poem_marquee = QCheckBox(tr("marquee_scroll"))
        self.chk_poem_marquee.setChecked(False)
        self.chk_poem_marquee.toggled.connect(self._on_property_changed)
        poem_form.addRow(self.chk_poem_marquee)

        self.poem_section.addLayout(poem_form)
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
        for _sb in prop_widget.findChildren(QSpinBox) + prop_widget.findChildren(QDoubleSpinBox):
            _sb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
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

        self.win_alpha_row = QWidget()
        row_a = QHBoxLayout(self.win_alpha_row)
        row_a.setContentsMargins(0, 0, 0, 0)
        row_a.addWidget(QLabel("窗口透明度"))
        self.win_alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.win_alpha_slider.setRange(10, 100)
        self.win_alpha_slider.setValue(int(self.project.window_alpha * 100))
        self.win_alpha_spin = QSpinBox()
        self.win_alpha_spin.setRange(10, 100)
        self.win_alpha_spin.setFixedWidth(64)
        self.win_alpha_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.win_alpha_spin.setSuffix("%")
        self.win_alpha_spin.setValue(int(self.project.window_alpha * 100))
        self.win_alpha_slider.valueChanged.connect(self._on_win_alpha_preview)
        self.win_alpha_slider.valueChanged.connect(lambda v: (self.win_alpha_spin.blockSignals(True), self.win_alpha_spin.setValue(v), self.win_alpha_spin.blockSignals(False)))
        self.win_alpha_spin.valueChanged.connect(self._on_win_alpha_spin)
        row_a.addWidget(self.win_alpha_slider, 1)
        row_a.addWidget(self.win_alpha_spin)
        win_lay.addWidget(self.win_alpha_row)

        self.win_radius_row = QWidget()
        row_radius = QHBoxLayout(self.win_radius_row)
        row_radius.setContentsMargins(0, 0, 0, 0)
        row_radius.addWidget(QLabel("窗口圆角半径"))
        self.win_radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.win_radius_slider.setRange(0, 30)
        self.win_radius_slider.setSingleStep(1)
        self.win_radius_slider.setValue(int(self.project.window_round_radius))
        self.win_radius_spin = QSpinBox()
        self.win_radius_spin.setRange(0, 30)
        self.win_radius_spin.setFixedWidth(64)
        self.win_radius_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.win_radius_spin.setSuffix("px")
        self.win_radius_spin.setValue(int(self.project.window_round_radius))
        self.win_radius_slider.valueChanged.connect(self._on_win_radius_changed)
        self.win_radius_slider.valueChanged.connect(lambda v: (self.win_radius_spin.blockSignals(True), self.win_radius_spin.setValue(v), self.win_radius_spin.blockSignals(False)))
        self.win_radius_spin.valueChanged.connect(self._on_win_radius_spin)
        row_radius.addWidget(self.win_radius_slider, 1)
        row_radius.addWidget(self.win_radius_spin)
        win_lay.addWidget(self.win_radius_row)

        row_b = QHBoxLayout()
        row_b.addWidget(QLabel("背景类型"))
        self.win_combo_bg = QComboBox()
        self.win_combo_bg.addItems(["纯色", "图片", "渐变", "动态", "透明"])
        bg_map = {"color": "纯色", "image": "图片", "gradient": "渐变", "dynamic": "动态", "transparent": "透明"}
        self.win_combo_bg.setCurrentText(bg_map.get(self.project.background_type, "纯色"))
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
        row_g.setSpacing(8)
        lbl_grad_start = QLabel("起点色")
        lbl_grad_start.setFixedWidth(48)
        row_g.addWidget(lbl_grad_start)
        self.win_grad_start_btn = QPushButton()
        self.win_grad_start_btn.setFixedSize(40, 22)
        self.win_grad_start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_grad_start_btn.setStyleSheet(
            f"background-color: {self.project.gradient_start}; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_grad_start_btn.clicked.connect(lambda: self._pick_win_color_attr(self.win_grad_start_btn, "grad_start"))
        row_g.addWidget(self.win_grad_start_btn)
        row_g.addSpacing(8)
        lbl_grad_end = QLabel("终点色")
        lbl_grad_end.setFixedWidth(48)
        row_g.addWidget(lbl_grad_end)
        self.win_grad_end_btn = QPushButton()
        self.win_grad_end_btn.setFixedSize(40, 22)
        self.win_grad_end_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.win_grad_end_btn.setStyleSheet(
            f"background-color: {self.project.gradient_end}; border-radius: 4px; border: 1px solid {tc2['border_color']};")
        self.win_grad_end_btn.clicked.connect(lambda: self._pick_win_color_attr(self.win_grad_end_btn, "grad_end"))
        row_g.addWidget(self.win_grad_end_btn)
        row_g.addStretch()
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
                if key in ("stars", "particles"):
                    self.win_combo_dyn.addItem(name, key)
        idx = self.win_combo_dyn.findData(self.project.dynamic_bg_type)
        if idx < 0 and self.project.dynamic_bg_type in ("aurora", "sky"):
            idx = self.win_combo_dyn.findData("stars")
        if idx >= 0: self.win_combo_dyn.setCurrentIndex(idx)
        self.win_combo_dyn.setToolTip("高渲染背景（极光/天空）请全屏模式下启用")
        self.win_combo_dyn_quality = QComboBox()
        self.win_combo_dyn_quality.setMinimumHeight(24)
        self.win_combo_dyn_quality.addItems(["高", "中", "低"])
        self.win_combo_dyn_quality.setCurrentIndex(
            0 if self.project.dynamic_quality == "high" else
            (1 if self.project.dynamic_quality == "medium" else 2))
        self.win_combo_dyn_fps = QComboBox()
        self.win_combo_dyn_fps.setMinimumHeight(24)
        self.win_combo_dyn_fps.addItems(["30 FPS", "60 FPS", "120 FPS"])
        fps_val = getattr(self.project, 'dynamic_fps', 30)
        self.win_combo_dyn_fps.setCurrentIndex(0 if fps_val <= 30 else (1 if fps_val <= 60 else 2))
        dyn_r.addWidget(self.win_combo_dyn)
        dyn_r.addWidget(self.win_combo_dyn_quality)
        dyn_r.addWidget(self.win_combo_dyn_fps)
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

        for _sb in self.win_settings_box.findChildren(QSpinBox) + self.win_settings_box.findChildren(QDoubleSpinBox):
            _sb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

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

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(6)
        self.splitter.setStyleSheet(
            f"QSplitter::handle {{ background-color: {get_theme_colors(self.current_theme)['border_color']}; }}"
        )
        self.splitter.addWidget(center_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        self.left_panel = left_panel
        self.center_panel = center_panel
        self.right_panel = right_panel

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.splitter, 1)
        _state = getattr(getattr(self.window, 'master', None), 'editor_splitter', '') if self.window else ''
        if _state:
            try:
                self.splitter.restoreState(QByteArray.fromHex(_state.encode('utf-8')))
            except Exception:
                pass

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

    def _on_win_alpha_preview(self, v):
        self.project.window_alpha = v / 100.0
        if self.window:
            self.window.setWindowOpacity(v / 100.0)

    def apply_and_close(self):
        self.project.window_alpha = self.win_alpha_slider.value() / 100.0

        bg_text = self.win_combo_bg.currentText()
        if "图片" in bg_text:
            self.project.background_type = "image"
        elif "渐变" in bg_text:
            self.project.background_type = "gradient"
        elif "动态" in bg_text:
            self.project.background_type = "dynamic"
        elif "透明" in bg_text:
            self.project.background_type = "transparent"
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
        fps_map = {0: 30, 1: 60, 2: 120}
        self.project.dynamic_fps = fps_map.get(self.win_combo_dyn_fps.currentIndex(), 30)
        self.project.window_round_radius = self.win_radius_slider.value()

        if self.window:
            self.window.apply_custom_layout()
            self.window.setup_dynamic_bg()
            self.window._update_tick_interval()
            self.window.update()
            self.persist_layout()
        self._dirty = False
        self._update_cancel_btn()
        self.accept()

    def cancel_and_close(self):
        if self._dirty:
            reply = QMessageBox.question(
                self, "确认放弃修改", "当前有未应用的修改，确定要放弃吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
        self.project.custom_layout = self._layout_backup
        self.project.window_alpha = self._alpha_backup
        if self.window:
            self.window.apply_custom_layout()
            self.window.setWindowOpacity(self._alpha_backup)
        self._dirty = False
        self.reject()

    def closeEvent(self, event):
        if self._dirty:
            reply = QMessageBox.question(
                self, "确认放弃修改", "当前有未应用的修改，确定要放弃吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self.project.custom_layout = self._layout_backup
            self.project.window_alpha = self._alpha_backup
            if self.window:
                self.window.apply_custom_layout()
                self.window.setWindowOpacity(self._alpha_backup)
            self._dirty = False
        event.accept()

    def _mark_dirty(self):
        if not self._dirty:
            self._dirty = True
            self._update_cancel_btn()

    def _update_cancel_btn(self):
        if not hasattr(self, 'btn_cancel'):
            return
        if self._dirty:
            self.btn_cancel.setText("❌ 放弃更改 (*)")
            self.btn_cancel.setToolTip("有未应用的修改，点击将放弃所有更改")
        else:
            self.btn_cancel.setText("❌ 取消")
            self.btn_cancel.setToolTip("")

    def done(self, result):
        try:
            _state = self.splitter.saveState().toHex().data().decode('utf-8')
            _app = getattr(self.window, 'master', None) if self.window else None
            if _app is not None:
                _app.editor_splitter = _state
                _app.save_config(force=True)
        except Exception:
            pass
        super().done(result)

    def _populate_element_list(self):
        self.element_list.blockSignals(True)
        self.element_list.clear()
        layout = self.project.custom_layout or {}
        for elem_id in layout:
            display = ELEMENT_DISPLAY_NAMES.get(elem_id, elem_id)
            icon = "👁️" if layout[elem_id].get("visible", True) else "🚫"
            item = QListWidgetItem(f"{icon}  {display}")
            item.setData(Qt.ItemDataRole.UserRole, elem_id)
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
            self.window.master.open_settings(tab="help", section="🛠️ 开发插件 - 快速开始")

    def _load_element_properties(self, elem_id):
        self._updating_ui = True
        layout = self.project.custom_layout
        elem = layout.get(elem_id, {})

        self.cb_visible.setChecked(elem.get("visible", True))
        self.slider_font_size.setValue(elem.get("font_size", 14))
        self.spin_font_size.blockSignals(True)
        self.spin_font_size.setValue(elem.get("font_size", 14))
        self.spin_font_size.blockSignals(False)
        auto_w = elem.get("auto_width", True)
        if elem_id == "weather":
            auto_w = False
        self.cb_auto_width.setChecked(auto_w)
        self.cb_auto_width.setVisible(elem_id != "weather")
        self.manual_size_widget.setVisible(not auto_w)
        rect = self.preview_canvas._get_elem_rect(elem_id, elem)
        canvas_rect = self.preview_canvas._get_canvas_rect()
        scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else 1.0
        cw = int(elem.get("custom_width", rect.width() / scale))
        ch = int(elem.get("custom_height", rect.height() / scale))
        cw_c = max(self.slider_width.minimum(), min(self.slider_width.maximum(), cw))
        ch_c = max(self.slider_height.minimum(), min(self.slider_height.maximum(), ch))
        self.slider_width.setValue(cw_c)
        self.slider_height.setValue(ch_c)
        self.spin_width.blockSignals(True)
        self.spin_width.setValue(cw_c)
        self.spin_width.blockSignals(False)
        self.spin_height.blockSignals(True)
        self.spin_height.setValue(ch_c)
        self.spin_height.blockSignals(False)
        font_family = elem.get("font_family", "")
        self.combo_font_family.setCurrentText(font_family if font_family else "Microsoft YaHei")

        color = elem.get("color", "#FFFFFF")
        self.btn_color.setStyleSheet(f"background-color: {{color}}; border-radius: 6px; border: 1px solid {{border_color}};".format(color=color, border_color=get_theme_colors(self.current_theme)['border_color']))
        self.btn_color.setProperty("color_value", color)

        opacity = int(elem.get("opacity", 1.0) * 100)
        self.slider_opacity.setValue(opacity)
        self.spin_opacity.blockSignals(True)
        self.spin_opacity.setValue(opacity)
        self.spin_opacity.blockSignals(False)

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

        pos_x = int(round(elem.get("x", 0.5) * 100))
        pos_y = int(round(elem.get("y", 0.1) * 100))
        self.slider_pos_x.blockSignals(True)
        self.slider_pos_x.setValue(pos_x)
        self.slider_pos_x.blockSignals(False)
        self.spin_pos_x.blockSignals(True)
        self.spin_pos_x.setValue(pos_x)
        self.spin_pos_x.blockSignals(False)
        self.slider_pos_y.blockSignals(True)
        self.slider_pos_y.setValue(pos_y)
        self.slider_pos_y.blockSignals(False)
        self.spin_pos_y.blockSignals(True)
        self.spin_pos_y.setValue(pos_y)
        self.spin_pos_y.blockSignals(False)

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
            self.chk_show_poem.setChecked(elem.get("show_poem", True))
            levels = elem.get("levels", ["extra"])
            self.chk_lv_primary.setChecked("primary" in levels)
            self.chk_lv_junior.setChecked("junior" in levels)
            self.chk_lv_senior.setChecked("senior" in levels)
            self.chk_lv_extra.setChecked("extra" in levels)
            ls_val = int(round(elem.get("line_spacing", 1.2) * 10))
            self.slider_poem_line_spacing.setValue(max(8, min(30, ls_val)))
            self.label_poem_ls.setText(f"{self.slider_poem_line_spacing.value() / 10:.1f}")
            self.chk_poem_marquee.setChecked(elem.get("marquee", False))
        if elem_id == "tip":
            tip_interval = elem.get("interval", self.project.tip_interval if hasattr(self.project, 'tip_interval') else self.project.typewriter_interval)
            self.spin_tip_interval.setValue(tip_interval)
        if elem_id == "static_text":
            self.edit_static_text.setText(elem.get("text", ""))
        if elem_id == "countdown":
            self.edit_expired_text.setText(self.project.expired_text)
            tmpl = getattr(self.project, 'display_format_template', '{days}天 {hours}时 {minutes}分')
            fmt = getattr(self.project, 'display_format', 'decimal')
            if fmt == "custom":
                if tmpl == "{days}天 {hours}时 {minutes}分":
                    fmt_idx = 2
                elif tmpl == "{hours}时 {minutes}分 {seconds}秒":
                    fmt_idx = 3
                else:
                    fmt_idx = 4
            else:
                fmt_idx = {"decimal": 0, "integer": 1, "hms": 3}.get(fmt, 0)
            self.combo_display_format.blockSignals(True)
            self.combo_display_format.setCurrentIndex(fmt_idx)
            self.combo_display_format.blockSignals(False)
            self.edit_format_template.setText(tmpl)
            self.custom_template_row.setVisible(fmt_idx == 4)

        self._updating_ui = False

    def _on_property_changed(self, *args):
        if self._updating_ui or not self.current_elem:
            return
        layout = self.project.custom_layout
        if self.current_elem not in layout:
            layout[self.current_elem] = {}
        elem = layout[self.current_elem]

        elem["visible"] = self.cb_visible.isChecked()
        elem["font_size"] = self.slider_font_size.value()
        elem["auto_width"] = self.cb_auto_width.isChecked()
        if self.current_elem == "weather":
            elem["auto_width"] = False
            elem["custom_width"] = self.slider_width.value()
            elem["custom_height"] = self.slider_height.value()
        elif elem["auto_width"]:
            elem.pop("custom_width", None)
            elem.pop("custom_height", None)
        else:
            elem["custom_width"] = self.slider_width.value()
            elem["custom_height"] = self.slider_height.value()
        elem["font_family"] = self.combo_font_family.currentText()
        elem["color"] = self.btn_color.property("color_value") or "#FFFFFF"
        elem["opacity"] = self.slider_opacity.value() / 100.0

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
            elem["show_poem"] = self.chk_show_poem.isChecked()
            levels = []
            if self.chk_lv_primary.isChecked(): levels.append("primary")
            if self.chk_lv_junior.isChecked(): levels.append("junior")
            if self.chk_lv_senior.isChecked(): levels.append("senior")
            if self.chk_lv_extra.isChecked(): levels.append("extra")
            elem["levels"] = levels
            elem["line_spacing"] = self.slider_poem_line_spacing.value() / 10.0
            elem["marquee"] = self.chk_poem_marquee.isChecked()
            if self.window and elem.get("show_poem", True) and elem.get("visible", False):
                if hasattr(self.window, 'start_typewriter_animation'):
                    self.window.typewriter_timer.start(self.project.typewriter_interval * 60000)
                    QTimer.singleShot(50, self.window.start_typewriter_animation)
        if self.current_elem == "tip":
            self.project.tip_interval = self.spin_tip_interval.value()
            elem["interval"] = self.project.tip_interval
            if self.window and elem.get("visible", False):
                if hasattr(self.window, 'start_tip_animation'):
                    self.window.tip_timer.start(self.project.tip_interval * 60000)
                    QTimer.singleShot(50, self.window.start_tip_animation)
        if self.current_elem == "static_text":
            elem["text"] = self.edit_static_text.text()
        if self.current_elem == "countdown":
            self.project.expired_text = self.edit_expired_text.text()
            fmt_map = {0: "decimal", 1: "integer", 2: "custom", 3: "custom", 4: "custom"}
            self.project.display_format = fmt_map.get(self.combo_display_format.currentIndex(), "decimal")
            self.project.display_format_template = self.edit_format_template.text()
            if self.window and hasattr(self.window, 'countdown_label'):
                self.window.countdown_label.set_display_format(
                    self.project.display_format, self.project.display_format_template)
                self.window._update_tick_interval()
                self.window.update_ticking_countdown()

        self.preview_canvas.refresh_layout()
        self._update_list_item_text()
        if self.window:
            self.window.apply_custom_layout()
        self._mark_dirty()

    def _on_pos_changed(self, _val):
        if self._updating_ui or not self.current_elem:
            return
        px = self.slider_pos_x.value()
        py = self.slider_pos_y.value()
        self.spin_pos_x.blockSignals(True)
        self.spin_pos_x.setValue(px)
        self.spin_pos_x.blockSignals(False)
        self.spin_pos_y.blockSignals(True)
        self.spin_pos_y.setValue(py)
        self.spin_pos_y.blockSignals(False)
        layout = self.project.custom_layout
        if self.current_elem in layout:
            layout[self.current_elem]["x"] = px / 100.0
            layout[self.current_elem]["y"] = py / 100.0
        self.preview_canvas.refresh_layout()
        if self.window:
            self.window.apply_custom_layout()
        self._mark_dirty()

    def _on_pos_x_spin(self, val):
        self.slider_pos_x.blockSignals(True)
        self.slider_pos_x.setValue(val)
        self.slider_pos_x.blockSignals(False)
        self._on_pos_changed(val)

    def _on_pos_y_spin(self, val):
        self.slider_pos_y.blockSignals(True)
        self.slider_pos_y.setValue(val)
        self.slider_pos_y.blockSignals(False)
        self._on_pos_changed(val)

    def _update_list_item_text(self):
        if not self.current_elem: return
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == self.current_elem:
                display = ELEMENT_DISPLAY_NAMES.get(self.current_elem, self.current_elem)
                icon = "👁️" if self.project.custom_layout.get(self.current_elem, {}).get("visible", True) else "🚫"
                item.setText(f"{icon}  {display}")
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
        self.spin_opacity.blockSignals(True)
        self.spin_opacity.setValue(val)
        self.spin_opacity.blockSignals(False)
        self._on_property_changed()

    def _on_opacity_spin(self, val):
        self.slider_opacity.blockSignals(True)
        self.slider_opacity.setValue(val)
        self.slider_opacity.blockSignals(False)
        self._on_property_changed()

    def _on_font_size_slider(self, val):
        self.spin_font_size.blockSignals(True)
        self.spin_font_size.setValue(val)
        self.spin_font_size.blockSignals(False)
        self._on_property_changed()

    def _on_font_size_spin(self, val):
        self.slider_font_size.blockSignals(True)
        self.slider_font_size.setValue(val)
        self.slider_font_size.blockSignals(False)
        self._on_property_changed()

    def _on_auto_width_toggled(self, checked):
        if self._updating_ui or not self.current_elem:
            return
        self.manual_size_widget.setVisible(not checked)
        elem = (self.project.custom_layout or {}).get(self.current_elem, {})
        if not checked:
            rect = self.preview_canvas._get_elem_rect(self.current_elem, elem)
            canvas_rect = self.preview_canvas._get_canvas_rect()
            scale = canvas_rect.width() / self.project.size[0] if self.project.size[0] > 0 else 1.0
            cw = int(elem.get("custom_width", rect.width() / scale))
            ch = int(elem.get("custom_height", rect.height() / scale))
            self.slider_width.setValue(max(30, cw))
            self.slider_height.setValue(max(20, ch))
        self._on_property_changed()

    def _on_manual_size_changed(self, _=0):
        if self._updating_ui or not self.current_elem:
            return
        elem = (self.project.custom_layout or {}).get(self.current_elem, {})
        w, h = self.slider_width.value(), self.slider_height.value()
        if elem.get("type") == "custom_image":
            aspect = elem.get("img_aspect")
            if aspect and aspect > 0:
                sender = self.sender()
                if sender is self.slider_width:
                    h = max(20, int(w / aspect))
                    self.slider_height.blockSignals(True)
                    self.slider_height.setValue(h)
                    self.slider_height.blockSignals(False)
                else:
                    w = max(30, int(h * aspect))
                    self.slider_width.blockSignals(True)
                    self.slider_width.setValue(w)
                    self.slider_width.blockSignals(False)
        self.spin_width.blockSignals(True)
        self.spin_width.setValue(w)
        self.spin_width.blockSignals(False)
        self.spin_height.blockSignals(True)
        self.spin_height.setValue(h)
        self.spin_height.blockSignals(False)
        self._on_property_changed()

    def _on_manual_size_spin(self, _=0):
        if self._updating_ui or not self.current_elem:
            return
        sender = self.sender()
        if sender is self.spin_width:
            self.slider_width.blockSignals(True)
            self.slider_width.setValue(self.spin_width.value())
            self.slider_width.blockSignals(False)
        elif sender is self.spin_height:
            self.slider_height.blockSignals(True)
            self.slider_height.setValue(self.spin_height.value())
            self.slider_height.blockSignals(False)
        elem = (self.project.custom_layout or {}).get(self.current_elem, {})
        w, h = self.slider_width.value(), self.slider_height.value()
        if elem.get("type") == "custom_image":
            aspect = elem.get("img_aspect")
            if aspect and aspect > 0:
                if sender is self.spin_width:
                    h = max(20, int(w / aspect))
                    self.slider_height.blockSignals(True)
                    self.slider_height.setValue(h)
                    self.slider_height.blockSignals(False)
                    self.spin_height.blockSignals(True)
                    self.spin_height.setValue(h)
                    self.spin_height.blockSignals(False)
                else:
                    w = max(30, int(h * aspect))
                    self.slider_width.blockSignals(True)
                    self.slider_width.setValue(w)
                    self.slider_width.blockSignals(False)
                    self.spin_width.blockSignals(True)
                    self.spin_width.setValue(w)
                    self.spin_width.blockSignals(False)
        self._on_property_changed()

    def persist_layout(self):
        if self.window and hasattr(self.window, 'master'):
            self.window.master.save_config(force=True)

    def _on_display_format_changed(self, index):
        if index == 2:
            self.edit_format_template.blockSignals(True)
            self.edit_format_template.setText("{days}天 {hours}时 {minutes}分")
            self.edit_format_template.blockSignals(False)
        elif index == 3:
            self.edit_format_template.blockSignals(True)
            self.edit_format_template.setText("{hours}时 {minutes}分 {seconds}秒")
            self.edit_format_template.blockSignals(False)
        self.custom_template_row.setVisible(index == 4)
        self._on_property_changed()

    def _insert_template_token(self, token):
        le = self.edit_format_template
        le.blockSignals(True)
        cursor = le.cursorPosition()
        text = le.text()
        new_text = text[:cursor] + token + text[cursor:]
        le.setText(new_text)
        le.setCursorPosition(cursor + len(token))
        le.blockSignals(False)
        self._on_property_changed()

    def add_element(self):
        layout = self.project.custom_layout or {}
        existing = set(layout.keys())
        available = [e for e in ALL_AVAILABLE_ELEMENTS if e not in existing]
        multi_elements = ["custom_text", "custom_image"] + EXTRA_ELEMENTS
        all_available = available + multi_elements
        display_items = []
        for e in all_available:
            if e == "custom_text": display_items.append("📝 自定义文字")
            elif e == "custom_image": display_items.append("🖼️ 自定义图片")
            else: display_items.append(ELEMENT_DISPLAY_NAMES.get(e, e))
        if not display_items:
            QMessageBox.information(self, "提示", "所有可用元素已添加（装饰图形和分割线可重复添加）")
            return
        choice, ok = QInputDialog.getItem(self, "添加元素", "选择要添加的元素：", display_items, 0, False)
        if not ok: return
        idx = display_items.index(choice)
        elem_id = all_available[idx]

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
        elif elem_id == "deco_shape":
            shape_types = ["矩形", "圆形"]
            choice, ok = QInputDialog.getItem(self, "选择形状", "选择图形类型：", shape_types, 0, False)
            if not ok: return
            shape_type = "rectangle" if choice == "矩形" else "circle"
            unique_id = f"deco_shape_{int(time.time())}"
            layout[unique_id] = {
                "visible": True, "x": 0.5, "y": 0.35, "custom_width": 120, "custom_height": 80,
                "opacity": 1.0, "color": "#4facfe",
                "stroke_color": "#3498db", "stroke_width": 2,
                "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 0, "shadow_blur": 0,
                "bg_color": "transparent", "bg_radius": 8,
                "alignment_h": "center", "alignment_v": "center", "auto_width": False,
                "type": "deco_shape", "shape_type": shape_type
            }
            shape_icon = "▬" if shape_type == "rectangle" else "●"
            ELEMENT_DISPLAY_NAMES[unique_id] = f"🎨 {shape_icon} {choice}"
        elif elem_id == "divider":
            unique_id = f"divider_{int(time.time())}"
            layout[unique_id] = {
                "visible": True, "x": 0.5, "y": 0.45, "custom_width": 200, "custom_height": 3,
                "opacity": 0.6, "color": "#666666",
                "stroke_color": "transparent", "stroke_width": 0,
                "shadow_color": "#000000", "shadow_offset_x": 0, "shadow_offset_y": 0, "shadow_blur": 0,
                "bg_color": "transparent", "bg_radius": 2,
                "alignment_h": "center", "alignment_v": "center", "auto_width": False,
                "type": "divider"
            }
            ELEMENT_DISPLAY_NAMES[unique_id] = f"➖ 分割线"
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
            if elem_id == "weather":
                layout[elem_id]["width"] = 0.10
                layout[elem_id]["height"] = 0.16
                layout[elem_id]["auto_width"] = False
                layout[elem_id]["custom_width"] = 140
                layout[elem_id]["custom_height"] = 160
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

    def _on_element_rows_moved(self, parent, start, end, dest, dest_row):
        new_keys = []
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            if item:
                new_keys.append(item.data(Qt.ItemDataRole.UserRole))
        layout = self.project.custom_layout or {}
        self.project.custom_layout = {k: layout[k] for k in new_keys if k in layout}
        self._on_property_changed()

    # ---------- 窗口级外观设置方法 ----------
    def _on_win_bg_type_changed(self, text):
        is_color = "纯色" in text
        is_image = "图片" in text
        is_grad = "渐变" in text
        is_dyn = "动态" in text
        is_trans = "透明" in text
        self.win_color_row.setVisible(is_color)
        self.win_grad_row.setVisible(is_grad)
        self.win_img_row.setVisible(is_image)
        self.win_dyn_row.setVisible(is_dyn)
        if self.win_alpha_row:
            self.win_alpha_row.setVisible(not is_trans)
        if self.win_radius_row:
            self.win_radius_row.setVisible(not is_trans)

    def _on_win_radius_changed(self, value):
        self.project.window_round_radius = value
        self.preview_canvas.update()
        if self.window:
            if self.window.bg_dynamic_widget and hasattr(self.window.bg_dynamic_widget, 'set_radius'):
                self.window.bg_dynamic_widget.set_radius(0 if self.window.is_fullscreen else value)
            self.window.update()

    def _on_win_radius_spin(self, value):
        self.win_radius_slider.blockSignals(True)
        self.win_radius_slider.setValue(value)
        self.win_radius_slider.blockSignals(False)
        self._on_win_radius_changed(value)

    def _on_win_alpha_spin(self, value):
        self.win_alpha_slider.blockSignals(True)
        self.win_alpha_slider.setValue(value)
        self.win_alpha_slider.blockSignals(False)
        self._on_win_alpha_preview(value)

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
                f"background-color: {color.name()}; border-radius: 4px; "
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
        self.setMinimumSize(460, 360)
        self.resize(500, 460)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        tc = get_theme_colors(self.app.theme)

        # ---- 项目信息 ----
        grp = QGroupBox("项目信息")
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

        self.date_widget = QWidget()
        date_layout = QHBoxLayout(self.date_widget)
        date_layout.setContentsMargins(0, 0, 0, 0)
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
        btn_cal.clicked.connect(lambda: self._show_calendar())
        date_layout.addWidget(btn_cal)
        self.date_label = QLabel(tr("target_date") + ":")
        form.addRow(self.date_label, self.date_widget)

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
        self.show_both_label = QLabel("")
        form.addRow(self.show_both_label, self.chk_show_both)

        self.chk_end_sound = QCheckBox("🔔 结束提示音")
        self.chk_end_sound.setChecked(getattr(self.project, 'enable_end_sound', True))
        self.chk_end_sound.setToolTip("倒计时归零时播放提示音")

        sound_row = QHBoxLayout()
        sound_row.setSpacing(6)
        self.combo_end_sound_mode = QComboBox()
        self.combo_end_sound_mode.addItems([
            "🎐 风铃(柔和)", "🎹 钢琴", "🔔 叮叮(双频)", "📢 哔哔哔(急促)",
            "📯 嘟——(长音)", "⏰ 闹钟(渐响)", "🌊 海浪潮汐", "🎹 电子合成", "📁 自定义"
        ])
        _mode_map = {"windchime": 0, "piano": 1, "double_ding": 2, "urgent_beep": 3,
                     "long_buzz": 4, "alarm_rise": 5, "ocean_wave": 6, "synth_arp": 7, "custom": 8}
        self.combo_end_sound_mode.setCurrentIndex(_mode_map.get(getattr(self.project, 'end_sound_mode', 'windchime'), 0))
        self.combo_end_sound_mode.setMinimumHeight(32)
        self.combo_end_sound_mode.currentIndexChanged.connect(self._on_end_sound_mode_changed)

        self.btn_browse_sound = QPushButton("▶ 试听")
        self.btn_browse_sound.setMinimumHeight(32)
        self.btn_browse_sound.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse_sound.clicked.connect(self._play_or_browse_sound)

        sound_row.addWidget(self.combo_end_sound_mode, 1)
        sound_row.addWidget(self.btn_browse_sound)
        form.addRow(self.chk_end_sound, sound_row)

        # 根据当前音效模式显示对应名称
        cur_mode = getattr(self.project, 'end_sound_mode', 'windchime')
        _mode_names = {"windchime": "🎐 风铃(柔和)", "piano": "🎹 钢琴", "double_ding": "🔔 叮叮(双频)",
                       "urgent_beep": "📢 哔哔哔(急促)", "long_buzz": "📯 嘟——(长音)",
                       "alarm_rise": "⏰ 闹钟(渐响)", "ocean_wave": "🌊 海浪潮汐",
                       "synth_arp": "🎹 电子合成", "custom": "📁 自定义"}
        _init_label_text = _mode_names.get(cur_mode, "🎐 风铃(柔和)")
        if cur_mode == "custom" and getattr(self.project, 'custom_sound_path', ''):
            _init_label_text = f"📁 {getattr(self.project, 'custom_sound_path', '')}"
        self._custom_sound_label = QLabel(_init_label_text)
        self._custom_sound_label.setStyleSheet(f"color: {tc['secondary_text']}; font-size: 11px;")
        form.addRow("", self._custom_sound_label)

        type_layout = QHBoxLayout()
        type_layout.setSpacing(8)
        self.combo_project_type = QComboBox()
        self.combo_project_type.addItems([tr("project_normal"), tr("project_recurring")])
        is_recurring = getattr(self.project, 'project_type', 'normal') == 'recurring'
        self.combo_project_type.setCurrentIndex(1 if is_recurring else 0)
        self.combo_project_type.setMinimumHeight(32)
        self.combo_project_type.currentIndexChanged.connect(self._on_project_type_changed)
        form.addRow(tr("project_type") + ":", self.combo_project_type)
        self.date_widget.setVisible(not is_recurring)
        self.date_label.setVisible(not is_recurring)
        self.chk_show_both.setVisible(not is_recurring)
        self.show_both_label.setVisible(not is_recurring)

        self.recur_box = QGroupBox(tr("recurring_settings"))
        recur_form = QFormLayout(self.recur_box)
        recur_form.setSpacing(8)
        wd_lay = QHBoxLayout()
        wd_lay.setSpacing(4)
        self.chk_weekdays = []
        for i, name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            chk = QCheckBox(name)
            chk.setChecked(i in (getattr(self.project, 'recur_weekdays', None) or []))
            self.chk_weekdays.append(chk)
            wd_lay.addWidget(chk)
        wd_lay.addStretch()
        recur_form.addRow(tr("recur_weekdays") + ":", wd_lay)

        end_lay = QHBoxLayout()
        end_lay.setSpacing(4)
        self.edit_recur_end = QLineEdit(getattr(self.project, 'recur_end_date', '') or '')
        self.edit_recur_end.setPlaceholderText("YYYY-MM-DD (" + tr("optional") + ")")
        self.edit_recur_end.setMinimumHeight(32)
        self.edit_recur_end.setStyleSheet(f"border-radius: 5px; padding: 4px 8px;")
        end_lay.addWidget(self.edit_recur_end)
        btn_end_cal = QPushButton("📅")
        btn_end_cal.setFixedWidth(36)
        btn_end_cal.setMinimumHeight(32)
        btn_end_cal.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_end_cal.setStyleSheet(f"background-color: {tc['input_bg']}; border: 1px solid {tc['border_color']}; border-radius: 5px; font-size: 16px;")
        btn_end_cal.clicked.connect(lambda: self._show_calendar(target=self.edit_recur_end))
        end_lay.addWidget(btn_end_cal)
        recur_form.addRow(tr("recur_end_date") + ":", end_lay)
        self.recur_box.setVisible(is_recurring)

        main_layout.addWidget(grp)
        main_layout.addWidget(self.recur_box)

        hint = QLabel("💡 字体、颜色、背景等外观设置请使用「自定义外观编辑器」")
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color: {tc['secondary_text']}; font-size: 11px; padding: 2px 4px;")
        main_layout.addWidget(hint)

        main_layout.addStretch()

        btn_save = QPushButton(tr("save"))
        btn_save.setMinimumHeight(40)
        btn_save.setProperty("primary", True)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.save_project)
        main_layout.addWidget(btn_save)

    def _on_project_type_changed(self, index):
        is_recurring = (index == 1)
        self.recur_box.setVisible(is_recurring)
        self.date_widget.setVisible(not is_recurring)
        self.date_label.setVisible(not is_recurring)
        self.chk_show_both.setVisible(not is_recurring)
        self.show_both_label.setVisible(not is_recurring)

    def _show_calendar(self, target=None):
        if target is None:
            target = self.edit_date
        if not hasattr(target, 'mapToGlobal'):
            log_message(f"_show_calendar 收到无效的 target: {type(target)}", "ERROR")
            return
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
            d = QDate.fromString(target.text().strip(), "yyyy-MM-dd")
            if d.isValid():
                cal.setSelectedDate(d)
        except Exception:
            pass
        cal.clicked.connect(lambda qdate: (
            target.setText(qdate.toString("yyyy-MM-dd")),
            cal_dlg.accept()
        ))
        cal_layout.addWidget(cal)
        cal_dlg.resize(310, 260)
        pos = target.mapToGlobal(target.rect().bottomLeft())
        cal_dlg.move(pos + QPoint(0, 4))
        cal_dlg.exec()

    def _on_end_sound_mode_changed(self, index):
        if index == 8:
            self.btn_browse_sound.setText("📁 浏览…")
        else:
            self.btn_browse_sound.setText("▶ 试听")
        _mode_names = {0: "🎐 风铃(柔和)", 1: "🎹 钢琴", 2: "🔔 叮叮(双频)",
                       3: "📢 哔哔哔(急促)", 4: "📯 嘟——(长音)",
                       5: "⏰ 闹钟(渐响)", 6: "🌊 海浪潮汐", 7: "🎹 电子合成", 8: "📁 自定义"}
        txt = _mode_names.get(index, "🎐 风铃(柔和)")
        if index == 8:
            cust = getattr(self.project, 'custom_sound_path', '')
            if cust:
                txt = f"📁 {cust}"
        self._custom_sound_label.setText(txt)

    def _play_or_browse_sound(self):
        idx = self.combo_end_sound_mode.currentIndex()
        if idx == 8:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择提示音文件", "", "音频文件 (*.wav *.mp3 *.ogg *.flac);;所有文件 (*)"
            )
            if not file_path:
                return
            sounds_dir = os.path.join(self.app.data_dir, "sounds")
            os.makedirs(sounds_dir, exist_ok=True)
            dest = os.path.join(sounds_dir, os.path.basename(file_path))
            try:
                if os.path.abspath(file_path) != os.path.abspath(dest):
                    import shutil
                    shutil.copy2(file_path, dest)
                rel = os.path.relpath(dest, self.app.data_dir)
                self.project.custom_sound_path = rel
                self._custom_sound_label.setText(rel)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"复制文件失败:\n{e}")
            if rel:
                self._custom_sound_label.setText(f"📁 {rel}")
            return

        _idx_to_mode = {0: "windchime", 1: "piano", 2: "double_ding", 3: "urgent_beep",
                        4: "long_buzz", 5: "alarm_rise", 6: "ocean_wave", 7: "synth_arp"}
        mode = _idx_to_mode.get(idx, "windchime")
        sound_map = {
            "windchime": "windchime.wav",
            "piano": "piano_ding.wav",
            "double_ding": "double_ding.wav",
            "urgent_beep": "urgent_beep.wav",
            "long_buzz": "long_buzz.wav",
            "alarm_rise": "alarm_rise.wav",
            "ocean_wave": "ocean_wave.wav",
            "synth_arp": "synth_arp.wav",
        }
        fname = sound_map.get(mode)
        if fname:
            sound_path = os.path.join(self.app.data_dir, "sounds", fname)
            if os.path.exists(sound_path):
                play_sound_file(sound_path)

    def save_project(self):
        is_recurring = self.combo_project_type.currentIndex() == 1
        date_str = self.edit_date.text().strip()
        if not is_recurring and not validate_date(date_str):
            QMessageBox.critical(self, "错误", "日期格式无效！请使用 YYYY-MM-DD")
            return
        time_str = self.edit_time.text().strip() if self.chk_exact_time.isChecked() else "00:00"
        if self.chk_exact_time.isChecked() and not validate_time(time_str):
            QMessageBox.critical(self, "错误", "时间格式无效！请使用 HH:MM")
            return

        self.project.name = self.edit_name.text().strip()
        if not is_recurring:
            self.project.target_date = date_str
        self.project.target_time = time_str
        self.project.show_both = self.chk_show_both.isChecked()

        self.project.enable_end_sound = self.chk_end_sound.isChecked()
        _idx_to_mode = {0: "windchime", 1: "piano", 2: "double_ding", 3: "urgent_beep",
                        4: "long_buzz", 5: "alarm_rise", 6: "ocean_wave", 7: "synth_arp", 8: "custom"}
        self.project.end_sound_mode = _idx_to_mode.get(self.combo_end_sound_mode.currentIndex(), "windchime")
        if self.project.end_sound_mode != "custom":
            self.project.custom_sound_path = ""

        if is_recurring:
            self.project.project_type = "recurring"
            weekdays = [i for i, chk in enumerate(self.chk_weekdays) if chk.isChecked()]
            if not weekdays:
                QMessageBox.critical(self, "错误", "循环项目请至少选择一个星期")
                return
            self.project.recur_weekdays = weekdays
            end_str = self.edit_recur_end.text().strip()
            if end_str:
                if not validate_date(end_str):
                    QMessageBox.critical(self, "错误", "结束日期格式无效！请使用 YYYY-MM-DD")
                    return
            self.project.recur_end_date = end_str
        else:
            self.project.project_type = "normal"
            self.project.recur_weekdays = []
            self.project.recur_end_date = ""

        self.app.save_config(force=True)
        for win in self.app.windows:
            if win.project == self.project:
                win.refresh()
        self.accept()


class WeatherDebugDialog(QDialog):
    """天气调试对话框 - 预览不同天气状态下的背景、圆形挂件和预报UI"""
    WEATHER_PRESETS = [
        ("晴 (白天)", "晴", True),
        ("晴 (夜晚)", "晴", False),
        ("多云 (白天)", "多云", True),
        ("多云 (夜晚)", "多云", False),
        ("阴天", "阴天", True),
        ("雾", "雾", True),
        ("霾", "霾", True),
        ("小雨", "小雨", True),
        ("中雨", "中雨", True),
        ("大雨", "大雨", True),
        ("雷暴", "雷暴", True),
        ("小雪", "小雪", True),
        ("大雪", "大雪", True),
    ]

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("倒计时·DJS - 天气调试预览")
        self.resize(720, 680)
        self._current_preset_idx = 0
        self._sunrise = "06:00"
        self._sunset = "18:00"
        theme = get_system_theme()
        c = get_theme_colors(theme)
        self.setStyleSheet(f"QDialog {{ background-color: {theme.bg_color}; color: {c['console_text']}; font-family: 'Microsoft YaHei'; }} QLabel {{ color: {c['console_text']}; }} QPushButton {{ background-color: {c['input_focus_border']}; color: white; border: none; border-radius: 4px; padding: 6px 12px; }} QPushButton:hover {{ background-color: {c['accent']}; }} QComboBox {{ background-color: {c['console_bg']}; color: {c['console_text']}; border: 1px solid {c['border_color']}; border-radius: 4px; padding: 4px 8px; }}")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 14, 14, 14)
        ctrl_row = QHBoxLayout()
        ctrl_row.addWidget(QLabel("天气状态:"))
        self.combo_preset = QComboBox()
        for name, _, _ in self.WEATHER_PRESETS:
            self.combo_preset.addItem(name)
        self.combo_preset.currentIndexChanged.connect(self._on_preset_changed)
        ctrl_row.addWidget(self.combo_preset, 1)
        self.btn_preview_dialog = QPushButton("预览天气预报UI")
        self.btn_preview_dialog.clicked.connect(self._on_preview_dialog)
        ctrl_row.addWidget(self.btn_preview_dialog)
        self.btn_preview_widget = QPushButton("预览圆形挂件")
        self.btn_preview_widget.clicked.connect(self._on_preview_widget)
        ctrl_row.addWidget(self.btn_preview_widget)
        layout.addLayout(ctrl_row)
        info_lbl = QLabel("💡 选择不同天气状态可预览对应的背景渐变、圆形挂件颜色和预报对话框 UI。\n日出/日落时间可在下方调整以模拟白天/黑夜。")
        info_lbl.setStyleSheet(f"color: {c['accent']}; font-size: 9pt;")
        info_lbl.setWordWrap(True)
        layout.addWidget(info_lbl)
        sun_row = QHBoxLayout()
        sun_row.addWidget(QLabel("日出:"))
        self.edit_sunrise = QLineEdit("06:00")
        self.edit_sunrise.setFixedWidth(60)
        sun_row.addWidget(self.edit_sunrise)
        sun_row.addWidget(QLabel("日落:"))
        self.edit_sunset = QLineEdit("18:00")
        self.edit_sunset.setFixedWidth(60)
        sun_row.addWidget(self.edit_sunset)
        self.btn_apply_sun = QPushButton("应用")
        self.btn_apply_sun.clicked.connect(self._on_apply_sun)
        sun_row.addWidget(self.btn_apply_sun)
        sun_row.addStretch()
        layout.addLayout(sun_row)
        self.preview_label = QLabel()
        self.preview_label.setMinimumHeight(380)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_label, 1)
        self._render_preview()

    def _current_preset(self):
        idx = self.combo_preset.currentIndex()
        if 0 <= idx < len(self.WEATHER_PRESETS):
            return self.WEATHER_PRESETS[idx]
        return ("晴 (白天)", "晴", True)

    def _on_preset_changed(self):
        self._render_preview()

    def _on_apply_sun(self):
        sr = self.edit_sunrise.text().strip()
        ss = self.edit_sunset.text().strip()
        if sr:
            self._sunrise = sr
        if ss:
            self._sunset = ss
        self._render_preview()

    def _render_preview(self):
        _, weather_text, is_day = self._current_preset()
        pix = QPixmap(self.preview_label.width() or 680, self.preview_label.height() or 380)
        pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = pix.width(), pix.height()
        ring_color = _weather_ring_color(weather_text)
        c_top, c_mid, c_bot = self._palette(weather_text, is_day)
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, c_top)
        grad.setColorAt(0.55, c_mid)
        grad.setColorAt(1.0, c_bot)
        painter.fillRect(pix.rect(), grad)
        if not is_day:
            painter.setPen(Qt.PenStyle.NoPen)
            rng = random.Random(42)
            for _ in range(60):
                sx = rng.random() * w
                sy = rng.random() * h * 0.5
                sa = rng.randint(60, 200)
                painter.setBrush(QColor(230, 240, 255, sa))
                painter.drawEllipse(QPointF(sx, sy), 1.2, 1.2)
        cd = min(150, h - 80)
        cx, cy = w / 2, h / 2 - 20
        painter.setPen(QPen(ring_color, max(2, cd // 28)))
        painter.setBrush(QColor(15, 22, 38, 180))
        painter.drawEllipse(QPointF(cx, cy), cd / 2, cd / 2)
        emoji = self._emoji_for(weather_text)
        emoji_font = QFont("Segoe UI Emoji")
        emoji_font.setPointSizeF(cd / 5.5)
        painter.setFont(emoji_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - cd / 2, cy - cd / 2 + 6, cd, cd * 0.45), Qt.AlignmentFlag.AlignCenter, emoji)
        temp_font = QFont("Microsoft YaHei")
        temp_font.setBold(True)
        temp_font.setPointSizeF(cd / 6.5)
        painter.setFont(temp_font)
        painter.setPen(QColor(240, 244, 248))
        painter.drawText(QRectF(cx - cd / 2, cy - 5, cd, cd / 2), Qt.AlignmentFlag.AlignCenter, "21°")
        city_font = QFont("Microsoft YaHei")
        city_font.setPointSizeF(cd / 14)
        painter.setFont(city_font)
        painter.setPen(QColor(200, 210, 220, 220))
        painter.drawText(QRectF(0, cy + cd / 2 + 6, w, 16), Qt.AlignmentFlag.AlignCenter, "安宁")
        info_font = QFont("Microsoft YaHei")
        info_font.setPointSizeF(10)
        painter.setFont(info_font)
        painter.setPen(QColor(255, 255, 255, 200))
        painter.drawText(QRectF(10, h - 50, w - 20, 20), Qt.AlignmentFlag.AlignLeft, f"天气: {weather_text}  |  {'白天' if is_day else '夜晚'}  |  日出 {self._sunrise}  日落 {self._sunset}")
        ring_str = f"圆环颜色 RGB({ring_color.red()},{ring_color.green()},{ring_color.blue()})"
        painter.drawText(QRectF(10, h - 30, w - 20, 20), Qt.AlignmentFlag.AlignLeft, ring_str)
        painter.end()
        self.preview_label.setPixmap(pix)

    def _emoji_for(self, text):
        if "雷" in text:
            return "⛈️"
        if "雪" in text:
            return "❄️"
        if "雨" in text:
            return "🌧️"
        if "雾" in text or "霾" in text:
            return "🌫️"
        if "阴" in text:
            return "☁️"
        if "晴" in text:
            return "☀️"
        if "多云" in text:
            return "⛅"
        return "🌤️"

    def _palette(self, weather_text, is_day):
        if "雷" in weather_text:
            return (QColor(28, 18, 48), QColor(45, 28, 70), QColor(60, 35, 90))
        if "雪" in weather_text:
            return (QColor(70, 90, 120) if is_day else QColor(40, 50, 80), QColor(120, 140, 170), QColor(180, 195, 215))
        if "大雨" in weather_text or "暴雨" in weather_text:
            return (QColor(25, 35, 55), QColor(40, 55, 80), QColor(55, 70, 95))
        if "雨" in weather_text:
            return (QColor(40, 55, 80) if is_day else QColor(20, 30, 55), QColor(60, 80, 110), QColor(85, 105, 135))
        if "雾" in weather_text or "霾" in weather_text:
            return (QColor(85, 90, 100), QColor(120, 125, 135), QColor(155, 160, 170))
        if "阴" in weather_text:
            return (QColor(55, 65, 80) if is_day else QColor(25, 30, 45), QColor(80, 90, 105), QColor(110, 120, 135))
        if "晴" in weather_text:
            if is_day:
                return (QColor(48, 102, 168), QColor(82, 134, 184), QColor(214, 142, 88))
            return (QColor(8, 12, 36), QColor(20, 18, 52), QColor(40, 24, 70))
        if "多云" in weather_text:
            if is_day:
                return (QColor(60, 95, 145), QColor(110, 140, 175), QColor(180, 165, 140))
            return (QColor(15, 20, 42), QColor(30, 30, 60), QColor(50, 35, 75))
        if is_day:
            return (QColor(48, 102, 168), QColor(82, 134, 184), QColor(214, 142, 88))
        return (QColor(8, 12, 36), QColor(20, 18, 52), QColor(40, 24, 70))

    def _on_preview_dialog(self):
        _, weather_text, is_day = self._current_preset()
        now = datetime.now()
        sr_h, ss_h = (6, 18)
        try:
            sr_h = int(self._sunrise.split(":")[0])
        except Exception:
            pass
        try:
            ss_h = int(self._sunset.split(":")[0])
        except Exception:
            pass
        now_min = now.hour * 60 + now.minute
        sr_min = sr_h * 60
        ss_min = ss_h * 60
        simulated_is_day = sr_min <= now_min < ss_min
        if is_day != simulated_is_day:
            if is_day:
                self._sunrise = f"{now.hour:02d}:00"
                self._sunset = f"{(now.hour + 12) % 24:02d}:00"
            else:
                self._sunset = f"{now.hour:02d}:00"
                self._sunrise = f"{(now.hour + 12) % 24:02d}:00"
        dlg = WeatherForecastDialog(25.0, 102.7, "安宁预览", self,
                                    provider="qweather", qw_key="", qw_host="",
                                    detailed_address="中国 云南省 昆明市 安宁市")
        dlg._weather_text = weather_text
        dlg.sunrise = f"2026-08-05T{self._sunrise}"
        dlg.sunset = f"2026-08-05T{self._sunset}"
        dlg.current_data = {
            "temp": "21", "feelsLike": "19", "text": weather_text,
            "icon": "", "wind": "西南风 2级", "humidity": "65",
            "obsTime": f"2026-08-05T{now.hour:02d}:{now.minute:02d}+08:00"
        }
        base_hour = now.hour
        dlg.hourly_data = []
        for i in range(24):
            h = (base_hour + i) % 24
            t = 18 + int(6 * math.sin((h - 6) / 24 * 2 * math.pi))
            pop = "30" if "雨" in weather_text else ("10" if "多云" in weather_text else "0")
            dlg.hourly_data.append({
                "time": f"2026-08-{5 if h >= base_hour else 6}T{h:02d}:00",
                "temp": str(t), "text": weather_text, "icon": "",
                "wind": "微风", "pop": pop, "humidity": "65", "precip": "0"
            })
        dlg._current_hour_idx = 0
        dlg.daily_data = []
        for i in range(7):
            d = now.day + i
            dlg.daily_data.append({
                "date": f"2026-08-{d:02d}", "max": str(25 + i % 3), "min": str(15 + i % 3),
                "text_day": weather_text, "icon_day": "", "text_night": weather_text, "icon_night": "",
                "sr": f"2026-08-{d:02d}T{self._sunrise}", "ss": f"2026-08-{d:02d}T{self._sunset}"
            })
        dlg.update_ui()
        dlg.exec()

    def _on_preview_widget(self):
        _, weather_text, _ = self._current_preset()
        for w in self.app.windows:
            if hasattr(w, 'weather_label') and hasattr(w.weather_label, 'setText'):
                temp = 21
                ring = _weather_ring_color(weather_text)
                display = f"{self._emoji_for(weather_text)} 安宁 {weather_text} {temp}°C"
                w.weather_label.setText(display)
                break


class TestPanel(QDialog):

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("倒计时·DJS - 测试面板")
        self.setMinimumSize(560, 620)
        self.resize(580, 700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        theme = get_system_theme()
        c = get_theme_colors(theme)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme.bg_color};
                color: {c['console_text']};
                font-family: 'Microsoft YaHei';
                font-size: 10pt;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {c['border_color']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 14px;
                color: {c['console_text']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }}
            QPushButton {{
                background-color: {c['input_focus_border']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 9pt;
            }}
            QPushButton:hover {{ background-color: {c['accent']}; }}
            QPushButton:pressed {{ background-color: {c['hover_accent']}; }}
            QSlider::groove:horizontal {{
                background: {c['border_color']};
                height: 6px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {c['input_focus_border']};
                width: 14px;
                height: 14px;
                border-radius: 7px;
                margin: -4px 0;
            }}
            QLineEdit {{
                background-color: {c['console_bg']};
                border: 1px solid {c['border_color']};
                border-radius: 4px;
                padding: 4px 8px;
                color: {c['console_text']};
            }}
            QLabel {{
                color: {c['console_text']};
            }}
            QCheckBox {{
                color: {c['console_text']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 14, 14, 14)

        # ── 到期闪烁 ──
        grp_blink = QGroupBox("到期闪烁")
        gl = QVBoxLayout(grp_blink)
        gl.setSpacing(6)

        row1 = QHBoxLayout()
        self.chk_blink = QCheckBox("启用闪烁")
        self.chk_blink.setChecked(True)
        self.chk_blink.toggled.connect(self._on_blink_toggle)
        row1.addWidget(self.chk_blink)
        row1.addStretch()
        lbl_speed = QLabel("速度:")
        row1.addWidget(lbl_speed)
        self.sld_blink = QSlider(Qt.Orientation.Horizontal)
        self.sld_blink.setRange(100, 2000)
        self.sld_blink.setValue(500)
        self.sld_blink.setFixedWidth(120)
        self.sld_blink.valueChanged.connect(self._on_blink_speed)
        row1.addWidget(self.sld_blink)
        self.lbl_blink_speed = QLabel("500ms")
        self.lbl_blink_speed.setFixedWidth(42)
        row1.addWidget(self.lbl_blink_speed)
        gl.addLayout(row1)

        row2 = QHBoxLayout()
        self.btn_blink_test = QPushButton("测试闪烁")
        self.btn_blink_test.clicked.connect(self._on_blink_test)
        row2.addWidget(self.btn_blink_test)
        self.btn_blink_stop = QPushButton("停止闪烁")
        self.btn_blink_stop.clicked.connect(self._on_blink_stop)
        row2.addWidget(self.btn_blink_stop)
        row2.addStretch()
        self.edit_blink_msg = QLineEdit()
        self.edit_blink_msg.setPlaceholderText("到期文字...")
        self.edit_blink_msg.setFixedWidth(140)
        row2.addWidget(self.edit_blink_msg)
        self.btn_blink_msg = QPushButton("应用")
        self.btn_blink_msg.clicked.connect(self._on_blink_msg)
        row2.addWidget(self.btn_blink_msg)
        gl.addLayout(row2)

        self.lbl_blink_status = QLabel("状态: —")
        self.lbl_blink_status.setStyleSheet(f"color: {c['input_focus_border']}; font-size: 9pt;")
        gl.addWidget(self.lbl_blink_status)

        layout.addWidget(grp_blink)

        # ── 声音测试 ──
        grp_sound = QGroupBox("声音测试")
        sl = QHBoxLayout(grp_sound)
        sl.setSpacing(8)
        self.btn_sound_piano = QPushButton("钢琴提示音")
        self.btn_sound_piano.clicked.connect(lambda: self._on_play_sound("piano"))
        sl.addWidget(self.btn_sound_piano)
        self.btn_sound_microwave = QPushButton("微波炉提示音")
        self.btn_sound_microwave.clicked.connect(lambda: self._on_play_sound("microwave"))
        sl.addWidget(self.btn_sound_microwave)
        self.btn_sound_custom = QPushButton("自定义...")
        self.btn_sound_custom.clicked.connect(self._on_play_custom_sound)
        sl.addWidget(self.btn_sound_custom)
        sl.addStretch()
        layout.addWidget(grp_sound)

        # ── 动画测试 ──
        grp_anim = QGroupBox("动画测试")
        al = QHBoxLayout(grp_anim)
        al.setSpacing(8)
        self.chk_flip = QCheckBox("翻页动画")
        self.chk_flip.setChecked(self.app.enable_flip_animation)
        self.chk_flip.toggled.connect(self._on_flip_toggle)
        al.addWidget(self.chk_flip)
        self.btn_typewriter = QPushButton("打字机测试")
        self.btn_typewriter.clicked.connect(self._on_typewriter_test)
        al.addWidget(self.btn_typewriter)
        self.btn_neon_pulse = QPushButton("霓虹脉冲")
        self.btn_neon_pulse.clicked.connect(self._on_neon_pulse_test)
        al.addWidget(self.btn_neon_pulse)
        al.addStretch()
        layout.addWidget(grp_anim)

        # ── 窗口操作 ──
        grp_win = QGroupBox("窗口操作")
        wl = QVBoxLayout(grp_win)
        wl.setSpacing(6)

        row_win = QHBoxLayout()
        self.btn_show_all = QPushButton("显示全部")
        self.btn_show_all.clicked.connect(self._on_show_all)
        row_win.addWidget(self.btn_show_all)
        self.btn_hide_all = QPushButton("隐藏全部")
        self.btn_hide_all.clicked.connect(self._on_hide_all)
        row_win.addWidget(self.btn_hide_all)
        self.btn_refresh_all = QPushButton("刷新全部")
        self.btn_refresh_all.clicked.connect(self._on_refresh_all)
        row_win.addWidget(self.btn_refresh_all)
        row_win.addStretch()
        wl.addLayout(row_win)

        row_alpha = QHBoxLayout()
        lbl_alpha = QLabel("透明度:")
        row_alpha.addWidget(lbl_alpha)
        self.sld_alpha = QSlider(Qt.Orientation.Horizontal)
        self.sld_alpha.setRange(10, 100)
        self.sld_alpha.setValue(100)
        self.sld_alpha.setFixedWidth(160)
        self.sld_alpha.valueChanged.connect(self._on_alpha_change)
        row_alpha.addWidget(self.sld_alpha)
        self.lbl_alpha_val = QLabel("1.0")
        self.lbl_alpha_val.setFixedWidth(30)
        row_alpha.addWidget(self.lbl_alpha_val)
        row_alpha.addStretch()
        wl.addLayout(row_alpha)

        self.lbl_win_count = QLabel(f"窗口数: {len(self.app.windows)}")
        self.lbl_win_count.setStyleSheet(f"color: {c['input_focus_border']}; font-size: 9pt;")
        wl.addWidget(self.lbl_win_count)

        layout.addWidget(grp_win)

        # ── 其他 ──
        grp_other = QGroupBox("调试与工具")
        ol1 = QHBoxLayout()
        ol1.setSpacing(8)
        self.btn_welcome = QPushButton("显示欢迎")
        self.btn_welcome.clicked.connect(self._on_show_welcome)
        ol1.addWidget(self.btn_welcome)
        self.btn_reset_welcome = QPushButton("重置欢迎")
        self.btn_reset_welcome.clicked.connect(self._on_reset_welcome)
        ol1.addWidget(self.btn_reset_welcome)
        self.btn_settings = QPushButton("打开设置")
        self.btn_settings.clicked.connect(lambda: self.app.open_settings())
        ol1.addWidget(self.btn_settings)
        ol1.addStretch()
        ol1_wrap = QHBoxLayout()
        ol1_wrap.addLayout(ol1)
        ol1_wrap.addStretch()

        ol2 = QHBoxLayout()
        ol2.setSpacing(8)
        self.btn_notify = QPushButton("测试通知")
        self.btn_notify.clicked.connect(self._on_test_notify)
        ol2.addWidget(self.btn_notify)
        self.btn_weather = QPushButton("刷新天气")
        self.btn_weather.clicked.connect(self._on_refresh_weather)
        ol2.addWidget(self.btn_weather)
        self.btn_weather_debug = QPushButton("天气调试")
        self.btn_weather_debug.clicked.connect(self._on_weather_debug)
        ol2.addWidget(self.btn_weather_debug)
        self.btn_gc = QPushButton("强制GC")
        self.btn_gc.clicked.connect(self._on_gc)
        ol2.addWidget(self.btn_gc)
        self.btn_backup = QPushButton("备份配置")
        self.btn_backup.clicked.connect(self._on_backup_config)
        ol2.addWidget(self.btn_backup)
        ol2.addStretch()
        ol2_wrap = QHBoxLayout()
        ol2_wrap.addLayout(ol2)
        ol2_wrap.addStretch()

        ol3 = QHBoxLayout()
        ol3.setSpacing(8)
        self.btn_app_info = QPushButton("应用信息")
        self.btn_app_info.clicked.connect(self._on_app_info)
        ol3.addWidget(self.btn_app_info)
        self.btn_perf_info = QPushButton("性能概览")
        self.btn_perf_info.clicked.connect(self._on_perf_info)
        ol3.addWidget(self.btn_perf_info)
        self.btn_threads = QPushButton("线程列表")
        self.btn_threads.clicked.connect(self._on_list_threads)
        ol3.addWidget(self.btn_threads)
        self.btn_clear_cache = QPushButton("清理缓存")
        self.btn_clear_cache.clicked.connect(self._on_clear_cache)
        ol3.addWidget(self.btn_clear_cache)
        ol3.addStretch()

        ol3_wrap = QHBoxLayout()
        ol3_wrap.addLayout(ol3)
        ol3_wrap.addStretch()

        ol4 = QHBoxLayout()
        ol4.setSpacing(8)
        self.btn_restart = QPushButton("重启应用")
        self.btn_restart.clicked.connect(self._on_restart)
        self.btn_restart.setStyleSheet("background-color: #e06c75;")
        ol4.addWidget(self.btn_restart)
        ol4.addStretch()

        gl = QVBoxLayout(grp_other)
        gl.setSpacing(6)
        gl.addLayout(ol1_wrap)
        gl.addLayout(ol2_wrap)
        gl.addLayout(ol3_wrap)
        gl.addLayout(ol4)
        layout.addWidget(grp_other)

        layout.addStretch()

        self._refresh_blink_status()

    def _refresh_blink_status(self):
        if not self.app.windows:
            self.lbl_blink_status.setText("状态: 无窗口")
            return
        w = self.app.windows[0]
        if hasattr(w, 'countdown_label'):
            info = w.countdown_label.blinkInfo()
            self.lbl_blink_status.setText(
                f"状态: enabled={info['enabled']} active={info['active']} "
                f"visible={info['visible']} interval={info['interval_ms']}ms expired={info['expired']}")

    def _on_blink_toggle(self, checked):
        for w in self.app.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.setBlinkEnabled(checked)
        self._refresh_blink_status()

    def _on_blink_speed(self, val):
        self.lbl_blink_speed.setText(f"{val}ms")
        for w in self.app.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.setBlinkSpeed(val)
        self._refresh_blink_status()

    def _on_blink_test(self):
        if not self.app.windows:
            return
        w = self.app.windows[0]
        if hasattr(w, 'countdown_label'):
            lbl = w.countdown_label
            lbl._expired = True
            lbl._expired_text = "[测试闪烁]"
            lbl._target_str = "[测试闪烁]"
            lbl._current_str = "[测试闪烁]"
            lbl._unit = ""
            lbl._blink_enabled = True
            lbl.startBlink()
        self._refresh_blink_status()

    def _on_blink_stop(self):
        for w in self.app.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.stopBlink()
        self._refresh_blink_status()

    def _on_blink_msg(self):
        msg = self.edit_blink_msg.text().strip() or "已到期"
        if not self.app.windows:
            return
        w = self.app.windows[0]
        if hasattr(w, 'countdown_label'):
            w.countdown_label.showExpired(msg)
        self._refresh_blink_status()

    def _on_play_sound(self, mode):
        sound_dir = os.path.join(self.app.data_dir, "sounds")
        if mode == "piano":
            path = os.path.join(sound_dir, "piano_ding.wav")
        else:
            path = os.path.join(sound_dir, "microwave_ding.wav")
        ensure_sound_assets(self.app.data_dir)
        if os.path.exists(path):
            play_sound_file(path)

    def _on_play_custom_sound(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择音频文件", "",
                                              "音频文件 (*.wav *.mp3 *.ogg *.flac);;所有文件 (*.*)")
        if path and os.path.exists(path):
            play_sound_file(path)

    def _on_flip_toggle(self, checked):
        self.app.enable_flip_animation = checked
        for w in self.app.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.enable_flip_animation = checked
            if hasattr(w, 'fullscreen_flip_clock') and w.fullscreen_flip_clock:
                w.fullscreen_flip_clock.setEnableFlip(checked)
        self.app.save_config(force=True)

    def _on_typewriter_test(self):
        if not self.app.windows:
            return
        w = self.app.windows[0]
        if hasattr(w, 'poem_label'):
            w.poem_label.start_animation("这是一段打字机效果测试文字——春风得意马蹄疾，一日看尽长安花。")

    def _on_neon_pulse_test(self):
        if not self.app.windows:
            return
        w = self.app.windows[0]
        if hasattr(w, 'countdown_label'):
            lbl = w.countdown_label
            use_neon = getattr(lbl, 'use_neon', False)
            if use_neon:
                lbl.use_neon = False
                self.btn_neon_pulse.setText("霓虹脉冲")
            else:
                lbl.use_neon = True
                lbl._pulse_phase = 0.0
                self.btn_neon_pulse.setText("霓虹脉冲 ✓")

    def _on_show_all(self):
        for w in self.app.windows:
            w.show()
        self.lbl_win_count.setText(f"窗口数: {len(self.app.windows)}")

    def _on_hide_all(self):
        for w in self.app.windows:
            w.hide()
        self.lbl_win_count.setText(f"窗口数: {len(self.app.windows)}")

    def _on_refresh_all(self):
        for w in self.app.windows:
            w.refresh()
        self.lbl_win_count.setText(f"窗口数: {len(self.app.windows)}")

    def _on_alpha_change(self, val):
        alpha = val / 100.0
        self.lbl_alpha_val.setText(f"{alpha:.1f}")
        for w in self.app.windows:
            if hasattr(w, 'set_alpha'):
                w.set_alpha(alpha)

    def _on_test_notify(self):
        if hasattr(self.app, 'tray_icon') and self.app.tray_icon:
            self.app.tray_icon.tray.showMessage("测试通知", "这是一条来自测试面板的通知消息",
                                                QSystemTrayIcon.MessageIcon.Information, 3000)

    def _on_refresh_weather(self):
        for w in self.app.windows:
            if hasattr(w, '_refresh_weather'):
                w._refresh_weather()

    def _on_weather_debug(self):
        dlg = WeatherDebugDialog(self.app, self)
        dlg.exec()

    def _on_gc(self):
        import gc
        before = len(gc.get_objects())
        gc.collect()
        after = len(gc.get_objects())
        QMessageBox.information(self, "GC 完成", f"回收前: {before} 对象\n回收后: {after} 对象\n释放: {before - after} 对象")

    def _on_restart(self):
        reply = QMessageBox.question(self, "确认重启", "确定要重启应用吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.app.save_config(force=True)
            subprocess.Popen([sys.executable] + sys.argv)
            self.app.quit()

    def _on_show_welcome(self):
        if hasattr(self.app, '_show_welcome'):
            self.app._show_welcome()

    def _on_reset_welcome(self):
        self.app.launch_count = 0
        self.app._first_run_done = False
        self.app.save_config(force=True)
        QMessageBox.information(self, "重置完成", "欢迎窗口状态已重置。\n下次启动将显示欢迎窗口。")

    def _on_backup_config(self):
        config_path = self.app.config_path
        if os.path.exists(config_path):
            import shutil
            backup_dir = os.path.join(self.app.data_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            bp = os.path.join(backup_dir, f"config_backup_{ts}.json")
            shutil.copy2(config_path, bp)
            QMessageBox.information(self, "备份完成", f"配置已备份到:\n{bp}")
        else:
            QMessageBox.warning(self, "备份失败", "配置文件不存在")

    def _on_app_info(self):
        info = (
            f"版本: {self.app.current_version}\n"
            f"Python: {sys.version.split()[0]}\n"
            f"平台: {platform.platform()}\n"
            f"数据目录: {self.app.data_dir}\n"
            f"项目数: {len(self.app.projects)}\n"
            f"悬浮窗: {len(self.app.windows)}\n"
            f"启动次数: {getattr(self.app, 'launch_count', 0)}\n"
            f"翻页动画: {getattr(self.app, 'enable_flip_animation', True)}"
        )
        QMessageBox.information(self, "倒计时·DJS - 应用信息", info)

    def _on_perf_info(self):
        try:
            import psutil
            proc = psutil.Process()
            mem = proc.memory_info()
            info = (
                f"物理内存: {mem.rss / 1024 / 1024:.1f} MB\n"
                f"虚拟内存: {mem.vms / 1024 / 1024:.1f} MB\n"
                f"CPU: {proc.cpu_percent(interval=0.1):.1f}%\n"
                f"线程数: {proc.num_threads()}"
            )
        except ImportError:
            info = "psutil 未安装"
        import gc
        info += f"\n活跃线程: {threading.active_count()}\nGC对象数: {len(gc.get_objects())}"
        QMessageBox.information(self, "性能概览", info)

    def _on_list_threads(self):
        lines = []
        for t in threading.enumerate():
            d = "守护" if t.daemon else "普通"
            a = "运行中" if t.is_alive() else "已停止"
            lines.append(f"[{d}] {t.name} ({a})")
        lines.append(f"\n共 {threading.active_count()} 个线程")
        QMessageBox.information(self, "线程列表", "\n".join(lines))

    def _on_clear_cache(self):
        import shutil
        cleared = 0
        pycache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__")
        if os.path.isdir(pycache):
            shutil.rmtree(pycache, ignore_errors=True)
            cleared += 1
        QMessageBox.information(self, "清理完成", f"已清理 {cleared} 个缓存目录")


class DebugConsole(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("倒计时·DJS - 控制台")
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
        btn_clear.setAutoDefault(False)
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
        btn_help.setAutoDefault(False)
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
        text = self.input_line.text().strip()
        if not text:
            return
        builtin_cmds = ["help", "root", "exit", "quit", "exit()", "quit()",
                        "read_file", "write_file", "ls", "pwd", "cd", "classes",
                        "restart", "clear_cache", "perf_info", "close_window",
                        "open_settings", "backup_config", "theme_info",
                        "app_info", "list_threads", "gc_collect", "clear",
                        "test", "blink_info"]
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
        color_map = {
            "white": "#cdd6f4",
            "red": "#f38ba8",
            "green": "#a6e3a1",
            "cyan": "#89dceb",
            "yellow": "#f9e2af",
            "magenta": "#cba6f7",
        }
        hex_color = color_map.get(color, "#cdd6f4")
        escaped = str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        if newline:
            self.output.append(f'<span style="color:{hex_color};">{escaped}</span>')
        else:
            self.output.moveCursor(QTextCursor.MoveOperation.End)
            self.output.insertHtml(f'<span style="color:{hex_color};">{escaped}</span>')
            self.output.ensureCursorVisible()

    def write_error(self, text):   self.write(text, "red")
    def write_success(self, text): self.write(text, "green")
    def write_info(self, text):    self.write(text, "cyan")
    def write_warning(self, text): self.write(text, "yellow")

    def execute_command(self):
        cmd = self.input_line.text().strip()
        if not cmd:
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
        elif cmd_lower == "welcome":
            self._cmd_welcome()
        elif cmd_lower == "reset_welcome":
            self._cmd_reset_welcome()
        elif cmd_lower == "toggle_log":
            self._cmd_toggle_log()
        elif cmd_lower.startswith("close_window"):
            arg = cmd[13:].strip()
            self._cmd_close_window(arg if arg else None)
        elif cmd_lower == "test":
            self._test_panel = TestPanel(self.app, self)
            self._test_panel.show()
            self.write_success("测试面板已打开")
        elif cmd_lower == "blink_info":
            self._cmd_blink_info()
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

    def _cmd_welcome(self):
        self.write_info("正在打开欢迎窗口...")
        self.app._show_welcome()

    def _cmd_reset_welcome(self):
        self.app.launch_count = 0
        self.app._first_run_done = False
        self.app.save_config(force=True)
        self.write_info("已重置欢迎窗口状态。下次启动将显示欢迎窗口（打包前执行此命令，新用户首次运行即可看到欢迎）。")

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

    def _cmd_blink_info(self):
        """查看到期闪烁状态（所有窗口）"""
        wins = self.app.windows
        if not wins:
            self.write_warning("没有打开的窗口")
            return
        self.write("到期闪烁状态:", color="cyan")
        for i, w in enumerate(wins):
            if hasattr(w, 'countdown_label'):
                info = w.countdown_label.blinkInfo()
                self.write(
                    f"  [窗口{i}] {w.project.name}: enabled={info['enabled']} "
                    f"active={info['active']} visible={info['visible']} "
                    f"interval={info['interval_ms']}ms expired={info['expired']}")
            else:
                self.write_warning(f"  [窗口{i}] {w.project.name}: 无 countdown_label")

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
                dlg.setWindowTitle("🔌 倒计时·DJS - 插件管理")
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

    def show_help(self):
        help_text = f"""
  ╔══════════════════════════ 控制台命令列表 ═══════════════════════════╗
  ║  版本: {self.app.current_version}
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
  │  welcome          打开欢迎窗口
  │  reset_welcome    重置欢迎窗口（打包前执行，让新用户首次看到欢迎）
  │  close_window [N] 关闭指定悬浮窗（不传参数列出所有窗口）
  │  toggle_log       切换日志转发开关（同顶部复选框）             
  │  read_file <路径> 读取文件内容（最多显示 5000 字符）           
  │  write_file <路径> <内容>  写入文件                    
  │  ls [路径]        列出目录内容                         
  │  pwd              显示当前工作目录                     
  │  cd <目录>        切换工作目录                         
  │  classes [类名]   列出所有类 / 查看类的继承链和方法             
  └──────────────────────────────────────────────────────────┘

  ┌──【窗口操作】──────────────────────────────────────────────┐
  │  list_windows()        列出所有悬浮窗                       
  │  show_windows()        显示所有悬浮窗                       
  │  hide_windows()        隐藏所有悬浮窗                       
  │  refresh_windows()     刷新所有悬浮窗                       
  │  set_window_alpha(0.8) 设置悬浮窗透明度 (0.1~1.0)            
  │  get_focused_window()  获取当前焦点控件                      
  ├──────────────────────────────────────────────────────────┤
  │  test                 打开测试面板（快速测试各项功能）      
  │  blink_info           查看到期闪烁状态（所有窗口）          
  └──────────────────────────────────────────────────────────┘

  ┌──【项目管理】──────────────────────────────────────────────────┐
  │  list_projects()       列出所有项目                          
  │  current_project(N)    查看/设置当前项目                       
  │  dump_project(N)       打印项目完整配置 (JSON)                 
  └─────────────────────────────────────────────────────────────┘

  ┌──【配置与主题】────────────────────────────────────────────────┐
  │  save_config()         保存配置                               
  │  reload_theme()        重新加载主题                             
  │  set_debug_level(N)    设置调试等级 (0=关闭 1=错误 2=信息 3=详细)
  │  backup_config         备份当前配置                             
  └─────────────────────────────────────────────────────────────┘

  ┌──【插件管理】─────────────────────────────────────────────────┐
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
  └─────────────────────────────────────────────────────────────┘

  ┌──【日志操作】──────────────────────────────────────────────────┐
  │  log("msg","INFO")     手动写入日志            
  │  show_log(50)          显示最近 N 行日志        
  │  clear_log()           清空日志文件            
  │  clear_screen()        清空控制台显示           
  │  clear                 清屏（内建命令）          
  │  toggle_log            切换日志实时转发到控制台      
  │  📋 顶部复选框         开启/关闭日志转发（默认关闭防刷屏）      
  └─────────────────────────────────────────────────────────────┘

  ┌──【其他工具】─────────────────────────────────────────────────┐
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
        self.write(help_text.strip(), color="white")

    def _show_welcome(self):
        username = getpass.getuser()
        self.write(f"Python {sys.version.split()[0]} 调试控制台 {self.app.current_version}", color="cyan")
        self.write(f"用户: {username}", color="yellow")

        if username.lower() == "guzhi":
            self.write("你好，开发者：GuZhi，欢迎您", color="magenta")

        if self.root_eligible:
            self.write_success("保留所有权限")
        else:
            self.write_warning("保留有限权限")

        self.write(f"日志转发: {'开启（日志会实时显示）' if self.log_forward_enabled else '关闭（推荐：防止刷屏）'}", color="green")
        self.write(f"输入 'help' 查看命令列表 | ↑↓ 历史 | Tab 补全 | 版本: {self.app.current_version}", color="green")

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
        QTreeWidgetItem(proj, ["🔄 循环项目设置"])
        QTreeWidgetItem(proj, ["🎨 自定义外观入门"])
        QTreeWidgetItem(proj, ["🗑️ 删除项目"])
        self.nav_tree.addTopLevelItem(proj)

        appearance = QTreeWidgetItem(["🎨 深度定制"])
        QTreeWidgetItem(appearance, ["🖼️ 背景类型详解"])
        QTreeWidgetItem(appearance, ["🖼️ 壁纸选择器"])
        QTreeWidgetItem(appearance, ["📝 文字元素样式"])
        QTreeWidgetItem(appearance, ["🌐 布局编辑器详解"])
        QTreeWidgetItem(appearance, ["✨ 动态壁纸机制"])
        QTreeWidgetItem(appearance, ["🍅 番茄钟使用"])
        QTreeWidgetItem(appearance, ["🌤️ 天气挂件配置"])
        QTreeWidgetItem(appearance, ["📜 诗词格言轮播"])
        QTreeWidgetItem(appearance, ["➕ 自定义文字/图片"])
        QTreeWidgetItem(appearance, ["🖱️ 鼠标穿透模式"])
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
            <h1>🎉 欢迎使用 倒计时·DJS</h1>
            <p>倒计时·DJS 是一款面向桌面用户的多功能倒计时工具，核心功能一览：</p>
            <ul>
            <li><b>多项目独立倒计时</b>：每个项目对应一个独立悬浮窗，可分别设置目标日期与精确到时分的时间。</li>
            <li><b>自然日 / 工作日双模式</b>：内置中国法定节假日与调休规则，自动计算并显示剩余工作日。</li>
            <li><b>循环项目</b>：按星期重复的周期性倒计时（每周例会、每日打卡等），详见「🔄 循环项目设置」。</li>
            <li><b>所见即所得布局编辑器</b>：拖拽调整文字、图片、天气、番茄钟等元素位置，详见「🌐 布局编辑器详解」。</li>
            <li><b>动态壁纸引擎（GPU 着色器）</b>：内置星空、鼠标粒子、极光、天空四种动态背景，极光 / 天空优先使用 OpenGL + GLSL 在 GPU 上渲染，详见「✨ 动态壁纸机制」。</li>
            <li><b>壁纸选择器</b>：管理图片集合并按间隔自动轮播，可应用到悬浮窗或系统桌面，详见「🖼️ 壁纸选择器」。</li>
            <li><b>鼠标穿透模式</b>：让悬浮窗不阻挡操作，点击直接穿透到下层窗口，详见「🖱️ 鼠标穿透模式」。</li>
            <li><b>备份与还原</b>：一键备份所有项目和设置到 <code>data/backups/</code>，方便迁移与恢复。</li>
            <li><b>插件系统（CAC）</b>：支持第三方扩展动态背景、桌面挂件、设置面板等，详见「🔌 CAC插件系统」。</li>
            </ul>
            <p>本帮助文档将按目录分类引导您从入门到精通。遇到问题可参考「❓ 常见问题」章节。</p>
            """,
            "🖱️ 悬浮窗操作指南": """
            <h2>🖱️ 悬浮窗基本操作</h2>
            <ul>
            <li><b>移动窗口</b>：在窗口<b>中心区域</b>按住鼠标左键拖拽即可移动，窗口会自动吸附屏幕边缘。</li>
            <li><b>调整大小</b>：将鼠标移至窗口的<b>边缘或角落</b>，光标变为双向箭头时拖拽即可缩放，最小尺寸 250×150 像素。</li>
            <li><b>右键菜单</b>：右键点击悬浮窗弹出菜单，包含设置、置顶/取消置顶、全屏模式、鼠标穿透、关闭窗口、退出应用等。</li>
            <li><b>双击动作</b>：双击悬浮窗任意位置，快速打开<b>全局设置面板</b>。</li>
            <li><b>全屏模式</b>：进入后自动隐藏其他窗口，鼠标移动到右下角出现悬浮控制面板，可调节透明度、切换动态壁纸、调整帧率/画质等。</li>
            </ul>
            """,
            "⚙️ 第一次使用设置": """
            <h2>⚙️ 第一次使用指南</h2>
            <ol>
            <li><b>创建第一个项目</b>：右键悬浮窗 → 设置 → 项目管理 → 添加项目。默认名称“新项目”，目标日期 30 天后。</li>
            <li><b>编辑项目细节</b>：选中项目，点击“编辑项目”。可修改项目名称、目标日期（YYYY-MM-DD），勾选“设置精确时间”可精确到时分。</li>
            <li><b>调整外观</b>：选中项目后点击“自定义外观”进入布局编辑器，拖拽元素位置或在右侧属性面板修改颜色、字体、阴影等，所有修改实时生效。</li>
            <li><b>全局设置</b>：在“全局设置”标签页选择全局字体、开机自启动、渲染引擎（GPU 着色器加速）等。诗词级别已移至「自定义外观编辑器 → 诗语轻扬」元素属性中，可为每个项目单独配置。</li>
            <li><b>插件系统</b>：进入“插件管理”标签页，先开启插件系统（默认关闭），再将插件 <code>.py</code> 文件放入 <code>plugins</code> 文件夹，刷新并启用。</li>
            </ol>
            """,
            "➕ 创建项目": "<h2>➕ 创建项目</h2><p>在设置面板 → 项目管理 → 点击“添加项目”，新项目使用默认配置（目标日期 30 天后，纯色背景）。一个项目对应一个独立的悬浮窗，后续可在编辑项目对话框中修改全部参数。</p>",
            "✏️ 编辑项目": "<h2>✏️ 编辑项目</h2><p>选中项目后点击“编辑项目”，对话框可修改：<br>• 项目名称<br>• 目标日期与精确时间<br>• 是否同时显示自然日和工作日<br>• 字体大小及自动调整<br>• 窗口透明度（0.1~1.0）<br>• 背景类型：纯色、图片、渐变、动态壁纸<br>• 字体颜色<br>• 诗词切换间隔（分钟）</p>",
            "🔄 循环项目设置": """
            <h2>🔄 循环项目设置</h2>
            <p>除“普通”项目外，可将项目类型切换为<b>“循环”</b>，用于周期性重复的倒计时（每周例会、每日打卡、周末提醒等）。</p>
            <h3>配置步骤</h3>
            <ol>
            <li>在“编辑项目”对话框中将<b>项目类型</b>选为“循环”。</li>
            <li>下方展开“循环设置”区域：
            <ul>
            <li><b>重复星期</b>：勾选每周触发日（周一至周日，至少选一个）。</li>
            <li><b>目标时间</b>：沿用上方的“目标时间”（HH:MM）作为当天触发时刻。</li>
            <li><b>结束日期</b>：可选。留空表示永久循环；填写日期（YYYY-MM-DD）后超过该日不再触发。</li>
            </ul>
            </li>
            <li>保存后倒计时会自动计算<b>下一个符合条件</b>的触发时刻并显示剩余时间。</li>
            </ol>
            <h3>触发逻辑</h3>
            <ul>
            <li>从当前时刻起向后查找，跳到第一个<b>被勾选的星期</b>且时间尚未过去的时刻。</li>
            <li>触发时刻到达后会自动滚动到下一个符合条件的日期，无需手动重置。</li>
            <li>若设置了结束日期且已超过，悬浮窗显示“已结束”。</li>
            </ul>
            <p><b>提示</b>：循环项目同样支持自定义外观、背景、诗词等所有元素，与普通项目完全一致。</p>
            """,
            "🎨 自定义外观入门": "<h2>🎨 自定义外观编辑器</h2><p>本软件最强大的功能之一。左侧元素列表可增删元素，中间预览区<b>直接拖拽元素位置</b>（支持吸附和参考线），右侧属性面板精细调整每个元素的样式。所有修改实时生效。</p>",
            "🗑️ 删除项目": "<h2>🗑️ 删除项目</h2><p>选中项目后点击“删除项目”。注意：至少需要保留一个项目，无法删除最后一个项目。</p>",
            "🖼️ 背景类型详解": """
            <h2>🖼️ 背景类型详解</h2>
            <ul>
            <li><b>纯色</b>：单一颜色背景，可调节透明度。当透明度 &lt; 1.0 且圆角为 0 时，会自动启用 Windows 亚克力模糊效果（仅 Win10/11）。</li>
            <li><b>图片</b>：支持 JPG/PNG/BMP/GIF 格式，GIF 会自动播放动画。图片会拉伸铺满整个窗口，可在编辑项目时上传到 <code>data/user</code> 目录。</li>
            <li><b>渐变</b>：线性渐变，可自定义起点色和终点色，渐变方向为左上到右下。</li>
            <li><b>动态</b>：四种内置动态壁纸 —— <b>星空</b>、<b>鼠标粒子</b>、<b>极光</b>、<b>天空</b>。可调节帧率（30/60/120 FPS）和画质（高/中/低）。
            <ul>
            <li><b>极光 / 天空</b>优先使用 GPU 着色器（OpenGL Compatibility Profile + GLSL <code>#version 330</code>）渲染，默认 60 FPS；GPU 不可用或未开启时自动回退到 CPU + numpy 路径。</li>
            <li><b>天空全屏模式</b>会在左下角绘制一张登机牌横向卡片，卡片内含项目名、倒计时和诗词显示，简约设计不抢背景画面。</li>
            </ul>
            </li>
            </ul>
            """,
            "🖼️ 壁纸选择器": """
            <h2>🖼️ 壁纸选择器</h2>
            <p>壁纸选择器是独立壁纸管理模块，位于<b>设置中心 → 壁纸选择器</b>标签页。可管理一组图片并按设定间隔自动轮播，既能应用到悬浮窗背景，也能直接设置为系统桌面壁纸。</p>
            <h3>图片管理</h3>
            <ul>
            <li><b>添加图片</b>：点击“添加图片”，选择本地图片（JPG/PNG/BMP 等），可多选。</li>
            <li><b>删除</b>：选中列表中的图片后点击“删除”可移除（仅从列表移除，不删除原文件）。</li>
            <li><b>上移/下移</b>：调整列表顺序，影响“顺序”模式下的播放次序。</li>
            </ul>
            <h3>轮播设置</h3>
            <ul>
            <li><b>启用轮播</b>：勾选后开始按间隔自动切换壁纸。</li>
            <li><b>切换模式</b>：顺序（到末尾停止）/ 随机 / 循环（默认，列表顺序循环）。</li>
            <li><b>切换间隔</b>：单位秒，默认 60 秒。</li>
            <li><b>填充方式</b>：拉伸 / 自适应 / 居中 / 平铺。</li>
            <li><b>淡入淡出过渡</b>：勾选后切换时有淡入淡出效果。</li>
            </ul>
            <h3>应用目标</h3>
            <ul>
            <li><b>应用到悬浮窗</b>：将当前壁纸作为悬浮窗背景显示。</li>
            <li><b>应用到桌面</b>：调用系统 API 直接设置桌面壁纸（Windows/macOS/Linux 均支持）。</li>
            <li><b>双屏扩展</b>：勾选后可在主屏/副屏分别指定壁纸。</li>
            </ul>
            <p><b>提示</b>：壁纸选择器与项目的“图片背景”相互独立。若希望悬浮窗跟随轮播，请在项目背景类型中选择由壁纸选择器提供的来源。</p>
            """,
            "📝 文字元素样式": """
            <h2>📝 文字元素样式设置</h2>
            <p>在布局编辑器右侧选中任意文字元素（名称、倒计时、静态文字等），可设置：</p>
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
            <li><b>拖拽定位</b>：在预览画布上直接按住元素拖拽，位置以百分比形式保存（相对于窗口宽高）。</li>
            <li><b>网格与吸附</b>：开启“网格”显示辅助格子，开启“吸附”后拖拽时自动对齐其他元素位置或参考线（三分线、中心线）。</li>
            <li><b>参考线</b>：显示水平/垂直居中线及三等分线，帮助精确对齐。</li>
            <li><b>元素层级</b>：通过“上移”“下移”按钮调整元素渲染顺序，后添加的元素默认在上层。</li>
            <li><b>添加自定义元素</b>：点击“添加”按钮可添加自定义文字或自定义图片。文字内容可任意编辑，图片可从本地选择（自动复制到用户目录）。</li>
            <li><b>删除元素</b>：选中元素后点击“删除”（项目名称和倒计时不可删除）。</li>
            </ul>
            """,
            "✨ 动态壁纸机制": """
            <h2>✨ 动态壁纸工作原理</h2>
            <p>本应用提供四种内置动态背景，每种都针对不同的视觉氛围设计：</p>
            <ul>
            <li><b>星空模式</b>：生成数百个随机亮度的星星，缓慢向左飘移，亮度周期性闪烁，模拟夜空效果。</li>
            <li><b>鼠标粒子模式</b>：创建大量带颜色的小圆点，具备初始速度。鼠标移动时粒子受到“引力”或“斥力”影响，距离小于阈值时绘制连线；点击窗口产生涟漪扩散效果。</li>
            <li><b>极光（GPU 着色器）</b>：基于 GLSL 片段着色器在 <code>QOpenGLWindow</code> 中实时绘制 <b>5 层体积光幕（绿 / 青 / 紫 / 粉 / 蓝绿）</b>，配合远山剪影与星空，呈现 <b>3D 透视极光效果</b>。需在全局设置中开启“实验性：GPU 着色器加速”，且系统支持 OpenGL 时启用；否则自动回退到 CPU + numpy 版本（画质一致，但 CPU 占用更高）。</li>
            <li><b>天空（清晨）</b>：<b>黄金时刻天空 + 4 层 FBM 云朵 + 太阳辉光 + 丁达尔光束</b>，同样优先走 GPU 着色器路径（默认 60 FPS），回退逻辑同极光。GPU 着色器会根据画质设置动态调整 FBM 八度数、云层数量与光束开关，并内置帧耗时监控实现自动降级 / 恢复。全屏模式下使用左下角登机牌横向卡片展示项目信息与倒计时，简约设计不抢背景。</li>
            </ul>
            <h3>GPU 着色器引擎</h3>
            <p>极光与天空背景使用 <b>OpenGL 3.3 Compatibility Profile + GLSL <code>#version 330</code></b> 渲染。为兼容不同显卡驱动，引擎通过<b>多版本函数探测</b>依次尝试以下上下文，确保最大兼容性：</p>
            <ol>
            <li>3.3 Compatibility Profile（推荐）</li>
            <li>4.1 Core Profile</li>
            <li>2.0 NoProfile（最终回退）</li>
            </ol>
            <p>探测到可用上下文后即可获取对应版本的 OpenGL 函数指针并初始化着色器程序。</p>
            <h3>自动降级与 CPU 回退</h3>
            <ul>
            <li><b>GPU 着色器自动降级</b>：内置帧耗时监控，检测到性能压力时自动降低画质（减少 FBM 八度数、云层数量、跳过光束计算）或降低帧率；性能恢复时自动升回。</li>
            <li><b>CPU 回退</b>：GPU 不可用或未开启加速时，使用 numpy + QPainter 渲染，并启用同样的自适应降级逻辑（按帧耗时自动调整画质与帧率）。</li>
            <li><b>渲染暂停机制</b>：右键菜单、下拉框、布局编辑器对话框交互时会自动暂停 GL 渲染；鼠标悬停在面板上时降至 12 FPS，移开后恢复。</li>
            </ul>
            <h3>登机牌诗词显示</h3>
            <p>天空全屏模式下，左下角登机牌卡片内会显示诗词：<b>每 10 秒从诗词库随机切换</b>一首，诗词显示在登机牌<b>分割线（撕裂口）右侧底部</b>，与项目名、倒计时共同构成一张优雅的“航班信息卡”。详见「📜 诗词格言轮播」。</p>
            <p>您可以在全屏模式下的控制面板或项目编辑器中调整动态壁纸的帧率和画质，高画质会使用更多粒子/星星，低画质则减少数量以提升性能。</p>
            """,
            "🍅 番茄钟使用": """
            <h2>🍅 番茄钟使用说明</h2>
            <p>在布局编辑器中添加“番茄钟”元素后，该元素会显示一个圆形计时器。</p>
            <ul>
            <li><b>单击</b>：开始/暂停当前计时（专注或休息）。</li>
            <li><b>双击</b>：重置计时器，恢复到专注状态。</li>
            <li>您可以在编辑器中分别设置专注时长（默认 25 分钟）和休息时长（默认 5 分钟）。</li>
            <li>番茄钟计时结束后会自动切换到休息/专注，并发出视觉提示（当前无声音）。</li>
            </ul>
            """,
            "🌤️ 天气挂件配置": """
            <h2>🌤️ 天气挂件配置</h2>
            <p>在布局编辑器中添加“天气挂件”元素，然后在右侧属性面板选择省份和城市。天气挂件为<b>圆形环 + 图标 + 温度 + 城市</b>样式，外圈颜色会根据天气自动变化（晴=橙、多云=蓝灰、雨=蓝、雪=白、雷=紫、阴=灰、雾=灰）。</p>
            <h3>数据源</h3>
            <p>在<b>全局设置 → 天气源</b>中选择：</p>
            <ul>
            <li><b>和风天气</b>（默认）：使用内置免费配额，开箱即用；也可切换为“自定义”填入自己的 API Key 和 Host（推荐生产环境使用）。</li>
            <li><b>自定义</b>：填入自定义 URL 模板（用 <code>{city}</code> 占位符代表城市名），返回纯文本会直接显示在挂件上。</li>
            </ul>
            <h3>挂件尺寸</h3>
            <p>天气挂件<b>不使用“自动宽度”</b>，请在右侧属性面板的<b>宽度/高度</b>滑块中直接调整像素尺寸（最小 72×88）。预览与实际渲染尺寸完全一致。</p>
            <h3>刷新策略</h3>
            <ul>
            <li>窗口启动 3 秒后自动获取；窗口可见性变化时刷新；之后每 30 分钟自动刷新一次。</li>
            <li>点击天气挂件会弹出未来 7 天预报窗口（含逐小时气温、降水概率、AQI、穿衣指数，需先成功获取一次经纬度）。</li>
            </ul>
            <h3>故障处理</h3>
            <ul>
            <li>长时间显示“获取天气...”或“天气离线”：请检查网络连接、API Key 是否正确，或尝试重启应用。</li>
            <li>城市名显示为拼音：和风 GeoAPI 部分城市返回拼音，已自动回退到上级行政区中文名，无需处理。</li>
            </ul>
            """,
            "📜 诗词格言轮播": """
            <h2>📜 诗词格言轮播</h2>
            <p>诗词级别已移至<b>「自定义外观编辑器 → 诗语轻扬」</b>元素属性中，可为每个项目单独设置来源：</p>
            <ul>
            <li><b>无</b>：不显示诗词，改为显示小提示（如“保持专注”）。</li>
            <li><b>初级（primary）</b>：简单易懂的短句或诗句（小学阶段）。</li>
            <li><b>中级（junior）</b>：经典诗词名句（初中阶段）。</li>
            <li><b>高级（senior）</b>：更长或更深刻的诗句（高中阶段）。</li>
            <li><b>课外（extra）</b>：课外经典名句合集。</li>
            </ul>
            <p>诗词每隔一段时间（默认 15 分钟，可在项目编辑器中修改）会以打字机效果逐字显示在悬浮窗上。诗词数据存放在 <code>data/poems.json</code> 中，分 <code>primary / junior / senior / extra</code> 四个级别，您可以自行增删。</p>
            <h3>登机牌诗词功能</h3>
            <p><b>天空全屏模式</b>下，左下角登机牌卡片内会自动显示诗词：<b>每 10 秒从诗词库随机切换</b>一首，诗词显示在登机牌<b>分割线（撕裂口）右侧底部</b>。当诗词库为空或未加载时，登机牌会显示默认文案 <b>“保持专注 · 享受当下”</b>。登机牌诗词与悬浮窗上的“诗语轻扬”元素独立运作，可同时显示。</p>
            """,
            "➕ 自定义文字/图片": """
            <h2>➕ 添加自定义文字/图片</h2>
            <p>在布局编辑器中点击“添加”按钮，选择“自定义文字”或“自定义图片”。</p>
            <ul>
            <li><b>自定义文字</b>：输入任意文本，之后可以像其他文字元素一样调整位置、颜色、字体等。</li>
            <li><b>自定义图片</b>：选择本地图片文件（支持 PNG/JPG/GIF 等），图片会被复制到 <code>data/user/</code> 目录并显示在悬浮窗上。您还可以在属性面板中调整图片的尺寸。</li>
            </ul>
            """,
            "🖱️ 鼠标穿透模式": """
            <h2>🖱️ 鼠标穿透模式</h2>
            <p>鼠标穿透（Click-Through）模式让悬浮窗不再接收鼠标事件，所有点击会<b>直接传递到下方的窗口或桌面</b>，同时悬浮窗仍然正常显示倒计时内容。适合需要把倒计时当作纯展示层、又不希望它挡住操作的场景。</p>
            <h3>开启方式</h3>
            <ul>
            <li><b>右键菜单</b>：右键悬浮窗 → 勾选“🖱️ 鼠标穿透”。该选项为开关项，再次点击可关闭。</li>
            <li>开启后，悬浮窗无法再被左键拖拽或右键点击，需要先通过<b>系统托盘菜单</b>打开设置、或再次从托盘取消穿透。</li>
            </ul>
            <h3>注意事项</h3>
            <ul>
            <li>穿透状态会<b>随项目保存</b>，重启应用后仍保持上次的状态。</li>
            <li>穿透开启时，悬浮窗的右键菜单也无法弹出，请通过托盘图标操作。</li>
            <li>若同时启用窗口置顶 + 鼠标穿透，可实现“始终显示但不阻挡操作”的桌面装饰效果。</li>
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
            <li><b>权限管理</b>：点击“权限”按钮，可单独授予或撤销插件的文件读取、文件写入、网络访问、执行命令等权限。修改后即时生效。</li>
            <li><b>插件详情</b>：选中插件后右侧会显示详细信息，如果插件提供了自定义设置面板，也会显示在此处。</li>
            <li><b>日志查看</b>：下方“常规日志”显示插件的运行日志，“敏感操作”记录插件对文件、网络、命令的每次调用。</li>
            </ul>
            """,
            "🔒 权限模型详解": """
            <h2>🔒 插件权限模型</h2>
            <p>插件在代码中必须声明其需要的权限（通过 <code>requested_permissions</code> 属性），用户启用插件时会弹出确认窗口。</p>
            <p>PluginPermission 共 <b>18 个权限位</b>（IntFlag 位掩码）：</p>
            <table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse; width:100%;'>
              <tr style='background:#3498db; color:white;'><th>权限</th><th>说明</th></tr>
              <tr><td><code>FILE_READ</code></td><td>读取文件</td></tr>
              <tr><td><code>FILE_WRITE</code></td><td>写入/创建文件</td></tr>
              <tr><td><code>FILE_DELETE</code></td><td>删除文件</td></tr>
              <tr><td><code>NETWORK</code></td><td>网络连接（总开关）</td></tr>
              <tr><td><code>NETWORK_HTTP</code></td><td>HTTP 请求</td></tr>
              <tr><td><code>NETWORK_SOCKET</code></td><td>原始 Socket 连接</td></tr>
              <tr><td><code>COMMAND</code></td><td>执行系统命令（总开关）</td></tr>
              <tr><td><code>COMMAND_EXEC</code></td><td>子进程执行</td></tr>
              <tr><td><code>CLIPBOARD</code></td><td>剪贴板读写</td></tr>
              <tr><td><code>SYSTEM_INFO</code></td><td>读取系统信息</td></tr>
              <tr><td><code>NOTIFICATION</code></td><td>发送系统通知</td></tr>
              <tr><td><code>UI_INJECT</code></td><td>注入 UI / 修改界面</td></tr>
              <tr><td><code>EVENT_LISTEN</code></td><td>监听应用事件</td></tr>
              <tr><td><code>THREAD_SPAWN</code></td><td>创建线程</td></tr>
              <tr><td><code>PROCESS_SPAWN</code></td><td>创建子进程</td></tr>
              <tr><td><code>REGISTRY</code></td><td>注册表读写（Windows）</td></tr>
              <tr><td><code>ENV_READ</code></td><td>读取环境变量</td></tr>
              <tr><td><code>DANGEROUS_EVAL</code></td><td>eval / exec 动态执行（极高风险）</td></tr>
            </table>
            <p>插件运行时，Python 审计钩子会拦截所有敏感操作，如果插件未获得对应权限，会抛出 <code>PermissionError</code>，操作被阻止并记录到日志。</p>
            """,
            "🛠️ 开发插件 - 快速开始": """
            <h2>🛠️ 开发自己的插件 - 5 分钟入门</h2>
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
            <h3>注册自定义动态背景</h3>
            <p>插件可通过 <code>api.register_dynamic_bg(id_name, display_name, widget_class, border_radius=None)</code> 注册自定义动态背景。背景类需继承自 <code>QWidget</code>，并实现以下接口以便应用统一调度：</p>
            <ul>
            <li><code>set_fps(fps)</code>：设置目标帧率（30/60/120）。</li>
            <li><code>set_quality(quality)</code>：设置画质（"high"/"medium"/"low"）。</li>
            <li><code>set_radius(radius)</code>：设置圆角半径（与悬浮窗圆角同步）。</li>
            </ul>
            <pre><code>class MyBgWidget(QWidget):
    def set_fps(self, fps): ...
    def set_quality(self, q): ...
    def set_radius(self, r): ...

class MyPlugin(Plugin):
    def on_enable(self):
        self.api.register_dynamic_bg("my_bg", "我的背景", MyBgWidget, border_radius=12)
</code></pre>
            <h3>注册 GPU 着色器背景</h3>
            <p>若插件需要注册 GPU 着色器背景，请<b>先检测 <code>HAS_OPENGL</code></b>（由应用顶层导出的全局变量），再使用 <code>QOpenGLWindow</code> 实现渲染。着色器代码建议使用 GLSL <code>#version 330</code> 以保证兼容性：</p>
            <pre><code>try:
    from PyQt6.QtOpenGL import QOpenGLWindow
    import djs_pyqt6 as app_mod
    HAS_OPENGL = app_mod.HAS_OPENGL
except Exception:
    HAS_OPENGL = False

if HAS_OPENGL:
    class MyShaderWindow(QOpenGLWindow):
        _FS_SRC = '''#version 330
        varying vec2 vUv;
        uniform float uTime;
        void main() { gl_FragColor = vec4(vUv, 0.5+0.5*sin(uTime), 1.0); }'''
        # ... initializeGL / paintGL / resizeGL ...
</code></pre>
            <p>注册方式与普通背景相同：<code>api.register_dynamic_bg("my_shader_bg", "我的着色器背景", MyShaderWindow)</code>。</p>
            <h3>注册桌面挂件与设置面板</h3>
            <ul>
            <li><code>api.register_widget(id_name, display_name, widget_class)</code>：注册自定义桌面挂件。</li>
            <li><code>api.register_settings_panel(id_name, display_name, widget_class)</code> 或 <code>api.register_settings_widget(...)</code>：注册插件设置面板，显示在插件管理详情区域。</li>
            </ul>
            """,
            "📘 插件API完整参考": """
            <h2>📘 PluginAPI 完整方法列表</h2>
            <p>在插件代码中，通过 <code>self.api</code> 可以调用以下方法：</p>
            <table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse; width:100%;'>
              <tr style='background:#3498db; color:white;'><th>方法</th><th>说明</th></tr>
              <tr><td><code>api.log(message, level="INFO")</code></td><td>记录日志，显示在插件管理界面“常规日志”中。</td></tr>
              <tr><td><code>api.register_dynamic_bg(id_name, display_name, widget_class, border_radius=None)</code></td><td>注册自定义动态背景。背景类需继承 QWidget，建议实现 <code>set_fps / set_quality / set_radius</code>。可注册 GPU 着色器背景（需检测 HAS_OPENGL，使用 QOpenGLWindow）。</td></tr>
              <tr><td><code>api.update_dynamic_bg_radius(id_name, border_radius)</code></td><td>动态更新已注册背景的圆角半径，对所有使用该背景的悬浮窗立即生效。</td></tr>
              <tr><td><code>api.register_settings_panel(id_name, display_name, widget_class)</code></td><td>注册插件设置面板，显示在插件管理详情区域。</td></tr>
              <tr><td><code>api.register_widget(id_name, display_name, widget_class)</code></td><td>注册自定义桌面挂件。</td></tr>
              <tr><td><code>api.register_settings_widget(id_name, display_name, widget_class)</code></td><td>同 register_settings_panel，等价方法。</td></tr>
              <tr><td><code>api.get_config(key, default=None)</code></td><td>读取插件配置（JSON 存储）。</td></tr>
              <tr><td><code>api.set_config(key, value)</code></td><td>保存插件配置。</td></tr>
              <tr><td><code>api.show_notification(title, message)</code></td><td>显示系统通知（需系统托盘图标支持）。</td></tr>
            </table>
            <p>所有注册方法都会校验 <code>widget_class</code> 是否继承自 <code>QWidget</code>，并检查 <code>id_name</code> 是否重复，重复时会抛出 <code>ValueError</code>。</p>
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
              <li><b>日志转发开关</b>：工具栏上的复选框，默认<b>关闭</b>，避免日志刷屏。开启后系统日志将实时显示在控制台中。</li>
              <li><b>↑↓ 方向键</b>：浏览历史命令，方便重复执行。</li>
              <li><b>Tab 键</b>：自动补全命令名，输入前几个字母按 Tab 即可。</li>
              <li><b>清空/帮助按钮</b>：一键清屏或查看所有命令。</li>
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
              <tr><td><code>app_info</code></td><td>-</td><td>显示应用版本、Python 版本、系统环境信息</td></tr>
              <tr><td><code>list_threads</code></td><td>-</td><td>列出所有活跃线程及其状态</td></tr>
              <tr><td><code>backup_config</code></td><td>-</td><td>备份当前配置文件到 backups/ 目录</td></tr>
              <tr><td><code>open_settings</code></td><td>-</td><td>快速打开全局设置窗口</td></tr>
              <tr><td><code>toggle_log</code></td><td>-</td><td>切换日志转发开关（开/关）</td></tr>
              <tr><td><code>close_window</code></td><td>&lt;N&gt;</td><td>关闭第 N 个悬浮窗（从 0 开始编号）</td></tr>
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
              <li>日志转发默认关闭——执行命令的输出不会被日志冲刷掉。</li>
              <li>修改应用状态的命令会立即生效（如 set_window_alpha、set_debug_level）。</li>
              <li><code>restart</code> 会关闭所有窗口并重新加载，请确认已保存。</li>
              <li><code>close_window N</code> 会彻底删除对应的悬浮窗，操作不可撤销。</li>
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
            <li><b>倒计时不更新</b>：检查目标日期是否已过，已到期会显示“已到期”。如果工作日为 0，静态文字可能为空，但数字倒计时应该仍会更新。检查日志文件是否有错误。</li>
            <li><b>数字滚动不流畅</b>：数字滚动使用 QPropertyAnimation，通常很流畅。如果出现卡顿，可能是动态壁纸占用过高，请降低帧率或画质。</li>
            </ul>
            """,
            "❔ 天气/网络问题": """
            <h2>❔ 天气挂件或网络相关问题</h2>
            <ul>
            <li><b>天气不显示</b>：请确认是否联网。默认供应商为<b>和风天气</b>（内置免费配额），开箱即用；如仍失败可在<b>全局设置 → 天气源</b>切换为“自定义”并填入自己的和风 API Key/Host，或换用自定义 URL 模板。</li>
            <li><b>城市名显示为拼音</b>：和风 GeoAPI 个别城市 <code>name</code> 字段返回拼音，已自动回退到上级行政区中文名，无需处理。</li>
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
            <li><b>启用 GPU 着色器加速</b>：在<b>全局设置 → 渲染引擎</b>中勾选“实验性：GPU 着色器加速”，极光 / 天空背景将使用 OpenGL Compatibility Profile + GLSL 在 GPU 上渲染，CPU 占用极低且可稳定 60 FPS（推荐）。</li>
            <li><b>降低帧率</b>：将帧率从 60 FPS 降低到 30 FPS，CPU/GPU 占用会明显下降。</li>
            <li><b>降低画质</b>：选择“低画质”会减少粒子/星星数量。极光 / 天空背景（无论 GPU 还是 CPU 渲染）都会根据帧耗时<b>自动降级</b>（画质或帧率），性能恢复时自动升回。GPU 着色器在低画质下会减少 FBM 八度数、云层数量并跳过光束计算。</li>
            <li><b>关闭动态壁纸</b>：如果硬件配置较低，建议使用静态图片或纯色背景。</li>
            <li><b>鼠标粒子模式</b>：该模式下粒子数量较多且连线计算密集，对性能要求较高，CPU 回退渲染时尤为明显。</li>
            <li><b>渲染暂停机制</b>：右键菜单、下拉框、布局编辑器对话框交互时会自动暂停 GL 渲染；鼠标悬停在面板上时降至 12 FPS，移开后恢复。</li>
            </ul>
            """,
            "🖱️ 鼠标操作速查": "<h2>🖱️ 鼠标操作速查表</h2><ul><li>左键拖拽中心 → 移动窗口</li><li>左键拖拽边缘/角 → 调整大小</li><li>右键 → 上下文菜单</li><li>双击 → 打开设置</li><li>全屏模式下鼠标移动到右下角 → 显示控制面板</li></ul>",
            "⌨️ 键盘快捷键": "<h2>⌨️ 键盘快捷键</h2><ul><li>在设置界面按 <code>~</code> 或 <code>`</code> → 打开调试控制台</li><li>在全屏模式下，目前没有预设键盘快捷键，可通过鼠标控制面板操作。</li></ul>",
            "💡 效率小技巧": """
            <h2>💡 效率小技巧</h2>
            <ul>
            <li><b>快速复制项目</b>：目前没有“复制项目”按钮，但您可以手动编辑一个项目后，在配置文件中复制项目块（谨慎操作）。</li>
            <li><b>备份配置</b>：在设置中心使用“备份配置”按钮可一键将当前配置存档到 <code>data/backups/</code> 目录；通过“还原配置”按钮可从备份恢复（恢复后需重启应用生效）。</li>
            <li><b>自定义诗词</b>：编辑 <code>data/poems.json</code>，按照已有格式添加您喜欢的诗句。</li>
            <li><b>窗口置顶技巧</b>：右键菜单中切换“置顶窗口”，可使窗口始终浮在其他应用之上。</li>
            <li><b>桌面装饰</b>：组合“置顶窗口 + 鼠标穿透”可让倒计时常驻桌面且不阻挡操作，详见「🖱️ 鼠标穿透模式」。</li>
            <li><b>循环提醒</b>：把项目类型设为“循环”可实现每周例会、每日打卡等周期倒计时，详见「🔄 循环项目设置」。</li>
            </ul>
            """,
            "📦 版本信息": f"<h2>📦 版本信息</h2><p><b>当前版本</b>：{self.app.current_version}<br><b>构建号</b>：{self.app.build_version}<br><b>Python版本</b>：{self.app.python_version}<br><b>操作系统</b>：{platform.system()} {platform.release()}<br><b>数据目录</b>：{self.app.data_dir}</p>",
            "👨‍💻 致谢与贡献": """
            <h2>👨‍💻 致谢与贡献</h2>
            <p>本软件由 <b>苗睿轩</b> 开发维护。感谢所有测试人员、插件开发者以及提出宝贵建议的用户。</p>
            <ul>
                <li>苗睿轩 (guzhiawa@qq.com) - 核心开发者</li>
                <li>FIZ_xingchen - 提供多个新想法与功能</li>
            </ul>
            <p>如果您想报告问题或贡献代码，请发送意见和建议到 <a href="mailto:guzhiawa@qq.com">guzhiawa@qq.com</a>。</p>
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

        act_show = QAction("显示所有窗口", self)
        act_show.triggered.connect(self.master.create_windows)
        self.menu.addAction(act_show)

        act_hide = QAction("隐藏所有窗口", self)
        act_hide.triggered.connect(self.hide_all_windows)
        self.menu.addAction(act_hide)

        act_reset = QAction("重置窗口位置", self)
        act_reset.triggered.connect(self.reset_windows_position)
        self.menu.addAction(act_reset)

        act_exam = QAction("考试模式", self)
        act_exam.triggered.connect(self.master.open_exam_mode)
        self.menu.addAction(act_exam)

        act_holiday = QAction("更新假期数据", self)
        act_holiday.triggered.connect(self.master.update_holidays)
        self.menu.addAction(act_holiday)

        self.menu.addSeparator()

        self.act_click_through = QAction("鼠标穿透", self)
        self.act_click_through.setCheckable(True)
        self.act_click_through.toggled.connect(self.toggle_click_through_all)
        self.menu.addAction(self.act_click_through)

        self.menu.aboutToShow.connect(self._sync_tray_menu_state)

        self.menu.addSeparator()

        act_quit = QAction("退出", self)
        act_quit.triggered.connect(self.master.quit_app)
        self.menu.addAction(act_quit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_activated)
        self.tray.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.master.open_settings()

    def toggle_click_through_all(self, enabled):
        for window in getattr(self.master, 'windows', []):
            window.set_click_through(enabled, save=True)

    def _sync_tray_menu_state(self):
        windows = getattr(self.master, 'windows', [])
        any_ct = any(getattr(w.project, 'click_through', False) for w in windows) if windows else False
        self.act_click_through.blockSignals(True)
        self.act_click_through.setChecked(any_ct)
        self.act_click_through.blockSignals(False)

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

        self.current_version = "2.9.0-rc1"
        self.build_version = 102
        self.python_version = sys.version.split()[0]
        self.global_font = "Microsoft YaHei"
        self.current_theme = "system"
        self.theme = get_system_theme()
        self.custom_themes = []
        self.projects = []
        self.windows = []
        self.plugin_settings_tabs = {}
        self.exam_mode_config = {}
        self.exam_mode_window = None

        self.auto_start = False
        self.last_save_time = 0
        self.poem_level = "junior"
        self.daily_poem = ""
        self.plugin_monitor = False
        self.plugin_prompt_on_deny = True
        self.global_disable_all_plugins = False
        self._sound_playing_flag = False

        self.weather_provider = "qweather"
        self.custom_weather_url = ""
        self.qweather_api_key = ""
        self.qweather_api_host = ""
        self.render_backend = "auto"
        self.launch_count = 0
        self.enable_flip_animation = True
        self.enable_gpu_acceleration = True
        self.editor_splitter = ""

        self.dynamic_bg_registry = {"stars": "✨ 星空", "particles": "🌌 鼠标粒子", "aurora": "🌌 极光 (GPU着色器)", "sky": "🌅 天空 (清晨)"}
        self.dynamic_bg_classes = {}

        self.settings_geometry = None
        self.editor_geometry = None
        self.help_geometry = None
        self.tools_geometry = None
        self.wallpaper_manager = WallpaperManager(self)

        self.current_dir = os.getcwd()
        self.data_dir = resource_path("data")
        self.user_dir = os.path.join(self.data_dir, "user")
        os.makedirs(self.user_dir, exist_ok=True)
        ensure_sound_assets(self.data_dir)

        self.config_path = os.path.join(self.data_dir, "countdown_config.json")

        self.show_splash()

        self.load_languages()
        self.load_poems()
        self.load_config()
        self.update_daily_poem()

        load_holiday_cache(self.data_dir)
        self._holiday_update_thread = None
        QTimer.singleShot(2000, self._auto_update_holidays)

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

        self.launch_count += 1
        self.save_config(force=True)
        if self.launch_count == 1:
            QTimer.singleShot(800, self._show_welcome)

    def _show_welcome(self):
        parent = self.settings_dlg if hasattr(self, 'settings_dlg') and self.settings_dlg else None
        dlg = QDialog(parent)
        dlg.setWindowTitle(tr("welcome_title"))
        dlg.setStyleSheet(get_theme_qss(self.theme))
        dlg.setMinimumWidth(460)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 16)

        msg = QLabel(tr("welcome_msg"))
        msg.setWordWrap(True)
        layout.addWidget(msg)

        row = QHBoxLayout()
        row.addWidget(QLabel(tr("language_label") + ":"))
        combo_lang = QComboBox()
        combo_lang.addItems(["🇨🇳 中文", "🇬🇧 English"])
        combo_lang.setCurrentIndex(0 if CURRENT_LANG == LANG_CHINESE else 1)
        row.addWidget(combo_lang)
        row.addStretch()
        layout.addLayout(row)

        combo_lang.currentIndexChanged.connect(self._on_language_changed)

        btn_row = QHBoxLayout()
        btn_help = QPushButton(tr("welcome_help"))
        btn_help.clicked.connect(lambda: (dlg.accept(), self.open_settings(tab="help")))
        btn_close = QPushButton(tr("close"))
        btn_close.clicked.connect(dlg.accept)
        btn_row.addWidget(btn_help)
        btn_row.addStretch()
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)

        dlg.exec()
        self._first_run_done = True
        self.save_config(force=True)

    def _on_system_theme_changed(self, is_dark):
        log_message(f"系统主题变化: {'深色' if is_dark else '浅色'}", "INFO")
        if getattr(self, 'current_theme', 'system') != "system":
            return
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
        self._refresh_log_size_label()

    def _refresh_log_size_label(self):
        if not hasattr(self, 'log_size_label'):
            return
        log_path = os.path.join(self.data_dir, "LOG.txt")
        try:
            if os.path.exists(log_path):
                size = os.path.getsize(log_path)
                if size < 1024:
                    text = f"{size} B"
                elif size < 1024 * 1024:
                    text = f"{size / 1024:.1f} KB"
                else:
                    text = f"{size / (1024 * 1024):.2f} MB"
                self.log_size_label.setText(f"📄 LOG.txt: {text}")
            else:
                self.log_size_label.setText("📄 LOG.txt: 未生成")
        except Exception:
            self.log_size_label.setText("")

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

    def get_highest_priority_expired_sound_index(self):
        for i, proj in enumerate(self.projects):
            if not getattr(proj, 'enable_end_sound', True):
                continue
            eff_date, eff_time = get_effective_target(proj)
            if eff_date is None:
                return i
            try:
                target = datetime.strptime(f"{eff_date} {eff_time}", "%Y-%m-%d %H:%M")
                if (target - datetime.now()).total_seconds() <= 0:
                    return i
            except Exception:
                continue
        return None

    def play_highest_priority_end_sound(self):
        if self._sound_playing_flag:
            return
        idx = self.get_highest_priority_expired_sound_index()
        if idx is None:
            return
        proj = self.projects[idx]
        mode = getattr(proj, 'end_sound_mode', 'windchime')
        sound_map = {
            "windchime": "windchime.wav",
            "piano": "piano_ding.wav",
            "double_ding": "double_ding.wav",
            "urgent_beep": "urgent_beep.wav",
            "long_buzz": "long_buzz.wav",
            "alarm_rise": "alarm_rise.wav",
            "ocean_wave": "ocean_wave.wav",
            "synth_arp": "synth_arp.wav",
        }
        if mode == 'custom':
            cust = getattr(proj, 'custom_sound_path', '')
            if not cust:
                sound_path = None
            elif os.path.isabs(cust):
                sound_path = cust
            else:
                sound_path = os.path.join(self.data_dir, cust)
        else:
            fname = sound_map.get(mode, "windchime.wav")
            sound_path = os.path.join(self.data_dir, 'sounds', fname)
        if not sound_path or not os.path.exists(sound_path):
            log_message(f"提示音文件不可用，跳过播放: {sound_path}", "WARNING")
            return
        self._sound_playing_flag = True
        play_sound_file(sound_path)
        QTimer.singleShot(3000, self._reset_sound_flag)

    def _reset_sound_flag(self):
        self._sound_playing_flag = False

    def _open_test_panel(self):
        self._test_panel = TestPanel(self)
        self._test_panel.show()

    def _blink_test_cmd(self):
        if not self.windows:
            return
        w = self.windows[0]
        if hasattr(w, 'countdown_label'):
            lbl = w.countdown_label
            lbl._expired = True
            lbl._expired_text = "[测试闪烁]"
            lbl._target_str = "[测试闪烁]"
            lbl._current_str = "[测试闪烁]"
            lbl._unit = ""
            lbl._blink_enabled = True
            lbl.startBlink()

    def _blink_speed_cmd(self, ms):
        for w in self.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.setBlinkSpeed(ms)

    def _blink_enable_cmd(self, enabled):
        for w in self.windows:
            if hasattr(w, 'countdown_label'):
                w.countdown_label.setBlinkEnabled(enabled)

    def _blink_msg_cmd(self, msg):
        if not self.windows:
            return
        w = self.windows[0]
        if hasattr(w, 'countdown_label'):
            w.countdown_label.showExpired(msg)

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
                self.poems_data = {"primary": [], "junior": [], "senior": [], "extra": []}
        else:
            self.poems_data = {"primary": [], "junior": [], "senior": [], "extra": []}
        for key in ("primary", "junior", "senior", "extra"):
            self.poems_data.setdefault(key, [])

    def update_daily_poem(self):
        if self.poem_level != "none" and self.poems_data.get(self.poem_level):
            self.daily_poem = random.choice(self.poems_data[self.poem_level])
        else:
            self.daily_poem = ""

    def get_random_poem_or_tip(self, levels=None):
        if levels:
            pool = []
            for lv in levels:
                pool.extend(self.poems_data.get(lv, []))
            if pool:
                return random.choice(pool)
            return ""
        elif self.poem_level != "none" and self.poems_data.get(self.poem_level):
            return random.choice(self.poems_data[self.poem_level])
        return ""

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

    def _auto_update_holidays(self):
        if self._holiday_update_thread and self._holiday_update_thread.isRunning():
            return
        cur_year = datetime.now().year
        max_lib_year = max(chinese_calendar.constants.holidays.keys()).year
        years = [y for y in range(max_lib_year + 1, cur_year + 3)]
        if not years:
            return
        self._holiday_update_thread = HolidayUpdateThread(self.data_dir, years)
        self._holiday_update_thread.finished_signal.connect(self._on_holiday_auto_done)
        self._holiday_update_thread.start()

    def _on_holiday_auto_done(self, updated_years, failed_years):
        if updated_years:
            log_message(f"假期数据自动更新成功: {updated_years}", "INFO")
            for win in self.windows:
                win.refresh()

    def update_holidays(self):
        if self._holiday_update_thread and self._holiday_update_thread.isRunning():
            QMessageBox.information(None, "更新假期数据", "假期数据正在更新中，请稍候...")
            return
        cur_year = datetime.now().year
        years = list(range(cur_year, cur_year + 3))
        log_message(f"用户手动触发假期数据更新: {years}", "INFO")
        self._holiday_update_thread = HolidayUpdateThread(self.data_dir, years)
        self._holiday_update_thread.finished_signal.connect(self._on_holiday_update_done)
        self._holiday_update_thread.start()
        QMessageBox.information(None, "更新假期数据", "正在后台获取最新假期数据，完成后会通知您...")

    def _on_holiday_update_done(self, updated_years, failed_years):
        if updated_years:
            msg = f"假期数据更新成功: {', '.join(map(str, updated_years))} 年"
            if failed_years:
                msg += f"\n部分年份获取失败: {', '.join(str(y) for y, _ in failed_years)}"
            log_message(f"手动更新完成: 成功 {updated_years}, 失败 {failed_years}", "INFO")
            QMessageBox.information(None, "更新完成", msg)
            for win in self.windows:
                win.refresh()
        elif failed_years:
            log_message(f"手动更新全部失败: {failed_years}", "WARNING")
            QMessageBox.warning(None, "更新失败",
                f"未能获取假期数据:\n" + "\n".join(f"{y}: {e}" for y, e in failed_years))

    def load_config(self):
        global DEBUG_MODE, STATUS_MONITOR, CURRENT_LANG
        screen_geo = self.primaryScreen().geometry()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                config_ver = config.get("config_version", 0)
                if config_ver < 3:
                    for p in config.get("projects", []):
                        cl = p.get("custom_layout", {})
                        if "poem" in cl and "levels" not in cl["poem"]:
                            lv = p.get("poem_level", self.poem_level)
                            if lv and lv != "none":
                                cl["poem"]["levels"] = [lv]
                            cl["poem"].setdefault("show_poem", True)
                            cl["poem"].setdefault("line_spacing", 1.2)
                        p.setdefault("project_type", "normal")
                        p.setdefault("click_through", False)
                        p.setdefault("recur_weekdays", [])
                        p.setdefault("recur_end_date", "")
                    log_message(f"配置已从 v{config_ver} 迁移到 v3", "INFO")
                if config_ver < 4:
                    for p in config.get("projects", []):
                        p.setdefault("enable_end_sound", True)
                        p.setdefault("end_sound_mode", "windchime")
                        p.setdefault("custom_sound_path", "")
                    log_message(f"配置已从 v{config_ver} 迁移到 v4", "INFO")
                if config_ver < 5:
                    _sound_migration = {"microwave": "double_ding", "beep": "urgent_beep", "chime": "windchime", "long_tone": "long_buzz"}
                    for p in config.get("projects", []):
                        old_mode = p.get("end_sound_mode", "piano")
                        if old_mode in _sound_migration:
                            p["end_sound_mode"] = _sound_migration[old_mode]
                    log_message(f"音效名称已从 v{config_ver} 迁移到 v5", "INFO")
                if config_ver < 6:
                    log_message(f"配置已从 v{config_ver} 迁移到 v6（新增音效：闹钟/海浪/电子合成）", "INFO")
                if config_ver < 7:
                    for p in config.get("projects", []):
                        fls = p.get("fullscreen_layouts", {})
                        if not fls:
                            old_fl = p.get("fullscreen_layout", {})
                            if old_fl:
                                p["fullscreen_layouts"] = {"default": old_fl}
                            else:
                                p["fullscreen_layouts"] = {}
                        p.setdefault("fullscreen_layouts", {})
                    log_message(f"配置已从 v{config_ver} 迁移到 v7（全屏布局按背景类型独立存储）", "INFO")
                if config_ver < 8:
                    if config.get("weather_provider") in ("wttr_in", "open_meteo"):
                        config["weather_provider"] = "qweather"
                    log_message(f"配置已从 v{config_ver} 迁移到 v8（精简天气API供应商为和风/自定义）", "INFO")
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
                self.weather_provider = config.get("weather_provider", "qweather")
                self.custom_weather_url = config.get("custom_weather_url", "")
                self.qweather_api_key = config.get("qweather_api_key", "")
                self.render_backend = config.get("render_backend", "auto")
                self.launch_count = config.get("launch_count", 0)
                self.enable_flip_animation = config.get("enable_flip_animation", True)
                self.enable_gpu_acceleration = config.get("enable_gpu_acceleration", True)
                self.editor_splitter = config.get("editor_splitter", "")
                self._first_run_done = config.get("first_run_done", False)
                self.exam_mode_config = config.get("exam_mode_config", {})

                def _decode_geom(hex_str):
                    return QByteArray.fromHex(hex_str.encode('utf-8')) if hex_str else None

                self.settings_geometry = _decode_geom(config.get("settings_geometry"))
                self.editor_geometry = _decode_geom(config.get("editor_geometry"))
                self.help_geometry = _decode_geom(config.get("help_geometry"))
                self.tools_geometry = _decode_geom(config.get("tools_geometry"))

                self.custom_themes = [Theme.from_dict(t) for t in config.get("custom_themes", [])]

                if hasattr(self, 'wallpaper_manager'):
                    self.wallpaper_manager.load_config(config.get("wallpaper_config", {}))

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

    @staticmethod
    def _atomic_replace(src, dst, retries=4, delay=0.05):
        for attempt in range(retries):
            try:
                os.replace(src, dst)
                return
            except OSError:
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                else:
                    import shutil
                    shutil.copy2(src, dst)
                    os.remove(src)

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
            "config_version": 8,
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
            "qweather_api_key": self.qweather_api_key,
            "qweather_api_host": self.qweather_api_host,
            "render_backend": self.render_backend,
            "launch_count": getattr(self, 'launch_count', 0),
            "enable_flip_animation": self.enable_flip_animation,
            "enable_gpu_acceleration": self.enable_gpu_acceleration,
            "plugin_states": plugin_states,
            "settings_geometry": _encode_geom(self.settings_geometry),
            "editor_geometry": _encode_geom(self.editor_geometry),
            "editor_splitter": self.editor_splitter,
            "help_geometry": _encode_geom(self.help_geometry),
            "tools_geometry": _encode_geom(self.tools_geometry),
            "wallpaper_config": self.wallpaper_manager.save_config() if hasattr(self, 'wallpaper_manager') else {},
            "first_run_done": getattr(self, '_first_run_done', False),
            "exam_mode_config": getattr(self, 'exam_mode_config', {})
        }
        try:
            temp_path = self.config_path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self._atomic_replace(temp_path, self.config_path)
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
        if getattr(self, 'current_theme', 'system') != "system":
            return
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
        try:
            self.save_config(force=True)
        except Exception:
            pass
        settings_dlg = getattr(self, 'settings_dlg', None)
        if settings_dlg is not None:
            dlg = settings_dlg
            dlg._closing = True
            log_timer = getattr(self, 'log_timer', None)
            if log_timer and log_timer.isActive():
                log_timer.stop()
            try:
                self.settings_geometry = dlg.saveGeometry()
            except Exception:
                pass
            self.settings_dlg = None
            try:
                dlg.deleteLater()
            except Exception:
                pass
        tray_icon = getattr(self, 'tray_icon', None)
        if tray_icon:
            try:
                tray_icon.tray.hide()
            except Exception:
                pass
        for w in list(getattr(self, 'windows', [])):
            try:
                w.close()
            except Exception:
                pass
        self.quit()

    def start_console_debugger(self):
        def console_loop():
            print("=" * 60)
            print(f"  倒计时 (Countdown) - 开发调试控制台 {self.current_version}")
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
                    # ── 到期闪烁调试命令 ──
                    if cmd == "test":
                        QTimer.singleShot(0, lambda: self._open_test_panel())
                        print("  测试面板已打开")
                        continue
                    if cmd == "blink_info":
                        for i, w in enumerate(self.windows):
                            if hasattr(w, 'countdown_label'):
                                info = w.countdown_label.blinkInfo()
                                print(f"  [窗口{i}] {w.project.name}: enabled={info['enabled']} "
                                      f"active={info['active']} visible={info['visible']} "
                                      f"interval={info['interval_ms']}ms expired={info['expired']}")
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

    def _animate_dialog_open(self, dialog, fade_effect, duration=220):
        try:
            geo = dialog.geometry()
            cx, cy = geo.center().x(), geo.center().y()
            sw, sh = int(geo.width() * 0.95), int(geo.height() * 0.95)
            start_geo = QRect(cx - sw // 2, cy - sh // 2, sw, sh)
            scale = QPropertyAnimation(dialog, b"geometry", dialog)
            scale.setDuration(duration)
            scale.setStartValue(start_geo)
            scale.setEndValue(geo)
            scale.setEasingCurve(QEasingCurve.Type.OutCubic)
            scale.start()
            fade = QPropertyAnimation(fade_effect, b"opacity", dialog)
            fade.setDuration(duration)
            fade.setStartValue(0.0)
            fade.setEndValue(1.0)
            fade.setEasingCurve(QEasingCurve.Type.OutCubic)
            fade.start()
            dialog._open_scale_anim = scale
            dialog._open_fade_anim = fade
        except Exception as e:
            log_message(f"弹出动画失败: {e}", "ERROR")
            try:
                fade_effect.setOpacity(1.0)
            except Exception:
                pass

    def _animate_tab_switch(self, tabs_widget, new_idx, duration=170, offset=10):
        try:
            page = tabs_widget.widget(new_idx)
            if page is None:
                self._last_tab_idx = new_idx
                return
            old_idx = getattr(self, '_last_tab_idx', None)
            self._last_tab_idx = new_idx
            if old_idx is None or old_idx == new_idx:
                return
            a = getattr(page, '_tab_slide_anim', None)
            if a is not None:
                a.stop()
            direction = 1 if new_idx > old_idx else -1
            target = page.pos()
            anim = QPropertyAnimation(page, b"pos", page)
            anim.setDuration(duration)
            anim.setStartValue(target + QPoint(direction * offset, 0))
            anim.setEndValue(target)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.start()
            page._tab_slide_anim = anim
        except Exception as e:
            log_message(f"标签切换动画失败: {e}", "ERROR")
            try:
                page.move(0, 0)
            except Exception:
                pass

    def open_exam_mode(self):
        if getattr(self, 'exam_mode_window', None) is not None:
            try:
                self.exam_mode_window.raise_()
                self.exam_mode_window.activateWindow()
                return
            except RuntimeError:
                self.exam_mode_window = None
        dlg = ExamModeConfigDialog(self, self.activeWindow())
        dlg.exec()

    def enter_exam_mode(self, config):
        try:
            if getattr(self, 'exam_mode_window', None) is not None:
                try:
                    self.exam_mode_window.close_exam()
                except Exception:
                    pass
                self.exam_mode_window = None
            win = ExamModeWindow(self, config)
            self.exam_mode_window = win
            win.show()
        except Exception as e:
            log_message(f"进入考试模式失败: {e}\n{traceback.format_exc()}", "ERROR")

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
        tc = get_theme_colors(self.theme)
        self.settings_dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.settings_dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.settings_dlg.setStyleSheet(get_theme_qss(self.theme) + "\nQDialog { background: transparent; border: none; }")
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

        outer_layout = QVBoxLayout(self.settings_dlg)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("settingsContainer")
        container.setStyleSheet(f"QFrame#settingsContainer {{ background-color: {tc['dark_bg']}; border-radius: 10px; border: 1px solid {tc['border_color']}; }}")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        title_bar = QFrame()
        title_bar.setObjectName("settingsTitleBar")
        title_bar.setFixedHeight(38)
        title_bar.setStyleSheet(f"QFrame#settingsTitleBar {{ background: transparent; border-bottom: 1px solid {tc['border_color']}; border-top-left-radius: 10px; border-top-right-radius: 10px; }}")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(14, 0, 6, 0)
        title_bar_layout.setSpacing(0)
        title_label = QLabel(tr("settings_title"))
        title_label.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {tc['accent']}; background: transparent; border: none;")
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        btn_close_dlg = QPushButton("✕")
        btn_close_dlg.setFixedSize(30, 30)
        btn_close_dlg.setAutoDefault(False)
        btn_close_dlg.setStyleSheet("QPushButton { border: none; font-size: 13px; background: transparent; color: #888; } QPushButton:hover { background-color: #e74c3c; color: white; border-radius: 4px; }")
        btn_close_dlg.clicked.connect(self.settings_dlg.close)
        title_bar_layout.addWidget(btn_close_dlg)

        def _title_mouse_press(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.settings_dlg._drag_pos = event.globalPosition().toPoint() - self.settings_dlg.frameGeometry().topLeft()
                event.accept()
        def _title_mouse_move(event):
            if getattr(self.settings_dlg, '_drag_pos', None) and event.buttons() & Qt.MouseButton.LeftButton:
                self.settings_dlg.move(event.globalPosition().toPoint() - self.settings_dlg._drag_pos)
                event.accept()
        title_bar.mousePressEvent = _title_mouse_press
        title_bar.mouseMoveEvent = _title_mouse_move

        container_layout.addWidget(title_bar)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 12)
        container_layout.addLayout(main_layout)
        outer_layout.addWidget(container)

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
        layout_proj.setSpacing(8)

        self.list_proj = QListWidget()
        self.list_proj.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.theme.frame_bg}; color: {self.theme.text_color};
                border: 1px solid {tc['border_color']}; border-radius: 6px; outline: none;
            }}
            QListWidget::item {{ padding: 10px 12px; border-bottom: 1px solid {tc['border_color']}; }}
            QListWidget::item:selected {{ background-color: {tc['accent']}; color: {tc['selected_text']}; }}
            QListWidget::item:hover {{ background-color: {tc['alternate_bg']}; color: {tc['text_color']}; }}
        """)
        for idx, p in enumerate(self.projects):
            item = QListWidgetItem()
            item.setText(self._format_proj_item_text(p, idx))
            item.setData(Qt.ItemDataRole.UserRole, p.name)
            self.list_proj.addItem(item)
        layout_proj.addWidget(self.list_proj)

        btn_layout_proj = QHBoxLayout()
        btn_layout_proj.setSpacing(6)
        btn_add = QPushButton(tr("add_project"))
        btn_add.setProperty("primary", True)
        btn_add.setMinimumHeight(32)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_project_ui)
        btn_edit = QPushButton(tr("edit_project"))
        btn_edit.setProperty("secondary", True)
        btn_edit.setMinimumHeight(32)
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.clicked.connect(self.edit_project_ui)
        btn_del = QPushButton(tr("delete_project"))
        btn_del.setProperty("danger", True)
        btn_del.setMinimumHeight(32)
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(self.del_project_ui)

        btn_custom = QPushButton(tr("customize_appearance"))
        btn_custom.setProperty("secondary", True)
        btn_custom.setMinimumHeight(32)
        btn_custom.setCursor(Qt.CursorShape.PointingHandCursor)
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

        self.btn_check_update = QPushButton(tr("check_update"))
        self.btn_check_update.setProperty("primary", True)
        self.btn_check_update.setCursor(Qt.CursorShape.PointingHandCursor)

        def on_check_update_clicked():
            msg = QMessageBox(self.settings_dlg)
            msg.setWindowTitle("倒计时·DJS - " + tr("check_update"))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(tr("update_in_dev_msg"))
            btn_open = msg.addButton(tr("open_project_page"), QMessageBox.ButtonRole.ActionRole)
            msg.addButton(QMessageBox.StandardButton.Ok)
            msg.exec()
            if msg.clickedButton() is btn_open:
                webbrowser.open("https://gitcode.com/2401_86556713/djs")

        self.btn_check_update.clicked.connect(on_check_update_clicked)

        btn_vote = QPushButton(tr("feature_vote"))
        btn_vote.setProperty("primary", True)
        btn_vote.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_vote.clicked.connect(lambda: webbrowser.open("https://gitcode.com/2401_86556713/djs/discussions"))

        action_row = QHBoxLayout()
        action_row.setSpacing(8)
        action_row.addWidget(self.btn_check_update, 1)
        action_row.addWidget(btn_vote, 1)
        lay_info.addLayout(action_row)

        backup_card = QFrame()
        backup_card.setObjectName("pillCard")
        backup_card.setStyleSheet(f"""
            QFrame#pillCard {{
                background-color: {tc['input_bg']};
                border: 1px solid {tc['border_color']};
                border-radius: 16px;
            }}
            QPushButton {{
                background: transparent; border: none; border-radius: 14px;
                padding: 8px 14px; color: {tc['text_color']}; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {tc['accent']}; color: white; }}
            QFrame#divider {{ background-color: {tc['border_color']}; max-width: 1px; }}
        """)
        backup_lay = QHBoxLayout(backup_card)
        backup_lay.setContentsMargins(4, 4, 4, 4)
        backup_lay.setSpacing(0)
        btn_backup = QPushButton("💾 " + tr("backup_config"))
        btn_backup.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_backup.clicked.connect(self._backup_config)
        backup_lay.addWidget(btn_backup)
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedWidth(1)
        backup_lay.addWidget(divider)
        btn_restore = QPushButton(tr("restore_config"))
        btn_restore.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_restore.clicked.connect(self._restore_config)
        backup_lay.addWidget(btn_restore)
        lay_info.addWidget(backup_card)

        layout_global.addWidget(grp_info)

        grp_basic = QGroupBox(tr("global_settings"))
        lay_basic = QGridLayout(grp_basic)
        lay_basic.setHorizontalSpacing(20)
        lay_basic.setVerticalSpacing(10)
        lay_basic.setColumnStretch(0, 1)
        lay_basic.setColumnStretch(1, 1)

        grp_debug = QGroupBox("🐛 调试与日志")
        lay_debug = QVBoxLayout(grp_debug)

        debug_layout = QHBoxLayout()
        debug_layout.addWidget(QLabel("日志等级:"))
        self.combo_debug = QComboBox()
        self.combo_debug.addItems(["❌ 关闭 (0)", "⚠️ 错误/警告 (1)", "ℹ️ 普通信息 (2)", "🔍 详细调试 (3)"])
        self.combo_debug.setCurrentIndex(DEBUG_MODE)
        self.combo_debug.currentIndexChanged.connect(self.auto_save_global_settings)
        debug_layout.addWidget(self.combo_debug)
        debug_layout.addStretch()
        self.log_size_label = QLabel("")
        self.log_size_label.setStyleSheet(f"color: {tc['secondary_text']}; font-size: 11px;")
        debug_layout.addWidget(self.log_size_label)
        lay_debug.addLayout(debug_layout)
        self._refresh_log_size_label()

        btn_view_log = QPushButton("查看日志文件")
        btn_view_log.clicked.connect(self.open_log_file)
        lay_debug.addWidget(btn_view_log)

        layout_global.addWidget(grp_debug)

        self.chk_auto_start = QCheckBox(tr("autostart"))
        self.chk_auto_start.setChecked(self.auto_start)
        self.chk_auto_start.toggled.connect(lambda v: setattr(self, 'auto_start', v) or self.auto_save_global_settings())
        lay_basic.addWidget(self.chk_auto_start, 0, 0)

        self.chk_flip_anim = QCheckBox(tr("flip_animation"))
        self.chk_flip_anim.setChecked(self.enable_flip_animation)
        self.chk_flip_anim.toggled.connect(self._on_flip_animation_toggled)
        lay_basic.addWidget(self.chk_flip_anim, 0, 1)

        self.chk_gpu_accel = QCheckBox("GPU 着色器加速")
        self.chk_gpu_accel.setChecked(self.enable_gpu_acceleration)
        self.chk_gpu_accel.setToolTip("启用后将使用 OpenGL 着色器渲染极光等动态背景，显著降低 CPU 占用。\n实验性功能，部分显卡可能不兼容，遇到问题可关闭。")
        self.chk_gpu_accel.toggled.connect(self._on_gpu_acceleration_toggled)
        lay_basic.addWidget(self.chk_gpu_accel, 0, 2)

        lang_lay = QHBoxLayout()
        lang_lay.addWidget(QLabel(tr("language_label") + ":"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["🇨🇳 中文", "🇬🇧 English"])
        self.combo_lang.setCurrentIndex(0 if CURRENT_LANG == LANG_CHINESE else 1)
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        lang_lay.addWidget(self.combo_lang, 1)
        lay_basic.addLayout(lang_lay, 1, 0)

        render_lay = QHBoxLayout()
        render_lay.addWidget(QLabel(tr("render_backend") + ":"))
        self.combo_render = QComboBox()
        self.render_backend_values = ["auto", "software", "opengl", "vulkan"]
        self.render_backend_labels = [tr("render_auto"), tr("render_software"), tr("render_opengl"), tr("render_vulkan")]
        if sys.platform == "win32":
            self.render_backend_values += ["d3d11", "d3d12"]
            self.render_backend_labels += [tr("render_d3d11"), tr("render_d3d12")]
        elif sys.platform == "darwin":
            self.render_backend_values += ["metal"]
            self.render_backend_labels += [tr("render_metal")]
        self.combo_render.addItems(self.render_backend_labels)
        self.combo_render.setCurrentIndex(self.render_backend_values.index(self.render_backend) if self.render_backend in self.render_backend_values else 0)
        self.combo_render.currentIndexChanged.connect(self._on_render_backend_changed)
        render_lay.addWidget(self.combo_render, 1)
        lay_basic.addLayout(render_lay, 1, 1)

        note_card = QFrame()
        note_card.setObjectName("noteCard")
        note_card.setStyleSheet(f"""
            QFrame#noteCard {{
                background-color: {tc['input_bg']};
                border: 1px solid {tc['accent']};
                border-left: 4px solid {tc['accent']};
                border-radius: 6px;
            }}
            QLabel {{ color: {tc['accent']}; font-size: 11px; }}
        """)
        note_lay = QHBoxLayout(note_card)
        note_lay.setContentsMargins(10, 6, 10, 6)
        poem_hint = QLabel("💡 " + tr("poem_level_moved"))
        poem_hint.setWordWrap(False)
        poem_hint.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        note_lay.addWidget(poem_hint)
        lay_basic.addWidget(note_card, 2, 0, 1, 2)
        self.combo_poem = QComboBox()
        self.combo_poem.setVisible(False)
        self.combo_poem.addItems([tr("poem_none"), tr("poem_primary"), tr("poem_junior"), tr("poem_senior")])
        self.combo_poem.setCurrentIndex(0)

        engine_status = QFrame()
        engine_status.setObjectName("engineStatus")
        is_d3d = self.render_backend in ("d3d11", "d3d12") if sys.platform == "win32" else self.render_backend == "metal"
        dot_color = "#2ecc71" if is_d3d else "#f39c12"
        engine_status.setStyleSheet(f"""
            QFrame#engineStatus {{ background: transparent; }}
            QLabel#dot {{ background-color: {dot_color}; border-radius: 5px; max-width: 10px; max-height: 10px; min-width: 10px; min-height: 10px; }}
            QLabel {{ color: gray; font-size: 9pt; }}
        """)
        es_lay = QHBoxLayout(engine_status)
        es_lay.setContentsMargins(0, 0, 0, 0)
        es_lay.setSpacing(6)
        dot = QLabel()
        dot.setObjectName("dot")
        es_lay.addWidget(dot)
        _cur_name = self._render_display_name(self.render_backend)
        self.lbl_render_info = QLabel(f"{tr('render_current')}: {_cur_name}  ·  💡 {tr('render_intel_tip')}")
        es_lay.addWidget(self.lbl_render_info)
        es_lay.addStretch()
        lay_basic.addWidget(engine_status, 3, 0, 1, 2)

        layout_global.addWidget(grp_basic)

        # 天气API配置
        grp_weather = QGroupBox(tr("weather_source"))
        lay_weather = QVBoxLayout(grp_weather)

        weather_src_lay = QHBoxLayout()
        weather_src_lay.addWidget(QLabel(tr("weather_source") + ":"))
        self.combo_weather_source = QComboBox()
        self.combo_weather_source.addItems(["和风天气", tr("custom")])
        provider_map = {"qweather": 0, "custom": 1}
        self.combo_weather_source.setCurrentIndex(provider_map.get(self.weather_provider, 0))
        self.combo_weather_source.currentIndexChanged.connect(self._on_weather_source_changed)
        weather_src_lay.addWidget(self.combo_weather_source)
        lay_weather.addLayout(weather_src_lay)

        self.weather_qweather_row = QWidget()
        qw_lay = QVBoxLayout(self.weather_qweather_row)
        qw_lay.setContentsMargins(0, 0, 0, 0)
        qw_lay.setSpacing(4)
        qw_mode_lay = QHBoxLayout()
        self.rb_qw_default = QRadioButton("默认")
        self.rb_qw_custom = QRadioButton("自定义")
        qw_mode_grp = QButtonGroup(self)
        qw_mode_grp.addButton(self.rb_qw_default)
        qw_mode_grp.addButton(self.rb_qw_custom)
        qw_mode_lay.addWidget(self.rb_qw_default)
        qw_mode_lay.addWidget(self.rb_qw_custom)
        qw_mode_lay.addStretch()
        qw_lay.addLayout(qw_mode_lay)

        self.qw_custom_box = QWidget()
        qw_custom_lay = QVBoxLayout(self.qw_custom_box)
        qw_custom_lay.setContentsMargins(0, 0, 0, 0)
        qw_custom_lay.setSpacing(4)
        qw_key_lay = QHBoxLayout()
        qw_key_lay.addWidget(QLabel("API Key:"))
        self.edit_qweather_api_key = QLineEdit()
        self.edit_qweather_api_key.setPlaceholderText("和风天气 API Key")
        self.edit_qweather_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.edit_qweather_api_key.setText(self.qweather_api_key)
        self.edit_qweather_api_key.textChanged.connect(self._on_qweather_key_changed)
        qw_key_lay.addWidget(self.edit_qweather_api_key)
        qw_custom_lay.addLayout(qw_key_lay)
        qw_host_lay = QHBoxLayout()
        qw_host_lay.addWidget(QLabel("API Host:"))
        self.edit_qweather_api_host = QLineEdit()
        self.edit_qweather_api_host.setPlaceholderText("如 abc1234xyz.def.qweatherapi.com")
        self.edit_qweather_api_host.setText(self.qweather_api_host)
        self.edit_qweather_api_host.textChanged.connect(self._on_qweather_host_changed)
        qw_host_lay.addWidget(self.edit_qweather_api_host)
        qw_custom_lay.addLayout(qw_host_lay)
        qw_lay.addWidget(self.qw_custom_box)

        qw_hint = QLabel("含实况天气、空气质量AQI、生活指数")
        qw_hint.setStyleSheet("color: gray; font-size: 10px;")
        qw_hint.setWordWrap(True)
        qw_lay.addWidget(qw_hint)
        lay_weather.addWidget(self.weather_qweather_row)
        self.weather_qweather_row.setVisible(self.weather_provider == "qweather")

        is_qw_custom = bool(self.qweather_api_key) and bool(self.qweather_api_host)
        self.rb_qw_custom.setChecked(is_qw_custom)
        self.rb_qw_default.setChecked(not is_qw_custom)
        self.qw_custom_box.setVisible(is_qw_custom)
        self.rb_qw_default.toggled.connect(self._on_qw_mode_changed)
        self.rb_qw_custom.toggled.connect(self._on_qw_mode_changed)

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
        top_row.setSpacing(8)
        self.plugin_toggle = FluentToggleSwitch(checked=not self.global_disable_all_plugins)
        self.plugin_toggle.toggled.connect(self.toggle_global_disable_plugins)
        top_row.addWidget(QLabel("启用插件系统"))
        top_row.addWidget(self.plugin_toggle)
        _ps_ver_label = QLabel(f"v{Plugin.PLUGIN_SYSTEM_VERSION}")
        _ps_ver_label.setStyleSheet(f"color: {get_theme_colors(self.theme)['secondary_text']}; font-size: 11px;")
        _ps_ver_label.setToolTip(f"插件系统版本 v{Plugin.PLUGIN_SYSTEM_VERSION}")
        top_row.addWidget(_ps_ver_label)
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

        title_label = QLabel(f"欢迎使用CAC插件系统 v{Plugin.PLUGIN_SYSTEM_VERSION}")
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
        splitter.setHandleWidth(6)
        splitter.setStyleSheet(
            f"QSplitter::handle {{ background-color: {get_theme_colors(self.theme)['border_color']}; }}"
        )

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
        self.btn_perm.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_perm.setStyleSheet(
            f"QPushButton {{ background-color: #B8860B; color: white; border: none; border-radius: 4px; padding: 5px 12px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: #DAA520; }}"
            f"QPushButton:pressed {{ background-color: #8B6914; }}"
        )
        self.btn_perm.setToolTip("管理插件权限（敏感操作）")
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

        self.plugin_right_tabs = QTabWidget()
        self.plugin_right_tabs.setDocumentMode(True)

        self.plugin_detail_group = QWidget()
        detail_layout_inner = QVBoxLayout(self.plugin_detail_group)
        detail_layout_inner.setContentsMargins(8, 8, 8, 8)
        self.detail_label = QLabel("请选择插件")
        self.detail_label.setWordWrap(True)
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_label.setStyleSheet(f"color: {get_theme_colors(self.theme)['secondary_text']}; padding: 24px; font-size: 13px;")
        detail_layout_inner.addWidget(self.detail_label)
        self.plugin_custom_widget = QStackedWidget()
        detail_layout_inner.addWidget(self.plugin_custom_widget)
        self._plugin_detail_tab_idx = self.plugin_right_tabs.addTab(self.plugin_detail_group, "插件详情")

        self.log_combined_frame = QWidget()
        log_combined_layout = QVBoxLayout(self.log_combined_frame)
        log_combined_layout.setContentsMargins(8, 8, 8, 8)
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
        self._plugin_log_tab_idx = self.plugin_right_tabs.addTab(self.log_combined_frame, "日志")

        tc = get_theme_colors(self.theme)
        self.plugin_panels_group = QWidget()
        panels_layout = QVBoxLayout(self.plugin_panels_group)
        panels_layout.setContentsMargins(8, 8, 8, 8)
        self.plugin_panels_list = QListWidget()
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
        self._plugin_panels_tab_idx = self.plugin_right_tabs.addTab(self.plugin_panels_group, "插件面板")
        self.plugin_right_tabs.setTabVisible(self._plugin_panels_tab_idx, False)

        right_layout.addWidget(self.plugin_right_tabs)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        mgmt_layout.addWidget(splitter)
        plugin_main_layout.addWidget(self.plugin_management_widget, 1)

        self._update_plugin_ui_state()
        self.tree_plugins.itemSelectionChanged.connect(self.on_plugin_selected)
        self.tree_plugins.model().rowsInserted.connect(lambda: self.empty_table_label.setVisible(self.tree_plugins.topLevelItemCount() == 0))
        self.tree_plugins.model().rowsRemoved.connect(lambda: self.empty_table_label.setVisible(self.tree_plugins.topLevelItemCount() == 0))

        tab_wallpaper = QWidget()
        layout_wallpaper = QVBoxLayout(tab_wallpaper)
        layout_wallpaper.setContentsMargins(10, 10, 10, 10)
        layout_wallpaper.setSpacing(10)

        grp_list = QGroupBox(tr("wallpaper_selector"))
        lay_list = QVBoxLayout(grp_list)
        self.wallpaper_list = QListWidget()
        self.wallpaper_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.wallpaper_list.setIconSize(QSize(140, 100))
        self.wallpaper_list.setGridSize(QSize(150, 130))
        self.wallpaper_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.wallpaper_list.setMovement(QListWidget.Movement.Static)
        self.wallpaper_list.setUniformItemSizes(True)
        self.wallpaper_list.setSpacing(8)
        self.wallpaper_list.setWordWrap(True)
        lay_list.addWidget(self.wallpaper_list)
        wp_btn_row = QHBoxLayout()
        self.btn_wp_add = QPushButton(tr("wallpaper_add"))
        self.btn_wp_remove = QPushButton(tr("wallpaper_remove"))
        self.btn_wp_up = QPushButton(tr("wallpaper_move_up"))
        self.btn_wp_down = QPushButton(tr("wallpaper_move_down"))
        for b in (self.btn_wp_add, self.btn_wp_remove, self.btn_wp_up, self.btn_wp_down):
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            wp_btn_row.addWidget(b)
        lay_list.addLayout(wp_btn_row)
        layout_wallpaper.addWidget(grp_list)

        grp_slide = QGroupBox(tr("wallpaper_slideshow"))
        lay_slide = QVBoxLayout(grp_slide)
        self.chk_wp_enabled = QCheckBox(tr("wallpaper_slideshow"))
        self.chk_wp_enabled.setChecked(self.wallpaper_manager.enabled)
        lay_slide.addWidget(self.chk_wp_enabled)
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel(tr("wallpaper_mode") + ":"))
        self.combo_wp_mode = QComboBox()
        self.combo_wp_mode.addItem(tr("wallpaper_mode_sequential"), "sequential")
        self.combo_wp_mode.addItem(tr("wallpaper_mode_random"), "random")
        self.combo_wp_mode.addItem(tr("wallpaper_mode_loop"), "loop")
        mode_idx = self.combo_wp_mode.findData(self.wallpaper_manager.mode)
        if mode_idx >= 0:
            self.combo_wp_mode.setCurrentIndex(mode_idx)
        mode_row.addWidget(self.combo_wp_mode)
        mode_row.addStretch()
        lay_slide.addLayout(mode_row)
        interval_row = QHBoxLayout()
        interval_row.addWidget(QLabel(tr("wallpaper_interval") + ":"))
        self.slider_wp_interval = QSlider(Qt.Orientation.Horizontal)
        self.slider_wp_interval.setRange(5, 3600)
        self.slider_wp_interval.setValue(int(self.wallpaper_manager.interval))
        self.lbl_wp_interval = QLabel(str(self.slider_wp_interval.value()))
        self.lbl_wp_interval.setMinimumWidth(48)
        interval_row.addWidget(self.slider_wp_interval)
        interval_row.addWidget(self.lbl_wp_interval)
        lay_slide.addLayout(interval_row)
        fill_row = QHBoxLayout()
        fill_row.addWidget(QLabel(tr("wallpaper_fill") + ":"))
        self.combo_wp_fill = QComboBox()
        self.combo_wp_fill.addItem(tr("wallpaper_fill_stretch"), "stretch")
        self.combo_wp_fill.addItem(tr("wallpaper_fill_fit"), "fit")
        self.combo_wp_fill.addItem(tr("wallpaper_fill_center"), "center")
        self.combo_wp_fill.addItem(tr("wallpaper_fill_tile"), "tile")
        fill_idx = self.combo_wp_fill.findData(self.wallpaper_manager.fill_mode)
        if fill_idx >= 0:
            self.combo_wp_fill.setCurrentIndex(fill_idx)
        fill_row.addWidget(self.combo_wp_fill)
        fill_row.addStretch()
        lay_slide.addLayout(fill_row)
        self.chk_wp_fade = QCheckBox(tr("wallpaper_fade"))
        self.chk_wp_fade.setChecked(self.wallpaper_manager.fade)
        lay_slide.addWidget(self.chk_wp_fade)
        layout_wallpaper.addWidget(grp_slide)

        grp_screen = QGroupBox(tr("wallpaper_dual_screen"))
        lay_screen = QVBoxLayout(grp_screen)
        self.chk_wp_dual = QCheckBox(tr("wallpaper_dual_screen"))
        self.chk_wp_dual.setChecked(self.wallpaper_manager.dual_screen)
        lay_screen.addWidget(self.chk_wp_dual)
        screen_row = QHBoxLayout()
        screen_row.addWidget(QLabel(tr("wallpaper_main_screen") + "/" + tr("wallpaper_sub_screen") + ":"))
        self.combo_wp_screen = QComboBox()
        self.combo_wp_screen.addItem(tr("wallpaper_main_screen"), "main")
        self.combo_wp_screen.addItem(tr("wallpaper_sub_screen"), "sub")
        screen_idx = self.combo_wp_screen.findData(self.wallpaper_manager.screen_target)
        if screen_idx >= 0:
            self.combo_wp_screen.setCurrentIndex(screen_idx)
        screen_row.addWidget(self.combo_wp_screen)
        screen_row.addStretch()
        lay_screen.addLayout(screen_row)
        layout_wallpaper.addWidget(grp_screen)

        wp_separator = QFrame()
        wp_separator.setFrameShape(QFrame.Shape.HLine)
        wp_separator.setFrameShadow(QFrame.Shadow.Sunken)
        wp_separator.setStyleSheet(f"color: {tc['border_color']}; max-height: 2px;")
        layout_wallpaper.addWidget(wp_separator)

        grp_apply = QGroupBox(tr("wallpaper_apply_desktop"))
        lay_apply = QVBoxLayout(grp_apply)
        apply_row = QHBoxLayout()
        self.btn_wp_apply_desktop = QPushButton(tr("wallpaper_apply_desktop"))
        self.btn_wp_apply_window = QPushButton(tr("wallpaper_apply_window"))
        self.btn_wp_apply_desktop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_wp_apply_window.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_row.addWidget(self.btn_wp_apply_desktop)
        apply_row.addWidget(self.btn_wp_apply_window)
        lay_apply.addLayout(apply_row)
        layout_wallpaper.addWidget(grp_apply)
        layout_wallpaper.addStretch()

        def _refresh_wallpaper_list():
            self.wallpaper_list.clear()
            for path in self.wallpaper_manager.wallpapers:
                item = QListWidgetItem(os.path.basename(path))
                pm = QPixmap(path)
                if not pm.isNull():
                    item.setIcon(QIcon(pm.scaled(140, 100, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                                 Qt.TransformationMode.SmoothTransformation)))
                item.setToolTip(path)
                self.wallpaper_list.addItem(item)
            if self.wallpaper_manager.current_index < self.wallpaper_list.count():
                self.wallpaper_list.setCurrentRow(self.wallpaper_manager.current_index)

        def _on_wp_add():
            files, _ = QFileDialog.getOpenFileNames(
                self.settings_dlg, tr("wallpaper_add"), "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)")
            for f in files:
                self.wallpaper_manager.add_wallpaper(f)
            _refresh_wallpaper_list()
            self.save_config()

        def _on_wp_remove():
            row = self.wallpaper_list.currentRow()
            if row >= 0:
                self.wallpaper_manager.remove_wallpaper(row)
                _refresh_wallpaper_list()
                self.save_config()

        def _on_wp_up():
            row = self.wallpaper_list.currentRow()
            if row > 0:
                self.wallpaper_manager.move_up(row)
                _refresh_wallpaper_list()
                self.wallpaper_list.setCurrentRow(row - 1)
                self.save_config()

        def _on_wp_down():
            row = self.wallpaper_list.currentRow()
            if 0 <= row < self.wallpaper_list.count() - 1:
                self.wallpaper_manager.move_down(row)
                _refresh_wallpaper_list()
                self.wallpaper_list.setCurrentRow(row + 1)
                self.save_config()

        def _on_wp_enabled_toggled(checked):
            self.wallpaper_manager.set_enabled(checked)
            self.save_config()

        def _on_wp_mode_changed(index):
            self.wallpaper_manager.mode = self.combo_wp_mode.currentData() or "loop"
            self.wallpaper_manager._preload_next()
            self.save_config()

        def _on_wp_interval_changed(value):
            self.wallpaper_manager.interval = int(value)
            self.lbl_wp_interval.setText(str(value))
            if self.wallpaper_manager.enabled:
                self.wallpaper_manager.start_slideshow()
            self.save_config()

        def _on_wp_fill_changed(index):
            self.wallpaper_manager.fill_mode = self.combo_wp_fill.currentData() or "fit"
            self.wallpaper_manager.wallpaper_changed.emit()
            self.save_config()

        def _on_wp_fade_toggled(checked):
            self.wallpaper_manager.fade = bool(checked)
            self.save_config()

        def _on_wp_dual_toggled(checked):
            self.wallpaper_manager.dual_screen = bool(checked)
            self.combo_wp_screen.setEnabled(not checked)
            self.save_config()

        def _on_wp_screen_changed(index):
            self.wallpaper_manager.screen_target = self.combo_wp_screen.currentData() or "main"
            self.save_config()

        def _on_wp_apply_desktop():
            ok = self.wallpaper_manager.apply_to_desktop()
            if ok:
                QMessageBox.information(self.settings_dlg, tr("wallpaper_apply_desktop"), tr("success"))
            else:
                QMessageBox.warning(self.settings_dlg, tr("wallpaper_apply_desktop"), tr("failed"))

        def _on_wp_apply_window():
            row = self.list_proj.currentRow() if hasattr(self, 'list_proj') else -1
            target_project = self.projects[row] if 0 <= row < len(self.projects) else None
            applied = False
            for win in self.windows:
                if target_project is not None and win.project is not target_project:
                    continue
                try:
                    win.project.background_type = "dynamic"
                    win.project.dynamic_bg_type = "slideshow"
                    win.setup_dynamic_bg()
                    applied = True
                except Exception as e:
                    log_message(f"应用轮播壁纸到悬浮窗失败: {e}", "ERROR")
            if applied:
                QMessageBox.information(self.settings_dlg, tr("wallpaper_apply_window"), tr("success"))
            else:
                QMessageBox.warning(self.settings_dlg, tr("wallpaper_apply_window"), tr("failed"))

        self.btn_wp_add.clicked.connect(_on_wp_add)
        self.btn_wp_remove.clicked.connect(_on_wp_remove)
        self.btn_wp_up.clicked.connect(_on_wp_up)
        self.btn_wp_down.clicked.connect(_on_wp_down)
        self.chk_wp_enabled.toggled.connect(_on_wp_enabled_toggled)
        self.combo_wp_mode.currentIndexChanged.connect(_on_wp_mode_changed)
        self.slider_wp_interval.valueChanged.connect(_on_wp_interval_changed)
        self.combo_wp_fill.currentIndexChanged.connect(_on_wp_fill_changed)
        self.chk_wp_fade.toggled.connect(_on_wp_fade_toggled)
        self.chk_wp_dual.toggled.connect(_on_wp_dual_toggled)
        self.combo_wp_screen.currentIndexChanged.connect(_on_wp_screen_changed)
        self.btn_wp_apply_desktop.clicked.connect(_on_wp_apply_desktop)
        self.btn_wp_apply_window.clicked.connect(_on_wp_apply_window)
        self.combo_wp_screen.setEnabled(not self.wallpaper_manager.dual_screen)

        _refresh_wallpaper_list()
        tabs.addTab(wrap_in_scroll(tab_wallpaper), tr("wallpaper_selector"))

        tabs.addTab(wrap_in_scroll(tab_plugin), "插件管理")

        self.tab_help = HelpTab(self)
        tabs.addTab(wrap_in_scroll(self.tab_help), tr("help"))

        main_layout.addWidget(tabs)

        grip_layout = QHBoxLayout()
        grip_layout.addStretch()
        grip_layout.addWidget(QSizeGrip(self.settings_dlg))
        main_layout.addLayout(grip_layout)

        _footer_engine = self._render_display_name(self.render_backend)
        if " → " in _footer_engine:
            _footer_engine = _footer_engine.split(" → ", 1)[1]
        self.lbl_render_footer = QLabel(_footer_engine)
        self.lbl_render_footer.setStyleSheet("color: gray; font-size: 9pt;")
        self.lbl_render_footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        _footer_lay = QHBoxLayout()
        _footer_lay.addStretch()
        _footer_lay.addWidget(self.lbl_render_footer)
        main_layout.addLayout(_footer_lay)

        self.settings_dlg.closeEvent = lambda event: self.on_settings_close(event)

        if tab == "help":
            tabs.setCurrentWidget(self.tab_help)
            if section:
                QTimer.singleShot(100, lambda: self.tab_help.navigate_to(section))

        _open_effect = QGraphicsOpacityEffect(container)
        container.setGraphicsEffect(_open_effect)
        _open_effect.setOpacity(0.0)
        self.settings_dlg.show()
        self._animate_dialog_open(self.settings_dlg, _open_effect)

        self._last_tab_idx = tabs.currentIndex()
        self._tab_overlay = None
        def _on_tab_changed(idx):
            self._animate_tab_switch(tabs, idx)
        tabs.currentChanged.connect(_on_tab_changed)

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
            self.plugin_right_tabs.setTabVisible(self._plugin_panels_tab_idx, False)
        else:
            self.plugin_right_tabs.setTabVisible(self._plugin_panels_tab_idx, True)
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
        dlg = self.settings_dlg
        if dlg is None:
            event.accept()
            return
        if getattr(dlg, '_closing', False):
            if hasattr(self, 'log_timer') and self.log_timer.isActive():
                self.log_timer.stop()
            self.settings_geometry = dlg.saveGeometry()
            self.save_config(force=True)
            self.plugin_manager.trigger_event("on_settings_closed")
            self.settings_dlg = None
            event.accept()
            return
        container = dlg.findChild(QFrame, "settingsContainer")
        effect = container.graphicsEffect() if container else None
        if isinstance(effect, QGraphicsOpacityEffect):
            dlg._closing = True
            fade = QPropertyAnimation(effect, b"opacity", dlg)
            fade.setDuration(150)
            fade.setStartValue(effect.opacity())
            fade.setEndValue(0.0)
            fade.setEasingCurve(QEasingCurve.Type.InCubic)
            fade.finished.connect(dlg.close)
            fade.start()
            dlg._close_fade_anim = fade
            event.ignore()
            return
        if hasattr(self, 'log_timer') and self.log_timer.isActive():
            self.log_timer.stop()
        self.settings_geometry = dlg.saveGeometry()
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
        if hasattr(self, 'plugin_right_tabs') and hasattr(self, '_plugin_log_tab_idx'):
            self.plugin_right_tabs.setTabVisible(self._plugin_log_tab_idx, enabled)
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
        dlg.setWindowTitle(f"倒计时·DJS - 权限管理 - {plugin.name}")
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

    def _format_proj_item_text(self, p, index=None):
        ptype = getattr(p, 'project_type', 'normal')
        icon = "🔁" if ptype == 'recurring' else "📅"
        pin = " 📌" if getattr(p, 'always_on_top', False) else ""
        idx_str = ""
        if index is not None:
            circled = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
            idx_str = circled[index] + " " if 0 <= index < len(circled) else f"#{index + 1} "
        sub = f"🎯 {p.target_date}" + (f" {p.target_time}" if getattr(p, 'target_time', '00:00') != '00:00' else "")
        return f"{idx_str}{icon}  {p.name}{pin}\n    {sub}"

    def add_project_ui(self):
        type_items = [tr("project_normal"), tr("project_recurring")]
        choice, ok = QInputDialog.getItem(self.settings_dlg, tr("add_project").strip(),
                                          tr("project_type") + ":", type_items, 0, False)
        if not ok:
            return
        new_proj = CountdownProject(screen_width=self.primaryScreen().size().width(),
                                     screen_height=self.primaryScreen().size().height())
        is_recurring = (choice == tr("project_recurring"))
        if is_recurring:
            new_proj.project_type = "recurring"
            new_proj.recur_weekdays = [0, 1, 2, 3, 4]
        self.projects.append(new_proj)
        item = QListWidgetItem()
        item.setText(self._format_proj_item_text(new_proj, len(self.projects) - 1))
        item.setData(Qt.ItemDataRole.UserRole, new_proj.name)
        self.list_proj.addItem(item)
        self.list_proj.setCurrentRow(len(self.projects) - 1)
        self.create_windows()
        self.save_config(force=True)
        if is_recurring:
            editor = ProjectEditorDialog(self, new_proj, self.settings_dlg)
            if editor.exec():
                self.list_proj.item(len(self.projects) - 1).setText(self._format_proj_item_text(new_proj, len(self.projects) - 1))
                self.create_windows()
                self.save_config(force=True)

    def edit_project_ui(self):
        row = self.list_proj.currentRow()
        if row >= 0:
            proj = self.projects[row]
            editor = ProjectEditorDialog(self, proj, self.settings_dlg)
            if editor.exec():
                self.list_proj.item(row).setText(self._format_proj_item_text(proj, row))
                self.create_windows()
                self.save_config(force=True)

    def del_project_ui(self):
        row = self.list_proj.currentRow()
        if row >= 0:
            if len(self.projects) <= 1:
                QMessageBox.warning(self.settings_dlg, "警告", "至少需要保留一个项目！")
                return
            proj = self.projects[row]
            confirm = QMessageBox(self.settings_dlg)
            confirm.setWindowTitle("确认删除")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.setText(f"确定要删除项目「{proj.name}」吗？")
            confirm.setInformativeText("此操作不可撤销，删除后无法恢复。")
            btn_yes = confirm.addButton("删除", QMessageBox.ButtonRole.DestructiveRole)
            confirm.addButton("取消", QMessageBox.ButtonRole.RejectRole)
            confirm.exec()
            if confirm.clickedButton() is not btn_yes:
                return
            del self.projects[row]
            self.list_proj.takeItem(row)
            for i in range(self.list_proj.count()):
                if i < len(self.projects):
                    self.list_proj.item(i).setText(self._format_proj_item_text(self.projects[i], i))
            self.create_windows()
            self.save_config(force=True)

    def _on_weather_source_changed(self, index):
        provider_map = {0: "qweather", 1: "custom"}
        self.weather_provider = provider_map.get(index, "qweather")
        self.weather_qweather_row.setVisible(self.weather_provider == "qweather")
        self.weather_custom_url_row.setVisible(self.weather_provider == "custom")
        self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _on_qweather_key_changed(self, text):
        self.qweather_api_key = text.strip()
        if self.weather_provider == "qweather":
            self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _on_qweather_host_changed(self, text):
        self.qweather_api_host = text.strip()
        if self.weather_provider == "qweather":
            self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _on_qw_mode_changed(self):
        is_custom = self.rb_qw_custom.isChecked()
        self.qw_custom_box.setVisible(is_custom)
        if not is_custom:
            self.edit_qweather_api_key.blockSignals(True)
            self.edit_qweather_api_host.blockSignals(True)
            self.edit_qweather_api_key.clear()
            self.edit_qweather_api_host.clear()
            self.edit_qweather_api_key.blockSignals(False)
            self.edit_qweather_api_host.blockSignals(False)
            self.qweather_api_key = ""
            self.qweather_api_host = ""
            if self.weather_provider == "qweather":
                self._apply_weather_config_to_windows()
            self.save_config(force=True)

    def _on_weather_url_changed(self, text):
        self.custom_weather_url = text.strip()
        if self.weather_provider == "custom":
            self._apply_weather_config_to_windows()
        self.save_config(force=True)

    def _apply_weather_config_to_windows(self):
        """将天气配置应用到所有窗口并刷新"""
        qw_key = (self.qweather_api_key or "").strip() or WeatherFetcher.QWEATHER_DEFAULT_KEY
        qw_host = (self.qweather_api_host or "").strip() or WeatherFetcher.QWEATHER_DEFAULT_HOST
        for w in self.windows:
            if hasattr(w, 'weather_fetcher') and w.weather_fetcher:
                w.weather_fetcher.api_provider = self.weather_provider
                w.weather_fetcher.custom_url_template = self.custom_weather_url
                w.weather_fetcher.qweather_api_key = qw_key
                w.weather_fetcher.qweather_api_host = qw_host
                w.weather_fetcher.fetch(w.project.weather_city)

    def _backup_config(self):
        import shutil
        backup_dir = os.path.join(self.data_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"config_backup_{timestamp}.json")
        try:
            shutil.copy2(self.config_path, backup_path)
            QMessageBox.information(self.settings_dlg, tr("success"), tr("backup_success") + f"\n{backup_path}")
        except Exception as e:
            QMessageBox.critical(self.settings_dlg, tr("warning"), f"{e}")

    def _restore_config(self):
        backup_dir = os.path.join(self.data_dir, "backups")
        if not os.path.exists(backup_dir):
            QMessageBox.information(self.settings_dlg, tr("warning"), "暂无备份文件")
            return
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("config_backup_")], reverse=True)
        if not backups:
            QMessageBox.information(self.settings_dlg, tr("warning"), "暂无备份文件")
            return
        choice, ok = QInputDialog.getItem(self.settings_dlg, tr("restore_config"),
                                          "选择要还原的备份:", backups, 0, False)
        if not ok:
            return
        import shutil
        backup_path = os.path.join(backup_dir, choice)
        try:
            shutil.copy2(backup_path, self.config_path)
            QMessageBox.information(self.settings_dlg, tr("success"), tr("restore_success"))
        except Exception as e:
            QMessageBox.critical(self.settings_dlg, tr("warning"), f"{e}")

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

    def _on_flip_animation_toggled(self, checked):
        self.enable_flip_animation = checked
        self.save_config(force=True)
        for win in self.windows:
            if hasattr(win, 'countdown_label'):
                win.countdown_label.enable_flip_animation = checked

    def _on_gpu_acceleration_toggled(self, checked):
        self.enable_gpu_acceleration = checked
        self.save_config(force=True)
        QMessageBox.information(getattr(self, 'settings_dlg', None), "GPU 加速", f"已{'启用' if checked else '关闭'} GPU 着色器加速。\n新的设置将在下次创建窗口或重启后完全生效。")

    def _render_display_name(self, backend):
        if backend == "auto":
            _auto = {"win32": tr("render_d3d11"), "darwin": tr("render_metal")}.get(sys.platform, tr("render_opengl"))
            return f"{tr('render_auto')} → {_auto}"
        idx = self.render_backend_values.index(backend) if backend in self.render_backend_values else -1
        if 0 <= idx < len(self.render_backend_labels):
            return self.render_backend_labels[idx]
        return backend

    def _on_render_backend_changed(self, index):
        new_backend = self.render_backend_values[index] if 0 <= index < len(self.render_backend_values) else "auto"
        if new_backend == self.render_backend:
            return
        self.render_backend = new_backend
        self.save_config(force=True)
        if hasattr(self, 'lbl_render_info'):
            self.lbl_render_info.setText(f"{tr('render_current')}: {self._render_display_name(new_backend)}  ·  💡 {tr('render_intel_tip')}")
        if hasattr(self, 'lbl_render_footer'):
            _n = self._render_display_name(new_backend)
            if " → " in _n:
                _n = _n.split(" → ", 1)[1]
            self.lbl_render_footer.setText(_n)
        reply = QMessageBox.question(
            self.settings_dlg if hasattr(self, 'settings_dlg') and self.settings_dlg else None,
            tr("render_backend"),
            tr("render_restart_hint"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.restart_application()

if __name__ == "__main__":
    import sys
    _single_instance_mutex = None
    _already_running = False
    if sys.platform == 'win32':
        try:
            _mutex_name = "Global\\DJS_Countdown_SingleInstance"
            _kernel32 = ctypes.windll.kernel32
            _ERROR_ALREADY_EXISTS = 183
            _single_instance_mutex = _kernel32.CreateMutexW(None, False, _mutex_name)
            if _kernel32.GetLastError() == _ERROR_ALREADY_EXISTS:
                _already_running = True
        except Exception:
            pass
    if _already_running:
        _pre_app = QApplication(sys.argv)
        _reply = QMessageBox.question(
            None,
            "倒计时已运行",
            "检测到一个进程已在运行，确定要开启新的进程吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if _reply != QMessageBox.StandardButton.Yes:
            sys.exit(0)
    try:
        with open(resource_path("data/countdown_config.json"), "r", encoding="utf-8") as _f:
            _rb = json.load(_f).get("render_backend", "auto")
    except Exception:
        _rb = "auto"
    if _rb == "software":
        os.environ["QSG_RHI_PREFER_SOFTWARE_RENDERER"] = "1"
    elif _rb in ("opengl", "vulkan", "metal", "d3d11", "d3d12"):
        os.environ["QSG_RHI_BACKEND"] = _rb
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
    fmt.setSamples(0)
    fmt.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    fmt.setAlphaBufferSize(0)
    QSurfaceFormat.setDefaultFormat(fmt)
    app = CountdownApp(sys.argv)
    sys.exit(app.exec())