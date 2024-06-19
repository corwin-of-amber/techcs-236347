Set Implicit Arguments. (* Allows us to use inference for dependent arguments *)

Require Import Reals.   (* Imports real arithmetic. *)
Notation Real := R.        (* Notice: due to the absence of overloading, all       *)
Delimit Scope R_scope   (* numerical constants and operators are nat-typed,     *)
  with Real.               (* unless stated otherwise via the scope delimiter '%'. *)

Check 3 + 4.            (* : ℕ  (nat)  *)
Check (3 + 4) % Real.      (* : ℝ  (Real) *)


Inductive Vec : nat -> Set :=
  VNil : Vec 0
| VCons : forall n, Real -> Vec n -> Vec (S n).

(* Some syntactic sugar *)
Notation "<< x , .. , y >>" := (VCons x .. (VCons y VNil) .. ).

Check << 5, 9, 6 >> .






(* For Q3 + Q4 *)

Fixpoint Vec' n : Set :=
  match n with
    0 => unit
  | S k => Real * Vec' k
  end.
