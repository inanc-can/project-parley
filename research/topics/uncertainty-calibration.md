# Uncertainty and calibration

Can LLMs tell how sure they should be, and do they act on it? Added 2026-11-20 after finding that
TERMS-Bench models ignore probabilities about the opponent ([[zhang2026terms]]). Two layers keep
coming up: **knowing** a probability (calibration, about one's own answers) and **using** one to
decide (about the world or another agent). The literature is strong on the first and thin on the
second.

**Knowing (own answers)**
- [[kadavath2022mostly]]: large pretrained models are well calibrated on multiple choice and can
  judge their own answers few-shot; trained "do I know this?" transfers to new tasks in ranking
  but not in calibration. (read: partial)
- [[lin2022teaching]]: fine-tuned GPT-3 states calibrated confidence in words and partly keeps it
  under distribution shift; the signal was already in pretrained representations. (read: partial)
- [[tian2023just]]: RLHF worsens token-probability calibration; just asking RLHF models for a
  number is better calibrated, more so after listing alternatives. (read: full)
- [[xiong2023llms]]: stated confidence is overconfident (80–100%, multiples of 5); low ECE can hide
  near-chance ability to tell right from wrong (GPT-4 AUROC 62.7%). (read: partial)
- [[kalai2025hallucinate]]: calibrated base models must err; 0–1 benchmarks reward guessing over
  "I don't know", so post-training keeps confident errors. (read: partial)

**Using (deciding and updating about others)**
- [[liu2024dellma]]: forecasts are fairly calibrated, yet plain prompting picks worse than random on
  larger choice sets; a posterior in the prompt doesn't help; computing expected utility outside
  the model does. (read: partial)
- [[qiu2025bayesian]]: LLMs barely update beliefs about a user over rounds; fine-tuning on a
  Bayesian model's guesses fixes much of it and transfers to new tasks, beating training on the
  right answers. (read: partial)
- [[zhang2026terms]]: in negotiation, a posterior about the opponent closes ~1% of the gap; belief
  error flat over rounds. (read: partial)

**Pattern for the research question ([[gap]])**: the "using" layer fails across settings
(negotiation, single-agent decisions, preference inference) and does not improve much with scale,
but [[qiu2025bayesian]] shows it can be trained and transfers. Whether that training carries into
adversarial, strategic settings is untested.
