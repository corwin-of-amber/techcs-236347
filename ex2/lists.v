Set Implicit Arguments.
Require Import Lists.List.
Import ListNotations.

Print list.
Print rev.


(* Q1. Define is_sorted.  (returns a Prop.)  *)


(* Q2. Show that this list is sorted. *)
Lemma warm_up : is_sorted [3;5;9] le.


(* Q3. Prove that an ascending list of nat, when reversed, 
 *     becomes a descending list. *)

Theorem rev_asc_desc : ...