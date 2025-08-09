import requests
import datetime
import time

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

def print_header(file):
    file.write("""<!DOCTYPE html>
<html lang="pl-PL" class="fontEnlarge-0">
<head> <meta charset="utf-8"> </head>
<body class="print">
<main>
<div class="word_content_wrapper">
<div class="print_wrapper">
<div class="word_content">
""")

def print_footer(file):
    file.write("</div> </div> </main> </body> </html>")

allowed_sections = {
    '<h3>Odmiana</h3>',
    '<h2 class="podhaslo">',
    '<h3>Kwalifikacja&nbsp;tematyczna</h3>'
}

stoppers = {
    '<div class="sekcja_container">',
    '<div class="copyright">Copyright&copy; Instytut Języka Polskiego PAN</div>'
}

def handle_container(file, lines, j):
    printing_on = lines[j + 4] in allowed_sections
    if printing_on:
        file.write(lines[j] + "\n")
    j += 1

    while j < len(lines) and lines[j] not in stoppers:
        if printing_on:
            file.write(lines[j] + "\n")
        j += 1

    return j

i_0 = 37711 # 116699
i_max = 37712 # 116699 * 2

def m(i):
    p = "{0:0.2f}".format(i / i_max * 100) + "%"
    print(f"{i} START {datetime.datetime.now().time()} {p}")
    
    url = f'http://wsjp.pl/haslo/do_druku/{i}'
    response = requests.get(url, headers=user_agent, timeout=5)

    print(f"{i} END   {datetime.datetime.now().time()} {'OK' if response.ok else ('NOT_OK ' + str(response.status_code))}")
    print()
    
    if response.ok:
        lines = [line.strip() for line in response.text.split('\n') if len(line.strip()) > 0]

        with open(f"{i}.html", "w") as file:
            print_header(file)
            
            j = 0
            while lines[j] != '<div id="haslo_forma">':
                j += 1
            
            while lines[j] != '<div class="sekcja_container">':
                file.write(lines[j] + "\n")
                j += 1
            
            while j < len(lines) and lines[j] == '<div class="sekcja_container">':
                j = handle_container(file, lines, j)
            
            print_footer(file)
    elif response.status_code == 401:
        p = " - hasło w trakcie opracowania"
        s = response.text.find(p)
        word = response.text[:s].split('\n')[-1].strip()
            
        with open("ERROR 401 (hasło w trakcie opracowania).txt", "a") as file:
            file.write(f"{i} {word}\n")

for i in range(i_0, i_max):
    # sleep_dur = 1
    while True:
        try:
            m(i)
        except:
            print(f"{i} ERROR {datetime.datetime.now().time()}")
            # time.sleep(sleep_dur)
            # sleep_dur += 5
        else:
            break
