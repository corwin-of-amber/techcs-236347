Require Import Nat.

Section EO.

  Inductive even : nat -> Prop :=
  | even_O : even 0
  | even_S : forall n, odd n -> even (S n)
  with odd : nat -> Prop :=
     | odd_S : forall n, even n -> odd (S n).

  Compute is_even 8.
    
  Fixpoint is_even n :=
    match n with
      0 => True
    | S 0 => False
    | S (S k) => is_even k
    end.

End EO.
