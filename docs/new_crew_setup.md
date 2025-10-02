# **CrewAI setup**

If you are creating a CrewAI project from scratch, follow the instructions below. 

Note: These steps are not required for running this lab project, as this project has been provided to you as a Crew project already. To run this lab, refer to `project_guide.md`. 

The instructions for creating a crewAI setup are also available at [crewAI documentation](https://docs.crewai.com/installation).

## Installations:
1. Install UV. You may have done this already during our sessions. If not, run the installation command below:

    On macOS/Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    On Windows:
    
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    If you run into any issues, refer to [UV’s installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.

2. Install CrewAI 🚀

    ```bash
    uv tool install crewai
    ```

## Creating a CrewAI project

1. Run the crewai CLI command: 
    ```bash
    crewai create crew <your_project_name>
    ```
2. You will get prompted to enter your choice of LLM/model/key. Once you input these, your CrewAI project is now created. You can open it in your IDE.
3. Customize your project:
    - Modify `src/<project_name>/config/agents.yaml` to define project specific agents
    - Modify `src/<project_name>/config/tasks.yaml` to define project specific tasks
    - Modify `src/<project_name>/crew.py` to add any project specific logic, tools and specific args
    - Modify `src/<project_name>/main.py` to add custom inputs for our agents and tasks
    - Keep sensitive information like API keys in `.env`.
4. Run your Crew:
    - Before you run your crew, make sure to run: `crewai install`
    - If you need to install additional packages, use: `uv add <package-name>`
    - To run your crew, execute the following command in the root of your project: `crewai run`