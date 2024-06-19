Set Implicit Arguments.


Inductive var := a | b | n | x | y.

Definition op := nat -> nat -> nat.
  
Inductive expr :=
  expr_var : var -> expr
| expr_num : nat -> expr
| expr_op : expr -> op -> expr -> expr.

Inductive cmd :=
  assign : var -> expr -> cmd
| seq : cmd -> cmd -> cmd
| skip : cmd
| if_then_else : expr -> cmd -> cmd -> cmd
| while : expr -> cmd -> cmd
| assume : expr -> cmd.

Definition state := var -> nat.

Fixpoint sem (e : expr) (s : state) :=
  match e with
  | expr_var v => s v
  | expr_num m => m
  | expr_op e1 op e2 => op (sem e1 s) (sem e2 s)
  end.


(* -- Defining the program `euclid` in IMP -- *)
Require Import Arith.
Import Nat.

(* some operators *)
Definition gt01 n m := if gt_dec n m then 1 else 0.
Definition ne01 n m := if eq_dec n m then 0 else 1.

(* This notation will shorten things a bit *)
Notation "$ v" := (expr_var v) (at level 7, format "$ v").

Definition euclid_body :=
    seq (assume (expr_op $a ne01 $b))
        (if_then_else (expr_op $a gt01 $b)
                      (assign a (expr_op $a sub $b))
                      (assign b (expr_op $b sub $a))).