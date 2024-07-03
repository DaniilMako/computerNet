import csv  # встроенные

from pythonping import ping  # скачанные

domains = ['google.com', 'yahoo.com', 'bing.com', 'yandex.com', 'vk.com', 'yandex.com', 'wikipedia.org',
           'stackoverflow.com', 'github.com', 'youtube.com']

with open('domains.csv', 'w', newline='') as csvfile:
    row = csv.writer(csvfile, quotechar=";", delimiter=";")
    row.writerow(["domain name", "ip", "min time", "avg time", "max time"])
    for domain in domains:
        result = ping(domain)
        row.writerow([domain, result._responses[0].message.source, round(result.rtt_min * 1000, 2),
                      round(result.rtt_avg * 1000, 2), round(result.rtt_max * 1000, 2)])
