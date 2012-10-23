AD Speakers Notes
=================

Overview
--------

While most of the previous studies have used a simple system based on WGET, the bases of our system is a Distributed Architecture.

To build this sytem, the Celery module will be used.
This is because it impliments a common python interface for a distributed task queue, in ths case RabbitMQ.

This is an advantage because the crawling system can be scaled up and distributed over a large cluster of many networked machines.

This also means that we can make requests from the system from lots of different IP addresses, so that the network cannot be blacklisted by Malware Distribution Networks.

Because RabbitMQ makes guaruntees about jobs, it means we can add and remove machines from "temporary style" cloud virtual machines. Such as Amazon Spot Instances.

Task Classes
------------

The system is split into three different classes. Trend Discovery, Search and Malware Scanning.

Each type can be implimented using different providers. Such as Twitter, Google and the different types of malware detection.

*change slide*

Each task type feeds into the next, so in this example. So in this example, each Topic discovered from Twitter is search on Dogpile, the meta search engine. Then URLs from that are then dispatched to the malware detection tasks.

Periodic Tasks
--------------

Because it's ulikely that malware will respond directly after a topic begins to trend, we must be able to investigate the same set of topics over time.

To do this tasks are run regularly, say each day, to download the new trending topics of that day and also search and crawl new pages for each of the topics that have ever been discussed.

"You're going to increase the amount you download forever!? (No It's going to be over a window. After say a year? The oldest topics will no longer be searched for)

This means that the database must be able to stroe malware indicence over time for each source.

We can look at changes over time and topic source when investigating malware. You find the most malware for Emma Watson, do you find the most malware for searches from The Sun headlines or topics trending on twitter? And how long does it take for a Malware network to find a topic not to be worth relating malware to.

*Should the demo be here?*

Now you're going to see a demo of the distributed system in process. We only have two machines running workers, and we havn't got any real malware scanning systems - so we're just returning the title of the document as a malware report. So we demonstrate that we can download and process the documents at the URLs we discover.