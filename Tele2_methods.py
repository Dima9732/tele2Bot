import requests
import json

class Tele2_methods:
    def get_list_services():
        r = requests.get('http://tele2-hackday-2017.herokuapp.com/api/services/available')
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def description_id(slug):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/services/'
        tmp += slug
        r = requests.get(tmp)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        elif r.status_code == 404:
            print("Услуга не найдена")
        elif r.status_code == 400:
            print("Задан неправильный параметр")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def activate_service(msisdn, api_token, slug):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/subscribers/'
        tmp += msisdn + '/services/' + slug
        headers = {'accept': 'application/json', 'X-API-Token': api_token}
        r = requests.put(tmp, headers = headers)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
            return False
        elif r.status_code == 404:
            print("Услуга не найдена")
            return False
        elif r.status_code == 400:
            print("Заданы неправильные параметры")
            print(r.json())
            return False
        else:
            return True
    def del_servesis(msisdn, pas, slug):
        url = "http://tele2-hackday-2017.herokuapp.com/api/subscribers/" + msisdn + "/services/" + slug
        payload = {'some':'data'}
        headers = {'accept': 'application/json', 'X-API-Token' : pas}
        r = requests.delete(url, data=json.dumps(payload),headers=headers)
        return r.json()["data"]
    def payment(msisdn, api_token, from_t, to_t):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/subscribers/'
        tmp += msisdn + '/payments'
        payload = {'from': from_t, 'to': to_t}
        headers = {'accept': 'application/json', 'X-API-Token': api_token}
        r = requests.get(tmp, params = payload, headers = headers)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        elif r.status_code == 404:
            print("Услуга не найдена")
        elif r.status_code == 400:
            print("Задан неправильный параметр")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def inform_about_sub(msisdn):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/subscribers/'
        tmp += msisdn
        headers = {'accept': 'application/json'}
        r = requests.get(tmp, headers = headers)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        elif r.status_code == 404:
            print("Услуга не найдена")
        elif r.status_code == 400:
            print("Задан неправильный параметр")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def changeAbonentInfo(msisdn, token, changes):
        url = "http://tele2-hackday-2017.herokuapp.com/api/subscribers/" + msisdn
        payload = changes
        headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': token}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
            return False
        elif r.status_code == 404:
            print("Услуга не найдена")
            return False
        elif r.status_code == 400:
            print("Задан неправильный параметр")
            return False
        else:
            return True
    def balance(msisdn, api_token):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/subscribers/'
        tmp += msisdn + '/balance'
        headers = {'accept': 'application/json', 'X-API-Token': api_token}
        r = requests.get(tmp, headers = headers)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        elif r.status_code == 404:
            print("Услуга не найдена")
        elif r.status_code == 400:
            print("Задан неправильный параметр")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def tariff(msisdn, api_token):
        tmp = 'http://tele2-hackday-2017.herokuapp.com/api/subscribers/'
        tmp += msisdn + '/tariff'
        headers = {'accept': 'application/json', 'X-API-Token': api_token}
        r = requests.get(tmp, headers = headers)
        ans = dict()
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
        elif r.status_code == 404:
            print("Услуга не найдена")
        elif r.status_code == 400:
            print("Задан неправильный параметр")
        else:
            pars = json.loads(r.text)
            ans = pars['data']
        return ans
    def changeTariff(msisdn, token, newTariff):
        url = "http://tele2-hackday-2017.herokuapp.com/api/subscribers/"+msisdn+"/tariff"
        payload = {'tariffSlug':newTariff}
        headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': token}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 500:
            print("Ошибка сервера, попробуйте позднее")
            return False
        elif r.status_code == 404:
            print("Услуга не найдена")
            return False
        elif r.status_code == 400:
            print("Задан неправильный параметр")
            return False
        else:
            return True
    def getServices(msisdn, pas):
        url = "http://tele2-hackday-2017.herokuapp.com/api/subscribers/" + msisdn +"/services"
        payload = {'some':'data'}
        headers = {'accept': 'application/json', 'X-API-Token' : pas}
        r = requests.get(url, data=json.dumps(payload),headers=headers)
        return r.json()["data"]
    def getCharges(msisdn, token, from1, to):
        url = "http://tele2-hackday-2017.herokuapp.com/api/subscribers/"+msisdn+"/charges" # вставляешь в строку что надо
        payload = {'from': from1, 'to': to} # тут параметры из URL после
        headers = {'accept': 'application/json', 'X-API-Token': token} # тут после application твои параметры
        r = requests.get(url, params=payload, headers=headers)
        print(r.url)
        return r.json()["data"]
    def getTariffById(slug):
        url = "http://tele2-hackday-2017.herokuapp.com/api/tariffs/" + slug
        payload = {'some': 'data'}
        headers = {'accept': 'application/json'}
        r = requests.get(url, data=json.dumps(payload), headers=headers)
        return r.json()["data"]
    def getTariffs():
        url = "http://tele2-hackday-2017.herokuapp.com/api/tariffs/available"
        payload = {'some': 'data'}
        headers = {'accept': 'application/json'}
        r = requests.get(url, data=json.dumps(payload), headers=headers)
        return r.json()["data"]
