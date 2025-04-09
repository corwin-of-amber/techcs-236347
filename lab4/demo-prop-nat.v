Set Implicit Arguments.

Section Propositional.

  Variables A B C D : Prop.
  
  Definition modpon1 : (A -> B) -> A -> B := fun x => x. (*🍎*)
  
  Definition modpon2 : A -> (A -> B) -> B := fun x f => f x. (*🍏*)
  
  Locate "/\ ".
  Print and.
  (*
  Inductive and (A B : Prop) : Prop :=
    conj : A -> B -> A /\ B
  *)
  
  Definition modpon3 : A /\ (A -> B) -> B := fun xf => (*🍐*)
    match xf with 
      conj x f => f x
    end.
    
  Locate "\/".
  Print or.
  (*
  Inductive or (A B : Prop) : Prop :=
    or_introl : A -> A \/ B 
  | or_intror : B -> A \/ B
  *)
    
  Definition and_or : A /\ B -> A \/ B := fun ab => (*🍋*)
    match ab with
      conj a b => or_introl a
    end.
    
  Definition either_or : (C -> C \/ D) /\ (D -> C \/ D) :=  (*🍉*)
    conj (@or_introl C D) (@or_intror C D).
    
  Lemma either_or' : (C -> C \/ D) /\ (D -> C \/ D).
  Proof. (*🍇*)
    apply conj.
    - apply or_introl.
    - apply or_intror.
  Qed.
  
  Lemma either_or'' : (C -> C \/ D) /\ (D -> C \/ D).
  Proof. (*🍌*)
    split.
    - intro. left. assumption.
    - intro. right. assumption.
  Qed.
  
    
End Propositional.


Section Naturals.

  Locate "<=".
  Print le.
  (*
  Inductive le (n : nat) : nat -> Prop :=
    le_n : n <= n
  | le_S : forall m : nat, n <= m -> n <= S m
  *)
  Check le.
  
  Definition nonneg_2 : 0 <= 2 :=
      le_S 0 1 (le_S 0 0 (le_n 0)).
  
  Lemma nonneg_2' : 0 <= 2.
  Proof. (*🍅*)
    repeat constructor.
  Qed.
  
  (*
  Inductive le (n : nat) : nat -> Prop :=
    le_n : n <= n
  | le_S : forall m : nat, n <= m -> n <= S m
  *)

  Fixpoint le_0 n : 0 <= n :=  (*🍆*)
    match n with
    | 0 => le_n 0
    | S k => le_S 0 k (le_0 k)
    end.
    
  Lemma le_0' : forall n, 0 <= n.
  Proof. (*🌽*)
    induction n.
    - apply le_n.
    - apply le_S. apply IHn.
  Qed.
  
  Locate "exists".
  Print ex.
  (*
  Inductive ex (A : Type) (P : A -> Prop) : Prop :=
    ex_intro : forall x : A, P x -> exists y, P y
  *)
    
  Definition base : forall n, n = 0 \/ exists k, n = 1 + k :=  (*🍩*)
    fun n => match n with
      0 => or_introl (eq_refl 0)
    | S k => or_intror (ex_intro 
               (fun k0 => S k = 1 + k0) 
               k 
               (eq_refl (S k)) )
    end.
    
  Lemma base' : forall n, n = 0 \/ exists k, n = 1 + k.
  Proof. (*🍭*)
    intro n.
    destruct n.
    - left. apply eq_refl.
    - right. exists n. reflexivity.
  Qed.
    
  Locate "+".
  Print Nat.add.
  (*
  Fixpoint add (n m : nat) : nat :=
    match n with
    | 0 => m
    | S p => S (add p m)
    end
  *)
  
  Variable n : nat.
  
  Eval cbn in 0 + n.
  Eval cbn in n + 0.
  
  Lemma plus_0_n : 0 + n = n.
  Proof. (*☕️*)
    reflexivity.
  Qed.
  
  Lemma plus_n_0 : n + 0 = n.
  Proof. (*🍺*)
    induction n.
    - simpl. reflexivity.
    - simpl. rewrite IHn0. reflexivity.
  Qed.
  
  
  
End Naturals.



Theorem f_equal : forall A B (f : A -> B) x y, x = y -> f x = f y.
Proof.
  intros. rewrite H. reflexivity.
Qed.


Lemma fsample1 : forall m n, m * (S n) = m * (1 + n).
Proof.
  intros.
  apply f_equal.
  reflexivity.
Qed.

Require Import PeanoNat.
Import Nat.

Lemma fsample2 : forall m n, m * (S n) = m * (n + 1).
Proof.
  intros.
  apply f_equal.
  (* reflexivity does not work *)
  rewrite add_1_r. reflexivity.
Qed.

