from typing import List, Optional

class Author:
    def __init__(self, author_info: dict):
        # Add more fields as needed
        self.name = author_info.get('name')
        self.authorId = author_info.get('authorId')

class Paper:
    def __init__(self, paper_info: dict):
        self.paperId = paper_info.get('paperId')
        self.corpusId = paper_info.get('corpusId')
        self.externalIds = paper_info.get('externalIds')
        self.url = paper_info.get('url')
        self.title = paper_info.get('title')
        self.abstract = paper_info.get('abstract')
        self.venue = paper_info.get('venue')
        self.publicationVenue = paper_info.get('publicationVenue')
        self.year = paper_info.get('year')
        self.referenceCount = paper_info.get('referenceCount')
        self.citationCount = paper_info.get('citationCount')
        self.influentialCitationCount = paper_info.get('influentialCitationCount')
        self.isOpenAccess = paper_info.get('isOpenAccess')
        self.openAccessPdf = paper_info.get('openAccessPdf')
        self.fieldsOfStudy = paper_info.get('fieldsOfStudy')
        self.s2FieldsOfStudy = paper_info.get('s2FieldsOfStudy')
        self.publicationTypes = paper_info.get('publicationTypes')
        self.publicationDate = paper_info.get('publicationDate')
        self.journal = paper_info.get('journal')
        self.citationStyles = paper_info.get('citationStyles')
        self.authors = [Author(author) for author in paper_info.get('authors', [])]
        self.CureMeRanking = 0

class SemanticQueryApiResponse:
 def __init__(self, total, papers):
        self.total = total
        self.papers = [Paper(paper) for paper in papers]