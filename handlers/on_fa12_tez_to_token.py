from decimal import Decimal

import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_parameters.transfer import TransferParameter
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_storage import Fa12TokenStorage
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_parameters.tez_to_token_payment import TezToTokenPaymentParameter
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_storage import QuipuFa12Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktTransaction


async def on_fa12_tez_to_token(
    ctx: HandlerContext,
    tez_to_token_payment: TzktTransaction[TezToTokenPaymentParameter, QuipuFa12Storage],
    transfer: TzktTransaction[TransferParameter, Fa12TokenStorage],
) -> None:
    decimals = int(ctx.template_values['decimals'])
    symbol = ctx.template_values['symbol']
    trader = tez_to_token_payment.data.sender_address

    min_token_quantity = Decimal(tez_to_token_payment.parameter.min_out) / (10**decimals)
    token_quantity = Decimal(transfer.parameter.value) / (10**decimals)
    assert tez_to_token_payment.data.amount is not None
    tez_quantity = Decimal(tez_to_token_payment.data.amount) / (10**6)
    if min_token_quantity > token_quantity:
        ctx.logger.warning('output is lower than `min_out` (%s > %s)', min_token_quantity, token_quantity)
        return

    trade = models.Trade(
        symbol=symbol,
        trader=trader,
        side=models.TradeSide.BUY,
        quantity=token_quantity,
        price=token_quantity / tez_quantity,
        slippage=(1 - (min_token_quantity / token_quantity)).quantize(Decimal('0.000001')),
        level=transfer.data.level,
        timestamp=transfer.data.timestamp,
        hash=transfer.data.hash,
    )
    await trade.save()