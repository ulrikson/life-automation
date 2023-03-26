from todoist import Todoist

todoist = Todoist()

# Get tasks from Todoist API that contain a question mark
tasks = todoist.get_completion_tasks()

print(tasks)