open Ocamltest

let test_true_pass () =
  assert_true true

let test_false_pass () =
  assert_false false

let test_greater_pass () =
  assert_greater 4 3

let test_less_pass () =
  assert_less "zardoz" "zeddycakes"

let test_equal_pass () = 
  assert_equal 42.0 42.0

let test_not_equal_pass () =
  assert_not_equal "r" "s"

let test_is_pass () =
  assert_is 42 42

let test_is_not_pass () =
  assert_is_not 1.0 1.0

let test_is_none_pass () = 
  assert_is_none None

let test_is_not_none_pass () =
  assert_is_not_none (Some 'x')

let test_assert_raises_pass () =
  assert_raises (lazy (1/0)) Division_by_zero
