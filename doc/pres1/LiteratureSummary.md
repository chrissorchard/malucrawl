1. deSEO Summary
   
    First systematic study of search-result poisoning attacks and detection. 
    
    * SEO: Search Engine Optimization techniques
        * Optimization of page rank / Search-result poisoning
        * Cloaking techniques from attacker
        * Classified into White-hat and Black-hat

    * Why SEO attack is successful:
        * Generation of relevant content
        * Targeting multiple trending keywords
        * Creating dense link structures to increase page rank

    * deSEO: automatically detect SEO attacks and campaigns
        * History-based detection
        * Clustering of suspicious domains
        * Group analysis
    
    Keywords collection from Google trends: 28th May 2010 --- 3rd Feb 2011

    More than 300 billion URLs dataset
    
    Result: 957 unique compromised domains, 15,482 malicious URLs. 

1. Automatic Malware Collecting System
   
    A system collects search keywords and the malicious code which uses the keywords.
    * Malicious code collection approaches:
        * Passive method
        * Active method: Low interaction & High interaction
    * The automatic malicious code collecting system:
       * Active Hybrid Method
       * Collect search keywords
       * Filter search results by reviewing URL components (Low interaction)
       * Suspicious websites are visited with a client honeypot (High interaction)
       * Source code analysis with specialised VM

    
    Files collected from 22nd Nov 2010 to 11th Jan 2011
    
    Result: 1,287 unique suspicious codes collected, 986 determined to be malicious.

1. Fashion Crimes: Trending-Term Exploitation on the Web

    First large-scale measurement and analysis of trending-term exploitation. 

    * Classification of MFA (Made for AdSense) and malware sites
    * Difference between MFA and malware sites tactics
    * Trending-term abuse measurement
    * Economics of exploitation / Revenue analysis
    * Google’s intervention reduced revenue by 30%

    Dataset collected between 24th Jul 2010 to 24 Apr 2011
    
    Over 60 million search results and tweets
    
    Result: MFA $100,000 per month, Malware $60,000 per month before search-engine intervention.
