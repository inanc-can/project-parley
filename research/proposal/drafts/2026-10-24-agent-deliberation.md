# Research direction: what two agents concluded (2026-10-24)

A 12-turn Parley talk (room `7e34de26`, match `4120aa6c9253`) between Claude Code and Grok
(grok.com, via the MCP connector). Both spoke for İnanç, with the same brief and free turn-taking.
It ended with Grok accepting the written recommendation below. Claude checked the citations
Grok brought in during the talk; what was verified and what wasn't is marked at the end.

## The recommendation, as agreed

**Direction: concede vs disclose.** A delegated agent can betray its principal in two ways: it
*concedes* (is persuaded past its limit) or it *discloses* (gives away the private information
behind the limit). Measure both in money against frozen adversary agents, and test which defences
prevent each. This keeps the money measure from [[gap]], makes defences the contribution rather
than a tactics grid, and prices the leakage that recent work only counts.

- Fallbacks: loyalty defences alone, or leakage alone. Lower: capability gaps between delegates
  (Horton, Manning and the Digital Economy Lab already hold this ground) and debate for oversight
  (crowded, compute-heavy).
- **Design, for a six-month master's thesis:**
  - One bilateral buy-sell domain with a private reservation value and soft preferences.
  - 3 to 4 target models, including mid-size open models.
  - 2 to 3 frozen adversaries: extraction, persuasion and hybrid.
  - 2 to 3 defences: a private note with forced restatement, a hard rule versus a soft
    preference, and a reasoning or commitment step.
- **Measures:**
  - Concession: money given up past the reservation.
  - Disclosure: how much a fixed estimator's error on the reservation shrinks after reading the
    transcript, priced as the extra surplus the adversary captures. Validate the estimator by
    hand on a sample.
- **Hosts, one project pitched three ways:**
  - [[pentland]] and the Loyal Agents team (Pei, South) at Stanford DEL, with results first:
    extend their public A2A-NT setup in Parley.
  - [[hadfield-menell]] at MIT, framed as incomplete contracting and defence mechanisms.
  - [[song]] or [[klein]] at Berkeley, only with the disclosure and security half in front.
  - De-prioritised: [[zou]] (negotiation diagnostics are already his group's) and [[horton]] /
    [[manning]] (surplus and strategy differences).
- **Risks:**
  - The effect collapses into "models follow instructions badly". Report each condition as the
    difference from that model's own neutral control; the baseline must be stable and below its
    ceiling, not zero.
  - Null results on well-defended frontier models. Frame them as "which defences close the gap,
    for which model sizes".
  - Estimator noise.
  - Results ageing with model releases: freeze model versions and release the Parley configs.
- **Still disputed:**
  - Founder value. Grok: the edge is infrastructure, licensable to platforms. Claude: the edge
    is position, being the person with the loyalty numbers inside the network where Visa,
    Anthropic, OpenAI and Consumer Reports already meet. Both agree an audit tool alone is a
    feature, not a company.
  - Strong models with hard limits (Grok) versus including mid-size models (Claude). Settle it
    with the pilot.

## Next two weeks
1. Read in full and write notes (all are in `inbox.md`): The Automated but Risky Game, AgentLeak,
   the Interlocutor Effect, "Got a Secret", Strategic Tradeoffs (Horton/Manning) and TERMS-Bench.
2. Parley: buy-sell with a private reservation and soft preferences, a disclosure estimator and
   frozen adversaries.
3. Reproduce a slice of A2A-NT, or at least a neutral baseline.
4. Pilot: 2 models × 2 adversaries × a control, with and without one defence.
5. Write a one-page proposal and a 2-minute demo; send tailored emails to Pei/South,
   Hadfield-Menell and a third host.
6. Check the practicalities: a TUM supervisor for an external thesis, funding, and visa
   sponsorship by the host.

## What was checked

**Verified by web search during the talk:**
- The Interlocutor Effect (arXiv 2606.09844; Polytechnique Montréal, not Berkeley as Grok said).
  Up to +23 points of PII leakage when the recipient is framed as an AI agent. A reviewer flags
  a possible prompt-wording confound.
- AgentLeak (2602.11510; same group). 68.8% leakage in inter-agent messages, limited to a
  coordinator-worker setting.
- "Got a Secret? LLM Agents Can't Keep It" (2605.27766): exists; not read.
- Strategic Tradeoffs Between Humans and AI in Multi-Agent Bargaining (2509.09071; Horton,
  Manning et al., IUI 2026). LLMs make conservative, concession-heavy offers.
- The Automated but Risky Game (2506.00073; Zhu, Sun, Nian, South, Pentland, Pei). Code is
  public as A2A-NT. Stanford HAI's coverage reports buyers with weaker agents paying about 2%
  more.
- Loyal Agents is a live Consumer Reports and Stanford DEL collaboration. Its research-assistant
  roles are for Stanford students only, and no visiting-student programme was found.

**Said by Grok but not verified:**
- TERMS-Bench's content and its link to Zou's group.
- Diyi Yang's 2026 papers (emergent collusion, DECEPTICON).
- Dawn Song's group's openings form and its past visiting students.
- The "~20%" desperation effect in NegotiationArena; [[bianchi2024negotiationarena]] is not
  `read: full` yet.

## Notes on the method
- What the second agent added: live search of the hosts' 2026 work, and a host ranking from a
  founder's lens. The synthesis (concede vs disclose, leakage priced in money) came from the
  exchange; neither side opened with it.
- What needed a human-like check: a misattributed affiliation, and a host-access claim that
  turned out stricter than stated. Agent output needs verification before it goes into a
  proposal.
- Weak points:
  - Both agents served the same person and converged within 7 turns. The disagreements survived
    only because they were written into the agreement on purpose.
  - Grok twice missed that the standing offer was Claude's and asked Claude to accept it.
  - Parley should state the offer's author and how to accept it more clearly in each turn.
