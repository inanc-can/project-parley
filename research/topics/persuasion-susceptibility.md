# What persuades an LLM

Research on what changes a model's answer, stance or compliance. Almost all of it measures
opinion or compliance, mostly in single turns, without stakes: the opening for [[gap]].

Notes (agent-to-agent, with stakes):

- [[sadab2026receiver]]: donation-extraction round robin; the holder's identity explains ~47% of
  outcome variance, the persuader's ~2%; persuasion fine-tuning erodes resistance, distillation
  installs it.
- [[li2026whose]]: PrincipalBench; agents acting for a principal leak, capitulate or over-refuse;
  a leak/over-refusal frontier that prompting, distillation and RL don't cross.
- [[micelibarone2026used]]: informed bargainers mislead, uninformed ones are credulous; RL for
  profit lowers honesty.

- [[sakhawat2026areg]]: the original AREG game; every model resists better than it persuades;
  small-step asks extract far more than one ask (correlational).
- [[bozdag2025persuade]]: multi-turn LLM-vs-LLM persuasion on opinions and false trivia; free
  persuaders almost never use deception or pressure, so such tactics must be scripted.
- [[zeng2024johnny]]: 40-technique persuasion taxonomy (jailbreaks); uneven technique effects;
  "not easily persuaded" system prompt cuts GPT-4 success 92% → 38%.
- [[sharma2023understanding]]: sycophancy; one content-free "Are you sure?" flips correct
  answers on 32–86% of questions.
- [[wan2024evidence]]: models weigh apparent relevance, not credibility cues.
- [[wallace2024instruction]]: training a privilege hierarchy beats stating it in a prompt.
- [[jose2026agents]]: persuasion generation; ORPO/SFT/DPO cut propaganda, prompting doesn't.

Still in `inbox.md`: Meincke et al. "Call Me A Jerk" (Cialdini principles), "Understanding
Persuasion in Long-Running Agents", anchoring in price negotiation (EMNLP Findings 2025). NegotiationArena's tactic findings: [[bianchi2024negotiationarena]].
- [[openai2023makemepay]]: MakeMePay; con-artist vs mark, OpenAI evals (no published numbers in repo).
- [[gajewska2026benchmarking]]: LLM replies to ad hominem attacks; counterattack far less than humans.
- [[taylor2026clocktower]]: persuasion and deception in social deduction.
- [[sarkar2025training]]: speaking reward = how far a message moves teammates' beliefs; crewmates learn to fabricate evidence.
