# Chapter 13. Agent Security: Prompt Injection, Sandboxes and Capability Boundaries

> Chapter focus: treat agent security as a system problem involving exploit-like prompt injection, capability boundaries and sandboxing, not merely as prompt wording.

## 13.1 The Question

Agent security cannot rely on prompts such as "please do not leak secrets." Once an agent is connected to files, browsers, mail, code execution, databases and external APIs, model output can become real side effects. An attacker may not need to break into the server. They may only need the agent to read malicious text.

Karpathy has used the LLM OS analogy in public discussions. If that analogy is taken seriously, the security model migrates too: prompt injection is closer to an exploit than to persuasion. Sandboxes, permissions, isolation, audit and least privilege become infrastructure for agent systems.

This chapter discusses the engineering boundary for agent security.

## 13.2 Prompt Injection as Input-Driven Exploit

Prompt injection is dangerous because it confuses data with instructions. Web pages, emails, documents, issues, code comments and logs are supposed to be data read by the agent, but they may contain malicious text such as "ignore previous instructions," "send the secret," or "call this tool."

In traditional systems, treating untrusted input as executable code is a classic vulnerability. In agent systems, treating untrusted text as high-priority instruction is a similar vulnerability.

The security question is therefore not only "will the model obey?" It is: where did this content come from, is it trusted, which decisions may it influence and can it trigger tool calls?

## 13.3 Instruction Levels and Data Labels

Agents need to distinguish content sources explicitly.

| Source | Trust Level | What It May Do |
| --- | --- | --- |
| System policy | Highest | Define non-bypassable rules |
| Developer instruction | High | Define application behavior and tool boundaries |
| User request | Medium | Define the current task goal |
| Project rule | Medium | Constrain execution inside the project |
| External content | Low | Act as data only, never elevate privilege |
| Tool result | Depends on tool | Preserve source and permission labels |

The context builder should preserve source labels. The model should not receive everything as one undifferentiated block of text. If an external web page and a system instruction both appear as natural language in the same context, the security boundary becomes blurry.

## 13.4 Capability Boundaries

Tool permission should be an explicit capability, not an all-powerful switch.

An agent that can read files should not automatically write files. An agent that can create an email draft should not automatically send it. An agent that can query a database should not automatically run migrations. An agent that can run tests should not automatically access production secrets.

Capability boundaries should be split by tool, resource, operation and parameter constraints:

- Files: read-only, write workspace, forbid system directories.
- Network: allow listed domains, forbid arbitrary outbound access.
- Shell: allow tests, forbid deletion or upload.
- Mail: allow drafts, require confirmation to send.
- Database: allow query, require transaction and audit for writes.

Prompts describe intent. The runtime must enforce the boundary.

## 13.5 Sandboxes

A sandbox is the default execution environment for agent safety. Code execution, shell commands, browser automation, file writes and external API calls should run inside constrained environments.

At minimum, a sandbox should limit the filesystem, network, environment variables, processes, time, memory and output size. High-risk tools also need audit logs and human confirmation.

This is not accidental complexity. Agents read untrusted content and turn model output into tool parameters. If one prompt injection succeeds and there is no sandbox, the attack becomes a real side effect.

## 13.6 Policy and User Confirmation

More confirmation dialogs do not automatically mean more safety. Confirmation should happen at meaningful boundaries: external side effects, high-risk writes, privilege escalation, sensitive data access, cross-tenant resources and irreversible operations.

The confirmation content should be structured. The system should show the tool to be called, the target resource, key parameters, risk level and rollback path instead of only asking "continue?"

The agent policy engine should classify operations as allow, require confirmation, require approval or deny. The model may request an action, but it must not grant itself more privilege.

## 13.7 Audit and Incident Analysis

Security incidents must be replayable. The system needs to record which untrusted content the agent read, how it entered context, what tool call the model proposed, why the runtime allowed or denied it and whether the user confirmed.

Without audit, a prompt injection incident becomes an unreproducible chat fragment. Security systems need to turn it into an analyzable execution chain.

## 13.8 Summary

This chapter placed agent security inside an OS security frame. Prompt injection is closer to an input-driven exploit. External content needs source and permission labels. Tool capability needs explicit boundaries. Code and external-system access need sandboxes. High-risk operations need structured confirmation and audit.

At this point, the book has covered the core surfaces of agent systems: context, storage, tools, planning, cost, reliability, scheduling and security. The final chapter brings these components back into the larger picture of an Agent Operating System.
