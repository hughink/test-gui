
"""
Configuration settings for the application
"""

# UI Settings
WINDOW_TITLE = "Nuclei Tools"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 840
ROWS_PER_PAGE = 50

# File Settings
YAML_FILE_EXTENSION = '.yaml'
TARGETS_FILENAME = 'targets.txt'

# Style Settings
TABLE_STYLE = """
    QTableWidget {
        background-color: #F3F3F3;
        alternate-background-color: #E8E8E8;
        color: #2D2D2D;
    }
    QTableWidget::item {
        border-bottom: 1px solid #D7D7D7;
    }
    QTableWidget::item:selected {
        background-color: #F0A30A;
        color: #FFFFFF;
    }
    QHeaderView::section {
        background-color: #9E9E9E;
        color: #2F2F2F;
        padding-left: 4px;
        border: 1px solid #BFBFBF;
        height: 25px;
    }
"""

EDITOR_STYLE = """
    QPlainTextEdit {
        background-color: #272822;
        color: #F8F8F2;
        font-family: 'Courier New';
        font-size: 12pt;
    }
"""

# Column Settings
TABLE_HEADERS = [
    '序号',
    '文件名',
    '危害',
    '作者',
    'tags',
    'CVE编号',
    '参考链接',
    '漏洞描述'
]

COLUMN_WIDTHS = [40, 255, 60, 100, 160, 106, 310, None]  # None for auto-width
