from itertools import islice
import libtmux
import os
import sys

from agents import (
    Agent,
    function_tool,
    OpenAIChatCompletionsModel,
    ToolCallItem,
    set_default_openai_client,
    Runner,
    AsyncOpenAI,
    set_tracing_disabled,
    ModelSettings,
    enable_verbose_stdout_logging,
)

# model = "google/gemini-2.0-flash-001"
# model = "openai/o4-mini-high"
model = "anthropic/claude-3.7-sonnet:thinking"

s = libtmux.Server()
stdout: list[str] = iter(s.cmd(*"capture-pane -S 1 -p".split()).stdout[::-1])


def get_command_hist(n: int) -> list[str]:
    from itertools import islice

    return list(islice(stdout, n))


@function_tool(description_override="Get command history")
async def get_command_hist_tool(n: int) -> list[str]:
    """Get command history"""

    return get_command_hist(n)


@function_tool(description_override="Ask for user")
async def ask_for_user(ask: str) -> str:
    """Ask for a command"""

    print(f"shelper needs to answer: {ask}")

    return input()


@function_tool(description_override="Execute command")
async def execute_command(command: str) -> str:
    """Execute command"""

    import subprocess

    print(f"shelper needs to execute command: {command}")
    ok = input("Do you want to execute? (y/n): ")
    if ok != "y":
        return "requested command was denied by user"

    res = subprocess.run(command, shell=True, capture_output=True, text=True)

    return f"stdout:{res.stdout},stderr:{res.stderr},returncode:{res.returncode}"


async def run_agent():
    key = os.environ.get("OPENROUTER_KEY")

    client = AsyncOpenAI(
        api_key=key,
        base_url="https://openrouter.ai/api/v1",
        timeout=60,
    )

    set_default_openai_client(client)
    set_tracing_disabled(True)

    pricing = {}
    for m in (await client.models.list()).data:
        pricing[m.id] = {
            "prompt": float(m.pricing["prompt"]),
            "completion": float(m.pricing["completion"]),
        }

    agent = Agent(
        name="shelper",
        instructions="""
あなたはシェルコマンドのヘルパーです。履歴とプロンプトを見て、適切なシェルコマンドを提示してください。

- 用いることができる情報
    - 今までのコマンドの履歴を得ることができます。デフォルトでは30行分の履歴を提示します。より多くの履歴が必要な場合、get_command_hist(n)を用いて追加の履歴を取得してください。履歴の中には、あなたとの過去のやり取りも含まれています。それを考慮して、適切なコマンドを提示してください。
    - ユーザから、実行したいコマンドの要求が渡されます。その意図を理解し、適切なコマンドを提示してください。しかし、暗黙の仮定はおかず、不明な点がある場合は`ask_for_user(ask)`を用いてユーザに質問してください。
    - 実際にコマンドを実行することで適切な情報を得られると判断した場合、`execute_command(command)`を用いてコマンド実行することが可能です。
- 注意点
    - 返答は日本語で行ってください。
""",
        model=OpenAIChatCompletionsModel(model=model, openai_client=client),
        model_settings=ModelSettings(
            max_tokens=2000,
            include_usage=True,
        ),
        tools=[
            get_command_hist_tool,
            ask_for_user,
            execute_command,
        ],
        mcp_servers=[],
    )

    messages = [
        {
            "role": "user",
            "content": "\n".join(get_command_hist(30)),
        },
        {
            "role": "user",
            "content": "User Prompt: " + " ".join(sys.argv[1:]),
        },
    ]

    response = await Runner.run(
        agent,
        messages,
        max_turns=10,
    )

    usage = response.raw_responses[-1].usage

    if usage is not None:
        input_token = usage.input_tokens
        output_token = usage.output_tokens
        cost = (
            input_token * pricing[model]["prompt"]
            + output_token * pricing[model]["completion"]
        )

        meta = f"meta {{ model: {model}, input: {input_token}, output: {output_token}, cost: {cost:.6f}$ }}"
    else:
        meta = "meta { no information provided }"

    print(response.final_output)
    print(meta)


