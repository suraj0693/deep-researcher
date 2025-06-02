from smolagents import CodeAgent
from smolagents.default_tools import DuckDuckGoSearchTool
import json

from src.tools.crawler import Crawler
from src.tools.web_search import WebSearch
from smolagents.models import LiteLLMModel
from src.models import QueryPlanResponse
from src.prompts.query_planner import query_planner_prompt
from src.memory import Memory


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

    def run(self, query: str):
        plans = self.planner_agent.run(query=query)
        self.memory.plan = plans['queries']
        yield self.memory.plan
        for sub_query in self.memory.plan:
            step_result = self.team_agent.run(task=sub_query['sub_query'])
            self.memory.step.append(step_result)


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

    def __init__(self, step_results):
        self.step_results = step_results

    def generate_report(self):
        pass

    def get_summary(self):
        pass


if __name__ == "__main__":
    dr = DeepResearcher(planning_steps=3)
