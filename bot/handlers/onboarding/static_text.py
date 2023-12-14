from .enums import ConversationStepsEnum


GREETING = "Привет, я виртуальный помощник Recar. Меня придумали для того, "\
           "что бы облегчить тебе жизнь и помочь с решением любого вопроса по автомобилю.\n\nЧем могу помочь?"

TEXTS = {
    ConversationStepsEnum.CHOOSE_CAR_REGISTRATION_NUMBER: "Пожалуйста, введите гос. номер автомобиля (слитно, используя кириллицу):",
    ConversationStepsEnum.CHOOSE_CAR_MILEAGE: "Пожалуйста, введите пробег автомобиля (в км):",
    ConversationStepsEnum.ADD_REPAIR_DESCRIPTION: "Пожалуйста, опишите проблему:",
    ConversationStepsEnum.ADD_CLIENT_PHONE_NUMBER: "Пожалуйста, введите номер телефона или отправьте ваш контакт, чтобы консультант мог с вами связаться:",
}