# Results

Per-run results of the first evaluation rounds (2026-11-03), one CSV per round:
`round`, `task`, `model`, `condition`, `run`, `passed`, `wall_s`, `turns`, `mcp_calls`,
`shell_calls`, `other_calls`, `cost_usd`.

- Agent: Claude Code, headless (`claude -p`), stream-json transcripts. The transcripts are not
  published, because they contain local paths.
- Models: Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5.
- LiteX: master of 2026-11-03 plus the `litex_mcp` fixes of
  [litex#2743](https://github.com/enjoy-digital/litex/pull/2743).
- `cost_usd` is the cost reported by the agent (list prices). It is blank for 2 runs that ended
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
