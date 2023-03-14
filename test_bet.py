from beaker import *
# from auction import Auction
from bet import Bet
from algosdk.dryrun_results import DryrunResponse
from algosdk import *
from algosdk.encoding import encode_address
from algosdk.atomic_transaction_composer import (
    TransactionWithSigner,
    AtomicTransactionComposer,
)
import pytest
from beaker.client.state_decode import decode_state

##########
# fixtures
##########


@pytest.fixture(scope="module")
def create_app():
    global accounts
    global creator_acct
    global app_client
    accounts = sorted(
        sandbox.get_accounts(),
        key=lambda a: sandbox.clients.get_algod_client().account_info(a.address)[
            "amount"
        ],
    )

    creator_acct = accounts.pop()

    app_client = client.ApplicationClient(
        client=sandbox.get_algod_client(),
        app=Bet(version=6),
        signer=creator_acct.signer,
    )

    app_client.create()

print("create_app() compiled")

@pytest.fixture(scope="module")
def start_bet():
    sp = app_client.get_suggested_params()

    axfer = TransactionWithSigner(
        txn=transaction.AssetTransferTxn(
            sender=creator_acct.address,
            receiver=app_client.app_addr,
            index=asa,
            amt=1,
            sp=sp,
        ),
        signer=creator_acct.signer,
    )

    app_client.call(
        Bet.start_bet, axfer=axfer, length=36_000
    )

print("start_bet() compiled")

# @pytest.fixture(scope="module")
# def send_first_bid():
#     global first_bidder
#     first_bidder = accounts.pop()

#     sp = app_client.get_suggested_params()

#     pay_txn = TransactionWithSigner(
#         txn=transaction.PaymentTxn(
#             sender=first_bidder.address, receiver=app_client.app_addr, amt=20_000, sp=sp
#         ),
#         signer=first_bidder.signer,
#     )

#     app_client.call(
#         Auction.bid,
#         payment=pay_txn,
#         previous_bidder=first_bidder.address,
#         signer=first_bidder.signer,
#     )


# @pytest.fixture(scope="module")
# def send_second_bid():
#     global second_bidder
#     global first_bidder_amount
#     second_bidder = accounts.pop()

#     sp = app_client.get_suggested_params()
#     sp.fee = sp.min_fee * 2
#     first_bidder_amount = app_client.client.account_info(first_bidder.address)["amount"]

#     pay_txn = TransactionWithSigner(
#         txn=transaction.PaymentTxn(
#             sender=second_bidder.address,
#             receiver=app_client.app_addr,
#             amt=30_000,
#             sp=sp,
#         ),
#         signer=second_bidder.signer,
#     )

#     app_client.call(
#         Auction.bid,
#         payment=pay_txn,
#         previous_bidder=first_bidder.address,
#         signer=second_bidder.signer,
#     )


# @pytest.fixture(scope="module")
# def end_auction():
#     sp = app_client.get_suggested_params()
#     sp.fee = sp.min_fee * 2

#     atc = AtomicTransactionComposer()

#     app_client.add_method_call(
#         atc=atc,
#         method=Auction.end_auction,
#         sender=creator_acct.address,
#         suggested_params=sp,
#         signer=creator_acct.signer,
#     )

#     dr_req = transaction.create_dryrun(
#         app_client.client,
#         atc.gather_signatures(),
#         latest_timestamp=2524608000,  # <- January 1, 2050
#     )
#     dr_res = DryrunResponse(app_client.client.dryrun(dr_req))
#     global global_delta

#     global_delta = decode_state(dr_res.txns[0].global_delta)


# @pytest.fixture(scope="module")
# def claim_bid():
#     sp = app_client.get_suggested_params()
#     sp.fee = sp.min_fee * 2
#     app_client.call(Auction.claim_bid, suggested_params=sp)




#     atc.execute(sandbox.get_algod_client(), 3)


# ##############
# # create tests
# ##############
#test

@pytest.mark.create
def test_create_pot(create_app):
    print("brug")
    assert app_client.get_application_state()["pot"] == 0

print("test_create_pot() compiled")


# @pytest.mark.create
# def test_create_highest_bid(create_app):
#     assert app_client.get_application_state()["highest_bid"] == 0


@pytest.mark.create
def test_create_bet_end(create_app):
    assert app_client.get_application_state()["bet_end"] == 0
print("test_create_bet_end() compiled")



# #####################
# # start_auction tests
# #####################


# @pytest.mark.start_auction
# def test_start_auction_end(create_app, opt_in, start_auction):
#     assert app_client.get_application_state()["auction_end"] != 0


# @pytest.mark.start_auction
# def test_start_auction_highest_bid(create_app, opt_in, start_auction):
#     assert app_client.get_application_state()["highest_bid"] == 10_000


# #################
# # first_bid tests
# #################


# @pytest.mark.first_bid
# def test_first_bid_highest_bid(create_app, opt_in, start_auction, send_first_bid):
#     assert app_client.get_application_state()["highest_bid"] == 20_000


# @pytest.mark.first_bid
# def test_first_bid_highest_bidder(create_app, opt_in, start_auction, send_first_bid):
#     addr = bytes.fromhex(app_client.get_application_state()["highest_bidder"])
#     assert encode_address(addr) == first_bidder.address


# ##################
# # second_bid tests
# ##################


# @pytest.mark.second_bid
# def test_second_bid_highest_bid(
#     create_app, opt_in, start_auction, send_first_bid, send_second_bid
# ):
#     assert app_client.get_application_state()["highest_bid"] == 30_000


# @pytest.mark.second_bid
# def test_second_bid_highest_bidder(
#     create_app, opt_in, start_auction, send_first_bid, send_second_bid
# ):
#     addr = bytes.fromhex(app_client.get_application_state()["highest_bidder"])
#     assert encode_address(addr) == second_bidder.address


# @pytest.mark.second_bid
# def test_second_bid_first_bidder_balance(
#     create_app, opt_in, start_auction, send_first_bid, send_second_bid
# ):
#     assert (
#         app_client.client.account_info(first_bidder.address)["amount"]
#         == first_bidder_amount + 20_000
#     )


# @pytest.mark.second_bid
# def test_second_bid_app_balance(
#     create_app, opt_in, start_auction, send_first_bid, send_second_bid
# ):
#     assert (
#         app_client.client.account_info(app_client.app_addr)["amount"]
#         == 30_000 + 200_000
#     )


# #################
# # claim_bid tests
# #################


# @pytest.mark.claim_bid
# def test_claim_bid(
#     create_app, opt_in, start_auction, send_first_bid, send_second_bid, claim_bid
# ):
#     pass
