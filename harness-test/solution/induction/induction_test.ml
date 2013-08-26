open Ocamltest

let test_proofs () =
  assert_equal (Induction_sol.induct ()) (Induction.induct ())
