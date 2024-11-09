import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QTime, QPoint, QEvent
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QAction, QImage, QPainter
from PyQt6.QtWidgets import (QTabWidget, QSpinBox, QTimeEdit, QSlider, 
                            QFileDialog, QHBoxLayout, QVBoxLayout, QProgressDialog,
                            QStyle)
import yt_dlp
import re
import cv2
from PyQt6.QtWidgets import (QTabWidget, QSpinBox, QTimeEdit, QSlider, 
                            QFileDialog, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QImage, QPixmap
from functools import wraps
import json
import logging
from datetime import datetime
import subprocess

# iOS 风格的全局样式
STYLE = """
/* 全局样式 */
QMainWindow {
    background-color: #F5F7FA;
}

/* 标签页样式 */
QTabWidget::pane {
    border: none;
    background-color: #F5F7FA;
}

QTabBar::tab {
    padding: 8px 16px;
    margin: 0;
    border: none;
    background-color: #EDF2F7;
    color: #4A5568;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #2B6CB0;
    border-bottom: 2px solid #4299E1;
}

QTabBar::tab:hover:!selected {
    background-color: #E2E8F0;
}

/* 分组框样式 */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 10px;
    padding: 12px;
    font-size: 13px;
    font-weight: 500;
    color: #1A202C;
}

/* 日志区域样式 */
QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 8px;
    color: #2D3748;
}

/* 输入框统一样式 */
QLineEdit {
    border: 1px solid #CBD5E0;
    border-radius: 6px;
    padding: 0 12px;
    background-color: #FFFFFF;
    color: #2D3748;
    font-size: 13px;
    min-height: 32px;
    selection-background-color: #007AFF;
}

QLineEdit:focus {
    border: 2px solid #4299E1;
    background-color: #EBF8FF;
}

QLineEdit::placeholder {
    color: #A0AEC0;
}

/* 按钮统一样式 */
QPushButton {
    background-color: #4299E1;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 0 15px;
    font-weight: 600;
    font-size: 13px;
    min-height: 32px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #3182CE;
}

QPushButton:pressed {
    background-color: #2B6CB0;
}

QPushButton:disabled {
    background-color: #E2E8F0;
    color: #A0AEC0;
}

/* 主要按钮 */
QPushButton#downloadButton, QPushButton#cancelButton {
    min-width: 100px;
    min-height: 36px;
    font-size: 14px;
    font-weight: 600;
}

/* 次要按钮 */
QPushButton[cssClass="secondary-button"] {
    background-color: #EDF2F7;
    color: #4299E1;
    border: 1px solid #4299E1;
    min-width: 70px;
    min-height: 32px;
}

QPushButton[cssClass="secondary-button"]:hover {
    background-color: #E2E8F0;
    color: #3182CE;
}

/* 分析按钮 */
QPushButton#analyzeButton {
    min-width: 90px;
    min-height: 32px;
}

/* 下拉框统一样式 */
QComboBox {
    border: 1px solid #CBD5E0;
    border-radius: 6px;
    padding: 0 12px;
    background-color: #FFFFFF;
    color: #2D3748;
    font-size: 13px;
    min-height: 32px;
}

QComboBox:focus {
    border-color: #4299E1;
    background-color: #EBF8FF;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

/* 复选框统一样式 */
QCheckBox {
    spacing: 6px;
    color: #2D3748;
    font-size: 13px;
    min-height: 32px;
    padding: 0 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #CBD5E0;
    border-radius: 4px;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked {
    background-color: #4299E1;
    border-color: #4299E1;
}

/* 进条统一样式 */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #EDF2F7;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4299E1;
    border-radius: 4px;
}

/* 标签样式 */
QLabel {
    min-height: 20px;
    color: #2D3748;
    font-size: 13px;
}

QLabel[cssClass="header"] {
    color: #1A202C;
    font-size: 24px;
    font-weight: 700;
}

QLabel[cssClass="section-header"] {
    color: #2D3748;
    font-size: 16px;
    font-weight: 600;
}

/* 特殊按钮样式 */
#downloadButton {
    background-color: #48BB78;
    font-size: 14px;
}

#downloadButton:hover {
    background-color: #38A169;
}

#downloadButton:disabled {
    background-color: #C6F6D5;
    color: #9AE6B4;
}

#cancelButton {
    background-color: #F56565;
    font-size: 14px;
}

#cancelButton:hover {
    background-color: #E53E3E;
}

#cancelButton:disabled {
    background-color: #FED7D7;
    color: #FCA5A5;
}

#analyzeButton {
    background-color: #805AD5;
}

#analyzeButton:hover {
    background-color: #6B46C1;
}

#analyzeButton:disabled {
    background-color: #E9D8FD;
    color: #B794F4;
}

/* 状态标签样式 */
QLabel[cssClass="status"] {
    color: #718096;
    font-size: 12px;
}

/* 错误文本样式 */
QLabel[cssClass="error"] {
    color: #E53E3E;
    font-size: 12px;
}

/* 成功文本样式 */
QLabel[cssClass="success"] {
    color: #38A169;
    font-size: 12px;
}

/* 进度信息标签样式 */
QLabel[cssClass="progress-info"] {
    color: #4A5568;
    font-size: 12px;
    min-width: 100px;
}

/* 分组框标题样式 */
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #4A5568;
    font-weight: 600;
}

/* 工具提示样式 */
QToolTip {
    background-color: #2D3748;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* 状态标签样式 */
QLabel[cssClass="status-success"] {
    color: #38A169;
}

QLabel[cssClass="status-error"] {
    color: #E53E3E;
}

QLabel[cssClass="status-warning"] {
    color: #D69E2E;
}
"""

class DownloadWorker(QThread):
    """下载工作线程"""
    progress = pyqtSignal(dict)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    log = pyqtSignal(str)

    def __init__(self, url, options):
        super().__init__()
        self.url = url
        self.options = options
        self.is_cancelled = False

    def run(self):
        try:
            with yt_dlp.YoutubeDL(self.options) as ydl:
                self.log.emit("开始获取视频信息...")
                info = ydl.extract_info(self.url, download=True)
                if info and not self.is_cancelled:
                    self.finished.emit(info.get('title', '未知标题'))
                elif self.is_cancelled:
                    self.log.emit("下载已取消")
        except Exception as e:
            if not self.is_cancelled:
                self.error.emit(str(e))

    def cancel(self):
        self.is_cancelled = True

class VideoAnalyzer(QThread):
    """视频分析线程"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    log = pyqtSignal(str)
    status = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.is_cancelled = False

    def run(self):
        try:
            self.status.emit("正在连接服务器...")
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self.is_cancelled:
                    return

                self.status.emit("正在获取视频信息...")
                self.log.emit("开始分析视频信息...")
                info = ydl.extract_info(self.url, download=False)
                
                if not info or self.is_cancelled:
                    return

                self.status.emit("正在解析可用格式...")
                formats = []
                if 'formats' in info:
                    total_formats = len(info['formats'])
                    for i, f in enumerate(info['formats']):
                        if self.is_cancelled:
                            return

                        # 更新进度
                        self.progress.emit(int((i + 1) * 100 / total_formats))
                        
                        try:
                            # 获取格式信息
                            format_id = f.get('format_id', 'N/A')
                            ext = f.get('ext', 'N/A')
                            
                            # 获取分辨率信息
                            width = f.get('width', 0) or 0
                            height = f.get('height', 0) or 0
                            resolution = "N/A"
                            if width > 0 and height > 0:
                                resolution = f"{width}x{height}"
                            
                            # 获取码率信息
                            vbr = f.get('vbr', 0) or 0
                            abr = f.get('abr', 0) or 0
                            vbr_str = f"{vbr:.1f}Kbps" if vbr > 0 else ""
                            abr_str = f"{abr:.1f}Kbps" if abr > 0 else ""
                            
                            # 获取编码信息
                            vcodec = f.get('vcodec', 'none')
                            acodec = f.get('acodec', 'none')
                            
                            # 获取文件大小
                            filesize = f.get('filesize', 0) or 0
                            filesize_str = f"{filesize/1024/1024:.1f}MB" if filesize > 0 else "未知"

                            # 确定格式类型和详细信息
                            format_type = ""
                            format_details = ""
                            
                            if vcodec != 'none' and acodec != 'none':
                                format_type = "视频+音频"
                                format_details = f"{resolution}"
                                if vbr_str:
                                    format_details += f" {vbr_str}"
                            elif vcodec != 'none':
                                format_type = "仅视频"
                                format_details = f"{resolution}"
                                if vbr_str:
                                    format_details += f" {vbr_str}"
                            elif acodec != 'none':
                                format_type = "仅音频"
                                format_details = abr_str if abr_str else "未知码率"
                            else:
                                continue

                            # 创建格式描述
                            description = f"{format_type} - {format_details} [{ext}] - {filesize_str}"

                            # 添加格式信息
                            format_info = {
                                'description': description,
                                'format_id': format_id,
                                'ext': ext,
                                'resolution': resolution,
                                'vcodec': vcodec,
                                'acodec': acodec,
                                'filesize': filesize,
                                'height': height
                            }
                            formats.append(format_info)
                            
                        except Exception as e:
                            self.log.emit(f"处理格式时出错: {str(e)}")
                            continue

                    if not self.is_cancelled and formats:
                        # 按类型和质量排序
                        formats.sort(key=lambda x: (
                            x['vcodec'] != 'none' and x['acodec'] != 'none',
                            x.get('height', 0) or 0,
                            x.get('filesize', 0) or 0
                        ), reverse=True)
                        
                        self.status.emit("分析完成")
                        self.finished.emit(formats)
                    else:
                        self.error.emit("未找到可用的视频格")
                else:
                    self.error.emit("无法获取视频格式信息")
                
        except Exception as e:
            if not self.is_cancelled:
                self.error.emit(str(e))
                self.status.emit("分析失败")

    def cancel(self):
        self.is_cancelled = True
        self.status.emit("正在取消...")

class QRangeSlider(QWidget):
    """自定义的范围选择滑块"""
    valueChanged = pyqtSignal(tuple)  # 发送(min, max)值的信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_value = 0
        self.max_value = 100
        self.current_min = 0
        self.current_max = 100
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建两个滑块
        self.min_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_slider = QSlider(Qt.Orientation.Horizontal)
        
        # 设置滑块范围
        self.min_slider.setRange(self.min_value, self.max_value)
        self.max_slider.setRange(self.min_value, self.max_value)
        
        # 设置初始值
        self.min_slider.setValue(self.current_min)
        self.max_slider.setValue(self.current_max)
        
        # 设置滑块样式
        slider_style = """
            QSlider {
                min-height: 30px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #E2E8F0;
                margin: 0 12px;
            }
            QSlider::handle:horizontal {
                background: #4299E1;
                border: 2px solid #4299E1;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #3182CE;
                border-color: #3182CE;
            }
        """
        self.min_slider.setStyleSheet(slider_style)
        self.max_slider.setStyleSheet(slider_style)
        
        # 连接信号
        self.min_slider.valueChanged.connect(self._min_value_changed)
        self.max_slider.valueChanged.connect(self._max_value_changed)
        
        # 添加到布局
        layout.addWidget(self.min_slider)
        layout.addWidget(self.max_slider)

    def _min_value_changed(self, value):
        """最值滑块变化处理"""
        if value > self.current_max:
            value = self.current_max
            self.min_slider.setValue(value)
        self.current_min = value
        self.valueChanged.emit((self.current_min, self.current_max))

    def _max_value_changed(self, value):
        """最大值滑变化处理"""
        if value < self.current_min:
            value = self.current_min
            self.max_slider.setValue(value)
        self.current_max = value
        self.valueChanged.emit((self.current_min, self.current_max))

    def setRange(self, min_value, max_value):
        """设置滑块范围"""
        self.min_value = min_value
        self.max_value = max_value
        self.min_slider.setRange(min_value, max_value)
        self.max_slider.setRange(min_value, max_value)
        self.min_slider.setValue(min_value)
        self.max_slider.setValue(max_value)

    def values(self):
        """获取当前值"""
        return (self.current_min, self.current_max)

def handle_exception(func):
    """异常处理装饰器"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.show_message(
                "错误",
                f"操作失败: {str(e)}",
                QMessageBox.Icon.Critical
            )
            self.append_log(f"错误: {str(e)}")
    return wrapper

