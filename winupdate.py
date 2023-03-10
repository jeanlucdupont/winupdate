""" ---------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------- 
    Get the latest update from Microsoft's horrible Windows update page
    Author:         JL Dupont
    Date/version:   20230303
"""

""" ---------------------------------------------------------------------------
    Imports
    ----------------------------------------------------------------------- """
import requests  
from bs4 import BeautifulSoup  
import re  

""" ---------------------------------------------------------------------------
    Functions
    ----------------------------------------------------------------------- """
def f_getinfo(regex, string):
    match = re.search(regex, string)
    if match:
        return str(match.group(1))
    else:
        return "EOL"


""" ---------------------------------------------------------------------------
    Main
    ----------------------------------------------------------------------- """

#  list of URLs to scrape
urls        = [ "https://support.microsoft.com/en-us/topic/windows-10-update-history-8127c2c6-6edf-4fdf-8b9f-0f7be1ef3562",
                "https://support.microsoft.com/en-us/topic/windows-server-2012-update-history-abfb9afd-2ebf-1c19-4224-ad86f8741edd"
                ]
updates     = []  # create an empty list to store update information
uniques     = []  # same as above but without duplicates


# loop through each URL in the list
for url in urls:  
    response = requests.get(url)  
    soup = BeautifulSoup(response.content, "html.parser")  
    uls = soup.find_all("ul", class_="supLeftNavArticles") 
    for ul in uls:  
        match = False  
        lis = ul.find_all("li", class_="supLeftNavArticle")  
        if lis != None:  
            for li in lis:  
                las = li.find_all("a")  # find hyperlink
                for la in las:  
                    # here we have the Windows version. Let's clean the string
                    if "update history" in la.string or "Windows Server 2012" in la.string:  
                        winver = re.sub(r'[^\x00-\x7F]+', ' ', la.string)  
                    elif "Preview" not in la.string and "Out-of-band" not in la.string:  
                        # Here we have the latest update. Let's extract the date, the KB number, and the URL
                        infotext    = re.sub(r'[^\x00-\x7F]+', ' ', la.string)  
                        infotext    = infotext.replace('-', ' ')
                        matchdate   = f_getinfo(r"([A-Z][a-z]+ \d{1,2}, \d{4})", infotext)
                        matchkb     = f_getinfo(r"(KB\d+)", infotext)
                        url         = 'https://support.microsoft.com' + re.search(r'href="([^"]+)"', str(la)).group(1)  
                        match       = True  
                        updates.append([winver, matchkb, matchdate, url])  
                    if match == True: 
                        break  
                if match == True:  
                    break  

uniques     = []  
for update in updates:  
    if update not in uniques: 
        uniques.append(update)

print(uniques)    

""" ---------------------------------------------------------------------------
    End
    ----------------------------------------------------------------------- """
