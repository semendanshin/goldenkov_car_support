from enum import Enum as pyEnum


class InsuranceConversationSteps(pyEnum):
    GET_SUBCATEGORY = 'get_subcategory'
    GET_REGISTRATION_NUMBER_OR_VIN = 'get_registration_number_or_vin'
    GET_PHONE_NUMBER = 'get_phone_number'
