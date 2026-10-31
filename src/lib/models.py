# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 hour
# DESCRIPTION  : One interface for every model call in the test bed, so that a structure can be rerun with a
#                different model by changing a model string. Two kinds of call:
#                  text_call  - one prompt in, one text answer out, no tools (ledger task);
#                  agent_call - a session in a working folder where the model may list, read and write files
#                               and run Python scripts, ending when it writes its decision file (report task).
#                Model strings are "<provider>:<model name>":
#                  claude-cli:<name>  Claude Code command-line client (the client used for the reference runs;
#                                     a bare name such as "claude-sonnet-5-5" means this provider)
#                  anthropic:<name>   Anthropic Messages API, key in ANTHROPIC_API_KEY (ANTHROPIC_BASE_URL optional)
#                  openai:<name>      any OpenAI-compatible chat endpoint: OpenAI, or an open-weight model served
#                                     locally by vLLM, Ollama, LM Studio or llama.cpp. Base URL in
#                                     OPENAI_BASE_URL (default https://api.openai.com/v1), key in OPENAI_API_KEY
#                                     (any string for local servers)
#                  mock:<anything>    no model; deterministic stand-in answers for pipeline tests
# INPUT FILES  : environment variables named above
# OUTPUT FILES : agent transcripts (JSON lines) at the path the caller gives
# ============================================================
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from . import paths

# ★ IMPORTANT: the reference runs used Claude Code CLI 2.0.43 with exactly these flags. Each text call ran in an
# empty folder with no tools and no settings files, so nothing but the prompt reached the model.
CLI_TEXT_FLAGS = ["--setting-sources", "", "--tools", ""]
CLI_AGENT_TOOLS = "Bash Read Write Edit Glob"
CLI_AGENT_ALLOWED = "Bash(python3:*) Bash(ls:*) Bash(head:*) Bash(cat:*) Bash(wc:*) Read Write Edit Glob"
MAX_TOKENS = int(os.environ.get("EVALBED_MAX_TOKENS", "16000"))
_EMPTY = None


def parse_model(spec):
    if ":" in spec and spec.split(":", 1)[0] in ("claude-cli", "anthropic", "openai", "mock"):
        prov, name = spec.split(":", 1)
        return prov, name
    return "claude-cli", spec


def model_name(spec):
    return parse_model(spec)[1]


def empty_cwd():
    """A fresh empty folder for text calls, so no project file can reach the model."""
    global _EMPTY
    if _EMPTY is None:
        _EMPTY = Path(tempfile.mkdtemp(prefix="evalbed_empty_"))
    assert not any(_EMPTY.iterdir()), "the model's working folder must stay empty"
    return _EMPTY


def claude_bin():
    b = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if not b:
        raise RuntimeError("Claude Code CLI not found; install it or set CLAUDE_BIN")
    return b


def _post(url, body, headers, timeout=900):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _anthropic_headers():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("set ANTHROPIC_API_KEY")
    return {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}


def _anthropic_url():
    return os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/") + "/v1/messages"


def _openai_url():
    return os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"


def _openai_headers():
    return {"Authorization": "Bearer " + os.environ.get("OPENAI_API_KEY", "none"), "content-type": "application/json"}


# ---------------------------------------------------------------------------------------------------------
# Text calls
# ---------------------------------------------------------------------------------------------------------
def _mock_text(prompt):
    """Pipeline test only: a reviewer that changes nothing, or an author that writes an empty ledger."""
    if "Return your changes only" in prompt or "ROWS IN DISPUTE" in prompt:
        return "row,action,doc_ids,date,account,pay,amount\n"
    return "doc_ids,date,account,pay,amount,confidence\n"


