import requests
import time
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = "BDLvr9XfeD7cyV1N9WTNV8KXoXyejrFu0MiDVYdDiJ8YTF91Puu1qM0BOp72mkF5MfY5U4FdJug6EVd9qhSbEA"
SECRETKEY = "2m6BVgy91RrhUR82qB9UsUQ3RhfjptpkJWkqULEuM0L8IQNljtSZM1qDZEJb5IH9sTYMcnDBCqR9IdPLBFBg"


class APIClass:
    def __init__(
        self,
        payload,
        path,
        method,
        paramsMap,
    ):
        self.payload = payload
        self.path = path
        self.method = method
        self.paramsMap = paramsMap

    def update_parameters(
        self,
        payload,
        path,
        method,
        paramsMap,
    ):
        self.payload = payload
        self.path = path
        self.method = method
        self.paramsMap = paramsMap

    def get_request(self):
        paramsStr = self.parseParam(self.paramsMap)
        return self.send_request(self.method, self.path, paramsStr, self.payload)

    def get_sign(self, api_secret, payload):
        signature = hmac.new(
            api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256
        ).hexdigest()
        print("sign=" + signature)
        return signature

    def send_request(self, method, path, urlpa, payload):
        url = "%s%s?%s&signature=%s" % (
            APIURL,
            path,
            urlpa,
            self.get_sign(SECRETKEY, urlpa),
        )
        print(url)
        headers = {
            "X-BX-APIKEY": APIKEY,
        }
        response = requests.request(method, url, headers=headers, data=payload)
        return response.text

    def parseParam(self, paramsMap):
        sortedKeys = sorted(paramsMap)
        paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
        if paramsStr != "":
            return paramsStr + "&timestamp=" + str(int(time.time() * 1000))
        else:
            return paramsStr + "timestamp=" + str(int(time.time() * 1000))


api = APIClass(
    {},
    "/v1/spot/orders",  # No puedo ejecutar la api si no tengo la apikey
    "POST",
    {
        "symbol": "BTC/USDT",
        "side": "BUY",  # usa esto para comprar y la otra para vender
        "type": "LIMIT",
        "price": "40000",
        "quantity": "1",
    },
)
api.get_request()

# Parametros a ingresar en la clase al hacer un pedido
# symbol: El símbolo del par comercial (por ejemplo, "BTC/USDT").
# side: La dirección de la orden ("BUY" para comprar o "SELL" para vender).
# type: El tipo de orden ("LIMIT" para una orden límite o "MARKET" para una orden de mercado).
# price: El precio límite para una orden límite (opcional para una orden de mercado).
# quantity: La cantidad de la orden.

# Usa la funcion update_parameters para ingresar los nuevos parametros antes de vender o comprar
# Y luego usa la funcion api.get_request para llamar a la api
