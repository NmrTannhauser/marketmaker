import requests, json
import threading
import time

def start(request, interval):
    thread = RepeatedTimer(interval, prices)

class RepeatedTimer(object):
  def __init__(self, interval, function, *args):
    self._timer = None
    self.interval = interval
    self.function = function
    self.is_running = False
    self.next_call = time.time()
  def _run(self):
    self.is_running = False
    self.start()
    self.function()
  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True
  def stop(self):
    self._timer.cancel()
    self.is_running = False


def prices():
    SCOPES = "https://www.googleapis.com/auth/spreadsheets.readonly"
    store = file.Storage("/home/projects/market/credentials.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("/home/projects/market/client_secret.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("sheets", "v4", http=creds.authorize(Http()))
    # Call the Sheets API
    SPREADSHEET_ID = "15RUQce2liQe5ojMzgynm8ghs3E7fwwkf5gm3mMyGV_8"
    RANGE_NAME = "Portfolio!C6:Q6"
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get("values", [])
    return values


def getData():
    res = requests.get('http://127.0.0.1:8000/json/').text
    res = res.replace('&#39;','"')
    return json.loads(res)

interval = 0
interval2 = 0
mainfun = None

def updaterobot():
    data = getData()
    mainfun.interval = data[0]['TimePrice']


try:
    res = requests.get('http://127.0.0.1:8000/json/').text
    res = res.replace('&#39;','"')
    res = json.loads(res)
    interval = res[0]['TimePrice']
    print(interval)
    mainfun = RepeatedTimer(interval, updaterobot)
    mainfun._run()
    print(mainfun)
except Exception as e:
    print(e)
