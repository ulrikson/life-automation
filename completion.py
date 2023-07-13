from todoist import Todoist
from openai_api import ChatGPT

todoist = Todoist()
chatgpt = ChatGPT()

# Get tasks from Todoist API that contain a question mark
tasks = todoist.get_completion_tasks()

for task in tasks:
    # Get the question from the task
    question = task["content"]

    # If parent_id is a number, then fetch the parent task's description and add it as context
    if task["parent_id"]:
        parent_task = todoist.get_task(task["parent_id"])
        context = parent_task["description"]

    # Get the answer from ChatGPT
    answer = chatgpt.curious(question, context)

    # Update the task with the answer
    todoist.update_task({"description": answer}, task["id"])
