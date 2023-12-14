from enum import Enum as pyEnum


class ServiceConversationSteps(pyEnum):
    GET_SUBCATEGORY = 'get_subcategory'
    GET_MILEAGE = 'get_mileage'
    GET_REGISTRATION_NUMBER_OR_VIN = 'get_registration_number_or_vin'
    GET_PROBLEM_DESCRIPTION = 'get_problem_description'
    GET_PHONE_NUMBER = 'get_phone_number'
