open Ocamltest
open Folding
open Folding_sol

let test_reverse_empty () =
  assert_equal (Folding_sol.reverse []) (Folding.reverse [])

let test_sum_naive () =
  let xs = [1] in
  assert_equal (Folding_sol.sum xs) (Folding.sum xs)

let test_zardoz () =
  let a = Folding_sol.zardoz () in
  let b = Folding.zardoz () in
  Printf.printf "A = %d, B = %d\n" a b;
  assert_equal a b  
