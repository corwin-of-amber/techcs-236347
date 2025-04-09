Set Implicit Arguments.
Import Nat.


  Inductive even : nat -> Prop :=
    even_0 : even 0
  | even_SS : forall n, even n -> even (S (S n)).

  Inductive odd : nat -> Prop :=
    odd_1 : odd 1
  | odd_SS : forall n, odd n -> odd (S (S n)).


  Require Import Wf_nat.

  Check lt_wf_ind.
  
  Lemma better_together n : even n \/ odd n.
  Proof.
    induction n using lt_wf_ind.
    destruct n.
    - left; constructor. (* admit. *)
    - destruct n.
      + right; constructor. (* admit. *)
      + destruct H with (m:=n).
        * constructor. constructor.
        * left. constructor. assumption.
        * right. constructor. assumption.
          (* == using existentials == *
      + edestruct H. Focus 2.
        * left. constructor. eassumption.
        * repeat constructor.
        * right. constructor. assumption.
        *)
  Qed.

  Lemma better_separate n : ~ (even n /\ odd n).
  Proof.
    induction n using lt_wf_ind.
    destruct n.
    - intros [_ O]. inversion O.
    - destruct n.
      + intros [E _]. inversion E.
      + intros [E O].
        apply H with (m:=n).
        * repeat constructor.
        * inversion E. inversion O. firstorder.
  Qed.
