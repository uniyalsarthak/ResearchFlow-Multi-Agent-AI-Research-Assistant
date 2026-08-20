# from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

# def run_research_pipeline(topic : str) -> dict:

#     state = {}

#     #search agent working 
#     print("\n"+" ="*50)
#     print("step 1 - search agent is working ...")
#     print("="*50)

#     search_agent = build_search_agent()
#     search_result = search_agent.invoke({
#         "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
#     })
#     state["search_results"] = search_result['messages'][-1].content

#     print("\n search result ",state['search_results'])

#     #step 2 - reader agent 
#     print("\n"+" ="*50)
#     print("step 2 - Reader agent is scraping top resources ...")
#     print("="*50)

#     reader_agent = build_reader_agent()
#     reader_result = reader_agent.invoke({
#         "messages": [("user",
#             f"Based on the following search results about '{topic}', "
#             f"pick the most relevant URL and scrape it for deeper content.\n\n"
#             f"Search Results:\n{state['search_results'][:800]}"
#         )]
#     })

#     state['scraped_content'] = reader_result['messages'][-1].content

#     print("\nscraped content: \n", state['scraped_content'])

#     #step 3 - writer chain 

#     print("\n"+" ="*50)
#     print("step 3 - Writer is drafting the report ...")
#     print("="*50)

#     research_combined = (
#         f"SEARCH RESULTS : \n {state['search_results']} \n\n"
#         f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
#     )

#     state["report"] = writer_chain.invoke({
#         "topic" : topic,
#         "research" : research_combined
#     })

#     print("\n Final Report\n",state['report'])

#     #critic report 

#     print("\n"+" ="*50)
#     print("step 4 - critic is reviewing the report ")
#     print("="*50)

#     state["feedback"] = critic_chain.invoke({
#         "report":state['report']
#     })

#     print("\n critic report \n", state['feedback'])

#     return state



# if __name__ == "__main__":
#     topic = input("\n Enter a research topic : ")
#     run_research_pipeline(topic)







from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
    sufficiency_chain,
)

MAX_ATTEMPTS = 3

def run_research_pipeline(topic: str) -> dict:
    state = {}
    sources_tried = []
    sufficient = False
    final_search_results = ""
    final_scraped_content = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):

        search_agent = build_search_agent()
        query = topic if attempt == 1 else f"{topic} (additional in-depth sources, attempt {attempt})"
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {query}")]
        })
        search_results = search_result["messages"][-1].content
        final_search_results = search_results

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{search_results[:800]}"
            )]
        })
        scraped_content = reader_result["messages"][-1].content
        final_scraped_content = scraped_content
        sources_tried.append(scraped_content)

        check = sufficiency_chain.invoke({
            "topic": topic,
            "content": scraped_content
        })

        if "YES" in check.upper():
            sufficient = True
            break

    state["search_results"] = final_search_results
    state["scraped_content"] = "\n\n---\n\n".join(sources_tried) if not sufficient else final_scraped_content
    state["attempts_used"] = attempt
    state["sufficient"] = sufficient

    # step 3 - writer chain
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # step 4 - critic chain
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)