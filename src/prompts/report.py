key_points_and_executive_summary_prompt = """
Here are the research results for the given user query. You task is to provide key points and an executive summary from all this research results.

Important notes:
1. You must strictly stick to the content provided to write this section. You dont have any liberty to add any additional information.
2. Your output must be in markdown format.

User Query: 
{query}

Research results : 
{research_results}

Begin!
"""

step_report_prompt = """
You have to generate a part of a complete research report. This part should be coherent to all the earlier generated part of the report.

Important notes:
1. You will be given all the previously generated report content and also the content to write the current section.
2. If the only key points and executive summary is generated then that means you are generating the first section of the report's main content.
3. keep the writing style and everything in line with whatever is already generated. It should not appear that different sections are writen by different persions.
4. You must strictly stick to the content provided to write this section. You dont have any liberty to add any additional information.
3. Your output must be in markdown format.

Previously genetated report contet :
{previously_generated}

content for current section :
{step_content}

Begin!
"""

conclusion_prompt= """
"""