from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
from bs4 import BeautifulSoup
import requests


# function to request a document from the scopus database using its scopusID
def get_request(paper_url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.114 Safari/537.36'}
    response = requests.get(paper_url, headers=headers)

    # if the response is different from Ok (200), no data is returned
    if response.status_code != 200:
        return None

    # read the XML response using beautiful soup
    paper_doc = BeautifulSoup(response.text, 'xml')
    return paper_doc


# Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

# Initialize client
client = ElsClient(config['apikey'])

# Search on scopus
doc_search = ElsSearch('biases in hiring decisions', 'scopus')
doc_search.execute(client, get_all=True)

# new file in which the program appends all the obtained abstracts
file = open('data/abstracts.txt', 'a')

for elem in doc_search.results:

    # retrieve the identifier of a document
    scopus_id = int(elem['dc:identifier'][10:])

    # request to the elsevier APIs the abstract and the keywords of the paper
    url = "https://api.elsevier.com/content/article/scopus_id/" + str(scopus_id) + '?apiKey=' + config['apikey'] + \
          '&xml-encode=true'
    document = get_request(url)

    if document is None:
        continue

    # Find and save the abstract on the text file
    tag = document.find('dc:description').text.lower().strip()

    file.write(tag)


file.close()
print('file successfully created')
