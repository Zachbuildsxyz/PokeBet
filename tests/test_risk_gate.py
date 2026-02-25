from wysper.config import WysperConfig, RiskConfig
from wysper.risk_gate import RiskGate


def _cfg(
    max_risk_per_trade=0.01,
    daily_loss_limit=0.03,
    max_open_positions=3,
    max_total_exposure=0.30,
):
    return WysperConfig(
        dry_run=True,
        risk=RiskConfig(
            max_risk_per_trade=max_risk_per_trade,
            daily_loss_limit=daily_loss_limit,
            max_open_positions=max_open_positions,
            max_total_exposure=max_total_exposure,
        ),
    )


def test_allows_entry_within_limits():
    cfg = _cfg()
    gate = RiskGate(cfg)

    approved = gate.evaluate_entry(
        symbol="TEST",
        risk_amount=0.005,      # below 1%
        exposure_amount=0.05,   # below 30%
    )

    assert approved is True


def test_blocks_when_risk_per_trade_exceeded():
    cfg = _cfg(max_risk_per_trade=0.01)
    gate = RiskGate(cfg)

    approved = gate.evaluate_entry(
        symbol="TEST",
        risk_amount=0.02,       # exceeds 1%
        exposure_amount=0.05,
    )

    assert approved is False


def test_blocks_when_daily_loss_limit_reached():
    cfg = _cfg(daily_loss_limit=0.03)
    gate = RiskGate(cfg)
    gate.daily_loss = 0.03  # simulate hitting cap

    approved = gate.evaluate_entry(
        symbol="TEST",
        risk_amount=0.005,
        exposure_amount=0.05,
    )

    assert approved is False


def test_blocks_when_max_open_positions_reached():
    cfg = _cfg(max_open_positions=3)
    gate = RiskGate(cfg)
    gate.open_positions = 3  # at cap

    approved = gate.evaluate_entry(
        symbol="TEST",
        risk_amount=0.005,
        exposure_amount=0.05,
    )

    assert approved is False


def test_blocks_when_exposure_limit_exceeded():
    cfg = _cfg(max_total_exposure=0.30)
    gate = RiskGate(cfg)
    gate.total_exposure = 0.28  # near cap

    approved = gate.evaluate_entry(
        symbol="TEST",
        risk_amount=0.005,
        exposure_amount=0.05,  # would push above 0.30
    )

    assert approved is False
