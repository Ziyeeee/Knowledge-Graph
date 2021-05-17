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
                    line = line[line.index('<')+1:line.index('>')]
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
    nodes = [{'index': graphData[0][-1], 'label': graphData[0][2], 'reference': graphData[0][3], 'groupId': text2groupId[graphData[0][1]]}]
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


soup = bs(open('chap18.html'), features='html.parser')
ps = soup.find_all('p')
for p in ps:
    # print(p)
    strs = p.strings
    for s in strs:
        print(s)