# ★ KEY FUNCTION: one text call. CLI errors are retried twice; a well-formed but wrong answer is never retried.
def text_call(prompt, spec):
    """Returns (text, meta). meta has cost_usd (as reported by the client; 0 when unknown), model_used and
    attempts."""
    prov, name = parse_model(spec)
    if prov == "mock":
        return _mock_text(prompt), dict(model_used=["mock"], cost_usd=0.0, attempts=1)
    last = ""
    for attempt in range(1, 4):
        try:
            if prov == "claude-cli":
                r = subprocess.run([claude_bin(), "-p", prompt] + CLI_TEXT_FLAGS + ["--model", name,
                                   "--output-format", "json"], cwd=empty_cwd(), capture_output=True, text=True,
                                   timeout=900)
                d = json.loads(r.stdout)
                if r.returncode == 0 and not d.get("is_error"):
                    # The CLI also makes small auxiliary calls on other models; keep tokens per model so a reader
                    # can see that the answer itself came from the requested model.
                    usage = {m: dict(input=u.get("inputTokens"), output=u.get("outputTokens"),
                                     cache_read=u.get("cacheReadInputTokens"))
                             for m, u in (d.get("modelUsage") or {}).items()}
                    return d.get("result") or "", dict(model_used=list(usage), model_usage=usage,
                                                       cost_usd=float(d.get("total_cost_usd") or 0.0), attempts=attempt)
                last = (d.get("result") or r.stderr or "")[:300]
            elif prov == "anthropic":
                d = _post(_anthropic_url(),
                          dict(model=name, max_tokens=MAX_TOKENS, messages=[dict(role="user", content=prompt)]),
                          _anthropic_headers())
                text = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
                return text, dict(model_used=[d.get("model", name)], usage=d.get("usage"), cost_usd=0.0, attempts=attempt)
            elif prov == "openai":
                d = _post(_openai_url(), dict(model=name, messages=[dict(role="user", content=prompt)]), _openai_headers())
                text = d["choices"][0]["message"].get("content") or ""
                return text, dict(model_used=[d.get("model", name)], usage=d.get("usage"), cost_usd=0.0, attempts=attempt)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError, KeyError) as e:
            last = repr(e)[:300]
        time.sleep(10 * attempt)
    raise RuntimeError(f"model call failed 3 times: {last}")


# ---------------------------------------------------------------------------------------------------------
# Agent calls (report task)
# ---------------------------------------------------------------------------------------------------------
def agent_env(cwd):
    """Environment for code the model runs: this interpreter first on PATH, the fit logger on PYTHONPATH."""
    env = dict(os.environ)
    py_dir = os.path.dirname(sys.executable)
    env.update({"PATH": py_dir + os.pathsep + "/usr/bin:/bin:/usr/sbin:/sbin" + os.pathsep + env.get("PATH", ""),
                "PYTHONPATH": str(paths.INSTRUMENT), "ORGEVAL_LOG": os.path.join(cwd, "_fits.jsonl"),
                "MPLBACKEND": "Agg"})
    return env


def _cli_agent(cwd, system, prompt, name, log_path, resume, timeout):
    cmd = [claude_bin(), "-p", prompt, "--setting-sources", "", "--tools", CLI_AGENT_TOOLS, "--allowedTools",
           CLI_AGENT_ALLOWED, "--permission-mode", "dontAsk", "--model", name, "--output-format", "stream-json",
           "--verbose"]
    cmd += ["--resume", resume] if resume else ["--system-prompt", system]
    # ★ IMPORTANT: stream the transcript straight to disk so an interrupted call still leaves a record.
    start = os.path.getsize(log_path) if os.path.exists(log_path) else 0
    with open(log_path, "a") as fh:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=fh, stderr=subprocess.DEVNULL, text=True, env=agent_env(cwd))
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    with open(log_path) as fh:
        fh.seek(start)
        out = fh.read()
    final = {}
    for line in out.splitlines():
        try:
            m = json.loads(line)
        except Exception:
            continue
        if m.get("type") == "result":
            final = m
    return final, float(final.get("total_cost_usd") or 0.0), final.get("session_id")


TOOL_SPECS = [
    ("list_files", "List the files in the working folder.", {}),
    ("read_file", "Read a text file in the working folder (first 200,000 characters).", {"path": "string"}),
    ("write_file", "Create or overwrite a file in the working folder.", {"path": "string", "content": "string"}),
    ("run_python", "Run a Python script in the working folder with `python3 <path>` and return its output.",
     {"path": "string"}),
]


def _safe(cwd, rel):
    p = (Path(cwd) / rel).resolve()
    if Path(cwd).resolve() not in p.parents and p != Path(cwd).resolve():
        raise ValueError("path outside the working folder")
    return p


