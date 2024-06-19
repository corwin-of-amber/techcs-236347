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
| while : expr -> cmd -> cmd.

Definition state := var -> nat.

Fixpoint sem (e : expr) (s : state) :=
  match e with
  | expr_var v => s v
  | expr_num m => m
  | expr_op e1 op e2 => op (sem e1 s) (sem e2 s)
  end.


Definition assertion := state -> Prop.

Definition var_eq_dec : forall v1 v2 : var, {v1 = v2} + {v1 <> v2}.
Proof.
  destruct v1, v2;  (left; reflexivity) || (right; discriminate 1).
Defined.
  
Definition set (s : state) (v : var) (z : nat) :=
  fun v' => if var_eq_dec v v' then z else s v'.

(* subst P v e  ===  P[e/v] *)
Definition subst (P : assertion) v e :=
  fun s : state => P (set s v (sem e s)).

Inductive hoare : assertion -> cmd -> assertion -> Prop :=
  hoare_assign : forall (v : var) (e : expr) (Q : assertion),
    hoare (subst Q v e) (assign v e) Q
| hoare_seq : forall c1 c2 P M Q,
    hoare P c1 M -> hoare M c2 Q -> hoare P (seq c1 c2) Q
| hoare_if : forall e c1 c2 P Q,
    hoare (fun s => P s /\ sem e s <> 0) c1 Q ->
    hoare (fun s => P s /\ sem e s = 0) c2 Q ->
    hoare P (if_then_else e c1 c2) Q
| hoare_while : forall e c P,
    hoare (fun s => P s /\ sem e s <> 0) c P ->
    hoare P (while e c) (fun s => P s /\ sem e s = 0)
| hoare_weaken : forall (P' P : assertion) c (Q Q' : assertion),
    (forall s, P' s -> P s) ->
    hoare P c Q ->
    (forall s, Q s -> Q' s) ->
    hoare P' c Q'.


(* weaken left:                      *)
(*                                   *)
(*        P' => P   {P} c {Q}        *)
(*     -------------------------     *)
(*            {P'} c {Q}             *)
(*                                   *)
Corollary hoare_weaken_l : forall (P' P : assertion) c (Q : assertion),
    (forall s, P' s -> P s) -> hoare P c Q -> hoare P' c Q.
Proof.
  intros; eapply hoare_weaken.
  - eassumption.
  - eassumption.
  - firstorder.
Qed.

(* weaken right:                     *)
(*                                   *)
(*        {P} c {Q}   Q => Q'        *)
(*     -------------------------     *)
(*            {P} c {Q'}             *)
(*                                   *)
Corollary hoare_weaken_r : forall (P : assertion) c (Q Q' : assertion),
    hoare P c Q -> (forall s, Q s -> Q' s) -> hoare P c Q'.
Proof.
  intros; eapply hoare_weaken.
  - intros. eassumption.
  - eassumption.
  - assumption.
Qed.

(* weaken + seq:                                      *)
(*                                                    *)
(*      {P1} c1 {Q1}   Q1 => P2   {P2} c2 {Q2}        *)
(*     ----------------------------------------       *)
(*                 {P1} c1;c2 {Q2}                    *)
(*                                                    *)
Lemma hoare_seq_weaken P1 c1 Q1 P2 c2 Q2 :
  hoare P1 c1 Q1 -> hoare P2 c2 Q2 -> (forall s, Q1 s -> P2 s) ->
  hoare P1 (seq c1 c2) Q2.
Proof.
  intros. econstructor.
  - eassumption.
  - eapply hoare_weaken.
    + eassumption.
    + eassumption.
    + intros; assumption.
Qed.


