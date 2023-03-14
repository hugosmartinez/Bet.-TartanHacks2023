#!/usr/bin/env python3
from pyteal import *
from beaker import *
import os
import json
from typing import Final

# from beaker import Application, ApplicationStateValue, Authorize, consts, external
from beaker.application import get_method_signature
from beaker.lib.storage import Mapping, List

# Use a box per better to denote amount and side
class BetRecord(abi.NamedTuple):
    bet_amount: abi.Field[abi.Uint64]
    voted: abi.Field[abi.Bool]

class Bet(Application):
    bet_and_amount = Mapping(abi.Address, BetRecord)
    # bet_address = Mapping(abi.DynamicBytes, abi.Uint64)
    # bet_amount = Mapping(abi.DynamicBytes, abi.Uint64)

    bet_end: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Timestamp of the end of the bet",
    )

    pot: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Total amount of money being collected",
    )

    bet_id: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="ID of the bet happening",
    )

    truers: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number of people voting true",
    )

    falsers: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number of people voting false",
    )

    @create
    def create(self):
        # Set all global state to the default values
        return self.initialize_application_state()

    @external(authorize=Authorize.only(Global.creator_address()))
    def start_bet(
        self,
        length: abi.Uint64,
        axfer: abi.PaymentTransaction,
    ):
        return Seq(
            # Ensure the betting hasn't already been started
            Assert(self.bet_end.get() == Int(0)),
            # Verify axfer
            Assert(
                axfer.get().receiver() == Global.current_application_address() #???
            ),
            Assert(axfer.get().tx_id() == self.bet_id.get()), #???
            # Set global state
            self.pot.set(axfer.get().amount()),
            self.bet_end.set(Global.latest_timestamp() + length.get()),
        )

    @internal(TealType.none)
    def pay(self, receiver: Expr, amount: Expr):
        return InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: receiver,
                TxnField.amount: amount,
                TxnField.fee: Int(0),  # cover fee with outer txn
            }
        )

    @external
    def make_bet(self, payment: abi.PaymentTransaction):
        return Seq(
            # Ensure betting hasn't ended
            Assert(Global.latest_timestamp() < self.bet_end.get()),
            
            # Verify payment transaction
            Assert(Txn.sender() == payment.get().sender()),

            # Set global state
            self.pot.set(self.pot.get() + payment.get().amount()), 

            (bet_amount := abi.Uint64()).set(Int(0)),
            (voted := abi.Bool()).set(consts.FALSE),
            (br := BetRecord()).set(bet_amount, voted),
            self.bet_and_amount[Txn.sender()].set(br),
            
            (decoded := BetRecord()).decode(self.bet_and_amount[Txn.sender()].get()),
            (bools:= abi.Bool()).set(decoded.voted),
            (false:= abi.Bool()).set(consts.FALSE),
            (true:= abi.Bool()).set(consts.TRUE),
            If(
                bools.get() == true.get(),
                self.truers.set(self.truers.get() + Int(1)),
            ),
            If(
                bools.get() == false.get(),
                self.falsers.set(self.falsers.get() + Int(1)),
            ),
        )

    @external
    def claim_pot(
        self, asset: abi.Asset): #abi.Address

        return Seq(
            # Send bet to better
            (decoded := BetRecord()).decode(self.bet_and_amount[Txn.sender()].get()),
            (bools:= abi.Bool()).set(decoded.voted),

            (bet_amount:= abi.Uint64()).set(decoded.bet_amount),

            (false:= abi.Bool()).set(consts.FALSE),
            (true:= abi.Bool()).set(consts.TRUE),
            
            If(
                bools.get() == true.get(),
                InnerTxnBuilder.Execute(
                    {
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.fee: Int(0),  # cover fee with outer txn
                        TxnField.amount: bet_amount.get(),
                        TxnField.receiver: Txn.sender(),
                    }
                ),
            ),

            If(
                bools.get() == false.get(),
                InnerTxnBuilder.Execute(
                    {
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.fee: Int(0),  # cover fee with outer txn
                        TxnField.amount: bet_amount.get(),
                        TxnField.receiver: Txn.sender(),
                    }
                ),
            ),

        )



if __name__ == "__main__":
    app = Bet(version=8)

    if os.path.exists("approval.teal"):
        os.remove("approval.teal")

    if os.path.exists("approval.teal"):
        os.remove("clear.teal")

    if os.path.exists("abi.json"):
        os.remove("abi.json")

    if os.path.exists("app_spec.json"):
        os.remove("app_spec.json")

    with open("approval.teal", "w") as f:
        f.write(app.approval_program)

    with open("clear.teal", "w") as f:
        f.write(app.clear_program)

    with open("abi.json", "w") as f:
        f.write(json.dumps(app.contract.dictify(), indent=4))

    with open("app_spec.json", "w") as f:
        f.write(json.dumps(app.application_spec(), indent=4))