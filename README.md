# patent-text-clustering

Patent analysis for specified corporation. Now the work is focused on Denso Corporation.

# Prerequiste

Carrot2-workbench 4.6
Selenium 3.4.3
PhantomJS 2.1.1 / (Firefox + geckodriver)

# Usage

`python crawler_patent.py`

`python format.py`

# Code Overview
* `crawler_patent.py`: Collect patents from [Google Patents](https://patents.google.com), and store it in patents.json
* `format.py`: Change patents.json into patents.xml, which can be passed into Carrot2 for text clustering

# Suggested Reading

[Clustering documents from XML files](http://download.carrot2.org/head/manual/index.html#section.getting-started.xml-files)
