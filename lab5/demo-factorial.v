Set Implicit Arguments.
Require Import Arith.
Import Nat.

Require Import Lia.

(* From "Formal Reasoning About Programs"

   factorial(n) {
      a = 1;
      while (n > 0) {
         a = a * n;
         n = n - 1;
      }
      return a; 
   }
*)

Inductive state : Set :=
  InLoop: nat -> nat -> state      (* n, a *)
| Exit:   nat -> state.          (* a *)

Inductive init n0 : state -> Prop :=
  start : init n0 (InLoop n0 1).

Inductive step : state -> state -> Prop :=
  iter : forall n a, 0 < n -> 
    step (InLoop n a) (InLoop (n - 1) (a * n))
| stop : forall a, 
    step (InLoop 0 a) (Exit a).


(*
 * Specification -- program returns `fact n0`
 *  (where n0 is the input, i.e. initial value of n)
 *)
Definition spec n0 s :=
  match s with
    Exit a => a = fact n0
  | _ => True
  end.

Print fact.  (* `fact` is defined in the Arith library *)


(* General Definition *)
Section ReflexiveTransitiveClosureDef.

  Variable D : Set.
  Variable R : D -> D -> Prop.

  Inductive tc : D -> D -> Prop :=
    tc_refl : forall s, tc s s
  | tc_step : forall s u t, tc s u -> R u t -> tc s t.

End ReflexiveTransitiveClosureDef.
(* - Notice: from this point on, D and R become *arguments* of tc.
             D, however, is implicit. *)
Check tc.
Print Implicit tc.


Theorem spec_holds n0 s0 s :
  init n0 s0 -> tc step s0 s -> spec n0 s.
Proof.
  intros Init Reach.
  induction Reach.
  - destruct Init.
    simpl. trivial.
  - Fail apply IHReach.
(*🍉*)                (* stuck. :( *)   
Abort.  (* well, this didn't work. *)

(*
 * Invariant -- supposed to hold for all reachable states.
 *)
Definition inv n0 s :=
  match s with
    InLoop n a => a * fact n = fact n0
  | Exit a => a = fact n0
  end.

(* Note that this is strictly stronger than spec_holds. *)
Lemma inv_inv n0 s0 s : 
    init n0 s0 -> tc step s0 s -> inv n0 s.
Proof.
  intros Init Reach.
  induction Reach.
  - destruct Init.
    unfold inv. lia.
  - destruct H.
    + destruct n.
      * inversion H.
      * unfold inv. unfold inv in IHReach. 
        simpl. rewrite sub_0_r.
        rewrite <- mul_assoc. firstorder. (* apply IHReach. assumption. *)
    + simpl in *. firstorder. lia. (* apply IHReach in Init. omega. *)
(*🍇*)
Qed. (* nice *)

(* Now we can try the previous one again, it should be easy. *)
Theorem spec_holds n0 s0 s : 
    init n0 s0 -> tc step s0 s -> spec n0 s.
Proof.
  intros.
  enough (inv n0 s).
  - destruct s.
    + simpl. trivial.
    + simpl. simpl in H1.
      assumption.
  - apply inv_inv with s0.  (* `with` fills missing holes *)
    (* try also: `eapply inv_inv` instead *)
    + eassumption.
    + assumption.
Qed.
