from enum import Enum
token = '494981490:AAFuUz4jP44tq0ff5R0DVuFl7dchU6qBlrw'
db_file = "database.vdb"
db_msisdn = "msisdn.vdb"
db_Tokens = "token.vdb"

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_TEL = "1" #Ввод номера
    S_ENTER_PAS = "2" #Ввод пароля
    S_PROFILE = "3" #Что хотите в профиле
    S_ACCINFO = "4" #информация об аккаунт
    S_PAYMENTS = "5"
    S_CHANGEINFO_ENTERNAME = "6"
    S_TAXES = "7"
    S_MY_TAX = "8"
    S_CHANGE_TAX = "9"
    S_SERVICES = "10"
    S_MY_SERVICES = "11"
    S_OFF_SERVICE = "12"
    S_CHANGEINFO_ENTERKEY = "13"
    S_CHANGEINFO_ENTERMIDNAME = "14"
    S_CHANGEINFO_ENTERLASTNAME = "15"
    S_CHANGEINFO_ENTERMAIL = "16"