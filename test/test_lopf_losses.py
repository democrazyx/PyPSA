# -*- coding: utf-8 -*-

import pytest
from conftest import optimize

SUPPORTED_APIS = ["pyomo", "native", "linopy"]


@pytest.mark.parametrize("api", SUPPORTED_APIS)
@pytest.mark.parametrize("transmission_losses", [1, 2])
def test_lopf_losses(scipy_network, api, transmission_losses):
    n = scipy_network
    n.lines.s_max_pu = 0.7
    n.lines.loc[["316", "527", "602"], "s_nom"] = 1715

    optimize(
        n,
        api,
        snapshots=n.snapshots[0],
        transmission_losses=transmission_losses,
    )

    gen = n.generators_t.p.iloc[0].sum() + n.storage_units_t.p.iloc[0].sum()
    dem = n.loads_t.p_set.iloc[0].sum()

    assert gen > 1.01 * dem, "For this example, losses should be greater than 1%"
    assert gen < 1.05 * dem, "For this example, losses should be lower than 5%"
