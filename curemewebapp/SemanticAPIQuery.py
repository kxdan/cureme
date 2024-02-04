#Queries the Semantic API for a given search term

import requests
import datetime
from .OpenAIHandler import getSummaryFromOpenai
from functools import lru_cache
from .SemanticQueryResponse import SemanticQueryApiResponse



def CallSemanticAPIByKeyword(keyword, counts):
    current_year = datetime.datetime.now().year
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    start_year = current_year - 1
    all_papers = []  # List to store aggregated paper data
    total_results = 0  # Variable to store total results count

    for i in range(counts):  # Loop to make 5 API calls
        offset = i * 100  # Increase offset by 100 with each iteration

        params = {
            'query': keyword,
            'fields': 'paperId,title,authors,abstract,venue,year,citationCount',
            'sort': 'citationCount:desc',
            'year': f"{start_year}-",
            'minCitationCount': 3,
            'limit': 100,
            'offset': offset
        }

        headers = {
            'Authorization': 'Bearer YourAPIToken',  # Replace 'YourAPIToken' with your actual API token, if needed
        }

        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            total_results = response_data.get('total')  # Assuming 'total' represents the total number of matching results
            papers = response_data.get('data', [])
            all_papers.extend(papers)  # Aggregate paper data from each call
            print(f"Batch {i+1}: Retrieved {len(papers)} papers.")
        else:
            print(f"Failed to retrieve data for batch {i+1}, status code: {response.status_code}")

    # After all batches are processed, create an ApiResponse object
    aggregated_response = SemanticQueryApiResponse(total=total_results, papers=all_papers)
    print("total results for search term " + keyword + " " + str(total_results))

    return aggregated_response


def GetAndRankPapers(keyword):
    semanticQueryApiResponse = CallSemanticAPIByKeyword(keyword, 2)

    lstPapers = semanticQueryApiResponse.papers

    for paper in lstPapers:
        H_Index = get_authors_h_index(paper.paperId)
        #print(H_Index)

        #So as to not heavily bias towards papers with huge numbers of authors, going to tag a max of 5, and take the average of those 5
        avgWeight = 0

        if len(H_Index.items()) > 5:
            top_5 = sorted(H_Index.items(), key=lambda x: x[1], reverse=True)[:5]

            # Extract only the numbers from the top 5 items
            top_5_numbers = [number for name, number in top_5]

            # Sum up the numbers
            total_sum = sum(top_5_numbers)

            avgWeight = total_sum/5

        else:
            top_n = sorted(H_Index.items(), key=lambda x: x[1], reverse=True)[len(H_Index)-1]

            # Extract only the numbers from the top 5 items
            top_n_numbers = [number for name, number in top_n]

            # Sum up the numbers
            total_sum = sum(top_n_numbers)

            avgWeight = total_sum/len(H_Index)

        #paper.CureMeRanking = avgWeight
            
            #I made this number up, highest h-index ever is 300, very few people gonna break 150
        paper.CureMeRanking = avgWeight + min(paper.citationCount, 150)
        
        #print(str(paper.citationCount))
        
        """if paper.publicationDate != None:
            daysSincePublication = (datetime.datetime.now() - paper.publicationDate).days
            print(str(paper.publicationDate))
            print(str(daysSincePublication))"""
        
        #print(str(paper.CureMeRanking))

        return sorted(lstPapers, key=lambda paper: paper.CureMeRanking, reverse=True)


def get_authors_h_index(paper_id: str) -> dict:
    # Define the base URL for fetching author details from a paper ID
    base_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/authors"

    # Specify the fields to retrieve, including the hIndex
    params = {
        'fields': 'authorId,name,hIndex'
    }

    # Make the GET request to the API
    response = requests.get(base_url, params=params)

    # Initialize a dictionary to store author names and their h-index
    authors_h_index = {}

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Iterate through each author in the response
        for author in data.get('data', []):
            # Store the author's name and h-index in the dictionary
            authors_h_index[author['name']] = author.get('hIndex', 'N/A')
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
    
    return authors_h_index

@lru_cache(maxsize=100)
def backendQuery(searchTerm):
    lstRankedPapers = GetAndRankPapers(searchTerm)
    return str(getSummaryFromOpenai(lstRankedPapers))
    #getSummaryFromOpenai(lstRankedPapers)
    #do things
    
if __name__ == "__main__":
    backendQuery('ulcerative colitis')

#Because researchers make even the simpliest things seem complicated.

# take each paper, get summarized versions of it, weight that by the author
    #For each author, get some kind of metric of weight
    #Could be as simple as getting their H-Index and summing them

# Then rank by date and time, and give synopsis of each paper, and a credibility rating
    
# add email functionality
    
# add cron job so it runs every N days
    


#Summarize each paper, then get a high level overall summary of them all











