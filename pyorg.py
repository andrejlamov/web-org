import re

def parseorg(f):
    f = open(f, 'r')

    headre = '^(\*+)\s+(.*)'
    todore = '(TODO|DONE)\s+(.*)'
    tagre ='^(.*)\s+(:\S+:)'
    priore = '\s*\[#(\S)\]\s*(.*)'

    lines = map(lambda l: l.strip(), f.readlines())
    res = []
    content = []
    level = 0
    for l in lines:

        todo = None
        tags = []
        title = None
        prio = None

        m = re.match(headre, l)
        if m:
            (level, title) = m.groups()
            m = re.match(todore, title)
            if(m):
                (todo, title) = m.groups()
            
            m = re.match(tagre, title)
            if(m):
                (title, tagstring) = m.groups()
                tags = tagstring.split(':')[1:-1]

            m = re.match(priore, title)
            if(m):
                (prio, title) = m.groups()

            if not len(res) is 0:
                res[-1]['content'] = content
            content = []
            res.append({
                'type': 'heading',
                'level': len(level),
                'prio': prio,
                'todo': todo,
                'val': title.strip(),
                'tags': tags,
                'content': content
            })
        else:
            content.append(l)
    f.close()
    return res

def makeorg(data, filename):
    f = open(filename, 'w')
    res = []
    for d in data:
        print d
        if d['type'] == 'heading':
            s = '*' * d['level']
            if d['todo']:
                s += ' ' + d['todo']
            if d['val']:
                s += ' ' + d['val']
            res.append(s)
            for c in d['content']:
                res.append(c)
    for l in res:
        f.write(l + '\n')
    print res
    f.close()

    
