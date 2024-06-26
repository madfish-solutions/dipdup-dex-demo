from decimal import Decimal

import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_parameters.transfer import TransferParameter
from dipdup_indexer_dex_test_2.types.fa12_token.tezos_storage import Fa12TokenStorage
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_parameters.token_to_tez_payment import TokenToTezPaymentParameter
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_storage import QuipuFa12Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOperationData
from dipdup.models.tezos_tzkt import TzktTransaction


async def on_fa12_token_to_tez(
    ctx: HandlerContext,
    token_to_tez_payment: TzktTransaction[TokenToTezPaymentParameter, QuipuFa12Storage],
    transfer: TzktTransaction[TransferParameter, Fa12TokenStorage],
    transaction_0: TzktOperationData,
) -> None:
    decimals = int(ctx.template_values['decimals'])
    symbol = ctx.template_values['symbol']
    trader = token_to_tez_payment.data.sender_address

    min_tez_quantity = Decimal(token_to_tez_payment.parameter.min_out) / (10**6)
    token_quantity = Decimal(token_to_tez_payment.parameter.amount) / (10**decimals)
    assert transaction_0.amount is not None
    tez_quantity = Decimal(transaction_0.amount) / (10**6)
    assert min_tez_quantity <= tez_quantity, f'{min_tez_quantity} >= {tez_quantity} {transaction_0.hash}'

    trade = models.Trade(
        symbol=symbol,
        trader=trader,
        side=models.TradeSide.SELL,
        quantity=token_quantity,
        price=token_quantity / tez_quantity,
        slippage=(1 - (min_tez_quantity / tez_quantity)).quantize(Decimal('0.000001')),
        level=transfer.data.level,
        timestamp=transfer.data.timestamp,
        hash=transfer.data.hash,
    )
    await trade.save()