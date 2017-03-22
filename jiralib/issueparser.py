
def errors_to_strings(argument):
    switcher = {
        0: "pass",
        1: "Need to add Acceptance criteria section",
        2: "Need to add more Acceptance criterias",
        3: "Need to add Descriptions",
        4: 'Need to add Responsible Manager',
        5: 'Need to add link to design document',
        6: 'Need to add Epic health field ',
        7: 'Need to add FixVersions field',
        8: 'Need to remove FixVersions field',
        9: 'Need to add Product Manager field',
        10: 'Neet do change status to In QA/Done',
        11: 'Neet do add US to the Epic',
        12: 'Neet do add QA engineers to the Epic',
        13: 'US does not have link to EPIC',
        14: 'Need to add link to Blueprint',
    }
    return switcher.get(argument)

def status_to_int(status):
        switcher = {
        'Open': 1,
        'Consideration': 2,
        'Backlog': 3,
        'Scoping': 4,
        'Design': 5,
        'In Development': 6,
        'In QA': 7,
        'Done': 8,
        }
        return switcher.get(status)

def priority_to_int(status):
        switcher = {
        'Some day': 1,
        'Nice to have': 2,
        'Major': 3,
        'Critical': 4,
        'Blocker': 5,
        }
        return switcher.get(status)


def parse_descriptions(text):
    text=text.lower()
    position = text.find('acceptance criteria')
    if position >=0:
        if len(text[position+len('acceptance criteria'):len(text)]) <10:
            return 2
        else:
            return 0
    else:
        return 1

