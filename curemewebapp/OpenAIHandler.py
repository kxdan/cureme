from openai import OpenAI

def constructAPIMessages(lstPapers):
    messages=[
        {"role": "system", "content": """You are a doctor who's role is to summarize
            the provided papers and give the latest information on treatment and medical advances in the given field. 
            Summarize each paper individually into 1-2 sentences. Use the weighting metric to determine how much attention each paper deserves and how relevant it's findings are, higher is better. They are sorted in order of relevance"""},
    ]

    for paper in lstPapers[:40]:
        messages.append(
            {"role": "user", "content": f"Title: {paper.title} Weight: {paper.CureMeRanking} Abstract: {paper.abstract}"}
        )

    return messages


def getSummaryFromOpenai(lstPapers, condition):
    client = OpenAI()

    APImessages = constructAPIMessages(lstPapers)

    completion = client.chat.completions.create(
      #model="gpt-4-0125-preview",
    model='gpt-3.5-turbo-0125',
      messages=APImessages
    )

    messages=[
          {"role": "system", "content": f"""Given the following papers and their summaries, produce 3-4 lines of advice for someone suffering with {condition} on the latest developments in the field based on the research papers provided, 
          things they might see in their treatment in the future, which are generally proving most effective and things they could potentially ask their doctor for, things that appear multiple times in the papers are worth more. In the last line, put 'Reasoning:' followed by why you gave that summary"""},
          {"role": "user", "content": f"{str(completion.choices[0].message)}"}
    ]

    completion = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=messages
    )

    print(completion.choices[0].message.content)

    return (completion.choices[0].message.content)


