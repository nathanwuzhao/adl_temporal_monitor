# adl-temporal-monitor

a research prototype exploring the use of **temporal logic** (specifically Linear Temporal Logic (LTL) and Signal Temporal Logic (STL)) as a formal monitoring layer for assistive systems that support people with cognitive impairments in completing Activities of Daily Living (ADLs).

## motivation

existing assistive cooking systems (e.g., Cueing Kitchen) provide structured cues to guide users through task steps. recent vision-language models (e.g., CHEF-VL) enable richer perceptual understanding of kitchen activities. can formal temporal specifications bridge these two worlds, providing verifiable, explainable, and proactive cue generation grounded in what the system actually observes?

## core idea

recipe tasks can be expressed as temporal logic specifications:
- **LTL** captures discrete step structure (ordering constraints, preconditions, skip detection)
- **STL** captures continuous signals (time-on-task, quantity, physical state)

a runtime monitor evaluates these specs against a stream of perceptual observations. when a specification's **robustness margin**, a real-valued measure of how close the system is to a violation, falls below a threshold, a cue is triggered. This enables *proactive* intervention before failure, not just reactive response after it.

## structure

```
src/adl_monitor/
├── types.py         # core data types and proposition vocabulary
├── spec.py          # recipe specification schema
├── ltl_monitor.py   # discrete step/ordering monitor
├── stl_monitor.py   # continuous signal monitor (STL robustness)
└── demo_specs.py    # example formal specs for simple recipes

experiments/
└── run_demo.py      # end-to-end demo pipeline

tests/               # unit tests for monitor logic
```

## related work

- Harshal P. Mahajan et al., Cueing Kitchen — University of Pittsburgh HERL
- Ruiqi Wang et al., CHEF-VL — Washington University in St. Louis
- RTAMT — runtime monitoring library for STL

## License

MIT