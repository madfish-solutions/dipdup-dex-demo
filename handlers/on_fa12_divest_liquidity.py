from decimal import Decimal

import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_parameters.transfer import TransferParameter
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_storage import Fa12TokenStorage
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_parameters.divest_liquidity import DivestLiquidityParameter
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_storage import QuipuFa12Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOperationData
from dipdup.models.tezos_tzkt import TzktTransaction


async def on_fa12_divest_liquidity(
    ctx: HandlerContext,
    divest_liquidity: TzktTransaction[DivestLiquidityParameter, QuipuFa12Storage],
    transfer: TzktTransaction[TransferParameter, Fa12TokenStorage],
    transaction_1: TzktOperationData,
) -> None:
    storage = divest_liquidity.storage

    decimals = int(ctx.template_values['decimals'])
    symbol = ctx.template_values['symbol']
    trader = divest_liquidity.data.sender_address

    position, _ = await models.Position.get_or_create(trader=trader, symbol=symbol)

    assert transaction_1.amount is not None
    tez_qty = Decimal(transaction_1.amount) / (10**6)
    token_qty = Decimal(transfer.parameter.value) / (10**decimals)
    shares_qty = int(divest_liquidity.parameter.shares)

    tez_pool = Decimal(storage.storage.tez_pool) / (10**6)
    token_pool = Decimal(storage.storage.token_pool) / (10**decimals)

    # NOTE: Empty pools mean exchange is not initialized yet
    if not tez_pool and not token_pool:
        return

    price = tez_pool / token_pool
    share_px = (tez_qty + price * token_qty) / shares_qty

    position.realized_pl += shares_qty * (share_px - position.avg_share_px)
    position.shares_qty -= shares_qty
    assert position.shares_qty >= 0, divest_liquidity.data.hash

    await position.save()