#
# This file is part of LiteX-Agent-Eval.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

# Selftest of the agent evaluation tasks: the checker fails on the fresh workspace and passes with
# the reference solution. The offline tasks always run; the simulation tasks (Verilator, ~10s to
# ~2min each) only with LITEX_AGENT_EVAL_SIM=1; the hardware tasks run a dry run (elaboration, no
# board) when litex_boards is available, and on the board with LITEX_AGENT_EVAL_HW=<board>.

import os
import shutil
import importlib.util

import pytest

from litex_agent_eval.common import list_tasks, task_module
from litex_agent_eval.run import selftest_task

def _is_sim_task(task):
    return hasattr(task_module(task, "check"), "UART_PORT")

def _is_hw_task(task):
    return hasattr(task_module(task, "check"), "HARDWARE")

SIM_TASKS     = [t for t in list_tasks() if _is_sim_task(t)]
HW_TASKS      = [t for t in list_tasks() if _is_hw_task(t)]
OFFLINE_TASKS = [t for t in list_tasks() if not _is_sim_task(t) and not _is_hw_task(t)]

def test_tasks_layout():
    for task in list_tasks():
        assert hasattr(task_module(task, "check"),    "check")
        assert hasattr(task_module(task, "solution"), "solve")
    # Each task has its own TCP ports.
    ports = [p for t in SIM_TASKS for p in (task_module(t, "check").UART_PORT, task_module(t, "check").SERVER_PORT)]
    ports += [task_module(t, "check").SERVER_PORT for t in HW_TASKS]
    assert len(ports) == len(set(ports))
    ranges = [set(task_module(t, "check").AGENT_PORTS) for t in list_tasks()]
    assert sum(len(r) for r in ranges) == len(set().union(*ranges))
    # Hardware tasks have a dry run (no board).
    for task in HW_TASKS:
        assert hasattr(task_module(task, "check"), "dry_run")

@pytest.mark.parametrize("task", OFFLINE_TASKS)
def test_offline_task(task):
    r = selftest_task(task)
    assert r["passed"], r

@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.skipif(os.environ.get("LITEX_AGENT_EVAL_SIM") != "1",
    reason="Agent evaluation simulations only run with LITEX_AGENT_EVAL_SIM=1.")
@pytest.mark.skipif(shutil.which("verilator") is None, reason="Verilator not found.")
@pytest.mark.parametrize("task", SIM_TASKS)
def test_sim_task(task):
    r = selftest_task(task)
    assert r["passed"], r

@pytest.mark.slow
@pytest.mark.skipif(importlib.util.find_spec("litex_boards") is None, reason="litex_boards not found.")
@pytest.mark.parametrize("task", HW_TASKS)
def test_hw_task(task):
    r = selftest_task(task)
    assert r["passed"], r

def test_agent_command():
    from litex_agent_eval.run import agent_command
    shell = agent_command("p", "shell", "{}")
    assert "Bash" in shell and "mcp__litex" not in shell and "--disallowedTools" not in shell
    both = agent_command("p", "mcp", "cfg.json")
    assert "Bash" in both and "mcp__litex" in both
    only = agent_command("p", "mcponly", "cfg.json", model="m")
    i = only.index("--allowedTools")
    assert "Bash" not in only[i:only.index("--disallowedTools")]
    assert only[only.index("--disallowedTools") + 1] == "Bash"
    assert only[-2:] == ["--model", "m"]

def test_delegate_command():
    import json
    from litex_agent_eval.run import agent_command, OPERATOR
    cmd = agent_command("p", "delegate", "cfg.json", model="claude-opus-5-5", operator_model="claude-haiku-5-5")
    assert cmd[cmd.index("--disallowedTools") + 1] == "Bash"
    agents = json.loads(cmd[cmd.index("--agents") + 1])
    assert agents[OPERATOR]["model"] == "claude-haiku-5-5"
    assert all(t.startswith("mcp__litex__") for t in agents[OPERATOR]["tools"])
    hooks = json.loads(cmd[cmd.index("--settings") + 1])["hooks"]["PreToolUse"]
    assert hooks[0]["matcher"] == "mcp__litex__.*"

def test_operator_hook():
    import json, subprocess
    from litex_agent_eval.run import operator_hook, OPERATOR
    def run(payload):
        return subprocess.run(operator_hook(), shell=True, input=json.dumps(payload), capture_output=True, text=True)
    r = run({"tool_name": "mcp__litex__litex_check"})
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
    r = run({"tool_name": "mcp__litex__litex_check", "agent_type": OPERATOR})
    assert r.returncode == 0 and r.stdout == ""