# ★ KEY FUNCTION: the same four capabilities the CLI reviewers had (list, read, write, run Python), offered to
# any model that supports tool calls. Everything happens inside the working folder.
def run_tool(cwd, name, args):
    try:
        if name == "list_files":
            return "\n".join(sorted(os.listdir(cwd)))
        if name == "read_file":
            return _safe(cwd, args["path"]).read_text(errors="replace")[:200_000]
        if name == "write_file":
            _safe(cwd, args["path"]).write_text(args.get("content", ""))
            return "written"
        if name == "run_python":
            f = _safe(cwd, args["path"])
            r = subprocess.run([sys.executable, f.name], cwd=cwd, capture_output=True, text=True, timeout=300,
                               env=agent_env(cwd))
            return ((r.stdout or "") + (r.stderr or ""))[-20_000:] or "(no output)"
        return f"unknown tool {name}"
    except Exception as e:  # tool errors go back to the model as text
        return f"error: {e!r}"[:2000]


def _tool_loop(cwd, system, prompt, prov, name, log_path, max_turns):
    def log(rec):
        with open(log_path, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    log(dict(type="system", subtype="init", provider=prov, model=name, tools=[t[0] for t in TOOL_SPECS]))
    if prov == "anthropic":
        tools = [dict(name=n, description=d, input_schema=dict(type="object", properties={k: {"type": v} for k, v in a.items()},
                                                               required=list(a))) for n, d, a in TOOL_SPECS]
        msgs = [dict(role="user", content=prompt)]
        for turn in range(max_turns):
            d = _post(_anthropic_url(), dict(model=name, max_tokens=MAX_TOKENS, system=system,
                      tools=tools, messages=msgs), _anthropic_headers())
            log(dict(type="assistant", message=d))
            msgs.append(dict(role="assistant", content=d["content"]))
            uses = [b for b in d["content"] if b.get("type") == "tool_use"]
            if not uses:
                break
            results = [dict(type="tool_result", tool_use_id=b["id"], content=run_tool(cwd, b["name"], b.get("input") or {}))
                       for b in uses]
            log(dict(type="user", message=dict(role="user", content=results)))
            msgs.append(dict(role="user", content=results))
    else:
        tools = [dict(type="function", function=dict(name=n, description=d, parameters=dict(
            type="object", properties={k: {"type": v} for k, v in a.items()}, required=list(a)))) for n, d, a in TOOL_SPECS]
        msgs = [dict(role="system", content=system), dict(role="user", content=prompt)]
        for turn in range(max_turns):
            d = _post(_openai_url(), dict(model=name, messages=msgs, tools=tools), _openai_headers())
            m = d["choices"][0]["message"]
            log(dict(type="assistant", message=m, usage=d.get("usage")))
            msgs.append({k: v for k, v in m.items() if k in ("role", "content", "tool_calls")})
            calls = m.get("tool_calls") or []
            if not calls:
                break
            for c in calls:
                try:
                    args = json.loads(c["function"].get("arguments") or "{}")
                except json.JSONDecodeError:
                    args = {}
                res = run_tool(cwd, c["function"]["name"], args)
                log(dict(type="tool", name=c["function"]["name"], args=args, result=res[:5000]))
                msgs.append(dict(role="tool", tool_call_id=c["id"], content=res))
    final = dict(type="result", provider=prov, model=name, turns=turn + 1, total_cost_usd=0.0)
    log(final)
    return final, 0.0, None


def _mock_agent(cwd, prompt, log_path):
    """Pipeline test only: a reviewer that approves, or an analyst that reports no effect."""
    if "verdict.json" in prompt:
        json.dump({"decision": "approve", "reason": "mock"}, open(os.path.join(cwd, "verdict.json"), "w"))
    else:
        json.dump({"conclusion": "no effect"}, open(os.path.join(cwd, "final_answer.json"), "w"))
        open(os.path.join(cwd, "report.md"), "w").write("mock report\n")
    final = dict(type="result", provider="mock", total_cost_usd=0.0)
    with open(log_path, "a") as fh:
        fh.write(json.dumps(final) + "\n")
    return final, 0.0, None


def agent_call(cwd, system, prompt, spec, log_path, resume=None, timeout=1500, max_turns=40):
    """Returns (final result record, cost reported by the client, session id or None, seconds)."""
    prov, name = parse_model(spec)
    t0 = time.time()
    if prov == "claude-cli":
        final, cost, sid = _cli_agent(cwd, system, prompt, name, log_path, resume, timeout)
    elif prov == "mock":
        final, cost, sid = _mock_agent(cwd, prompt, log_path)
    else:
        if resume:
            prompt = "(continuing) " + prompt
        final, cost, sid = _tool_loop(cwd, system, prompt, prov, name, log_path, max_turns)
    return final, cost, sid, time.time() - t0


def read_json(path):
    try:
        return json.load(open(path))
    except Exception:
        return None
