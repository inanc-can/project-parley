# Negotiation benchmarks for LLM agents

Platforms and benchmarks where LLM agents negotiate. The space is crowded: Parley's contribution
cannot be "a negotiation platform" (see [[gap]]).

- [[lewis2017deal]]: pre-LLM item split with a human dialogue dataset (human baseline).
- [[abdelnabi2023cooperation]]: multi-party, multi-issue, with greedy and saboteur variants.
- [[bianchi2024negotiationarena]]: two-agent games; tactics such as desperation change payouts.
- [[liu2026agenticpay]]: 110+ buyer–seller tasks up to many-to-many markets.
- [[zhang2026terms]]: TERMS-Bench, a scripted counterpart with a hidden type as verifier; deal rate
  saturates while surplus, cue use and belief accuracy diverge.
- [[zhu2025automated]]: delegated buyer/seller agents break budgets, sell below cost, reveal
  budgets and overpay; stronger models win.
- [[liu2026instructing]]: RL with a verifiable surplus reward trains a 30B buyer that beats
  frontier models and resists begging/insulting/stubborn sellers.
- [[micelibarone2026used]]: honesty and credulity under information asymmetry.
- [[sadab2026receiver]]: agent-to-agent resource extraction; the holder decides.
- [[he2026socialgym]]: 22 verifiable social games incl. bargaining; negotiation coverage thin.
- [[wang2024sotopia]]: SOTOPIA-π; fine-tuning a 7B model on a broad mix of social tasks raises
  goal completion to GPT-4's judge level, but humans see a much smaller gain.
- [[liu2025spiral]]: self-play on three zero-sum games (incl. negotiation) improves reasoning;
  the multi-game model is worse at negotiation than the negotiation specialist.
- [[bergemann2026training]]: 15,000-negotiation round robin with binding tool-call offers; o3
  pushes weaker sellers past their limits; SFT then GRPO training of Qwen3.
- [[liang2026agents]]: nine models vs a Perfect Bayesian Equilibrium benchmark; delay costs
  21–34% of surplus; limit breaches mostly in weak non-reasoning models.
- [[juneja2025magpie]]: multi-party cooperative negotiation; 25–61% private-information leakage.
- [[erdogan2026should]]: trade, bargaining and double auctions under least / coarse / full
  disclosure; more information helps some models and destroys value for others.

In `inbox.md`: Davidson et al. (faithfulness metrics), Simchi-Levi's multi-buyer paper, MERIT,
PieArena.

## Added 2026-11-15 (map batch)
- [[xia2024measuring]]: AmazonHistoryPrice bargaining; every LLM buyer loses money vs a gpt-3.5 seller.
- [[davidson2024evaluating]]: LAMEN; cooperative (integrative) bargaining is hardest; faithfulness metric.
- [[oh2026merit]]: MERIT/AgoraBench; human-fitted buyer utility; SFT transfer across market types.
- [[zhu2026piearena]]: MBA negotiation cases vs business students; lying raises share; rankings flip single vs multi-issue.
- [[vaccaro2025advancing]]: 182,812 negotiations from 286 human-written prompts; warmth vs dominance.
- [[shapira2024glee]]: GLEE; bargaining, negotiation and persuasion games with 3,405 humans.
- [[bansal2025magentic]]: Magentic Marketplace; first-offer bias, manipulation susceptibility in delegated buying.
- [[chen2023your]]: AucArena; ascending auctions; a rule bidder beats most LLMs.
- [[zheng2026market]]: Market-Bench; 20 LLM retailers; profit driven by procurement, not slogans.
- [[backlund2025vending]]: Vending-Bench; long-horizon coherence running a vending business.
- [[fan2026commerce]]: E-Commerce Bench; 365-day store operation with fraudulent suppliers.
- [[wu2026measuring]]: Collaborative Intelligence Benchmark ("CIB", Zou lab); conflict handling opposes the other 7 dimensions.
- [[hua2026passive]]: SocialRL; RL transfer matrix across six negotiation domains; structure predicts transfer, some pairs hurt.
- [[vendrell2026gametalk]]: GameTalk; GRPO/DPO/STaR for strategic dialogue in 3 games; DPO learns to argue high while undercutting.
