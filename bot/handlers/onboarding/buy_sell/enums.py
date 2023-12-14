from enum import Enum as pyEnum


class BuySellConversationSteps(pyEnum):
    GET_SUBCATEGORY = 1
    GET_CAR_REGISTRATION_NUMBER_OR_VIN = 2
    GET_CAR_BRAND_AND_MODEL = 3
    GET_CAR_MILEAGE = 4
    GET_CLIENT_PHONE = 5
