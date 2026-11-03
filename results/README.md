# Results

Per-run results of the first evaluation rounds (2026-11-03), one CSV per round:
`round`, `task`, `model`, `condition`, `run`, `passed`, `wall_s`, `turns`, `mcp_calls`,
`shell_calls`, `other_calls`, `cost_usd`. Round 4 adds `timed_out`, `register_sequence_calls`,
`delegations`, `operator_calls`, `planner_cost_usd` and `operator_cost_usd`.

- Agent: Claude Code, headless (`claude -p`), stream-json transcripts. The transcripts are not
  published, because they contain local paths.
- Models: Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5.
- LiteX: master of 2026-11-03 plus the `litex_mcp` fixes of
  [litex#2743](https://github.com/enjoy-digital/litex/pull/2743). Round 4 also has
  `litex_register_sequence` and `litex_build_start(..., build=False)` from the same PR.
- `cost_usd` is the cost reported by the agent (list prices). It is blank for 3 runs that ended
  without a final result event.
- `turns` is the sum of the result events' turns.
- In `mcponly` runs, `shell_calls` counts attempted shell calls, which were denied.
- Wall times include whatever else was running on the machine. Up to five tasks ran in parallel,
  each on its own ports, so read the times as rough.

Tables: pass count, median wall time (s), mean turns, mean MCP calls, mean cost (USD).

## Round 1: faults visible in the source (v1 tasks)

One run per condition. `shell`: shell and file tools. `mcp`: the same tools plus `litex_mcp`.

| Task | Model | Condition | Pass | Wall | Turns | MCP | Cost |
|---|---|---|---|---|---|---|---|
| `bios_memtest` | opus-5-5 | shell | 1/1 | 582 | 13 | 0 | 0.26 |
| `bios_memtest` | opus-5-5 | mcp | 1/1 | 144 | 14 | 2 | 0.24 |
| `csr_address` | opus-5-5 | shell | 1/1 | 76 | 10 | 0 | 0.26 |
| `csr_address` | opus-5-5 | mcp | 1/1 | 67 | 12 | 0 | 0.32 |
| `fsm_stuck` | opus-5-5 | shell | 1/1 | 115 | 13 | 0 | 0.36 |
| `fsm_stuck` | opus-5-5 | mcp | 1/1 | 59 | 8 | 0 | 0.31 |
| `ticker_reset` | opus-5-5 | shell | 1/1 | 390 | 13 | 0 | 0.31 |
| `ticker_reset` | opus-5-5 | mcp | 1/1 | 76 | 11 | 0 | 0.30 |
| `timing_triage` | opus-5-5 | shell | 1/1 | 29 | 6 | 0 | 0.27 |
| `timing_triage` | opus-5-5 | mcp | 1/1 | 22 | 5 | 0 | 0.22 |

In every task, the agent found the fault by reading `target.py` before running anything. These
tasks measure reading, not tools. The time differences mostly come from the order of the runs and
from one self-written console polling loop.

## Round 2: faults only visible at runtime (v2 tasks), shell vs shell + MCP

| Task | Model | Condition | Pass | Wall | Turns | MCP | Cost |
|---|---|---|---|---|---|---|---|
| `firmware_blob` | opus-5-5 | shell | 3/3 | 173 | 20 | 0 | 0.48 |
| `firmware_blob` | opus-5-5 | mcp | 3/3 | 523 | 22 | 4 | 0.52 |
| `firmware_blob` | sonnet-5-5 | shell | 1/1 | 627 | 22 | 0 | 0.24 |
| `firmware_blob` | sonnet-5-5 | mcp | 1/1 | 470 | 14 | 0 | 0.18 |
| `opaque_gain` | opus-5-5 | shell | 3/3 | 188 | 20 | 0 | 0.68 |
| `opaque_gain` | opus-5-5 | mcp | 3/3 | 315 | 22 | 0 | 0.66 |
| `opaque_gain` | sonnet-5-5 | shell | 1/1 | 344 | 16 | 0 | 0.20 |
| `opaque_gain` | sonnet-5-5 | mcp | 1/1 | 289 | 14 | 0 | 0.19 |
| `stale_regs` | opus-5-5 | shell | 3/3 | 131 | 12 | 0 | 0.37 |
| `stale_regs` | opus-5-5 | mcp | 3/3 | 68 | 12 | 0 | 0.34 |
| `stale_regs` | sonnet-5-5 | shell | 1/1 | 126 | 8 | 0 | 0.12 |
| `stale_regs` | sonnet-5-5 | mcp | 1/1 | 70 | 11 | 0 | 0.16 |
| `stream_packer` | opus-5-5 | shell | 3/3 | 322 | 18 | 0 | 0.52 |
| `stream_packer` | opus-5-5 | mcp | 3/3 | 329 | 11 | 0 | 0.35 |
| `stream_packer` | sonnet-5-5 | shell | 1/1 | 427 | 17 | 0 | 0.17 |
| `stream_packer` | sonnet-5-5 | mcp | 1/1 | 256 | 12 | 0 | 0.13 |

All 32 runs passed. Only one of the 16 runs that had the MCP server used it. The agents did observe
the running SoC, but from the shell, using the LiteX tools that `litex_mcp` wraps. There is no
consistent difference in time or cost.

## Round 3: shell only vs MCP only, bench pre-started (`--bench`)

`shell`: shell and file tools, no MCP server. `mcponly`: `litex_mcp` and file tools, no shell.

| Task | Model | Condition | Pass | Wall | Turns | MCP | Cost |
|---|---|---|---|---|---|---|---|
| `ecpix5_scaler` (board) | opus-5-5 | shell | 2/2 | 316 | 13 | 0 | 0.49 |
| `ecpix5_scaler` (board) | opus-5-5 | mcponly | 2/2 | 123 | 43 | 34 | 0.45 |
| `ecpix5_scaler` (board) | sonnet-5-5 | shell | 1/1 | 70 | 7 | 0 | 0.15 |
| `ecpix5_scaler` (board) | sonnet-5-5 | mcponly | 1/1 | 84 | 43 | 32 | 0.22 |
| `ecpix5_scaler` (board) | haiku-5-5 | shell | 0/2 | 640 | 24 | 0 | 0.04 |
| `ecpix5_scaler` (board) | haiku-5-5 | mcponly | 2/2 | 222 | 80 | 69 | 0.06 |
| `opaque_gain` | opus-5-5 | shell | 3/3 | 444 | 14 | 0 | 0.46 |
| `opaque_gain` | opus-5-5 | mcponly | 3/3 | 110 | 51 | 43 | 0.51 |
| `opaque_gain` | sonnet-5-5 | shell | 1/1 | 168 | 8 | 0 | 0.13 |
| `opaque_gain` | sonnet-5-5 | mcponly | 1/1 | 63 | 30 | 21 | 0.15 |
| `opaque_gain` | haiku-5-5 | shell | 1/2 | 706 | 36 | 0 | 0.05 |
| `opaque_gain` | haiku-5-5 | mcponly | 2/2 | 134 | 64 | 51 | 0.03 |
| `firmware_blob` | opus-5-5 | shell | 3/3 | 307 | 16 | 0 | 0.44 |
| `firmware_blob` | opus-5-5 | mcponly | 3/3 | 175 | 28 | 19 | 0.54 |
| `firmware_blob` | sonnet-5-5 | shell | 1/1 | 552 | 23 | 0 | 0.25 |
| `firmware_blob` | sonnet-5-5 | mcponly | 1/1 | 86 | 12 | 3 | 0.14 |
| `firmware_blob` | haiku-5-5 | shell | 2/2 | 448 | 27 | 0 | 0.03 |
| `firmware_blob` | haiku-5-5 | mcponly | 1/2 | 218 | 32 | 23 | 0.03 |
| `stale_regs` | opus-5-5 | shell | 3/3 | 24 | 4 | 0 | 0.14 |
| `stale_regs` | opus-5-5 | mcponly | 3/3 | 61 | 19 | 8 | 0.29 |
| `stale_regs` | haiku-5-5 | shell | 2/2 | 56 | 9 | 0 | 0.01 |
| `stale_regs` | haiku-5-5 | mcponly | 2/2 | 76 | 20 | 9 | 0.02 |
| `stream_packer` | opus-5-5 | shell | 3/3 | 316 | 12 | 0 | 0.41 |
| `stream_packer` | opus-5-5 | mcponly | 3/3 | 63 | 16 | 10 | 0.34 |

### What the transcripts show

- **The MCP alone is enough.** With only `litex_mcp`, Opus, Sonnet and Haiku solved the board task.
  The agent read the IP ID, swept the registers with 30 to 70 single reads and writes, fixed the
  driver, and checked the fix through the bus.
- **The two models differ.** Opus and Sonnet pass in both conditions. Haiku passed 7 of 8 runs
  with MCP only and 5 of 8 with a shell. On the two scaler IP tasks it passed 4 of 4 with MCP only
  and 1 of 4 with a shell.
  - Every Haiku failure in the shell condition fixed the gain format. It then concluded that the
    output clamp was a hard limit of the IP.
  - The MCP-only runs probed registers one at a time. They noticed that the "reserved" register
    read back the clamp value, and fixed it.
  - These are 2 runs per condition: suggestive, not conclusive.
- **Wall time mostly reflects how much the agent verified.** Shell agents run the host
  application end to end over a slow UART bridge, and several sat in two-minute commands.
  MCP-only agents cannot run it, so they check registers instead.
- **MCP-only takes many more turns:** one register per call.
- **A gap was found.** `litex_build_start` always added `--build`, so MCP-only agents could not
  restart a project's own simulation script.
  - `stream_packer` was fixed without being re-run in 3 of 3 runs. One Opus and one Sonnet `firmware_blob` run were also
    left unverified.
  - The Haiku `firmware_blob` failure is an unverified fix that does not elaborate (overlapping CSR
    fields).
  - Two Opus runs worked around the gap by adding a `--build` option to the script.
  - Fixed in [litex#2743](https://github.com/enjoy-digital/litex/pull/2743)
    (`litex_build_start(..., build=False)`).

## Round 4: `litex_register_sequence`, and a planner delegating to a bench operator

Same bench setup as round 3. Two changes:

- `litex_mcp` now has `litex_register_sequence` (writes, reads, polls and waits in one call, optionally
  repeated over a sweep) and `litex_build_start(..., build=False)` (run a project's own script).
- New condition `delegate`. The planner (Opus) has the file tools and the `Agent` tool, no shell and
  no direct MCP access. The bench is only reachable through a `bench-operator` subagent (Haiku) that
  has only the `litex_mcp` tools. A PreToolUse hook denies MCP calls that do not come from the
  operator, so the split is enforced, not just requested.

`Seq` is the mean number of `litex_register_sequence` calls (planner and operator).

| Task | Model | Condition | Pass | Wall | Turns | MCP | Seq | Cost |
|---|---|---|---|---|---|---|---|---|
| `ecpix5_scaler` (board) | opus-5-5 | delegate | 2/2 | 136 | 16 | 22 | 20 | 0.56 |
| `ecpix5_scaler` (board) | opus-5-5 | mcponly | 2/2 | 100 | 14 | 6 | 4 | 0.47 |
| `ecpix5_scaler` (board) | opus-5-5 | shell | 2/2 | 442 | 10 | 0 | 0 | 0.34 |
| `ecpix5_scaler` (board) | haiku-5-5 | mcponly | 1/2 | 140 | 35 | 26 | 4 | 0.03 |
| `ecpix5_scaler` (board) | haiku-5-5 | shell | 2/2 | 398 | 18 | 0 | 0 | 0.03 |
| `opaque_gain` | opus-5-5 | delegate | 2/2 | 309 | 12 | 75 | 22 | 0.43 |
| `opaque_gain` | opus-5-5 | mcponly | 2/2 | 85 | 16 | 8 | 5 | 0.37 |
| `opaque_gain` | opus-5-5 | shell | 2/2 | 933 | 20 | 0 | 0 | 0.65 |
| `opaque_gain` | haiku-5-5 | mcponly | 2/2 | 114 | 77 | 65 | 0 | 0.03 |
| `opaque_gain` | haiku-5-5 | shell | 2/2 | 1636 | 37 | 0 | 0 | 0.17 |
| `firmware_blob` | opus-5-5 | delegate | 1/2 | 900 | 12 | 18 | 2 | 0.75 |
| `firmware_blob` | opus-5-5 | mcponly | 2/2 | 163 | 24 | 17 | 0 | 0.44 |
| `firmware_blob` | opus-5-5 | shell | 2/2 | 575 | 20 | 0 | 0 | 0.49 |
| `firmware_blob` | haiku-5-5 | mcponly | 1/2 | 298 | 32 | 22 | 0 | 0.04 |
| `firmware_blob` | haiku-5-5 | shell | 2/2 | 680 | 26 | 0 | 0 | 0.03 |
| `stream_packer` | opus-5-5 | delegate | 2/2 | 718 | 8 | 16 | 4 | 0.28 |
| `stream_packer` | opus-5-5 | mcponly | 2/2 | 105 | 24 | 16 | 1 | 0.39 |
| `stream_packer` | opus-5-5 | shell | 2/2 | 592 | 14 | 0 | 0 | 0.40 |
| `stream_packer` | haiku-5-5 | mcponly | 2/2 | 62 | 22 | 13 | 0 | 0.01 |
| `stream_packer` | haiku-5-5 | shell | 2/2 | 121 | 19 | 0 | 0 | 0.02 |

Totals over the 4 tasks (8 runs each): Opus shell 8/8, mean $0.47, median wall 575 s. Opus MCP only
8/8, $0.42, 103 s. Opus delegate 7/8, $0.51, 562 s. Haiku shell 8/8, $0.07, 398 s. Haiku MCP only
6/8, $0.03, 114 s.

### What the transcripts show

- **`litex_register_sequence` cut the call count where there is a sweep.** Opus with MCP only used it in
  6 of 8 runs. On the board task, MCP calls per run went from 34 (round 3) to 6, and turns from 43 to
  14. On `opaque_gain`, MCP calls went from 43 to 8 and turns from 51 to 16. The cost moved less
  (board: $0.45 to $0.47; `opaque_gain`: $0.51 to $0.37), because most of the tokens go to reading the
  sources and reasoning, not to register traffic.
- **`build=False` closed the verification gap.** All 4 Opus MCP-only runs of `firmware_blob` and
  `stream_packer` restarted the project's simulation and checked the fix. In round 3, 3 of 3
  `stream_packer` runs were left unverified.
- **Haiku used the new tool only when told about it.** On its own, Haiku called
  `litex_register_sequence` in 1 of 8 runs. As the bench operator, whose prompt names the tool, it
  used it in every run that had a sweep (up to 30 calls in one run).
- **The round 3 Haiku result did not hold.** This round, Haiku passed 8 of 8 with a shell and 6 of 8 with
  MCP only. Over rounds 3 and 4, both conditions are at 13 of 16. The MCP-only board failure is the
  round 3 shell failure: the agent fixed the gain format, then concluded that the output clamp was a
  limit of the IP. The other failure (`firmware_blob`) diagnosed the fault correctly on the bench, but
  without a shell the agent could not read the firmware's bit layout, and it stopped.
- **Delegation worked, but it did not save anything on these tasks.**
  - The planner wrote precise requests: "write these registers, poll this status, read these, for
    these 6 configurations", and the operator answered with tables. The hook denied no MCP call
    from the planner, because none was attempted.
  - The operator cost $0.003 to $0.08 per run. The planner was 96% of the cost: the planner's
    reading and reasoning, not the bench work, is the bulk of the cost, so moving the bench work to a
    cheaper model changes little.
  - Wall time was longer. The operator waited on the wrong pattern while a rebuilt simulation was
    starting (up to 600 s), and the planner sat idle until the operator returned.
  - The `firmware_blob` failure is about the planner having no shell. It needed to disassemble the
    firmware, tried to get a general-purpose subagent to do it (no shell there either), then asked the
    operator to build a diagnostic SoC. The run ended while it was waiting.
- **Opus with a shell is still fine.** 8 of 8, at a similar cost. The shell runs are slower because they
  run the host application end to end over the UART bridge.

These are 2 runs per condition. Read the differences as indications, not measurements.