class ModernVideoDownloaderGUI(QMainWindow):
    update_progress_signal = pyqtSignal(dict)
    append_log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能视频下载器")
        self.setMinimumSize(960,1000)
        self.setStyleSheet(STYLE)
        
        # 初始化成员变量
        self.current_download = None
        self.current_analyzer = None
        self.available_formats = []
        self.is_analyzing = False
        self.analyze_button_handler = None
        
        # 初始化进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        
        # 初始化其他UI组件
        self.progress_label = QLabel("准备下载...")
        self.file_label = QLabel("文件名:")
        self.size_label = QLabel("文件大小:")
        self.downloaded_label = QLabel("已下载:")
        self.speed_label = QLabel("速度:")
        self.eta_label = QLabel("剩余时间:")
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号
        self.update_progress_signal.connect(self._update_progress)
        self.append_log_signal.connect(self._append_log)
        
        # 加载配置
        self.load_settings()
        
        # 初始化日志
        self.setup_logging()
        
        # 删除这里的format_combo初始化，移到create_downloader_tab中
        # self.format_combo = QComboBox()
        # self.format_combo.setEnabled(False)
        # self.format_combo.addItem("请先分析视频...")
        # self.format_combo.currentIndexChanged.connect(self.on_format_changed)

    def init_ui(self):
        # 创建主窗口部件和局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_downloader_tab(), "视频下载")
        self.tab_widget.addTab(self.create_processor_tab(), "视频处理")
        main_layout.addWidget(self.tab_widget)

    def create_downloader_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # 标题区域
        header_label = QLabel("视频下载")
        header_label.setProperty("cssClass", "header")
        layout.addWidget(header_label)

        # URL输入区域 - iOS 风格卡片
        url_card = QGroupBox()
        url_card.setStyleSheet("""
            QGroupBox {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        url_layout = QVBoxLayout(url_card)
        url_layout.setSpacing(12)
        
        url_header = QLabel("视频地址")
        url_header.setProperty("cssClass", "section-header")
        url_layout.addWidget(url_header)
        
        input_container = QHBoxLayout()
        input_container.setSpacing(12)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入或粘贴视频URL (Ctrl+V)")
        self.url_input.setMinimumWidth(400)
        self.url_input.textChanged.connect(self.on_url_changed)
        self.url_input.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        paste_action = QAction("粘贴", self.url_input)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_url)
        self.url_input.addAction(paste_action)
        
        self.paste_button = QPushButton("粘贴")
        self.paste_button.setProperty("cssClass", "secondary-button")
        self.paste_button.clicked.connect(self.paste_url)
        
        self.analyze_button = QPushButton("分析视频")
        self.analyze_button.setObjectName("analyzeButton")
        self.analyze_button.clicked.connect(self.analyze_video)
        
        input_container.addWidget(self.url_input, 7)
        input_container.addWidget(self.paste_button, 1)
        input_container.addWidget(self.analyze_button, 2)
        
        url_layout.addLayout(input_container)
        layout.addWidget(url_card)

        # 下载选项区域 - iOS 风格卡片
        options_card = QGroupBox()
        options_layout = QVBoxLayout(options_card)
        options_layout.setSpacing(16)

        options_header = QLabel("下载选项")
        options_header.setProperty("cssClass", "section-header")
        options_layout.addWidget(options_header)

        # 格式择
        format_container = QWidget()
        format_layout = QHBoxLayout(format_container)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(12)
        
        format_label = QLabel("视频格式")
        format_label.setMinimumWidth(80)
        
        # 创建下载格式选择下拉菜单
        self.download_format_combo = QComboBox()  # 改名以区分用途
        self.download_format_combo.setEnabled(False)  # 初始状态禁用
        self.download_format_combo.addItem("请先分析视频...")
        self.download_format_combo.currentIndexChanged.connect(self.on_download_format_changed)  # 更新信号连接
        self.download_format_combo.setMinimumWidth(350)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.download_format_combo, 1)
        
        # 分析进度
        self.analyze_progress = QProgressBar()
        self.analyze_progress.setFixedWidth(120)
        self.analyze_progress.hide()
        self.analyze_status = QLabel("")
        
        format_layout.addWidget(self.analyze_progress)
        format_layout.addWidget(self.analyze_status)
        
        options_layout.addWidget(format_container)

        # 下载选项复框
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(20)
        
        self.subtitle_check = QCheckBox("下载字幕")
        self.thumbnail_check = QCheckBox("下载缩略图")
        self.metadata_check = QCheckBox("包含元数据")
        
        checkbox_layout.addWidget(self.subtitle_check)
        checkbox_layout.addWidget(self.thumbnail_check)
        checkbox_layout.addWidget(self.metadata_check)
        checkbox_layout.addStretch()
        
        options_layout.addWidget(checkbox_container)

        # 保存位置
        save_container = QWidget()
        save_layout = QHBoxLayout(save_container)
        save_layout.setContentsMargins(0, 0, 0, 0)
        save_layout.setSpacing(12)
        
        save_label = QLabel("保存位置")
        save_label.setMinimumWidth(80)
        self.save_path = QLineEdit()
        self.save_path.setText(os.path.expanduser("~/Downloads"))
        self.browse_button = QPushButton("浏览")
        self.browse_button.setProperty("cssClass", "secondary-button")
        self.browse_button.clicked.connect(self.browse_folder)
        
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_path, 1)
        save_layout.addWidget(self.browse_button)
        
        options_layout.addWidget(save_container)

        # Cookies选择
        cookies_container = QWidget()
        cookies_layout = QHBoxLayout(cookies_container)
        cookies_layout.setContentsMargins(0, 0, 0, 0)
        cookies_layout.setSpacing(12)

        cookies_label = QLabel("Cookies文件")
        cookies_label.setMinimumWidth(80)
        self.cookies_path = QLineEdit()
        self.cookies_path.setPlaceholderText("可选: 用于下载需要登录的视频")
        self.browse_cookies_button = QPushButton("浏览")
        self.browse_cookies_button.setProperty("cssClass", "secondary-button")
        self.browse_cookies_button.clicked.connect(self.browse_cookies)

        cookies_layout.addWidget(cookies_label)
        cookies_layout.addWidget(self.cookies_path, 1)
        cookies_layout.addWidget(self.browse_cookies_button)

        options_layout.addWidget(cookies_container)
        layout.addWidget(options_card)

        # 进度区域
        progress_card = QGroupBox("下载进度")
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setSpacing(12)

        # 添加详细进度信息
        progress_info = QWidget()
        progress_info_layout = QGridLayout(progress_info)
        progress_info_layout.setContentsMargins(0, 0, 0, 0)

        self.file_label = QLabel("文件名:")
        self.size_label = QLabel("文件大小:")
        self.downloaded_label = QLabel("已下载:")
        self.speed_label = QLabel("速度:")
        self.eta_label = QLabel("剩余时间:")

        progress_info_layout.addWidget(self.file_label, 0, 0)
        progress_info_layout.addWidget(self.size_label, 0, 1)
        progress_info_layout.addWidget(self.downloaded_label, 1, 0)
        progress_info_layout.addWidget(self.speed_label, 1, 1)
        progress_info_layout.addWidget(self.eta_label, 1, 2)

        progress_layout.addWidget(progress_info)
        progress_layout.addWidget(self.progress_bar)
        layout.addWidget(progress_card)

        # 日志区域
        log_card = QGroupBox()
        log_layout = QVBoxLayout(log_card)
        log_layout.setSpacing(12)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(120)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_card)

        # 控制按钮区域
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(20)
        
        button_layout.addStretch()
        
        self.download_button = QPushButton("开始下载")
        self.download_button.setObjectName("downloadButton")
        self.download_button.setMinimumWidth(120)
        self.download_button.setMinimumHeight(36)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.start_download)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setMinimumHeight(36)
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_download)
        
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addWidget(button_container)

        tab.setLayout(layout)
        return tab

    def paste_url(self):
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择保存位置")
        if folder:
            self.save_path.setText(folder)

    def get_format_option(self):
        """获取当前选择的格式选项"""
        try:
            # 获取当前选择的format_id
            format_id = self.download_format_combo.currentData()  # 修改这里
            
            # 如果没有format_id，使用默认值
            if not format_id:
                return "bv*+ba/b"  # 默认最佳质量
            
            # 记录日志
            self.log_text.append(f"选择下载格式: {self.download_format_combo.currentText()} (ID: {format_id})")  # 修改这里
            return format_id
        
        except Exception as e:
            self.log_text.append(f"获取格式选项失败: {str(e)}")
            return "bv*+ba/b"  # 出错时使用默认值

    def update_progress(self, d):
        # 通过信号发送更新
        self.update_progress_signal.emit(d)

    def _update_progress(self, d):
        """实际更新进度的方法，在主线程中执行"""
        if d['status'] == 'downloading':
            try:
                # 清理ANSI转义序列
                percent_str = re.sub(r'\x1b\[[0-9;]*[mG]', '', d.get('_percent_str', '0%'))
                speed_str = re.sub(r'\x1b\[[0-9;]*[mG]', '', d.get('_speed_str', '--'))
                eta_str = re.sub(r'\x1b\[[0-9;]*[mG]', '', d.get('_eta_str', '--'))
                
                # 更新进度条
                percentage = float(percent_str.replace('%', '').strip())
                self.progress_bar.setValue(int(percentage))
                
                # 更新详细信息
                filename = os.path.basename(d.get('filename', '未知文件'))
                total_bytes = d.get('total_bytes', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                self.file_label.setText(f"文件名: {filename}")
                self.size_label.setText(f"文件大小: {self.format_size(total_bytes)}")
                self.downloaded_label.setText(f"已下载: {self.format_size(downloaded_bytes)}")
                self.speed_label.setText(f"速度: {speed_str}")
                self.eta_label.setText(f"剩余时间: {eta_str}")
                
                # 设置窗口标题显示进度
                self.setWindowTitle(f"视频下载器 - {percent_str}")
                
            except Exception as e:
                self.append_log_signal.emit(f"进度更新误: {str(e)}")

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def start_download(self):
        """开始载的处理"""
        try:
            url = self.url_input.text().strip()
            if not url:
                QMessageBox.warning(self, "错误", "请输入视频URL")
                return

            # 验证格式选择
            current_format = self.download_format_combo.currentText()
            if not current_format or current_format == "请先分析视频..." or current_format == "----- 可用格式 -----":
                QMessageBox.warning(self, "错误", "请选择有效的下载格式")
                return

            # 验证保存路径
            save_path = self.save_path.text().strip()
            if not save_path:
                QMessageBox.warning(self, "错误", "请选择保存位置")
                return

            # 设置下载选项
            ydl_opts = {
                'format': self.get_format_option(),
                'outtmpl': os.path.join(save_path, '%(title)s-%(id)s.%(ext)s'),
                'progress_hooks': [self.update_progress],
                'writesubtitles': self.subtitle_check.isChecked(),
                'writethumbnail': self.thumbnail_check.isChecked(),
                'socket_timeout': 30,
                'retries': 10,
                'ignoreerrors': True,
                'no_warnings': False,
                'quiet': False,
                'verbose': True,
            }

            # 检查是否提供了 cookies 文件
            cookies_file = self.cookies_path.text().strip()
            if cookies_file:
                if os.path.exists(cookies_file):
                    ydl_opts['cookiefile'] = cookies_file
                    self.append_log(f"使用 cookies 文件: {cookies_file}")
                else:
                    self.append_log(f"警告: cookies 文件不存在: {cookies_file}")

            if self.metadata_check.isChecked():
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                }]

            # 禁用相关按钮
            self.download_button.setEnabled(False)
            self.analyze_button.setEnabled(False)
            self.download_format_combo.setEnabled(False)
            self.cancel_button.setEnabled(True)

            # 重置进度显示
            self.progress_bar.setValue(0)
            self.progress_label.setText("准备下载...")
            self.speed_label.setText("速度: --")
            self.eta_label.setText("剩余时间: --")

            # 创建并启动下载线程
            self.current_download = DownloadWorker(url, ydl_opts)
            self.current_download.progress.connect(self.update_progress)
            self.current_download.finished.connect(self.download_finished)
            self.current_download.error.connect(self.download_error)
            self.current_download.log.connect(self.append_log)
            
            self.append_log("开始下载...")
            self.current_download.start()

        except Exception as e:
            self.append_log(f"启动下载时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"启动下载失败: {str(e)}")
            self.reset_ui()

    def cancel_download(self):
        if self.current_download and self.current_download.isRunning():
            # 先禁用取消按钮防止重复点击
            self.cancel_button.setEnabled(False)
            # 设置取消标
            self.current_download.is_cancelled = True
            # 等待线程结束
            self.current_download.wait(1000)  # 等待最多1秒
            if self.current_download.isRunning():
                self.current_download.terminate()
            self.append_log_signal.emit("下载已取消")
            self.reset_ui()

    def download_finished(self, title):
        self.log_text.append(f"成功下载: {title}")
        self.reset_ui()
        QMessageBox.information(self, "完成", f"视频 {title} 下载完成！")

    def download_error(self, error_msg):
        self.log_text.append(f"错误: {error_msg}")
        self.reset_ui()
        self.show_message("错误", f"下载失败: {error_msg}", QMessageBox.Icon.Critical)

    def reset_ui(self):
        """重置UI状态"""
        self.download_button.setEnabled(True)
        self.download_button.setVisible(True)
        self.cancel_button.setEnabled(False)
        self.analyze_button.setEnabled(True)
        self.download_format_combo.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("准备下载...")
        self.speed_label.setText("速度: --")
        self.eta_label.setText("剩余时间: --")

    def append_log(self, message):
        """通过信号发送日志更"""
        self.append_log_signal.emit(message)

    def _append_log(self, message):
        """实际添加日志的方法，在主线程中执行"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        """窗口关闭时的处理"""
        try:
            # 停止播放
            if self.is_playing:
                self.preview_timer.stop()
                self.is_playing = False
                
            # 释放视频资源
            if hasattr(self, 'cap') and self.cap:
                self.cap.release()
                
            # 停止所有定时器
            if hasattr(self, 'preview_timer'):
                self.preview_timer.stop()
                
            # 检查下载线程
            if self.current_download and self.current_download.isRunning():
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('确认退出')
                msg_box.setText("下载正在进行中，确定要退出吗？")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | 
                                         QMessageBox.StandardButton.No)
                msg_box.setDefaultButton(QMessageBox.StandardButton.No)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #FFFFFF;
                    }
                    QMessageBox QLabel {
                        color: #2D3748;
                        min-width: 300px;
                        padding: 12px;
                        background-color: #FFFFFF;
                    }
                    QPushButton {
                        background-color: #4299E1;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 16px;
                        min-width: 80px;
                        margin: 6px;
                    }
                    QPushButton:hover {
                        background-color: #3182CE;
                    }
                    QMessageBox QFrame {
                        background-color: #FFFFFF;
                    }
                """)
                
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    if self.current_download:
                        self.current_download.is_cancelled = True
                        self.current_download.wait(1000)
                        if self.current_download.isRunning():
                            self.current_download.terminate()
                    event.accept()
                else:
                    event.ignore()
                    return
                    
            # 检查分析线程
            if self.current_analyzer and self.current_analyzer.isRunning():
                self.current_analyzer.cancel()
                self.current_analyzer.wait(1000)
                
            event.accept()
            
        except Exception as e:
            self.show_message("错误", f"关闭程序时出错: {str(e)}", QMessageBox.Icon.Critical)
            event.accept()

    def analyze_video(self):
        """分析视频"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "错误", "请输入视频URL")
            return

        if self.is_analyzing:
            # 如果正在分析，则取消分析
            self.cancel_analysis()
            return

        # 设置分析状态
        self.is_analyzing = True

        # 更新UI状态
        self.analyze_button.setText("取消分析")
        self.download_button.setEnabled(False)
        self.download_format_combo.clear()  # 使用新的命名
        self.download_format_combo.addItem("正在分析视频...")
        self.download_format_combo.setEnabled(False)
        self.log_text.append("开始分析视频信息...")

        # 显示进度条
        self.analyze_progress.setValue(0)
        self.analyze_progress.show()
        self.analyze_status.setText("准备分析...")

        # 创建并启动分析线程
        self.current_analyzer = VideoAnalyzer(url)
        self.current_analyzer.finished.connect(self.analysis_finished)
        self.current_analyzer.error.connect(self.analysis_error)
        self.current_analyzer.log.connect(self.append_log)
        self.current_analyzer.progress.connect(self.analyze_progress.setValue)
        self.current_analyzer.status.connect(self.analyze_status.setText)
        
        self.current_analyzer.start()

    def cancel_analysis(self):
        if self.current_analyzer and self.current_analyzer.isRunning():
            self.current_analyzer.cancel()
            self.analyze_button.setEnabled(False)
            self.analyze_button.setText("正在取消...")
            self.is_analyzing = False

    def analysis_finished(self, formats):
        """分析完成后的处理"""
        try:
            # 重置分析状态
            self.is_analyzing = False
            
            # 恢复按钮状态
            self.analyze_button.setEnabled(True)
            self.analyze_button.setText("分析视频")
            
            # 清空并更新格式列表
            self.download_format_combo.blockSignals(True)  # 使用新的命名
            self.download_format_combo.clear()
            
            if formats:
                # 启用下拉框
                self.download_format_combo.setEnabled(True)
                
                # 添加默认的智能选择选项
                default_formats = [
                    {"description": "最佳质量 (自动选择)", "format_id": "bv*+ba/b"},
                    {"description": "720p (自动选择)", "format_id": "bv*[height<=720]+ba/b"},
                    {"description": "480p (自动选择)", "format_id": "bv*[height<=480]+ba/b"},
                    {"description": "仅音频 (最佳质量)", "format_id": "ba/b"}
                ]
                
                # 添加默认选项
                for fmt in default_formats:
                    self.download_format_combo.addItem(fmt["description"], fmt["format_id"])
                
                # 添加分隔线
                self.download_format_combo.insertSeparator(self.download_format_combo.count())
                
                # 添加所有可用格式
                for fmt in formats:
                    if 'description' in fmt and 'format_id' in fmt:
                        self.download_format_combo.addItem(fmt['description'], fmt['format_id'])
                
                # 选择第一个选项
                self.download_format_combo.setCurrentIndex(0)
                
                # 启用下载按钮
                self.download_button.setEnabled(True)
                
                # 记录日志
                self.log_text.append(f"分析完成，找到 {len(formats)} 个可用格式")
                
                # 确保下拉菜单可用
                QApplication.processEvents()  # 处理待处理的事件
                self.download_format_combo.setEnabled(True)
                self.download_format_combo.showPopup()  # 测试下拉功能
                
            else:
                # 如果没有找到格式，显示提示
                self.download_format_combo.addItem("未找到可用格式", "")
                self.download_format_combo.setEnabled(False)
                self.download_button.setEnabled(False)
                self.log_text.append("分析完成，但未找到可用格式")
            
            self.download_format_combo.blockSignals(False)  # 恢复信号
            
            # 手动触发格式变化处理
            self.on_download_format_changed(self.download_format_combo.currentIndex())
            
            # 隐藏进度条
            self.analyze_progress.hide()
            self.analyze_status.clear()
            
        except Exception as e:
            self.log_text.append(f"更新格式列表时出错: {str(e)}")
            self.analysis_error(str(e))

    def analysis_error(self, error_msg):
        """分析错误处理"""
        try:
            # 重置分析状态
            self.is_analyzing = False
            
            # 恢复按钮状态
            self.analyze_button.setEnabled(True)
            self.analyze_button.setText("分析视频")
            
            # 重置格式下拉菜单
            self.download_format_combo.clear()
            self.download_format_combo.addItem("请先分析视频...")
            self.download_format_combo.setEnabled(False)
            
            # 禁用下载按钮
            self.download_button.setEnabled(False)
            
            # 隐藏进度条
            self.analyze_progress.hide()
            self.analyze_status.clear()
            
            # 显示错误信息
            self.log_text.append(f"分析错误: {error_msg}")
            self.show_message("错误", f"视频分析失败: {error_msg}", QMessageBox.Icon.Critical)
            
        except Exception as e:
            self.log_text.append(f"处理分析错误时出错: {str(e)}")

    def browse_cookies(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择 Cookies 文件",
            "",
            "Cookies Files (*.txt);;All Files (*.*)"
        )
        if file_name:
            self.cookies_path.setText(file_name)

    def on_url_changed(self, text):
        """当URL输入框内容变化时调用"""
        text = text.strip()
        if text:
            # 检查是否是URL格式
            if text.startswith(('http://', 'https://', 'www.')):
                self.analyze_button.setEnabled(True)
                # 自动发分析
                if not self.is_analyzing:
                    self.analyze_video()
            else:
                self.analyze_button.setEnabled(False)
        else:
            self.analyze_button.setEnabled(False)

    @handle_exception
    def browse_video(self, *args):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mkv *.mov);;所有文件 (*.*)"
        )
        if file_name:
            self.video_path.setText(file_name)
            self.load_video_info(file_name)

    def load_video_info(self, video_path):
        """加载视频信息"""
        try:
            # 释放之前的视频资源
            if hasattr(self, 'cap') and self.cap:
                self.cap.release()
                
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                raise Exception("无法打开视频文件")
                
            # 获取视频信息
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.total_duration = total_frames / fps  # 保存总时长
            
            # 设置滑块属性
            self.video_slider.setRange(0, total_frames - 1)
            self.video_slider.setSingleStep(1)  # 设置单步值
            self.video_slider.setPageStep(int(fps))  # 设置页面步长为1秒的帧数
            
            # 更新UI显示
            self.video_slider.setRange(0, total_frames - 1)
            total_time = QTime(0, 0).addSecs(int(self.total_duration))
            self.start_time.setTime(QTime(0, 0))
            self.end_time.setTime(total_time)
            
            # 显示视频信息
            info_text = f"视频信息:\n分辨率: {width}x{height}\n帧率: {fps:.2f}fps\n时长: {self.format_time(self.total_duration)}"
            self.preview_label.setText(info_text)
            
            # 加载一帧作为预览
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = 0
                self.display_frame(frame)
                
            # 重置播放状态
            self.is_playing = False
            self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            
            # 启用控制按钮
            self.play_btn.setEnabled(True)
            self.prev_frame_btn.setEnabled(True)
            self.next_frame_btn.setEnabled(True)
            self.extract_btn.setEnabled(True)
            
            # 初始化时间范围
            self.start_time.setTime(QTime(0, 0))
            total_time = QTime(0, 0).addSecs(int(self.total_duration))
            self.end_time.setTime(total_time)
            
            # 保存初始的有效时间值
            self.last_valid_start_time = QTime(0, 0)
            self.last_valid_end_time = total_time
            
            # 连接时间变化信号
            self.start_time.timeChanged.connect(self.on_start_time_changed)
            self.end_time.timeChanged.connect(self.on_end_time_changed)
            
            # 设置悬浮进度条
            self.floating_progress.setRange(0, total_frames - 1)
            self.floating_progress.setTotalTime(self.format_time(self.total_duration))
            self.floating_progress.valueChanged.connect(self.on_floating_progress_changed)
            
        except Exception as e:
            self.show_message("错误", f"加载视频失败: {str(e)}", QMessageBox.Icon.Critical)
            # 禁用控制按钮
            self.play_btn.setEnabled(False)
            self.prev_frame_btn.setEnabled(False)
            self.next_frame_btn.setEnabled(False)
            self.extract_btn.setEnabled(False)

    def toggle_preview_playback(self):
        """切换播放/暂停状态"""
        if not self.cap:
            self.show_message("提示", "请先选择视频文件", QMessageBox.Icon.Information)
            return
            
        if self.is_playing:
            # 暂停播放
            self.preview_timer.stop()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.play_btn.setText("播放")
        else:
            # 开始播放
            if self.current_frame >= self.cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
                # 如果到达视频末尾，重新开始
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.current_frame = 0
                
            # 使用视频的实际帧率设置定时器
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.preview_timer.setInterval(int(1000 / fps))  # 转换为毫秒
            self.preview_timer.start()
            
            self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.play_btn.setText("暂停")
        
        self.is_playing = not self.is_playing

    def update_frame(self):
        """更新视频帧"""
        if not self.cap:
            return
            
        try:
            if self.current_frame >= self.cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
                # 到达视频末尾
                self.preview_timer.stop()
                self.is_playing = False
                self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
                self.play_btn.setText("播放")
                return

            # 设置当前帧位置
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            ret, frame = self.cap.read()
            
            if ret:
                self.display_frame(frame)
                # 更新进度条位置，但不触发valueChanged信号
                self.video_slider.blockSignals(True)
                self.video_slider.setValue(self.current_frame)
                self.video_slider.blockSignals(False)
                
                # 更新悬浮进度条
                if hasattr(self, 'floating_progress'):
                    self.floating_progress.blockSignals(True)
                    self.floating_progress.setValue(self.current_frame)
                    fps = self.cap.get(cv2.CAP_PROP_FPS)
                    current_time = self.current_frame / fps
                    self.floating_progress.setCurrentTime(self.format_time(current_time))
                    self.floating_progress.blockSignals(False)
                
                # 更新时间显示
                self.update_time_display()
                # 更新当前帧计
                self.current_frame += 1
            else:
                self.preview_timer.stop()
                self.is_playing = False
                self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
                self.play_btn.setText("播放")
                
        except Exception as e:
            self.preview_timer.stop()
            self.is_playing = False
            self.show_message("错误", f"播放出错: {str(e)}", QMessageBox.Icon.Critical)

    def display_frame(self, frame):
        """显示视频帧"""
        try:
            if frame is None:
                return
                
            # 获取预览容器的尺寸
            container_size = self.preview_label.parent().size()
            
            # 转换颜色间
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 计算缩放尺寸，保持宽高比
            height, width = frame_rgb.shape[:2]
            aspect_ratio = width / height
            
            if container_size.width() / container_size.height() > aspect_ratio:
                # 以高度为基准缩放
                new_height = container_size.height()
                new_width = int(new_height * aspect_ratio)
            else:
                # 以宽度为基准缩放
                new_width = container_size.width()
                new_height = int(new_width / aspect_ratio)
                
            # 缩放帧
            frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
            
            # 创建QImage
            image = QImage(
                frame_resized.data,
                new_width,
                new_height,
                frame_resized.strides[0],
                QImage.Format.Format_RGB888
            )
            
            # 创建QPixmap并设置给标签
            pixmap = QPixmap.fromImage(image)
            
            # 计算居中位置
            x = (container_size.width() - new_width) // 2
            y = (container_size.height() - new_height) // 2
            
            # 更新标签位置和大小
            self.preview_label.setGeometry(x, y, new_width, new_height)
            self.preview_label.setPixmap(pixmap)
            
        except Exception as e:
            self.show_message("错误", f"显示帧失败: {str(e)}", QMessageBox.Icon.Critical)

    def on_slider_changed(self, value):
        """当滑值改变时调用"""
        if not self.cap or self.video_slider.signalsBlocked():
            return
            
        # 更新时间显示
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = value / fps
        
        # 更新当前时间显示
        self.current_time.setText(self.format_time(current_time))
        # 修复：使用duration_label替代time_label
        self.duration_label.setText(f"/ {self.format_time(self.total_duration)}")
        
        # 如果是用户拖动导致的改变，更新预览
        if self.video_slider.isSliderDown():
            # 暂停播放器
            was_playing = self.is_playing
            if was_playing:
                self.preview_timer.stop()
                
            # 更新预览
            self.update_preview_at_position(value)
            
            # 如果之前在播放，则继续播放
            if was_playing:
                self.current_frame = value
                self.preview_timer.start()

    def on_slider_released(self):
        """当滑块释放时调用"""
        if not self.cap:
            return
            
        # 获取目标帧位置
        frame_pos = self.video_slider.value()
        self.current_frame = frame_pos
        
        # 更新视频位置和预览
        self.update_preview_at_position(frame_pos)
        
        # 如果正在播放，从新位置继续播放
        if self.is_playing:
            self.preview_timer.start()

    def update_preview_at_position(self, frame_pos):
        """在指定位置更新预览画面"""
        try:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.update_time_display()
                # 回退一帧，避免下次读取时跳过这一帧
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                # 更新当前帧位置
                self.current_frame = frame_pos
        except Exception as e:
            self.show_message("错误", f"更新预览失败: {str(e)}", QMessageBox.Icon.Critical)

    def on_range_changed(self, values):
        """当范围滑块值改变时调用"""
        min_value, max_value = values
        if not self.cap:
            return
            
        # 更新时间显示
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        start_time = min_value / fps
        end_time = max_value / fps
        
        # 更新时间编框
        self.start_time.setTime(QTime(0, 0).addSecs(int(start_time)))
        self.end_time.setTime(QTime(0, 0).addSecs(int(end_time)))

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        """显示统一样式的消息框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        
        # 设置样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #2D3748;
                min-width: 300px;
                padding: 12px;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #4299E1;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                min-width: 80px;
                margin: 6px;
            }
            QPushButton:hover {
                background-color: #3182CE;
            }
            QPushButton:pressed {
                background-color: #2B6CB0;
            }
            QMessageBox QFrame {
                background-color: #FFFFFF;
            }
        """)
        
        return msg_box.exec()

    def load_settings(self):
        """加载配置"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                # 恢复保存路径
                if 'save_path' in settings:
                    self.save_path.setText(settings['save_path'])
                    
                # 恢复下载选项
                if 'download_options' in settings:
                    opts = settings['download_options']
                    self.subtitle_check.setChecked(opts.get('subtitle', False))
                    self.thumbnail_check.setChecked(opts.get('thumbnail', False))
                    self.metadata_check.setChecked(opts.get('metadata', False))
                    
        except Exception as e:
            self.append_log(f"加载配置失败: {str(e)}")

    def save_settings(self):
        """保存配置"""
        try:
            settings = {
                'save_path': self.save_path.text(),
                'download_options': {
                    'subtitle': self.subtitle_check.isChecked(),
                    'thumbnail': self.thumbnail_check.isChecked(),
                    'metadata': self.metadata_check.isChecked()
                }
            }
            
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            self.append_log(f"保存配置失: {str(e)}")

    def setup_logging(self):
        """设置日志"""
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(
            log_dir,
            f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
    def append_log(self, message):
        """添加日志"""
        logging.info(message)
        self.append_log_signal.emit(message)

    def setup_preview_controls(self):
        """设置视频预览控件"""
        # 创建预览容器
        preview_container = QWidget()
        preview_container.setFixedSize(960, 540)  # 16:9 比例
        preview_container.setStyleSheet("""
            QWidget {
                background-color: #000000;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
        """)
        preview_container.setMouseTracking(True)
        
        # 创建预览标签
        self.preview_label = QLabel(preview_container)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: none;
                background-color: transparent;
                color: #718096;
            }
        """)
        self.preview_label.setText("请选择视频文件进行预览")
        self.preview_label.setMouseTracking(True)
        
        # 创建悬浮进度条
        self.floating_progress = FloatingProgressBar(preview_container)
        self.floating_progress.hide()  # 初始隐藏
        
        # 设置悬浮进度条的背景和位置
        self.floating_progress.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 4px;
            }
        """)
        
        # 安装事件过滤器到预览容器
        preview_container.installEventFilter(self)
        
        return preview_container

    def create_processor_tab(self):
        """创建视频处理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # 视频选择区域
        video_group = QGroupBox("视频选择")
        video_layout = QHBoxLayout()
        
        self.video_path = QLineEdit()
        self.video_path.setPlaceholderText("选择要处理的视频文件")
        
        browse_video_btn = QPushButton("浏览")
        browse_video_btn.clicked.connect(self.browse_video)
        browse_video_btn.setProperty("cssClass", "secondary-button")
        
        video_layout.addWidget(self.video_path)
        video_layout.addWidget(browse_video_btn)
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)

        # 预设格式选择
        format_group = QGroupBox("输出格式")
        format_layout = QVBoxLayout()
        
        # 创建处理格式选择下拉菜单
        self.process_format_combo = QComboBox()  # 改名以区分用途
        self.process_format_combo.addItems([
            "PPT最佳兼容 (1280x720, MP4)",
            "PPT高清演示 (1920x1080, MP4)",
            "PPT轻量化 (854x480, MP4)",
            "高清视频 (1920x1080)",
            "标清视频 (1280x720)",
            "移动设备 (720x1280)",
            "社交媒体 (1080x1080)",
            "自定义格式"
        ])
        
        # 添加格式说明
        format_tips = QLabel("""
            <p style='margin-bottom: 4px;'><b>PPT格式说明：</b></p>
            <p>• 最佳兼容：平衡大小和质量，适合大多数场景</p>
            <p>• 高清演示：适合大屏幕展示，文字清晰度高</p>
            <p>• 轻量化：适合需要频繁分享的文档</p>
        """)
        format_tips.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                background-color: #F7FAFC;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        format_layout.addWidget(self.process_format_combo)
        format_layout.addWidget(format_tips)
        
        # 编码设置
        encoding_group = QWidget()
        encoding_layout = QGridLayout()
        
        self.codec_combo = QComboBox()
        self.codec_combo.addItems([
            "H.264 (最佳兼容)",
            "H.265/HEVC (更小体积)",
            "VP9 (高压缩比)"
        ])
        
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems([
            "自动 (根据分辨率)",
            "2 Mbps (轻量化)",
            "4 Mbps (标准质量)",
            "8 Mbps (高质量)",
            "自定义比特率"
        ])
        
        encoding_layout.addWidget(QLabel("编码格式:"), 0, 0)
        encoding_layout.addWidget(self.codec_combo, 0, 1)
        encoding_layout.addWidget(QLabel("码率设置:"), 1, 0)
        encoding_layout.addWidget(self.bitrate_combo, 1, 1)
        
        encoding_group.setLayout(encoding_layout)
        format_layout.addWidget(encoding_group)

        # 视频截取控制
        trim_group = QGroupBox("视频截取")
        trim_layout = QVBoxLayout()
        
        # 预览播控制
        preview_controls = QHBoxLayout()
        self.play_btn = QPushButton("播放")
        self.play_btn.setProperty("cssClass", "secondary-button")
        self.play_btn.clicked.connect(self.toggle_preview_playback)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
        preview_controls.addWidget(self.play_btn)
        
        # 时间控制
        time_layout = QHBoxLayout()
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm:ss.zzz")
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm:ss.zzz")
        
        # 添加设置当前时间的按钮
        set_start_btn = QPushButton("设为开始")
        set_start_btn.setProperty("cssClass", "secondary-button")
        set_start_btn.clicked.connect(self.set_current_as_start)
        
        set_end_btn = QPushButton("设为结束")
        set_end_btn.setProperty("cssClass", "secondary-button")
        set_end_btn.clicked.connect(self.set_current_as_end)
        
        self.current_time = QLabel("00:00:00")
        self.duration_label = QLabel("/ 00:00:00")
        
        time_layout.addWidget(QLabel("开始:"))
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(set_start_btn)
        time_layout.addWidget(QLabel("结束:"))
        time_layout.addWidget(self.end_time)
        time_layout.addWidget(set_end_btn)
        time_layout.addStretch()
        time_layout.addWidget(self.current_time)
        time_layout.addWidget(self.duration_label)
        
        # 修改进度滑块部分
        slider_layout = QHBoxLayout()
        slider_container = QWidget()
        slider_container.setMinimumHeight(50)  # 为时间提示留出空间
        
        # 创建滑块
        self.video_slider = QSlider(Qt.Orientation.Horizontal)
        self.video_slider.setTracking(True)  # 改为实时更新
        self.video_slider.valueChanged.connect(self.on_slider_changed)
        self.video_slider.sliderReleased.connect(self.on_slider_released)
        self.video_slider.sliderMoved.connect(self.on_slider_moved)
        
        # 创建时间提示标签
        self.time_tooltip = QLabel(slider_container)
        self.time_tooltip.setStyleSheet("""
            QLabel {
                background-color: #4299E1;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        self.time_tooltip.hide()
        
        slider_layout.addWidget(slider_container)
        slider_container.setLayout(QVBoxLayout())
        slider_container.layout().addWidget(self.video_slider)
        
        trim_layout.addLayout(preview_controls)
        trim_layout.addLayout(time_layout)
        trim_layout.addLayout(slider_layout)
        trim_group.setLayout(trim_layout)
        layout.addWidget(trim_group)

        # 预览区域
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout()

        # 使用setup_preview_controls替换原有的预览容器创建代码
        preview_container = self.setup_preview_controls()
        preview_layout.addWidget(preview_container)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # 控按钮
        button_layout = QHBoxLayout()
        
        # 添加预览帧按钮
        self.prev_frame_btn = QPushButton("上一帧")
        self.prev_frame_btn.setProperty("cssClass", "secondary-button")
        self.prev_frame_btn.clicked.connect(self.prev_frame)
        
        self.next_frame_btn = QPushButton("下一帧")
        self.next_frame_btn.setProperty("cssClass", "secondary-button")
        self.next_frame_btn.clicked.connect(self.next_frame)
        
        self.extract_btn = QPushButton("提取视频片段")
        self.extract_btn.clicked.connect(self.extract_video)
        self.extract_btn.setObjectName("downloadButton")
        
        button_layout.addWidget(self.prev_frame_btn)
        button_layout.addWidget(self.next_frame_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.extract_btn)
        layout.addLayout(button_layout)

        # 初始化预览相关变量
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_frame)
        self.is_playing = False
        self.current_frame = 0
        self.cap = None

        tab.setLayout(layout)
        return tab

    def eventFilter(self, obj, event):
        """事件过滤器，处理鼠标移动事件"""
        if obj == self.preview_label.parent():
            if event.type() == QEvent.Type.Enter:
                # 鼠标进入时显示进度条
                if self.cap:  # 只在有视频时显示
                    self.floating_progress.show()
                    # 设置进度条位置
                    self.floating_progress.setGeometry(
                        0,
                        obj.height() - self.floating_progress.height(),
                        obj.width(),
                        self.floating_progress.height()
                    )
            elif event.type() == QEvent.Type.Leave:
                # 鼠标离开时隐藏进度条
                self.floating_progress.hide()
            elif event.type() == QEvent.Type.MouseMove:
                # 鼠标移动时保持进度条显示
                if self.cap:
                    self.floating_progress.show()
                
        return super().eventFilter(obj, event)

    def prev_frame(self):
        """显示上一帧"""
        if not self.cap:
            return
            
        # 计算上一帧的位置
        self.current_frame = max(0, self.current_frame - 1)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        
        # 读取并显示帧
        ret, frame = self.cap.read()
        if ret:
            self.display_frame(frame)
            self.video_slider.setValue(self.current_frame)
            self.update_time_display()
        else:
            self.show_message("错误", "无法读取上一帧", QMessageBox.Icon.Warning)

    def next_frame(self):
        """显示下一帧"""
        if not self.cap:
            return
            
        # 读取下一帧
        ret, frame = self.cap.read()
        if ret:
            self.current_frame += 1
            self.display_frame(frame)
            self.video_slider.setValue(self.current_frame)
            self.update_time_display()
        else:
            # 如果到达视频末尾，回到当前帧
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            self.show_message("提示", "已到达视频末尾", QMessageBox.Icon.Information)

    def update_time_display(self):
        """更新时间显示"""
        if not self.cap:
            return
            
        # 计算当前时间和总时长
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = self.current_frame / fps
        total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_time = total_frames / fps
        
        # 更新时间标签
        self.current_time.setText(self.format_time(current_time))
        # 修复：使用duration_label替代time_label
        self.duration_label.setText(f"/ {self.format_time(total_time)}")

    def format_time(self, seconds):
        """格式化时间显示，增加毫秒显示"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_int = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds_int:02d}.{milliseconds:03d}"

    def extract_video(self):
        """提取视频片段"""
        if not self.cap:
            self.show_message("错误", "请先选择视频文件", QMessageBox.Icon.Warning)
            return
            
        try:
            # 获取输出格式设置
            format_text = self.process_format_combo.currentText()
            codec = self.codec_combo.currentText()
            bitrate = self.bitrate_combo.currentText()
            
            # PPT专用格式设置
            ppt_formats = {
                "PPT最佳兼容 (1280x720, MP4)": {
                    "size": (1280, 720),
                    "bitrate": "4M",
                    "codec": "h264",  # H.264编码，佳兼容性
                    "preset": "medium",  # 平衡压缩率和速度
                    "crf": 23  # 视觉质量参数，范围0-51，越小质越好
                },
                "PPT高清演示 (1920x1080, MP4)": {
                    "size": (1920, 1080),
                    "bitrate": "8M",
                    "codec": "h264",
                    "preset": "slow",  # 更好的压缩率
                    "crf": 18  # 更高的视觉质量
                },
                "PPT轻量化 (854x480, MP4)": {
                    "size": (854, 480),
                    "bitrate": "2M",
                    "codec": "h264",
                    "preset": "faster",  # 更快的编码速度
                    "crf": 28  # 更高的压缩率
                }
            }
            
            # 其他格式设置
            other_formats = {
                "高清视频 (1920x1080)": {
                    "size": (1920, 1080),
                    "bitrate": "8M",
                    "codec": "h264",
                    "preset": "medium",
                    "crf": 20
                },
                "标清视频 (1280x720)": {
                    "size": (1280, 720),
                    "bitrate": "4M",
                    "codec": "h264",
                    "preset": "medium",
                    "crf": 23
                },
                "移动设备 (720x1280)": {
                    "size": (720, 1280),
                    "bitrate": "3M",
                    "codec": "h264",
                    "preset": "medium",
                    "crf": 25
                },
                "社交媒体 (1080x1080)": {
                    "size": (1080, 1080),
                    "bitrate": "5M",
                    "codec": "h264",
                    "preset": "medium",
                    "crf": 23
                }
            }
            
            # 获取格式设置
            if format_text in ppt_formats:
                format_settings = ppt_formats[format_text]
            elif format_text in other_formats:
                format_settings = other_formats[format_text]
            else:  # 自定义格式
                format_settings = {
                    "size": (self.width_spin.value(), self.height_spin.value()),
                    "bitrate": "4M",
                    "codec": "h264",
                    "preset": "medium",
                    "crf": 23
                }
            
            # 处理编码器选择
            if codec == "H.264 (最佳兼容)":
                format_settings["codec"] = "h264"
            elif codec == "H.265/HEVC (更小体积)":
                format_settings["codec"] = "hevc"
                format_settings["crf"] += 5  # HEVC需要更高的CRF值
            elif codec == "VP9 (高压缩比)":
                format_settings["codec"] = "vp9"
                format_settings["crf"] += 10  # VP9使用不同的质量范围
            
            # 处理码率设置
            if bitrate != "自动 (根分辨率)":
                if bitrate == "2 Mbps (轻量化)":
                    format_settings["bitrate"] = "2M"
                elif bitrate == "4 Mbps (标准质量)":
                    format_settings["bitrate"] = "4M"
                elif bitrate == "8 Mbps (高质量)":
                    format_settings["bitrate"] = "8M"
            
            # 选择保存路径
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存视频片段",
                "",
                "MP4文件 (*.mp4);;所有文件 (*.*)"
            )
            
            if not save_path:
                return
                
            # 构建FFmpeg命令
            input_file = self.video_path.text()
            start_time = self.start_time.time().msecsSinceStartOfDay() / 1000.0
            end_time = self.end_time.time().msecsSinceStartOfDay() / 1000.0
            duration = end_time - start_time
            
            # 基本命令参数
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', input_file,
                '-ss', str(start_time),
                '-t', str(duration)
            ]
            
            # 添加视频编码参数
            if format_settings["codec"] == "h264":
                ffmpeg_cmd.extend([
                    '-c:v', 'libx264',
                    '-preset', format_settings["preset"],
                    '-crf', str(format_settings["crf"])
                ])
            elif format_settings["codec"] == "hevc":
                ffmpeg_cmd.extend([
                    '-c:v', 'libx265',
                    '-preset', format_settings["preset"],
                    '-crf', str(format_settings["crf"])
                ])
            elif format_settings["codec"] == "vp9":
                ffmpeg_cmd.extend([
                    '-c:v', 'libvpx-vp9',
                    '-crf', str(format_settings["crf"]),
                    '-b:v', '0'  # VP9使用CRF模式
                ])
            
            # 添加音频参数
            ffmpeg_cmd.extend([
                '-c:a', 'aac',
                '-b:a', '128k'  # 音频码率
            ])
            
            # 添加其他参数
            ffmpeg_cmd.extend([
                '-vf', f'scale={format_settings["size"][0]}:{format_settings["size"][1]}',
                '-movflags', '+faststart',  # 优化网络播放
                '-y',  # 覆盖输出文件
                save_path
            ])
            
            # 显示进度对话框
            progress = QProgressDialog("正在处理视频...", "取消", 0, 100, self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setStyleSheet("""
                QProgressDialog {
                    background-color: #FFFFFF;
                }
                QProgressDialog QLabel {
                    color: #2D3748;
                    padding: 10px;
                }
                QProgressBar {
                    border: none;
                    background-color: #EDF2F7;
                    height: 8px;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background-color: #4299E1;
                    border-radius: 4px;
                }
                QPushButton {
                    background-color: #4299E1;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 16px;
                    min-width: 80px;
                }
            """)
            
            try:
                # 执行FFmpeg命令
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # 监控进度
                while True:
                    if progress.wasCanceled():
                        process.terminate()
                        break
                        
                    return_code = process.poll()
                    if return_code is not None:
                        break
                    
                    # 更新进度这里可以添加进度解析）
                    QApplication.processEvents()
                
                if return_code == 0 and not progress.wasCanceled():
                    self.show_message("完成", "视频片段提取完成！")
                elif progress.wasCanceled():
                    self.show_message("提示", "操作已取消", QMessageBox.Icon.Information)
                else:
                    self.show_message("错误", "视频处理失败", QMessageBox.Icon.Critical)
                
            except Exception as e:
                self.show_message("错误", f"处理过程出错: {str(e)}", QMessageBox.Icon.Critical)
                
        except Exception as e:
            self.show_message("错误", f"视频处理失败: {str(e)}", QMessageBox.Icon.Critical)

    def update_preview(self, frame=None):
        """update_frame 的别名，用于向后兼容"""
        return self.update_frame()

    def set_current_as_start(self):
        """设置当前时间为开始时间"""
        if not self.cap:
            return
            
        current_frame = self.video_slider.value()
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = current_frame / fps
        
        # 检查是否超过结束时间
        end_time = self.end_time.time().msecsSinceStartOfDay() / 1000.0
        if current_time >= end_time:
            self.show_message("警告", "开始时间不能晚于结束时间", QMessageBox.Icon.Warning)
            return
            
        # 设置开始时间
        self.start_time.setTime(QTime(0, 0).addMSecs(int(current_time * 1000)))

    def set_current_as_end(self):
        """设置当前时间为结束时间"""
        if not self.cap:
            return
            
        current_frame = self.video_slider.value()
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = current_frame / fps
        
        # 检查是否早于开始时间
        start_time = self.start_time.time().msecsSinceStartOfDay() / 1000.0
        if current_time <= start_time:
            self.show_message("警告", "结束时间不能早于开始时间", QMessageBox.Icon.Warning)
            return
            
        # 设置结束时间
        self.end_time.setTime(QTime(0, 0).addMSecs(int(current_time * 1000)))

    def on_start_time_changed(self, time):
        """开始时间变化处理"""
        if not self.cap:
            return
            
        start_time = time.msecsSinceStartOfDay() / 1000.0
        end_time = self.end_time.time().msecsSinceStartOfDay() / 1000.0
        
        if start_time >= end_time:
            # 恢复到上一个有效值
            self.start_time.setTime(self.last_valid_start_time)
            self.show_message("警告", "开始时间不能晚于结束时间", QMessageBox.Icon.Warning)
        else:
            self.last_valid_start_time = time

    def on_end_time_changed(self, time):
        """结束时间变化处理"""
        if not self.cap:
            return
            
        start_time = self.start_time.time().msecsSinceStartOfDay() / 1000.0
        end_time = time.msecsSinceStartOfDay() / 1000.0
        
        if end_time <= start_time:
            # 恢复到上一个有值
            self.end_time.setTime(self.last_valid_end_time)
            self.show_message("警告", "结束时间不能早于开始时间", QMessageBox.Icon.Warning)
        else:
            self.last_valid_end_time = time

    def on_slider_moved(self, value):
        """滑块移动时的处理"""
        if not self.cap:
            return
            
        # 显示时间提示
        self.show_time_tooltip(value)
        
        # 更新预览画面
        self.update_preview_at_position(value)

    def show_time_tooltip(self, pos):
        """显示时间提示"""
        if not self.cap:
            return
            
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = pos / fps
        time_str = self.format_time(current_time)
        
        # 更新提示标签
        self.time_tooltip.setText(time_str)
        
        # 计算提示位置
        slider = self.video_slider
        width = slider.width()
        x = int((pos - slider.minimum()) * width / (slider.maximum() - slider.minimum()))
        
        # 确保提示不会超出范围
        tooltip_width = self.time_tooltip.sizeHint().width()
        x = max(0, min(x - tooltip_width // 2, width - tooltip_width))
        
        # 设置位置并显示
        self.time_tooltip.move(slider.mapToParent(QPoint(x, 0)).x(), slider.y() - 25)
        self.time_tooltip.show()

    def on_floating_progress_changed(self, value):
        """处理悬浮进度条值变化"""
        if not self.cap:
            return
            
        # 更新视频位置
        self.update_preview_at_position(value)
        
        # 更新时间显示
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_time = value / fps
        self.floating_progress.setCurrentTime(self.format_time(current_time))

    def on_download_format_changed(self, index):
        """下载格式选择变化处理"""
        try:
            if index < 0 or self.download_format_combo.count() == 0:
                return
            
            current_data = self.download_format_combo.currentData()
            current_text = self.download_format_combo.currentText()
            
            # 忽略分隔线和无效选项
            if not current_data or current_text.startswith("-----") or current_text == "未找到可用格式":
                self.download_button.setEnabled(False)
                return
            
            # 记录日志
            self.log_text.append(f"选择格式: {current_text} (ID: {current_data})")
            
            # 更新下载选项
            self.update_download_options(current_data)
            
            # 启用下载按钮
            self.download_button.setEnabled(True)
            
        except Exception as e:
            self.log_text.append(f"切换格式失败: {str(e)}")
            self.show_message("错误", f"切换格式失败: {str(e)}", QMessageBox.Icon.Warning)
            self.download_button.setEnabled(False)

    def update_download_options(self, format_id):
        """更新下载选项"""
        try:
            if not format_id:
                return
            
            # 根据格式ID更新下载选项
            is_video = not format_id.startswith('ba/')
            
            # 更新UI状态
            self.thumbnail_check.setEnabled(is_video)
            if not is_video:
                self.thumbnail_check.setChecked(False)
            
            # 启用下载按钮
            self.download_button.setEnabled(True)
            
            # 记录日志
            self.log_text.append(f"更新下载选项: {'视频' if is_video else '音频'} 格式")
            
        except Exception as e:
            self.log_text.append(f"更新下载选项失败: {str(e)}")

# 添加新的悬浮进度条控件类
class FloatingProgressBar(QWidget):
    """视频预览区域的悬浮进度条"""
    valueChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        
        # 设置固定高度
        self.setFixedHeight(40)
        
        # 创建进度条
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: rgba(255, 255, 255, 0.2);
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #4299E1;
                border: 2px solid #4299E1;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: #3182CE;
                border-color: #3182CE;
            }
            QSlider::sub-page:horizontal {
                background: #4299E1;
            }
        """)
        
        # 创建时间标签
        self.current_time = QLabel("00:00:00")
        self.total_time = QLabel("00:00:00")
        for label in [self.current_time, self.total_time]:
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    background: transparent;
                }
            """)
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.addWidget(self.current_time)
        layout.addWidget(self.slider, 1)  # 1表示拉伸因子
        layout.addWidget(self.total_time)
        
        # 连接信号
        self.slider.valueChanged.connect(self.valueChanged.emit)
        
        # 设背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def setRange(self, minimum, maximum):
        self.slider.setRange(minimum, maximum)
        
    def setValue(self, value):
        self.slider.setValue(value)
        
    def value(self):
        return self.slider.value()
        
    def setCurrentTime(self, time_str):
        self.current_time.setText(time_str)
        
    def setTotalTime(self, time_str):
        self.total_time.setText(time_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernVideoDownloaderGUI()
    window.show()
    sys.exit(app.exec()) 