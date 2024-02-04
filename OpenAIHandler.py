from openai import OpenAI


def constructAPIMessages(lstPapers):
    messages=[
\        {"role": "system", "content": """You are a doctor who's role is to summarize
            the provided papers and give the latest information on treatment and medical advances in the given field. 
            Summarize each paper individually into 1-2 sentences. Use the weighting metric to determine how much attention each paper deserves and how relevant it's findings are, higher is better. They are sorted in order of relevance"""},
    ]

    for paper in lstPapers[:100]:
        messages.append(
            {"role": "user", "content": f"Title: {paper.title} Weight: {paper.CureMeRanking} Abstract: {paper.abstract}"}
        )

    return messages


def getSummaryFromOpenai(lstPapers):
    client = OpenAI()

    completion = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=constructAPIMessages(lstPapers)
    )

    #print(completion.choices[0].message)


    messages=[
          {"role": "system", "content": """Given the following papers and their summaries, produce 3-4 lines of advice for someone suffering with ulceritive colitis on the latest developments in the field
          things they might see in their treatment in the future, which are generally proving most effective and things they could potentially ask their doctor for, things that appear multiple times are worth more. In the last line, put 'Reasoning:' followed by why you gave that summary"""},
          {"role": "user", "content": f"{str(completion.choices[0].message)}"}
    ]

    completion = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=messages
    )

    print(completion.choices[0].message)


