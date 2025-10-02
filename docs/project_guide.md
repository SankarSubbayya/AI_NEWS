# How to run this lab

## Installing UV (ignore if done)

You may have done this already during our sessions. If not, run the installation command below:

On macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows:
    
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If you run into any issues, refer to [UV’s installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.

## Steps to execute this project

1. `uv sync` in the root folder, after unzipping the code.
2. Create the `.env` file (Rename the `.env.example` file in this project to `.env`)
3. Add the following keys to your `.env` file:
    - OpenAI API key
    - Serper API key
4. Go to [Serper website](https://serper.dev/api-key), create an account and copy your API key. Add it to `.env`
5. To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project: `crewai run`
6. Output will be saved in the `results` folder.