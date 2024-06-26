import dipdup_indexer_dex_test_2.models as models
from dipdup_indexer_dex_test_2.types.quipu_fa2.tezos_storage import QuipuFa2Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOrigination


async def on_fa2_origination(
    ctx: HandlerContext,
    quipu_fa2_origination: TzktOrigination[QuipuFa2Storage],
) -> None:
    symbol = ctx.template_values['symbol']

    for address, value in quipu_fa2_origination.storage.storage.ledger.items():
        shares_qty = value.balance
        await models.Position(trader=address, symbol=symbol, shares_qty=shares_qty).save()