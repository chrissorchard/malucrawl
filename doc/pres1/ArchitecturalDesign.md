Architectural Design Slides
===========================

1. Distributed Archetecture
    * [Celery](http://www.celeryproject.org/) with [RabbitMQ](http://www.rabbitmq.com/) for message passing and [Redis](http://redis.io/) to store results
    * "Celery is an asynchronous task queue/job queue based on distributed message passing."
    * Work can be distributed over a cluster of many machines on different networks.
    * Machines can be added and removed from the cluster without losing tasks
1. The system is split into three types of Task
    <dl>
        <dt>Trend Discovery</dt>
        <dd>
            <p>Find trends on [Twitter](https://www.twitter.com/), or news feeds like [The Sun](http://www.thesun.co.uk), [BBC News](http://www.bbc.com/news/) and [The Register](http://www.theregister.co.uk/]</p>
            <p>Takes no input, outputs a list of keywords</p>
        </dd>
        <dt>Search</dt>
        <dd>
            <p>Searches for a keyword in a Search Engine such as Google or Dogpile.</p>
            <p>Takes a keyword as input, outputs a list of URLs</p>
        </dd>
        <dt>Malware Scan</dt>
        <dd>
            <p>Dispatches a page to be scanned for malware. Either the active or passive scanning systems.</p>
            <p>Takes a URL as input, outputs a malware report.</p>
        </dd>
    </dl>
1. Periodic Tasks
    * Each period run each Trend Discorery, launching Search and Malware Scanning tasks as required.
    * Also run a new set of Search and Malware Scanning tasks for each Trend Discovery task that has been run historically.
    * So as to investigate malware incidence over time for each trend source
        * How long does it take on average for topics to be targeted by malware?
        * How long before malware is removed?
        * Which source gets the most malware?
1. Diagram
1. Demo