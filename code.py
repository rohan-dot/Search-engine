def webpage(url):                  #isse we get the basic html page we want to deploy our search engine on
    try:
        import urllib   
        return urllib.urlopen(url).read()   #opens url 
    except:
        return ""                           #if not found return blank 
    
def webcrawl1(page):       #get 1  link                              #web crawler begins
    start = page.find('<a href=')                  #do ctrl+f on any site and youll find all link have ahref before them
    if start == -1:
        return None, 0
    begin_quote = page.find('"', start)     #1
    end_quote = page.find('"', begin_quote + 1) #2
    url = page[begin_quote + 1:end_quote]       #with this we get rest of the urls on that page that will help us to crawl further
    return url, end_quote
    #with 1 and 2 we get a link in webpage that is between the 2 quotes
def webcrawl2(page):      #get all links on 1 url
    links = []
    while True:
        url, lastpos = webcrawl1(page)
        if url:
            links.append(url)
            page = page[lastpos:]
        else:
            break
    return links


def union(a, b):
    for p in b:
        if p not in a:
            a.append(p)

def webcrawl3(start_page): # returns index, graph of inlinks
    to_crawl = [start_page]   #yahaan se crawling begina coz ab code url waale page pe run karega
    crawled = []    #initially 0 pages crawled
    graph = {}  # <url>, [list of pages it links to]  #ranking algo to explain in class
    index = {} #dictionary
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            info = webpage(page)
            update_index(index, page, info)
            output = webcrawl2(info)
            graph[page] = output
            union(to_crawl, output)
            crawled.append(page)
    return index, graph


#index of search eng y



def update_index(index, url, info):
    
    words = info.split()
    for word in words:               #for loop to traverse for words
        update_index2(index, word, url)           #if word is found store to be displayed

def update_index2(index, keyword, url):     #adding to 
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def search(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

    
#ranking algo basically popularity meter concept is used

def page_rank_algo(graph):
    d = 0.7 # damping factor kuch bhi le sakte ahin between 0 and 1 to make it more optimal
    numloops = 15 #how many loops to iterate

    ranks = {}    #ranking all keyword to be stored.url as empty
    npages = len(graph)   #graph mein sabpages stored hain hence all pages ki length 
    for page in graph: 
        ranks[page] = 1.0 / npages   #har page ki rank

    for i in range(0, numloops):       #formula and idea of ranking algo taken from alta vista
        newranks = {}           #concept similar to fibionicci current and prev[-1] values are kept in mind
        for page in graph:
            newrank = (1 - d) / npages     #current
            for node in graph:                   #go through graph
                if page in graph[node]:   #check if page links to graph node
                    newrank = newrank + d * (ranks[node] / len(graph[node]))  #new rank d chosen for web serve to not access the page
            newranks[page] = newrank  
        ranks = newranks  #value updated
        #print ranks
    return ranks

#ek baar go through quick sort algo in cormen or geeksforgeeks
#sorting is termed as a extra component basically isme we are sorting ranks from best to worst quick sort is preferred because of optimality
def quicksort(url_lst,ranks):
    url_sorted_worse=[]    #self explanatory
    url_sorted_better=[]  #"  "
    if len(url_lst)<=1:
        return url_lst    #if only 1 url then return that url because no url to sort
    pivot=url_lst[0] #pivot elemet 
    for url in url_lst[1:]:
        if ranks[url]<=ranks[pivot]:
            url_sorted_worse.append(url)
        else:
            url_sorted_better.append(url)
    return quicksort(url_sorted_better,ranks)+[pivot]+quick_sort(url_sorted_worse,ranks)

        
def search(index, ranks, keyword):
    if keyword in index:
        
        all_urls=index[keyword]
        return all_urls
    else:
        return None
    return quicksort(all_urls,ranks)







index, graph = webcrawl3('http://hyperakt.com/')
ranks = page_rank_algo(graph)
print search(index, ranks, 'ABOUT')



#print ordered_search(index, ranks, 'zindagi')
# None
