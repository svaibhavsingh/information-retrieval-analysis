# information-retrieval-analysis


NOTE:
Please change the directory of the documents accordingly as per your system in the source code. e.g. 
docDirectory = "D:\\Visual Studio  Projects\\PythonApplication1\\crawlDir_set10\\"



Output:
Section 1:
4 files I1, I2, I3 and I4 (in .txt format) will be generated in the same directory as the source-file of the inverted indexes created in Step 1, Step 2, Step 3 and Step 4 respectively of Section-I. 

Also in python terminal, the following 5 stats will be printed for each inverted index:
1. Number of Terms
2. Maximum Length of Postings List
3. Minimum Length of Postings List
4. Average Length of Postings List
5. Size of the file that stores the inverted index
Section 2:
Most frequent, median and least frequent K (20) words, their Posting List size and for each of these words, average gap between documents in the Postings List are printed in terminal. The value of K can be changed by changing the variable K inside the source code.
Section 3:
A png file containing the graph for 'log of the rank of the term' vs 'log of collection frequency of the term' will be generated in the same directory named “logRankCollectionFreq”.
Section 4:
A png file containing the graph for 'log of the number of tokens already seen' vs 'log of the vocabulary size' will be generated in the same directory named “logTokenVacabulary”.
