# -------------------------------------------------------------------------------------------
#  Copyright (c) 2024.  SupportVectors AI Lab
#
#  This code is part of the training material, and therefore part of the intellectual property.
#  It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#  Use is limited to the duration and purpose of the training at SupportVectors.
#
#  Author: SupportVectors AI Training
# -------------------------------------------------------------------------------------------



from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from crewai_tools import SerperDevTool
from assignment.schemas import FetchResult, SummariesOutput

web_search_tool = SerperDevTool()

@CrewBase
class Assignment():
    """Assignment crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def research_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['research_assistant'], # type: ignore[index]
            tools = [web_search_tool],
            verbose=True
        )

    @agent
    def editor_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['editor_assistant'], # type: ignore[index]
            verbose=True
        )

    @agent
    def chief_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_editor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def judge_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['judge_editor'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def fetch_ai_news(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_ai_news'], # type: ignore[index]
            output_file='results/news.md',
            output_pydantic=FetchResult
        )

    @task
    def summarize_ai_news(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_ai_news'], # type: ignore[index]
            context=[self.fetch_ai_news()],
            output_file='results/editorial.md',
            output_pydantic=SummariesOutput
        )

    @task
    def draft_html_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config['draft_html_newsletter'], # type: ignore[index]
            output_file='results/draft.html'
        )

    @task
    def finalize_html_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_html_newsletter'], # type: ignore[index]
            output_file='results/newsletter.html'
        )
    @crew
    def crew(self) -> Crew:
        """Creates the Assignment crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )