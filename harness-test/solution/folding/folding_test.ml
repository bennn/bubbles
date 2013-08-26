open Ocamltest

let test_reverse_empty () =
  assert_equal (Folding_sol.reverse []) (Folding.reverse [])
