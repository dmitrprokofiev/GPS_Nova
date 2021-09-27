import requests

myurl = "https://s4.geotek.online/api"

accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjcyOSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiJnYXNvbGluZSIsInN1YnVzZXIiOiIxIiwiQ3VsdHVyZSI6InN0cmluZyIsIm5iZiI6MTYzMTAyMTYxNSwiZXhwIjoxNjMxMDIzNDE1LCJpc3MiOiJHZW9UZWsiLCJhdWQiOiJHZW9UZWtBUEkifQ.ipKyiETXtbMujRKkJ-39OOPVwAHjLzTh-SdCYQoeuMc"

head = {'Authorization' : f'Bearer {accessToken}'}

p = "/ObjectsHistory/DriverSessions"

s = "/Profile"

param = {
  "from": 0,
  "till": 0,
  "objectID": 3338
}

response = requests.get(url=myurl+p, headers=head)

print(requests.get(url=myurl+s, headers=head))

print(requests.post(url=myurl+p, headers=head, json=param))