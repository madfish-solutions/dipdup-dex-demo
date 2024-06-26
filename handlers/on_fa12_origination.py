import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.quipu_fa12.tezos_storage import QuipuFa12Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOrigination


async def on_fa12_origination(
    ctx: HandlerContext,
    quipu_fa12_origination: TzktOrigination[QuipuFa12Storage],
) -> None:
    symbol = ctx.template_values['symbol']

    for address, value in quipu_fa12_origination.storage.storage.ledger.items():
        shares_qty = value.balance
        await models.Position(trader=address, symbol=symbol, shares_qty=shares_qty).save()