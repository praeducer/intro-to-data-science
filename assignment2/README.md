Problem 1: Inspecting the Reuters Dataset; Basic Relational Algebra
====================================================================
(a) select:
-----------
Write a query that is equivalent to the following relational algebra expression.
```
σdocid=10398_txt_earn(frequency)
```
What to turn in: Run your query against your local database and determine the number of records returned. On the assignment page, upload a text file, select.txt, which includes a single line with the number of records.

(b) select project: 
-------------------
Write a SQL statement that is equivalent to the following relational algebra expression.
```
πterm(σdocid=10398_txt_earn and count=1(frequency))
```
What to turn in: Run your query against your local database and determine the number of records returned as described above. upload a text file select_project.txt which states the number of records.

(c) union:
----------
Write a SQL statement that is equivalent to the following relational algebra expression. 
```
πterm(σdocid=10398_txt_earn and count=1(frequency)) U πterm(σdocid=925_txt_trade and count=1(frequency))
```
What to turn in: Run your query against your local database and determine the number of records returned as described above. In your browser, upload a text file union.txt with a single line containing the number of records.

(d) count:
----------
Write a SQL statement to count the number of documents containing the word "parliament"

What to turn in: Run your query against your local database and determine the count returned as described above. On the assignment page, upload a text file count.txt with a single line containing the number of records.

(e) big documents:
------------------
Write a SQL statement to find all documents that have more than 300 total terms, including duplicate terms. (Hint: You can use the HAVING clause, or you can use a nested query.

What to turn in: Run your query against your local database and determine the number of records returned as described above. On the assignment page, upload a text file big_documents.txt with a single line containing the number of records.

(f) two words:
--------------
Write a SQL statement to count the number of unique documents that contain both the word 'transactions' and the word 'world'.

What to turn in: Run your query against your local database and determine the number of records returned as described above. On the assignment page, upload a text file two_words.txt with a single line containing the number of records.

Problem 2: Matrix Multiplication in SQL
========================================
Recall from lecture that a sparse matrix has many positions with a value of zero.

Systems designed to efficiently support sparse matrices look a lot like databases: They represent each cell as a record (i,j,value).

The benefit is that you only need one record for every non-zero element of a matrix.

Now, since you can represent a sparse matrix as a table, it's reasonable to consider whether you can express matrix multiplication as a SQL query and whether it makes sense to do so.

Within matrix.db, there are two matrices A and B represented as follows:
```
A(row_num, col_num, value)

B(row_num, col_num, value)
```
The matrix A and matrix B are both square matrices with 5 rows and 5 columns each.

(g) multiply:
--------------
Express A X B as a SQL query, referring to the class lecture for hints.

What to turn in: On the assignment page, turn in a text document multiply.txt with a single line containing the value of the cell (2,3)

Problem 3: Working with a Term-Document Matrix
===============================================
The reuters dataset can be considered a term-document matrix, which is an important representation for text analytics.

Each row of the matrix is a document vector, with one column for every term in the entire corpus. Naturally, some documents may not contain a given term, so this matrix is rather sparse. The value in each cell of the matrix is the term frequency. (You'd often want this this value to be a weighted term frequency, typically using "tf-idf": term frequency - inverse document frequency. But we'll stick with the raw frequency for now.)

What can you do with the term-document matrix D? One thing you can do is compute the similarity of documents. Just multiply the matrix with its own transpose S = DDT, and you have an (unnormalized) measure of similarity.

The result is a square document-document matrix, where each cell represents the similarity. Here, similarity is pretty simple: if two documents both contain a term, then the score goes up by the product of the two term frequencies. This score is equivalent to the dot product of the two document vectors.


(h) similarity matrix:
-----------------------
Write a query to compute the similarity matrix DDT. (Hint: The transpose is trivial -- just join on columns to columns instead of columns to rows.) The query could take some time to run if you compute the entire result. But notice that you don't need to compute the similarity of both (doc1, doc2) and (doc2, doc1) -- they are the same, since similarity is symmetric. If you wish, you can avoid this wasted work by adding a condition of the form a.docid < b.docid to your query. (But the query still won't return immediately if you try to compute every result -- don't expect otherwise.)

What to turn in: On the assignment website, turn in a text document similarity_matrix.txt that contains a single line giving the similarity of the two documents '10080_txt_crude' and '17035_txt_earn'.

You can also use this similarity metric to implement some primitive search capabilities. Consider a keyword query that you might type into Google: It's a bag of words, just like a document (typically a keyword query will have far fewer terms than a document, but that's ok).

So if we can compute the similarity of two documents, we can compute the similarity of a query with a document. You can imagine taking the union of the keywords represented as a small set of (docid, term, count) tuples with the set of all documents in the corpus, then recomputing the similarity matrix and returning the top 10 highest scoring documents.

(i) keyword search:
--------------------
Find the best matching document to the keyword query "washington taxes treasury". You can add this set of keywords to the document corpus with a union of scalar queries:
```
SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count
```
Then, compute the similarity matrix again, but filter for only similarities involving the "query document": docid = 'q'. Consider creating a view of this new corpus to simplify things.

What to turn in: On the assignment page, upload a text document keyword_search.txt that contains a single line giving the maximum similarity score between the query and any document. Your SQL query should return a list of (docid, similarity) pairs, but you will submit a file containing only a single number: the highest score in the list.
