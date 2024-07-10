Require Import Arith.Arith.
Import Nat.


Inductive euclid : nat -> nat -> nat -> Prop :=   (* copied from euclid.v *)
  stop    : forall z, euclid z z z
| step_a' : forall a b z, a > b -> euclid (a - b) b z -> euclid a b z
| step_b' : forall a b z, a < b -> euclid a (b - a) z -> euclid a b z.  


Theorem noether_max P :
  (forall a b, (forall a' b', max a' b' < max a b -> P a' b') -> P a b) ->
  forall a b, P a b.
(* I have a truly remarkable proof of this theorem which this file  *
 * is too small to contain.                                         *)
Admitted.

Theorem case_split_3way P : forall a b,
    (a < b -> P a b) -> (a = b -> P a b) -> (a > b -> P a b) -> P a b.
Proof.
  intros. destruct (lt_eq_lt_dec a b) as [[Hlt|Heq]|Hgt]; firstorder.
Qed.


Section PlayingWithTheBigBoysNow.
  
  (*
  Lemma max_decreases :  ???        <-----   fill this in and prove!!
  *)

  Theorem euclid_terminates : forall a b, a > 0 -> b > 0 -> exists z, euclid a b z.
  Proof.
    intros a b. apply noether_max with (a:=a) (b:=b).
    clear a b.
    intros a b IH apos bpos.
    apply case_split_3way with (a:=a) (b:=b); intro H.
    - destruct IH with (a':=a) (b':=b-a).     (* a < b *)
      (*  ???  *)
    - subst. eexists. constructor.            (* a = b *)
    - destruct IH with (a':=a-b) (b':=b).     (* a > b *)
      (*  ???  *)
  Qed.

End PlayingWithTheBigBoysNow.
