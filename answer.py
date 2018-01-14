
import re
import urllib.request
import urllib.parse
import urllib.error


def answer(question_key_words, options_key_words):

    params = ' '.join(question_key_words)
    url = "http://www.baidu.com/s?wd=" + urllib.parse.quote(params)
    contents = list()
    with urllib.request.urlopen(url) as response:
        html = response.read()
    content = html.decode('utf-8')
    content = content.replace('\n', '').replace('\r', '')
    contents.append(content)

    option_count = [0]*len(options_key_words)
    for i in range(len(options_key_words)):
        for w in options_key_words[i]:
            option_count[i] += content.count(w)

    for i in range(len(options_key_words)):
        print(' '.join(options_key_words[i]) + ': ' + str(option_count[i]))
    print('')

    href_regex = r'<h3.*?>.*?href\s*=\s*"(.*?)".*</h3>'
    h3_regex = r'<h3.*?/h3>'

    search_res = list()
    matches = re.findall(h3_regex, content)
    for m in matches:
        href = re.findall(href_regex, m)
        search_res.extend(href)

    search_res = search_res[:2]

    for url in search_res:
        try:
            with urllib.request.urlopen(url) as response:
                char_set = (response.headers.get_content_charset())
                if not char_set:
                    char_set = 'utf-8'
                try:
                    content = response.read().decode(char_set)
                except UnicodeDecodeError:
                    content = response.read().decode('gbk')
            contents.append(content)

            for i in range(len(options_key_words)):
                for w in options_key_words[i]:
                    option_count[i] += content.count(w)

            for i in range(len(options_key_words)):
                print(' '.join(options_key_words[i]) + ': ' + str(option_count[i]))
            print('')


        except urllib.error.HTTPError:
            continue

    for option in options_key_words:
        appearance = 0
        for content in contents:
            for w in option:
                appearance += content.count(w)
        print(' '.join(option) + ':' + str(appearance))

