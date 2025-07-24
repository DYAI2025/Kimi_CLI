import threading
from typing import Optional
from kimi_client import KimiClient
from execution_toolkit import execute_shell_command, read_file, write_file, delete_file


class KimiK2Agent:
    """Autonomous agent with direct execution capabilities."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = KimiClient(api_key=api_key)
        self.stop_requested = False

    def run_command(self, command: str) -> str:
        result = execute_shell_command(command)
        output = []
        if result["stdout"]:
            output.append(result["stdout"])
        if result["stderr"]:
            output.append(result["stderr"])
        output.append(f"exit_code={result['exit_code']}")
        return "\n".join(output)

    def stop(self):
        self.stop_requested = True

    def run_plan(self, plan: str):
        """Simple loop executing shell commands from a plan string."""
        for line in plan.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if self.stop_requested:
                break
            print(f"$ {line}")
            result = self.run_command(line)
            print(result)


def run_agent(plan_path: str, api_key: Optional[str] = None):
    agent = KimiK2Agent(api_key)
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = f.read()
    agent_thread = threading.Thread(target=agent.run_plan, args=(plan,), daemon=True)
    agent_thread.start()
    try:
        while agent_thread.is_alive():
            agent_thread.join(0.5)
    except KeyboardInterrupt:
        agent.stop()
        agent_thread.join()
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 kimi_k2_agent.py <plan_file>")
    else:
        run_agent(sys.argv[1])
