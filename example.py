"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
from bs4 import BeautifulSoup
import requests


def get_request(paper_url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    response = requests.get(paper_url, headers=headers)

    if response.status_code != 200:
        print('Status code: ', response.status_code)
        raise Exception('Failed to fetch web page!')
    paper_doc = BeautifulSoup(response.text, 'xml')
    return paper_doc


## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])

print(client.api_key)
#Search on scopus
doc_search = ElsSearch('hiring decisions', 'scopus')
doc_search.execute(client, get_all=True)

keyword_counter = {}

for elem in doc_search.results:

    # retrieve the identifier of a document
    id = int(elem['dc:identifier'][10:])

    # request to the elsevier APIs the abstract and the keywords of the paper
    url = "https://api.elsevier.com/content/abstract/scopus_id/" + str(id) + '?apiKey=' + config['apikey']
    document = get_request(url)

    # Find and save all the keywords
    tags = document.find_all('dn:author-keyword')
    for tag in tags:
        keyword = tag.text.lower()
        if keyword in keyword_counter.keys():
            keyword_counter[keyword] += 1
        else:
            keyword_counter[keyword] = 1

keyword_counter = sorted(keyword_counter.items(), key=lambda x: x[1], reverse=True)
print(keyword_counter)




#
# ## Scopus (Abtract) document example
# # Initialize document with ID as integer
# scp_doc = AbsDoc(scp_id=84872135457)
# if scp_doc.read(client):
#     print("scp_doc.title: ", scp_doc.title)
#     scp_doc.write()
# else:
#     print("Read document failed.")
#
# ## ScienceDirect (full-text) document example using PII
# pii_doc = FullDoc(sd_pii='S1674927814000082')
# if pii_doc.read(client):
#     print("pii_doc.title: ", pii_doc.title)
#     pii_doc.write()
# else:
#     print("Read document failed.")
#
# ## ScienceDirect (full-text) document example using DOI
# doi_doc = FullDoc(doi='10.1016/S1525-1578(10)60571-5')
# if doi_doc.read(client):
#     print("doi_doc.title: ", doi_doc.title)
#     doi_doc.write()
# else:
#     print("Read document failed.")
#
# ## Load list of documents from the API into affilation and author objects.
# # Since a document list is retrieved for 25 entries at a time, this is
# #  a potentially lenghty operation - hence the prompt.
# print("Load documents (Y/N)?")
# s = input('--> ')
#
# if (s == "y" or s == "Y"):
#
#     ## Read all documents for example author, then write to disk
#     if my_auth.read_docs(client):
#         print("my_auth.doc_list has " + str(len(my_auth.doc_list)) + " items.")
#         my_auth.write_docs()
#     else:
#         print("Read docs for author failed.")
#
#     ## Read all documents for example affiliation, then write to disk
#     if my_aff.read_docs(client):
#         print("my_aff.doc_list has " + str(len(my_aff.doc_list)) + " items.")
#         my_aff.write_docs()
#     else:
#         print("Read docs for affiliation failed.")
#
# ## Initialize author search object and execute search
# auth_srch = ElsSearch('authlast(keuskamp)', 'author')
# auth_srch.execute(client)
# print("auth_srch has", len(auth_srch.results), "results.")
#
# ## Initialize affiliation search object and execute search
# aff_srch = ElsSearch('affil(amsterdam)', 'affiliation')
# aff_srch.execute(client)
# print("aff_srch has", len(aff_srch.results), "results.")
#
# ## Initialize doc search object using Scopus and execute search, retrieving
# #   all results
# doc_srch = ElsSearch("AFFIL(dartmouth) AND AUTHOR-NAME(lewis) AND PUBYEAR > 2011", 'scopus')
# doc_srch.execute(client, get_all=True)
# print("doc_srch has", len(doc_srch.results), "results.")
#
# ## Initialize doc search object using ScienceDirect and execute search,
# #   retrieving all results
# doc_srch = ElsSearch("star trek vs star wars", 'sciencedirect')
# doc_srch.execute(client, get_all=False)
# print("doc_srch has", len(doc_srch.results), "results.")