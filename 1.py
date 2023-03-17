import requests

url = "https://akabab.github.io/superhero-api/api/all.json"
resp = requests.get(url)
res_json = resp.json()
heroes_names_for_search = ["Hulk", "Captain America", "Thanos"]
compare_list = {}

for item in res_json:
    if item['name'] in heroes_names_for_search:
        compare_list[item['name']] = item['powerstats']['intelligence']

print(max(compare_list))
