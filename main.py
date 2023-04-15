import openai
import typer

from utils import Config
from rich import print
from rich.table import Table

config = Config()
openai.api_key = config.get('api_key')
table = Table("Comando", "Descripción")
table.add_row("exit", "Stop the CLI")
table.add_row("new", "Start new conversation")
print(table)


def main():
    context = {"role": "system",
               "content": "You are an useful assistant that translates from spanish to english and vice versa."
                          "You are able to detect the language used."
                          "Your name is Axel."
                          "If a question starts with Axel, you assume it's a question that doesn't have to do "
                          "with the translation and will look for a useful and helpful response."
                          "Otherwise you'll only respond with the translation."}
    messages = [context]

    while True:
        content = _prompt()
        if content == 'new':  # new unrelated conversation
            messages = [context]
            print("[bold green]<[/bold green] [green]Let's start a new conversation[/green]")
            content = _prompt()

        messages.append({"role": "user", "content": content})
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
        response_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_content})
        print(f"[bold green]<[/bold green] [green]{response_content}[/green]")


def _prompt() -> str:
    request = typer.prompt('\n> ', prompt_suffix='')
    if request == 'exit':  # salir
        print('[bold green]<[/bold green] [green]Bye[/green]')
        raise typer.Abort()
    return request


if __name__ == "__main__":
    typer.run(main)