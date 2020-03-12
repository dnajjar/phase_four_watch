## Phase Four Watch

When the FDA approves a new molecular entity, it can impose an additional requirement known as a post-marketing requirement or phase four study. This means that the drug manufacturers are required to conduct large scale and often multi-year studies "to assess possible serious risks associated with the drugs," according to the FDA. Unfortunately the FDA seldom follows up on this requirement, and many drug companies do not comply with it. This script scrapes the FDA website and archive for new molecular entity approval letters since 2015. It then parses the letters for the word `postmarketing`, and downloads the data into a csv file that includes drug name, link url, and requirement. Approval letters before 2015 have been taken down from the FDA archive. 

## TODO:
If there is a requirement, find deadline
Check the clinical trials API to see if phase 4 trial has been registered
Find letters pre-2015
