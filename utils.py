from apiclient.discovery import build


api_key="AIzaSyARJ3eYy7G-Jxc_aDjU8QfecAScmFeVdXc"

resource = build('customsearch', 'v1', developerKey=api_key).cse()

response = resource.list(q='python', cx="001380558770229582407:s9fgjefe8qi", searchType='image').execute()

for i in response['items']:
    print(i['title'], i['link'])