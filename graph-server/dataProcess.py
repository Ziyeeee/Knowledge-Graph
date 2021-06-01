import json, re
from bs4 import BeautifulSoup as bs


def md2json(mdName, jsonName):
    graphData = []
    text2deep = {
        '#': 0,
        '##': 1,
        '###': 2,
        '-': 3,
        '\t-': 4,
        '\t\t-': 5,
        '\t\t\t-': 6,
        '\t\t\t\t-': 7,
        '\t\t\t\t\t-': 8
    }
    text2groupId = {
        '任务': 0,
        '方法': 1,
        '步骤': 2,
        '属性': 3,
        '概念': 4
    }

    with open('./templates/' + mdName, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    index = 0
    for line in lines:
        if len(line) > 2:
            # print('------------------------------------------------------------------------')
            # print(line)
            line = line.replace('\n', '')
            line = re.split('[ ：\n]', line)
            try:
                line[0] = text2deep[line[0]]
                line.append('')
                line.append(index)
                graphData.append(line)
                index += 1
            except KeyError:
                line = ''.join(line)
                try:
                    line = line[line.index('<') + 1:line.index('>')]
                    # print(line)
                    graphData[-1][-2] = line
                except ValueError:
                    pass
            # print(line)
            if len(line) != 4:
                # print(line)
                pass

    print(graphData)

    dfs = [graphData[0]]
    curDeep = graphData[0][0]
    nodes = [{'index': graphData[0][-1], 'label': graphData[0][2], 'reference': graphData[0][3],
              'groupId': text2groupId[graphData[0][1]]}]
    links = []
    for data in graphData[1:]:
        nodes.append({'index': data[-1], 'label': data[2], 'reference': data[3], 'groupId': text2groupId[data[1]]})
        if data[0] <= curDeep:
            while dfs.pop()[0] > data[0]:
                continue
        curDeep = data[0]
        links.append({'source': dfs[-1][-1], 'target': data[-1]})
        dfs.append(data)

    with open('./templates/' + jsonName, 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f)


def matchSpans(soup, content):
    p_s = soup.find_all('p', class_=['MsoNormal', 'MsoListParagraph', 'MsoFootnoteText'])
    match_span_s = []
    i = 0
    for p in p_s:
        span_s = p.find_all('span')
        for span in span_s:
            str_s = span.strings
            for string in str_s:
                j = 0
                # string = string.replace('：', '')
                while j < len(string):
                    if i < len(content):
                        if string[j] == content[i] or not isChinese(content[i]):
                            if span not in match_span_s:
                                match_span_s.append(span)
                            i = i + 1
                            j = j + 1
                        elif string[j] == '：':
                            j = j + 1
                        else:
                            match_span_s = []
                            j = j + 1
                    else:
                        return list(set(match_span_s))



    return list(set(match_span_s))


def isChinese(char):
    if u'\u4e00' <= char <= u'\u9fff':
        return True
    else:
        return False


# md2json('graph.md', 'data.json')

soup = bs(open('chap18.html'), features='html.parser')
with open('./templates/data.json', 'r') as f:
    data = json.load(f)
nodes = data['nodes']
for node in nodes:
    if len(node['reference']) > 0:
        spans = matchSpans(soup, node['reference'])
        # if len(spans) == 0:
        #     print(node['reference'])

        for span in spans:
            try:
                span['class'] += ' node' + str(node['index'])
            except KeyError:
                span['class'] = 'node' + str(node['index'])
            # print(span['class'])

html = soup.prettify("utf-8")
with open("chap18_marked.html", "wb") as file:
    file.write(html)

# print(matchSpans(soup, '单维关联规则若关联规则中的项或属性只涉及一个维，则称它为单维关联规则。单维关联规则展示了同一个属性或维内的联系。'))