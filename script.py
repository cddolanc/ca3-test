month = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])
# Show the resulting timestamp
print(month)
# Ectract the week number from the start of the calendar year
# Extract the week number from the start of the calendar year
print(month.strftime("%V"))

#  Assemble the payload
data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

# Assemble the correct summary
summary = '<a href="https://mikhail-cct.github.io/ooapp/wk1/">Week 1: Introduction</a>'
summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/">Week 1: Introduction</a><br>'

# Assign the correct summary
data[0]['summary'] = summary