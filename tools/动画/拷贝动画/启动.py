import importlib, sys, os

# 动态获取启动脚本所在目录，无论放在哪里都能正确找到工具
_path = os.path.dirname(os.path.abspath(__file__))
if _path not in sys.path:
    sys.path.insert(0, _path)

import importlib
import 关键帧跟随 as KeyFollow
importlib.reload(KeyFollow)
