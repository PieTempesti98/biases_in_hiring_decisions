# Hiring decisions biases
#### Business and project manager project work made by Pietro Tempesti and Beedetta Tessa

Objective of this project is to find the most common biases in the hiring decisions. To do so, a preliminary research in
literature is crucial to address our researches.

In this repository you can find the code we've used to scrape the *scopus* database ([`scraping.py`](./scraping.py)) and
our keyphrase extractor from the scraping results ([`nlp.py`](./nlp.py)).

## How to run the code
Add a `config.json` file with your *scopus APIKey* in the repository. The format of the file is:

<pre><code>{
  "apikey": "[YOUR API KEY]",
  "insttoken": "[YOUR INSTITUTION CODE]"    //if you don't have an institution code, then leave ""
}</code></pre>

Then, start the `scraping.py` script. It fetches from scopus at most 5000 documents and saves their abstracts in the 
`data/abstracts.txt` file.

Start the `nlp.py` script to perform the keyphrase extraction from the .txt file; the results will be saved in the 
`data/keyphrases_[# of words].csv` file


