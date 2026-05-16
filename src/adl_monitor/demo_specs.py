from adl_monitor.spec import ADLSpec, LTLRule, STLRule

BOIL_WATER_SPEC = ADLSpec(
    name="boil_water",
    description="toy ADL spec for boiling water on a stove",
    propositions=(
        "water_added",
        "pot_on_stove",
        "stove_on",
        "boiling",
        "user_interacting",
        "task_complete",
    ),
    signals=(
        "temperature_c",
    ),
    ltl_rules=(
        LTLRule(
            name="stove_requires_water",
            kind="precedence",
            before="water_added",
            after="stove_on",
            severity="error",
            description="water should be added before the stove is turned on",
        ),
        LTLRule(
            name="stove_requires_pot",
            kind="safety",
            forbidden=("stove_on", "pot_absent"),
            severity="critical",
            description="stove should not be on while the pot is absent",
        ),
        LTLRule(
            name="eventually_boiling",
            kind="eventually",
            target="boiling",
            severity="warning",
            description="water should eventually boil",
        ),
    ),
    stl_rules=(
        STLRule(
            name="boil_within_5_minutes",
            kind="eventually_within",
            trigger="stove_on",
            target="boiling",
            horizon_s=300.0,
            severity="warning",
            description="after the stove is turned on, boiling should occur within 5 minutes",
        ),
    ),
)