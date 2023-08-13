from todoist import Todoist
from openai_api import ChatGPT

todoist = Todoist()
chatgpt = ChatGPT(model="gpt-3.5-turbo")

# Get tasks from Todoist API that contain a question mark
tasks = todoist.get_completion_tasks()

for task in tasks:
    # Get the question from the task
    question = task["content"]

    # Get the answer from ChatGPT
    answer = chatgpt.curious(question)

    # Update the task with the answer
    todoist.update_task({"description": answer}, task["id"])
