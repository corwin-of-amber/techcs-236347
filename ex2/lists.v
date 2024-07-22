Set Implicit Arguments.
Require Import Lists.List.
Import ListNotations.

Print list.
Print rev.


(* Q1. Define `is_sorted`.  (should return a Prop.)  *)


(* Show that this list is sorted. *)
Lemma warm_up : is_sorted [3;5;9] le.


(* Q2. Prove that an ascending list of nat, when reversed, 
 *     becomes a descending list. *)

(*     Don't forget to use the _hint_ when proving it. *)

Theorem rev_asc_desc : ...