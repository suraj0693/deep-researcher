from smolagents import CodeAgent
from smolagents.default_tools import DuckDuckGoSearchTool
import json
from concurrent.futures import ThreadPoolExecutor

from src.tools.crawler import Crawler
from src.tools.web_search import WebSearch
from smolagents.models import LiteLLMModel
from src.models import QueryPlanResponse
from src.prompts.query_planner import query_planner_prompt
from src.memory import Memory
from src.llm import LLM
from src.prompts.report import key_points_and_executive_summary_prompt, step_report_prompt, conclusion_prompt


class DeepResearcher:
    def __init__(self, planning_steps):
        self.memory = Memory()
        self.planner_agent = QueryPlanner(planning_steps=planning_steps)
        self.team_agent = CodeAgent(
            name="Web search agent",
            description="A web search agent that can search the web for information, crawl the webistes and provide "
                        "the information to the deep researcher agent",
            model=LiteLLMModel(model_id="openai/qwen/qwen3-4b",
                               api_base="http://192.168.0.105:1234/v1/",
                               api_key="fake_key",
                               ),
            tools=[DuckDuckGoSearchTool()],
        )
        self.reporter_agent = Reporter(self.memory)

    def run(self, query: str):
        plans = self.planner_agent.run(query=query)
        self.memory.plan = plans['queries']
        yield self.memory.plan
        # make concurrent calls to team agent for each query and wait for all the results
        def run_query_concurrently(sub_query):
            return self.team_agent.run(task=sub_query['sub_query'])

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_query_concurrently, sub_query) for sub_query in self.memory.plan]
            results = [future.result() for future in futures]
            for result, sub_query in zip(results, self.memory.plan):
                self.memory.step.append({sub_query: result})
        report = self.reporter_agent.get_key_points_and_executive_summary(query)
        for step_result in self.memory.step:
            report = report + "\n\n"+ self.reporter_agent.generate_step_report(report, step_result)
        yield report


class QueryPlanner:
    """
    A query planner agent that will do a investigative search for content to better understand the query.
    After understanding the query, it will divide the query into multiple queries to do a comprehensive research.
    """

    def __init__(self, planning_steps: int):
        self.agent = CodeAgent(
            name="QueryPlanner",
            description="A query planner agent that will do a investigative search for content to better understand "
                        "the query. After understanding the query, it will divide the query into multiple queries to "
                        "do a comprehensive research.",
            model=LiteLLMModel(model_id="openai/qwen/qwen3-4b",
                               api_base="http://192.168.0.105:1234/v1/",
                               api_key="fake_key",
                               ),
            tools=[]
        )
        self.planning_steps = planning_steps

    def run(self, query: str):
        query = query_planner_prompt.format(query=query, num_queries=self.planning_steps)
        plans = self.agent.run(task=query, max_steps=5)
        plans = json.loads(plans)
        sub_queries = plans['queries']
        print(sub_queries)
        return plans


class Reporter:

    def __init__(self, memory=None):
        self.llm = LLM(model_id="openai/qwen/qwen3-4b",
                       api_base="http://192.168.0.105:1234/v1/",
                       api_key="fake_key",
                       )
        self.memory: Memory = memory

    def generate_step_report(self, partial_report, step_result):
        prompt = step_report_prompt.format(previously_generated=partial_report, step_content=str(step_result)) + step_result
        step_report = self.llm.run(prompt)
        return step_report

    def get_key_points_and_executive_summary(self, query):
        prompt = key_points_and_executive_summary_prompt.format(query=query, research_results=str(self.memory.step)) 
        key_points_and_executive_summary = self.llm.run(prompt)
        return key_points_and_executive_summary

    def get_conclusion(self):
        prompt = conclusion_prompt + self.step_results
        conclusion = self.llm.run(prompt)
        return conclusion


if __name__ == "__main__":
    dr = DeepResearcher(planning_steps=3)
