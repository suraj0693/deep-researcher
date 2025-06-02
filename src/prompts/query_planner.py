query_planner_prompt = """
Given the query, use available tools to comprehensively understand the query.

 - You should ultimately come up with a total of {num_queries} sub queries for the given query. These sub queries should cover all the aspects of the query.
 - The sub queries need not be a single sentence. you can have multiple sentences and as much context as you deem necessary. Clearer and more specific the sub queries with more context, better it is.
 - These sub queries are required to do a comprensive research on the query.
 - Use the tools available to you to have better understanding and  expanse of the query.
 - More number of sub queries required means a more comprehensive research is required, so prepare sub queries accordingly.
 - provide the sub queries in a json format. The json should have a key "queries" and the value should be a list of dictionary. Each dictionary will have a key for "sub_query" which will contain actual sub query and other "plan". This plan will contain a couple of lines on how what are we going to achieve in this sub query. When someone reads through all the plan one by one, he/she will get an idea on how the query is getting approached for research. The final response format should be like {{\"queries\":[{{\"sub_query\": \"_SUB_QUERY_\", \"plan\": \"_PLAN_\"}}, {{}}, ...]}}

The query is: {query}
"""