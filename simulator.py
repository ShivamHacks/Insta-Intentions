"""
A continuous simulation of the system.

Gives ChatGPT the API surface and lets it interact with the system.
"""

from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override
from database import Database

client = OpenAI(api_key=open(".ai_key.txt", "r").read())

api_surface = [
    {
        "type": "function",
        "function": {
            "name": "create_user_id",
            "description": "Create a new user with a unique ID and default fields.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_liked_username",
            "description": "Add a liked Instagram username to a user and update the Instagram handle table.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique ID of the user.",
                    },
                    "username": {
                        "type": "string",
                        "description": "The Instagram username to add to the liked list.",
                    },
                },
                "required": ["user_id", "username"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_people_that_have_liked",
            "description": "Retrieve users who have liked a particular Instagram handle.",
            "parameters": {
                "type": "object",
                "properties": {
                    "insta_handle": {
                        "type": "string",
                        "description": "The Instagram handle to query.",
                    },
                },
                "required": ["insta_handle"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "is_user_verified",
            "description": "Check if a user is verified.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique ID of the user.",
                    },
                },
                "required": ["user_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verify_user",
            "description": "Verify a user by setting their verified status and Instagram handle.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique ID of the user.",
                    },
                    "insta_handle": {
                        "type": "string",
                        "description": "The Instagram handle of the user.",
                    },
                },
                "required": ["user_id", "insta_handle"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dump_full_database",
            "description": "Retrieve a full dump of the database (for debugging purposes).",
            "parameters": {},
        },
    },
]

instructions = """
You are running a simulation of a world where you interface with
the database of a social media platform. Create realistic users,
usernames, and interactions to test the system. You do not have
any user input, you just keep taking actions.
"""


assistant = client.beta.assistants.create(
    name="Database Simulator",
    instructions=instructions,
    model="gpt-4o",
    tools=api_surface,
)

database = Database()


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_text_done(self, text):
        print()

    @override
    def on_tool_call_created(self, tool_call):
        # print(f"\nassistant > tool call: {tool_call.type}\n", flush=True)
        return

    @override
    def on_event(self, event):
        if event.event == "thread.run.requires_action":
            self.handle_requires_action(event.data)

    def handle_requires_action(self, data):
        tool_outputs = database.process_function_calls(
            data.required_action.submit_tool_outputs.tool_calls
        )
        self.submit_tool_outputs(tool_outputs)

    def submit_tool_outputs(self, tool_outputs):
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()


print("Starting simulation")
thread = client.beta.threads.create()
while True:
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=f"Take some action in the system.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
