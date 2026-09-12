# Application/Move/MoveBuilders/MoveModuleBuilder.py
from Application.Common.Dispatcher import Dispatcher
from Application.Move.MoveHandler import MoveHandler
from Application.Move.MoveRequest import MoveRequest
from Application.Move.MoveResult import MoveResult
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Presentation.CLI.Request.RequestCreator.MoveRequestCreator import MoveRequestCreator
from Presentation.CLI.Formatters.MoveResultFormatter import MoveResultFormatter

class MoveModuleBuilder:
    """Assembling the transport unit (Move) and registering it in the application"""
    
    def build(self, dispatcher: Dispatcher, request_factory: RequestFactory, formatters: dict):
        # 1. إنشاء المعالج
        handler = MoveHandler()
        
        # 2. تسجيل الطلب مع المعالج في الـ Dispatcher
        dispatcher.register(MoveRequest, handler)
        
        # 3. تسجيل اسم الأمر "move" مع الـ Creator في الـ Factory
        request_factory.register("move", MoveRequestCreator())
        
        # 4. تسجيل النتيجة مع الـ Formatter
        formatters[MoveResult] = MoveResultFormatter()