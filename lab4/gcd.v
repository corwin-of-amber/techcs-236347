Set Implicit Arguments.

Require Import Arith.Arith.
Import Nat.

(* ----------------------------------------------------------------- *)
(* Let's start by proving some basic facts about natural numbers.    *)

(* this one is going to come in handy *)
Theorem f_equal : forall A B (f : A -> B) x y, x = y -> f x = f y.
Proof.
  intros. rewrite H. reflexivity.  (* First one's free. *)
Qed.                               (* Try to understand it though! *)

(* notice that "+" is not defined symmetrically! *)
Print Nat.add.
Eval simpl in fun x => 1 + x.
Eval simpl in fun x => x + 1.

Lemma plus_one : forall x, x + 1 = S x.

Lemma plus_one' : forall x y, x + S y = S x + y.

(* Definition of divisibility + some syntactic sugar *)
Definition divides a b := exists k, a * k = b.
Notation "( a | b )" := (divides a b).

(* commutativity lemmas. we're about to need them. *)
Check Nat.add_comm.
Check Nat.mul_comm.
  
Lemma divides_refl : forall n, (n | n).



(* ----------------------------------------------------------------- *)
(* Armed with these lemmas, let's try to define the Greatest Common  *)
(* Denominator and Euclid's algorithm.                               *)

Section Gcd.

  Definition is_gcd (a b z : nat) :=
    (z | a) /\ (z | b) /\ forall z', (z' | a) -> (z' | b) -> (z' | z).  

  (* First some basic properties of gcd *)
  Theorem is_gcd_refl : forall z, is_gcd z z z.

  Theorem is_gcd_comm : forall a b z, is_gcd a b z -> is_gcd b a z.

  
  (* -- this is a simplified version of Euclid -- *)
  Inductive gcd : nat -> nat -> nat -> Prop :=
    base : (forall z, gcd z z z)
  | step_a : forall a b z, gcd a b z -> gcd (a + b) b z
  | step_b : forall a b z, gcd a b z -> gcd a (a + b) z.

  
  (* distributivity lemmas. you will need them too! *)
  Check Nat.mul_add_distr_l.
  Check Nat.mul_sub_distr_l.

  Search (_ * (_ + _)).       (* this is how you could find them yourself *)
  Search (_ * (_ - _)).       (* if I hadn't told you *)

  Lemma gcd_step_aux : forall a b z, is_gcd a b z -> is_gcd (a + b) b z.
 
  Theorem gcd_pcorrect : forall a b z, gcd a b z -> is_gcd a b z.


End Gcd.
