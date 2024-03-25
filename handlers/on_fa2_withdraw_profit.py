from decimal import Decimal
from typing import Optional

import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.quipu_fa2.tezos_parameters.withdraw_profit import WithdrawProfitParameter
from dipdup_indexer_dex_test_2.types.quipu_fa2.tezos_storage import QuipuFa2Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOperationData
from dipdup.models.tezos_tzkt import TzktTransaction


async def on_fa2_withdraw_profit(
    ctx: HandlerContext,
    withdraw_profit: TzktTransaction[WithdrawProfitParameter, QuipuFa2Storage],
    transaction_0: TzktOperationData | None = None,
) -> None:
    symbol = ctx.template_values['symbol']
    trader = withdraw_profit.data.sender_address

    position, _ = await models.Position.get_or_create(trader=trader, symbol=symbol)

    if transaction_0:
        assert transaction_0.amount is not None
        position.realized_pl += Decimal(transaction_0.amount) / (10**6)

        await position.save()