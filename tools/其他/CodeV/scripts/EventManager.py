from maya.OpenMaya import MEventMessage

class EventManager:
    _instance = None
    
    # 预定义的常用 Maya 事件映射表
    # 如果用户注册这些 key，程序会自动去绑定对应的 Maya Native Event
    MAYA_EVENT_MAP = {
        "SelectionChanged": "SelectionChanged",
        "SceneOpened": "SceneOpened",
        "SceneImported": "SceneImported",
        "NewSceneOpened": "NewSceneOpened",
        "timeChanged": "timeChanged"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        """仅在单例创建时初始化一次数据结构"""
        self._observers = {}
        self._maya_callbacks = {}
        print("[EventManager] 核心管理器已就绪")

    def __init__(self):
        """
        注意：在单例模式中，__init__ 每次调用 EventManager() 都会执行。
        所以这里不要写 self._observers = {}，否则会清空已有的数据。
        """
        pass

    def register_observer(self, event_type, callback):
        """
        注册观察者，并自动判断是否需要映射 Maya 事件。
        """
        if event_type not in self._observers:
            self._observers[event_type] = []
        
        if callback not in self._observers[event_type]:
            self._observers[event_type].append(callback)
            print(f"[EventManager] 注册观察者: {callback.__name__} -> {event_type}")

            # --- 自动映射逻辑 ---
            # 如果 event_type 在映射表中，且还没注册过 Maya 回调，则自动注册
            if event_type in self.MAYA_EVENT_MAP:
                if event_type not in self._maya_callbacks:
                    maya_native_name = self.MAYA_EVENT_MAP[event_type]
                    self.register_maya_event(event_type, maya_native_name)

    def register_maya_event(self, event_type, maya_event_name):
        """公开方法：手动或自动注册 Maya 事件监听"""
        if event_type in self._maya_callbacks:
            return

        def callback_wrapper(*args):
            # 这里的 *args 接收来自 Maya 的参数（通常是 clientData）
            self._on_maya_event_triggered(event_type)

        try:
            cb_id = MEventMessage.addEventCallback(maya_event_name, callback_wrapper)
            self._maya_callbacks[event_type] = cb_id
            print(f"[EventManager] 自动映射 Maya 事件成功: {maya_event_name}")
        except Exception as e:
            print(f"[EventManager] 映射 Maya 事件失败 [{maya_event_name}]: {e}")

    def _on_maya_event_triggered(self, event_type):
        """内部通知逻辑"""
        if event_type in self._observers:
            # 复制一份列表进行迭代，防止回调函数内部修改观察者列表导致报错
            for callback in self._observers[event_type][:]:
                try:
                    callback()
                except Exception as e:
                    print(f"[EventManager] 回调执行异常: {e}")

    def unregister_observer(self, event_type, callback):
        """注销观察者，并根据需要清理底层 Maya 监听"""
        if event_type in self._observers and callback in self._observers[event_type]:
            self._observers[event_type].remove(callback)
            
            # 如果没有观察者了，释放 Maya 资源
            if not self._observers[event_type]:
                self._cleanup_maya_event(event_type)

    def _cleanup_maya_event(self, event_type):
        """释放 Maya 回调资源"""
        if event_type in self._maya_callbacks:
            MEventMessage.removeCallback(self._maya_callbacks[event_type])
            del self._maya_callbacks[event_type]
            print(f"[EventManager] 已释放不再需要的 Maya 监听: {event_type}")

    def unregister_all_for_client(self, callback_list):
        """
        清理一组特定的回调函数
        :param callback_list: 比如 [self.on_selection_changed, self.on_scene_save]
        """
        for event_type in list(self._observers.keys()):
            for cb in callback_list:
                self.unregister_observer(event_type, cb)
                
    def unregister_all_observers(self):
        """强制清理所有映射和观察者"""
        for event_type in list(self._maya_callbacks.keys()):
            self._cleanup_maya_event(event_type)
        self._observers.clear()