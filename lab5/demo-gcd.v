Set Implicit Arguments.
Require Import Arith.
Import Nat.

Require Import Lia.



  (* Definition of divisibility + some syntactic sugar *)
  Definition divides a b := exists k, a * k = b.
  Notation "( a | b )" := (divides a b).

  Lemma divides_refl : forall n, (n | n).
  Proof.
    exists 1. lia.
  Qed.


  Section Gcd.

    Definition state : Set := nat * nat.
  
    Inductive step : state -> state -> Prop :=
      step_a : forall a b, a > b -> step (a, b) (a - b, b)
    | step_b : forall a b, a < b -> step (a, b) (a, b - a).


		(* Off-the-shelf definition of tc *)
    Section ReflexiveTransitiveClosureDef.

      Variable D : Set.
      Variable R : D -> D -> Prop.

      Inductive tc : D -> D -> Prop :=
        tc_refl : forall s, tc s s
      | tc_step : forall s u t, tc s u -> R u t -> tc s t.

    End ReflexiveTransitiveClosureDef.


    Lemma gcd_positive a b a' b' :
    	a > 0 /\ b > 0 ->
    	tc step (a, b) (a', b') ->
    	a' > 0 /\ b' > 0.
    Proof.
    	intros [A B] H.
      induction H.
      (* Oops *)
    Abort.
    
    Definition inv (s : state) :=
    	let (a, b) := s in a > 0 /\ b > 0.
      
      
    Lemma gcd_positive s s' :
    	inv s -> tc step s s' -> inv s'.
    Proof.
    	intros I H.
      induction H.
      - assumption.
      - apply IHtc in I.
      	destruct H0.
        + unfold inv in *. lia.
        + unfold inv in *. lia.
   	Qed.
      
    
    (* Curious: you might be tempted to try the proof this way.
       However, it fails for some technical reasons.
    Lemma gcd_positive s s' a b a' b' :
    	s = (a,b) -> s' = (a',b') ->
      a > 0 /\ b > 0 ->
      tc step s s' ->
      a' > 0 /\ b' > 0.
    Proof.
    	intros S S' [A B] H.
      induction H.
      - subst. inversion S'. subst. split; assumption.
      - (oops)
    *)
    
    
    Lemma div_inv a b a' b' : step (a, b) (a', b') ->
            forall z,  (z | a) /\ (z | b)  <->  (z | a') /\ (z | b').
    Proof.
      intro H. inversion H.
      - subst. firstorder.
        + exists (x0 - x). rewrite mul_sub_distr_l. firstorder.
        + exists (x0 + x). rewrite mul_add_distr_l. lia.
      - subst. firstorder.
        + exists (x - x0). rewrite mul_sub_distr_l. firstorder. (*   firstorder also works, *)
        + exists (x0 + x). rewrite mul_add_distr_l. firstorder. (* <- when Lia is loaded  *)
    Qed.

  
    Definition is_gcd (a b z : nat) :=
      (z | a) /\ (z | b) /\ forall z', (z' | a) -> (z' | b) -> (z' | z).  


    Lemma gcd_inv a b a' b' : step (a, b) (a', b') ->
                              forall z, is_gcd a b z <-> is_gcd a' b' z.
    Proof.
      intro H. pose (div_inv H).
      firstorder.
      - apply H2; firstorder.
      - apply H2; firstorder.
    Qed.

    (* Lesson learned: *)
    (* `firstorder` is mighty powerful, if you know what *)
    (* assumptions to feed it. *)
  
  End Gcd.
