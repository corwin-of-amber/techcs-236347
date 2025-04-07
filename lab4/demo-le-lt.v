Set Implicit Arguments.
Import Nat.


  Inductive le : nat -> nat -> Prop :=
    le_n : forall n, le n n
  | le_S : forall m n, le m n -> le m (S n).

  Notation "m <= n" := (le m n).
  
  Definition le0 : forall n, 0 <= n :=
    fix h n :=
      match n with
        0 => le_n 0
      | S k => le_S (h k)
      end.

  Fixpoint le0' n : 0 <= n :=
    match n with
      0 => le_n 0
    | S k => le_S (le0' k)
    end.

  Lemma le0'' : forall n, 0 <= n.
  Proof.
    induction n.
    - constructor.
    - constructor. assumption.
  Qed.

  Lemma le1 : forall n, 1 <= S n.
  Proof.
    induction n.
    - constructor.
    - constructor. assumption.
  Qed.

  Definition lt m n := le (S m) n.
  Notation "m < n" := (lt m n).

  Lemma lt0 : forall n, n = 0 \/ 0 < n.
  Proof.
    induction n.
    - left. reflexivity.
    - right.  (* at this point, we could finish with `apply le1` *)
      induction n.
      + constructor.
      + constructor. induction IHn.
        * discriminate H.
        * assumption.
  Qed.
  


  Theorem f_equal : forall A B (f : A -> B) x y, x = y -> f x = f y.
  Proof.
    intros. rewrite H. reflexivity.
  Qed.
