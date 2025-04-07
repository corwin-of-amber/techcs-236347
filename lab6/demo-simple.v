Require Import Arith.
Require Import Lia.
Import Nat.


Load "/lib/hoare".


Definition gt01 n m := if gt_dec n m then 1 else 0.

Notation "[ e1 `+` e2 ]" := (expr_op e1 add e2).
Notation "[ e1 `*` e2 ]" := (expr_op e1 mul e2).
Notation "[ e1 `-` e2 ]" := (expr_op e1 sub e2).
Notation "[ e1 `>` e2 ]" := (expr_op e1 gt01 e2).

Notation "$ v" := (expr_var v) (at level 7, format "$ v").
Notation "# n" := (expr_num n) (at level 7, format "# n").


(*
x := y;
while i > 0 do
	x := x + 1;
	y := y + 1;
	i := i – 1
*)
Definition simple_cmd :=
  seq (assign x $y)
      (while [$n `>` #0]
             (seq (assign x [$x `+` #1])
                  (seq (assign y [$y `+` #1])
                       (assign n [$n `-` #1])))).

Module SmallExample.

  Definition c := (seq (assign x [$x `+` #1])
                       (seq (assign y [$y `+` #1])
                            (assign n [$n `-` #1]))).

  Definition inv (σ : state) := σ x = σ y.
  Lemma inv_preserved : hoare inv c inv.
  Proof.
    unfold c.
    econstructor.
    2: {
      econstructor.
      2: {
        econstructor.
      }
      unfold subst, inv.
      simpl. unfold set. simpl.
      econstructor.
    }
    unfold subst. simpl. unfold set. simpl.
    eapply hoare_weaken_l.
    2: {
      econstructor.
    }
    unfold subst, set, inv. simpl.
    lia.
  Qed.
  
  Lemma spec : hoare (fun _ => True) simple_cmd inv.
  Proof.
    econstructor.
    2: {
      eapply hoare_weaken_r.
      econstructor.
      eapply hoare_weaken_l.
      2: apply inv_preserved.
      - firstorder.
      - firstorder.
    }
    eapply hoare_weaken_l.
    2: econstructor.
    intros; unfold subst, set, inv. simpl. reflexivity.
  Qed.
  
End SmallExample.
