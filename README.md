# Enron-DG

The dataset is available for download [here](https://drive.google.com/file/d/0B16iuQ0QrgB1aERkaTlqUF9LTnc/view). It is a large collection of semi-structured data made publicly available that describes the email correspondence of Enron employees. More information about the dataset is available [here](https://en.wikipedia.org/wiki/Enron_Corpus).

## Scripts

The script runs on the downloaded Enron dataset. Run the *dg_test.py* script, it will prompt for a file pathname of the downloaded csv file. The output will be a csv file with extractedcmessage fields.

For the second part of the test I attempted *Option 1: Extracting Conversations*. Initially I attempted to write my own algorithm for this whereby I would ignore messages with no subject heading, classify message with subject headings that occur once as unique/trivial message threads, and then attempt to only extract message threads between single addresses (i.e. messages where there is only one sender and one recipient). This would have allowed me to extract message threads from around 60% of the messages as predicted by Klimt B., [Yang Y. (2004, 225)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.1645&rep=rep1&type=pdf). However, implementing this algorithm was time-consuming. So I decided to implement a widely used algorithm for the detection of email threads by [Jamie Zawinski](https://www.jwz.org/doc/threading.html). My old algorithm can be found at the bottom of the *draft.py* script. 

To implement this algorithm, I plan to use [A.M. Kuchling's Python implementation](https://github.com/akuchling/jwzthreading). This can be found in the *jwzthreading.py* script. This second part was leading to some errors which I could not fix due to the time constraints of the test. I have therefore commented out this implentation at the bottom of the *dg_test.py* script. 
