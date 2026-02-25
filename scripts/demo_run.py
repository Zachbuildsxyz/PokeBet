from wysper.config import load_config
from wysper.risk_gate import RiskGate
from wysper.constants import SYSTEM_START, SYSTEM_STOP
from wysper.event_logger import EventLogger


def main():
    cfg = load_config("config.json")  # falls back to defaults if missing
    logger = EventLogger()
    logger.log_event(SYSTEM_START, meta={"dry_run": getattr(cfg, "dry_run", True)})

    gate = RiskGate(cfg)

    # Demo: a candidate entry (paper scenario)
    symbol = "DEMO"
    risk_amount = 0.005
    exposure_amount = 0.05

    approved = gate.evaluate_entry(symbol, risk_amount, exposure_amount)

    logger.log_event(
        "DEMO_RESULT",
        reason="approved" if approved else "blocked",
        symbol=symbol,
        meta={"risk_amount": risk_amount, "exposure_amount": exposure_amount},
    )

    logger.log_event(SYSTEM_STOP)


if __name__ == "__main__":
    main()
